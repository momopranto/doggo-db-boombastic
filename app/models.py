from config import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Member(db.Model):
	username = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(128))
	firstname = db.Column(db.String(20))
	lastname = db.Column(db.String(20))
	email = db.Column(db.String(32), unique = True)
	zipcode = db.Column(db.Integer())

	def __init__(self, username, password, firstname, lastname, email, zipcode):
		self.username =  username
		self.password = password
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.zipcode = zipcode

class Friend(db.Model):
	friend_of = db.Column(db.String(20), db.ForeignKey('member.username'), primary_key=True)
	friend_to = db.Column(db.String(20), db.ForeignKey('member.username'), primary_key=True)

	def __init__(self, friend_of, friend_to):
		self.friend_of = friend_of
		self.friend_to = friend_to


class AGroup(db.Model):
	group_id = db.Column(db.Integer(), primary_key=True)
	group_name = db.Column(db.String(20))
	description = db.Column(db.Text())
	creator = db.Column(db.String(20), db.ForeignKey('member.username'))

	def __init__(self, creator, group_name, description, category, keyword):
		self.group_name = group_name
		self.description = description
		self.creator = creator
		interest = Interest(category, keyword)
		db.session.add(interest)
		db.session.commit()
		interestedin = InterestedIn(creator, category, keyword)
		db.session.add(interestedin)
		db.session.commit()
		db.session.close()


class Interest(db.Model):
	category = db.Column(db.String(20), primary_key=True)
	keyword = db.Column(db.String(20), primary_key=True)

	def __init__(self, category, keyword):
		self.category = category
		self.keyword = keyword

class About(db.Model):
	group_id = db.Column(db.Integer(), db.ForeignKey('a_group.group_id'), primary_key=True)
	category = db.Column(db.String(20), primary_key=True)
	keyword = db.Column(db.String(20), primary_key=True)
	db.ForeignKeyConstraint(['category', 'keyword'], ['interest.category', 'interest.keyword'])

	def __init__(self, group_id, category, keyword):
		self.group_id = group_id
		self.category = category
		self.keyword = keyword

class InterestedIn(db.Model):
	username = db.Column(db.String(20), db.ForeignKey('member.username'), primary_key=True)
	category = db.Column(db.String(20), primary_key=True)
	keyword = db.Column(db.String(20), primary_key=True)
	db.ForeignKeyConstraint(['category', 'keyword'], ['interest.category', 'interest.keyword'])

	def __init__(self, username, category, keyword):
		self.username = username
		self.category = category
		self.keyword = keyword

class BelongsTo(db.Model):
	group_id = db.Column(db.Integer(), db.ForeignKey('a_group.group_id'), primary_key=True)
	username = db.Column(db.String(20), db.ForeignKey('member.username'), primary_key=True)
	authorized = db.Column(db.Boolean(), default=True)

	def __init__(self, group_id, username, authorized):
		self.username = username
		self.group_id = group_id
		self.authorized = authorized

class Location(db.Model):
	location_name = db.Column(db.String(20), primary_key=True)
	zipcode = db.Column(db.Integer(), primary_key=True)
	address = db.Column(db.String(50))
	description = db.Column(db.Text())
	latitude = db.Column(db.Float())
	longitude = db.Column(db.Float())

        def __init__(self, location_name, zipcode, address, desc, lat, lon):
		self.location_name = location_name
		self.zipcode = zipcode
                self.address = address
                self.description = desc
                self.latitude = lat
                self.longitude = lon

class AnEvent(db.Model):
	event_id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(100))
	description = db.Column(db.Text())
	start_time = db.Column(db.DateTime())
	end_time = db.Column(db.DateTime())
	location_name = db.Column(db.String(20))
	zipcode = db.Column(db.Integer())
	db.ForeignKeyConstraint(['location_name', 'zipcode'], ['location.location_name', 'location.zipcode'])

	def __init__(self, title, description, start_time, end_time, location_name, zipcode, lat, lon):
            if not Location.query.filter_by(location_name=location_name, zipcode=zipcode).first():
                location = Location(location_name, zipcode, '','',lat,lon)
		db.session.add(location)
		db.session.commit()
		db.session.close()

            self.title = title
            self.description = description
            self.start_time = start_time
            self.end_time = end_time
            self.location_name = location_name
            self.zipcode = zipcode


class Organize(db.Model):
	event_id = db.Column(db.Integer(), db.ForeignKey('an_event.event_id'), primary_key=True)
	group_id = db.Column(db.Integer(), db.ForeignKey('a_group.group_id'), primary_key=True)

	def __init__(self, event_id, group_id):
		self.event_id = event_id
		self.group_id = group_id

class SignUp(db.Model):
	event_id = db.Column(db.Integer(), db.ForeignKey('an_event.event_id'), primary_key=True)
	username = db.Column(db.String(20), db.ForeignKey('member.username'), primary_key=True)
	rating = db.Column(db.Integer(), default=None)

	def __init__(self, event_id, username):
		self.event_id = event_id
		self.username = username

	def rate(rating):
		self.rating = rating
