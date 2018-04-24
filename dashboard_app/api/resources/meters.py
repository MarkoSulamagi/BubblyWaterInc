from flask import jsonify

from .base import Resource
from models import models


class MeterCount(Resource):

    def get(self, **kwargs):
        count = models.Meters.query.count()
        return jsonify({'count': count})
