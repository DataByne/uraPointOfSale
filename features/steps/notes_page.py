from behave import *
from flask import url_for
from time import sleep
from app import db
from app.models import User, Note, Tag, NoteTags
from flask_login import current_user

@given('I edit that note')
def step_impl(context):
    assert(False)
