from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from . import login_manager
from datetime import datetime
from sqlalchemy import text


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    photos = db.relationship('ProfilePhoto', backref = 'user', lazy = 'dynamic')
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id',backref = 'user', lazy='dynamic')
    pass_secure = db.Column(db.String(255))


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def like_post(self,post):
        if not self.has_liked_post(post):
            like = PostLike(user_id, pitches_id = post.id)
            db.session.add(like)

    def unlike_post(self, pitches):
        if self.has_liked_post(pitches):
            PostLike.query.filter_by(user_id=self.id, pitches_id = pitches.id).delete()

    def has_liked_post(self,pitches):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.pitches_id == pitches.id).count() > 0

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy = "dynamic")



    def __repr__(self):
        return f'User {self.name}'


class PostLike(db.Model):
    __tablename__ = 'post_like'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitches_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ProfilePhoto(db.Model):
    __tablename__ = 'profile_photos'
    
    id = db.Column(db.Integer, primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    likes = db.relationship('PostLike', backref ='post', lazy ='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitch(cls, id):
        pitches = Pitch.query.filter_by(id = id).all()
        return pitches

    @classmethod
    def get_pitches(cls, category):
        pitches = Pitch.query.filter_by(category = category).all()
        return pitches

    def __repr__(self):
        return f'Pitch {self.pitch_title}'


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.Text())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable = False)
    pitches_id = db.Column(db.Integer,db.ForeignKey("pitches.id"), nullable = False)


    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitches_id):
        comments = Comment.query.filter_by(post_id = pitches_id).all()
        return comments

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Comments: {self.comment}'