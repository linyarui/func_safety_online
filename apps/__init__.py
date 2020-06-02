from flask import Flask
from exts import db
from exts import mail
from config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    db.init_app(app)
    mail.init_app(app)

    from apps.front import api
    api.init_app(app)

    from apps.backend import backend as backend_blueprint
    app.register_blueprint(backend_blueprint)
    from apps.common import common as common_blueprint
    app.register_blueprint(common_blueprint)
    from apps.front import front as front_blueprint
    app.register_blueprint(front_blueprint)

    return app
