import os
import secrets

from flask import request, Response, g

API_KEY = os.getenv("API_KEY")
MOCK_USER_ID = os.getenv("MOCK_USER_ID")

def check_api_key() -> bool:
    key = request.headers.get('Authorization')
    if key:
        return secrets.compare_digest(key, API_KEY)
    return False

# Auth validation
def validAuth() -> dict | bool:
    """
    Function for authentication using a simple token (for simplicity)
    Should be replaced by JWT token or AWS Cognito service
    """

    # routes exempted from authentication
    exempt_routes = ["home"]
    if request.endpoint in exempt_routes:
        return
    
    # Check if api key is correct
    api_key = check_api_key()
    if api_key:
        g.user = MOCK_USER_ID
        return
    response = {"success": False,
                "message": "Invalid User Token."}
    return Response(response, 401)