# pathfinder
pathfinder is a tool that finds where to scrape

![Python](https://img.shields.io/badge/python-3.10-blue.svg) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Install

install poetry:

windows    
```bash
pip install poetry
```

linux
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Use
get bcy meta:
```bash
poetry install
poetry shell
python3 bcy_runner.py --start_date="20220610" --end_date="20230610" --target_dir="jsons"
```