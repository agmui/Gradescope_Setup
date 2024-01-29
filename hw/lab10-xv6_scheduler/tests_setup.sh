#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR

clone_dir clab xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

mv $SRC_DIR/kernel/*.c $SRC_DIR/csse332-labs/xv6-riscv/kernel/
cd $SRC_DIR/csse332-labs/xv6-riscv/
make > /dev/null
