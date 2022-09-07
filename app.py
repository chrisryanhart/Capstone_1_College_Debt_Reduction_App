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
from secret import API_key
from all_majors_seed import unique_major_titles

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

connect_db(app)

# better to 

# logout user

# login user

# could allow user to search 1 or 2 times before forcing account creation


@app.route('/')
def show_home_page():

    # if user logged in show homepage

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

    # provide new user form
    form = AddUserForm()
    
    if form.validate_on_submit():

        username = request.form['username']

        # encrypt plain text password
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        state = request.form['state']
        household_income = request.form['household_income']

        state_inst = State.query.filter_by(name=state).first()
        household_income_inst = HouseholdIncome.query.filter_by(household_income=household_income).first()

        # convert password with bcrypt
        # store new user/password in db
        user = User(username=username, password=pw_hash, home_state_id=state_inst.id, household_income_id=household_income_inst.id)

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        # add user to the global var
        
        return redirect('/')
    
    states = State.query.all()


    return render_template('signup.html',form=form, states=states)

@app.route('/userProfile',methods=['GET','POST'])
def edit_user():


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
            
            # user_update = User(id=user.id,username=username,password=password, home_state_id=home_state_id,household_income_id=household_income_id)
        db.session.add(user)
        db.session.commit()

        # update database with username information

        return redirect('/')

    states = State.query.all()

    # autofill form data 
    # form.choices['username']
    user = User.query.filter_by(id=session['user_id']).first()


    form.username.data = user.username
    form.state.data = user.states.name
    form.household_income.data = user.household_incomes.household_income

    return render_template('editUser.html',form=form, states=states)


@app.route('/logout')
def logout_user():

    # try pop.  Will cause error if logged in.  Change so that only logged can see logout
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

        password_check = bcrypt.check_password_hash(hashed_pw,password_candidate)

        if not password_check:
            flash('Username/password combination incorrect')
            return redirect('/login')

        

        session['user_id'] = user.id
        
        return redirect('/')

    # if form.validate_on_submit()

    return render_template('login.html', form=form)


@app.route('/search', methods=['GET','POST'])
def search_schools_majors():
    # All school and major combos will have to be preloaded

    # show form with multi-add majors and schools
    # when they type, the majors update; school choices will be refined
    if 'user_id' not in session:
        # flash message
        return redirect('/')

    form = SearchForm()

    form_status = False

    if form.validate_on_submit():
        form_status = True

        school1_name = request.form['school1']
        school_state = request.form['school_state']
        major_title = request.form['major1']
        major_inst = Major.query.filter_by(title=major_title).first()
        # check for multiple major names

        state_inst = State.query.filter_by(name=school_state).first()

        
        school_inst = School.query.filter_by(name=school1_name,state_id=state_inst.id).first()
        
        if school_inst == None:
            form_status = False
            form.school_state.errors = ['School is not located in the state selected. Select state from dropdown list.']
        
            # update error message: 'school and state don't match'
            # they can input the wrong state
            # consider using try/except

        elif major_inst not in school_inst.majors:
            form_status = False
            form.major1.errors = ['Major not available at selected school. Select available school from the dropdown list.']
            test = 1


        # if all inputs don't match
        #  form status = False
        # confirm states all match
        # confirm error fields can still be accessed


        test=1
        # return redirect('/search/results')
    
    # query database for majors and schools
    if form_status:

        data = {}

        # school cost based on income.  Will change the data structure.  

        # id will change based on desired school
        # can search multiple school costs with one git request by adding to the id
        # form will have to accept multiple form values; may need a dynamic form if wanting to add multiple schools

        # have to loop through the number of form fields and add school ids to the list
        user = User.query.filter_by(id=session['user_id']).first()

        home_state = user.states.name
    
        data['state'] = user.states.name

        household_income = user.household_incomes.household_income
        data['household_income'] = household_income

        # household_income = request.form['household_income']
        # data['household_income'] = household_income

        # Extract specified state from form input (this is not the user home state)
        school_state = request.form['school_state']
        school_state_inst = State.query.filter_by(name=school_state).first()
        school_state_id = school_state_inst.id
        data['school_state'] = school_state

        school1_name = request.form['school1']
        data['school'] = school1_name

        # state_id should be from user input, not the home state in their profile
        school1 = School.query.filter_by(name=school1_name,state_id=school_state_id).first()


        payload = {"id": f"{school1.id}","school.state": f"{school_state}", "_fields": "id,school.name,latest.cost,latest.school.ownership,latest.school.state", "api_key": f"{API_key}"}
        # print(r.url)

        cost_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json', params=payload)

        # cost_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json?id=157085&_fields=latest.cost.net_price,id,school.name&api_key={API_key}')

        cost_data = cost_resp.json()

        # school_state = cost_data['results'][0]['latest.school.state']
        ownership = cost_data['results'][0]['latest.school.ownership']

        # verify tuition is out of state and public
        if home_state != school_state and ownership == 1:
            out_of_state_tuition = cost_data['results'][0]['latest.cost.tuition.out_of_state']
            books = cost_data['results'][0]['latest.cost.booksupply']
            roomboard = cost_data['results'][0]['latest.cost.roomboard.oncampus']
            misc_expense = cost_data['results'][0]['latest.cost.otherexpense.oncampus']
            
            total_out_of_state_cost = out_of_state_tuition + roomboard + books + misc_expense

            data['tuition'] = total_out_of_state_cost
            data['tuition_type'] = 'Out-of-state'


        # include option to not accept student aid (in-state total cost without aid)

       
        # Verify school is private (not public)
        if ownership != 1:
            private_net_cost = cost_data['results'][0][f'latest.cost.net_price.private.by_income_level.{household_income}']
            data['tuition'] = private_net_cost
            data['tuition_type'] = 'N/A'

        if home_state == school_state and ownership == 1:
            net_in_state_public_cost = cost_data['results'][0][f'latest.cost.net_price.public.by_income_level.{household_income}']
            data['tuition'] = net_in_state_public_cost
            data['tuition_type'] = 'In-state'

        # may to have to revise given that there could be multiple requests per search

        major_name = request.form['major1']
        data['major'] = major_name

        major = Major.query.filter_by(title=major_name).first()

        # make degree dynamic with user input
        degree = 3
        degree_name = 'Bachelors Degree'
        data['degree'] = degree_name
        data['degree_id'] = 3

        major_params = {
            'id':f'{school1.id}','latest.programs.cip_4_digit.credential.level':f"{degree}", 'latest.programs.cip_4_digit.code':f"{major.id}", 
            '_fields':'id,school.name,latest.programs.cip_4_digit.earnings.highest.1_yr.overall_median_earnings,latest.programs.cip_4_digit.earnings.highest.2_yr.overall_median_earnings,latest.programs.cip_4_digit.earnings.highest.3_yr.overall_median_earnings',
            "api_key": f"{API_key}"
            }
        # payload = {"id": f"{school_ids[0]}", "_fields": "id,school.name,latest.cost,latest.school.ownership,latest.school.state", "api_key": f"{API_key}"}

        earnings_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json', major_params)

        # earnings_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json?id=157085&latest.programs.cip_4_digit.code=1419&_fields=latest.programs.cip_4_digit,id,school.name&api_key={API_key}')

        earnings_data = earnings_resp.json()

        # if results don't exist, exit function and flash message
        yr_1_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['1_yr']['overall_median_earnings']
        yr_2_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['2_yr']['overall_median_earnings']
        yr_3_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['3_yr']['overall_median_earnings']

        if not yr_1_earnings or yr_1_earnings < 0:
            yr_1_earnings = 'No data available'

        if not yr_2_earnings or yr_2_earnings < 0:
            yr_2_earnings = 'No data available'

        if not yr_3_earnings or yr_3_earnings < 0:
            yr_3_earnings = 'No data available'

        data['yr_1_earnings'] = yr_1_earnings
        data['yr_2_earnings'] = yr_2_earnings
        data['yr_3_earnings'] = yr_3_earnings
        

        return render_template('results.html',data=data, form=form)



    schools = School.query.order_by(School.name).all()
    majors = Major.query.order_by(Major.title).all()
    states = State.query.all()

    # majors = [(major.id,major.title) for major in Major.query.all()]

    # form.major1.choices = majors

    return render_template('/search.html',form=form,schools=schools,majors=majors, states=states)

# @app.route('/search/results', methods=['POST'])
# def show_search_results():
#     data = {}

#     if 'user_id' not in session:
#         # flash message
#         return redirect('/')

#     form = SearchForm()


@app.route('/savedQueries', methods=['GET'])
def show_saved_queries():
    if 'user_id' not in session:
        # flash message
        return redirect('/')

    program_finances = ProgramFinance.query.filter_by(user_id=session['user_id']).all()
    # retreive stored searches from db from the logged in user

    # queries have to be made to get the state, HH_income_id
    # multiple API calls or combine?  
    # function will have to take multiple parameters if combining into one query
    # does combining the query depend on if the major is the same?
    # data = []

    data = retrieve_program_finances(program_finances)

    # data = [query_data]

    # for query in saved_queries:
    #     # as I loop through, I can retrieve the names to add the results screen
    #     school_id = query.school_id
    #     major_id = query.major_id
    #     credential_id = query.credential_id
    #     state = query.states.name
    #     household_income = query.household_incomes.household_income

    #     resp = call_college_API(school_id,major_id,credential_id,state,household_income)

    #     resp['school_name'] = query.schools.name
    #     resp['major_name'] = query.majors.title
    #     resp['credential_title'] = query.credentials.title
        
    #     data.append(resp)

        # loop through results in the template

    return render_template('savedQueries.html', data=data)


def retrieve_program_finances(program_finances):
    data = []

    for program_finance in program_finances:
        program_finance_data = {}
        
        program_finance_data['school_name'] = program_finance.schools.name
        program_finance_data['major_name'] = program_finance.majors.title
        program_finance_data['credential_title'] = 'Bachelors Degree'
        program_finance_data['school_state'] = program_finance.schools.states.name
     
        # program_finance_inst = ProgramFinance.query.get(query.program_finance_id)

        program_finance_data['yr_1_earnings'] = program_finance.year_1_income
        program_finance_data['yr_2_earnings'] = program_finance.year_2_income
        program_finance_data['yr_3_earnings'] = program_finance.year_3_income
        program_finance_data['cost'] = program_finance.cost
        program_finance_data['tuition_type'] = program_finance.tuition_types.tuition_type
        
        # as I loop through, I can retrieve the names to add the results screen
        # school_id = query.school_id
        # major_id = query.major_id
        # credential_id = query.credential_id
        # state = query.states.name
        # household_income = query.household_incomes.household_income

        # resp = call_college_API(school_id,major_id,credential_id,state,household_income)

       
        data.append(program_finance_data)

    return data


@app.route('/API/saveSearch',methods=['POST'])
def save_search_result():
    # have to extract form input data from both Query and Results
    # save to local database
    # state now required

    if 'user_id' not in session:
        # flash message
        return redirect('/')
    
    data = json.loads(request.data)

    if 'user_id' in session:
        curr_user = User.query.filter_by(id=session['user_id']).first()


        if data['check_status']:

            # confirm current user
            # make new entry in the users_queries join table in the database



        #   tuition_type: $tuitionType,
        #   check_status: isChecked


            school_name = data['school']
            major_title = data['major']
            degree_title = data['degree']
            household_income_range = data['household_income']
            home_state_name = data['home_state']

            school_state = data['school_state']
            cost = data['cost']
            income_yr1 = data['income_yr1']
            income_yr2 = data['income_yr2']
            income_yr3 = data['income_yr3']
            tuition_type = data['tuition_type']


            # 1. store program finance entry
            tuition_type_inst = TuitionType.query.filter_by(tuition_type=tuition_type).first()

            state_inst = State.query.filter_by(name=school_state).first()
            school_state_id = state_inst.id

            school_inst = School.query.filter_by(name=school_name,state_id=school_state_id).first()
            school_id = school_inst.id

            major_inst = Major.query.filter_by(title=major_title).first()
            major_id = major_inst.id


            new_program_finance = ProgramFinance(user_id=session['user_id'], school_id=school_id, major_id=major_id, cost=cost,year_1_income=income_yr1,year_2_income=income_yr2,year_3_income=income_yr3,tuition_type_id=tuition_type_inst.id)
            db.session.add(new_program_finance)
            db.session.commit()



            # class ProgramFinance(db.Model):
            #     __tablename__ = "program_finances"

            #     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
            #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
            #     school_id = db.Column(db.String, db.ForeignKey("schools.id"), nullable=False)
            #     major_id = db.Column(db.String, db.ForeignKey("majors.id"), nullable=False)
            #     cost = db.Column(db.Integer, nullable=False)
            #     year_1_income = db.Column(db.Integer)
            #     year_2_income = db.Column(db.Integer)
            #     year_3_income = db.Column(db.Integer)
            #     tuition_type_id = db.Column(db.Integer,db.ForeignKey("tuition_types.id"),nullable=False)


            # 3. Add saved_query to user profile


            # degree_inst = Credential.query.filter_by(title=degree_title).first()
            # degree_id = degree_inst.id

            # new_saved_query = QuerySave(major_id=major_id,school_id=school_id, program_finance_id=new_program_finance.id)
            # db.session.add(new_saved_query)
            # db.session.commit()

            # household_income_inst = HouseholdIncome.query.filter_by(household_income=household_income_range).first()
            # household_income_id = household_income_inst.id

            # home_state_inst = State.query.filter_by(name=home_state_name).first()
            # home_state_id = home_state_inst.id

            # favorite_query = QuerySave(school_id=school_id, major_id=major_id, state_residency_id=home_state_id, credential_id=degree_id, household_income_id=household_income_id)
            # db.session.add(favorite_query)
            # db.session.commit()

            # user_saved_query = UserQuerySave(query_id=new_saved_query.id,user_id=curr_user.id)

            # db.session.add(user_saved_query)
            # db.session.commit()

            # data = {
            #     # 'users_saved_querires_id': user_saved_query.id,
            #     'saved_query_id': new_saved_query.id,
            #     'program_finance_id': new_program_finance.id
            # }

            data = {
                'program_finance_id': new_program_finance.id,
                'status': 'Program finance added to database'
            }

            return jsonify(data)


        elif data['check_status'] == False:
            
            # saved_query_id = data['saved_query_id']
            program_finance_id = data['program_finance_id']
            user_id = session['user_id']

            program_finance = ProgramFinance.query.filter_by(id=program_finance_id).first()
            # user_saved_query = UserQuerySave.query.filter_by(query_id=saved_query_id,user_id=user_id).first()
            # UserQuerySave(query_id=saved_query_id,user_id=user_id)
            db.session.delete(program_finance)
            db.session.commit()

            data = {
                'program_finance_id': program_finance_id,
                'status': 'Program finance deleted from database'
            }

            return jsonify(data)


    return 'success'
unique_major_titles = unique_major_titles

# looks up majors in schools 
@app.route('/API/findMajors', methods=['GET'])
def find_majors_of_schools():
    if 'user_id' not in session:
        # flash message
        return redirect('/')

    school_query = School.query

    # major_title_list = []
    major_codes = []
    all_majors = []
    unique_search_majors = []

    # unique_major_titles1 = unique_major_titles

    # get name from form
    # tag = request.form["tag"]
    textbox_val = request.args['school']

    school_query = School.query.filter_by(name=textbox_val).all()
    if len(school_query) > 2:
        return 'Too many schools'

    if len(textbox_val) == 0:
        # query all major titles directly
        major_list = []

        all_majors = Major.query.all()

        for major in all_majors:
            major_list.append(major.title)

        major_list.sort()

        state_list = []
        all_states = State.query.all()
        
        for state in all_states:
            state_list.append(state.name)
        
        state_list.sort()

        data = {
            'type': 'all_majors',
            'major_list': major_list,
            'state_list': state_list
        }
        return jsonify(data)

    else:
        # split word by spaces 
        # ensure first letter of the first word is capital so there will be a match in the database
        formated_text = textbox_val

        if textbox_val[0].islower():
            formated_text = textbox_val.capitalize()

        name = "%{}%".format(formated_text)
        school_list = School.query.filter(School.name.like(name)).all()
    # don't loop through unless there is a match
    if len(school_list) <= 3 and len(school_list) > 0:
        # consider using every
        state_list = []
        for school in school_list:
            # have to loop through bc school_list is from DB query
            # don't have to loop through a schools majors
            # can simply append a list of each school's major titles 
            # unique_search_majors = unique_search_majors + school.majors
            # unique_search_majors.append(school.)
            state_list.append(school.states.name)
            for major in school.majors:
                all_majors.append(major.title)
        #     unique_search_majors.add(major.title)
            # major_title_list.append(major.title)           
            
            # if major.majors.id not in major_codes:
            #     # don't want duplicates
            #     major_list.append(major.majors.title)
            #     major_codes.append(major.majors.id)
    # have to loop to extract in JS


    # major_title_list.sort()
        unique_states = list(set(state_list))
        unique_search_majors = list(set(all_majors))
        # unique_search_majors = list(unique_search_majors)
        unique_search_majors.sort()
        unique_states.sort()

        data = {
            'type': 'select',
            'major_list': unique_search_majors,
            'state_list': unique_states
            }

        return jsonify(data)
    else:
        # No update at all
        return 'Invalid school name'
    



@app.route('/API/findSchools', methods=['GET'])
def find_schools_of_a_major():
    if 'user_id' not in session:
        # flash message
        return redirect('/')

    all_schools = []
    school_list = []
    school_ids = []
    unique_school_names = []

    textbox_val = request.args['major']

    if len(textbox_val) == 0:
        all_schools = School.query.all()

        for school in all_schools:
            school_list.append(school.name)

        school_list.sort()

        state_list = []
        all_states = State.query.all()
        
        for state in all_states:
            state_list.append(state.name)
        
        state_list.sort()

        data = {
            'type': 'all_schools',
            'school_list': school_list,
            'state_list': state_list
        }

        return jsonify(data)


    
    name = "%{}%".format(textbox_val)
    major_list = Major.query.filter(Major.title.like(name)).all()

    if len(major_list) > 2:
        return 'Too many majors'

    else:
        state_list = []
        for major in major_list:
            for school in major.schools:
                school_list.append(school.name)
                state_list.append(school.states.name)
                # if school.schools.id not in school_ids:
                #     # don't want duplicates
                #     school_list.append(school.schools.name)
                #     school_ids.append(school.schools.id)



        unique_school_names = list(set(school_list))
        unique_state_names = list(set(state_list))
        
        unique_school_names.sort()
        unique_state_names.sort()

        data = {
            'type': 'selected',
            'school_list': unique_school_names,
            'state_list': unique_state_names
            }

        test = 1

        return jsonify(data)

# @app.route('/API/processStateInput',methods=['GET'])
# def process_state_input():
#     # process school and major

#     if 'user_id' not in session:
#         # flash message
#         return redirect('/')

#     # state_input = State.query.

#     all_states = []
#     state_list = []
#     school_list = []
#     school_ids = []
#     unique_school_names = []

#     textbox_val = request.args['school']

#     if len(textbox_val) == 0:
#         # update all majors/schools
#         all_states = State.query.all()

#         for state in all_states:
#             state_list.append(state.name)

#         state_list.sort()

#         # state_list = []
#         # all_states = State.query.all()
        
#         for state in all_states:
#             state_list.append(state.name)
        
#         state_list.sort()

#         data = {
#             'type': 'all_schools',
#             'school_list': school_list,
#             'state_list': state_list
#         }

#         return jsonify(data)


    
#     name = "%{}%".format(textbox_val)
#     major_list = Major.query.filter(Major.title.like(name)).all()

#     if len(major_list) > 2:
#         return 'Too many majors'

#     else:
#         state_list = []
#         for major in major_list:
#             for school in major.schools:
#                 school_list.append(school.name)
#                 state_list.append(school.states.name)
#                 # if school.schools.id not in school_ids:
#                 #     # don't want duplicates
#                 #     school_list.append(school.schools.name)
#                 #     school_ids.append(school.schools.id)



#         unique_school_names = list(set(school_list))
#         unique_state_names = list(set(state_list))
        
#         unique_school_names.sort()
#         unique_state_names.sort()

#         data = {
#             'type': 'selected',
#             'school_list': unique_school_names,
#             'state_list': unique_state_names
#             }

#         test = 1

#         return jsonify(data)

#     return

def call_college_API(school_id,major_id,credential_id,state,household_income):
        data = {}

        payload = {"id": f"{school_id}", "_fields": "id,school.name,latest.cost,latest.school.ownership,latest.school.state", "api_key": f"{API_key}"}

        cost_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json', params=payload)

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
            data['tuition_type'] = 'Out-of-state'

       
        # Verify school is private (not public)
        if ownership != 1:
            private_net_cost = cost_data['results'][0][f'latest.cost.net_price.private.by_income_level.{household_income}']
            data['tuition'] = private_net_cost
            data['tuition_type'] = 'N/A'

        if state == school_state and ownership == 1:
            net_in_state_public_cost = cost_data['results'][0][f'latest.cost.net_price.public.by_income_level.{household_income}']
            data['tuition'] = net_in_state_public_cost
            data['tuition_type'] = 'In-state'

        # may have to revise given that there could be multiple requests per search


        major_params = {
            'id':f'{school_id}','latest.programs.cip_4_digit.credential.level':f"{credential_id}", 'latest.programs.cip_4_digit.code':major_id, 
            '_fields':'id,school.name,latest.programs.cip_4_digit.earnings.highest.1_yr.overall_median_earnings,latest.programs.cip_4_digit.earnings.highest.2_yr.overall_median_earnings,latest.programs.cip_4_digit.earnings.highest.3_yr.overall_median_earnings',
            "api_key": f"{API_key}"
            }

        earnings_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json', major_params)

        earnings_data = earnings_resp.json()

        # if results don't exist, exit function and flash message
        yr_1_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['1_yr']['overall_median_earnings']
        yr_2_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['2_yr']['overall_median_earnings']
        yr_3_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['3_yr']['overall_median_earnings']

        data['yr_1_earnings'] = yr_1_earnings
        data['yr_2_earnings'] = yr_2_earnings
        data['yr_3_earnings'] = yr_3_earnings


        return data


