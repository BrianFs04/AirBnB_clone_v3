#!/usr/bin/python3
""" creating blueprint """
from flask import Blueprint
app_views = Blueprint('name', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
