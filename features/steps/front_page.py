from behave import *
from flask import url_for

@given('I am on the landing page')
def step_impl(context):
    #browser = Browser('flask', app=app )
    context.browser.visit('http://localhost:5000/')
    assert(context.browser.title == 'Home - Note Weaver')

@then('I see the company name')
def step_impl(context):
    assert(context.browser.is_text_present("Note Weaver"))

@then('I see a link to "{link}"')
def step_impl(context, link):
    assert(context.browser.find_link_by_href(link))
