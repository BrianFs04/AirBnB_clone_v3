#!/usr/bin/python3
""" Places_reviews view """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """ returns a json string with the reviews"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    place = []
    for val in places.reviews:
        place.append(val.to_dict())
    return (jsonify(place))


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review(review_id):
    """ returns a json string with a specific review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return (jsonify(review.to_dict()))


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes a review """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def creates_review(place_id):
    """ creates a review """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in re:
        abort(400, 'Missing user_id')
    user = storage.get(User, re['user_id'])
    if not user:
        abort(404)
    if 'text' not in re:
        abort(400, 'Missing text')
    review = Review(**re)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def updates_review(review_id):
    """ updates a review """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    re = request.get_json()
    if re is None:
        abort(400, 'Not a JSON')
    for k, v in re.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
