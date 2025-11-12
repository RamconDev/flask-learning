def register_blueprints(app):
    from app.main import main_bp
    app.register_blueprint(main_bp)