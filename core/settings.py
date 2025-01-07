# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, environ
from datetime import timedelta

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# LOCAL_MEDIA_URL = '/media/'
LOCAL_MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'customer.Customer'

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
# DEBUG = False

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') 

# load production server from .env
ALLOWED_HOSTS        = ['localhost', 'localhost:85', '127.0.0.1',               env('SERVER', default='127.0.0.1') ]
CSRF_TRUSTED_ORIGINS = ['http://localhost:85', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1') ]

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.home',  # Enable the inner home (home)
    'customer',
    'products',
    'django_otp',
    'django_otp.plugins.otp_totp',  # Time-based One-Time Password
    'django_otp.plugins.otp_static',  # Static OTP for recovery
    'two_factor',
    'django.contrib.sites',  # Required for some views
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',  # Enable OTP middleware
]

# Configure login URLs
LOGIN_URL = 'two_factor:login'

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
                'django.template.context_processors.media',
                'customer.context_processors.categories_processor',
                'customer.context_processors.subscriber_form',
                'customer.context_processors.checkout_form'
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Change to DEBUG for more detailed output
            'propagate': True,
        },
        'your_custom_logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

WSGI_APPLICATION = 'core.wsgi.application'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Default
)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Enforce email verification
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  # Allow login via username or email
ACCOUNT_USERNAME_REQUIRED = False  # Disable username requirement
LOGIN_REDIRECT_URL = "/"  # Redirect after login
ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # Redirect after logout
DEFAULT_FROM_EMAIL = "oshadhakavinthajava@gmail.com"  # Sender email for verification

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "oshadhakavinthajava@gmail.com"
EMAIL_HOST_PASSWORD = "wwhb vurv oghs bxdy"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "mysql":
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.mysql', 
        'NAME'    : os.getenv('DB_NAME'     , 'appseed_db'),
        'USER'    : os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        'PASSWORD': os.getenv('DB_PASS'     , 'pass'),
        'HOST'    : os.getenv('DB_HOST'     , 'localhost'),
        'PORT'    : os.getenv('DB_PORT'     , 3306),
        }, 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

AWS_ACCESS_KEY_ID = 'AKIAYEKP5WKBTZQNKA4E'
AWS_SECRET_ACCESS_KEY = '8PM/Q3cRRQlNUh5BgazMmYoXG0j0VgDUd9333P0z'
AWS_STORAGE_BUCKET_NAME = 'django-app-experiment'
AWS_S3_REGION_NAME = 'eu-north-1'  # e.g., 'us-east-1'
AWS_QUERYSTRING_AUTH = True  # Ensures generated links are time-limited
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

PURCHASE_EXPIRATION_PERIOD = timedelta(days=2)

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'


