from flask import jsonify
from flask_restful import abort

from sqlalchemy.orm import joinedload

from .base import Resource
from models import models


class Customers(Resource):

    def get(self, **kwargs):
        query = models.Customers.query
        return jsonify([i.serialize for i in query.all()])


class CustomerCount(Resource):

    def get(self, **kwargs):
        count = models.Customers.query.count()
        return jsonify({'count': count})


class Customer(Resource):

    def get(self, customer_id, **kwargs):
        customer = models.Customers.query.options(joinedload('meters')).get(customer_id)

        if not customer:
            abort(404, error_code='resource_not_found')

        return jsonify(customer.serialize)
