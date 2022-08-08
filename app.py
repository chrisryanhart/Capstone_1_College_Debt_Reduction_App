from crypt import methods
from logging import exception
from flask import Flask, render_template, request, jsonify, g
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from random import SystemRandom, randint
# import requests
# import json
import os

from forms import SearchForm

CURR_USER_KEY = "curr_user"

# https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/NaPali_overlook_Kalalau_Valley.jpg/1024px-NaPali_overlook_Kalalau_Valley.jpg

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///college_app'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

# connect_db(app)


# better to 

# logout user

# login user

# could allow user to search 1 or 2 times before forcing account creation


@app.route('/')
def show_home_page():

    # if user logged in show homepage
    # homepage/dashboard should show if logged in 
    # dashboard should include past searches and provide option for new search


    # else invite user to sign up or login

    return render_template('base.html')


# create new user 

@app.route('/newUser')
def create_new_user():

    return render_template


# conduct searches 
# handle search on the front end with AJAX?  

# get major and school lists or store in database? 
# retrieving from API will ensure schools and majors stay up to date

# can give users options for fields they'd like to search

@app.route('/search')
def search_schools_majors():
    # All school and major combos will have to be preloaded

    # show form with multi-add majors and schools
    # when they type, the majors update; school choices will be refined


    # if blank, show form with different fields they can include

    return render_template('/search.html')


@app.route('/user/searches')
def show_user_searches():

    # retreive stored searches from db

    return render_template()