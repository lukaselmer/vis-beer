# VIS Beer API

## Setup

* Install python 3.4
* Install virtualenvwrapper

Make sure that this has been added to your environment (e.g. .zprofile, .profile):

export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

```sh
git clone git@github.com:VIS-ETH/vis-beer.git
cd vis-beer
mkvirtualenv vis-beer
pip install -r requirements.txt
```

## Usage

```sh
workon vis-beer
pip install -r requirements.txt
```

## Install New Requirements

pip install <whatever>
pip freeze > requirements.txt

## Tests

```sh
python -m unittest
```
