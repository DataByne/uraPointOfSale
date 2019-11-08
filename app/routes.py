from app import app
from flask import render_template, send_from_directory
from app.forms import LoginForm, RegisterForm

@app.route( '/' )
@app.route( '/index' )
def index():
    return render_template('index.html', title='Home')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title="Register", form=RegisterForm())

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title="Login", form=LoginForm())

