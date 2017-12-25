# Import important class.
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

# Create form fucntion.
class PivotalForm(FlaskForm):
  pivotal_id = StringField(u'Pivotal ID', validators=[InputRequired()])
  submit_search = SubmitField(u'Search', render_kw={"class": "btn btn-primary"})
  submit_update = SubmitField(u'Update Data Pivotal', render_kw={"class": "btn btn-warning"})
