
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    make_response,
)

users_bp = Blueprint(
    "users",
    __name__,
    template_folder="templates"
)

VALID_USERNAME = "user1"
VALID_PASSWORD = "12345"


@users_bp.route("/hi/<name>")
def greetings(name):
    age = request.args.get("age", "не вказано")
    return render_template(
        "users/hi.html",
        title="Привітання",
        name=name,
        age=age
    )


@users_bp.route("/admin")
def admin():
    return redirect(
        url_for("users.greetings", name="Administrator", age=45)
    )


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Вхід успішний!", "success")
            return redirect(url_for("users.profile"))

        flash(
            "Неправильне ім'я користувача або пароль. Спробуйте ще раз.",
            "danger"
        )

    return render_template("users/login.html", title="Вхід")


@users_bp.route("/profile")
def profile():
    username = session.get("username")

    if not username:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("profile_theme", "light")

    if theme not in ("light", "dark"):
        theme = "light"

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=username,
        theme=theme
    )


@users_bp.route("/profile/theme", methods=["POST"])
def change_theme():
    if not session.get("username"):
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    theme = request.form.get("theme", "light")

    if theme not in ("light", "dark"):
        theme = "light"

    response = make_response(
        redirect(url_for("users.profile"))
    )

    response.set_cookie(
        "profile_theme",
        theme,
        max_age=30 * 24 * 60 * 60,
        httponly=True,
        samesite="Lax"
    )

    return response


@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))
