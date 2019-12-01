from behave import *
from flask import url_for
from app import routes

@given('I visit my notes')
def step_impl(context):
    with context.context:
        context.browser.visit(url_for('app.notes'))

@then('I am redirected to login')
def step_impl(context):
    with context.context:
        assert(context.browser.url == url_for('app.login'))

@given('I have more than zero notes')
def step_impl(context):
    assert(False)

@given('I have zero notes')
def step_impl(context):
    assert(False)
