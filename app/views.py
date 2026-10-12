
from flask import render_template
from app import app


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")
