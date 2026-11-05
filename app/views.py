from flask import Blueprint, render_template

app_bp = Blueprint("main", __name__)


@app_bp.route("/")
def home():
    return render_template("homepage.html")


@app_bp.route("/resume")
def resume():
    return render_template("resume.html")


@app_bp.route("/contacts")
def contacts():
    return render_template("contacts.html")