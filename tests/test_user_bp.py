
import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

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
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"PC", response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
