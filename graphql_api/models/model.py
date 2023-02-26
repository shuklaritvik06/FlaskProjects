from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    orders = db.relationship("Orders", backref="customer")


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    delivery_address = db.Column(db.String, nullable=False)
    delivery_date = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
