# from flask import Flask 
from enum import unique
from tokenize import ContStr
from unicodedata import name
from wsgiref.validate import validator
import bcrypt
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    home_state_id = db.Column(db.Integer,db.ForeignKey("states.id"))
    household_income_id = db.Column(db.Integer, db.ForeignKey("household_incomes.id"))

    # user_saved_queries = db.relationship('UserQuerySave', backref='user')
    states = db.relationship('State',backref='user')
    household_incomes = db.relationship('HouseholdIncome',backref='user')

    # searches = db.relationship('Search', secondary= 'users_searches', backref='users')

    def __repr__(self):
        return f'Username: {self.username}'

class Major(db.Model):
    __tablename__ = "majors"

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)

    # make a through relationship
    schools = db.relationship('School',secondary='schools_majors',backref='majors')

class HouseholdIncome(db.Model):
    __tablename__ = "household_incomes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    household_income = db.Column(db.String, nullable=False)

class School(db.Model):
    __tablename__= "schools"

    id = db.Column(db.String,unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer,db.ForeignKey("states.id"), nullable=False)

    states = db.relationship('State',backref='schools')

class SchoolMajor(db.Model):
    __tablename__= "schools_majors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.String,db.ForeignKey("schools.id")) 
    major_id = db.Column(db.String,db.ForeignKey("majors.id")) 


class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2), unique=True, nullable=False)

class TuitionType(db.Model):
    __tablename__ = "tuition_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tuition_type = db.Column(db.String, nullable = False)

class ProgramFinance(db.Model):
    __tablename__ = "program_finances"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    school_id = db.Column(db.String, db.ForeignKey("schools.id"), nullable=False)
    major_id = db.Column(db.String, db.ForeignKey("majors.id"), nullable=False)
    cost = db.Column(db.String, nullable=False)
    year_1_income = db.Column(db.String)
    year_2_income = db.Column(db.String)
    year_3_income = db.Column(db.String)
    tuition_type_id = db.Column(db.Integer,db.ForeignKey("tuition_types.id"),nullable=False)

    tuition_types = db.relationship('TuitionType', backref='program_finances')
    majors = db.relationship('Major', backref='program_finances')
    schools = db.relationship('School', backref='program_finances')
    users = db.relationship('User', backref='program_finances')


