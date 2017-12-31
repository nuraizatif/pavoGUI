# Import Request
import requests

# Import development class
from var_dump import var_dump

# Import important class.
from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

# Import model
from app.pivotal.model import Pivotal as pivotalModel

# Import actions
from app.pivotal.actions import PivotalAction

# Import form
from app.pivotal.form import PivotalForm

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
    'msg' : '',
    'data' : ''
  }

  if 'status' in request.args:
    notif['status'] = request.args["status"]

  if 'msg' in request.args:
    notif['msg'] = request.args["msg"]

  # Define action.
  pivotalAction = PivotalAction(pivotalModel)

  # Check if form is submitted and validated
  if form.validate_on_submit():
    # Get pivotal id value.
    pivotal_id = form.pivotal_id.data
    updateButton = form.submit_update.data

    # Get data from database.
    result = pivotalAction.findByPivotalID(pivotal_id)

    if result['status'] == False :
      # Get data from pivotal.
      data_pivotal = pivotalAction.getDataPivotal(pivotal_id)
      # Check status get data.
      if data_pivotal['status'] == False:
        # Return error form request.
        notif['msg'] = data_pivotal['message']
      else :
        # Set msg data found in pivotal
        notif['msg'] = u'Data Ditemukan di pivotal tracker.'
        # Processing data to database.
        ## Define data.
        data ={
          'pivotal_id': str(data_pivotal['data']['id']),
          'title': data_pivotal['data']['name'],
          'type': data_pivotal['data']['story_type'],
          'status': data_pivotal['data']['current_state'],
          'json_data': str(data_pivotal['data'])
        }
        if 'description' in data_pivotal['data']:
          data['description'] = data_pivotal['data']['description']

        insert_data = pivotalAction.insertData(data)

        if insert_data['status'] == False:
          # Return error form request.
          notif['msg'] = insert_data['message']
        else :
          # Return success msg.
          notif['status'] = 'success'
          notif['msg'] = u'Data Ditemukan di pivotal tracker dan berhasil dimasukan ke dalam database.'

          # Parsing data.
          notif['data'] = pivotalAction.parsingData(insert_data['data'])
    else :
      # Parsing data from database.
      notif['status'] = 'success'
      notif['msg'] = u'Data Berhasil Ditemukan Di Database'

      if updateButton:
        # update data pivotal.
        result = pivotalAction.updatePivotal(pivotal_id)

      # Parsing data.
      notif['data'] = pivotalAction.parsingData(result['data'])

  # Try to load template.
  try:
    return render_template('pivotalForm.html', form=form, notif=notif)
  except TemplateNotFound:
    abort(404)