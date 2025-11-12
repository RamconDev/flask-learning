from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, DevelopmentConfig, TestingConfig

from app.register_blueprints import register_blueprints

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Simple Route GLOBAL
    # @app.route('/')
    # def index():
    #     return "Index page"
    
    # Blueprints
    register_blueprints(app)

    return app