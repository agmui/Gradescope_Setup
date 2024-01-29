#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR

clone_dir klist xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

cp -r $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/ > /dev/null
cd $SRC_DIR/csse332-labs/xv6-riscv/
make clean > /dev/null
make > /dev/null
echo ran make
