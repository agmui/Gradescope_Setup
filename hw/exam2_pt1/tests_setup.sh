#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder
cp -r /autograder/submission/* $SRC_DIR
make clean
make > /dev/null

#./problem1.bin abcdefgh 4 4
#./problem2.bin abcdefgh 4 4
#./problem3.bin abcdefghij 5 3

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
