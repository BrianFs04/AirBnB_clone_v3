#!/usr/bin/python3
""" creating a new app """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """ close the storage """
    storage.close()


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    API_HOST = getenv('HBNB_API_HOST')
    API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not API_HOST else API_HOST
    port = 5000 if not API_PORT else API_PORT
    app.run(host=host, port=port, threaded=True)
