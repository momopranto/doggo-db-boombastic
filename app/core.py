from flask import *

web = Blueprint('web', __name__)

@web.route('/')
def home():
    return render_template('index.html')

# @web.route('/login')
# def login():
#     pass

@web.route('/logout')
def logout():
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

<<<<<<< HEAD
@web.route('/view_events')
def view_events():
    pass
#AssertionError: View function mapping is overwriting an existing endpoint function: web.login
=======
>>>>>>> 75167887b52794dca9b0d5e6a076b29ab9187d8f
