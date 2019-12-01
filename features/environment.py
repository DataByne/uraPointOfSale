import os
import tempfile
from behave import fixture, use_fixture
from splinter import Browser
from flask_sqlalchemy import SQLAlchemy

import app

@fixture
def splinter_browser( context, type='chrome' ):
	  """Sets up a splinter browser session

	  Generator function that provides a web driver browser object for use in
	  testing. The browser defaults to a Chrome web driver.

	  Args:
		    context:	Behave testing context
		    type:		Specific webdriver to run

	  Yields:
		    A browser object attribute to the Behave testing module's context. The
		    type of the browser is set to whichever the generator is provided.
	  """
	  context.browser = Browser('firefox')
	  yield context.browser
	  context.browser.quit()

@fixture
def flask_client(context, *args, **kwargs):
	'''app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
	app.app.testing = True
	context.client = app.app.test_client()
	context.request = app.app.test_request_context()
	with app.app.app.app_context():
		ontext.db = SQLAlchemy()
		context.db.init_app.app(app.app)
		context.db.create_all()
		yield context.client
		context.db.session.remove()
		context.db.drop_all()'''
	app.app.testing = True
	#context = app.app.app_context()
	context.client = app.app.test_client()
	context.request = app.app.test_request_context()
	yield context.client
	#yield context.client

	  # close temp db code
	  # remove temp db code

def before_all( context ):
	  """Runs before each test

	  Args:
  		  context:	Behave testing context
	  """
	  use_fixture(splinter_browser, context)
	  use_fixture(flask_client, context)
	  #models.init(environment='test')

def before_tag( context, tag ):
	  """Prepares fixtures based on tags

	  Description

	  Args:
		    context:	Behave testing context
		    tag:		Tag passed via @fixture.[tag]
	  """
	  if tag == "fixture.browser":
		  use_fixture(splinter_browser, context)
	  if tag == "fixture.client":
	      use_fixture(flask_client, context)
