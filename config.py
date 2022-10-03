import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #against attacks, generate signiture or tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SESSION_PERMANENT = True
    SESSION_TYPE= "filesystem"
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://yoguupsymkqcab:45e0edd4229991c42dbe18ee7386be68b0673abecc9203e51f' \
                              '5f408c052aa6e0@ec2-54-155-110-181.eu-west-1.compute.amazonaws.com:5432/d25fdvi0lvl60f'
    #signal to app about changes in db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_USERNAME = '34c508781b963a'
    MAIL_PASSWORD= 'af0939aa4ca29e'