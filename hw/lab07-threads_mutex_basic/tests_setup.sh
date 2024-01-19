#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
mv $SRC_DIR/user/*.c $SRC_DIR/
cd $SRC_DIR
make > /dev/null
