#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

cp -r /autograder/submission/processbatch.c $SRC_DIR/

cd $SRC_DIR/
echo '#include "exam.h"'$'\n'"$(cat processbatch.c)" > processbatch.c # inserts #include "exam.h" at the top of the file
cat processbatch.c
#make clean > /dev/null
make > /dev/null

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
#$SRC_DIR/processbatch.bin 1.txt 2.txt 3.txt 4.txt 5.txt
#stdbuf -oL -eL $SRC_DIR/processbatch.bin 1.txt 2.txt 3.txt 4.txt 5.txt
#unbuffer $SRC_DIR/processbatch.bin 1.txt 2.txt 3.txt 4.txt 5.txt
python3 run_tests.py
