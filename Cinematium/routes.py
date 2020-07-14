from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, login_required, \
                        logout_user, current_user

from Cinematium import app, bcrypt, db
from Cinematium.forms import RegisterForm, LoginForm

from Cinematium.models import User

# main
@app.route('/')
def index():
    return render_template('index.html', title="Home")

# user
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        u = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(u)
        db.session.commit()
        flash('Account Created Successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title="Register" ,form=form)

# user
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful, Please check your email!', 'warning')

    return render_template('login.html', title="Login" ,form=form)

#user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out Successfully', 'success')
    return redirect(url_for('index'))

#user
@app.route('/profile')
@login_required
def profile():
    return "Profile"
