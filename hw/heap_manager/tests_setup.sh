#!/bin/bash

# shellcheck disable=SC2164
SRC_DIR=/autograder/source/src
cd $SRC_DIR

function clone_dir() {
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
clone_dir heapmm xv6-riscv https://github.com/rhit-csse332/csse332-labs.git
#svn export https://github.com/rhit-csse332/csse332-labs/branches/heapmm/xv6-riscv/ > /dev/null

if test -f $SRC_DIR/user/*.c; then # TODO: add this to all hws
  echo ur one of the gud ones c:
  mv $SRC_DIR/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
elif test -f $SRC_DIR/*/*.c; then
  echo Y U ZIP WRONG RAWWWWWWW >:c
  mv $SRC_DIR/*/user/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
elif test -f $SRC_DIR/*.c; then
  echo Y U ZIP WRONG RAWWWWWWW >:c
  mv $SRC_DIR/*.c $SRC_DIR/csse332-labs/xv6-riscv/user/
fi

cd $SRC_DIR/csse332-labs/xv6-riscv/
make > /dev/null
#strace -e fork,clone --decode-pids=comm -f -o output.log expect ./test.exp