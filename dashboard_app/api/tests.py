from datetime import datetime, timedelta
from random import randint, choice

import requests
from flask import Flask
from flask_restful import Api, abort
from flask_testing import LiveServerTestCase
from resources.customers import Customers, Customer, CustomerCount
from resources.meters import MeterCount
from resources.meter_readings import MeterReadings
from faker import Faker
from sqlalchemy.orm import joinedload, contains_eager
from webargs.flaskparser import parser

from config import get_test_database_url
from models.models import db
from models import models


class BaseTestCase(LiveServerTestCase):
    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_test_database_url()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        self.app.config['TESTING'] = True
        db.init_app(self.app)

        # TODO: Should be moved to Blueprint to make it testable
        api = Api(self.app)
        api.add_resource(Customers, '/api/customers')
        api.add_resource(CustomerCount, '/api/customers/count')
        api.add_resource(Customer, '/api/customers/<int:customer_id>')
        api.add_resource(MeterCount, '/api/meters/count')
        api.add_resource(MeterReadings, '/api/meters/readings')

        @parser.error_handler
        def handle_request_parsing_error(err):
            abort(422, error_code='validation_error', message=err.messages)

        return self.app

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        Truncate instead of drop to increase speed of running tests
        """
        self.truncate_all_tables()

    def truncate_all_tables(self):
        with self.app.app_context():
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())
                db.session.commit()

    def get_endpoint_url(self, endpoint=None):
        url = self.get_server_url()
        if endpoint:
            url += endpoint
        return url


class PopulateDatabase(object):
    @staticmethod
    def single_customer_no_meters():
        faker = Faker()
        customer = models.Customers(first_name=faker.first_name(), last_name=faker.last_name(), address=faker.address(),
                                    created_at=faker.past_datetime(), updated_at=faker.past_datetime())
        db.session.add(customer)
        db.session.commit()

        return customer

    @staticmethod
    def multiple_customers_with_meters_and_readings(count=5, populate_meters=True, populate_readings=True):
        faker = Faker()
        customers = []
        for i in range(0, count):
            customer = models.Customers(first_name=faker.first_name(), last_name=faker.last_name(),
                                        address=faker.address(), created_at=faker.past_datetime(),
                                        updated_at=faker.past_datetime())
            db.session.add(customer)
            db.session.flush()

            if populate_meters:
                PopulateDatabase.populate_meters_for_customer(customer, populate_readings)

            eager_loaded = db.session.query(models.Customers) \
                .options(joinedload('meters').joinedload('last_reading')) \
                .filter_by(id=customer.id).first()
            customers.append(eager_loaded)

        db.session.commit()

        return customers

    @staticmethod
    def meter_readings_for_graphs():
        """
        Generates a ton of data so it would be possible to test graph queries.
        Not using the data on other tests, because takes a while to insert and tests would be slow
        """
        faker = Faker()
        faked_customers_w_meters = PopulateDatabase.multiple_customers_with_meters_and_readings(5, populate_meters=True,
                                                                                                populate_readings=False)

        meter_readings = []
        for customer_idx, customer in enumerate(faked_customers_w_meters):
            for meter_idx, meter in enumerate(customer.meters):
                reading_value = randint(0, 100)
                battery_percentage = randint(80, 100)
                measured_at = datetime.now() - timedelta(days=30)

                for day in range(0, 1000):
                    reading = models.MeterReadings(meter_id=meter.id, value=reading_value,
                                                   battery_percentage=battery_percentage, measured_at=measured_at,
                                                   created_at=faker.past_datetime(), updated_at=faker.past_datetime())

                    db.session.add(reading)
                    meter_readings.append(reading)

                    reading_value += randint(0, 5)
                    battery_percentage -= randint(0, 3)
                    if battery_percentage <= 0:
                        battery_percentage = 0
                    measured_at = measured_at + timedelta(minutes=10)

                db.session.commit()

        return faked_customers_w_meters, meter_readings


    @staticmethod
    def populate_meters_for_customer(customer, populate_readings=True):
        faker = Faker()

        for j in range(0, randint(1, 2)):
            meter = models.Meters(customer_id=customer.id, type=choice(['COLD', 'HOT']),
                                  created_at=faker.past_datetime(), updated_at=faker.past_datetime())
            db.session.add(meter)
            db.session.flush()

            if populate_readings:
                PopulateDatabase.populate_readings_for_meter(meter)

    @staticmethod
    def populate_readings_for_meter(meter):
        faker = Faker()

        last_reading = randint(0, 100)
        last_battery_percentage = randint(0, 100)
        last_measured_at = faker.past_datetime()
        for k in range(0, randint(0, 30)):
            reading = models.MeterReadings(meter_id=meter.id, value=last_reading,
                                           battery_percentage=last_battery_percentage, measured_at=last_measured_at,
                                           created_at=faker.past_datetime(), updated_at=faker.past_datetime())
            db.session.add(reading)

            last_reading = randint(last_reading, 1000)
            last_battery_percentage = randint(0, last_battery_percentage)
            last_measured_at = faker.date_time_between_dates(last_measured_at, datetime.now())


class GeneralApiTests(BaseTestCase):
    def test_server_is_up_and_running(self):
        response = requests.get(self.get_endpoint_url())
        self.assertEqual(response.status_code, 404)


class CustomersEndpointTests(BaseTestCase):
    def test_get_all_customers_no_results(self):
        response = requests.get(self.get_endpoint_url('/api/customers'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_all_customers_has_single_result(self):
        faked = PopulateDatabase.single_customer_no_meters()

        response = requests.get(self.get_endpoint_url('/api/customers'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [faked.serialize])

    def test_get_all_customers_has_multiple_results(self):
        faked = PopulateDatabase.multiple_customers_with_meters_and_readings()

        response = requests.get(self.get_endpoint_url('/api/customers'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(faked))

    def test_get_all_customer_count(self):
        faked = PopulateDatabase.multiple_customers_with_meters_and_readings(10)

        response = requests.get(self.get_endpoint_url('/api/customers/count'))
        self.assertEqual(response.status_code, 200)
        response_obj = response.json()
        self.assertEqual(response_obj['count'], 10)

    def test_get_all_customer_count_no_customers(self):
        faked = PopulateDatabase.multiple_customers_with_meters_and_readings(0)

        response = requests.get(self.get_endpoint_url('/api/customers/count'))
        self.assertEqual(response.status_code, 200)
        response_obj = response.json()
        self.assertEqual(response_obj['count'], 0)


class SingleCustomerEndpointTests(BaseTestCase):
    def test_customer_doesnt_exist(self):
        response = requests.get(self.get_endpoint_url('/api/customers/9999'))
        self.assertEqual(response.status_code, 404)

        response_obj = response.json()
        self.assertEqual(response_obj['error_code'], 'resource_not_found')

    def test_customer_exists(self):
        faked = PopulateDatabase.multiple_customers_with_meters_and_readings()

        response = requests.get(self.get_endpoint_url('/api/customers/' + str(faked[0].id)))
        self.assertEqual(response.status_code, 200)

        response_obj = response.json()
        self.assertEqual(len(faked[0].meters), len(response_obj['meters']))


class MetersEndpointTests(BaseTestCase):
    def test_get_all_meters_count_no_meters(self):
        response = requests.get(self.get_endpoint_url('/api/meters/count'))
        self.assertEqual(response.status_code, 200)
        response_obj = response.json()
        self.assertEqual(response_obj['count'], 0)

    def test_get_all_meters_count(self):
        faked = PopulateDatabase.multiple_customers_with_meters_and_readings(10)
        faked_meter_count = 0
        for customer in faked:
            faked_meter_count += len(customer.meters)

        response = requests.get(self.get_endpoint_url('/api/meters/count'))
        self.assertEqual(response.status_code, 200)
        response_obj = response.json()
        self.assertEqual(response_obj['count'], faked_meter_count)


class MeterReadingsEndpointTests(BaseTestCase):
    """
    This needs way more testing on real-world products.
    It's quite complicated feature and has a lot of exceptions. I'll leave some
    testing out to reduce scope of the test assignment.
    """

    def test_get_readings_no_dataset(self):
        response = requests.get(self.get_endpoint_url('/api/meters/readings'))
        self.assertEqual(response.status_code, 422)
        response_obj = response.json()
        self.assertEqual(response_obj['error_code'], 'validation_error')

    def test_get_readings_incorrect__dataset(self):
        response = requests.get(self.get_endpoint_url('/api/meters/readings?dataset=dataset-does-not-exist'))
        self.assertEqual(response.status_code, 422)
        response_obj = response.json()
        self.assertEqual(response_obj['error_code'], 'validation_error')

    def test_get_daily_total_readings_no_results(self):
        response = requests.get(self.get_endpoint_url('/api/meters/readings?dataset=daily-total'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'COLD': {}, 'HOT': {}})

    def test_get_daily_total_readings_incorrect_customer_id(self):
        response = requests.get(self.get_endpoint_url('/api/meters/readings?dataset=daily-total&customer_id=123'))
        self.assertEqual(response.status_code, 422)
        response_obj = response.json()
        self.assertEqual(response_obj['error_code'], 'validation_error')

    def test_get_daily_total_for_all_customers(self):
        """
        This needs way more testing on real-world products
        """
        faked_customers, meter_readings = PopulateDatabase.meter_readings_for_graphs()
        response = requests.get(self.get_endpoint_url('/api/meters/readings?dataset=daily-total'))
        self.assertEqual(response.status_code, 200)

    def test_get_daily_total_for_single_customer(self):
        """
        This needs way more testing on real-world products
        """
        faked_customers, meter_readings = PopulateDatabase.meter_readings_for_graphs()
        response = requests.get(
            self.get_endpoint_url('/api/meters/readings?dataset=daily-total&customer_id=' + str(faked_customers[0].id)))

        self.assertEqual(response.status_code, 200)
