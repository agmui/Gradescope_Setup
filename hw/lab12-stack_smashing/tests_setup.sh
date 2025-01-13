#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR

clone_dir clab xv6-riscv https://github.com/rhit-csse332/csse332-labs.git


#mv $SRC_DIR/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
cp -r /autograder/submission/* $SRC_DIR

cd $SRC_DIR
#make > /dev/null

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
