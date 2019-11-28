from app import app, db, mail
from datetime import datetime, timezone, timedelta
from app.models import User, Note, Tag, Note_Tags, Reminder
from flask_mail import Mail, Message

def sendmail():
    reminders = Reminder.query.all()
    for reminder in reminders:
        if not reminder.already_reminded and reminder.reminder_date <= datetime.utcnow():
            user = User.query.filter_by(id=reminder.user_id).first()
            msg = Message(reminder.title, sender="noteweavermail@gmail.com", recipients=[user.email])
            msg.body = reminder.reminder
            mail.send(msg)
            reminder.already_reminded = True
            db.session.commit()

sendmail()
