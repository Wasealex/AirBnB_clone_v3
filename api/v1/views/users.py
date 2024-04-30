#!/usr/bin/python3
"""users api view
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, user


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getall_users():
    user_list = []
    users = storage.all("User").values()
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_one_user(user_id):
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    new_user = user.User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
