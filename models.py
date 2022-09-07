# from flask import Flask 
from enum import unique
from tokenize import ContStr
from unicodedata import name
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

# done
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), unique=True, nullable=False)
    home_state_id = db.Column(db.Integer,db.ForeignKey("states.id"))
    household_income_id = db.Column(db.Integer, db.ForeignKey("household_incomes.id"))

    # user_saved_queries = db.relationship('UserQuerySave', backref='user')
    states = db.relationship('State',backref='user')
    household_incomes = db.relationship('HouseholdIncome',backref='user')

    # searches = db.relationship('Search', secondary= 'users_searches', backref='users')

    def __repr__(self):
        return f'Username: {self.username}'

# done
class Major(db.Model):
    __tablename__ = "majors"

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)

    # make a through relationship
    schools = db.relationship('School',secondary='schools_majors',backref='majors')

# done
class HouseholdIncome(db.Model):
    __tablename__ = "household_incomes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    household_income = db.Column(db.String, nullable=False)

# done
class School(db.Model):
    __tablename__= "schools"

    id = db.Column(db.String,unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer,db.ForeignKey("states.id"), nullable=False)

    states = db.relationship('State',backref='schools')

# done
class SchoolMajor(db.Model):
    __tablename__= "schools_majors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.String,db.ForeignKey("schools.id")) 
    major_id = db.Column(db.String,db.ForeignKey("majors.id")) 

    # schools = db.relationship('School',backref="schools_majors")
    # majors = db.relationship('Major',backref="schools_majors")

    # states = db.relationship('State', backref='saved_queries')

# obsolete
# done
# class Credential(db.Model):
#     __tablename__ = "credentials"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String, unique=True, nullable=False)

# done
class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2), unique=True, nullable=False)

# done
class TuitionType(db.Model):
    __tablename__ = "tuition_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tuition_type = db.Column(db.String, nullable = False)

# done
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

# class QuerySave(db.Model):
#     __tablename__ = "saved_queries"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     program_finance_id = db.Column(db.Integer, db.ForeignKey("program_finances.id"), nullable=False)

#     users = db.relationship('User',secondary="users_saved_queries", backref='saved_queries')
#     schools = db.relationship('School', backref='saved_queries')
#     majors = db.relationship('Major', backref='saved_queries')
#     program_finances = db.relationship('ProgramFinance',backref='saved_queries')
    # could add program_finances if desired





# class UserQuerySave(db.Model):
#     __tablename__ = "users_saved_queries"

#     # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     query_id = db.Column(db.Integer,db.ForeignKey("saved_queries.id"),primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey("users.id"),primary_key=True)



# populated by get request to API; updates each new session
# class SchoolCost(db.Model):
#     __tablename__ = "school_costs"

#     id = db.Column(db.Integer, primary_key=True)
#     school_id = db.Column(db.String, db.ForeignKey("schools.id"))
#     in_state_cost = db.Column(db.Integer)
#     out_of_state_cost = db.Column(db.Integer)
#     household_income_id = db.Column(db.Integer, db.ForeignKey("household_incomes.id"))

# class QuerySave(db.Model):
#     __tablename__ = "saved_queries"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     school_cost_id = db.Column(db.Integer, db.ForeignKey("school_costs.id"))
#     program_id = db.Column(db.Integer)
#     residency_state_id = db.Column(db.Integer, db.ForeignKey("states.id"))
#     annual_cash_payment = db.Column(db.Integer)
    # major_id = db.Column(db.String, db.ForeignKey("majors.id"))
    # degree_level_id = db.Column(db.Integer, db.ForeignKey("degrees.id"))
    # household_income = db.Column(db.Integer)
    # annual_cost = db.Column(db.Integer)
    # earnings = db.Column(db.Integer)


# class Program(db.Model):
#     __tablename__ = "programs"

#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     major_id = db.Column(db.Integer,db.ForeignKey("majors.id"))
#     credential_id = db.Column(db.Integer, db.ForeignKey("credentials.id"))
#     expected_earnings = db.Column(db.Integer)



# class UserSearch(db.Model):
#     __tablename__ = "users_searches"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
#     search_id = db.Column(db.Integer, db.ForeignKey("searches.id"))






# user_searches
# this should appear in the dashboard


# multi-search?
# should I itemize each the searches 


# These may not need to be stored in my database
# schools
# majors
