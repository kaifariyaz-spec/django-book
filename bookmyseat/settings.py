import os
from pathlib import Path
import dj_database_url

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-test-key-change-this'
DEBUG = True

ALLOWED_HOSTS = [
    'django-book-r45u.onrender.com',
    ]


# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # your app
    'users.apps.UsersConfig',
    'movies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
AUTH_USER_MODEL = 'auth.User'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_URL = 'static/'

STATICFILES_DIRS =[
    os.path.join(BASE_DIR,'static')
]

MEDIA_URL = '/media_movies/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_movies')

ROOT_URLCONF = 'bookmyseat.urls'
LOGIN_URL ='/login/'
LOGIN_REDIRECT_URL ='/profile/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # do NOT add anything here
        'APP_DIRS': True,  # this loads templates inside each app
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

WSGI_APPLICATION = 'bookmyseat.wsgi.application'


# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES['default'] = dj_database_url.parse('postgresql://django_bookmyshow_qjz6_user:GwkcbUD6mmDW0C9gkanlSLF0ZNWBvrpS@dpg-d5idcgp5pdvs73bv5j00-a.oregon-postgres.render.com/django_bookmyshow_qjz6')


# PASSWORD VALIDATION

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


# LANGUAGE & TIMEZONE
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
