# Oklahoma Mesonet Coding Project

This is a simple CLI tool that reads a CSV file and outputs a new CSV file which is sorted by the input parameter. The new csv file will contain two columns: *time* and the *input parameter*. By default, the file will be sorted in *descending* order unless specified via the *\[-a/--ascending\]* flag.

## Usage
```bash
rank.py [-o --output] [-a --ascending] <path/to/csv> <parm>
```
There are two required positional arguments. The first is the *\<path/to/input/csv\>*, then the *\<parameter\>* that you would like to sort by. You can also specify the output location via the *\[-o/--output\]* flag.
## Installation
After cloning the repo to your python virtual environment, execute the following commmand while in the project folder to build the project:
```bash
pip install -e .
```
#### Testing
To install the testing requirements, execute the following command while in the project folder:
```bash
pip install -e ".[testing]"
```
To run tests, execute the following command while in the project folder:
```bash
pytest
```