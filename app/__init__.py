from flask import Flask, Markup
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from datetime import timedelta
from flask_mail import Mail, Message
from flask_caching import Cache
from werkzeug.exceptions import ServiceUnavailable
import bleach
import pytz
import os

cache = Cache()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app(testing=False):
    app = Flask(__name__)
    app.testing = testing
    app.config.from_object(Config)
    if app.config['MAIL_USERNAME'] is None or app.config['MAIL_PASSWORD'] is None:
        raise ServiceUnavailable('Mail service is not properly configured')
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'app.login'
    login_manager.refresh_view = 'app.login'
    login_manager.needs_refresh_message = "Session expired, please login again.";
    login_manager.needs_refresh_message_category = "info"
    mail.init_app(app)
    migrate.init_app(app, db)
    # Set the markup filter
    app.jinja_env.filters['markup'] = markup_text_filter
    # Set the user time zone filter
    app.jinja_env.filters['user_datetime'] = user_datetime_filter
    with app.app_context():
        from . import errors, models, routes
        app.register_blueprint(routes.app)
        app.register_blueprint(errors.app)
        return app

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

def markup_text_filter(text):
    """ Filters the contents of note content to mark as html safe to convert tags on webpages
    Returns:
        String markedup
    """
    # Markup the string
    return Markup(bleach.clean(
        text,
        tags=['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'p', 'small', 'span', 'strong', 'ul'],
        attributes={'a': ['href', 'title'], 'abbr': ['title'], 'acronym': ['title'], '*': ['style']},
        styles=['color', 'font-family', 'font-weight'],
        protocols=['http', 'https', 'mailto']
    ))

