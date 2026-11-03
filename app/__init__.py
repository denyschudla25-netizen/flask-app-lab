
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config["SECRET_KEY"] = "lab5-secret-key-change-later"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

csrf = CSRFProtect(app)

from app import views
from app.users.views import users_bp
from app.products.views import products_bp

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp)
