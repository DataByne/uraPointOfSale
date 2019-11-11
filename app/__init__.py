from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
import pytz
    
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

def user_datetime_filter(value, time_zone, format='%Y-%m-%d %I:%M:%S%p %Z'):
    """ Filters a date and time for the user's timezone
    
    Returns:
        Date and time for user's timezone or UTC
    """
    # Check current user exists and there is no time zone supplied
    if current_user and not time_zone:
        # Set the user time zone
        time_zone = current_user.time_zone
    # Localize the timestamp to UTC
    value = pytz.timezone('UTC').localize(value, is_dst=None);
    # Check if the time zone exists
    if not time_zone in pytz.all_timezones:
        # Format the time to UTC
        return value.strftime(format);
    # Format the time to the user time zone
    return value.astimezone(pytz.timezone(time_zone)).strftime(format)

# Set the user time zone filter
app.jinja_env.filters['user_datetime'] = user_datetime_filter

