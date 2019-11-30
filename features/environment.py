import os
import tempfile
from behave import fixture, use_fixture
from splinter import Browser

from app import app

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
	  context.browser = Browser( driver_name='flask', app=app )
	  yield context.browser
	  context.browser.quit()

@fixture
def flask_client(context, *args, **kwargs):
	  """Sets up temporary flask context

	  Generator function.

	  Yields:
		  A flask testing client attribute to Behave's context.
	  """
	  # temporary db file code here
	  app.testing = True
	  context.client = app.test_client()
	  context.request = app.test_request_context()
	  # with app.app_context():
		  # initialize db code here
	  yield context.client

	  # close temp db code
	  # remove temp db code

def before_all( context ):
	  """Runs before each test

	  Args:
  		  context:	Behave testing context
	  """
	  use_fixture(splinter_browser, context)
	  use_fixture(flask_client, context)

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
