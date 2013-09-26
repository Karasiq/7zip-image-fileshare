import os
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_FILES_DEST = 'files'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024; # 50 Мегабайт

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/fileshare'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'changeme'