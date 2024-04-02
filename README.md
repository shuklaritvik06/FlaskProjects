# Flask Projects

![banner](https://github.com/shuklaritvik06/FlaskProjects/assets/72812470/5422174d-f718-45a8-95df-b32d976667b8)

Welcome to the Flask Projects repository.

## Application Context

Application context is an application-level context in Flask that represents the state and configurations of the Flask application. It holds information such as configuration settings, registered blueprints, and extensions. The application context is created when the Flask application starts running and is destroyed when the application stops.

In Flask, you can access the application context using the `current_app` proxy or by using the `app_context()` method.

```python
from flask import current_app

current_app.config['DEBUG'] = True

with app.app_context():
    pass
```

## Request Context

Request context is a request-level context in Flask that represents the state of an individual request made to the Flask application. It contains information about the current request such as request headers, request method, request data, and request parameters. Flask automatically creates and manages request contexts for each incoming request.

In Flask, you can access the request context using the `request` proxy.

```python
from flask import request

request.method  
request.args    
request.form    
request.headers 
```

## Projects

- [x] Basic Authentication
- [x] CRUD MONGO
- [x] CRUD SQLite
- [x] JWT Authentication
- [x] Relationships in Database
- [x] WTForms
- [x] OAuth Authentication
- [x] File Upload
- [x] Graphql
- [x] Websocket
