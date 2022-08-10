from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'theComiccave',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd26gaarfqkr6vv',
        'USER': 'qhqakrlmbkwaso',
        'PASSWORD': '4a0c8940f3fb932639d5dbd64b354ce2b09479538108cf300e8a31ef56bd1c17',
        'HOST': 'ec2-3-225-110-188.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))




