#!/usr/bin/python3
"""View for State"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ List of states """
    states = storage.all(State).values()
    state = []
    for val in states:
        state.append(val.to_dict())
    return (jsonify(state))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def no_state_id(state_id):
    """ No state id """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    return (jsonify(states.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_id(state_id):
    """ Deletes a state object """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    storage.delete(states)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state_id():
    """ Create a state object """
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    if 'name' not in re:
        abort(400, 'Missing name')
    state = State(**re)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_id(state_id):
    """ Update a state object """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    for k, v in re.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(states, k, v)
    storage.save()
    return make_response(jsonify(states.to_dict()), 200)
