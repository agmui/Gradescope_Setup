#!/usr/bin/env bash

#TODO: check if you can read json
grep -Po '"title":.*?",' $AUTOGRADER_ROOT/submission_metadata.json | cut -d':' -f 2 | tr -d '"' | tr -d ',' | awk '{$1=$1;print}' >> assignmentName.txt
assignment="c_review"
ls autograder/source

apt update -y > /dev/null && apt upgrade -y
apt install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu # for xv6 labs

apt-get install -y subversion

# svn uses trunk, explanation: https://datascience.101workbook.org/07-DataParsing/01-FILE-ACCESS/03-4-tutorial-download-github-folders-svn.html#github-folder
svn checkout https://github.com/agmui/gradescope_semgrep/trunk/hw/$assignment /autograder/source

apt-get install -y python3 python3-pip python3-dev

pip3 install -r /autograder/source/requirements.txt
