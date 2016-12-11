from flask import *
from datetime import datetime, timedelta
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp
from sqlalchemy import and_

def check_signup(username, event_id):
    signed_up = SignUp.query.filter(and_(SignUp.username == username, SignUp.event_id == event_id)) #check if user was signed up
    db.session.close()
    return signed_up

template_globals.filters['check_signup'] = check_signup

def populate_groups(username):
    groups = BelongsTo.query.filter_by(username=username)
    db.session.close()
    return [{'group_id':group.group_id,'authorized':group.authorized} for group in groups]

def check_authorized(username):
    groups = BelongsTo.query.filter_by(username=username, authorized=True)
    if groups:
        return groups.first().group_id
    else:
        return None

