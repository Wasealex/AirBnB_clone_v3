#!/usr/bin/python3
"""status checking
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """returns status ok"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    stats = {}
    classes = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('BaseModel'),
        'Places': storage.count('Place'),
        'Reviews': storage.count('Review'),
        'States': storage.count('State'),
        'Users': storage.count('User')
    }
    for key, value in classes.items():
        stats[key] = value
    return jsonify(stats)
