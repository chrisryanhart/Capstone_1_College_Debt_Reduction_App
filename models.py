from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from app import app, db

db = SQLAlchemy(app)

db.create_all()



# users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'Username: {self.username}'

# searches 


# user_searches
# this should appear in the dashboard


# multi-search?
# should I itemize each the searches 


# These may not need to be stored in my database
# schools
# majors
