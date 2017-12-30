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
  PORT = 5000
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
  BASE_URL = cfg['app']['base_url']

  PIVOTAL_API_URL = cfg['pivotal']['url']
  PIVOTAL_USER_TOKEN = cfg['pivotal']['user_token']
  PIVOTAL_PRONGHORN_PROJECT_ID = cfg['pivotal']['pronghorn_project_id']
  PIVOTAL_HUGGIN_PROJECT_ID = cfg['pivotal']['huggin_project_id']
  PIVOTAL_MUNNIN_PROJECT_ID = cfg['pivotal']['munnin_project_id']
  PIVOTAL_FRIGATE_PROJECT_ID = cfg['pivotal']['frigate_project_id']
  PIVOTAL_PHOENIX_PROJECT_ID = cfg['pivotal']['phoenix_project_id']

  PRACTITEST_API_URL = cfg['practitest']['url']
  PRACTITEST_USER = cfg['practitest']['user']
  PRACTITEST_USER_TOKEN = cfg['practitest']['token']
  PRACTITEST_PROJECT_ID = cfg['practitest']['id']

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
