from app import app, db
from datetime import datetime
from flask import render_template, send_from_directory, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegisterForm, NoteForm, EditNoteForm
from flask_login import current_user, logout_user, login_required
from app.models import User, Note
from pytz import all_timezones, country_names, country_timezones

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<CountryID>', methods=['GET', 'POST'])
def register(CountryID=None):
    """Route for registration action

    Returns:
        Rendering of registration page or redirect to home.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    form.country.choices = [(country_id, country_names[country_id]) for country_id in country_names]
    if CountryID in country_timezones:
      form.country.data = CountryID
    else:
      form.country.data = 'US'
    form.time_zone.choices = [(tz, tz) for tz in country_timezones[form.country.data]]
    form.time_zone.data = country_timezones[form.country.data][0]
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, country=form.country.data, time_zone=form.time_zone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form, country_names=country_names)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for login action

    Returns:
        Rendering of login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    """Exits out of the user context

    Returns:
        Redirects to home page.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/notes')
@login_required
def notes():
    """Route to note directory

    Returns:
        Rendering of notes page.
    """
    userNotes = Note.query.filter_by(user_id=current_user.id)
    return render_template('notes.html', title='Your Notes', notes=userNotes)


@app.route('/notes/add', methods=['GET', 'POST'])
@login_required
def addnote():
    form = NoteForm()
    if form.validate_on_submit():
        newnote = Note(title = form.title.data, note=form.note.data, user_id=current_user.id)
        db.session.add(newnote)
        db.session.commit()
        return redirect(url_for('notes'))
    return render_template('addnote.html', title='Add A Note', form=form)

@app.route('/notes/edit/<NoteID>', methods=['GET', 'POST'])
@login_required
def editnote(NoteID):
    note = Note.query.filter_by(id=int(NoteID)).first()
    if note is None or note.user_id != current_user.id:
       return redirect(url_for('notes'))
    form = EditNoteForm();
    if form.validate_on_submit():
        if form.delete.data:
          return redirect(url_for('deletenote', NoteID=NoteID))
        note.title = form.title.data
        note.note = form.note.data
        note.last_edited = datetime.utcnow()
        db.session.commit();
        return redirect(url_for('singlenote', NoteID=NoteID))
    form.title.data = note.title
    form.note.data = note.note
    return render_template('editnote.html', title='Edit', form=form);

@app.route('/notes/delete/<NoteID>')
@login_required
def deletenote(NoteID):
    note = Note.query.filter_by(id=int(NoteID)).first()
    if note is not None and note.user_id == current_user.id:
        title = note.title;
        db.session.delete(note)
        db.session.commit()
        flash("Deleted note '" + title + "'.")
    return redirect(url_for('notes'))

@app.route('/notes/<NoteID>')
@login_required
def singlenote(NoteID):
    note = Note.query.filter_by(id=int(NoteID)).first()
    if note is None or note.user_id != current_user.id:
        return redirect(url_for('notes'))
    return render_template('singlenote.html', title=note.title, note=note)

@app.route('/api/timezones')
@app.route('/api/timezones/<CountryID>')
def gettimezones(CountryID=None):
    if CountryID in country_timezones:
        timezones = country_timezones[CountryID]
    else:
        timezones = all_timezones
    return jsonify([(tz, tz) for tz in timezones])

