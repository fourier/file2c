#!/usr/bin/python

###########################################################
# binary files to c converter
# Copyright (c) Alexey Veretennikov 2013
###########################################################


from __future__ import with_statement
from sys import argv,exit
from os import path

BUFFER_SIZE = 12

def read_file(filename, chunksize=BUFFER_SIZE):
  with open(filename, "rb") as f:
    while True:
      chunk = f.read(chunksize)
      if chunk:
        yield chunk
      else:
        break

def output_filename(fname):
  return path.basename(fname).replace(".","_") + ".c"

def bytes_variable(fname):
  return path.basename(fname).replace(".","_")
def size_variable(fname):
  return path.basename(fname).replace(".","_") + "_len"


def process_path(fname):
  output_fname = output_filename(fname)
  print("Output to file %s" % output_fname)
  size = 0
  with open(output_fname, "wt+") as f:
    f.write("#ifdef __ICCARM__\n#pragma data_alignment=8\n#endif\n")
    f.write("const char %s[] = {\n" % bytes_variable(fname))
    for bytes in read_file(fname):
      f.write("  ")
      size = size + len(bytes)
      if len(bytes) == BUFFER_SIZE:  
        map(lambda x: f.write("0x%02x, " % x), (ord(i) for i in bytes))
      else:                             # last bytes
        f.write( ", ".join("0x%02x" % ord(i) for i in bytes))
      f.write("\n")
    f.write("};\n")
    f.write("const int %s = %d;\n" % (size_variable(fname), size))

if len(argv) < 2:
  print("Syntax: %s path" % argv[0])
else:
  print("Processing %s" % argv[1])
  if not path.isfile(argv[1]):
    print("%s is not a file" % argv[1])
  else:
    process_path(path.normpath(argv[1]))
