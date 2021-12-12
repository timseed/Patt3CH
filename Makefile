.DEFAULT_GOAL := all

PYSRC= "."
PYTEST=
PYDATA="./"
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

VENV_NAME=pe39
VENV_ACTIVATE=. ~/$(VENV_NAME)/bin/activate
PYTHON=~/${VENV_NAME}/bin/python3
PIP=pip3
PYCOV=$(PYTHON) -m coverage
Package=""
current_version = '0.1.0'

check:
	$(PYTHON) -m pylint -E            $(PYSRC)
	$(PYTHON) -m black --check --diff $(PYSRC)

format:
	$(PYTHON) -m black $(PYSRC)


test:
	$(PYTHON) -m pytest $(PYTST)

coverage:
	pytest --cov=$(PYSRC)

update-data:
	wget http://www.supercheckpartial.com/MASTER.SCP -O $(ROOT_DIR)$(PYDATA)"MASTER.SCP"
	$(info  "")
	$(info  "")
	$(info  "Data Files need adding in Git. And a new version needs to be installed.")
	$(info  "")
	$(info  "")
	$(info  "Failing to do this will mean you use the old data.")

bump-minor:
	$(PYTHON) -m bumpversion minor --tag --commit

bump-patch:
	$(PYTHON) -m bumpversion patch --tag --commit

test0:
	$(PYTHON) SkimPattern.py format0.lst

test1:
	$(PYTHON) SkimPattern.py format1.lst

test2:
	$(PYTHON) SkimPattern.py format2.lst

test3:
	$(PYTHON) SkimPattern.py format3.lst

test0p:
	$(PYTHON) SkimPattern.py format0.lst MASTERPLUS.SCP

test1p:
	$(PYTHON) SkimPattern.py format1.lst MASTERPLUS.SCP

test2p:
	$(PYTHON) SkimPattern.py format2.lst MASTERPLUS.SCP

test3p:
	$(PYTHON) SkimPattern.py format3.lst MASTERPLUS.SCP

buildmaster:
	$(PYTHON) PatternBuilder.py MASTER.SCP

buildmasterplus:
	#cat MASTER.SCP calls.txt |sort | uniq > MASTERPLUS.SCP
	$(PYTHON) PatternBuilder.py MASTERPLUS.SCP


all : buildmasterplus test0p test1p
#test build install
