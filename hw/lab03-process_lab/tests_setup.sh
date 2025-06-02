#!/bin/bash
set -e -u -o pipefail
GREEN=$(tput -T xterm-256color setaf 2)
RESET=$(tput -T xterm-256color sgr0)
export PS4='[$GREEN$BASH_SOURCE$RESET:$LINENO] '
set -x

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

#clone_dir main process_lab https://github.com/rhit-csse332/csse332-labs.git
#rm process_lab/simple_test.c

#mv $SRC_DIR/user/*.c $SRC_DIR/
cp -r /autograder/submission/simple_test.c $SRC_DIR
cd $SRC_DIR/
make clean > /dev/null
make simple_test > /dev/null

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
