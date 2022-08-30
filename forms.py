from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired
from enum import Enum

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
    major1 = StringField('Major:', validators=[DataRequired()])
    # major1 = SelectField('Select Major: ',coerce=int)
    school1 = StringField('College:', validators=[DataRequired()])
    school_state = StringField('State:', validators=[DataRequired()])
    # household_income = SelectField('Household Income:', choices=incomes, validators=[DataRequired()])
    # household_income = StringField('Household Income', va)



class AddUserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    state = StringField('State of Residency:', validators=[DataRequired()])
    household_income = SelectField('Household Income:', choices=incomes, validators=[DataRequired()])

class EditUserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    state = StringField('State of Residency:', validators=[DataRequired()])
    household_income = SelectField('Household Income:', choices=incomes, validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
