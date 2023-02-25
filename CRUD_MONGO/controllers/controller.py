import json

from ..database.model import collection_ece, collection_cse, collection_bme
from flask import request, jsonify
from bson import json_util


def insert_data(args):
    dict_res = {}
    for key, value in args.items():
        dict_res[key] = value
    return dict_res


def gen_response(result):
    response = []
    for item in result:
        sanitized = dict(json.loads(json_util.dumps(item.items())))
        response.append(sanitized)
    return jsonify({
        'data': response
    })


def create_student():
    obj = insert_data(request.args)
    if request.args["dept"] == "cse":
        result = collection_cse.insert_one(obj)
    elif request.args["dept"] == "ece":
        result = collection_ece.insert_one(obj)
    else:
        result = collection_bme.insert_one(obj)
    return jsonify({
        '_id': str(result.inserted_id)
    })


def get_student(roll):
    if request.args["dept"] == "cse":
        result = collection_cse.find_one({'roll_num': roll})
    elif request.args["dept"] == "ece":
        result = collection_ece.find_one({'roll_num': roll})
    else:
        result = collection_bme.find_one({'roll_num': roll})
    return gen_response(result)


def get_students():
    if request.args["dept"] == "cse":
        result = collection_cse.find()
    elif request.args["dept"] == "ece":
        result = collection_ece.find()
    else:
        result = collection_bme.find()
    return gen_response(result)


def update_student(roll):
    roll = str(roll)
    obj = insert_data(request.args)
    if request.args["dept"] == "cse":
        result = collection_cse.update_one({'roll_num': roll}, {'$set': obj})
    elif request.args["dept"] == "ece":
        result = collection_ece.update_one({'roll_num': roll}, {'$set': obj})
    else:
        result = collection_bme.update_one({'roll_num': roll}, {'$set': obj})
    return jsonify({
        'count': result.matched_count,
    })


def delete_student(roll):
    roll = str(roll)
    if request.args["dept"] == "cse":
        result = collection_cse.delete_one({'roll_num': roll})
    elif request.args["dept"] == "ece":
        result = collection_ece.delete_one({'roll_num': roll})
    else:
        result = collection_bme.delete_one({'roll_num': roll})
    return jsonify({
        'count': result.deleted_count,
    })
