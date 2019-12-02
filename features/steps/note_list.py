from behave import *
from flask import url_for
from app import routes
from app import db
from app.models import User, Note, Tag, NoteTags

@given('I visit my notes')
def step_impl(context):
    with context.context:
        context.browser.visit(url_for('app.notes'))

@then('I am redirected to login')
def step_impl(context):
    with context.context:
        assert(context.browser.url != url_for('app.addnote'))

@given('I have more than zero notes')
def step_impl(context):
    with context.context:
        assert(len(Note.query.filter_by(user_id = 0).all()) > 0)

@given('I have zero notes')
def step_impl(context):
    with context.context:
        assert(len(Note.query.filter_by(user_id = 0).all()) == 0)
