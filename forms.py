from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators
from wtforms.validators import DataRequired, AnyOf, InputRequired, Length
from enum import Enum

# from seed import states
from all_majors_seed import states, majors, unique_school_list, unique_major_titles

# class Income(Enum):

                        #         "75000-plus": 22909,
    #  "0-48000": 12900,
    #  "30001-75000": 15139,
#     '0-10' = 1
                        #    "0-30000": 12593,
                        #    "30001-48000": 13424,
                        #    "48001-75000": 16708,
                        #    "75001-110000": 20959
                        #    "110001-plus": 23946,

incomes = [("0-30000","0-$30k"),("30001-48000","$30k-$48k"),("48001-75000","$48k-$75k"),("75001-110000","$75k-$110k"),("110001-plus","$110k+")]


class SearchForm(FlaskForm):
    major1 = StringField('Major:', validators=[InputRequired(),AnyOf(unique_major_titles,message='Invalid Major. Must select input from dropdown list.')])
    # major1 = SelectField('Select Major: ',coerce=int)
    school1 = StringField('College:', validators=[InputRequired(),AnyOf(unique_school_list, message='Invalid school name. Must select input from dropdown list')])
    school_state = StringField('State:', validators=[InputRequired(),AnyOf(states,message='Invalid state format. Select state from dropdown list')])
    # household_income = SelectField('Household Income:', choices=incomes, validators=[DataRequired()])
    # household_income = StringField('Household Income', va)


class AddUserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=4,max=25)])
    password = PasswordField('password', validators=[DataRequired(),Length(min=4,max=25)])
    state = StringField('State of Residency:', validators=[DataRequired(),AnyOf(states,message='Invalid state format. Select state from dropdown list')])
    household_income = SelectField('Household Income:', choices=incomes, validators=[DataRequired()])

class EditUserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=4,max=25)])
    state = StringField('State of Residency:', validators=[DataRequired(),AnyOf(states,message='Invalid state format. Select state from dropdown list')])
    household_income = SelectField('Household Income:', choices=incomes, validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=4,max=25)])
    password = PasswordField('password', validators=[DataRequired(),Length(min=4,max=25)])
