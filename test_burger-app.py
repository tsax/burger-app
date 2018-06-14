import unittest
import os
import json
from app import create_app, db
from app.models import Burger

class BurgerAppTestCase(unittest.TestCase):
    """This class represents the burgerapp test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.burger = {'name': 'mc_gyver'}

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_burger_creation(self):
        res = self.client().post('/burgers/', data=self.burger)
        self.assertEqual(res.status_code, 201)
        self.assertIn('mc_gyver', str(res.data))

    def test_api_can_get_all_burgers(self):
        with self.app.app_context():
            Burger(name=self.burger['name']).save()
        res = self.client().get('/burgers/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('mc_gyver', str(res.data))

    def test_api_can_get_burger_by_id(self):
        """Test API can get a single burger by using its id"""
        rv = self.client().post('/burgers/', data=self.burger)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/burgers/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('mc_gyver', str(result.data))

    def test_burger_can_be_edited(self):
        """Test API can edit an existing burger. (PUT request)"""
        rv = self.client().post(
            '/burgers/',
            data={'name': 'mc_gyver'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/burgers/1',
            data={
                'name': 'shake_shack'
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/burgers/1')
        self.assertIn('shake_shack', str(results.data))

    def test_burger_deletion(self):
        """Test API can delete an existing burger. (DELETE request)."""
        rv = self.client().post(
            '/burgers/',
            data={'name': 'shake_shack'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/burgers/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/burgers/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
