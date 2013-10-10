from flask import Flask, render_template, flash, redirect, request, send_file, send_from_directory
from werkzeug import secure_filename
from forms import SendForm
from flask.ext.sqlalchemy import SQLAlchemy
import hashlib
from datetime import date, datetime, time, timedelta
import uuid
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from models import File

def utf8str(src):
	return src.decode('utf-8')

def unique_id():
    return hashlib.md5(hex(uuid.uuid4().time)[2:-1]).hexdigest()

def access_token(filekey, ip):
	return hashlib.sha224(date.today().strftime("%Y-%m-%d") + filekey + ip).hexdigest()

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

@app.route('/favicon.ico')
def favicon():
	return send_from_directory('static', 'favicon.ico')
	
@app.route('/', methods = ['GET', 'POST'])
def index():
	form = SendForm()
	if form.validate_on_submit():
		file = request.files['file']
		uid = unique_id()
		dir = os.path.join(app.config['UPLOADED_FILES_DEST'], uid)
		if not os.path.exists(dir):
			os.makedirs(dir)
		
		filepath = os.path.join(dir, secure_filename(file.filename))
		file.save(filepath)
		deltime = datetime.combine(date.today(), time()) + timedelta(days=30)
		rec = File(filepath = filepath, filename = file.filename, filekey = uid, deletetime = deltime, from_ip = request.remote_addr)
		db.session.add(rec)
		db.session.commit()
		return redirect("/" + uid)
		# return render_template("file.html", filename = filename, deltime = deltime)
	
	return render_template("index.html", form = form)

@app.route('/<filekey>')
def showfile(filekey):
	file = File.query.filter_by(filekey=filekey).first()
	if(file is None):
		return render_template("error.html", errortitle = utf8str("Файл не найден"))

	return render_template("showfile.html", file = file, fileurl = '/load/' + filekey + '/' + access_token(filekey, request.remote_addr), filesize = sizeof_fmt(os.path.getsize(file.filepath)))
	
@app.route('/load/<filekey>/<accesstoken>')
def loadfile(filekey, accesstoken):
	if access_token(filekey, request.remote_addr) != accesstoken:
		return redirect('/' + filekey)
		# return render_template("error.html", errortitle = utf8str("Ошибка доступа"))
	file = File.query.filter_by(filekey=filekey).first()
	file.loads += 1
	db.session.add(file)
	db.session.commit()
	return send_file(file.filepath.encode('utf-8'), None, True, file.filename.encode('utf-8'))