from flask import *

web = Blueprint('web', __name__)

@web.route('/')
def home():
    return render_template('index.html')
