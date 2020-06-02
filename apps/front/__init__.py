from flask import Blueprint
from flask_restful import Api

front = Blueprint('front', __name__)
api = Api()
from apps.front import views
