from app import db


class User(db.Model):
	__table__ = db.Model.metadata.tables['users']
	id = __table__.c.id
	username = __table__.c.login
	fname = __table__.c.fname
	lname = __table__.c.lname
	email = __table__.c.email
	phone = __table__.c.phone
	paycheck = __table__.c.pay_check
	password = __table__.c.password
	university = __table__.c.university

	def __repr__(self):
		return '<user %r>' % (self.username)

	def __init__(self, username, email, password, fname, lname, phone, university, paycheck):
		self.username = username
		self.email = email
		self.password = password
		self.fname = fname
		self.lname = lname
		self.phone = phone
		self.paycheck = paycheck
		self.university = university
