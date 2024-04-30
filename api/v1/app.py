#!/usr/bin/python3
"""set up flask app
"""
from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close session"""
    storage.close()


@app.errorhandler(404)
def handle_error_page(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
