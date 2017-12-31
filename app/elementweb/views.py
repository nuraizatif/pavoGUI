# Import Request.
import requests

# Import development class.
from var_dump import var_dump

# Import important class.
from flask import Blueprint, render_template, abort, request, redirect, url_for
from jinja2 import TemplateNotFound

# Import form.
from app.elementweb.form import ElementWebForm

# Import Action.
from app.elementweb.actions import ElementWebAction

# Import model.
from app.elementweb.model import Elementweb as ElementwebModel

# Create Blueprint.
elementweb = Blueprint('elementweb', __name__)

# Define route for elementweb blueprint.
@elementweb.route('/elementWebForm', methods=['GET', 'POST'])
# Function for this route.
def elementWebForm():

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

  op = ''
  if 'op' in request.args:
    op = request.args["op"]

  elementId = ''
  if 'id' in request.args:
    elementId = request.args["id"]

  # Create action object.
  elementAction = ElementWebAction(ElementwebModel)

  if op == 'delete':
    # Delete Data.
    deleteData = elementAction.deleteData(elementId)

    # Check status
    if deleteData['status'] == False :
      notif['msg'] = deleteData['message']
    else :
      return redirect(url_for('elementweb.elementWebForm', msg=deleteData['message'], status='success'))

  elementDetails = {}
  if op == 'edit':
    # Get details element
    elementDetailsData = elementAction.findId(elementId)

    if elementDetailsData['status'] == True:
      elementDetails = elementDetailsData['data']

  # Define variable form.
  form = ElementWebForm(elementDetails)

  # Check if form is submitted and validated
  if form.validate_on_submit():
    # Get hidden id.
    elementHiddenId = form.element_id.data

    if elementHiddenId == '':
      # Prepare Data Insert.
      data = {
        'name' : form.name_element.data,
        'type' : form.element_type.data,
        'value' : form.element_value.data,
      }

      # Insert Data.
      insertElement = elementAction.insertData(data)

      if insertElement['status'] == True:
        notif['status'] = 'success'
      else :
        notif['status'] = 'danger'
      notif['msg'] = insertElement['message']
    else :
      # Prepare Data Update.
      data = {
        'name' : form.name_element.data,
        'type' : form.element_type.data,
        'value' : form.element_value.data,
      }

      # Update Data.
      updateElement = elementAction.updateData(elementHiddenId, data)

      if updateElement['status'] == True:
        notif['status'] = 'success'
        notif['msg'] = 'Berhasil Edit Element'
      else :
        notif['status'] = 'danger'
        notif['msg'] = updateElement['message']

  # Get data element.
  elementData = elementAction.findAll()

  if elementData['status'] == True:
    notif['data'] = elementData['data']

  # Try to load template.
  try:
    return render_template('elementWebForm.html', form=form, notif=notif)
  except TemplateNotFound:
    abort(404)