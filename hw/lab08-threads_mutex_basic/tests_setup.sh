#!/bin/bash
set -e -u -o pipefail
#GREEN=$(tput -T xterm-256color setaf 2)
#RESET=$(tput -T xterm-256color sgr0)
#export PS4='[$GREEN$BASH_SOURCE$RESET:$LINENO] '
#set -x


# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

# TODO: make it a global func like clone_dir (also maybe add a second from_dir arg)
# TODO: maybe do this in python after the cp but before build just run a util python func
find_and_mv () {
  DESTINATION="$1"   # Save first argument in a variable
  shift            # Shift all arguments to the left (original $1 gets lost)
  FILES=("$@") # Rebuild the array with rest of arguments
  echo ==== searching for FILES =====
  for f in "${FILES[@]}"
  do
    echo --  searching for: $f  --

    # if already at target destination
    if [ -f "$DESTINATION/$f" ]; then
      echo found file: "$DESTINATION/$f"
      continue
    fi
    file_path=$(find "$DESTINATION" -maxdepth 20 -name "$f" -print -quit)
    if  [ -z "$file_path" ]; then
      echo found path: "$file_path"
      mv $file_path $DESTINATION
    else
      echo cound not find file
    fi
  done
  echo ==============================
}

find_and_mv /autograder/submission factoring.c threadSort.c add_a_lot.c red_blue_purple.c

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


# ==== remapping main ==== #TODO: integrate this for all thread labs
gcc -c red_blue_purple_tests.c
objcopy --redefine-sym main=oldmain red_blue_purple_tests.o
objcopy --redefine-sym red_blue_purple_tests=main red_blue_purple_tests.o
gcc red_blue_purple_tests.o -o test
rm *.o
echo "=== running ./test ==="
./test # TODO: this should be run inside of the python test suite for prettier output
echo "=============="
# =====================


cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
