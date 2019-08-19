import os

MONGO_URI = os.getenv('MONGO_URI')
PAGINATION = False
HATEOAS = False
DEBUG = True

DOMAIN = {
    'features': {
        'schema': {
            'name': {
                'type': 'string'
            },
            'feat': {
                'type': 'string'
            },
        },
        'resource_methods': ['GET', 'POST', 'DELETE'],
    }
}

