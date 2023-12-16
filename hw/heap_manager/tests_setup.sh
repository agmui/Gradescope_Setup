#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR
svn export https://github.com/rhit-csse332/csse332-labs/branches/heapmm/xv6-riscv/ > /dev/null
mv $SRC_DIR/user/*.c $SRC_DIR/xv6-riscv/user/ # TODO: if not found try $SRC_DIR/*/usr/*c
cd $SRC_DIR/xv6-riscv/
make > /dev/null
