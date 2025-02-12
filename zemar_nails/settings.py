from pathlib import Path
from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured
import environ
import certifi
import pymysql
pymysql.install_as_MySQLdb()
import ssl
import os

BASE_DIR = Path(__file__).resolve().parent.parent

if 'DEBUG' in os.environ:
    del os.environ['DEBUG']

ssl_context = ssl.create_default_context(cafile=certifi.where())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize django environ
env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Security key
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False) 
print(DEBUG)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# App definitions
INSTALLED_APPS = [
    'admin_interface', 
    'colorfield', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Configured apps
    'core',
    'accounts',
    'appointments',
    'services',
    'reviews',
    'reports',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zemar_nails.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core/templates', 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.mensaje_especial_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'zemar_nails.wsgi.application'

# DB config
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),  
        'NAME': env('DB_NAME'),  
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),  
        'HOST': env('DB_HOST'), 
        'PORT': env('DB_PORT'), 
        'OPTIONS': {
            'charset': 'utf8mb4',  
        },
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

# Language config
LANGUAGE_CODE = 'es'

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Español'),
]

TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Url redirection
LOGIN_URL = 'login'
LOGOUT_URL= "/"

# Cookie session config
SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
SESSION_COOKIE_NAME = 'sessionid'


# Error logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # Handler para errores de correo electrónico
        'email_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'email_errors.log',
            'formatter': 'verbose',
        },
        # Handler para errores generales
        'general_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'general_errors.log',
            'formatter': 'verbose',
        },
        # Handler para errores críticos (500)
        'critical_file': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'critical_errors.log',
            'formatter': 'verbose',
        },
        # Handler para consola (opcional, útil en desarrollo)
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        # Logger para errores específicos de correo electrónico
        'django.core.mail': {
            'handlers': ['email_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Logger para errores generales
        'django': {
            'handlers': ['general_file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
        # Logger para errores críticos
        'critical': {
            'handlers': ['critical_file', 'console'],
            'level': 'CRITICAL',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'general_file'],
        'level': 'INFO',
    },
}


# Email config
EMAIL_BACKEND = env('EMAIL_BACKEND')  
EMAIL_HOST = env('EMAIL_HOST') 
EMAIL_PORT = env.int('EMAIL_PORT')  
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')  
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')  
EMAIL_HOST_USER = env('EMAIL_HOST_USER')  
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  

REQUIRED_ENV_VARS = [
    'EMAIL_BACKEND',
    'EMAIL_HOST',
    'EMAIL_PORT',
    'EMAIL_USE_TLS',
    'EMAIL_USE_SSL',
    'EMAIL_HOST_USER',
    'EMAIL_HOST_PASSWORD',
]

for var in REQUIRED_ENV_VARS:
    if not env(var, default=None): 
        raise ImproperlyConfigured(f"La variable de entorno {var} no está definida.")

# Leer y procesar ADMINS desde el archivo .env
admins_env = env('ADMINS', default='')

ADMINS = [tuple(admin.split(',')) for admin in admins_env.split(';')] if admins_env else []

# Static files & config
MEDIA_ROOT = BASE_DIR / 'media'  

MEDIA_URL = '/media/'


# Archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = '/static/'

# Directorio donde se almacenarán los archivos estáticos recolectados (con collectstatic)
STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Message config
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Config / for routes
APPEND_SLASH = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


