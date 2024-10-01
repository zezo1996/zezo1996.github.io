from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(150))

    # relationship
    products = db.relationship('Product', backref=db.backref('admin', lazy=True))

    # methods
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self,verify_password):
        return check_password_hash(self.password_hash,verify_password)





class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    # relationship
    cart_items = db.relationship('Cart', backref=db.backref('customer', lazy=True))
    orders = db.relationship('Order', backref=db.backref('customer', lazy=True))
    # hashing password
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self,verify_password):
        return check_password_hash(self.password_hash,verify_password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000),nullable=False)
    flash_sale = db.Column(db.Boolean,default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship
    carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
    
    orders = db.relationship('Order', backref=db.backref('product', lazy=True))

    # admin relationship
    admin_link =  db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)
    # relationship between cart and customer
    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    # relationshio between product and cart
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

