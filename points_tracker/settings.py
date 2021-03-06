# -*- coding: utf-8 -*-
import os, sys

### logging configure values ###############################################
import logging
from logging import config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s| %(name)s/%(process)d: %(message)s @%(funcName)s:%(lineno)d #%(levelname)s',
        }
    },
    'handlers': {
        'console': {
           'formatter': 'standard',
           'class': 'logging.StreamHandler'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'points_tracker': {
            'level': 'INFO',
        },
    }
}
config.dictConfig(LOGGING)
############################################################################x

class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    SECRET_KEY = 'TYdVdFdsuyEBYL9UGN4VGLTm'
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    ADMIN_ENABLED = True
    ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'mp4', 'ogg'])

class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    ASSETS_DEBUG = True
    # Uncomment this line to debug javascript/css assets
    # ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/points_tracker'

    # Ease up on password requirements in dev to allow simple testing
    PASSWORD_REQUIRE_MIN = 4
    PASSWORD_REQUIRE_SPECIAL = False
    PASSWORD_REQUIRE_UPPER = False
    PASSWORD_REQUIRE_LOWER = False
    PASSWORD_REQUIRE_NUMBER = False
    UPLOAD_FOLDER = os.path.abspath(os.path.join(Config.PROJECT_ROOT, 'points_tracker/static/audio'))

    AUDIO_DB_LEVEL = -21.9297220851 #after this setting is changed you should run normalize_audio_files from manage.py
    MAX_AUDIO_DURATION_MS = 15*1000 #this is in ms

    APP_URL = 'localhost:5000'

    PLAY_ON_SONOS = True
    SONOS_IP = '10.10.110.32'
    SONOS_VOLUME = 50

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    ADMIN_ENABLED = False


def get_config_for_current_environment():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        return TestConfig
    elif os.environ.get("APP_ENV") == 'dev':
        return DevConfig
    else:
        # stage, demo, prod, etc. all get prod-like settings (e.g. no asset debugging)
        return ProdConfig
