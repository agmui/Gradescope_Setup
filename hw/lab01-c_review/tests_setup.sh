#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/hw/test_suite/src
cd $SRC_DIR

clone_dir clab xv6-riscv https://github.com/rhit-csse332/csse332-labs.git
#svn export https://github.com/rhit-csse332/csse332-labs/branches/clab/xv6-riscv/ > /dev/null

#TODO: only move the 4 .c files
mv $SRC_DIR/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
#cp -r /autograder/submission/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
cd $SRC_DIR/csse332-labs/xv6-riscv/
make clean > /dev/null
make > /dev/null
