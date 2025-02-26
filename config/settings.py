import os
from django.contrib.messages import constants as messages
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zjv+iqw$i=l$1r^2x&6quhazt#3g0o!a4$nh)eifd!%3r*pfn7"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Adicionando o ip da minha máquina para habilitar o acesso pelo smartphone
ALLOWED_HOSTS = ['192.168.4.106', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
   "django.contrib.admin",
   'django.contrib.auth',
   'django.contrib.contenttypes',
   "django.contrib.sessions",
   "django.contrib.messages",
   "django.contrib.staticfiles",
   "autenticacao",
   "core",
   "cadastros",
   "sistema",
   "reservas",
   "financeiro",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.NoCacheMiddleware",
]

ROOT_URLCONF = "config.urls"

# integra com o sistema de auth padrao do Django

#integra com o sistema de auth padrao do Django
AUTH_USER_MODEL = 'cadastros.Usuario' 
AUTHENTICATION_BACKENDS = [
    'cadastros.backends.EmailBackend',  #backend de autenticacao personalizado
    # 'django.contrib.auth.backends.ModelBackend',  #backend de autenticacao padrao
]
# AUTH_USER_MODEL = 'sistema.CustomUser'



TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "resources")],  # define recursos usados pelos templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

#URL de redirecionamento apos login
LOGIN_REDIRECT_URL = 'core:main'
LOGOUT_REDIRECT_URL = 'autenticacao:login'
LOGIN_URL = 'autenticacao:login'


WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bd_gestoriihost",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Settings for messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "resources/static/"),
]

# Arquivos de midia 
# Configuração de arquivos de mídia
MEDIA_URL = '/media/'  # URL para acessar os arquivos de mídia
MEDIA_ROOT = os.path.join(BASE_DIR, 'resources', 'media')  # Diretório onde os arquivos de mídia serão armazenados


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Configurações de variáveis globais
NUMBER_GRID_PAGES = 10
NUMBER_GRID_MODAL = 3

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "gestoriihost@gmail.com"
EMAIL_HOST_PASSWORD = "rnux bjgo ojdv lmro"