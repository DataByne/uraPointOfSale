from behave import *
from flask import url_for
from time import sleep

@given('I am on the landing page')
def step_impl(context):
    with context.context:
        context.browser.visit(url_for('app.index'))
        assert(context.browser.url == url_for('app.index'))

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
    with context.context:
        context.browser.find_link_by_href('/about').first.click()
        sleep(0.5)
        assert(context.browser.url == url_for('app.about'))

@given('I am registered')
def step_impl(context):
    with context.context:
        context.browser.visit(url_for('app.register'))
        context.browser.find_by_xpath("//input[@name='email']").fill('exampleuser@exampleuser.com')
        context.browser.find_by_xpath("//input[@name='username']").fill('exampleusername')
        context.browser.find_by_xpath("//input[@name='password']").fill('ExamplePa33word!')
        context.browser.find_by_xpath("//input[@name='password_confirm']").fill('ExamplePa33word!')
        context.browser.find_by_xpath("//input[@name='submit']").first.click()
        sleep(0.5)
        assert(context.browser.url == url_for('app.login'))

@then('I see the text "{text}"')
def step_impl(context, text):
    with context.context:
        assert(context.browser.is_text_present(text))
