#include <stdio.h>

#include "embedded_files.h"

int main()
{
  size_t size = 0;
  const char* buffer = 0;
  
  if (open_embedded_file("file2c.py", &size, &buffer) == 0)
    printf("file2c.py: size %ld, first 3 bytes: '%c%c%c', last 3 bytes: '%c%c%c'",
        size, buffer[0], buffer[1], buffer[2],
        buffer[size-3], buffer[size-2], buffer[size-1]);
  if (open_embedded_file("files2c.py", &size, &buffer) == 0)
    printf("files2c.py: size %ld, first 3 bytes: '%c%c%c', last 3 bytes: '%c%c%c'",
        size, buffer[0], buffer[1], buffer[2],
        buffer[size-3], buffer[size-2], buffer[size-1]);



  return 0;
}
