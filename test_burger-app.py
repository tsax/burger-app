from flask import jsonify
import unittest
import os
import json
from app import create_app, db
from app.models import Burger, Topping

class BurgerAppTestCase(unittest.TestCase):
    """This class represents the burgerapp test case"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.burger = {'name': 'mc_gyver'}
        self.burger_with_toppings = {"name": "awesome3_brgr", "has_bun": "false", "toppings": ["lettuce", "pickled_onions"]}

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

    # def test_api_can_get_burger_by_topping(self):
    #     with self.app.app_context():
    #         Topping(name='picked_onions').save()
    #         Topping(name='swiss_chard').save()

    #     rv = self.client().post('/burgers/', data=self.burger_with_toppings)
    #     self.assertEqual(rv.status_code, 201)

    #     result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
    #     result = self.client().get(
    #         '/burgers/{}'.format(result_in_json['id']))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('mc_gyver', str(result.data))

    def test_burger_can_be_edited(self):
        rv = self.client().post('/burgers/', data=self.burger)
        self.assertEqual(rv.status_code, 201)

        rv = self.client().put('/burgers/1', data={
                        'name': 'shake_shack'
                        })
        self.assertEqual(rv.status_code, 200)

        with self.app.app_context():
            burger = Burger.query.filter_by(name='shake_shack').first()
            self.assertEqual('shake_shack', burger.name)

    def test_burger_deletion(self):
        rv = self.client().post(
            '/burgers/',
            data={'name': 'shake_shack'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/burgers/1')
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
