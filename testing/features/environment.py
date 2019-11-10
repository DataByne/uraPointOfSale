import os
import tempfile
from behave import fixture, use_fixture
from splinter import Browser

from app import app

@fixture
def splinter_browser( context, type='chrome' ):
	"""Sets up a splinter browser session

	Defaults to a Chrome webdriver
	
	Args:
		context:	Behave testing context
		type:		Specific webdriver to run
	"""
	context.browser = Browser( driver_name=type )
	yield context.browser
	context.browser.quit()


@fixture
def flask_client( context, *args, **kwargs ):
	"""Sets up temporary flask context
	"""
	# temporary db file code here
	app.testing = True
	context.client = app.test_client()
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
	# use_fixture( splinter_browser, context )


def before_tag( context, tag ):
	"""Prepares fixtures based on tags
	
	Description
	
	Args:
		context:	Behave testing context
		tag:		Tag passed via @fixture.[tag]
	"""
	if tag == "fixture.browser":
		use_fixture( splinter_browser, context )