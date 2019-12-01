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
    with context.request:
        context.browser.find_link_by_href('/about').first.click()
        assert(context.browser.url == url_for('about'))

@given('I am logged in')
def step_impl(context):
    with context.request:
        context.browser.find_link_by_href('/register').click()
        context.browser.find_by_xpath("//input[@name='email']").fill('exampleuser@exampleuser.com')
        context.browser.find_by_xpath("//input[@name='username']").fill('exampleusername')
        context.browser.find_by_xpath("//input[@name='password']").fill('ExamplePa33word!')
        context.browser.find_by_xpath("//input[@name='password_confirm']").fill('ExamplePa33word!')
        context.browser.find_by_xpath("//input[@value='Register']").first.click()
        assert(context.browser.url == url_for('login'))
        context.browser.fill('username', 'exampleusername')
        context.browser.fill('password', 'ExamplePa33word!')
        context.browser.find_by_id('submit').first.click()

@then('I see the text "{text}"')
def step_impl(context, text):
    with context.request:
        assert(context.browser.find_by_text(text))
