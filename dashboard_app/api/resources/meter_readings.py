from webargs import fields, validate, ValidationError
from webargs.flaskparser import use_kwargs

from flask import jsonify
from flask_restful import abort

from .base import Resource
from models import models


def validate_customer_in_db(val):
    if not models.Customers.query.get(val):
        raise ValidationError('Customer does not exist.')


def validate_dataset(val):
    if val != 'daily-total':
        raise ValidationError('Dataset does not exist.')


class MeterReadings(Resource):
    filter_args = {
        'dataset': fields.Str(required=True, validate=validate_dataset),
        'customer_id': fields.Str(required=False, validate=validate_customer_in_db)
    }

    @use_kwargs(filter_args)
    def get(self, **kwargs):
        dataset = kwargs.get('dataset', None)
        customer_id = kwargs.get('customer_id', None)

        readings = {}
        if dataset == 'daily-total':
            readings = self.get_daily_total_readings(customer_id)

        return jsonify(readings)

    def get_daily_total_readings(self, customer_id=None, period=7):
        """
        :param customer_id:
        :param period: Not implemented
        :return:
        """
        if customer_id:
            readings = models.MeterReadings.get_daily_total_readings_for_customer(customer_id=customer_id)
        else:
            readings = models.MeterReadings.get_daily_total_readings()

        return self.format_readings(readings)

    def format_readings(self, readings):
        formatted = {
            'HOT': {},
            'COLD': {}
        }

        previous_readings = {}
        for reading in readings:
            date = reading['measured_at'].strftime('%Y-%m-%d')
            if reading['meter_id'] in previous_readings:
                daily_consumption = reading['value'] - previous_readings[reading['meter_id']]

                if date not in formatted[reading['type']]:
                    formatted[reading['type']][date] = 0

                formatted[reading['type']][date] += daily_consumption

            previous_readings[reading['meter_id']] = reading['value']

        return formatted
