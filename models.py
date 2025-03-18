from exts import db

from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    avatar = db.Column(db.String(500), nullable=True, default="default_avatar.png")
    seeEmail = db.Column(db.Integer, nullable=True, unique=False, default=1)
    balance = db.Column(db.Integer, nullable=True, unique=False, default=0)
    gigs = db.relationship("Gig", backref='author', lazy=True)
    orders = db.relationship("Order", backref = 'buyer',lazy = True)


    # def __repr__(self):
    #     return f"User('{self.username}','{self.email}')"


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Gig(db.Model):
    __tablename__ = "gigs"
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    root_dir = '/Users/azalea/team_16-main'
    pic = db.Column(db.String(500), nullable=True, default=root_dir+"/static/pic/jin.jpg")
    module = db.Column(db.String(100), nullable=False)

    orders = db.relationship("Order", backref='gig', lazy=True)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    requirement = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(10), nullable=False)
    ongoing = db.Column(db.Integer,default=0)
    oncart = db.Column(db.Integer,default = 0)
    finished = db.Column(db.Integer,default = 0)
    gig_id = db.Column(db.Integer, db.ForeignKey('gigs.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class SearchModel(db.Model):
    __tablename__ = "search_model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(200), nullable=False, unique=False)
    search_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, nullable=False)
    num = db.Column(db.Integer, nullable=False,default=0)