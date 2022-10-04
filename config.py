import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #against attacks, generate signiture or tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #signal to app about changes in db
    SQLALCHEMY_TRACK_MODIFICATIONS = False