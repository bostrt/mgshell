#define _GNU_SOURCE

#include <sys/stat.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main() {
  char *cwd = get_current_dir_name();
  struct stat sb;
  // Continue searching to root
  while (strcmp(cwd, "/") != 0) {
    // Stat for .mgshell in current directory
    if (stat(".mgshell", &sb) == 0) {
      free(cwd);
      // Found it!
      return 0;
    }
    // Haven't found it yet, keep going up.
    chdir("..");
    cwd = get_current_dir_name();
  }

  // Give up.
  free(cwd);
  return -1;
}
