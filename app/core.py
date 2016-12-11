import re
from datetime import datetime, timedelta
from passlib.hash import bcrypt_sha256 as bcrypt
from flask import *
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp, About
from sqlalchemy import and_

web = Blueprint('web', __name__)

@web.route('/')
def index():
	current_time = datetime.utcnow()
	within_time = current_time + timedelta(3) # current time + 3 days
    	events = AnEvent.query.filter(and_(AnEvent.start_time == current_time, AnEvent.end_time == within_time))
    	return render_template('index.html', events=events)

@web.route('/home', methods = ['GET'])
def home():
	current_time = datetime.utcnow()
	within_time = current_time + timedelta(3) # current time + 3 days
    	events = AnEvent.query.join(SignUp, SignUp.event_id ==  AnEvent.event_id).filter(and_(AnEvent.start_time == current_time, AnEvent.end_time == within_time, SignUp.username == session['username']))
    	return render_template('index.html', events=events)
	

@web.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' and len(request.form) == 2:
	username = request.form['username']
	member = Member.query.filter_by(username=username).first()
	if member:
            if bcrypt.verify(request.form['password'], member.password):
		session['username'] = member.username
                session['firstname'] = member.firstname
                session['lastname'] = member.lastname

                return redirect(url_for('web.home'))
            else:
                return render_template('login.html', error='Username or password is incorrect')
        else:
            return render_template('login.html', error='Username does not exist')
    else:
        return render_template('login.html')

@web.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("web.login"))

@web.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST' and len(request.form) == 6:
        errors = []
        firstname = request.form['first-name']
        lastname = request.form['last-name']

        if Member.query.filter_by(username=request.form['username']).first():
            errors.append('This username has already been taken')
        else:
            username = request.form['username']

        if isinstance(int(request.form['zipcode']), int) and len(request.form['zipcode']) == 5:
            zipcode = int(request.form['zipcode'])
        else:
            errors.append('Invalid zipcode')

        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form['email']):
            if Member.query.filter_by(email=request.form['email']).first():
                errors.append('This email has already been used')
            else:
                email = request.form['email']
        else:
            errors.append('Invalid email')

        if len(request.form['password']) > 0:
            password = bcrypt.hash(request.form['password'])
        else:
            errors.append('Password cannot be blank')

	if len(errors) > 0:
            return render_template('register.html', errors=errors)
	else:
            member = Member(username, password, firstname, lastname, email, zipcode)
            db.session.add(member)
            db.session.commit()
            db.session.close()

            return render_template('login.html', success='Account was successfully created')
    else:
        return render_template('register.html')

@web.route('/events')
def events():
	events = AnEvent.query.all()
    	return render_template('events.html', events=events)

@web.route('/groups')
def groups():
	groups = AGroup.query.join(About, AGroup.group_id == About.group_id).all()
    	return render_template('groups.html', groups=groups)

@web.route('/create_event', methods = ['GET', 'POST'])
def create_event():
	if request.method == "POST" and len(request.form == 5):
		errors = []
		# title = request.form['title']
		# if isinstance(int(request.form['zipcode']), int) and len(request.form['zipcode']) == 5:
  #           zipcode = int(request.form['zipcode'])
  #       else:
  #           errors.append('Invalid zipcode')
    	return render_template('create_event.html')

@web.route('/create_group')
def create_group():
	if request.method == "POST" and len(request.form) == 4:
		name = request.form['name']
		description = request.form['description']
		category = request.form['category']
		keyword = request.keyword['keyword']
		group = AGroup(session['username'], name, description, category, keyword)
		db.session.add(group)
		db.session.commit()
		db.session.close()
    	return render_template('create_group.html')

@web.route('/signup', methods = ['POST'])
def signup():

    return redirect(url_for("web.events"))

@web.route('/rate', methods = ['GET'])
def rate():
    if request.args.get('eid') and request.args.get('rating'):
        eid = request.args.get('eid')
        rating = request.args.get('rating')
        e = SignUp.query.filter_by(event_id=eid).first()
        if e:
            e.rate(rating)
            db.session.commit()
            db.session.close()
            return 'Success'
    return 'Error'
