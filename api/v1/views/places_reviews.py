#!/usr/bin/python3
"""places_review api view
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def getreview_place(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place_reviews = []
    for review in place.reviews:
        place_reviews.append(review.to_dict())
    return jsonify(place_reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_one_review(review_id):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviewies/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'text')
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)

    new_review = review.Review(**data)
    review.place_id = place_id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
