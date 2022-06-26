# Django settings for ecomstore project.
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

SECRET_KEY = '(-(73dveotti(1rkovdzwtj$f&ag7tk(%&)@s*15bla*rj+h^s'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    #'django.contrib.postgres',

    'catalog',
    'cart',
    'accounts',
    'search',
    'checkout',
    'stats',
    'taggit',
    #'tagging',
    'billing',
]

WSGI_APPLICATION = 'ecomstore.wsgi.application'

ROOT_URLCONF = 'ecomstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR / 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ecomstore.context_processors.ecomstore',
            ],
        },
    },
]

# Upon deployment, change to True
ENABLE_SSL = False

# Uncomment the following line after installing memcached
# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ecomstore.db',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'blog',
#         'USER': 'blog',
#         'PASSWORD': '*****',
#     }
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # 'marketing.urlcanon.URLCanonicalizationMiddleware',
    # 'ecomstore.SSLMiddleware.SSLRedirect',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

CACHE_TIMEOUT = 60 * 60

LOGIN_REDIRECT_URL = '/accounts/my_account/'

SESSION_COOKIE_DAYS = 90

SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_COOKIE_DAYS

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'assets'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

AUTH_PROFILE_MODULE = 'accounts.userprofile'


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

# for use with URL Canonicalization Middleware:
# this is the canonical hostname to be used by your app (required)
CANON_URL_HOST = 'www.your-domain.com'
# these are the hostnames that will be redirected to the CANON_URL_HOSTNAME
# (optional; if not provided, all non-matching will be redirected)
CANON_URLS_TO_REWRITE = ['your-domain.com', 'other-domain.com']

# Google Analytics tracking ID
# should take the form of 'UA-xxxxxxx-x', where the X's are digits
ANALYTICS_TRACKING_ID = ''

# Email Settings

LOGIN_REDIRECT_URL = '/accounts/my_account/'

LOGOUT_REDIRECT_URL = 'catalog_home'

CACHE_TIMEOUT = 60 * 60

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django-tagging settings
FORCE_LOWERCASE_TAGS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'your_account@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_password'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
