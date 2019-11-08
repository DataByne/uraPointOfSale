from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(150), index = True, unique = True)
    creation_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), index = True)
    note = db.Column(db.String(500), index = True)
    note_date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    last_edited = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    def __repr__(self):
        return '<Note: {}>'.format(self.note)
