import time
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def dump_datetime(value):
    """Deserialize datetime object into UNIX timestamp."""
    if value is None:
        return None
    return int(value.timestamp())


class BaseModel(db.Model):
    __abstract__ = True

    @staticmethod
    def serialize_multiple(resources):
        serialized = []
        for resource in resources:
            serialized.append(resource.serialize)

        return serialized


class Customers(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    address = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    meters = db.relationship('Meters')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'meters': Meters.serialize_multiple(self.meters),
        }


class Meters(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', onupdate='CASCADE', ondelete='CASCADE'))
    type = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    last_reading = db.relationship('MeterReadings')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'type': self.type,
            'last_reading': MeterReadings.serialize_multiple(self.last_reading)
        }


class MeterReadings(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    battery_percentage = db.Column(db.Integer)
    measured_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'meter_id': self.meter_id,
            'value': self.value,
            'battery_percentage': self.battery_percentage,
            'measured_at': dump_datetime(self.measured_at),
        }

    @classmethod
    def get_daily_total_readings(cls):
        result = db.session.execute('SELECT DISTINCT ON (mr.meter_id, mr.measured_at::date) '
                           'm.customer_id, m.id as meter_id, m.type, mr.value, mr.measured_at '
                           'FROM meter_readings mr '
                           'LEFT JOIN meters m ON m.id = mr.meter_id '
                           'ORDER BY mr.meter_id, mr.measured_at::date ASC, mr.measured_at DESC;')

        readings = []
        for row in result:
            readings.append(row)

        return readings

    @classmethod
    def get_daily_total_readings_for_customer(cls, customer_id):
        result = db.session.execute('SELECT DISTINCT ON (mr.meter_id, mr.measured_at::date) '
                                    'm.customer_id, m.id as meter_id, m.type, mr.value, mr.measured_at '
                                    'FROM meter_readings mr '
                                    'LEFT JOIN meters m ON m.id = mr.meter_id '
                                    'WHERE m.customer_id = %s '
                                    'ORDER BY mr.meter_id, mr.measured_at::date ASC, mr.measured_at DESC;' % (customer_id, ))

        readings = []
        for row in result:
            readings.append(row)

        return readings
