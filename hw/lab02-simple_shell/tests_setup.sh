#!/bin/bash

cd "$SRC_DIR" # Defined in Gradescope_setup/autograder/run_autograder

#clone_dir clab xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

cp -r /autograder/submission/* $SRC_DIR
make clean > /dev/null
make > /dev/null
#apt install -y cowsay expect > /dev/null
#PATH="$PATH:/usr/games" # adds cowsay to path
export PATH
expect ./test.exp > output.txt
#strace -e fork,clone --decode-pids=comm -f -o output.log expect ./test.exp

#generates gif https://github.com/charmbracelet/vhs?tab=readme-ov-file
apt install vhs
vhs cassette.tape -o out.gif

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
