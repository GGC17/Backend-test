import json

from flask import Response
from flask_restful import Resource


# Just to check the API status
class Home(Resource):

    def get(self):
        """
        Endpoint to test if API is working fine
        """

        response = {
            "success": True,
            'message': 'Backend-Test Orders working fine'}
        return Response(json.dumps(response), status=200)