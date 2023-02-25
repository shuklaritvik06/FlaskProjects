import json

from ..models.model import db, User
from jwt import (
    JWT,
    jwk_from_dict,
)
from flask import request, jsonify

instance = JWT()


def login_user():
    token = request.json["token"]
    with open('key.json', 'r') as f:
        verifying_key = jwk_from_dict(json.load(f))
    message_received = instance.decode(token, verifying_key, do_time_check=True, do_verify=True)
    try:
        current_user = User.query \
            .filter_by(email=message_received['email']) \
            .first()
        if current_user:
            return jsonify({
                "message": {
                    "email": current_user.email
                }
            })
        else:
            return jsonify({
                "message": "User not found!"
            })
    except ValueError as e:
        return jsonify({
            'message': 'Token is invalid !!'
        })


def register_user():
    email = request.json["email"]
    password = request.json["password"]
    message = {
        "email": email,
        "password": password
    }
    with open('key.json', 'r') as f:
        signing_key = jwk_from_dict(json.load(f))
    token = instance.encode(message, signing_key, alg='RS256')
    user = User(
        email=email,
        password=password,
        token=token
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "token": token
    })


def delete_user():
    token = request.json["token"]
    with open('key.json', 'r') as f:
        verifying_key = jwk_from_dict(json.load(f))
    message_received = instance.decode(token, verifying_key, do_time_check=True, do_verify=True)
    try:
        current_user = User.query \
            .filter_by(email=message_received['email']) \
            .first()
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({
            "message": "User Deleted!"
        })
    except ValueError as e:
        return jsonify({
            'message': 'Token is invalid !!'
        })
