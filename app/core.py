from hashlib import md5
from flask import *
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp

web = Blueprint('web', __name__)

@web.route('/')
def home():
    return render_template('index.html')

@web.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		member = Member.query.filter(username=username).first()
		if member:
			if md5(member.password).hexdigest() == request.form['password']:
				#create session
				#relocate to home page
				pass
    	return render_template('login.html')

@web.route('/logout')
def logout():
    pass

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

			#create session
    		return render_template(redirect(url_for('web.register_member')))
    	return render_template('register.html')

@web.route('/search')
def search():
    pass


@web.route('/create')
def create():
    pass

@web.route('/view_events')
def view_events():
    pass
