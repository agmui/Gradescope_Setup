#!/bin/bash
set -e -u -o pipefail
GREEN=$(tput -T xterm-256color setaf 2)
RESET=$(tput -T xterm-256color sgr0)
export PS4='[$GREEN$BASH_SOURCE$RESET:$LINENO] '
set -x


# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

clone_dir cow xv6-riscv https://github.com/rhit-csse332/csse332-labs.git


#mv $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/
#cp -r $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/ > /dev/null #TODO: find out if this can just be mv
#TODO: only cp the needed files ['kernel/kalloc.c', 'kernel/trap.c', 'kernel/vm.c', 'user/simplefork.c']
cp -r /autograder/submission/* $SRC_DIR/csse332-labs/xv6-riscv/

cd $SRC_DIR/csse332-labs/xv6-riscv/
make clean > /dev/null
make > /dev/null

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
