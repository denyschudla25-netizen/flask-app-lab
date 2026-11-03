
import uuid
from pathlib import Path
from datetime import datetime
from decimal import Decimal

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
)
from tinydb import TinyDB, Query
from werkzeug.utils import secure_filename

from app.forms import ProductForm


# Створення Blueprint
products_bp = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/products/static"
)


# Налаштування TinyDB
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "products.json"

db = TinyDB(DB_PATH, encoding="utf-8")
products_table = db.table("products")

ProductQuery = Query()


# Папка для фотографій
UPLOAD_FOLDER = Path(__file__).resolve().parent / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


# Перевірка формату фотографії
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Збереження фотографії
def save_image(file):
    if not file or not file.filename:
        return None

    if not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    extension = filename.rsplit(".", 1)[1].lower()

    new_filename = f"{uuid.uuid4().hex}.{extension}"

    file.save(UPLOAD_FOLDER / new_filename)

    return f"uploads/{new_filename}"


# Видалення фотографії
def delete_image(image_path):
    if not image_path:
        return

    full_path = Path(__file__).resolve().parent / "static" / image_path

    if full_path.exists():
        full_path.unlink()


# Генерація наступного ID
def get_next_id():
    products = products_table.all()

    if not products:
        return 1

    return max(product.get("id", 0) for product in products) + 1


# Отримання товару за ID
def get_product(product_id):
    return products_table.get(ProductQuery.id == product_id)


# ==========================================
# 1. СПИСОК ТОВАРІВ
# ==========================================

@products_bp.route("/product")
@products_bp.route("/products")
@products_bp.route("/products/", strict_slashes=False)
def products_list():
    all_products = products_table.all()

    return render_template(
        "products/products.html",
        title="Товари",
        products=all_products
    )


# ==========================================
# 2. ДОДАВАННЯ ТОВАРУ
# ==========================================

@products_bp.route("/product/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():

        uploaded_file = form.image.data

        if not uploaded_file or not uploaded_file.filename:
            flash("Додайте зображення товару.", "danger")

            return render_template(
                "products/add_product.html",
                title="Додавання товару",
                form=form
            )

        if not allowed_file(uploaded_file.filename):
            flash("Дозволені лише PNG, JPG та JPEG.", "danger")

            return render_template(
                "products/add_product.html",
                title="Додавання товару",
                form=form
            )

        image_path = save_image(uploaded_file)

        product = {
            "id": get_next_id(),
            "name": form.name.data,
            "content": form.content.data,
            "price": str(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        products_table.insert(product)

        flash("Товар успішно додано!", "success")

        return redirect(url_for("products.products_list"))

    return render_template(
        "products/add_product.html",
        title="Додавання товару",
        form=form
    )


# ==========================================
# 3. ДЕТАЛЬНА ІНФОРМАЦІЯ ПРО ТОВАР
# ==========================================

@products_bp.route("/product/<int:product_id>")
@products_bp.route("/products/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        title=product["name"],
        product=product
    )


# ==========================================
# 4. РЕДАГУВАННЯ ТОВАРУ
# ==========================================

@products_bp.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    product = get_product(product_id)

    if product is None:
        flash("Товар не знайдено.", "danger")
        return redirect(url_for("products.products_list"))

    form = ProductForm()

    # Заповнення форми поточними даними
    if request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = Decimal(product["price"])
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    if form.validate_on_submit():

        old_image = product.get("image")
        uploaded_file = form.image.data

        # Якщо користувач завантажив нове фото
        if uploaded_file and uploaded_file.filename:

            if not allowed_file(uploaded_file.filename):
                flash("Дозволені лише PNG, JPG та JPEG.", "danger")

                return render_template(
                    "products/edit_product.html",
                    title="Редагування товару",
                    form=form,
                    product=product
                )

            new_image = save_image(uploaded_file)

            if new_image:
                delete_image(old_image)
                old_image = new_image

        updated_product = {
            "id": product["id"],
            "name": form.name.data,
            "content": form.content.data,
            "price": str(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": old_image,
            "created_at": product["created_at"],
        }

        products_table.update(
            updated_product,
            ProductQuery.id == product_id
        )

        flash("Товар успішно оновлено!", "success")

        return redirect(
            url_for("products.product_detail", product_id=product_id)
        )

    return render_template(
        "products/edit_product.html",
        title="Редагування товару",
        form=form,
        product=product
    )


# ==========================================
# 5. ВИДАЛЕННЯ ТОВАРУ
# ==========================================

@products_bp.route("/product/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    product = get_product(product_id)

    if product is None:
        flash("Товар не знайдено.", "danger")
        return redirect(url_for("products.products_list"))

    # Видаляємо фотографію
    delete_image(product.get("image"))

    # Видаляємо товар із TinyDB
    products_table.remove(ProductQuery.id == product_id)

    flash("Товар успішно видалено!", "success")

    return redirect(url_for("products.products_list"))
