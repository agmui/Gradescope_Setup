#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR

clone_dir main ext2 https://github.com/rhit-csse332/csse332-labs.git
rm $SRC_DIR/ext2access.c

cp -r $SRC_DIR/* $SRC_DIR/csse332-labs/ext2/ > /dev/null
cd $SRC_DIR/csse332-labs/ext2/
make clean > /dev/null
make > /dev/null
echo ran make
