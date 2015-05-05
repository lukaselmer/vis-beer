# VIS Beer API

## Setup

* Install [pyenv](https://github.com/yyuu/pyenv) and [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)

```sh
pyenv install
```

* Install virtualenvwrapper

Make sure that this has been added to your environment (e.g. .zshrc):

```sh
eval "$(pyenv init - zsh)"
eval "$(pyenv virtualenv-init -)"
```

Clone the project, setup virtualenv and install dependencies:

```sh
git clone git@github.com:VIS-ETH/vis-beer.git
cd vis-beer
pyenv virtualenv 2.7.9 vis-beer-2.7.9
pyenv activate vis-beer-2.7.9
pip install -r requirements.txt
```

## Usage

```sh
pyenv activate vis-beer-2.7.9
pip install -r requirements.txt
```

## Install New Requirements

```sh
pip install <whatever>
pip freeze > requirements.txt
```

## Tests

```sh
python -m unittest discover
```
