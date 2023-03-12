#!/usr/bin/env bash
cd src
apt install cowsay
cat input.txt | ./simpleshell > output.txt
