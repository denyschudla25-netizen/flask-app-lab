
import unittest
import tempfile
from pathlib import Path

from tinydb import TinyDB

from app import create_app
from app.products import views as products_views


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app.config["TESTING"] = True

        self.client = self.app.test_client()

        # Створюємо окрему тимчасову базу для тестів
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.test_db = TinyDB(
            Path(self.temp_dir.name) / "products.json",
            encoding="utf-8"
        )
        self.addCleanup(self.test_db.close)

        # Підміняємо таблицю товарів на тестову
        products_views.products_table = self.test_db.table("products")

        # Додаємо ASUS
        products_views.products_table.insert({
            "id": 1,
            "name": "ASUS TUF Gaming F15",
            "content": "Ігровий ноутбук ASUS",
            "price": "32999.99",
            "category": "electronics",
            "quantity": 5,
            "image": "",
            "created_at": "2026-11-03 20:52:34"
        })

        # Додаємо Logitech
        products_views.products_table.insert({
            "id": 2,
            "name": "Logitech G102",
            "content": "Ігрова миша Logitech",
            "price": "899.99",
            "category": "electronics",
            "quantity": 10,
            "image": "",
            "created_at": "2026-11-03 20:52:34"
        })

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data.upper())
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        response = self.client.get(
            "/users/admin",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data.upper())
        self.assertIn(b"45", response.data)

    def test_products_page(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ASUS TUF Gaming F15", response.data)
        self.assertIn(b"Logitech G102", response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ASUS TUF Gaming F15", response.data)
        self.assertIn(b"32999", response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
