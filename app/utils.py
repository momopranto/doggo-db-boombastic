from flask import *
from datetime import datetime, timedelta
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp
from sqlalchemy import and_

def check_signup(username, event_id):
	signed_up = SignUp.query.filter(and_(SignUp.username == username, SignUp.event_id == event_id)) #check if user was signed up
	return signed_up

template_globals.filters['check_signup'] = check_signup