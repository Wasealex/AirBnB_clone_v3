#!/usr/bin/python3
"""
"""
from flask import jsonify

@app_views.route("/status", strict_slashes=Flase)
def status():
  """returns status ok"""
  return jsonify({'status': 'OK'})
