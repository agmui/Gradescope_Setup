#!/usr/bin/env bash

assignment="heap_manager2"

apt-get install -y subversion 

svn checkout https://github.com/agmui/gradescope_semgrep/trunk/hw/$assignment /autograder/source

apt-get install -y python3 python3-pip python3-dev

pip3 install -r /autograder/source/requirements.txt
