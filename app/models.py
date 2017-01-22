from app import db


class User(db.Model):
    __table__ = db.Model.metadata.tables['tusers']
    id = __table__.c.uid
    username = __table__.c.username
    name = __table__.c.name
    email = __table__.c.email
    password = __table__.c.password

    def __repr__(self):
        return '<user %r>' % (self.username)

    def __init__(self, username, email, name, password):
        self.username = username
        self.email = email
        self.name = name
        self.password = password
