#!/usr/bin/env bash

assignment="c_review"
ls autograder/source

apt-get install -y subversion

# svn uses trunk, explanation: https://datascience.101workbook.org/07-DataParsing/01-FILE-ACCESS/03-4-tutorial-download-github-folders-svn.html#github-folder
svn checkout https://github.com/agmui/gradescope_semgrep/trunk/hw/$assignment /autograder/source

apt-get install -y python3 python3-pip python3-dev

pip3 install -r /autograder/source/requirements.txt
