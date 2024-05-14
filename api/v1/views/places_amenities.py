#!/usr/bin/python3
"""link place and amenityes
"""
from flask import jsonify, abort, request
from models import storage, amenity, place
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_ameities(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity_list = []
    for amenity in place.amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201
