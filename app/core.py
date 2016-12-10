
from flask import *
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
def register_member():
	if request.method == 'POST':
		firstname = request.form['first-name']
		lastname = request.form['last-name']
		zipcode = request.form['zipcode']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		
		member = Member(username, password, firstname, lastname, email, zipcode)
		db.session.add(member)
		db.session.commit()
		db.session.close()
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
