#!/usr/bin/python3
"""cities api view
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, city, state


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def getcity_states(state_id):
    state = storage.get("State", state_id)
    if state:
        city_list = []
        for city in state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list), 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_one_city(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    new_city = city.City(state_id=state_id, **data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
