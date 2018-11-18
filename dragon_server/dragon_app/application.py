import logging.config

import os
from flask import Flask, Blueprint
from dragon_app import settings
from dragon_app.api.simulations.simulations import ns as simulation_namespace 
from dragon_app.api.restplus import api
from dragon_app.database import db

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['HDFILE_PATH'] = settings.HDFILE_PATH

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(simulation_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)

def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<<'.format(app.config['SERVER_NAME']))
    settings.HDFILE_PATH = "/Users/xiedandan/Desktop/dragon/dragon-platform/dragon_server/data/"
    app.run(debug = settings.FLASK_DEBUG)
    # app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    main()
