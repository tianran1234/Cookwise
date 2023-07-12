"""Favorite view tests."""

# run these tests like:
#
# python -m unittest test_favorite_views.py


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


class FavoriteViewTestCase(TestCase):
    """Test views for favorites."""

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

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_add_favorite(self):
        """Can user add a favorite?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/8989/52772/favorite", data={"meal_id": "52772", "user_id": "8989"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            favorite = Favorite.query.one()
            self.assertEqual(favorite.meal_id, 52772)

    def test_add_no_session(self):
        with self.client as c:
            resp = c.post("/users/8989/52772/favorite", data={"meal_id": "52772", "user_id": "8989"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))
    
    def test_favorites_show(self):

        f = Favorite(
            id=1234,
            meal_id="52772",
            user_id=self.testuser_id
        )
        
        db.session.add(f)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            f = Favorite.query.get(1234)

            resp = c.get(f'/users/8989/favorites')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(str(f.meal_id), str(resp.data))

    def test_delete_favorite(self):

        f = Favorite(
            id=1234,
            meal_id="52772",
            user_id=self.testuser_id
        )
        db.session.add(f)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/8989/52772/unfavorite", follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            f = Favorite.query.get(1234)
            self.assertIsNone(f)

    def test_favorite_delete_no_session(self):

        f = Favorite(
            id=1234,
            meal_id="52772",
            user_id=self.testuser_id
        )
        db.session.add(f)
        db.session.commit()

        with self.client as c:
            resp = c.post("/users/8989/52772/unfavorite", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

            f = Favorite.query.get(1234)
            self.assertIsNotNone(f)
