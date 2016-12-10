from hashlib import md5
from flask import *
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp

web = Blueprint('web', __name__)

@web.route('/')
def index():
	return render_template('index.html')

@web.route('/home', methods = ['GET'])
def home():
    return render_template('home.html', username=session['username'])

@web.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		errors = []
		user = request.form['username']
		member = Member.query.filter_by(username=user).first()
		if member:
			if member.password == md5(request.form['password']).hexdigest():
				session['username'] = member.username
				return render_template(redirect(url_for('web.home')))
			else:
				errors.append("Password is incorrect")
		else:
			errors.append("Member does not exist please register")
		if len(errors) > 0:	
    			return render_template('login.html', errors=errors)
    	return render_template('login.html')

@web.route('/logout')
def logout():
    session.clear()
    return render_template("logout.html")

@web.route('/register', methods = ['GET', 'POST'])
def register_member():
	if request.method == 'POST':
		errors = []
		firstname = request.form['first-name']
		lastname = request.form['last-name']
		zipcode = int(request.form['zipcode'])
		email = request.form['email']
		username = request.form['username']
		password = md5(request.form['password']).hexdigest()
		
		username_check = Member.query.filter_by(username=username).first()
		email_check = Member.query.filter_by(email=email).first()
		if username_check:
			errors.append("That username is already taken")
		if email_check:
			errors.append("That email is already registered")
		if len(errors) > 0:
			return render_template('register.html', errors=errors)

		else:
			member = Member(username, password, firstname, lastname, email, zipcode)
			db.session.add(member)
			db.session.commit()
			db.session.close()

			session['username'] = member.username
    		return render_template(redirect(url_for('web.home')))
    	return render_template('register.html')

@web.route('/events')
def events():
    pass

@web.route('/groups')
def groups():
    pass

@web.route('/create_event')
def create_event():
	pass

@web.route('/create_group')
def create_group():
	pass

@web.route('/signup')
def signup():
	pass