#!/bin/bash
set -e -u -o pipefail
GREEN=$(tput -T xterm-256color setaf 2)
RESET=$(tput -T xterm-256color sgr0)
export PS4='[$GREEN$BASH_SOURCE$RESET:$LINENO] '
set -x

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

clone_dir heapmm xv6-riscv https://github.com/rhit-csse332/csse332-labs.git
rm $SRC_DIR/csse332-labs/xv6-riscv/user/rhmalloc.c

cp /autograder/submission/user/rhmalloc.c $SRC_DIR/csse332-labs/xv6-riscv/user

cd $SRC_DIR/csse332-labs/xv6-riscv/
make clean > /dev/null
make > /dev/null
#strace -e fork,clone --decode-pids=comm -f -o output.log expect ./test.exp

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
