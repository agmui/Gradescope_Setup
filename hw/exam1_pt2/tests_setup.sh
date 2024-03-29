#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

cp -r /autograder/submission/*.c $SRC_DIR/

cd $SRC_DIR/
#make clean > /dev/null
make > /dev/null

echo 10 | ./problem3.bin > problem3_rez.txt
echo 10 | ./problem4_parent.bin> problem4_rez.txt

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
#$SRC_DIR/processbatch.bin 1.txt 2.txt 3.txt 4.txt 5.txt
#stdbuf -oL -eL $SRC_DIR/processbatch.bin 1.txt 2.txt 3.txt 4.txt 5.txt
#unbuffer $SRC_DIR/processbatch.bin 1.txt 2.txt 3.txt 4.txt 5.txt
python3 run_tests.py
