
from flask import render_template, request, redirect, url_for, make_response, flash
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


@app.route("/cookies", methods=["GET", "POST"])
def cookies():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            name = request.form.get("name", "").strip()
            value = request.form.get("value", "").strip()

            if not name or not value:
                flash("Введи назву та значення cookie", "warning")
                return redirect(url_for("cookies"))

            response = make_response(redirect(url_for("cookies")))
            response.set_cookie(name, value, max_age=7 * 24 * 60 * 60)
            return response

        if action == "delete":
            name = request.form.get("name", "").strip()

            if name:
                response = make_response(redirect(url_for("cookies")))
                response.delete_cookie(name)
                return response

    return render_template("cookies.html", cookies=request.cookies)
