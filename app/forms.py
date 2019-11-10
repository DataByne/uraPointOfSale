from flask_wtf import FlaskForm
from flask_login import login_user
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, ValidationError
from pytz import all_timezones, country_names, country_timezones
from app.models import User

class LoginForm(FlaskForm):
    """Form for logging into the site

    Flask form.
    
    Attributes:
        username:	    Username or email field
        password:       Disguised field for password
        rememberMe:     Store credentials
        submit:         Submit action
    """
    username = StringField('Email or Username:', validators=[InputRequired('Email address or username is required.'), DataRequired()])
    password = PasswordField('Password:', validators=[InputRequired('Password is required.'), DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    def validate_submit(self, submit):
        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            user = User.query.filter_by(email=self.username.data).first()
        if user is None or not user.check_password(self.password.data):
            raise ValidationError('Login authentication failed.')
        else:
            login_user(user, remember=self.rememberMe.data)

class RegisterForm(FlaskForm):
    """Form for registering on site

    Flask form.
    
    Attributes:
        email:	            User's email address
        username:	          Account name on site
        password:           Field for new password
        password_confirm:   Confirmation field of password
        time_zone:          Timezone string for user
        submit:             Submit action
    """
    email = StringField('Email:', validators=[InputRequired('Email address is required.'), DataRequired(), Email('Email address must be valid.')])
    username = StringField('Username:', validators=[InputRequired('Username is required.'), DataRequired()])
    password = PasswordField('Password:', validators=[InputRequired('Password is required.'), DataRequired()])
    password_confirm = PasswordField('Confirm Password:', validators=[InputRequired(), DataRequired(), EqualTo('password', 'Passwords must match.')])
    country = SelectField('Country:', validators=[InputRequired('Country is required.'), DataRequired()])
    time_zone = SelectField('Time Zone:', validators=[InputRequired('Time Zone is required'), DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_country(self, country):
        if not country.data in country_timezones:
            raise ValidationError('Invalid country.')

    def validate_timezone(self, time_zone):
        if not time_zone.data in all_timezones:
            raise ValidationError('Invalid time zone.')

class NoteForm(FlaskForm):
    """Form for creating a note
    
    Flask form
    
    Attributes:
        title:	Note's title field
        note:	The body text of a note
        submit: Submit action
    """
    title = StringField('Title:', validators=[InputRequired('Title is required'), DataRequired()])
    note = TextAreaField('Note:', validators=[InputRequired('Note contents is required'), DataRequired()])
    submit = SubmitField('Create Note')

class EditNoteForm(FlaskForm):
    """Form for editing a note
    
    Flask form
    
    Attributes:
        title:	Note's title field
        note:	The body text of a note
        submit: Submit action
    """
    title = StringField('Title:', validators=[InputRequired('Title is required'), DataRequired()])
    note = TextAreaField('Note:', validators=[InputRequired('Note contents is required'), DataRequired()])
    submit = SubmitField('Save')
    delete = SubmitField('Delete');

