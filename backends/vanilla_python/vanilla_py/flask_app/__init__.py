import os
from flask import Flask, jsonify
from pathlib import Path
from flask_cors import CORS
from flask_app.blueprints.phase_0_simple_api import simple_api
from . import db

def create_app(test_config =None):
    # create and configure the app 
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.register_blueprint(simple_api, url_prefix = '/api')
    
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["DATABASE"] = os.path.join(app.instance_path, "app.db")
    print("DB PATH:", app.config["DATABASE"])
    db.init_app(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
 
    return app

    