#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR

clone_dir clab xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

mv $SRC_DIR/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
cd $SRC_DIR/csse332-labs/xv6-riscv/
make > /dev/null
#apt install -y cowsay expect > /dev/null
PATH="$PATH:/usr/games" # adds cowsay to path
export PATH
expect ./test.exp > output.txt
#strace -e fork,clone --decode-pids=comm -f -o output.log expect ./test.exp
