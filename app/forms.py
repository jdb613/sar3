from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Srep


class LoginForm(FlaskForm):
    repcode = StringField('RepCode', validators=[DataRequired()])
    teamcode = StringField('TeamCode', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    repcode= StringField('RepCode', validators=[DataRequired()])
    teamcode = StringField('TeamCode', validators=[DataRequired()])
    submit = SubmitField('Register')

class BokehForm(FlaskForm):
    submit = SubmitField('Bokeh Test')
