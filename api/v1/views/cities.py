#!/usr/bin/python3
""" index """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ returns a json string with the cities"""
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    state = []
    for val in states.cities:
        state.append(val.to_dict())
    return (jsonify(state))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """ returns a json string with a specific city"""
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    return (jsonify(cities.to_dict()))


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """ deletes a city """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    storage.delete(cities)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ deletes a city """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    if 'name' not in re:
        abort(400, 'Missing name')
    city = City(**re)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updated a city object """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    for k, v in re.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(cities, k, v)
    storage.save()
    return make_response(jsonify(cities.to_dict()), 200)
