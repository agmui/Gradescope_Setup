#!/bin/bash

# shellcheck disable=SC2164
cd $SRC_DIR # Defined in Gradescope_setup/autograder/run_autograder

clone_dir klist xv6-riscv https://github.com/rhit-csse332/csse332-labs.git


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
    if  [ -z "$filepath" ]; then
      echo found path: "$file_path"
      mv $file_path $DESTINATION
    else
      echo cound not find file
    fi
  done
  echo ==============================
}

#find_and_mv /autograder/submission factoring.c threadSort.c add_a_lot.c red_blue_purple.c


if [ -d /autograder/submissions/kernel ]; then
  cp -r /autograder/submission/* $SRC_DIR/csse332-labs/xv6-riscv/kernel
else
  cp -r /autograder/submission/* $SRC_DIR/csse332-labs/xv6-riscv/
fi
#cp -r $SRC_DIR/* $SRC_DIR/csse332-labs/xv6-riscv/ > /dev/null

cd $SRC_DIR/csse332-labs/xv6-riscv/
make clean > /dev/null
make > /dev/null

cd $SRC_DIR/..
echo "--- running run_tests.py ---"
python3 run_tests.py
