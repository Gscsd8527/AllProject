"""
Django settings for RestFramework project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd%=w@)#q7ro(y=j44rwaf4hi-)h5(*a5$ohsy$3!y&u--atr_q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RestFramework.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'RestFramework.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rest_test',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '10.0.90.190',
        'PORT': '3306',
        "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# rest分页配置
# REST_FRAMEWORK = {
#     'PAGE_SIZE': 5  # 每页数目
# }


# DRF配置信息
# REST_FRAMEWORK = {
#     # 全局认证
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # BasicAuthentication:此身份验证方案使用HTTP基本身份验证
#         'rest_framework.authentication.BasicAuthentication',
#         # SessionAuthentication:此身份验证方案使用Django的默认会话后端进行身份验证
#         'rest_framework.authentication.SessionAuthentication',
#     ],
#     # 全局权限
#     'DEFAULT_PERMISSION_CLASSES': [
#         # 'rest_framework.permissions.IsAuthenticated',  # 仅通过认证的用户
#         'rest_framework.permissions.AllowAny',  # 允许所有用户
#         #'rest_framework.permissions.IsAdminUser',  # 仅管理员用户
#     ]
# }


# 自定义权限
REST_FRAMEWORK = {
    # 全局认证 优先级高于试图类中的配置
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'Api.auth.JewQueryParamsAuthenticate' # 这里配置了，视图中就不用配置了
        # 'Api.permission.MyAuthenticate',  # 用户认证的权限
    ],
    "UNAUTHENTICATED_USER": None,  # 匿名，request.user = None
    "UNAUTHENTICATED_TOKEN": None, # 匿名，request.auth = None
    # "DEFAULT_PERMISSION_CLASSES": ['Api.permission.MyPremission'],  # 表示每一个视图类（只要不重写permission_classes属性），都需要SVIP的用户才能访问。
}

import datetime
# jwt载荷中的有效期设置
JWT_AUTH = {
    # token 有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=8),
    'JWT_ALLOW_REFRESH': True,
     #续期有效期（该设置可在24小时内带未失效的token 进行续期）
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=24), # token前缀
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    # 自定义返回格式，需要手工创建
    'JWT_RESPONSE_PAYLOAD_HANDLER': "Users.utils.jwt_response_payload_handler",
}