
import logging

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    flash,
)

from app import app
from app.forms import ContactForm


# Налаштування журналу контактних повідомлень
logging.basicConfig(
    filename="contact.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)


# Головна сторінка
@app.route("/")
def home():
    return render_template("homepage.html")


# Резюме
@app.route("/resume")
def resume():
    return render_template("resume.html")


# Контакти
@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


# Робота з Cookies
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
            response.set_cookie(
                name,
                value,
                max_age=7 * 24 * 60 * 60
            )
            return response

        if action == "delete":
            name = request.form.get("name", "").strip()

            if name:
                response = make_response(redirect(url_for("cookies")))
                response.delete_cookie(name)
                return response

    return render_template(
        "cookies.html",
        cookies=request.cookies
    )


# Контактна форма лабораторної №5
@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():

        logging.info(
            "Ім'я: %s | Email: %s | Тема: %s | Повідомлення: %s",
            form.name.data,
            form.email.data,
            form.subject.data,
            form.message.data
        )

        flash(
            "Ваше повідомлення успішно надіслано!",
            "success"
        )

        return redirect(url_for("contact"))

    return render_template(
        "contact.html",
        title="Контактна форма",
        form=form
    )
