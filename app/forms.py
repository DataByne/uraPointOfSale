from flask_wtf import FlaskForm
from flask_login import login_user, current_user
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, ValidationError
from pytz import all_timezones, country_names, country_timezones
from app.models import User

class LoginForm(FlaskForm):
    """Form for logging into the site

    Flask form

    Fields:
        username:	  Username or email field
        password:   Disguised field for password
        rememberMe: Store credentials
        submit:     Submit action
    """
    username = StringField('Email or Username:', validators=[InputRequired('Email address or username is required.'), DataRequired()])
    password = PasswordField('Password:', validators=[InputRequired('Password is required.'), DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_submit(self, submit):
        """Validate the login form on submit

        Parameters:
            self:   The login form
            submit: The submit button

        Raises:
            ValidationError: The user could not be authenticated
        """
        # Query the user by user name
        user = User.query.filter_by(username=self.username.data).first()
        # Check if the user was found
        if user is None:
            # Query the user by email address
            user = User.query.filter_by(email=self.username.data).first()
        # Check user exists and the password hash matches
        if user is None or not user.check_password(self.password.data):
            # Raise validation error that user could not be authenicated
            raise ValidationError('Login authentication failed.')
        else:
            # Login user
            login_user(user, remember=self.rememberMe.data)

class RegisterForm(FlaskForm):
    """Form for registering on site

    Flask form

    Fields:
        email:	          User's email address
        username:	        Account name on site
        password:         Field for new password
        password_confirm: Confirmation field of password
        country:          Country code for user
        time_zone:        Timezone string for user
        submit:           Submit action
    """
    email = StringField('Email:', validators=[InputRequired('Email address is required.'), DataRequired(), Email('Email address must be valid.')])
    username = StringField('Username:', validators=[InputRequired('Username is required.'), DataRequired()])
    password = PasswordField('Password:', validators=[InputRequired('Password is required.'), DataRequired()])
    password_confirm = PasswordField('Confirm Password:', validators=[InputRequired('Passwords must match.'), DataRequired(), EqualTo('password', 'Passwords must match.')])
    country = SelectField('Country:', validators=[InputRequired('Country is required.'), DataRequired()])
    time_zone = SelectField('Time Zone:', validators=[InputRequired('Time Zone is required'), DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Validate form username field

        Parameters:
            self:     The RegisterForm form to validate
            username: The username to validate does not exist

        Raises:
            ValidationError: A validation error if the username is already in use

        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Validate form email address field

        Parameters:
            self:     The RegisterForm form to validate
            username: The email address to validate does not exist

        Raises:
            ValidationError: A validation error if the email address is already in use

        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_country(self, country):
        """Validate form country field

        Parameters:
            self:    The RegisterForm form to validate
            country: The country code to validate exists

        Raises:
            ValidationError: A validation error if the country code does not exist
        """
        if not country.data in country_timezones:
            raise ValidationError('Invalid country.')

    def validate_timezone(self, time_zone):
        """Validate form time zone field

        Parameters:
            self:      The RegisterForm form to validate
            time_zone: The time zone to validate exists

        Raises:
            ValidationError: A validation error if the time zone does not exist
        """
        if not time_zone.data in all_timezones:
            raise ValidationError('Invalid time zone.')

class EditUserForm(FlaskForm):
    """Form for editing user information

    Flask form

    Fields:

    """
    email = StringField('Email:', validators=[InputRequired('Email address is required.'), DataRequired(), Email('Email address must be valid.')])
    username = StringField('Username:', validators=[InputRequired('Username is required.'), DataRequired()])
    password = PasswordField('Password:')
    password_confirm = PasswordField('Confirm Password:', validators=[EqualTo('password', 'Passwords must match.')])
    country = SelectField('Country:', validators=[InputRequired('Country is required.'), DataRequired()])
    time_zone = SelectField('Time Zone:', validators=[InputRequired('Time Zone is required'), DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Validate form username field

            Parameters:
                self:     The RegisterForm form to validate
                username: The username to validate does not exist

            Raises:
                ValidationError: A validation error if the username is already in use

            """
        user = User.query.filter_by(username=username.data).first()
        if user is not None and current_user.id != user.id:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Validate form email address field

            Parameters:
                self:     The RegisterForm form to validate
                username: The email address to validate does not exist

            Raises:
                ValidationError: A validation error if the email address is already in use

            """
        user = User.query.filter_by(email=email.data).first()
        if user is not None and current_user.email != user.email:
            raise ValidationError('Please use a different email address.')

    def validate_country(self, country):
        """Validate form country field

            Parameters:
                self:    The RegisterForm form to validate
                country: The country code to validate exists

            Raises:
                ValidationError: A validation error if the country code does not exist
            """
        if not country.data in country_timezones:
            raise ValidationError('Invalid country.')

    def validate_timezone(self, time_zone):
        """Validate form time zone field

            Parameters:
                self:      The RegisterForm form to validate
                time_zone: The time zone to validate exists

            Raises:
                ValidationError: A validation error if the time zone does not exist
            """
        if not time_zone.data in all_timezones:
            raise ValidationError('Invalid time zone.')

class NoteForm(FlaskForm):
    """Form for creating a note

    Flask form

    Fields:
        title:	The title of a note
        note:	  The body text of a note
        submit: Submit action
    """
    title = StringField('Title:', validators=[InputRequired('Title is required'), DataRequired()])
    note = TextAreaField('Note:', validators=[InputRequired('Note contents is required'), DataRequired()])
    submit = SubmitField('Create Note')

class EditNoteForm(FlaskForm):
    """Form for editing a note

    Flask form

    Fields:
        title:	The title of a note
        note:	  The body text of a note
        submit: Submit action
        delete: Delete action
    """
    title = StringField('Title:', validators=[InputRequired('Title is required'), DataRequired()])
    note = TextAreaField('Note:', validators=[InputRequired('Note contents is required'), DataRequired()])
    submit = SubmitField('Save')
    delete = SubmitField('Delete');
