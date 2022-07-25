import os
from datetime import timedelta 

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.adpater.sqlite_connexion import init_db
from src.services.users import user_bp
from src.services.authenticate import auth_bp

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    if test_config is None:
        app.config.from_mapping(
            FLASK_ENV = os.environ.get('FLASK_ENV'),
            FLASK_APP = os.environ.get('FLASK_APP'),
            SECRET_KEY = os.environ.get('SECRET_KEY'),
            FLASK_DEBUG = os.environ.get('FLASK_DEBUG'),
            JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY'),
            JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours= int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))),
            JWT_REFRESH_TOKEN_EXPIRES = timedelta(days= int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES')))
        )
    else:
        app.config.from_mapping(test_config)
        
    init_db()
    JWTManager(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    
    return app