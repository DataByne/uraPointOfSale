from app import app, db, mail, login_manager
from datetime import datetime, timezone, timedelta
from flask import render_template, send_from_directory, flash, redirect, session, url_for, request, jsonify, Response
from app.forms import LoginForm, RegisterForm, NoteForm, EditNoteForm, EditUserForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
from app.models import User, Note, Tag, Note_Tags
from pytz import all_timezones, country_names, country_timezones
from werkzeug.urls import url_parse
from sqlalchemy import or_, desc
from sqlalchemy.sql.functions import func
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask_mail import Mail, Message
import operator

def login_expired(timeout=timedelta(minutes=1)):
    """Check whether a login session expired by timing out after a specified interval

    Returns:
        Whether a login session is expired
    """
    # Check the session expired
    if 'start' not in session or (datetime.utcnow() - session['start']) > timeout:
        # clear the session
        session.clear()
        return True
    # Session is still fresh enough
    return False

@app.route('/')
@app.route('/index')
def index():
    """Route for landing page

    Returns:
        Rendering of the landing page
    """
    userNotes = None
    numNotes = None
    time = None
    average_count = 0
    if not current_user.is_anonymous:
        userNotes = Note.query.order_by(desc(Note.note_date)).filter_by(user_id=current_user.id).limit(5).all()
        numNotes = Note.query.filter_by(user_id=current_user.id).count()
        if (numNotes > 0):
            time = datetime.utcnow() - userNotes[0].note_date
        notes = Note.query.filter_by(user_id=current_user.id).all()
        temp = 0
        for note in notes:
            temp = temp + len(note.note)
        if len(notes) != 0:
            average_count = temp / len(notes)
            average_count = int(average_count)
    return render_template('index.html', title='Home', notes=userNotes, num=numNotes, time=time, average_count=average_count)

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

@app.route('/images/user_activity_by_weekday.png')
def user_activity_by_weekday_png():
    #This is the figure to modify
    fig = Figure(figsize=(9,5))
    #This is the stuff the makes the images
    weekdata = [0,0,0,0,0,0,0]
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dates = Note.query.filter_by(user_id=current_user.id).all()
    for date in dates:
        weekdata[date.note_date.weekday()] = weekdata[date.note_date.weekday()] + 1
    axis = fig.add_subplot(1,1,1)
    axis.bar(weekdays,weekdata)
    axis.set_xlabel('Days of the Week')
    axis.set_ylabel('Notes Made on that Day')
    axis.set_title('Notes Made on Each Day of the Week')
    #This just displays it
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/images/user_tag_useage.png')
def user_tag_useage_png():
    #This is the figure to modify
    fig = Figure(figsize=(9,5))
    #This is the stuff the makes the images
    notes = Note.query.filter_by(user_id=current_user.id).all()
    note_totals = {}
    for note in notes:
        tags = getTagsList(note.id)
        for tag in tags:
            if tag in note_totals:
                note_totals[tag] = note_totals[tag] + 1
            else:
                note_totals[tag] = 1
    axis = fig.add_subplot(1,1,1)
    lists = sorted(note_totals.items(), key=operator.itemgetter(1), reverse=True)
    x, y = zip(*lists)
    axis.bar(x,y)
    axis.set_xlabel('Tags')
    axis.set_ylabel('Times Used')
    axis.set_title('Most Used Tags')
    #This just displays it
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/scripts/<path:path>')
def send_scripts(path):
    """Route for static script files

    Parameters:
        path: The path of the static script file

    Returns:
        Static content from the 'scripts' directory
    """
    return send_from_directory('scripts', path)

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
    if request.method == 'POST' and form.validate_on_submit():
        # Create a new user model from the form data
        user = User(username=form.username.data, email=form.email.data, country=form.country.data, time_zone=form.time_zone.data)
        # Set the user model password hash
        user.set_password(form.password.data)
        # Add the model to the database
        db.session.add(user)
        db.session.commit()
        # Flash a successfully register message
        flash("Succesfully registered new user '" + user.username + "'.", 'success')
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
@fresh_login_required
def edituser(UserID):
    """Route for user edits

    Parameters:
        UserID: used to find the user tuple and passed by html page

    Returns:
        redirect to user page if not right user or user edit page render
    """
    #finds user
    user = User.query.filter_by(id=int(UserID)).first()
    #redirects if not the valid user
    if user is None or user.id != current_user.id:
        return redirect(url_for('user', UserID=current_user.id))
    # Check if the session expired
    if login_expired():
        # redirect to the login
        flash('Please login to edit your profile.', 'info')
        return redirect(url_for('login', next=url_for('edituser', UserID=UserID)))
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
    if request.method == 'POST' and form.validate_on_submit():
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
@fresh_login_required
def deleteuser(UserID):
    """Route for deleting a user

    Parameters:
        UserID: used to find the user tuple and all user notes as well as veryify the correct user is deleting themself

    Returns:
        Redirect to logout
    """
    #redirects user if they are trying to delete another users account
    if UserID is None or current_user.id != int(UserID):
        return redirect(url_for('user', UserID=current_user.id))
    # Check if the session expired
    if login_expired(timedelta(seconds=2)):
        # redirect to the login
        flash('Please login to delete your account.', 'warning')
        return redirect(url_for('login', next=url_for('deleteuser', UserID=UserID)))
    #finds user tuple
    user = User.query.filter_by(id = int(UserID)).first()
    flash("Successfully deleted the user '" + user.username + "' and all authored notes.", 'success');
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
    if request.method == 'POST':
        if form.validate_on_submit():
            # Query the user by user name
            user = User.query.filter_by(username=form.username.data).first()
            # Check if the user was found
            if user is None:
                # Query the user by email address
                user = User.query.filter_by(email=form.username.data).first()
            # Check user exists and the password hash matches
            if user is not None and user.check_password(form.password.data):
                # Login user
                login_user(user, remember=form.rememberMe.data)
                # set session information
                app.permanent_session_lifetime = timedelta(days=1)
                session.setdefault('start', datetime.utcnow())
                session.permanent = True
                session.modified = True
                #store url user was trying to access
                next_page = request.values.get('next')
                #if there is no next argument or if next arg is set to a full url, redirect to index
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
        # Flash error that user could not be authenicated
        flash('Login authentication failed.', 'danger')
    # Set the hidden form next so the correct next redirect will happen
    form.next.data = request.values.get('next');
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
    # Flash message that user logged out
    flash('Successfully logged out.', 'success')
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

    #This gets all the tags of a note
    tags = {}
    for note in userNotes:
        actual_tags = getTagsString(note.id)
        if len(actual_tags) == 0:
            tags[note.id] = ""
        else:
            tags[note.id] = actual_tags
    #
    return render_template('notes.html', title='Your Notes', notes=userNotes, search=False, taglist=tags)

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
    if request.method == 'POST' and form.validate_on_submit():
        # Create a new note from the form data
        newnote = Note(title = form.title.data, note=form.note.data, user_id=current_user.id)
        # Add the note to the database
        db.session.add(newnote)

        #This is the temporary stuff to add nots, if a better way is added this is the stuff to replace
        str = form.tags.data
        tags_list = str.split(',')
        for tag in tags_list:
            tag.strip()
            tag.strip(',')
        note = Note.query.order_by(desc(Note.note_date)).filter_by(user_id=current_user.id).first()
        for tag in tags_list:
            setTag(note.id, tag)

        #So ends the hopeful temporary stuff

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
    if request.method == 'POST' and form.validate_on_submit():
        # Check if deleting note
        if form.delete.data:
          # Delete note
          return deletenote(NoteID)
        # Set note to form data
        note.title = form.title.data
        note.note = form.note.data
        # Update note last edited timestamp to now
        note.last_edited = datetime.utcnow()
        # Save the changes
        db.session.commit()
        # Redirect to the note detail page
        return redirect(url_for('notes'))
    # Set the form data from the note
    form.title.data = note.title
    form.note.data = note.note
    form.tags.data = getTagsString(NoteID)
    # Render the edit not page from the template and form
    return render_template('editnote.html', title='Edit', form=form, NoteID=NoteID)

@app.route('/notes/delete/<NoteID>', methods=['GET', 'POST', 'DELETE'])
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
        # Flash a successful delete message
        flash("Deleted note '" + note.title + "'.", 'success')
        # Delete the note
        db.session.delete(note)
        db.session.commit()
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

@app.route('/notes/search/')
@app.route('/notes/search')
@app.route('/notes/search/<Query>')
@login_required
def searchnote(Query=''):
    """Route for searching notes by query text

    Parameters:
        Query The query text for searching

    Returns:
        Rendering of the notes list page filtered by the query text search
    """
    notes = None
    if Query is not None and Query != '':
        notes = Note.query.filter(or_(Note.title.ilike('%'+ Query+ '%'), Note.note.ilike('%'+ Query+ '%')), Note.user_id==current_user.id)
    elif Note.query.filter(Note.user_id==current_user.id).count() <= 0:
        Query = False;
    return render_template('notes.html', title='Search Results', notes=notes, search=Query)

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

def getTagsList(NoteID):
    links = Note_Tags.query.filter_by(note_id=NoteID).all()
    tags = []
    for link in links:
        tmptag = Tag.query.filter_by(id=link.tag_id).first()
        if tmptag != None:
            tags.append(tmptag.tag)
    return tags

def getTagsString(NoteID):
    links = Note_Tags.query.filter_by(note_id=NoteID).all()
    tags = []
    for link in links:
        tmptag = Tag.query.filter_by(id=link.tag_id).first()
        if tmptag != None:
            tags.append(tmptag.tag)
    return_string = str(tags).strip("[]").replace("'","")
    return return_string

def setTag(NoteID, tag):
    temp = Tag.query.filter_by(tag=tag).first()
    if temp == None:
        new_tag = Tag(tag=tag)
        db.session.add(new_tag)
        temp = Tag.query.filter_by(tag=tag).first()
    new_note_tag = Note_Tags(note_id = NoteID, tag_id = temp.id)
    db.session.add(new_note_tag)
    db.session.commit()
