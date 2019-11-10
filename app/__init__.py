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

def user_datetime_filter(value, time_zone, format='%Y-%m-%d %-I:%M:%S%p %Z'):
    """ Filters a date and time for the user's timezone
    
    Returns:
        Date and time for user's timezone or UTC
    """
    if current_user and not time_zone:
        time_zone = current_user.time_zone
    value = pytz.timezone('UTC').localize(value, is_dst=None);
    if not time_zone in pytz.all_timezones:
        return value.strftime(format);
    return value.astimezone(pytz.timezone(time_zone)).strftime(format)

app.jinja_env.filters['user_datetime'] = user_datetime_filter

