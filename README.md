# pathfinder
pathfinder is a lightweight tool that finds where to scrape

![Python](https://img.shields.io/badge/python-3.10-blue.svg) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Functions
- [x] bcy: get metadata; write processed data to parquet

## Install

install poetry:   
```bash
# universal, no root
pip install poetry

# OR: linux, with root
curl -sSL https://install.python-poetry.org | python3 -
```

to setup & enter the environment:
```bash
git clone https://github.com/trojblue/pathfinder.git && cd pathfinder
poetry install # creates venv
poetry shell  # activates venv
```

## Use
(in poetry shell):

get bcy meta as json files:
```bash
python run_bcy.py --start_date="20220610" --end_date="20230610" --target_dir="jsons"
```

export bcy json files as a single csv / parquet file:
```bash
# saves to <curr_dir>/bcy_2015_2019.parquet
python write_bcy.py D:\CSC\pathfinder\bcy_2015_2019
```

download danbooru metadata, from id 6408262 to 6000000, with 4 threads:
```bash
python run_dbr.py 6408262 6000000 -n 1
```
