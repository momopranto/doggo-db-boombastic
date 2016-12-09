from flask import *

web = Blueprint('web', __name__)

@web.route('/')
def home():
    return render_template('index.html')

# @web.route('/login')
# def login():
#     pass

@web.route('/logout')
def login():
    pass

@web.route('/register')
def register():
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
#AssertionError: View function mapping is overwriting an existing endpoint function: web.login