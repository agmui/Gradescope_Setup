#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR

clone_dir cow xv6-riscv https://github.com/rhit-csse332/csse332-labs.git


#mv $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/
cp -r $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/ > /dev/null
cd $SRC_DIR/csse332-labs/xv6-riscv/
ls
pwd
make clean > /dev/null
make > /dev/null
echo ran make