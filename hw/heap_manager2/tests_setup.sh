#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR
svn export https://github.com/rhit-csse332/csse332-labs/branches/clab/xv6-riscv/ > /dev/null
if test -f $SRC_DIR/user/*.c; then # TODO: add this to all hws
  echo ur one of the gud ones c:
  mv $SRC_DIR/user/*.c $SRC_DIR/xv6-riscv/user/
elif test -f $SRC_DIR/*/*.c; then
  echo Y U ZIP WRONG RAWWWWWWW >:c
  mv $SRC_DIR/*/user/*.c $SRC_DIR/xv6-riscv/user/
elif test -f $SRC_DIR/*.c; then
  echo Y U ZIP WRONG RAWWWWWWW >:c
  mv $SRC_DIR/*.c $SRC_DIR/xv6-riscv/user/
fi

cd $SRC_DIR/xv6-riscv/
make > /dev/null
