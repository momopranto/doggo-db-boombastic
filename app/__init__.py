from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from os import urandom
import config

def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)
    app.config.from_object(config)

    from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp     
	
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']): #create database
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app) #initialize db
    db.app = app #initialize db
    db.create_all() #create tables
    app.db = db #set the app's db to db

    from core import web
    app.register_blueprint(web)

    return app
