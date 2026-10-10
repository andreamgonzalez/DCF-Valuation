import os
from unittest import TestCase

# has to be set before app is imported, the database connection is set up on import
os.environ['DATABASE_URL'] = 'postgresql:///valuation_test'

from app import app
from models import db

with app.app_context():
    db.drop_all()
    db.create_all()


class AppTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_homepage(self):
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 200)