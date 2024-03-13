#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

clone_dir heapmm xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

if test -f $SRC_DIR/user/*.c; then # TODO: add this to all hws
  echo ur one of the gud ones c:
  mv $SRC_DIR/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
elif test -f $SRC_DIR/*/*.c; then
  echo Y U ZIP WRONG RAWWWWWWW >:c
  mv $SRC_DIR/*/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
elif test -f $SRC_DIR/*.c; then
  echo Y U ZIP WRONG RAWWWWWWW >:c
  mv $SRC_DIR/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
fi

cd $SRC_DIR/csse332-labs/xv6-riscv/
make clean > /dev/null
make > /dev/null
#strace -e fork,clone --decode-pids=comm -f -o output.log expect ./test.exp