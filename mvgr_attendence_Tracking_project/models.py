from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    idno = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)

class Students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    idno = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    sub1 = db.Column(db.Integer)
    sub2 = db.Column(db.Integer)
    sub3 = db.Column(db.Integer)
    sub4 = db.Column(db.Integer)
    sub5 = db.Column(db.Integer)
    sub6 = db.Column(db.Integer)
    sub7 = db.Column(db.Integer)
    sub8 = db.Column(db.Integer)
    sub9 = db.Column(db.Integer)
    sub10 = db.Column(db.Integer)
    sub11 = db.Column(db.Integer)
    sub12 = db.Column(db.Integer)
    tot = db.Column(db.Integer)
    per = db.Column(db.Float)
    year = db.Column(db.Integer)
    sec = db.Column(db.String)
    counseller = db.Column(db.String)

class Subjects(db.Model):
	__tablename__="subjects"
	id = db.Column(db.Integer, primary_key=True)
	sub = db.Column(db.String, nullable=False)
	seca = db.Column(db.Integer)
	secb = db.Column(db.Integer)
	secc = db.Column(db.Integer)
	year = db.Column(db.Integer)

class History(db.Model):
	__tablename__="history"
	id = db.Column(db.Integer, primary_key=True)
	idno = db.Column(db.String, nullable=False)
	first = db.Column(db.Float)
	second = db.Column(db.Float)
	third = db.Column(db.Float)
	fourth = db.Column(db.Float)
	fifth = db.Column(db.Float)
	sixth = db.Column(db.Float)
	seventh = db.Column(db.Float)
	eigth = db.Column(db.Float)
	nineth = db.Column(db.Float)
	tenth = db.Column(db.Float)

class Dates(db.Model):
	__tablename__="dates"
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date, nullable=False)
	year = db.Column(db.Integer)
	tota=db.Column(db.Integer)
	totb=db.Column(db.Integer)
	totc=db.Column(db.Integer)


class Start(db.Model):
	__tablename__="start"
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date, nullable=False)
	year = db.Column(db.Integer)

