# Import config class {root_dir}/config.py.
import config, orator, os

# Import important class.
from flask import Flask, render_template, redirect, url_for
from flask_wtf import Form
from flask_orator import Orator
from flask_bootstrap import Bootstrap

# Import development class.
from var_dump import var_dump

# Create app variable.
app = Flask(__name__, static_folder="static")

# Try to get config variable.
try:
  ## check environment var.
  env = os.environ.get('FLASK_ENV', 'development')
  if env=='production':
    app.config.from_object(config.ProductionConfig)
  elif env=='testing':
    app.config.from_object(config.TestingConfig)
  elif env=='staging':
    app.config.from_object(config.StagingConfig)
  else:
    app.config.from_object(config.DevelopmentConfig)
except Exception as e:
  raise e

# Use Bootstrap class .
Bootstrap(app)
# Create db varuable.
db  = Orator(app)

# Import Blueprint.
from app.pivotal.views import pivotal as pivotalForm

# Registering Blueprint.
app.register_blueprint(pivotalForm)

# Registering Index Apps.
@app.route('/')
def index():
  ## Redirect to pivotal form.
  return redirect(url_for('pivotal.pivotal_form'))

if __name__ == '__main__':
  app.run(debug=True)