import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from oxiterp.settings.base import *

# Override base.py settings here


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oxit_career',
        'USER': 'postgres',
        'PASSWORD': 'oxit2016',
        #'HOST': '185.122.203.207',
        'HOST': 'localhost',
        'PORT': '5432',
    }

}

GCM_APIKEY = "AAAAEgdR9KM:APA91bGJbWnT6MzzKIxRi9aAkfgyWCCRKxMNypBgpVjiM0ywTTU3xUyyK4_8Q3O8j-vVeY_k_genzinOnul2wDJKWQa3cnhuaHvG-3BVmdnjq3H1da1DHeKGjbF9ykimR-DlsC2ktnUw"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aybukarmer@ybu.edu.tr'
EMAIL_HOST_PASSWORD = 'Karmer2021.....'


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
