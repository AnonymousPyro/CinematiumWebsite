from flask import Flask, render_template,\
                 url_for, flash, redirect

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

from Cinematium.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
admin = Admin(app)
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

from Cinematium import routes
