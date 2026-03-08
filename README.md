# What is this project about
This project has the following functionalities at the moment:
1. extract the zips of bank statement csv files from OP bank to a target directory

This is the script `extract_zips_from_directory.sh`

2. generate tax report on base of the given directory, where the bank statements reside

## Demo

[![Demo](https://img.youtube.com/vi/NzRyE-s3JDY/0.jpg)](https://www.youtube.com/watch?v=NzRyE-s3JDY)

# Pre-requisite
1. `venv` is assumed to be built-in Action: my local is python3.12 => need `sudo apt-get install python3.12-venv`
2. when `venv` module is installed to your system, run `python -m venv .venv` to create a virtual environment in this project *working directory* based on https://www.youtube.com/watch?v=eDe-z2Qy9x4&t=11s
3. run `python -m pip install -e .` to install the project
# How to run
`python tax_report extracted_directory` or `python -m tax_report extracted_directory`

## How to run tests
`python -m pip install -e ".[test]" && python -m pytest tests/ -v`

# Tutorial of SETUPTOOLS
https://setuptools.pypa.io/en/latest/userguide/quickstart.html

