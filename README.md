# What is this project about
This project generates *financial statements* and forms needed in *tax report* on base of the bank statement csv files, which are stored in a given directory

## Demo

[![Demo](https://img.youtube.com/vi/NzRyE-s3JDY/0.jpg)](https://www.youtube.com/watch?v=NzRyE-s3JDY) (outdated, updated soon)

# Pre-requisite
1. `cd` to this project directory
2. `venv` is assumed to be built-in Action: my local is python3.12 => need `sudo apt-get install python3.12-venv`
3. when `venv` module is installed to your system, run `python3 -m venv .venv` to create a virtual environment in this project *working directory* based on https://www.youtube.com/watch?v=eDe-z2Qy9x4&t=11s
# How to run in project directory
1. initialize venv with command `python3 -m venv .venv`
2. activate venv with command `source .venv/bin/activate`
3. install project with command `pip install e .`
4. execution
* dry-run with command: `python calculation pdf --input-dir <input-directory> --company-name <company-name>`

example: `python accounting pdf --input-dir ~/Documents/outlierx/tiliote/extracted --company-name "xxx"`

## How to run tests
1. install `pip install -e ".[test]"`
2. run command `pytest tests`

# Tutorial of SETUPTOOLS
https://setuptools.pypa.io/en/latest/userguide/quickstart.html

