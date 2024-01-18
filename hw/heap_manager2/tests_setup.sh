#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR

clone_dir buddy xv6-riscv https://github.com/rhit-csse332/csse332-labs.git
#SVN is no longer supported (https://github.blog/2023-01-20-sunsetting-subversion-support/)
#svn export https://github.com/rhit-csse332/csse332-labs/branches/buddy/xv6-riscv/ > /dev/null

pwd
ls
#if test -f $SRC_DIR/user/*.c; then # TODO: add this to all hws
#  echo ur one of the gud ones c:
#  mv $SRC_DIR/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
#elif test -f $SRC_DIR/*/*.c; then
#  echo Y U ZIP WRONG RAWWWWWWW >:c
#  mv $SRC_DIR/*/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
#elif test -f $SRC_DIR/*.c; then
#  echo Y U ZIP WRONG RAWWWWWWW >:c
#  mv $SRC_DIR/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
#fi
cp -r $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/user

cd $SRC_DIR/csse332-labs/xv6-riscv/
ls
pwd
make > /dev/null
