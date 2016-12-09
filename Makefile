all: setup

db: mysql
	mysql -u root -p -e "create database FindFolks"; mysql -u root -p FindFolks < ./db/ProjectPart2.sql; export DB_URL=mysql://root@localhost/FindFolks

setup:
	if which sudo >/dev/null; then sudo apt-get install -y build-essential python-dev python-pip libffi-dev; else apt-get install -y build-essential python-dev libffi-dev; fi; pip install -r requirements.txt

run:
	python serve.py
