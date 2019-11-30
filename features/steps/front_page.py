from behave import *
from flask import url_for

@given('I am on the landing page')
def step_impl(context):
    with context.request:
        context.browser.visit(url_for('index'))
        assert(context.browser.url == url_for('index'))
