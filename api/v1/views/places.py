#!/usr/bin/python3
"""places api view
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def getplace_cities(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_one_place(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)

    data['city_id'] = city_id
    new_place = place.Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    if not request.json:
        abort(400, "Not a JSON")

    states = request.json.get('states', [])
    cities = request.json.get('cities', [])
    amenities = request.json.get('amenities', [])

    places = storage.all("Place").values()

    if not states and not cities and not amenities:
        return jsonify([place.to_dict() for place in places])

    results = []
    for place_obj in places:
        place = place_obj.to_dict()
        if states:
            if place['city']['state_id'] in states:
                results.append(place)
        if cities:
            if place['city_id'] in cities:
                results.append(place)

    if amenities:
        results = [
            place for place in results
            if all(amenity_id in place['amenities'] for amenity_id in amenities)
        ]

    return jsonify(results)
