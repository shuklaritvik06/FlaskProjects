from flask import Blueprint
from CRUD_MVC.controller.controller import get_employees, create_employee, update_employee, delete_employee, get_employee

employee_manager = Blueprint('employee_manager', __name__)

employee_manager.route('/', methods=['GET'])(get_employees)
employee_manager.route('/create', methods=['POST'])(create_employee)
employee_manager.route('/<int:id>', methods=['GET'])(get_employee)
employee_manager.route('/<int:id>/edit', methods=['POST'])(update_employee)
employee_manager.route('/<int:id>', methods=['DELETE'])(delete_employee)
