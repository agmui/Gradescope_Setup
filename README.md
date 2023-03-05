# gradescope setup

## gradescope configuration
To setup which assignment to grade go into `setup.sh` and change the
variable `assignment` to a directory name in the `hw` directory.

To upload to gradescope just zip `run_autograder` and `setup.sh` in a file and
upload

(image)

* bc of src dir rembember to put `os.chdir("src")` somewhere in your python test files`
## writing tests
* add guide on how to download gradescope submissions
* unit tests in `test_integration.py` should be the same number of rules in `rules.yaml`
* if file not uploaded do a try catch statment
* writing test follow python untests format (link)
    * to write test there must be a dir called `tests` next to the `run_tests.py` file
    * inside the `tests` dir each file must have `test_...` in the name
    * there must be a gradescope_utils class imported
(example test file)
    * each test must start with prefix `test_...`


### writing tests for xv6 labs
follow the c_review as a template guide
copy .glbinit.tmpl... into src
copy `grade-lab-5.py`'s code into `test_grading_script.py`
copy all the imports in c_review's `test_grading_script.py` 
copy `gradelib.py` into the test dir
write multiple tests for gradescopes autograder by checking the `TESTS` array (look at c_review `test_grading_script.py` as a guide)

## running tests localy
You should run from top dir of the assignment
For example to run `test_grading_script.py` for c_review run `python3 tests/test_grading_script.py`

## running tests in grade scope


## writing tests for test_integration.py
this file is my atempt at over enginering something bc i wanted to be lazy when grading
##### TODO:
* test fail help msg
* check for over sending files
* setup the file dir for each assignment
    * file check
* implement partial credit
* add doc about running tests localy
* setup github deploy_key
