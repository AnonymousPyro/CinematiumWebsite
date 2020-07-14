from Cinematium import admin, db
from flask_admin.contrib.sqla import ModelView

from datetime import datetime

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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    is_super = db.Column(db.Boolean, default=False, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    headerImg = db.Column(db.Text, nullable=False, default='default.png')
    views = db.Column(db.Integer, nullable=False, default=0)
    hearts = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.String(100), nullable=False)
    hearts = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(80), nullable=False, unique=True)
    posts = db.relationship('Post', backref='category', lazy=True)


class PostView(ModelView):
    form_widget_args = dict(content={'class': 'form-control ckeditor'})

    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'

admin.add_view(ModelView(Category, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
