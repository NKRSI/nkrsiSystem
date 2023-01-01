import os

DEBUG_MODE = True
SECRET_KEY = 'secret'

# Database config
DB_USER = 'postgres'
DB_NAME = 'postgres'
DB_PASSWORD = ''
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Slack config
ROCKET_USERNAME = 'adminbot'
ROCKET_PASSWORD = ''
ROCKET_LOGIN_URL = ''
ROCKET_ADD_USER_URL = ''

# Email config
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

PROJECTOR_IP = ''
DOOR_ENDPOINT = ''

FACEBOOK_TOKEN = ''
GOOGLE_MAPS_API_KEY = ''
