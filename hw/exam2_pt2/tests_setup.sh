#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

cp -r /autograder/submission/*.c $SRC_DIR/

cd $SRC_DIR/
make clean > /dev/null
make > /dev/null

#python3 -c "import os; os.system(\"./coffee_pot.bin\")" #> output.txt

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
