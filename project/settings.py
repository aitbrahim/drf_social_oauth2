import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*', ]


def project_base(f=''):
    return os.path.join(BASE_DIR, f)


def public_assets():
    return os.path.join(BASE_DIR, os.path.pardir, 'public_assets')


sys.path.insert(0, project_base())

# Application definition


ROOT_URLCONF = 'project.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9l#mp^ezfer(n1k=ltf-6n(-av^((15vq!0c74=hqipv#6m@yr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_docs',
    'profile',
    'social_oauth2'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'profile.User'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT
STATIC_ROOT = public_assets()



# SOCIAL auth config
AUTHENTICATION_BACKENDS = (
    'social_oauth2.backends.facebook.FacebookOAuth2',
)

# Facebook

SOCIAL_AUTH_FACEBOOK_KEY = '174280429741376'
SOCIAL_AUTH_FACEBOOK_SECRET = 'fe84f7f3e150708bef7e4837a52fee62'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]  # optional
# This is mandatory since facebook does return the email authorization api
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}
SOCIAL_AUTH_FACEBOOK_API_VERSION = '3.0'


SOCIAL_AUTH_PIPELINE = (
    'social_oauth2.pipeline.social_auth.social_details',
    'social_oauth2.pipeline.social_auth.social_uid',
    'social_oauth2.pipeline.social_auth.social_user',
    'social_oauth2.pipeline.social_auth.associate_by_email',
    # 'profile.pipeline.validate_data',
    'social_oauth2.pipeline.user.create_user',
    'social_oauth2.pipeline.social_auth.associate_user',
    'social_oauth2.pipeline.social_auth.load_extra_data',
    'social_oauth2.pipeline.user.user_details',
    'profile.pipeline.create_token',
    # 'django_profile.pipeline.save_profile_picture',
)
