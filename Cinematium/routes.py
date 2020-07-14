from flask import render_template, url_for, flash, redirect

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
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', title="Login" ,form=form)
