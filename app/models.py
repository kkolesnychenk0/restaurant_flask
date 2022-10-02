# classes for db
from datetime import datetime
import jwt as jwt
from time import time
from app import db, login,app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_number=db.Column(db.Integer)
    orders = db.relationship('Order', backref='orders', lazy='dynamic')

    def __repr__(self):
        return f'{self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64), index=True)
    product_type = db.Column(db.String(64), index=True)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Products_for_order', backref='product', lazy=True)


    def __repr__(self):
        return f'Product {self.product_name}'


class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    items = db.relationship('Products_for_order', backref='order', lazy=True)

    def __repr__(self):
        return f'{self.order_id}'

class Products_for_order(db.Model):
    __tablename__ = 'products_for_order'
    pr_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    quantity = db.Column(db.Integer)
    total_price=db.Column(db.Float)

    def __repr__(self):
        return f'{self.quantity,self.total_price}'

