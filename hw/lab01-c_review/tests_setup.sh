#!/bin/bash
set -e -u -o pipefail
GREEN=$(tput setaf 2)
RESET=$(tput sgr0)
export PS4='[$GREEN$BASH_SOURCE$RESET:$LINENO] '
set -x

# shellcheck disable=SC2164
cd "$SRC_DIR" # Defined in Gradescope_setup/autograder/run_autograder

clone_dir clab xv6-riscv https://github.com/rhit-csse332/csse332-labs.git > /dev/null # TODO: decide to hide
#SVN is no longer supported (https://github.blog/2023-01-20-sunsetting-subversion-support/)
#svn export https://github.com/rhit-csse332/csse332-labs/branches/clab/xv6-riscv/ > /dev/null

#TODO: only move the 4 .c files
#mv $SRC_DIR/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
cp -r /autograder/submission/user/*c "$SRC_DIR"/csse332-labs/xv6-riscv/user/

#TODO: maybe move the build into python along with the file sub dir searching?
cd "$SRC_DIR"/csse332-labs/xv6-riscv/
make clean > /dev/null
make > /dev/null

cd "$SRC_DIR"/..
echo "--- running run_tests.py ---"
python3 run_tests.py
