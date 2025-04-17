import json
import uuid

from flask import Response, g
from flask_restful import Resource, request
from models.order import OrderModel


class Order(Resource):

    def post(self):

        """
        Endpoint to create a new order.

        :param items: array of {productId, quantity}
            {"items": [{"productID1": quantity}, {"productID2": quantity}]}
        :returns: Flask response
        """
    
        # Get message body
        order_data = json.loads(request.get_data())

        # Input validation
        if 'items' not in order_data or not isinstance(order_data["items"], list) or \
            not all(isinstance(item, dict) for item in order_data["items"]):
            response = {"success": False,
                        "message": "Input error"}
            return Response(json.dumps(response), 400)
        # Add order to database
        order = OrderModel(userId=g.user,
                           items=order_data["items"])
        order.save_to_db()

        response = {"success": True,
                    "message": order.json()}
        return Response(json.dumps(response), 201)

    def get(self):

        """
        Endpoint to list all orders.
        ***Should filter by user's orders
        Admin can view all orders
        ***

        :returns: Flask response
        """
        # Query for all orders
        orders = OrderModel.find_all()

        response = {"success": True,
                    "message": [order.json() for order in orders]}

        return Response(json.dumps(response),
                        200)


class OrderById(Resource):
    def get(self, id):

        """
        Endpoint to get order by id.
        ***Should filter by user's order
        Admin can view any order by id
        ***

        :returns: Flask response
        """
        # Validate if id is uuid
        try:
            uuid.UUID(str(id))
        except ValueError:
            response = {"success": False,
                        "message": "Id not of type uuid"}
            return Response(json.dumps(response), 400)

        # Query for order by id
        order = OrderModel.find_by_id(id)

        # Handle order not found
        if not order:
            response = {"success": False,
                        "message": "Order not found"}
            return Response(json.dumps(response), 404)

        response = {"success": True,
                    "message": order.json()}

        return Response(json.dumps(response),
                        200)
            
    def delete(self, id):
        """
        Endpoint to cancel an order by id.

        :returns: Flask response
        """
        # Validate if id is uuid
        try:
            uuid.UUID(str(id))
        except ValueError:
            response = {"success": False,
                        "message": "Id not of type uuid"}
            return Response(json.dumps(response), 400)

        # Query for order by id
        order = OrderModel.find_by_id(id)

        # Handle order not found
        if not order:
            response = {"success": False,
                        "message": "Order not found"}
            return Response(json.dumps(response), 404)
        # Handle order already canceled
        elif order.status != "Created":
            response = {"success": False,
                        "message": "Order already processed"}
            return Response(json.dumps(response), 400)

        # Change status in db
        order.status = "Cancelled"
        order.save_to_db()

        response = {"success": True,
                    "message": "Order Cancelled!"}

        return Response(json.dumps(response),
                        200)
