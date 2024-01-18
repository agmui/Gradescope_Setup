#!/usr/bin/env bash

#ls autograder/source

apt update -y > /dev/null && apt upgrade -y
apt install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu # for xv6 labs
apt install -y cowsay expect # for simpleshell labs

#function clone_dir() {
#  BRANCH=$1
#  DIR=$2
#  URL=$3
#  # --no-checkout avoids us from downloading unneeded junk
#  git clone --no-checkout $URL
#  cd gradescope_semgrep
#  git checkout $BRANCH
#  #setups sparse checkout https://github.blog/2020-01-17-bring-your-monorepo-down-to-size-with-sparse-checkout/
#  git sparse-checkout set --cone
#  git sparse-checkout set $DIR #clones only xv6-riscv/ DIR
#}
#clone_dir main hw/$assignment https://github.com/agmui/gradescope_semgrep

#svn checkout https://github.com/agmui/gradescope_semgrep/trunk/hw/$assignment /autograder/source

git clone https://github.com/agmui/gradescope_semgrep

apt-get install -y python3 python3-pip python3-dev jq

mv /autograder/source/clone_dir /usr/bin