
import unittest
import tempfile
from pathlib import Path
from io import BytesIO
from decimal import Decimal

from tinydb import TinyDB

from app import app
from app.products import views as products_views


class ProductTests(unittest.TestCase):

    def setUp(self):
        # Налаштування тестового Flask-застосунку
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.client = app.test_client()

        # Створення тимчасової бази даних
        self.temp_dir = tempfile.TemporaryDirectory()

        self.db = TinyDB(
            Path(self.temp_dir.name) / "test_products.json"
        )

        # Зберігаємо оригінальну таблицю
        self.original_table = products_views.products_table

        # Підключаємо тестову таблицю
        products_views.products_table = self.db.table("products")

    def tearDown(self):
        # Відновлюємо оригінальну таблицю
        products_views.products_table = self.original_table

        self.db.close()
        self.temp_dir.cleanup()

    # Допоміжний метод для створення товару
    def add_test_product(self):

        data = {
            "name": "Logitech G102",
            "content": "Ігрова мишка з RGB-підсвічуванням.",
            "price": "799.50",
            "category": "electronics",
            "quantity": "12",
            "image": (
                BytesIO(b"fake image content"),
                "mouse.jpg"
            ),
            "submit": "Зберегти товар"
        }

        response = self.client.post(
            "/product/add",
            data=data,
            content_type="multipart/form-data"
        )

        return response

    # Тест 1. Додавання товару
    def test_add_product(self):

        response = self.add_test_product()

        self.assertEqual(response.status_code, 302)

        products = products_views.products_table.all()

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Logitech G102")
        self.assertEqual(products[0]["price"], "799.50")
        self.assertEqual(products[0]["category"], "electronics")
        self.assertEqual(products[0]["quantity"], 12)
        self.assertTrue(products[0]["image"].startswith("uploads/"))

    # Тест 2. Перегляд списку товарів
    def test_products_list(self):

        self.add_test_product()

        response = self.client.get("/product")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logitech G102", response.data)

    # Тест 3. Перегляд детальної інформації
    def test_product_detail(self):

        self.add_test_product()

        response = self.client.get("/product/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logitech G102", response.data)

    # Тест 4. Редагування товару
    def test_edit_product(self):

        self.add_test_product()

        data = {
            "name": "Logitech G102 Updated",
            "content": "Оновлена ігрова мишка з RGB.",
            "price": "999.99",
            "category": "electronics",
            "quantity": "20",
        }

        response = self.client.post(
            "/product/1/edit",
            data=data
        )

        self.assertEqual(response.status_code, 302)

        product = products_views.products_table.get(
            products_views.ProductQuery.id == 1
        )

        self.assertEqual(
            product["name"],
            "Logitech G102 Updated"
        )

        self.assertEqual(product["price"], "999.99")
        self.assertEqual(product["quantity"], 20)

        # Перевірка, що дата створення не змінилася
        self.assertTrue(product["created_at"])

    # Тест 5. Видалення товару
    def test_delete_product(self):

        self.add_test_product()

        response = self.client.post("/product/1/delete")

        self.assertEqual(response.status_code, 302)

        products = products_views.products_table.all()

        self.assertEqual(len(products), 0)

    # Тест 6. Перевірка неіснуючого товару
def test_product_not_found(self):

    response = self.client.get("/product/999")

    self.assertEqual(response.status_code, 404)
    self.assertIn(b"not found", response.data.lower())


if __name__ == "__main__":
    unittest.main()
