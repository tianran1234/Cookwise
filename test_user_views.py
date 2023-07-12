"""User view tests."""

# run these tests like:
#
# python -m unittest test_user_views.py


import os
from unittest import TestCase
from sqlalchemy import exc
from app import app, CURR_USER_KEY
from models import db, User, Favorite

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING']

os.environ['DATABASE_URL'] = "postgresql:///mealdb-test"


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None,
                                    header_image_url=None,
                                    location=None,
                                    bio=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        db.session.commit()

        self.u1 = User.signup("abc", "test1@test.com", "password", None, None, None, None)
        self.u1_id = 778
        self.u1.id = self.u1_id
        self.u2 = User.signup("efg", "test2@test.com", "password", None, None, None, None)
        self.u2_id = 884
        self.u2.id = self.u2_id
        self.u3 = User.signup("hij", "test3@test.com", "password", None, None, None, None)
        self.u4 = User.signup("testing", "test4@test.com", "password", None, None, None, None)

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_recipe_show(self):
        with self.client as c:
            resp = c.get(f"/recipes/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("testuser", str(resp.data))

    def setup_favorites(self):
        f1 = Favorite(meal_id="52770", user_id=self.testuser_id)
        f2 = Favorite(meal_id="52771", user_id=self.testuser_id)
        f3 = Favorite(id=9876, meal_id="52772", user_id=self.u1_id)
        db.session.add_all([f1, f2, f3])
        db.session.commit()

    def test_user_show_with_favorites(self):
        self.setup_favorites()

        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("testuser", str(resp.data))
    



