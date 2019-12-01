from behave import *
from flask import url_for
from app import routes
from time import sleep

@given('I want to create a note')
def step_impl(context):
    with context.context:
        context.browser.visit(url_for('app.addnote'))
        sleep(0.5)
        assert(context.browser.url == url_for('app.addnote'))

@given('I create a note')
def step_impl(context):
    with context.context:
        context.browser.find_by_xpath("//input[@name='title']").fill('This is the title')
        context.browser.find_by_xpath("//input[@name='note']").fill('This is the note')
        context.browser.find_by_xpath("//input[@name='tags']").fill('tag, tag2, tag3')
        context.browser.find_by_id("submit").first.click()
        sleep(0.5)
        assert(context.browser.url == url_for('app.notes'))

@then('The note is created')
def step_impl(context):
    with context.context:
        assert(context.broser.is_text_present('This is the title') and context.broser.is_text_present('This is the note') and context.broser.is_text_present('tag, tag2, tag3'))

@given('I try to make an empty note')
def step_impl(context):
    with context.context:
        context.browser.find_by_xpath("//input[@name='title']").fill('')
        context.browser.find_by_xpath("//input[@name='note']").fill('')
        context.browser.find_by_id("submit").first.click()

@then('the note is not created')
def step_impl(context):
    with context.context:
        assert(context.browser.is_text_present('Title is required') or context.browser.is_text_present('Note contents is required'))
