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

@then('I see the navigation bar')
def step_impl(context):
    assert(context.browser.find_by_css('.navbar'))

@then('I can navigate to other pages')
def step_impl(context):
    context.browser.find_link_by_href('/about').first.click()
    #yes I know it should be "== url_for('about')" but I was getting strange errors so this needs to be fixed but works for now
    assert(context.browser.title == "About Us - Note Weaver")

@given('I am logged in')
def step_impl(context):
    context.browser.find_link_by_href(url_for('register')).click()
    context.browser.fill('email', 'exampleuser@exampleuser.com')
    context.browser.fill('username', 'exampleusername')
    context.browser.fill('password', 'ExamplePa33word!')
    context.browser.fill('password_confirm', 'ExamplePa33word!')
    context.broser.find_by_id('submit').first.click()
