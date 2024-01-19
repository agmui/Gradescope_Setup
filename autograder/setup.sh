#!/usr/bin/env bash

#ls autograder/source

apt update -y > /dev/null && apt upgrade -y
apt install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu # for xv6 labs
apt install -y cowsay expect # for simpleshell labs

git clone https://github.com/agmui/gradescope_semgrep

apt-get install -y python3 python3-pip python3-dev jq

chmod +x /autograder/source/clone_dir
mv /autograder/source/clone_dir /usr/bin