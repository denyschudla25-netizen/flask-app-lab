import unittest

from app import create_app
from app.extensions import db
from app.posts.models import Post


class PostTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_post(self):
        with self.app.app_context():
            post = Post(
                title="Test Post",
                content="This is a test post.",
                category="news",
                author="Tester"
            )

            db.session.add(post)
            db.session.commit()

            return post.id

    def test_posts_page(self):
        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)

    def test_create_post_page(self):
        response = self.client.get("/post/create")
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        post_id = self.create_test_post()

        response = self.client.get(f"/post/{post_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Post", response.data)

    def test_post_not_found(self):
        response = self.client.get("/post/999")

        self.assertEqual(response.status_code, 404)

    def test_edit_post_page(self):
        post_id = self.create_test_post()

        response = self.client.get(f"/post/{post_id}/update")

        self.assertEqual(response.status_code, 200)

    def test_delete_confirmation(self):
        post_id = self.create_test_post()

        response = self.client.get(f"/post/{post_id}/delete")

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()