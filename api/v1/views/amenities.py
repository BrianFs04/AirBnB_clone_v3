#!/usr/bin/python3
"""View for Amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ List of amenities """
    amenities = storage.all(Amenity).values()
    amenity = []
    for val in amenities:
        amenity.append(val.to_dict())
    return (jsonify(amenity))


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Amenity object id """
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    return (jsonify(amenities.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an amenity object """
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an amenity object """
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    if 'name' not in re:
        abort(400, 'Missing name')
    amenity = Amenity(**re)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an amenity object """
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    for k, v in re.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenities, k, v)
    storage.save()
    return make_response(jsonify(amenities.to_dict()), 200)
