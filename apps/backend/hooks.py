from flask import session, g
from apps.backend import backend
from apps.backend.models import BackendUser
from config import config


@backend.before_request
def before_request():
    if config['development'].BACKEND_USER_ID in session:
        user_id = session.get(config['development'].BACKEND_USER_ID)
        user = BackendUser.query.get(user_id)
        if user:
            g.backend_user = user
        else:
            g.backend_user = None
    else:
        g.backend_user = None
