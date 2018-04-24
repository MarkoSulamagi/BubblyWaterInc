from smart_getenv import getenv

config = {
    'debug': getenv('DEBUG', type=bool, default=False),

    'postgresql': {
        'host': getenv('POSTGRES_HOST', default='postgres'),
        'db': getenv('POSTGRES_DB', default='bubblywater'),
        'username': getenv('POSTGRES_USERNAME', default='bubblywater'),
        'password': getenv('POSTGRES_PASSWORD', default='As1234'),
    }
}


def get_database_url():
    return 'postgresql://' + config['postgresql']['username'] + ':' + config['postgresql']['password'] + '@' + \
           config['postgresql']['host'] + '/' + config['postgresql']['db']


def get_test_database_url():
    return 'postgresql://' + config['postgresql']['username'] + ':' + config['postgresql']['password'] + '@' + \
           config['postgresql']['host'] + '/tests'


def debug():
    return config['debug']
