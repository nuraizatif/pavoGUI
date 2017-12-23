import configparser, logging
# from simplekv.memory.redisstore import RedisStore
from datetime import timedelta
from var_dump import var_dump

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

if cfg['mysql']['log_queries'].upper() == 'TRUE':
  log_query = True
else:
  log_query = False

class Config():
  HOST = 'localhost'
  PORT = 8000
  DEBUG = True
  TESTING = False
  ORATOR_DATABASES = {
    'default': 'main',
    'main': {
      'driver': 'mysql',
      'host': cfg['mysql']['host'],
      'database': cfg['mysql']['db'],
      'user': cfg['mysql']['user'],
      'password': cfg['mysql']['password'],
      'prefix': cfg['mysql']['prefix'],
      'log_queries': log_query
    }
  }

  APP_NAME = cfg['app']['name']
  SECRET_KEY = cfg['app']['secret_key']

class ProductionConfig(Config):
  DEBUG = False

class DevelopmentConfig(Config):
  DEBUG = True

class StagingConfig(Config):
  DEBUG = False

class TestingConfig(Config):
  TESTING = True
  # DAMN : ORATOR masih ada isu soal migration di SQLite
  # ORATOR_DATABASES = {
  #   'default': 'main',
  #   'main': {
  #     'driver': 'sqlite',
  #     'database': '/tmp/hedwig_test.db',
  #     'log_queries': log_query
  #   },
  # }
  ORATOR_DATABASES = {
    'default': 'main',
    'main': {
      'driver': 'mysql',
      'host': cfg['mysql']['host'],
      'database': 'hedwig_test',
      'user': cfg['mysql']['user'],
      'password': cfg['mysql']['password'],
      'prefix': cfg['mysql']['prefix'],
      'log_queries': log_query
    }
  }
