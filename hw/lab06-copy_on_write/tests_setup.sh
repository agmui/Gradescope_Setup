#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

clone_dir cow xv6-riscv https://github.com/rhit-csse332/csse332-labs.git


#mv $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/
#cp -r $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/ > /dev/null #TODO: find out if this can just be mv
cp -r /autograder/submission/* $SRC_DIR/csse332-labs/xv6-riscv/

cd $SRC_DIR/csse332-labs/xv6-riscv/
make clean > /dev/null
make > /dev/null

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
