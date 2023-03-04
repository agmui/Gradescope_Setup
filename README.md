# gradescope_semgrep

## gradescope configuration
To setup which assignment to grade go into `setup.sh` and change the
variable `assignment` to a directory name in the `hw` directory.

To upload to gradescope just zip `run_autograder` and `setup.sh` in a file and
upload

(image)

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
##### TODO:
* check for over sending files
* setup the file dir for each assignment
    * file check
* implement partial credit
* add doc about running tests localy
* setup github deploy_key
