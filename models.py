from app import db

class File(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filekey = db.Column(db.String(32), unique = True)
	filepath = db.Column(db.String(260))
	filename = db.Column(db.String(100))
	deletetime = db.Column(db.DateTime)
	from_ip = db.Column(db.String(15))
	loads = db.Column(db.Integer, default = 0)

	def __repr__(self):
		return '<Post %r>' % (self.body)