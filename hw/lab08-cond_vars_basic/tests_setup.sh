#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR
make clean > /dev/null # TODO: have every hw run make clean before make
make > /dev/null
