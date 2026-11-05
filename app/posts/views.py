from datetime import datetime

from flask import render_template, redirect, url_for, flash, request, abort, session

from app.extensions import db
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm


@post_bp.route("/post")
def all_posts():
    posts = db.session.scalars(
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    ).all()

    return render_template("posts/posts.html", posts=posts)


@post_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.enabled.data,
            author=session.get("username", "Anonymous"),
            posted=form.publish_date.data or datetime.utcnow()
        )

        db.session.add(post)
        db.session.commit()

        flash("Пост успішно створено!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template(
        "posts/add_post.html",
        form=form,
        title="Створити пост"
    )


@post_bp.route("/post/<int:id>")
def detail_post(id):
    post = db.get_or_404(Post, id)

    if not post.is_active:
        abort(404)

    return render_template("posts/detail_post.html", post=post)


@post_bp.route("/post/<int:id>/update", methods=["GET", "POST"])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    if request.method == "GET":
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.enabled.data

        if form.publish_date.data:
            post.posted = form.publish_date.data

        db.session.commit()

        flash("Пост успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template(
        "posts/add_post.html",
        form=form,
        title="Редагувати пост"
    )


@post_bp.route("/post/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()

        flash("Пост успішно видалено!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template("posts/delete_confirm.html", post=post)