from app import app, db
from datetime import datetime
from flask import render_template, send_from_directory, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegisterForm, NoteForm, EditNoteForm, EditUserForm
from flask_login import current_user, logout_user, login_required
from app.models import User, Note
from pytz import all_timezones, country_names, country_timezones

@app.route('/')
@app.route('/index')
def index():
    """Route for landing page

    Returns:
        Rendering of the landing page
    """
    return render_template('index.html', title='Home')


@app.route('/css/<path:path>')
def send_css(path):
    """Route for static CSS files

    Parameters:
        path: The path of the static CSS file

    Returns:
        Static content from the 'css' directory
    """
    return send_from_directory('css', path)


@app.route('/images/<path:path>')
def send_images(path):
    """Route for static image files

    Parameters:
        path: The path of the static image file

    Returns:
        Static content from the 'images' directory
    """
    return send_from_directory('images', path)


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<CountryID>', methods=['GET', 'POST'])
def register(CountryID=None):
    """Route for registration

    Parameters:
        CountryID: The country code to assume is default

    Returns:
        Rendering of registration page, redirect to login for successful login, or redirect to landing page if a user is already logged in
    """
    # Check if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Create registration form
    form = RegisterForm()
    # Add country codes to the country code select field
    form.country.choices = [(country_id, country_names[country_id]) for country_id in country_names]
    # Set the default country code to the supplied CountryID or default to 'US'
    if CountryID in country_timezones:
      form.country.data = CountryID
    else:
      form.country.data = 'US'
    # Add the time zones for the selected country code to the time zone select field
    form.time_zone.choices = [(tz, tz) for tz in country_timezones[form.country.data]]
    # Set the default time zone to the first
    form.time_zone.data = country_timezones[form.country.data][0]
    # Validate the form
    if form.validate_on_submit():
        # Create a new user model from the form data
        user = User(username=form.username.data, email=form.email.data, country=form.country.data, time_zone=form.time_zone.data)
        # Set the user model password hash
        user.set_password(form.password.data)
        # Add the model to the database
        db.session.add(user)
        db.session.commit()
        # Flash a successfully register message
        flash("Succesfully registered new user '" + user.username + "'.");
        # Redirect to the login page
        return redirect(url_for('login'))
    # Render the registration page from the template and form
    return render_template('register.html', title="Register", form=form, country_names=country_names)


@app.route("/user/<UserID>", methods=['GET', 'POST'])
@login_required
def user(UserID):
    user = User.query.filter_by(id = int(UserID)).first()
    if user is None or user.id != current_user.id:
        return redirect(url_for('index'))

    return render_template('user.html', title=user.username)


@app.route('/user/edit/<UserID>', methods=['GET', 'POST'])
@login_required
def edituser(UserID):
    user = User.query.filter_by(id=int(UserID)).first()
    if user is None or user.id != current_user.id:
        return redirect(url_for('user', UserID=current_user.id))
    form = EditUserForm()
    # Add country codes to the country code select field
    CountryID = form.country.data
    if CountryID is None or CountryID == "" or CountryID.upper() == "NONE":
        CountryID = user.country
        if CountryID is None:
            CountryID = 'US'
    form.country.choices = [(country_id, country_names[country_id]) for country_id in country_names]
    form.time_zone.choices = [(tz, tz) for tz in country_timezones[CountryID]]
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.country = form.country.data
        user.time_zone = form.time_zone.data
        if form.password.data != "":
            user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('user', UserID=UserID))
    form.username.data = user.username
    form.email.data = user.email
    form.country.data = user.country
    form.time_zone.data = user.time_zone
    return render_template('edituser.html', title='Edit ' + current_user.username, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for login

    Returns:
        Rendering of login page or redirect to landing page
    """
    # Check if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Create login form
    form = LoginForm()
    # Validate the form
    if form.validate_on_submit():
        # Redirect to landing page on successful authenticatation
        return redirect(url_for('index'))
    # Render the login page from the template and form
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    """Route for logout

    Returns:
        Redirects to landing page
    """
    # Logout user
    logout_user()
    # Redirect to landing page
    return redirect(url_for('index'))


@app.route('/notes')
@login_required
def notes():
    """Route to notes list

    Returns:
        Rendering of notes list page
    """
    # Query notes of current user
    userNotes = Note.query.filter_by(user_id=current_user.id)
    # Render notes list page from the template and user notes
    return render_template('notes.html', title='Your Notes', notes=userNotes)


@app.route('/notes/add', methods=['GET', 'POST'])
@login_required
def addnote():
    """Route to add a note

    Returns:
        Rendering of add note page or redirect to notes list page when note is added
    """
    # Create a note form
    form = NoteForm()
    # Validate the form
    if form.validate_on_submit():
        # Create a new note from the form data
        newnote = Note(title = form.title.data, note=form.note.data, user_id=current_user.id)
        # Add the note to the database
        db.session.add(newnote)
        db.session.commit()
        # Redirect to notes list page
        return redirect(url_for('notes'))
    # Render the add note page from the template and form
    return render_template('addnote.html', title='Add A Note', form=form)

@app.route('/notes/edit/<NoteID>', methods=['GET', 'POST'])
@login_required
def editnote(NoteID):
    """Route to edit a note

    Parameters:
        NoteID: The unique identifier of the note to edit

    Returns:
        Rendering of the edit note page, redirect to delete the note, redirect to note detail page, or redirect to the notes list page if note can not be found
    """
    # Query note by identifier
    note = Note.query.filter_by(id=int(NoteID)).first()
    # Check note exists and is authored by current user
    if note is None or note.user_id != current_user.id:
        # Redirect to notes list page
       return redirect(url_for('notes'))
    # Create the edit note form
    form = EditNoteForm();
    # Validate the form
    if form.validate_on_submit():
        # Check if deleting note
        if form.delete.data:
          # Redirect to delete note
          return redirect(url_for('deletenote', NoteID=NoteID))
        # Set note to form data
        note.title = form.title.data
        note.note = form.note.data
        # Update note last edited timestamp to now
        note.last_edited = datetime.utcnow()
        # Save the changes
        db.session.commit();
        # Redirect to the note detail page
        return redirect(url_for('singlenote', NoteID=NoteID))
    # Set the form data from the note
    form.title.data = note.title
    form.note.data = note.note
    # Render the edit not page from the template and form
    return render_template('editnote.html', title='Edit', form=form);

@app.route('/notes/delete/<NoteID>')
@login_required
def deletenote(NoteID):
    """Route to delete a note

    Parameters:
        NoteID: The unique identifier of the note to delete

    Returns:
        Redirect to the notes list page
    """
    # Query note by idenifier
    note = Note.query.filter_by(id=int(NoteID)).first()
    # Check note exists and is authored by current user
    if note is not None and note.user_id == current_user.id:
        # Save the note title
        title = note.title;
        # Delete the note
        db.session.delete(note)
        db.session.commit()
        # Flash a successful delete message
        flash("Deleted note '" + title + "'.")
    # Redirect to notes list page
    return redirect(url_for('notes'))

@app.route('/notes/<NoteID>')
@login_required
def singlenote(NoteID):
    """Route for note detail

    Parameters:
        NoteID: The unique identifier of the note

    Returns:
        Rendering of the note detail page or redirects to notes list page if the note can not be found
    """
    # Query note by identifier
    note = Note.query.filter_by(id=int(NoteID)).first()
    # Check note exists and is authored by current user
    if note is None or note.user_id != current_user.id:
        # Redirect to notes list page
        return redirect(url_for('notes'))
    # Render note detail from the template and note
    return render_template('singlenote.html', title=note.title, note=note)

@app.route('/api/timezones')
@app.route('/api/timezones/<CountryID>')
def gettimezones(CountryID=None):
    """Get time zone names by country code

    Parameters:
        CountryID: The country code for which to get the time zones

    Returns:
        A dictionary of time zones
    """
    # Check country code is valid
    if CountryID in country_timezones:
        # Get time zones for country
        timezones = country_timezones[CountryID]
    else:
        # Get all time zones
        timezones = all_timezones
    # Convert timezones to JSON
    return jsonify([(tz, tz) for tz in timezones])
