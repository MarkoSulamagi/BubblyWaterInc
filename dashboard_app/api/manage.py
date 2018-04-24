from flask import Flask
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from models.models import db, Customers

from config import get_database_url
from tests import PopulateDatabase


class SeedDatabase(Command):

    def run(self):
        print('Seeding database!')
        users, readings = PopulateDatabase.meter_readings_for_graphs()
        print('Database seeded (%s users and %s meter readings)' % (len(users), len(readings)))


class PurgeDatabase(Command):

    def run(self):
        print('Purging database!')
        with app.app_context():
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())
                db.session.commit()

        customer_count = Customers.query.count()
        if customer_count == 0:
            print('%s customers in database' % (str(customer_count), ))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('seed', SeedDatabase)
manager.add_command('purge', PurgeDatabase)


if __name__ == '__main__':
    manager.run()
