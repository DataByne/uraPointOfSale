from behave import *
from flask import url_for
import environment
from splinter import Browser
from app import app

@given('I am on the landing page')
def step_impl(context):
    #browser = Browser('flask', app=app )
    context.browser.get(url_for('index'))
    assert(context.browser.url() == 'http://localhost:5000/')
