from behave import *
from flask import url_for

@given('I am on the landing page')
def step_impl(context):
    with context.request:
        context.browser.visit(url_for('index'))
        assert(context.browser.url == url_for('index'))

@then('I see the company name')
def step_impl(context):
    assert(context.browser.is_text_present("Note Weaver"))

@then('I see a link to "{link}"')
def step_impl(context, link):
    assert(context.browser.find_link_by_href(link))
