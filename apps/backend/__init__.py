from flask import Blueprint

backend = Blueprint('backend', __name__, url_prefix='/backend')
from apps.backend import views
