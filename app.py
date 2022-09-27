from crypt import methods
from logging import exception

from flask import Flask, render_template, request, jsonify, g, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm

from random import SystemRandom, randint
import requests
import json
import os

from models import HouseholdIncome, ProgramFinance, TuitionType, db, connect_db, User, School, Major, State, SchoolMajor
from forms import SearchForm, AddUserForm, LoginForm, EditUserForm
from utilities import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# app.run(debug = False)

# app.config['DEBUG_TB_ENABLED'] = False

API_key = os.getenv('API_key')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///college_app'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def show_home_page():


    if 'user_id' in session:

        # pull search results from the local database
        # add messages for user to add new stories if he has none

        user = User.query.filter_by(id=session['user_id']).first()

        program_finances = user.program_finances

        data = retrieve_program_finances(program_finances)

        return render_template('savedQueries.html', user=user, data=data)

    return render_template('welcome.html')


# create new user 
@app.route('/signup', methods=["GET","POST"])
def create_new_user():

    form = AddUserForm()

    form_status = False

    # Verify username not already taken
    if form.validate_on_submit():
        form_status = True
        
        new_username = request.form['username']

        preexisting_user= User.query.filter_by(username=new_username).first()
        
        if preexisting_user != None:
            form_status = False
            form.username.errors = ['Username already taken!']
        
    
    if form_status:

        username = request.form['username']
        password = request.form['password']

        # use bcrypt to store encrypted password
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        state = request.form['state']
        household_income = request.form['household_income']

        state_inst = State.query.filter_by(name=state).first()
        household_income_inst = HouseholdIncome.query.filter_by(household_income=household_income).first()

        # store encrypted password in db
        user = User(username=username, password=pw_hash, home_state_id=state_inst.id, household_income_id=household_income_inst.id)

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
     
        return redirect('/')
    
    # Provide states for datalist options
    states = State.query.all()

    return render_template('signup.html',form=form, states=states)

@app.route('/userProfile',methods=['GET','POST'])
def edit_user():
    if 'user_id' not in session:
        flash('Must log in to edit a user!')
        return redirect('/')

    form = EditUserForm()

    if form.validate_on_submit():

        username = request.form['username']
        home_state = request.form['state']
        household_income = request.form['household_income']

        user = User.query.filter_by(username=username).first()

        if user == None:
            flash('Invalid username')
            return redirect('/userProfile')

        password_candidate = request.form['password']
        hashed_pw = user.password

        # confirm password attempt matches encrypted password
        password_check = bcrypt.check_password_hash(hashed_pw,password_candidate)

        if not password_check:
            flash('Username/password combination incorrect')
            return redirect('/userProfile')

        home_state_inst = State.query.filter_by(name=home_state).first()
        home_state_id = home_state_inst.id

        household_income_inst = HouseholdIncome.query.filter_by(household_income=household_income).first()
        household_income_id = household_income_inst.id


        user.home_state_id = home_state_id
        user.household_income_id = household_income_id
            
        db.session.add(user)
        db.session.commit()

        flash('User profile updated!')

        return redirect('/')

    states = State.query.all()

    # Populate form with existing user data
    user = User.query.filter_by(id=session['user_id']).first()

    form.username.data = user.username
    form.state.data = user.states.name
    form.household_income.data = user.household_incomes.household_income

    return render_template('editUser.html',form=form, states=states)


@app.route('/logout')
def logout_user():
    if 'user_id' not in session:
        flash('No user logged in!')
        return redirect('/')

    session.pop('user_id')

    return redirect('/')

@app.route('/login', methods=["GET","POST"])
def login_user():

    form = LoginForm()
    
    if form.validate_on_submit():

        username = request.form['username']
        password_candidate = request.form['password']


        user = User.query.filter_by(username=username).first()

        if user == None:
            flash('Invalid username')
            return redirect('/login')

        hashed_pw = user.password

        # confirm password attempt matches encrypted password in database
        password_check = bcrypt.check_password_hash(hashed_pw,password_candidate)

        if not password_check:
            flash('Username/password combination incorrect')
            return redirect('/login')
       

        session['user_id'] = user.id
        
        return redirect('/')

    return render_template('login.html', form=form)


@app.route('/search', methods=['GET','POST'])
def search_schools_majors():

    if 'user_id' not in session:
        flash('User not logged in')
        return redirect('/')

    form = SearchForm()

    form_status = False

    if form.validate_on_submit():
        form_status = True
        
        # extract form data
        school_name = request.form['school1']
        school_state = request.form['school_state']
        major_title = request.form['major1']

        # get instances of model classes
        major_inst = Major.query.filter_by(title=major_title).first()
        state_inst = State.query.filter_by(name=school_state).first()
        school_state = state_inst.name
        school_inst = School.query.filter_by(name=school_name,state_id=state_inst.id).first()
        
        # verify schools and majors exist with the selected criteria
        if school_inst == None:
            form_status = False
            form.school_state.errors = ['School is not located in the state selected. Select state from dropdown list.']
        
        elif major_inst not in school_inst.majors:
            form_status = False
            form.major1.errors = ['Major not available at selected school. Select available school from the dropdown list.']
      
    if form_status:

        data = {}

        user = User.query.filter_by(id=session['user_id']).first()

        # Retrieve and define search data
        home_state = user.states.name
        household_income = user.household_incomes.household_income
        major_name = request.form['major1']
        degree_id = 3
        degree_name = 'Bachelors Degree'
        
        major = Major.query.filter_by(title=major_name).first()

        # store results to data
        data['degree'] = degree_name
        data['degree_id'] = degree_id
        data['major'] = major_name
        # 
        data['state'] = home_state     
        # 
        data['household_income'] = household_income
        data['school_state'] = school_state
        data['school'] = school_inst.name
        
        resp = call_college_API(school_inst.id,major.id,school_state,household_income,home_state,degree_id,data,API_key)

        return render_template('results.html',data=resp, form=form)

    # Provide lists for dynamic datalist options
    schools = School.query.order_by(School.name).all()
    school_list = [item.name for item in schools]

    unique_school_list = list(set(school_list))
    unique_school_list.sort()

    majors = Major.query.order_by(Major.title).all()
    states = State.query.all()

    return render_template('/search.html',form=form,schools=unique_school_list,majors=majors, states=states)


@app.route('/API/saveSearch',methods=['POST'])
def save_search_result():

    if 'user_id' not in session:
        flash('No user logged in')
        return redirect('/')
    
    data = json.loads(request.data)

    if 'user_id' in session:
        curr_user = User.query.filter_by(id=session['user_id']).first()

        if data['check_status']:

            # extract data from JS AJAX request
            school_name = data['school']
            major_title = data['major']
            school_state = data['school_state']
            cost = data['cost']
            income_yr1 = data['income_yr1']
            income_yr2 = data['income_yr2']
            income_yr3 = data['income_yr3']
            tuition_type = data['tuition_type']

            # Create instances from form data 
            tuition_type_inst = TuitionType.query.filter_by(tuition_type=tuition_type).first()
            state_inst = State.query.filter_by(name=school_state).first()
            school_inst = School.query.filter_by(name=school_name,state_id=state_inst.id).first()
            major_inst = Major.query.filter_by(title=major_title).first()

            # Use above instances to create new program finance and commit to db
            new_program_finance = ProgramFinance(user_id=session['user_id'], school_id=school_inst.id, major_id=major_inst.id, cost=cost,year_1_income=income_yr1,year_2_income=income_yr2,year_3_income=income_yr3,tuition_type_id=tuition_type_inst.id)

            db.session.add(new_program_finance)
            db.session.commit()

            data = {
                'program_finance_id': new_program_finance.id,
                'status': 'Program finance added to database'
            }

            return jsonify(data)

        # If form checkbox was initially checked upon clicking, delete the entry from the database 
        elif data['check_status'] == False:
            
            # get program_finance_id from hidden input on the table
            program_finance_id = data['program_finance_id']

            program_finance = ProgramFinance.query.filter_by(id=program_finance_id).first()
            db.session.delete(program_finance)
            db.session.commit()

            data = {
                'program_finance_id': program_finance_id,
                'status': 'Program finance deleted from database'
            }

            return jsonify(data)



@app.route('/API/findMajors', methods=['GET'])
def find_majors_of_schools():

    if 'user_id' not in session:
        flash('No user logged in')
        return redirect('/')
    
    major_list = []
    state_list = []

    # Retrieve school input
    textbox_val = request.args['school']

    # Reset datalist options to all majors and states when school input removed 
    if len(textbox_val) == 0:

        # Gather all major titles for datalist options
        all_majors = Major.query.all()

        for major in all_majors:
            major_list.append(major.title)

        major_list.sort()

        # Gather all state names for datalist options
        all_states = State.query.all()
        for state in all_states:
            state_list.append(state.name)
        
        state_list.sort()

        # Send data to update DOM 
        data = {
            'type': 'all_majors',
            'major_list': major_list,
            'state_list': state_list
        }
        return jsonify(data)
    
        # Update major list if number of schools from the db query is less than 2 or no match
    school_query = School.query.filter_by(name=textbox_val).all()
    if len(school_query) > 2 or len(school_query)==0:
        return 'No update required'

    else:

        for school in school_query:
            state_list.append(school.states.name)
            for major in school.majors:
                major_list.append(major.title)
        
        # Remove duplicates
        unique_states = list(set(state_list))
        unique_search_majors = list(set(major_list))
        
        unique_search_majors.sort()
        unique_states.sort()

        # Send data to front-end for DOM update
        data = {
            'type': 'select',
            'major_list': unique_search_majors,
            'state_list': unique_states
            }

        return jsonify(data)
    

@app.route('/API/findSchools', methods=['GET'])
def find_schools_of_a_major():
    if 'user_id' not in session:
        flash('No user logged in')
        return redirect('/')
    state_list = []
    school_list = []
    unique_school_names = []

    # Retrieve major input from form
    textbox_val = request.args['major']
    school_input = request.args['school']

    # if school already been selected, don't update schools
    school_query = School.query.filter_by(name=school_input).all()

    if len(school_query) == 1 or len(school_query) == 2:
        return 'No update required'

    # If input field reset, update datalist options with all school names and states
    if len(textbox_val) == 0:
        all_schools = School.query.all()

        for school in all_schools:
            school_list.append(school.name)
        
        unique_school_names = list(set(school_list))
        unique_school_names.sort()

        all_states = State.query.all()
        for state in all_states:
            state_list.append(state.name)
        
        state_list.sort()

        data = {
            'type': 'all_schools',
            'school_list': unique_school_names,
            'state_list': state_list
        }

        return jsonify(data)
    
    name = "%{}%".format(textbox_val)
    major_list = Major.query.filter(Major.title.like(name)).all()

    # if major list not small enough, don't update schools
    if len(major_list) > 2 or len(major_list)==0:
        return 'No update required'

    else:
        # update schools with the available major
        for major in major_list:
            for school in major.schools:
                school_list.append(school.name)
                state_list.append(school.states.name)

        unique_school_names = list(set(school_list))
        unique_state_names = list(set(state_list))
        
        unique_school_names.sort()
        unique_state_names.sort()

        data = {
            'type': 'selected',
            'school_list': unique_school_names,
            'state_list': unique_state_names
            }

        return jsonify(data)


