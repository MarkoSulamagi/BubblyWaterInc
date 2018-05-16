from flask import Flask
from flask_restful import Api, abort
from webargs.flaskparser import parser
from flask_cors import CORS, cross_origin

from config import debug, get_database_url

from models.models import db
from resources.customers import Customers, Customer, CustomerCount
from resources.meters import MeterCount
from resources.meter_readings import MeterReadings

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

db.init_app(app)

# TODO: Should be moved to Blueprint to make it testable
api.add_resource(Customers, '/api/customers')
api.add_resource(CustomerCount, '/api/customers/count')
api.add_resource(MeterCount, '/api/meters/count')
api.add_resource(Customer, '/api/customers/<int:customer_id>')
api.add_resource(MeterReadings, '/api/meters/readings')


@parser.error_handler
def handle_request_parsing_error(err):
    abort(422, error_code='validation_error', message=err.messages)


if __name__ == '__main__':
    app.run(debug=debug())
