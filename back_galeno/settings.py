from pathlib import Path
import os

import dj_database_url

from decouple import config




BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config('SECRET_KEY')


DEBUG = True

ALLOWED_HOSTS = ['*']



THIRDY_APPS=[
    'rest_framework',
    'corsheaders',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'applications.api',
    
] + THIRDY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'back_galeno.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'back_galeno.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'galenos',
        'USER': 'postgres',
        'PASSWORD': '41060109',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = '/static/'


MEDIA_URL='/media/'


STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')

MEDIA_ROOT=os.path.join(BASE_DIR,'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS=True


# CORS_ALLOWED_ORIGINS = [
 
#     "http://localhost:8080",
#     "http://127.0.0.1:8000",
# ]

STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'


db_from_env=dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

