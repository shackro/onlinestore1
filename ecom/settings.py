import os


# STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
# USERNAME = config('USERNAME')
# PASSWORD = config('PASSWORD')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '+5v@@hv^37k3*#y4c0)h6s1yl*8)=)y=wd9$m%wtpbr6fnwl1e'

DEBUG = True

ALLOWED_HOSTS = ['*','.vercel.app']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'paypal.standard.ipn',

    'crispy_forms',
    'django_countries',
    "widget_tweaks",

    'catalog',

        # Providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.apple',
]

MIDDLEWARE = [
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Add this line
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]



SITE_ID = 1

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ecom.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


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
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
LOGIN_REDIRECT_URL = 'home/'
SIGNUP_REDIRECT_URL = 'login/'
LOGIN_URL = '/login/' 


CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# PayPal Settings
PAYPAL_RECEIVER_EMAIL = 'amazontechphone@gmail.com'
PAYPAL_TEST = False  # Set to False in production


PAYPAL_BUY_BUTTON_IMAGE = "https://www.paypalobjects.com/webstatic/en_US/i/buttons/checkout-logo-medium.png"
PAYPAL_CLIENT_ID = 'your-client-id'
PAYPAL_CLIENT_SECRET = 'your-secret-key'

# Square Settings
SQUARE_ACCESS_TOKEN = 'EAAAl8Tg6VKgyckyhiJLo5mUv8hpfVzgApGihC9LBQLR4ZJgRfZITLnoPsmOMVUC'
SQUARE_ENVIRONMENT = 'production'  # Use 'production' for live payments
SQUARE_LOCATION_ID = 'LM5PM9RRKNM5B'



