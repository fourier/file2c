File2C converter
================

This simple tool converts a set of files to C source code, providing a lookup-function to get a pointer and a size. Similar tools are *xxd* and *bin2c*.

Usage:
------
<pre>
python file2c.py filename.ext
</pre>
generates the file **filename_ext.c**
<pre>
python files2c.py file1 [file2 file3...]
</pre>
generates files **embedded_files.h** and **embedded_files.c**
The **files2c.py** creates the lookup function:
```c
int open_embedded_file(/*[in]*/const char *file_name, /*[out]*/size_t* size, /*[out]*/const char** contents_ptr);
```
which can be used to get the pointer to the embedded file and its size by given  name of the embedded file. See *example.c* for the usage example

----
*Copyright (c) 2013 Alexey Veretennikov <alexey dot veretennikov at gmail dot com>*
