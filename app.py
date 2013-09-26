from flask import Flask, render_template, flash, redirect, request, send_file, send_from_directory
from werkzeug import secure_filename
from forms import SendForm
from flask.ext.sqlalchemy import SQLAlchemy
import hashlib
from datetime import date, datetime, time, timedelta
import uuid
import os
from sevenzip_jpeg import Make7zJpeg

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from models import File

def unique_id():
    return hashlib.md5(hex(uuid.uuid4().time)[2:-1]).hexdigest()

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

@app.route('/', methods = ['GET', 'POST'])
def index():
    import tempfile
    form = SendForm()
    if form.validate_on_submit():
        srcfile = request.files['file']
        imgfile = request.files['img']
        password = request.form['pwd']
        uid = unique_id()
        dir = os.path.join(app.config['UPLOADED_FILES_DEST'], uid)
        if not os.path.exists(dir):
            os.makedirs(dir)
        if(srcfile.filename != imgfile.filename):
           tfn = os.path.join(dir, secure_filename(srcfile.filename))
        else:
            tfn = os.path.join(dir, secure_filename("0_" + srcfile.filename))
        filepath = os.path.join(dir, secure_filename(imgfile.filename))
        imgfile.save(filepath)
        srcfile.save(tfn)
        szip_out = Make7zJpeg(os.path.abspath(tfn), filepath, filepath, password)
        if __debug__:
            print(szip_out)
        os.remove(tfn)
        deltime = datetime.combine(date.today(), time()) + timedelta(days=30)
        rec = File(filepath = filepath, filename = imgfile.filename, filekey = uid, deletetime = deltime, from_ip = request.remote_addr)
        db.session.add(rec)
        db.session.commit()
        return redirect("/" + str(rec.id) + '/' + uid)
    return render_template("index.html", form = form)

@app.route('/<fid>/<fkey>')
def showfile(fid, fkey):
    entry = File.query.filter_by(id=fid).first()
    if entry is None or entry.filekey != fkey:
        return render_template("error.html", errortitle = u"Файл не найден")
    fsize = os.path.getsize(entry.filepath)
    return render_template("showfile.html", file = entry, fileurl = '/img/' + fid + '/' + fkey, filesize = sizeof_fmt(fsize), showimg = (fsize <= 2 * 1024 * 1024))
	
@app.route('/img/<fid>/<fkey>')
def loadfile(fid, fkey):
    entry = File.query.filter_by(id=fid).first()
    if entry.filekey == fkey:
        return send_file(entry.filepath.encode('utf-8'))
    else:
        return render_template("error.html", errortitle = u"Файл не найден")