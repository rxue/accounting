# What is this project about
Given the bank statement of a small investment company as input, this project generates *financial statements* and forms needed in *tax report*. 

The generated forms includes Form 8A and Form 70 from verotoimisto in Finland, and they can directly be attached to veroilmoitus through vero.fi

## Demo

[![Demo](https://img.youtube.com/vi/dmA0IM8xf74/0.jpg)](https://www.youtube.com/watch?v=rzavvbLi03s)

# Pre-requisite
1. `cd` to this project directory
2. `venv` is assumed to be built-in Action: my local is python3.12 => need `sudo apt-get install python3.12-venv`
3. when `venv` module is installed to your system, run `python3 -m venv .venv` to create a virtual environment in this project *working directory* based on https://www.youtube.com/watch?v=eDe-z2Qy9x4&t=11s
# How to run in project directory
1. initialize venv with command `python3 -m venv .venv`
2. activate venv with command `source .venv/bin/activate`
3. install project with command `pip install e .`
4. execute command: `python -m investment.tax_report pdf config.yml`, where `config.yml` is the configuration file for running the program

## How to run tests
1. install `pip install -e ".[test]"`
2. run command `pytest tests`

# Tutorial of SETUPTOOLS
https://setuptools.pypa.io/en/latest/userguide/quickstart.html

