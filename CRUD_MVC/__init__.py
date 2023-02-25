from flask import Flask
from flask_migrate import Migrate
from CRUD_MVC.models.model import db
from CRUD_MVC.routes.routes import employee_manager
from CRUD_MVC.config.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(employee_manager, url_prefix='/employee')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
