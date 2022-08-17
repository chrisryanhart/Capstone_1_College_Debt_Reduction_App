from crypt import methods
from logging import exception

from flask import Flask, render_template, request, jsonify, g, redirect, session
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm

from random import SystemRandom, randint
import requests
import json
import os

from models import db, connect_db, User, Search, School, Major, Degree, State, UserSearch
from forms import SearchForm, AddUserForm, LoginForm
from secret import API_key

CURR_USER_KEY = "curr_user"

# https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/NaPali_overlook_Kalalau_Valley.jpg/1024px-NaPali_overlook_Kalalau_Valley.jpg

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///college_app'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# better to 

# logout user

# login user

# could allow user to search 1 or 2 times before forcing account creation


@app.route('/')
def show_home_page():

    # if user logged in show homepage

    if 'user_id' in session:

        user = User.query.get(session['user_id'])


        return render_template('userProfile.html', user=user)
    # homepage/dashboard should show if logged in 
    # dashboard should include past searches and provide option for new search


    # else invite user to sign up or login

    return render_template('welcome.html')


# create new user 

@app.route('/signup', methods=["GET","POST"])
def create_new_user():

    # provide new user form
    form = AddUserForm()
    
    if form.validate_on_submit():

        username = request.form['username']
        password = request.form['password']

        # convert password with bcrypt
        # store new user/password in db

        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        # add user to the global var
        
        return redirect('/')


    return render_template('signup.html',form=form)

@app.route('/logout')
def logout_user():

    # try pop.  Will cause error if logged in.  Change so that only logged can see logout
    session.pop('user_id')

    return redirect('/')

@app.route('/login', methods=["GET","POST"])
def login_user():

    # provide login form

    form = LoginForm()
    
    if form.validate_on_submit():

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        session['user_id'] = user.id
        
        return redirect('/')

    # if form.validate_on_submit()

    return render_template('login.html', form=form)


@app.route('/search', methods=['GET','POST'])
def search_schools_majors():
    # All school and major combos will have to be preloaded

    # show form with multi-add majors and schools
    # when they type, the majors update; school choices will be refined

    form = SearchForm()

    if form.validate_on_submit():

        data = {}

        # school cost based on income.  Will change the data structure.  

        # id will change based on desired school
        # can search multiple school costs with one git request by adding to the id
        # form will have to accept multiple form values; may need a dynamic form if wanting to add multiple schools

        # have to loop through the number of form fields and add school ids to the list

        state = request.form['state']
        data['state'] = state

        school1_name = request.form['school1']
        data['school'] = school1_name


        school1 = School.query.filter_by(school=school1_name).first()
        school1.id

        # school2 = request.form['school2']


        school_ids = [school1.id]
        # school_ids = [157085,157289]

        # lst = [8,9,4,1]
        # s = ",".join([str(i) for i in school_ids])
        # print(s)


        payload = {"id": f"{school_ids[0]}", "_fields": "id,school.name,latest.cost,latest.school.ownership,latest.school.state", "api_key": f"{API_key}"}
        # print(r.url)

        cost_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json', params=payload)

        # cost_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json?id=157085&_fields=latest.cost.net_price,id,school.name&api_key={API_key}')

        cost_data = cost_resp.json()

        school_state = cost_data['results'][0]['latest.school.state']
        ownership = cost_data['results'][0]['latest.school.ownership']

        # verify tuition is out of state and public
        if state != school_state and ownership == 1:
            out_of_state_tuition = cost_data['results'][0]['latest.cost.tuition.out_of_state']
            books = cost_data['results'][0]['latest.cost.booksupply']
            roomboard = cost_data['results'][0]['latest.cost.roomboard.oncampus']
            misc_expense = cost_data['results'][0]['latest.cost.otherexpense.oncampus']
            
            total_out_of_state_cost = out_of_state_tuition + roomboard + books + misc_expense

            data['tuition'] = total_out_of_state_cost



        # include option to not accept student aid (in-state total cost without aid)

        # Make dynamic based on household income level form input
        household_income = '0-30000'
        data['household_income'] = household_income
        
        # Verify school is private (not public)
        if ownership != 1:
            private_net_cost = cost_data['results'][0][f'latest.cost.net_price.private.by_income_level.{household_income}']
            data['tuition'] = private_net_cost

        if state == school_state and ownership == 1:
            net_in_state_public_cost = cost_data['results'][0][f'latest.cost.net_price.public.by_income_level.{household_income}']
            data['tuition'] = net_in_state_public_cost

        # may to have to revise given that there could be multiple requests per search

        major_name = request.form['major1']
        data['major'] = major_name

        major = Major.query.filter_by(major=major_name).first()

        # make degree dynamic with user input
        degree = 3
        degree_name = 'Bachelors'
        data['degree'] = degree_name

        major_params = {
            'id':f'{school1.id}','latest.programs.cip_4_digit.credential.level':f"{degree}", 'latest.programs.cip_4_digit.code':major.id, 
            '_fields':'id,school.name,latest.programs.cip_4_digit.earnings.highest.1_yr.overall_median_earnings,latest.programs.cip_4_digit.earnings.highest.2_yr.overall_median_earnings,latest.programs.cip_4_digit.earnings.highest.3_yr.overall_median_earnings',
            "api_key": f"{API_key}"
            }
        # payload = {"id": f"{school_ids[0]}", "_fields": "id,school.name,latest.cost,latest.school.ownership,latest.school.state", "api_key": f"{API_key}"}

        earnings_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json', major_params)

        # earnings_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json?id=157085&latest.programs.cip_4_digit.code=1419&_fields=latest.programs.cip_4_digit,id,school.name&api_key={API_key}')

        earnings_data = earnings_resp.json()

        yr_1_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['1_yr']['overall_median_earnings']
        yr_2_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['2_yr']['overall_median_earnings']
        yr_3_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['3_yr']['overall_median_earnings']

        data['yr_1_earnings'] = yr_1_earnings
        data['yr_2_earnings'] = yr_2_earnings
        data['yr_3_earnings'] = yr_3_earnings
        

        session['data'] = data

        return redirect('/search/results')

    return render_template('/search.html',form=form)

@app.route('/search/results')
def show_search_results():

    data = session['data']

    # if user likes the data, store the search results
    # stay on same page 


    return render_template('results.html',data=data)


@app.route('/user/profile')
def show_user_searches():

    # retreive stored searches from db

    return render_template()


@app.route('/API/saveSearch',methods=['POST'])
def save_search_result():

    data = json.loads(request.data)


    # extract form data

    # if checkbox checked, save data

    # if checkbox unchecked, delete instance

    # Create model instance
    # commit to database


    return 'Save successful'