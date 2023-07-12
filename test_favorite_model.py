"""Favorite model tests."""

# run these tests like:
#
#python -m unittest test_favorite_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from app import app
from models import db, User, Favorite

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING']

os.environ['DATABASE_URL'] = "postgresql:///mealdb-test"


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class FavoriteModelTestCase(TestCase):
    """Test favorite model."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "password", None, None, None, None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_favorite_model(self):
        """Does basic model work?"""
        
        f = Favorite(
            user_id=self.uid,
            meal_id= "52772"
        )

        db.session.add(f)
        db.session.commit()

        # User should have 1 favorite
        self.assertEqual(len(self.u.favorites), 1)
        self.assertEqual(self.u.favorites[0].meal_id, 52772)

    