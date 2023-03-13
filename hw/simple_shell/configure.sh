#!/usr/bin/env bash
# shellcheck disable=SC2164
cd src
apt update -y > /dev/null
apt install -y cowsay # > /dev/null
make
echo cowsay test
cowsay test
cat input.txt | ./simpleshell > output.txt
