#!/usr/bin/python3
"""status checking
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """returns status ok"""
    return jsonify({'status': 'OK'})
