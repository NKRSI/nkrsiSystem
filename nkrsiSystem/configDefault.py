import os

DEBUG_MODE = True
SECRET_KEY = 'secret'

# Database config
DB_USER = 'postgres'
DB_NAME = 'postgres'
DB_PASSWORD = ''
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Email config
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

PROJECTOR_IP = ''
DOOR_ENDPOINT = ''

FACEBOOK_TOKEN = ''
GOOGLE_MAPS_API_KEY = ''

# Servers
GPU_SERVERS = [('plaster', '192.168.0.180'), ('walter', '192.168.0.200')]

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_PASSWORD = ''
CELERY_BROKER_URL = "redis://" + ':' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_RESULT_BACKEND = "redis://" + ':' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + REDIS_PORT + '/1'

