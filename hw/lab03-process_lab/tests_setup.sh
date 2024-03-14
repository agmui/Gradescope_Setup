#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

clone_dir main xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

#mv $SRC_DIR/user/*.c $SRC_DIR/
cp -r /autograder/submission/simple_test.c $SRC_DIR
cd $SRC_DIR/
make clean > /dev/null
make > /dev/null

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
