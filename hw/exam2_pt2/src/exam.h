// Don't change this file!
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

// Don't change this file!
#undef printf
#undef puts
#undef putchar
#undef fork
extern int __real_puts(const char* str);
extern int __real_putchar(const char str);
extern int __real_fork();
int __wrap_printf(const char *format, ...){
  // https://stackoverflow.com/questions/205529/passing-variable-number-of-arguments-around
  va_list argptr;
  va_start(argptr,format);
  int result = vprintf(format, argptr);
  //vprintf("Hello from printf\n", argptr);
  va_end(argptr);
  fflush(stdout);
  return result;
}

int __wrap_puts(const char* str){
  int result = __real_puts(str);
  //__real_puts("Hello from puts\n");
  fflush(stdout);
  return result;
}

int __wrap_putchar(const char str){
  int result = __real_putchar(str);
  //__real_puts("Hello from putchar\n");
  fflush(stdout);
  return result;
}

int __wrap_fork(){
  fflush(stdout);
  return __real_fork();
}
