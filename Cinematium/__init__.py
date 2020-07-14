from flask import Flask, render_template,\
                 url_for, flash, redirect, flash
import click
from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user

from Cinematium.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_super:
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        flash('Put your seatbelts and enjoy the page', 'warning')
        return redirect(url_for('login'))


admin = Admin(app, index_view=MyAdminIndexView())

@click.command('bigbang')
@with_appcontext
def bigbang():
    db.create_all()
    from Cinematium.models import User
    _hash = bcrypt.generate_password_hash('COOL').decode('utf-8')
    u = User(username='admin', email='p.rhubanraj@gmail.com',password=_hash, is_super=True)
    db.session.add(u)
    db.session.commit()

@click.command('destroy')
@with_appcontext
def destroy():
    db.drop_all()

app.cli.add_command(bigbang)
app.cli.add_command(destroy)

from Cinematium import routes
