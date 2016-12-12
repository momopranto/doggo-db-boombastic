from flask import *
from datetime import datetime, timedelta
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp
from sqlalchemy import and_

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

def init_utils(app):
    app.jinja_env.globals.update(signed_up=signed_up)
    app.jinja_env.globals.update(joined_group=joined_group)

def signed_up(username, event_id):
    if SignUp.query.filter_by(username=username, event_id=event_id).first():
        return True
    return False

def joined_group(username, group_id):
    if BelongsTo.query.filter_by(username=username, group_id=group_id).first():
        return True
    return False
