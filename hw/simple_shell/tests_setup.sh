#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR
#svn export https://github.com/rhit-csse332/csse332-labs/branches/clab/xv6-riscv/ > /dev/null
#mv $SRC_DIR/user/*.c $SRC_DIR/xv6-riscv/user/
#cd $SRC_DIR/xv6-riscv/
make > /dev/null
#apt install -y cowsay expect > /dev/null
PATH="$PATH:/usr/games"
export PATH
expect ./test.exp > output.txt
#whereis cowsay
#whereis expect
cowsay test
cat output.txt