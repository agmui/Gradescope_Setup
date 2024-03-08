#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/hw/test_suite/src
cd $SRC_DIR

#clone_dir clab xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

mv $SRC_DIR/simpleshell.c $SRC_DIR/
cd $SRC_DIR
make clean > /dev/null
make > /dev/null
#apt install -y cowsay expect > /dev/null
#PATH="$PATH:/usr/games" # adds cowsay to path
export PATH
expect ./test.exp > output.txt
#strace -e fork,clone --decode-pids=comm -f -o output.log expect ./test.exp
