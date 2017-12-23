# Import Request
import requests

# Import development class
from var_dump import var_dump

# Import important class.
from flask import Blueprint, render_template, abort
from flask_wtf import FlaskForm 
from wtforms import StringField
from wtforms.validators import InputRequired
from jinja2 import TemplateNotFound

# Import model
from app.pivotal.model import Pivotal as pivotalModel

# Import parent
from app import app, view

# Create form fucntion.
class PivotalForm(FlaskForm):
  pivotal_id = StringField('Pivotal ID', validators=[InputRequired()])

class PivotalAction(view.BaseCrud):
  """docstring for PivotalAction"""
  def __init__(self, Model):
    super(PivotalAction, self).__init__(Model)

  def findId(self, pivotal_id):
    # Find data in database.
    result = self.get(pivotal_id)
    return result

  def getDataPivotal(self, pivotal_id):
    # Find data in Pivotal use Pivotal API.
    ## Define URL.
    url = str(app.config['PIVOTAL_API_URL']) + '/projects/' + str(app.config['PIVOTAL_PRONGHORN_PROJECT_ID']) + '/stories/' + str(pivotal_id)
    ## Define header.
    headers = {
      'X-TrackerToken': str(app.config['PIVOTAL_USER_TOKEN'])
    }
    r = requests.get(url, headers=headers)
    json_data = r.json()
    if json_data['kind'] == 'error' and json_data['error']:
      self.response['message'] = json_data['error']
    else :
      self.response['status'] = True
      self.response['message'] = u'Data Ditemukan.'
      self.response['data'] = json_data
    return self.response

  def function():
    pass

# Create Blueprint.
pivotal = Blueprint('pivotal', __name__)

# Define route for pivotal blueprint.
@pivotal.route('/pivotalForm', methods=['GET', 'POST'])
# Function for this route.
def pivotal_form():
  # Define variable form.
  form = PivotalForm()

  # Define notif.
  notif = {
    'status' : 'danger',
    'msg' : ''
  }

  # Define action.
  pivotalAction = PivotalAction(pivotalModel)

  # Check if form is submitted and validated
  if form.validate_on_submit():
    # Get pivotal id value.
    pivotal_id = form.pivotal_id.data

    # Get data from database.
    result = pivotalAction.findId(pivotal_id)

    if result['status'] == False :
      # Get data from pivotal
      data_pivotal = pivotalAction.getDataPivotal(pivotal_id)
      # Check status get data.
      if data_pivotal['status'] == False:
        # Return error form request.
        notif['msg'] = data_pivotal['message']
      else :
        # Return success msg.
        notif['status'] = 'success'
        notif['msg'] = u'Data Ditemukan.'
    else :
      # Parsing data from database.
      notif['msg'] = result['data']

  # Try to load template.
  try:
    return render_template('pivotalForm.html', form=form, notif=notif)
  except TemplateNotFound:
    abort(404)