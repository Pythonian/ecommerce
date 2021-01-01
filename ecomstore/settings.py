# Django settings for ecomstore project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

SECRET_KEY = '(-(73dveotti(1rkovdzwtj$f&ag7tk(%&)@s*15bla*rj+h^s'

WSGI_APPLICATION = 'ecomstore.wsgi.application'


SITE_NAME = 'Modern Musician'
META_KEYWORDS = 'Music, instruments, sheet music, musician'
META_DESCRIPTION = 'Modern Musician is an online supplier of instruments, sheet music, and other accessories for musicians'

CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Upon deployment, change to True
ENABLE_SSL = False

# Uncomment the following line after you have installed memcached on your local development machine
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(CURRENT_PATH, 'ecomstore.db'),
    }
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

CACHE_TIMEOUT = 60 * 60


PRODUCTS_PER_PAGE = 1
PRODUCTS_PER_ROW = 4

LOGIN_REDIRECT_URL = '/accounts/my_account/'

SESSION_COOKIE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_COOKIE_DAYS

STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(CURRENT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'marketing.urlcanon.URLCanonicalizationMiddleware',
    'ecomstore.SSLMiddleware.SSLRedirect',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]


AUTH_PROFILE_MODULE = 'accounts.userprofile'

ROOT_URLCONF = 'ecomstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(CURRENT_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.ecomstore',
            ],
        },
    },
]

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

INSTALLED_APPS = (
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

    'catalog',
    'cart',
    'accounts',
    'search',
    'checkout',
    'utils',
    'stats',
    'caching',
    'djangodblog',
    'tagging',
    'billing',
)
# for use with URL Canonicalization Middleware:
# this is the canonical hostname to be used by your app (required)
CANON_URL_HOST = 'www.your-domain.com'
# these are the hostnames that will be redirected to the CANON_URL_HOSTNAME
# (optional; if not provided, all non-matching will be redirected)
CANON_URLS_TO_REWRITE = ['your-domain.com', 'other-domain.com']

# Google Checkout API credentials
GOOGLE_CHECKOUT_MERCHANT_ID = ''
GOOGLE_CHECKOUT_MERCHANT_KEY = ''
GOOGLE_CHECKOUT_URL = 'https://sandbox.google.com/checkout/api/checkout/v2/merchantCheckout/Merchant/' + GOOGLE_CHECKOUT_MERCHANT_ID

# Authorize.Net API Credentials
AUTHNET_POST_URL = 'test.authorize.net'
AUTHNET_POST_PATH = '/gateway/transact.dll'
AUTHNET_LOGIN = ''
AUTHNET_KEY = ''

# Google Analytics tracking ID
# should take the form of 'UA-xxxxxxx-x', where the X's are digits
ANALYTICS_TRACKING_ID = ''

# Email Settings

LOGIN_REDIRECT_URL = '/accounts/my_account/'

LOGOUT_REDIRECT_URL = 'catalog_home'

# AUTH_PROFILE_MODULE = 'accounts.userprofile'

CACHE_TIMEOUT = 60 * 60
