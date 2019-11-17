from app import app, db
from datetime import datetime
from flask import render_template, send_from_directory, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegisterForm, NoteForm, EditNoteForm, EditUserForm
from flask_login import current_user, logout_user, login_required
from app.models import User, Note
from pytz import all_timezones, country_names, country_timezones
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    """Route for landing page

    Returns:
        Rendering of the landing page
    """
    if not current_user.is_anonymous:
        userNotes = Note.query.filter_by(user_id=current_user.id).limit(5).all()
        numNotes = Note.query.filter_by(user_id=current_user.id).count()
        time = datetime.utcnow() - userNotes[0].note_date
    return render_template('index.html', title='Home', notes=userNotes, num=numNotes, time=time)


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


@app.route('/about')
def about():
    return render_template('about.html', title = 'About Us')

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
        flash("Succesfully registered new user '" + user.username + "'.")
        # Redirect to the login page
        return redirect(url_for('login'))
    # Render the registration page from the template and form
    return render_template('register.html', title="Register", form=form, country_names=country_names)


@app.route("/user/<UserID>")
@login_required
def user(UserID):
    """Route for user page

    Parameters:
        UserID: self explanatory, passed by the html page

    Returns:
        Rendering of user page, redirect to index if the current user is not the user of UserID
    """
    #gets the user from the user table
    user = User.query.filter_by(id = int(UserID)).first()
    #gets the count of total notes
    count = Note.query.filter_by(user_id = int(UserID)).count()
    #checks user is valid
    if user is None or user.id != current_user.id:
        return redirect(url_for('index'))
    #renders page
    return render_template('user.html', title=user.username, count=count)


@app.route('/user/edit/<UserID>', methods=['GET', 'POST'])
@login_required
def edituser(UserID):
    """Route for user edits

    Parameters:
        UserID: used to find the user tuple and passed by html page

    Returns:
        redicret to user page if not rigth user or user edit page render
    """
    #finds user
    user = User.query.filter_by(id=int(UserID)).first()
    #redirects if not the valid user
    if user is None or user.id != current_user.id:
        return redirect(url_for('user', UserID=current_user.id))
    form = EditUserForm()
    # Add country codes to the country code select field
    #This works for reasons, do not touch it or it will break
    CountryID = form.country.data
    if CountryID is None or CountryID == "" or CountryID.upper() == "NONE":
        CountryID = user.country
        if CountryID is None:
            CountryID = 'US'
    #sets choices for country and time zone fields
    form.country.choices = [(country_id, country_names[country_id]) for country_id in country_names]
    form.time_zone.choices = [(tz, tz) for tz in country_timezones[CountryID]]
    #updates user information, commits the changes and redirects back to the user page
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.country = form.country.data
        user.time_zone = form.time_zone.data
        #password fields are set to empty and passwords are only changed if they are modified in any way
        if form.password.data != "":
            user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('user', UserID=UserID))
    #sets the fields to the current user information
    form.username.data = user.username
    form.email.data = user.email
    form.country.data = user.country
    form.time_zone.data = user.time_zone
    #renders the page
    return render_template('edituser.html', title='Edit ' + current_user.username, form=form)

@app.route('/user/delete/<UserID>')
@login_required
def deleteuser(UserID):
    """Route for deleting a user

    Parameters:
        UserID: used to find the user tuple and all user notes as well as veryify the correct user is deleting themself

    Returns:
        redicret to logout that redirects to index
    """
    #redirects user if they are trying to delete another users account
    if UserID is None or current_user.id != int(UserID):
        return redirect(url_for('user', UserID=current_user.id))
    #finds user tuple
    user = User.query.filter_by(id = int(UserID)).first()
    flash("Successfully deleted the user '" + user.username + "' and all authored notes.");
    #finds all notes of the user and deletes them
    note = Note.query.filter_by(user_id=int(UserID)).first()
    while note is not None:
        db.session.delete(note)
        note = Note.query.filter_by(user_id=int(UserID)).first()
    #deletes user and commits the changes
    db.session.delete(user)
    db.session.commit()
    #logs the user out
    return logout()



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
       # user = User.query.filter_by(username=form.username.data).first()
        #store url user was trying to access
        next_page = request.args.get('next')
        #if there is no next argument or if next arg is set to a full url, redirect to index
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
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
    form = EditNoteForm()
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
        db.session.commit()
        # Redirect to the note detail page
        return redirect(url_for('singlenote', NoteID=NoteID))
    # Set the form data from the note
    form.title.data = note.title
    form.note.data = note.note
    # Render the edit not page from the template and form
    return render_template('editnote.html', title='Edit', form=form)

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
        title = note.title
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
