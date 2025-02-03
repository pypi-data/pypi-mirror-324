import os
import re
from pathlib import Path
import argparse

CWD = Path(os.getcwd())
def readlines(p:Path):
  with p.open() as f:return f.readlines()
def is_pragma_once(line: str)->bool:return re.match(r"^\s*#\s*pragma\s+once\s*$",line) is not None
def remove_comment(line:str)->str:return line[:line.find('//')].rstrip()
def bundle(src:str,include_paths:list[str]=None)->str:
  if include_paths is None:include_paths=[]
  include_paths=[Path(p) for p in include_paths]
  src=Path(src)
  is_once = set()
  edges = set()
  def expand(file:Path)->str:
    file=file.resolve()
    dir=file.parent
    def included_file(line:str)->Path|None:
      m = re.match(r"^\s*#\s*include\s*\"(.+)\"\s*$",line)
      if m is None:return None
      header = m.groups()[0]
      file=(dir/header).resolve()
      if file.exists():return file
      for d in include_paths:
        file = (d/header).resolve()
        if file.exists():return file
      return None
    lines=[]
    for line in readlines(file):
      line=remove_comment(line)
      if line=='':continue
      if is_pragma_once(line):
        is_once.add(file)
        continue
      dep = included_file(line)
      if dep is None:
        lines.append(line)
        continue
      if dep in is_once: continue
      e = (file, dep)
      if e in edges: raise "circular includes"
      edges.add(e)
      lines.append(expand(dep))
      edges.remove(e)
    return '\n'.join(lines)
  return expand(src)

def cli():
  parser = argparse.ArgumentParser()
  parser.add_argument("-I",type=str,action="append",metavar="include_path",default=[CWD],dest="include_paths")
  parser.add_argument("src",type=str,help="e.g. main.cpp")
  args = parser.parse_args()
  print(bundle(args.src,args.include_paths))

if __name__ == "__main__":
  cli()
