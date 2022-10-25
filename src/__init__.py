from flask import Flask
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    
    app.config['MONGODB_SETTINGS'] = {
    'host':"{}".format(os.getenv("MONGODB_SETTINGS")),
    }
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    from .database.db import initialize_db
    initialize_db(app)
    
    from .routes.movies import movie
    from .routes.auth import auth
    app.register_blueprint(movie)
    app.register_blueprint(auth)
    
    bcrypt = Bcrypt(app)
    
    jwt = JWTManager(app)

    return app