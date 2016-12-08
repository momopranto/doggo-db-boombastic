all: setup

db: mysql
	mysql -u root -p -e "create database FindFolks"; mysql -u root -p FindFolks < ./db/ProjectPart2.sql

setup:
	sudo apt-get install -y build-essential python-dev python-pip libffi-dev; pip install -r requirements.txt

run:
	python serve.py
