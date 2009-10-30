#-*- coding:utf-8 -*-
from os import path
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'postgresql_psycopg2' 
DATABASE_NAME = 'pylogs'
DATABASE_USER = 'root'
DATABASE_PASSWORD = '8855'
DATABASE_HOST = '10.2.1.235'
DATABASE_PORT = ''

TIME_ZONE = 'Asia/Chongqing'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1

USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path.join(path.dirname(__file__),'media')
ALLOW_FILE_TYPES = ('.jpg','.gif','.png')
# URL that handles the media served from MEDIA_URL.
MEDIA_URL = '/media/'
# the theme name 'default, techicon, beijing2008'
THEME_NAME = 'techicon'

STATIC_PATH = './media'

ADMIN_MEDIA_PREFIX = '/admin_media/'

#Send Email settings
EMAIL_HOST = 'smtp.sohu.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''

SECRET_KEY = 'zb2&a4g41snkt&*c92s=djl+*fcp((i85w(k&&)#$5j!+zz!!*'
#setting session expire after half a hour.
#SESSION_COOKIE_AGE =  60 * 30

FACEBOOK_API_KEY = 'b69ea032ef6948cb396c78507381560b'
FACEBOOK_SECRET_KEY = '18c4b39c5e366069f2b77a5258740f5f'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
	'facebook.djangofb.FacebookMiddleware',
)

ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
    path.join(path.dirname(__file__),'templates'),
	'django.template.loaders.app_directories.load_template_source'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'blog',
    'todo',
    'filemanager',
    'wap',    
    'tests',
)
VERSION = (1, 15, 'beta')	


#FEED CONF START
FEED_BLOG_URL_PREFIX = "http://code.google.com/p/pylogs/"  #change to your site url
FEED_POST_AUTHOR_NAME = "Sky"
FEED_COPYRIGHT =  "Pylogs by Sky"
FEED_GLOBAL_TITLE = "Pylogs: Latest Posts"
FEED_GLOBAL_DESCRIPTION = "logging your life..."
#FEED CONF END
