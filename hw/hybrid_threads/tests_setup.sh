#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR

# first arg is branch second is directory
function clone_dir() {#TODO: make this into a program
  BRANCH=$1
  DIR=$2
  URL=$3
  # --no-checkout avoids us from downloading unneeded junk
  git clone --no-checkout $URL
  cd csse332-labs
  git checkout $BRANCH
  #setups sparse checkout https://github.blog/2020-01-17-bring-your-monorepo-down-to-size-with-sparse-checkout/
  git sparse-checkout set --cone
  git sparse-checkout set $DIR #clones only xv6-riscv/ DIR
}
clone_dir clab xv6-riscv https://github.com/rhit-csse332/csse332-labs.git

mv $SRC_DIR/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
cd $SRC_DIR/csse332-labs/xv6-riscv/
make > /dev/null
