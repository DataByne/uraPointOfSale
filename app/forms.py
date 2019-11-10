from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, validators
from app.models import User

class LoginForm( FlaskForm ):
    """Form for logging into the site

    Flask form.
    
    Attributes:
        username:	    Username or email field
        password:       Disguised field for password
        rememberMe:     Store credentials
        submit:         Submit action
    """
    username = StringField('Email or Username:', validators=[validators.InputRequired(), validators.DataRequired()])
    password = PasswordField('Password:', validators=[validators.InputRequired(), validators.DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm( FlaskForm ):
    """Form for registering on site

    Flask form.
    
    Attributes:
        email:	            User's email address
        username:	        Account name on site
        password:           Field for new password
        password_confirm:   Confirmation field of password
        submit:             Submit action
    """
    email = StringField('Email:', validators=[validators.InputRequired(), validators.DataRequired(), validators.Email()])
    username = StringField('Username:', validators=[validators.InputRequired(), validators.DataRequired()])
    password = PasswordField('Password:', validators=[validators.InputRequired(), validators.DataRequired()])
    password_confirm = PasswordField('Confirm Password:', validators=[validators.InputRequired(), validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username( self, username ):
        user = User.query.filter_by( username=username.data ).first()
        if user is not None:
            raise validators.ValidationError('Please use a different username.')

    def validate_email( self, email ):
        user = User.query.filter_by( email=email.data ).first()
        if user is not None:
            raise validators.ValidationError( 'Please use a different email address.' )

class NoteForm( FlaskForm ):
    """Form for creating a note
    
    Flask form
    
    Attributes:
        title:	Note's title field
        note:	The body text of a note
        submit: Submit action
    """
    title = StringField('Title:', validators=[validators.InputRequired(), validators.DataRequired()])
    note = TextAreaField('Note:', validators=[validators.InputRequired(), validators.DataRequired()])
    submit = SubmitField('Create Note')
