import logging
import os

from db import db
from flask import Flask
from flask_restful import Api
from resources.home import Home
from resources.order import Order, OrderById
from utils.valid_auth import validAuth


RDS_USER = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_HOST = os.getenv("RDS_HOST")
RDS_PORT = os.getenv("RDS_PORT")


# Instantiate Flask and rds conn
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "postgresql://{}:{}@{}:{}/".format(RDS_USER,
                                       RDS_PASSWORD,
                                       RDS_HOST,
                                       RDS_PORT)
api = Api(app)
db.init_app(app)

# Create rds postgres tables
with app.app_context():
    try:
        db.create_all()
    except Exception:
        print("Skipping, tables already created")

# Home
app.before_request(validAuth)
api.add_resource(Home, "/")

# Orders Endpoints
api.add_resource(Order, "/orders")
api.add_resource(OrderById, "/orders/<string:id>")


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
