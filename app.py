from flask import Flask, render_template,\
                 url_for, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy

from forms import RegisterForm, LoginForm


db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


#<------------------------>
#|         MODELS         |
#<------------------------>


# """
# Post:
#     title     : String
#     content   : String
#     headerImg : String( URL )
#     views     : Integer
#     hearts    : Integer
#     comments  : <Comment Object>

# Comment:
#     timestamp : <Datetime Object>
#     author    : String
#     message   : String
#     replies   : <List of Comment Objects>
#     hearts    : Integer
# """

class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Category(Base):
    name = db.Column(db.String(80), nullable=False, unique=True)
    posts = db.relationship('Post', backref='category', lazy=True)

class User(Base):
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    is_super = db.Column(db.Boolean, default=False, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)

class Post(Base):
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    headerImg = db.Column(db.Text, nullable=False, default='default.png')
    views = db.Column(db.Integer, nullable=False, default=0)
    hearts = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)


class Comment(Base):
    message = db.Column(db.String(100), nullable=False)
    hearts = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref='parent', lazy='dynamic')

#<------------------------>
#|         ROUTES         |
#<------------------------>

# main
@app.route('/')
def index():
    return render_template('index.html', title="Home")

# user
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', title="Register" ,form=form)

# user
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', title="Login" ,form=form)




if __name__ == '__main__':
    app.run()
