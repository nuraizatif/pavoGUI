#!bin/python
# from app import create_app
from app import app
import config

if __name__ == '__main__':
  app.run(host=app.config['HOST'],
          port=app.config['PORT'],
          debug=app.config['DEBUG'])
