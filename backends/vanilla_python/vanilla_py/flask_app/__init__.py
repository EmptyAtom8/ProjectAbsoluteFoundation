import os
from flask import Flask, jsonify
from pathlib import Path
from flask_cors import CORS
from flask_app.blueprints.phase_0_simple_api import simple_api

def create_app(test_config =None):
    # create and configure the app 
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.register_blueprint(simple_api, url_prefix = '/api')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
 
    return app

    