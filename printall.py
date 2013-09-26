from app import db, app
from models import File
from datetime import date, datetime, time, timedelta

def printall():
	old = File.query.all()
	if old != None:
		for e in old:
			print "%s %s %s" % (e.filename, e.deletetime.strftime("%Y-%m-%d"), e.from_ip)
printall()