from flask import jsonify

from .base import Resource


class ApiEndpoints(Resource):

    def get(self, **kwargs):
        api_endpoints = [
            'GET /api',
            'GET /api/customers',
            'GET /api/customers/count',
            'GET /api/meters/count',
            'GET /api/customers/<int:customer_id>',
            'GET /api/meters/readings?dataset=daily-total&customer_id=123',
        ]

        return jsonify(api_endpoints)
