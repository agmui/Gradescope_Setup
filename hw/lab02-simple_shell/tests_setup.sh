#!/bin/bash
#set -e -u -o pipefail # TODO: decide bc in the expect call things could fail
GREEN=$(tput -T xterm-256color setaf 2)
RESET=$(tput -T xterm-256color sgr0)
export PS4='[$GREEN$BASH_SOURCE$RESET:$LINENO] '
set -x

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

#generates gif: https://github.com/charmbracelet/vhs?tab=readme-ov-file
apt install  ./vhs_0.8.0_amd64.deb
vhs cassette.tape -o out.gif
base64 out.gif > base64gif.txt

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
