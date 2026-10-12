
from flask import Flask

app = Flask(__name__)

from app import views
from app.users.views import users_bp
from app.products.views import products_bp

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp, url_prefix="/products")
