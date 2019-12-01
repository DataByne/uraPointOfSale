from behave import *
from flask import url_for
from app import routes

@given('I visit my notes')
def step_impl(context):
    with context.request:
        context.browser.visit(url_for('notes'))

@then('I am redirected to login')
def step_impl(context):
    with context.request:
        assert(context.browser.url == url_for('login'))

@given('I have more than zero notes')
def step_impl(context):
    assert(False)

@given('I have zero notes')
def step_impl(context):
    assert(False)
