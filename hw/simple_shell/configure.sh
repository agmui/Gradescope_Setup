#!/usr/bin/env bash
# shellcheck disable=SC2164
cd src
apt update -y > /dev/null
apt install -y cowsay # > /dev/null
echo cowsay test
cowsay test
make
cat input.txt | ./simpleshell > output.txt
