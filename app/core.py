<<<<<<< HEAD
from flask import *
=======
from flask import Flask, render_template, Blueprint, url_for, request, redirect, jsonify, json
>>>>>>> ccccf7c386439e8d24822a8e89f203b987721cb1
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp

web = Blueprint('web', __name__)

@web.route('/test')
def test():
    #m1 = Member('a','b','c','d','e',12345)
    #db.session.add(m1)
    #db.session.commit()
    #db.session.close()
    results = Member.query.all()
    return results[0].username + ' ' + results[0].email

@web.route('/')
def home():
    return render_template('index.html')

@web.route('/login')
def login():
    pass

@web.route('/logout')
def logout():
    pass

@web.route('/register', methods = ['GET', 'POST'])
def register():
<<<<<<< HEAD
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		zipcode = request.form['zipcode']
		member = Member(username, password, firstname, lastname, email, zipcode)
		db.session.add(member)
		db.session.commit()
    return(render_template("register.html"))

=======
    return render_template("register.html")
>>>>>>> ccccf7c386439e8d24822a8e89f203b987721cb1

@web.route('/search')
def search():
    pass


@web.route('/create')
def create():
    pass

@web.route('/view_events')
def view_events():
    pass
<<<<<<< HEAD

=======
>>>>>>> ccccf7c386439e8d24822a8e89f203b987721cb1
