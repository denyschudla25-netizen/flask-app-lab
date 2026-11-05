from flask import Flask, render_template

from app.config import configurations
from app.extensions import db, migrate, csrf


def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(
        configurations.get(config_name, configurations["development"])
    )

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app import views
    from app.users.views import users_bp
    from app.products.views import products_bp
    from app.posts import post_bp
    from app.posts import models
    from app.posts import views as posts_views

    app.register_blueprint(views.app_bp)
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp)
    app.register_blueprint(post_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app