from behave import *
from flask import url_for
from time import sleep
from app import db
from app.models import User, Note, Tag, NoteTags
from flask_login import current_user
from selenium.webdriver.common.keys import Keys

@given('I edit that note')
def step_impl(context):
    with context.context:
        context.browser.visit(url_for('app.notes'))
        context.browser.find_by_id('editnote').first.click()
        context.browser.find_by_xpath("//input[@name='title']").fill(' and even more title')
        context.browser.find_by_id("submit").first.click()
        sleep(1)
        assert(context.browser.url == url_for('app.notes'))

@given('I delete that note')
def step_impl(context):
    with context.context:
        context.browser.visit(url_for('app.notes'))
        context.browser.find_by_id('deletenote').first.click()
        alert = context.browser.get_alert()
        alert.accept()
        sleep(1)
        assert(context.browser.url == url_for('app.notes'))

@given('I search for that note')
def step_impl(context):
    with context.context:
        context.browser.find_by_xpath("//input[@type='text']").fill('This is the title')
        context.browser.find_by_id("search").first.click()
