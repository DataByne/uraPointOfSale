from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators

class LoginForm(FlaskForm):
    username = StringField('Email or Username:', validators=[validators.InputRequired(), validators.DataRequired()])
    password = PasswordField('Password:', validators=[validators.InputRequired(), validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email:', validators=[validators.InputRequired(), validators.DataRequired()])
    username = StringField('Username:', validators=[validators.InputRequired(), validators.DataRequired()])
    password = PasswordField('Password:', validators=[validators.InputRequired(), validators.DataRequired()])
    password_confirm = PasswordField('Confirm Password:', validators=[validators.InputRequired(), validators.DataRequired()])
    submit = SubmitField('Register')

