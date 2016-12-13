import re
from datetime import datetime, timedelta
from passlib.hash import bcrypt_sha256 as bcrypt
from flask import *
from models import db, Member, Friend, AGroup, Interest, InterestedIn, BelongsTo, Location, AnEvent, Organize, SignUp, About
from sqlalchemy import and_
from utils import populate_groups, check_authorized

web = Blueprint('web', __name__)

@web.route('/')
def index():
	current_time = datetime.utcnow()
	within_time = current_time + timedelta(3) # current time + 3 days
        events = AnEvent.query.filter(and_(AnEvent.start_time == current_time, AnEvent.end_time == within_time))
        db.session.close()
        return render_template('index.html', events=events)

@web.route('/home', methods = ['GET'])
def home():
    try:
        if session['auth']:
            current_time = datetime.utcnow()
            within_time = current_time + timedelta(3) # current time + 3 days
            events = AnEvent.query.join(SignUp, SignUp.event_id ==  AnEvent.event_id).filter(and_(AnEvent.start_time == current_time, AnEvent.end_time == within_time, SignUp.username == session['username']))
            db.session.close()
            return render_template('home.html', events=events)
    except:
        pass
    return redirect(url_for('web.login'))

@web.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        if session['auth']:
            return redirect(url_for('web.home'))
    except:
        pass

    if request.method == 'POST' and len(request.form) == 2:
	username = request.form['username']
	member = Member.query.filter_by(username=username).first()
        db.session.close()
	if member:
            if bcrypt.verify(request.form['password'], member.password):
                session['auth'] = True
		session['username'] = member.username
                session['firstname'] = member.firstname
                session['lastname'] = member.lastname
                session['groups'] = populate_groups(session['username'])

                return redirect(url_for('web.home'))
            else:
                return render_template('login.html', error='Username or password is incorrect')
        else:
            return render_template('login.html', error='Username does not exist')
    else:
        return render_template('login.html')

@web.route('/logout')
def logout():
    try:
        if session['auth']:
            session.clear()
            return redirect(url_for("web.login"))
    except:
        return redirect(url_for('web.login'))

@web.route('/register', methods = ['GET', 'POST'])
def register():
    try:
        if session['auth']:
            return redirect(url_for('web.home'))
    except:
        pass

    if request.method == 'POST' and len(request.form) == 6:
        errors = []
        firstname = request.form['first-name']
        lastname = request.form['last-name']

        if Member.query.filter_by(username=request.form['username']).first():
            errors.append('This username has already been taken')
        else:
            username = request.form['username']

        if len(request.form['zipcode']) == 5:
            try:
                zipcode = int(request.form['zipcode'])
            except:
                errors.append('Invalid zipcode')
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

@web.route('/change_password', methods = ['GET', 'POST'])
def changepassword():
    try:
        if session['auth']:
            pass
    except:
        return redirect(url_for('web.login'))

    if request.method == 'POST' and len(request.form) == 3:
        if request.form['newPassword'] == request.form['confirmPassword']:
            member = Member.query.filter_by(username=session['username']).first()
            if member and bcrypt.verify(request.form['oldPassword'], member.password):
                new_pass = bcrypt.hash(request.form['newPassword'])
                member.change_password(new_pass)
                return redirect(url_for('web.home', success="Password successfully changed"))
            return redirect(url_for('web.home', error="Password could not be changed"))
        else:
            return redirect(url_for('web.home', error="Password change failed, please confirm your current password"))
    return render_template('change_password.html')

@web.route('/events')
def events():
    try:
        if session['auth']:
            pass
    except:
        return redirect(url_for('web.login'))
    events = AnEvent.query.all()
    if request.args.get('search'):
        events = AnEvent.query.join(Organize, AnEvent.event_id == Organize.event_id).join(About, Organize.group_id == About.group_id).filter_by(keyword=request.args.get('search'))
    elif request.args.get('search_zip'):
        try:
            if len(request.args.get('search_zip')) == 5:
                events = AnEvent.query.filter_by(zipcode=int(request.args.get('search_zip')))
            else:
                return render_template('events.html', error='Not Valid Zipcode', username=session['username'])
        except:
            return render_template('events.html', error='Not Valid Zipcode', username=session['username'])
    else:
        events = AnEvent.query.join(Organize, AnEvent.event_id == Organize.event_id).join(About, Organize.group_id == About.group_id).all()
    return render_template('events.html', events=events, username=session['username'])

@web.route('/groups', methods = ['GET'])
def groups():
    try:
        if session['auth']:
            pass
    except:
        return redirect(url_for('web.login'))
    if request.args.get('search'):
        groups = AGroup.query.join(About, AGroup.group_id == About.group_id).filter_by(keyword=request.args.get('search'))
    elif request.args.get('search_zip'):
        try:
            if len(request.args.get('search_zip')) == 5:
                groups = AGroup.query.filter_by(zipcode=int(request.args.get('search_zip')))
            else:
                return render_template('groups.html', error='Not Valid Zipcode', username=session['username'])
        except:
            return render_template('groups.html', error='Not Valid Zipcode', username=session['username'])
    else:
        groups = AGroup.query.join(About, AGroup.group_id == About.group_id).all()
    return render_template('groups.html', groups=groups, username=session['username'])

@web.route('/create_event', methods=['GET','POST'])
def create_event():
    try:
        if session['auth']:
            pass
    except:
        return redirect(url_for('web.login'))

    if request.method == 'POST' and len(request.form) == 8:
        errors = []
        if session['auth']:
            if len(request.form['title']) > 0: title = request.form['title']
            else: errors.append('Title cannot be blank')

            if len(request.form['desc']) > 0: desc = request.form['desc']
            else: errors.append('Description cannot be blank')

            try:
                start = datetime.strptime(request.form['start'],'%Y-%m-%dT%H:%M')
                if start < datetime.now():
                    errors.append("Start time cannot be in the past")
            except:
                errors.append('Not a valid start date')

            try:
                end = datetime.strptime(request.form['end'],'%Y-%m-%dT%H:%M')
                if end < datetime.now() or end <= start:
                    errors.append('End time cannot be in the past or before start time.')
            except:
                errors.append('Not a valid end date')

            if len(request.form['location']) > 0: location = request.form['location']
            else: errors.append('Location cannot be blank')

            if len(request.form['zipcode']) == 5:
                try:
                    zipcode = int(request.form['zipcode'])
                except:
                    errors.append('Invalid zipcode')
            else:
                errors.append('Invalid zipcode')

            try:
                lat = float(request.form['latitude'])
            except:
                errors.append('Invalid latitude')

            try:
                lon = float(request.form['longitude'])
            except:
                errors.append('Invalid longitude')

        if len(errors) > 0:
            return render_template('create_event.html', errors=errors)
        else:
            e = AnEvent(title, desc, start, end, location, zipcode, lat, lon)
            db.session.add(e)
            db.session.commit()
            o = Organize(e.event_id, check_authorized(session['username']))
            db.session.add(o)
            db.session.commit()
            s = SignUp(e.event_id, session['username'])
            db.session.add(s)
            db.session.commit()
            db.session.close()
            return render_template('create_event.html', success='Event was successfully created')
    return render_template('create_event.html')

@web.route('/create_group', methods = ['GET','POST'])
def create_group():
    #try:
    if session['auth']:
        if request.method == "POST" and len(request.form) == 8:
            errors = []
            if len(request.form['name']) == 0:
                errors.append('Group Name too short')
            else:
                name = request.form['name']
            if len(request.form['description']) == 0:
                errors.append('Please Provide a description')
            else:
                description = request.form['description']
            if len(request.form['category']) == 0:
                errors.append('Please Write a Category')
            else:
                category = request.form['category']
            if len(request.form['keyword']) == 0 or ' ' in request.form['keyword']:
                errors.append("Please provide a keyword, No spaces")
            else:
                keyword = request.form['keyword']
            if len(request.form['location']) > 0:
                location = request.form['location']
            else:
                errors.append('Location cannot be blank')
            if len(request.form['zipcode']) == 5:
                try:
                    zipcode = int(request.form['zipcode'])
                except:
                    errors.append('Invalid zipcode')
            else:
                errors.append('Invalid zipcode')

            try:
                lat = float(request.form['latitude'])
            except:
                errors.append('Invalid latitude')

            try:
                lon = float(request.form['longitude'])
            except:
                errors.append('Invalid longitude')
            if len(errors) > 0:
                return render_template('create_group.html', errors=errors)

            group = AGroup(session['username'], name, description, category, keyword, location, zipcode,'','', lat, lon)
            db.session.add(group)
            db.session.commit()
            a = About(group.group_id, category, keyword)
            db.session.add(a)
            db.session.commit()
            b = BelongsTo(group.group_id, session['username'], True)
            db.session.add(b)
            db.session.commit()
            db.session.close()
            session['groups'] = populate_groups(session['username'])
            return render_template('create_group.html', success='Group successfully created')
        else:
            return render_template('create_group.html')
    # except:
    #     return redirect(url_for('web.login'))

@web.route('/signup/<event_id>')
def signup(event_id):
	signup_check = SignUp.query.filter_by(event_id=event_id, username=session['username']).first()
        if not signup_check:
            signup = SignUp(event_id, session['username'])
            db.session.add(signup)
            db.session.commit()
            db.session.close()
            return "Success"
        return "Error"

@web.route('/join/<group_id>')
def join(group_id):
    joined_check = BelongsTo.query.filter_by(group_id=group_id, username=session['username']).first()
    if not joined_check:
        join = BelongsTo(group_id, session['username'], False)
        db.session.add(join)
        db.session.commit()
        db.session.close()
        return "Success"
    return "Error"

@web.route('/rate', methods = ['GET'])
def rate():
    try:
        if session['auth']:
            pass

    except:
        return redirect(url_for('web.login'))
    if request.args.get('eid') and request.args.get('rating'):
        eid = request.args.get('eid')
        rating = request.args.get('rating')
        e = SignUp.query.filter_by(event_id=eid, username=session['username']).first()
        if e:
            e.rate(int(rating))
            db.session.commit()
            db.session.close()
            return 'Success'
    return 'Error'
