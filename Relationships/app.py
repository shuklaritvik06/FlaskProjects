from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

"""
One-To-Many Relationship
"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    pets = db.relationship("Pets", backref="owner")


class Pets(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


"""
Many-To-Many Relationship
"""

Employee_Dept = db.Table(
    "Employee_Dept",
    db.Column(
        "employee_id", db.Integer, db.ForeignKey("employee.id"), primary_key=True
    ),
    db.Column("dept_id", db.Integer, db.ForeignKey("dept.dept_id"), primary_key=True),
)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    departments = db.relationship(
        "Dept", secondary=Employee_Dept, backref=db.backref("employees", lazy=True)
    )


class Dept(db.Model):
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String, unique=True, nullable=False)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
