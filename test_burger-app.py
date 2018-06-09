import unittest
import os
import json
from app import create_app, db

class BurgerAppTestCase(unittest.TestCase):
    """This class represents the burgerapp test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.burger = {'name', 'mc_gyver'}

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_burger_creation(self):
        """Test API can create a burger (POST request)"""
        res = self.client().post('/burgers/', data=self.burger)
        print("HAHAHAHA")
        self.assertEqual(res.status_code, 201)
        self.assertIn('mc_gyver', str(res.data))

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
