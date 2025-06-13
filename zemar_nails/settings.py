from pathlib import Path
from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured
import environ
import pymysql
pymysql.install_as_MySQLdb()
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializa django-environ (ya no pasamos ALLOWED_HOSTS/CSRF aquí)
env = environ.Env(
    DEBUG=(bool, False),
)


# → Load .env immediately, **before** any env.bool/env.list
env_file = BASE_DIR / ".env"
if env_file.exists():
    env.read_env(env_file=env_file)


# Now we can safely read DEBUG and all the rest
DEBUG = env.bool("DEBUG")
SECRET_KEY = env("SECRET_KEY")

# Hosts and CSRF origins (lists)
ALLOWED_HOSTS = [
    "carla-marquez.up.railway.app",
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
]

CSRF_TRUSTED_ORIGINS = [
    "https://carla-marquez.up.railway.app",
]

# SSL / Proxy headers
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE   = not DEBUG
CSRF_COOKIE_SECURE      = not DEBUG
SECURE_HSTS_SECONDS     = 3600 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD     = not DEBUG
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST    = True


# App definitions
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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


# Configuración de la base de datos
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=None,
    )
}

if not DATABASES['default']:
    raise ValueError("DATABASE_URL no está configurada en las variables de entorno")

# Forzar el charset utf8mb4
DATABASES['default']['OPTIONS'] = {
    'charset': 'utf8mb4',
    'init_command': "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'",
}

"""
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
"""

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

TIME_ZONE = 'Atlantic/Canary'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Url redirection
LOGIN_URL = 'login'
LOGOUT_URL= "/"

# Cookie session config
SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
SESSION_COOKIE_NAME = 'sessionid'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # Todo log va a consola: Railway lo captura en sus propios logs
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Envia correo a ADMINS si hay errores en peticiones HTTP (500)
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'loggers': {
        # Captura errores de vistas y middlware (500)
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Mensajes generales de Django al nivel WARNING+
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
    # Logs de tu propia app (nivel INFO+)
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Forzar que el handler 'console' use el formateador 'verbose'
LOGGING['handlers']['console']['formatter'] = 'verbose'

# Asegurarte de que django.request solo loguea ERROR (y no INFO/WARNING)
LOGGING['loggers']['django.request']['level'] = 'ERROR'


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

# Static files & WhiteNoise configuration
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']       # Tus carpetas de CSS/JS sin colectar
STATIC_ROOT = BASE_DIR / 'staticfiles'        # Aquí cae collectstatic
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Opciones extra de WhiteNoise
WHITENOISE_ROOT = STATIC_ROOT
WHITENOISE_ALLOW_ALL_ORIGINS = True           # Permite CORS en tus assets
WHITENOISE_AUTOREFRESH = DEBUG                # Recarga en desarrollo
WHITENOISE_USE_FINDERS = DEBUG                 # Encuentra archivos en DEBUG


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


