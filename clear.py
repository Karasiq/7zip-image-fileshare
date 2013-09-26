from app import db, app
from models import File
from datetime import date, datetime, time, timedelta
import os
import shutil

def clean():
	old = File.query.all()
	i = 0
	if old != None:
		for e in old:
			dir = os.path.join(app.config['UPLOADED_FILES_DEST'], e.filekey)
			if os.path.exists(dir): shutil.rmtree(dir)
			db.session.delete(e)
			i = i + 1
	db.session.commit()
	print "Deleted %d entries" % (i)
	
clean()