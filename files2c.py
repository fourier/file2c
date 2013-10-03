#!/usr/bin/python

###########################################################
# binary files to c converter
# Copyright (c) Alexey Veretennikov 2013
###########################################################

from __future__ import with_statement
from sys import argv,exit
from os import path
from string import Template

BUFFER_SIZE = 12
EXPORT_HEADER_NAME = "embedded_files.h"
EXPORT_SOURCE_NAME = "embedded_files.c"

HEADER_CONTENT="""/*********************************************************/
/* Generated by files2c.py (c) Alexey Veretennikov 2013  */
/* This is automatically generated file, do not modify!  */
/*********************************************************/
#ifndef _EMBEDDED_FILES_H_
#define _EMBEDDED_FILES_H_

/*
 * files included:
 * $files
 */

#include <stddef.h>
 
/**
 * Retrieves a pointer to the embedded file.
 * @param file_name Name of the embedded file
 * @param size the size of embedded file
 * @param contents_ptr the pointer to the file's contents
 * @return 0 if ok, -1 otherwise
 */
int open_embedded_file(/*[in]*/const char *file_name, /*[out]*/size_t* size, /*[out]*/const char** contents_ptr);

#endif
"""


SOURCE_CONTENT="""/*********************************************************/
/* Generated by files2c.py (c) Alexey Veretennikov 2013  */
/* This is automatically generated file, do not modify!  */
/*********************************************************/

#include \"embedded_files.h\"
#include \"string.h\"

$files_data

int open_embedded_file(/*[in]*/const char *file_name, /*[out]*/size_t* size, /*[out]*/const char** contents_ptr)
{
$files_table
  return -1;
}
"""
TABLE_HEADER="""  static const struct
  {
    const char* name;
    size_t len;
    const char* ptr;
  } files_table [] =
  {
"""
TABLE_FOOTER="""    {0,0,0}
  };
  int i = 0;
  while( files_table[i].name)
  {
    if (!strcmp(files_table[i].name, file_name))
    {
      *size = files_table[i].len;
      *contents_ptr = files_table[i].ptr;
      return 0;
    }
    ++i;
  }
"""
TABLE_ENTRY_CONTENT="    {\"$fname\", $sv, $bv},\n"
def read_file(filename, chunksize=BUFFER_SIZE):
  with open(filename, "rb") as f:
    while True:
      chunk = f.read(chunksize)
      if chunk:
        yield chunk
      else:
        break

def bytes_variable(fname):
  return path.basename(fname).replace(".","_")
def size_variable(fname):
  return path.basename(fname).replace(".","_") + "_len"


def process_file(fname):
  size = 0
  bv = bytes_variable(fname)
  sv = size_variable(fname)
  content = "#ifdef __ICCARM__\n#pragma data_alignment=8\n#endif\n"
  content += "const char %s[] = {\n" % bv
  for bytes in read_file(fname):
    content += "  "
    size = size + len(bytes)
    if len(bytes) == BUFFER_SIZE:
      content += ", ".join(map(lambda x: ("0x%02x" % x), (ord(i) for i in bytes))) + ",\n"
    else:                             # last bytes
      content += ", ".join("0x%02x" % ord(i) for i in bytes)
      content += "\n"
  content += "};\n"
  content += "const size_t %s = %d;\n" % (size_variable(fname), size)
  return (fname, bv, sv, content)

def create_header(file_list):
  print("Generating header")
  content = Template(HEADER_CONTENT).substitute(files="\n * ".join(file_list))
  with open(EXPORT_HEADER_NAME, "wt+") as f:
    f.write(content)
    
def create_source(file_list):
  print("Generating source")
  generated = map(process_file, file_list)
  files_data = "\n".join(map(lambda x: x[3],generated))
  files_table = TABLE_HEADER + "".join(map(lambda x: Template(TABLE_ENTRY_CONTENT).substitute(fname=x[0], bv=x[1], sv=x[2]), generated)) + TABLE_FOOTER
  content = Template(SOURCE_CONTENT).substitute(files_data=files_data, files_table=files_table)
  with open(EXPORT_SOURCE_NAME, "wt+") as f:
    f.write(content)
    
if len(argv) < 2:
  print("Binary to C converter.")
  print("(c) Alexey Veretennikov<alexey dot veretennikov at gmail dot com>, 2013"
  print("Syntax: %s file1 [file2 file3 ... file]" % argv[0])
  print("Generates the %s and %s in the current directory" % (EXPORT_HEADER_NAME, EXPORT_SOURCE_NAME))
else:
  file_list = []
  for fname in argv[1:]:
    if not path.isfile(fname):
      print("%s is not a file" % fname)
    else:
      file_list.append(path.normpath(fname))
  if len(file_list):
    create_header(file_list)
    create_source(file_list)
