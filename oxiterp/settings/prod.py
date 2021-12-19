import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = True
ALLOWED_HOSTS = ['*']

""""'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'dfrdqvu734v8c',
       'USER': 'zdqozojtqxtaef',
       'PASSWORD': '616ad722cef96d815d78b1f0beb2c0cd5a4a596440c78644a827864ef88b6a93',
       'HOST': 'ec2-54-196-111-158.compute-1.amazonaws.com',
       'PORT': '5432',
   }"""

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oxit_career',
        'USER': 'postgres',
        'PASSWORD': 'oxit2016',
        'HOST': 'localhost',
        'PORT': '5432',
    },





}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aybukarmer@ybu.edu.tr'
EMAIL_HOST_PASSWORD = 'Kariyer2020'

STATIC_ROOT = "/var/www/static/service"

STAICFILES_DIR = [

    "/var/www/static/service"

]

WKHTMLTOPDF_CMD = '/usr/bin/wkhtmltopdf'
sentry_sdk.init(
    dsn="https://b0aae20b07294bd78547bab08d59b988@o1089299.ingest.sentry.io/6104283",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

try:
    from oxiterp.settings.local import *
except:
    pass
