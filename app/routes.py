from app import app
from flask import render_template
from app.forms import LoginForm

@app.route( '/' )
@app.route( '/index' )
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)
