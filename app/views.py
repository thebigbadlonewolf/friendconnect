from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm, SignupForm, EditProfileForm
from app.models import User
from datetime import datetime

@app.before_request
def before_request():
    g.user = current_user
    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    user = g.user
    posts = [
        {
            'author': User(username='john77', email='johnsmith@gmail.com'),
            'body': 'Nice weather in Japan!'
        },
        {
            'author': User(username='justsusan', email='susan111@gmail.com'),
            'body': 'A Flower! Lorem ipsum segeeg egaaeg  gaeqew hssrnvc erhrrs geuen usegbhuaegnu uesnghuheus eaguseshunhs seguneusnh gesnuesnhesu hsuhnuehsnh sehuhnueshn uesgunheuhn seunhuesnhu egusneusenh',
            'image': '/static/img/test.jpg'
        }
    ]
    return render_template('index.html', title='Home', user=g.user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # TODO: Add password functionality
        if user is None:
            flash('Account with username %s does not exist!' % form.username.data)
            return redirect(url_for('signup'))
        
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
            
        login_user(user, remember = remember_me)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/explore')
def explore():
    return render_template('explore.html', title='Explore')

@app.route('/friends')
@login_required
def friends():
    return render_template('friends.html', title='Friends')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # TODO: Add password functionality
        if user is None:
            return redirect(url_for('signup'))
        
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
            
        login_user(user, remember = remember_me)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('signup.html', title='Create Account', form=form)
@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found!' % username)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Hey'}
    ]
    action = 'show'
    form = EditProfileForm()
    if g.user is not None and g.user.is_authenticated and not g.user.is_anonymous:
        if user.id == g.user.id:
            if form.validate_on_submit():
                g.user.username = form.username.data
                g.user.bio = form.bio.data
                db.session.add(g.user)
                db.session.commit()
                flash('Your changes have been saved.')
                return redirect('/user/' + g.user.username)
            else:
                form.username.data = g.user.username
                form.bio.data = g.user.bio
            if request.method == 'POST':
                if 'edit' in request.form:
                    action = 'edit'
                else:
                    action = 'show'
    return render_template('user.html', title=user.username, user=user, posts=posts, action=action, form=form)
    return render_template('user.html', title=user.username, user=user, posts=posts, action=action, form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html', title='404'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html', title='500'), 500