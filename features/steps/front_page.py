from behave import *
from flask import url_for

@given('I am on the landing page')
def step_impl(context):
    #browser = Browser('flask', app=app )
    context.browser.visit('http://localhost:5000/')
    assert(context.browser.title == 'Home - Note Weaver')
