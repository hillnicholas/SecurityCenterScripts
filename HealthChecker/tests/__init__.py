import os, re

files = os.listdir( os.path.dirname(__file__) )
files = list(filter( lambda f: re.search(".*\.py$", f ), files ) )
files.remove("__init__.py")
files = list(map( lambda f: f[:len(f)-3], files ))
__all__ = files

