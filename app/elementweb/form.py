# Import important class.
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import InputRequired

# Create form fucntion.
class ElementWebForm(FlaskForm):
  element_id = HiddenField(u'Element ID')
  name_element = StringField(u'Element Name', validators=[InputRequired()])
  element_type = SelectField(
    u'Element Type',
    choices=[
      ('id', 'id'),
      ('css', 'css'),
      ('xpath', 'xpath'),
    ],
    render_kw={
      'style' : 'width:200px;',
    },
    validators=[InputRequired()]
  )
  element_value = StringField(u'Element Value', validators=[InputRequired()])
  submit_button = SubmitField(u'Add Element', render_kw={"class": "btn btn-primary"})

  def __init__(self, data = {}):
    super(ElementWebForm, self).__init__()

    if data != {}:
      self.element_id.data = data['id']
      self.element_id.value = data['id']
      self.name_element.value = data['name']
      self.element_type.value = data['type']
      self.element_value.value = data['value']
