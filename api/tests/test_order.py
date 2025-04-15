import json
import os
import unittest

from wsgi import app
from resources.order import OrderModel


API_KEY = os.getenv("API_KEY")


class test_order(unittest.TestCase):

    def setUp(self):
        """
        Creates a new flask instance for tests
        """

        self.client = app.test_client()
        self.order_obj = {"items": [{"product1": 10},
                                    {"product2": 2}]
                          }

    def test_create_order(self):

        # Create new order
        order_data = self.order_obj
        response = self.client.post('/orders',
                                    headers={"Authorization": API_KEY},
                                    json=order_data)
        self.assertEqual(response.status_code, 201)
        
        res_order = json.loads(response.get_data())
        
        self.assertTrue(res_order["success"])
        self.assertIn("id", res_order["message"])
        self.assertIn("userId", res_order["message"])
        self.assertIn("items", res_order["message"])
        self.assertIn("status", res_order["message"])
        self.assertIn("createdAt", res_order["message"])
        self.assertEqual(res_order["message"]["items"], [{"product1": 10},
                                                         {"product2": 2}])

        with app.app_context():
            delete_order_from_rds(res_order["message"]["id"])

    def test_create_order_bad_input(self):

        # Create new order with bad input
        order_data = {"items": "safaff"}
        response = self.client.post('/orders',
                                    headers={"Authorization": API_KEY},
                                    json=order_data)
        self.assertEqual(response.status_code, 400)

        res_order = json.loads(response.get_data())
        self.assertFalse(res_order["success"])
        self.assertEqual(res_order["message"],
                         "Input error")

    def test_list_all_orders(self):

        # Create new order
        order_data = self.order_obj
        response = self.client.post('/orders',
                                    headers={"Authorization": API_KEY},
                                    json=order_data)
        self.assertEqual(response.status_code, 201)
        order_id = json.loads(response.get_data())["message"]["id"]

        # Get list of orders for validation
        response = self.client.get("/orders",
                                   headers={"Authorization": API_KEY})
        self.assertEqual(response.status_code, 200)

        res_order = json.loads(response.get_data())
        self.assertTrue(res_order["success"])
        self.assertIsInstance(res_order["message"], list)
        
        with app.app_context():
            delete_order_from_rds(order_id)

    def test_get_order_by_id(self):

        # Create new order
        order_data = self.order_obj
        response = self.client.post('/orders',
                                    headers={"Authorization": API_KEY},
                                    json=order_data)
        self.assertEqual(response.status_code, 201)
        order_id = json.loads(response.get_data())["message"]["id"]

        # Get list of orders for validation
        response = self.client.get("/orders/{}".format(order_id),
                                   headers={"Authorization": API_KEY})
        self.assertEqual(response.status_code, 200)

        res_order = json.loads(response.get_data())
        
        self.assertTrue(res_order["success"])
        self.assertIn("id", res_order["message"])
        self.assertIn("userId", res_order["message"])
        self.assertIn("items", res_order["message"])
        self.assertIn("status", res_order["message"])
        self.assertIn("createdAt", res_order["message"])
        self.assertEqual(res_order["message"]["items"], [{"product1": 10},
                                                         {"product2": 2}])
        
        with app.app_context():
            delete_order_from_rds(order_id)
        
    def test_get_order_by_id_not_found(self):

        test_id = "79993c24-3fd8-4aad-9a3c-1fef530a1933"
        # Get order
        response = self.client.get("/orders/{}".format(test_id),
                                   headers={"Authorization": API_KEY})
        self.assertEqual(response.status_code, 404)

        res_order = json.loads(response.get_data())
        self.assertFalse(res_order["success"])
        self.assertEqual(res_order["message"],
                         "Order not found")
        
    def test_cancel_order_by_id(self):
        
        # Create new order
        order_data = self.order_obj
        response = self.client.post('/orders',
                                    headers={"Authorization": API_KEY},
                                    json=order_data)
        self.assertEqual(response.status_code, 201)
        order_id = json.loads(response.get_data())["message"]["id"]

        # Cancel order
        response = self.client.delete("/orders/{}".format(order_id),
                                      headers={"Authorization": API_KEY})
        self.assertEqual(response.status_code, 200)

        res_order = json.loads(response.get_data())
        self.assertTrue(res_order["success"])
        self.assertEqual(res_order["message"],
                         "Order Cancelled!")
        
        with app.app_context():
            delete_order_from_rds(order_id)
        
    def test_cancel_order_by_id_not_found(self):

        test_id = "79993c24-3fd8-4aad-9a3c-1fef530a1933"
        # Get order
        response = self.client.delete("/orders/{}".format(test_id),
                                      headers={"Authorization": API_KEY})
        self.assertEqual(response.status_code, 404)

        res_order = json.loads(response.get_data())
        self.assertFalse(res_order["success"])
        self.assertEqual(res_order["message"],
                         "Order not found")


def delete_order_from_rds(order_id):
    # Get order
    order_delete = OrderModel.find_by_id(order_id)
    # Delete entry from table
    order_delete.delete_from_db()