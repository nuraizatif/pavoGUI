# Import development class
from var_dump import var_dump

# Import important class.
from flask import Blueprint, render_template, abort
from flask_wtf import FlaskForm 
from wtforms import StringField
from wtforms.validators import InputRequired
from jinja2 import TemplateNotFound

# Create form fucntion.
class PivotalForm(FlaskForm):
  pivotal_id = StringField('Pivotal ID', validators=[InputRequired()])

# class PivotalAction():
#   """docstring for PivotalAction"""
#   def __init__(self):

# Create Blueprint.
pivotal = Blueprint('pivotal', __name__)

# Define route for pivotal blueprint.
@pivotal.route('/pivotalForm', methods=['GET', 'POST'])
# Function for this route.
def pivotal_form():
  # Define variable form.
  form = PivotalForm()

  # Check if form is submitted and validated
  if form.validate_on_submit():
    # Logic button
    return 'Form Successfully Submitted!'

  # Try to load template.
  try:
    return render_template('pivotalForm.html', form=form)
  except TemplateNotFound:
    abort(404)