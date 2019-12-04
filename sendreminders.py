from app import create_app, db, mail
from app.models import User, Note
from flask_mail import Message

def sendmail():
    reminders = Note.query.all()
    for reminder in reminders:
        if not reminder.already_reminded and not reminder.reminder_date is None and reminder.reminder_date <= datetime.utcnow():
            user = User.query.filter_by(id=reminder.user_id).first()
            msg = Message(reminder.title, sender=current_app.config['USER_EMAIL'], recipients=[user.email])
            msg.body = reminder.reminder
            mail.send(msg)
            reminder.already_reminded = True
            db.session.commit()

app = create_app()
with app.app_context():
    sendmail()

