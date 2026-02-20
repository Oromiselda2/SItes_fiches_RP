from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Change cette clé en production
SECRET_KEY = 'django-insecure-change-this-key-please-123456'

DEBUG = True

ALLOWED_HOSTS = []  # Pour local. Si accès externe : ['*']

# ======================
# Applications
# ======================

# Dans INSTALLED_APPS, ajoutez :
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # ← Nouveau
    
    # Allauth
    'allauth',  # ← Nouveau
    'allauth.account',  # ← Nouveau
    'allauth.socialaccount',  # ← Nouveau
    'allauth.socialaccount.providers.discord',  # ← Nouveau
    
    # Vos apps
    'core',
    'fiches',
    'comments',
]

# ======================
# Middleware
# ======================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    # Middleware custom pour logs
  #  'core.middleware.RequestMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ======================
# Templates
# ======================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# ======================
# Base de données (SQLite)
# ======================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ======================
# User personnalisé
# ======================

AUTH_USER_MODEL = 'core.User'

# ======================
# Validation mots de passe
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

# ======================
# Internationalisation
# ======================

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True
USE_TZ = True

# ======================
# Static & Media
# ======================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================
# Logs Django (console)
# ======================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ======================
# Sites Framework
# ======================
SITE_ID = 1

# ======================
# Allauth Configuration
# ======================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuration allauth
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True

# Configuration Discord
SOCIALACCOUNT_PROVIDERS = {
    'discord': {
        'APP': {
            'client_id': '1473040707089469665',  # À remplacer
            'secret': '8_zs99RCNYvSS3-USPo_tTAUDbLGd6zx',  # À remplacer
            'key': ''
        },
        'SCOPE': ['identify', 'email', 'guilds'],  # Permissions demandées
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Redirection après connexion
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'