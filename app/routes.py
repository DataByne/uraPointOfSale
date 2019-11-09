from app import app, db
from flask import render_template, send_from_directory, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, NoteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Note

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=RegisterForm())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/notes')
@login_required
def notes():
    #for title, note in Note.query.filter_by(user_id = current_user.id):
    userNotes = Note.query.filter_by(user_id = current_user.id)
    return render_template('notes.html', title='Your Notes', notes = userNotes)

@app.route('/addnote', methods=['GET', 'POST'])
@login_required
def addnote():
    form = NoteForm()
    if form.validate_on_submit():
        newnote = Note(title = form.title.data, note=form.note.data, user_id=current_user.id)
        db.session.add(newnote)
        db.session.commit()
        return redirect(url_for('index'))#may need to be changed depending on things
    return render_template('addnote.html', title='Add A Note', form=form)
