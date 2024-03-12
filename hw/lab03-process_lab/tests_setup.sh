#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/hw/test_suite/src
cd $SRC_DIR

clone_dir main xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

mv $SRC_DIR/user/*.c $SRC_DIR/
cd $SRC_DIR/
make clean > /dev/null
make > /dev/null
