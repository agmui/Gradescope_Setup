#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder
cp -r /autograder/submission/* $SRC_DIR
#make > /dev/null

#gcc -Wall -g -pthread -c -pthread -ggdb factoring.c -o thread_factoring.bin
#gcc -Wall -g -pthread -c -pthread -ggdb threadSort.c -o thread_sort.bin
#gcc -Wall -g -pthread -c -pthread -ggdb add_a_lot.c -o basic_mutex.bin
#gcc -Wall -g -pthread -c -pthread -ggdb red_blue_purple.c -o red_blue_purple.bin
gcc -pthread -ggdb factoring.c -o thread_factoring.bin
gcc -pthread -ggdb threadSort.c -o thread_sort.bin
gcc -pthread -ggdb add_a_lot.c -o basic_mutex.bin
gcc -pthread -ggdb red_blue_purple.c -o red_blue_purple.bin

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
