"""Test app view functions"""
#
#    FLASK_ENV=production python -m unittest test_message_views.py

from cgitb import html
import os
from unicodedata import name
from unittest import TestCase
from sqlalchemy import exc, orm
from flask import session

from models import SchoolMajor, db, connect_db, HouseholdIncome, ProgramFinance, TuitionType, User, School, Major, State

os.environ['DATABASE_URL'] = "postgresql:///college_app-test"


from app import app, CURR_USER_KEY, bcrypt


db.create_all()

# Not testing CSRF
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class CollegeAppViewsTestCase(TestCase):
    """Test views for all tests."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.new_income = HouseholdIncome(household_income="0-30000")
        self.new_income_id = 1
        self.new_income.id = self.new_income_id

        self.new_income2 = HouseholdIncome(household_income="30001-48000")
        self.new_income2_id = 2
        self.new_income2.id = self.new_income2_id

        db.session.add(self.new_income)
        db.session.add(self.new_income2)
        db.session.commit()

        self.new_state1 = State(name='KY')
        self.new_state1_id = 18
        self.new_state1.id = self.new_state1_id

        self.new_state2 = State(name='MA')
        self.new_state2_id = 19
        self.new_state2.id = self.new_state2_id

        db.session.add(self.new_state1)
        db.session.add(self.new_state2)

        db.session.commit()

        pw_hash = bcrypt.generate_password_hash('spants').decode('utf-8')

        self.new_user = User(username='spongebob',password=pw_hash,home_state_id=18,household_income_id=1)
        
        pw_hash2 = bcrypt.generate_password_hash('test').decode('utf-8')
        self.new_user2 = User(username='testuser',password=pw_hash2,home_state_id=19,household_income_id=1)

        db.session.add(self.new_user)
        db.session.add(self.new_user2)
        db.session.commit()

        self.new_user_id = self.new_user.id 
        self.new_user2_id = self.new_user2.id

        self.new_school = School(id='157085',name='University of Kentucky', state_id=18)
        self.new_school_id = self.new_school.id

        db.session.add(self.new_school)
        db.session.commit()

        self.new_major = Major(id='5203',title='Accounting and Related Services.')

        db.session.add(self.new_major)
        db.session.commit()

        self.new_major_id = self.new_major.id

        self.new_school_major = SchoolMajor(school_id='157085',major_id='5203')
        db.session.add(self.new_school_major)
        db.session.commit()

        
        # # add tuition types
        # tuition_type1 = TuitionType(id=1,tuition_type='In-state')
        # db.session.add(tuition_type1)
        # db.session.commit()

        # tuition_type2 = TuitionType(id=2,tuition_type='Out-of-state')
        # db.session.add(tuition_type2)
        # db.session.commit()

        # tuition_type3 = TuitionType(id=3,tuition_type='Private')
        # db.session.add(tuition_type3)
        # db.session.commit()



        # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        # username = db.Column(db.String(), unique=True, nullable=False)
        # password = db.Column(db.String(), unique=True, nullable=False)
        # home_state_id = db.Column(db.Integer,db.ForeignKey("states.id"))
        # household_income_id = db.Column(db.Integer, db.ForeignKey("household_incomes.id"))

        # make instances of models
        # User, HouseholdIncome, ProgramFinance, TuitionType, User, School, Major, State

    
    def tearDown(self):
        # tearDown user after each function
        User.query.delete()

        db.session.commit()
        

    def test_user_signup(self):
        """Ensure user can signup"""
        with self.client as c:
            # with c.session_transaction() as sess:
            #     # sess[CURR_USER_KEY] = self.testuser_id
            #     test=1
            # username, password, home_state_id, household_income_id
            resp = c.post('/signup', 
                data={
                'username':'superman',
                'password':'test',
                'state':'KY', 
                'household_income':"0-30000"}
                ,follow_redirects=True)
            html = resp.get_data(as_text=True)

            test_user = User.query.filter_by(username='superman').first()

            # verify page after user creation exists 
            self.assertIn('<p>Add a new search above to compare outcomes between schools.</p>',html)
            
            # verify new user was added through the route
            self.assertEqual(test_user.username,'superman')
            self.assertEqual(test_user.home_state_id,18)
            self.assertEqual(resp.status_code, 200)
        
    def test_user_logout(self):
        """Ensure user can logout"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.new_user_id
            
            resp = c.get('/logout',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertNotIn('user_id',session)
            self.assertNotIn('No user logged in!',html)
            self.assertIn('<p class="welcome">Welcome to the College Saving App!',html)

    def test_user_login(self):
        """Ensure user can login"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.new_user_id

            resp = c.post('/login', 
                data={
                'username':'spongebob',
                'password':'spants'}
                ,follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('user_id',session)
            # For new user, message below appears
            self.assertIn('<p>Add a new search above to compare outcomes between schools.</p>',html)
            self.assertEqual(resp.status_code,200)

    def test_edit_user_profile(self):
        """Ensure user can edit profile"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.new_user_id

            resp = c.post('/userProfile', 
                data={
                'username':'spongebob',
                'state': 'MA',
                'household_income': "30001-48000",
                'password':'spants',
                },
                follow_redirects=True)

            html = resp.get_data(as_text=True)

            edited_user = User.query.get(self.new_income_id)

            self.assertEqual(edited_user.home_state_id,19)
            self.assertEqual(edited_user.household_income_id,2)
            self.assertIn('<li class="message">User profile updated!</li>',html)
            self.assertEqual(resp.status_code,200)

            # add some html check
    
    def test_in_state_search_result(self):
        """Test user search parameters"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.new_user_id

            resp = c.post('/search', 
                data={
                'major1':'Accounting and Related Services.',
                'school1': 'University of Kentucky',
                'school_state': "KY"
                },
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            # income
            self.assertIn('id="income-year2" type="text" value="$50,000"></td>',html)
            # In/out of state
            self.assertIn('type="text" value="In-state"></td>',html)  
            # tuition
            self.assertIn('id="cost" type="text" value="$12,593"></td>',html)

    def test_out_of_state_search_result(self):
        """Test user search parameters"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.new_user2_id

            resp = c.post('/search', 
                data={
                'major1':'Accounting and Related Services.',
                'school1': 'University of Kentucky',
                'school_state': "KY"
                },
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            # income
            self.assertIn('id="income-year3" type="text" value="$57,566"></td>',html)
            # In/out of state
            self.assertIn('id="tuition-type" type="text" value="Out-of-state"></td>',html)  
            # tuition
            self.assertIn('id="cost" type="text" value="$50,356"></td>',html)





 