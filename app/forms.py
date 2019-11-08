from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Email or Username:', validators=[validators.InputRequired(), validators.DataRequired()])
    password = PasswordField('Password:', validators=[validators.InputRequired(), validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email:', validators=[validators.InputRequired(), validators.DataRequired(), validators.Email()])
    username = StringField('Username:', validators=[validators.InputRequired(), validators.DataRequired()])
    password = PasswordField('Password:', validators=[validators.InputRequired(), validators.DataRequired()])
    password_confirm = PasswordField('Confirm Password:', validators=[validators.InputRequired(), validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise validators.ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise validators.ValidationError('Please use a different email address.')
