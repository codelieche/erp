"""
Django settings for erp project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# 把apps添加到path路径中，app统一放apps中
# PyCharm中需要右击apps，点击：Mark Directory As >>> Sources Root
sys.path.append(str(BASE_DIR.joinpath('apps')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!%h&_kmw5twx(hwwiwt^y%l9(apu-xiu(h98uq=gcg#%0$p6qj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方app
    'rest_framework',
    'django_filters',
    'corsheaders',
    # 自己写的app
    'codelieche.apps.CodeliecheConfig',
    'account.apps.AccountConfig',
    'config.apps.ConfigConfig',
    'modellog.apps.ModellogConfig',
    'utils.apps.UtilsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # cors
    'corsheaders.middleware.CorsMiddleware',
    # 自定义中间件
    'codelieche.middlewares.csrf.ApiDisableCsrfMiddleware',
]

APPEND_SLASH = False
ROOT_URLCONF = 'erp.urls.main'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
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

WSGI_APPLICATION = 'erp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("ERP_DEVELOP_DB", "erp_develop"),
        'USER': os.environ.get("MYSQL_USER", 'root'),
        'PASSWORD': os.environ.get("MYSQL_PASSWORD", ''),
        'HOST': os.environ.get("MYSQL_HOST", '127.0.0.1'),
        'PORT': os.environ.get("MYSQL_PORT", 3306),
        'OPTIONS': {
           'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = Path.joinpath(BASE_DIR, '../static')
STATICFILES_DIRS = (
    # str(Path.joinpath(BASE_DIR, 'static')),
    str(BASE_DIR.joinpath('static')),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Rest Framework的配置
REST_FRAMEWORK = {
    # 设置分页
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'codelieche.pagination.SelfPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 为了调试，需要BrowsableAPIRenderer，正式环境需要注释下面这行
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # DatetimeField设置时间格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    # 用户认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# 注册用户系统使用哪个用户模型
# 不需要加入中间的models
AUTH_USER_MODEL = 'account.UserProfile'

# 使用自定义后台auth认证方法
AUTHENTICATION_BACKENDS = (
    # 'django_python3_ldap.auth.LDAPBackend',
    'account.auth.CustomBackend',
)

# 多个系统在本地开发，防止sessionid被覆盖，不使用默认的seession cookie name
SESSION_COOKIE_NAME = "erp_seessionid"

# 跨域访问相关配置
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'OPTIONS',
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-headers',
]

# 对称加密秘钥
PASSWORD_KEY = "0000000000000000"

# Redis相关配置
REDIS_HOST_PORT = os.environ.get("REDIS_HOST_PORT", "127.0.0.1:6379")
REDIS_CONFIG = {
    "host": REDIS_HOST_PORT.split(':')[0],
    "port": REDIS_HOST_PORT.split(':')[1],
    "db": 7,
    "password": None
}

CELERY_BROKER_URL = 'redis://{}/8'.format(REDIS_HOST_PORT)
CELERY_RESULT_BACKEND = 'redis://{}/9'.format(REDIS_HOST_PORT)
CELERY_ACCEPT_CONTENT = ['application/json', 'pickle']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'pickle'
