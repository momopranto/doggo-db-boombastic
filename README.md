# FindFolks Project

Division of Work:

Matthew Ricci - Handled the front-end portion of the project. Utilized the Bootstrap CSS/JS framework to create a more user-friendly navbar and to style the various forms across the project that are used to interact with the database. In addition, coded the script for generating a temporary password and emailing it to a user if the user has forgotten their password.

Rasheeq Rahman - Created the models found in models.py that are used by SQLAlchemy to build and interact with the database; commented the queries below their SQLAlchemy equivalents in core.py; implemented the search feature for groups and events; coded the back-end for the forms found on Register and Login; made enhancements to parts of the front-end; coded the features allowing a user to sign up for events as well as join a group

Mohammed Al Amin - Wrote a Dockerfile and Makefile for distributing the project easily to different computers; lots of bugfixing and polishing of code; added much of the input validation, making it hard for a user to crash the webapp due to incorrect or unexpected input; wrote the code for allowing a user to create an event; programmed login checks and verified all URL redirects based on different use cases; 

Extra features:
Creating groups - Implemented a feature where users can create groups based on a single, common interest. The groups are publicly listed and can be searched for
Joining groups - Users can find public groups via the search function and opt to join the groups in order to attend the group's events

```
/app
	/templates
		base.html - served as the template base
		create_event.html - template for the create events form
		events.html - displayed all events 
		groups.html - displayed all groups
		home.html - home page for users
		index.html - first page seen
		login.html - template used for users to login
		register.html - template that registers users

	/static
		/css - style for the website
			bootstrap.min.css
			style.css
		/js - dynamic styling for the app
			bootstrap.min.js
			jquery-3.1.1.min.js
	
	__init__.py - initialized databases and registered necessary pages
	config.py - setup the server setting for the app
	core.py - full backend of all pages used in the app
	models.py - held all the database tables derived from ProjectPart2.sql 
	utils.py - utility functions necessary for the app
/db
	ProjectPart2.sql - original tables
	all_sql_statements.txt - contains all the sql statements and reason for usage

.gitignore - states to git which files to ignore
Dockerfile - contains commands a user calls to build a container
Makefile - used to create the database and start the server
docker-compose.yml - configuration file for the docker container
serve.py - file to execute the server
```