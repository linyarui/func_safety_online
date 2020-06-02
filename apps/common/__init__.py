from flask import Blueprint

common = Blueprint('common', __name__, url_prefix='/common')
from apps.common import views
