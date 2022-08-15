# from flask import Flask 
from enum import unique
from wsgiref.validate import validator
import bcrypt
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
# from app import app, db

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

# users
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)

    searches = db.relationship('Search', secondary= 'users_searches', backref='users')

    def __repr__(self):
        return f'Username: {self.username}'

class Search(db.Model):
    __tablename__ = "searches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"))
    major_id = db.Column(db.Integer, db.ForeignKey("majors.id"))
    degree_level_id = db.Column(db.Integer, db.ForeignKey("degrees.id"))
    residency_state_id = db.Column(db.Integer, db.ForeignKey("states.id"))
    household_income = db.Column(db.Integer)
    cash = db.Column(db.Integer)
    annual_cost = db.Column(db.Integer)
    earnings = db.Column(db.Integer)

# populated by get request to API; updates each new session
class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String, unique=True, nullable=False)

# populated by get request to API; updates each new session
# enhanced performance if I update these as maintenance on set intervals?

class Major(db.Model):
    __tablename__ = "majors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    major = db.Column(db.String, unique=True, nullable=False)


class Degree(db.Model):
    __tablename__ = "degrees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    degree = db.Column(db.String, unique=True, nullable=False)


class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String(2), unique=True, nullable=False)

class UserSearch(db.Model):
    __tablename__ = "users_searches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    search_id = db.Column(db.Integer, db.ForeignKey("searches.id"))






# user_searches
# this should appear in the dashboard


# multi-search?
# should I itemize each the searches 


# These may not need to be stored in my database
# schools
# majors
