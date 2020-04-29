#!/usr/bin/python3
""" index """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """ returns a json string with the places"""
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    city = []
    for val in cities.places:
        city.append(val.to_dict())
    return (jsonify(city))


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place(place_id):
    """ returns a json string with the place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return (jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ deletes a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ creates a place """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in re:
        abort(400, 'Missing user_id')
    user = storage.get(User, re['user_id'])
    if not user:
        abort(404)
    if 'name' not in re:
        abort(400, 'Missing name')
    place = Place(**re)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Updates a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    for k, v in re.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
