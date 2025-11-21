def register_blueprints(app):
    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.posts import posts_bp
    app.register_blueprint(posts_bp)