import re
from passlib.hash import bcrypt_sha256 as bcrypt
from flask import *
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')

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
