#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR

clone_dir main ext2 https://github.com/rhit-csse332/csse332-labs.git
rm $SRC_DIR/csse332-labs/ext2/ext2access.c

#cp -r $SRC_DIR/* $SRC_DIR/csse332-labs/ext2/ > /dev/null
cp -r /autograder/submission/* $SRC_DIR/csse332-labs/xv6-riscv/

cd $SRC_DIR/csse332-labs/ext2/
make clean > /dev/null
make > /dev/null

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
