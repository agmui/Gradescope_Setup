#!/usr/bin/env bash

assignment="c_review"

git-svn(){
  if [[ ! -z "$1" && ! -z "$2" ]]; then
          echo "Starting clone/copy ..."
          repo=$(echo $1 | sed 's/\/$\|.git$//')
          svn export "$repo/trunk/$2"
  else
          echo "Use: git-svn <repository> <subdirectory>"
  fi  
}

sudo apt-get install subversion 
# clone subdirectory
git-svn https://github.com/agmui/gradescope_semgrep.git hw/$assignment
apt-get install -y python3 python3-pip python3-dev

pip3 install -r /autograder/source/requirements.txt
