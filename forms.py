from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    major1 = StringField('Major:', validators=[DataRequired()])
    school1 = StringField('College:', validators=[DataRequired()])
    state = StringField('State of Residency', validators=[DataRequired()])
    # household_income = StringField('Household Income', va)



class AddUserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
