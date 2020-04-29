#!/usr/bin/python3
"""View for User"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ List of users """
    users = storage.all(User).values()
    user = []
    for val in users:
        user.append(val.to_dict())
    return (jsonify(user))


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user(user_id):
    """ User object id """
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    return (jsonify(users.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes an user object """
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    storage.delete(users)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates an user object """
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    if 'email' not in re:
        abort(400, 'Missing email')
    if 'password' not in re:
        abort(400, 'Missing password')
    user = User(**re)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Update an user object """
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    for k, v in re.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(users, k, v)
    storage.save()
    return make_response(jsonify(users.to_dict()), 200)
