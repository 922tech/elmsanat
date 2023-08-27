from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-zktszoq-z(=nb+*a@+9rl!hwc-$$(s0xbt*$j94y5+m@qmz2fl'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','aras', 'localhost']
SITE_ID = 1
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'
##################### Application definition ###################################################

INSTALLED_APPS = [
    # asgi
    'daphne',
    'apps.delay',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # 3ed party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_extensions',
    'ckeditor',
    'debug_toolbar',
    'oauth2_provider',
    'channels',

    # local apps in 'apps',
    'apps.blog',
    'apps.users',
]

########################################################################################

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

########################################################################################
INTERNAL_IPS = [
    "127.0.0.1",
]
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
########################################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
########################################################################################


########################Database #######################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '<db>',
#         'USER': 'postgres',
#         'PASSWORD': '<password>',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
########################################################################################

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

################### Internationalization ################################################

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

####################### Static Files #################################################################
STATIC_URL = 'static/'

####################### Default Field #################################################################
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


###################### REST framework ########################
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',

        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES':(
    #     'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    # )
}
##############################################################

########################## Celery ~ Redis ####################

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_IGNORE_RESULT = False
CELERY_TIMEZONE = TIME_ZONE
CELERY_TRACK_STARTED = True
CELERYD_LOG_FILE = os.path.join(BASE_DIR, 'celery', 'logs')   
CELERYD_LOG_LEVEL = "INFO"
# CELERY_TIMEZONE = "Asia/Tehran"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_CACHE_BACKEND = 'default'



######################### Cache #############################
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': "redis://localhost:6379/1",
        # 'OPTIONS': {
        #     "CLIENT_CLASS": "django_reids.client.DefaultClient"
        # }
    },
}
CACHE_TTL = 60 * 15
##############################################################

############################### Oauth2 #######################################

LOGIN_URL = 'https://127.0.0.1/admin'

TOKEN_URL = 'http://localhost:8000/o/token/'
REVOKE_TOKEN_URL = 'http://localhost:8000/o/revoke_token/'

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'},
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,
    'REFRESH_TOKEN_EXPIRE_SECONDS': 3600 * 24 * 365,
}
OAUTH_CREDENTIALS = {
    'login':{
        'client_id':'cuYpFUwIxAUiPPlwTYZIpmZBKD4k94FCKU1sURkE',
        'client_secret':'6TozRm6roJS0lawEGZQJ82xylzydt91VvItNb3VzozCd3DAitQOItr1k7e0sWw3YxhTvnidoSgCfd8lZh9sTpJFsTVsjS6T5DKFVAy3dPtJBrjWN86kZZ6jElUj2NGih',
        'client_type':'confidential',
        'Authorization_grant_type':'password'
    },
}

############################## Channels #########################################
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}