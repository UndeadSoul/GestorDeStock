"""
Django settings for GestorDeStock project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import dj_database_url
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
#!SECRET_KEY = "2b3fc96558f385896227ca6a5ceea69c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG","False").lower() == "true"
#!DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split()
#!ALLOWED_HOSTS = ["localhost","127.0.0.1"]

IS_PRODUCTION = os.environ.get("DJANGO_ENV") == "production"

# Redirección HTTPS solo en producción
SECURE_SSL_REDIRECT = IS_PRODUCTION

# Configura CSRF solo para producción
CSRF_TRUSTED_ORIGINS = ["https://gestordestock.onrender.com"] if IS_PRODUCTION else []

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if IS_PRODUCTION else None

#Se establecen las direcciones url útiles para el login
LOGIN_URL = 'accounts/login/'
LOGIN_REDIRECT_URL = "custom_login_redirect"
LOGOUT_REDIRECT_URL = "login"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'login.apps.LoginConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'registerlogin.apps.RegisterloginConfig',
    'core',
    'crud',
    'cloudinary',
    'cloudinary_storage'

]

CRISPY_ALLOWED_TEMPLATE_PACKS="bootstrap5"
CRISPY_TEMPLATE_PACK="bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Debe estar aquí para servir archivos estáticos.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GestorDeStock.urls'

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

WSGI_APPLICATION = 'GestorDeStock.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}

#! DATABASES["default"]=dj_database_url.parse("postgresql://gestordestock_django_render_user:ehmMD0TzTeGTQKfuuEGIit48SSDTbT1e@dpg-ctfns2tds78s73ds7jk0-a.oregon-postgres.render.com/gestordestock_django_render")

database_url=os.environ.get("DATABASE_URL")
DATABASES["default"]=dj_database_url.parse(database_url) 

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'ddfknxf4e'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', "731293374554384"),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', 'uyrCSmro4jFtB5IXn1u0dcEMhto'),
}
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': 'ddfknxf4e',
#     'API_KEY': "731293374554384",
#     'API_SECRET': 'uyrCSmro4jFtB5IXn1u0dcEMhto',
# }

# Looking to send emails in production? Check out our Email API/SMTP product!
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'c986c7998ae9f6'
EMAIL_HOST_PASSWORD = '587a32959371ca'
EMAIL_PORT = '2525'

