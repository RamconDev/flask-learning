import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from app.register_blueprints import register_blueprints

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Simple Route GLOBAL
    # @app.route('/')
    # def index():
    #     return "Index page"
    
    # Blueprints
    register_blueprints(app)

    return app