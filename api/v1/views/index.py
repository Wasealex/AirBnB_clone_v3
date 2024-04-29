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
    """stats for classess
    """
    stats = {}
    classes = {
        'amenities': storage.count('Amenity'),
        'basemodel': storage.count('BaseModel'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    for key, value in classes.items():
        stats[key] = value
    return jsonify(stats)
