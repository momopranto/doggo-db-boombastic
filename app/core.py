from flask import *
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp

web = Blueprint('web', __name__)

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


@web.route('/search')
def search():
    pass


@web.route('/create')
def create():
    pass

@web.route('/view_events')
def view_events():
    pass

