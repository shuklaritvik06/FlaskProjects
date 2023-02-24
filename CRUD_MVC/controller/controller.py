from CRUD_MVC.models.model import Employee, db
from flask import request, jsonify


def get_employees():
    employees = db.session.execute(db.select(Employee).order_by(Employee.id)).scalars()
    data = []
    for i in employees:
        data.append(i.serialize)
    return jsonify({
        'data': data
    })


def create_employee():
    employee = Employee(
        name=request.args["name"],
        age=request.args["age"],
        address=request.args["address"],
        dept=request.args["dept"]
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify({
        'data': employee.serialize
    })


def get_employee(id):
    employee = db.get_or_404(Employee, id)
    return jsonify({
        'data': employee.serialize
    })


def delete_employee(id):
    employee = db.get_or_404(Employee, id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({
        'data': employee.serialize
    })


def update_employee(id):
    employee = db.get_or_404(Employee, id)
    for key, value in request.args.items():
        if key == "name":
            employee.name = value
        elif key == "age":
            employee.age = value
        elif key == "address":
            employee.address = value
        else:
            employee.dept = value

    db.session.commit()
    return jsonify({
        'data': employee.serialize
    })
