import os
import unittest

import flask
from flask import session

from app import app,db
from app.models import User, Order
#from app.tests.web import create_app,db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None
    LOGIN_DISABLED=True
    WTF_CSRF_ENABLED = False
    DEBUG=False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'



class UserModelCase(unittest.TestCase):

    def setUp(self):
        #self.app = create_app(TestConfig)
        app.config.from_object(TestConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies=True)
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response=self.client.get('/')
        assert response.status_code==200

    def test_login_page(self):
        response = self.client.get('/login',follow_redirects=True)
        assert response.status_code==200

    def test_register_page(self):
        response = self.client.get('/register',follow_redirects=True)
        assert response.status_code==200

    def test_registration(self,):
        response=self.client.post('/register',
                                data={'username': 'test', 'password': 'test', 'password2': 'test',
                                      'phone_number': '1111111'},
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert b'Register' in response.data

    def login(self, username, password):
        return self.client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)

    def test_login(self):
        #response=self.client.post('/login', data={'username': 'test', 'password': 'test'}, follow_redirects=True)
        response=self.login('test','test')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Sign In' in response.data)


    def test_password_hashing(self):
        u = User(username='John')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))






if __name__ == '__main__':
    unittest.main(verbosity=2)