#!/bin/bash

# shellcheck disable=SC2164
cd /autograder/source/src
svn export https://github.com/rhit-csse332/csse332-labs/branches/clab/xv6-riscv/ > /dev/null
#mv ./xv6-riscv/ /autograder/source/src/
mv /autograder/source/src/user/*.c /autograder/source/src/xv6-riscv/user/
make > /dev/null
