# Import important class.
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextField, SelectField, FieldList, FormField

# Create Field List.
class PractitestTestCase(FlaskForm):
  testcase_title = StringField(
    u'Title',
    render_kw={
      'style' : 'width:200px;',
    }
  )
  testcase_gherkin = TextField(
    u'Gherkin',
    render_kw={
      'style' : 'height:200px;resize: none;',
    }
  )


# Create form fucntion.
class PractitestFrom(FlaskForm):
  pivotal_id = StringField(
    u'Pivotal ID',
    render_kw={
      'disabled' : True,
      'style' : 'width:200px;',
    }
  )
  pivotal_title = StringField(
    u'Pivotal Title',
    render_kw={
      'disabled' : True
    }
  )
  pivotal_type = StringField(
    u'Pivotal Type',
    render_kw={
      'disabled' : True,
      'style' : 'width:200px;',
    }
  )
  pivotal_description = TextField(
    u'Pivotal Description',
    render_kw={
      'disabled' : True,
      'style' : 'height:200px;resize: none;',
    }
  )
  pivotal_status = StringField(
    u'Pivotal Current Status',
    render_kw={
      'disabled' : True,
      'style' : 'width:200px;',
    }
  )
  practitest_status = SelectField(
    u'Practitest Status',
    choices=[
      ('Ready', 'Ready'),
      ('Draft', 'Draft'),
      ('To Repair', 'To Repair'),
      ('Obsolete', 'Obsolete')
    ],
    render_kw={
      'style' : 'width:200px;',
    }
  )
  practitest_testing_phase = SelectField(
    u'Practitest Testing Phase',
    choices=[
      ('Unit', 'Unit'),
      ('Integration', 'Integration'),
      ('System', 'System'),
      ('User Acceptence', 'User Acceptence')
    ],
    render_kw={
      'style' : 'width:200px;',
    }
  )
  practitest_testing_level = SelectField(
    u'Practitest Testing Level',
    choices=[
      ('Sanity', 'Sanity'),
      ('Regresion', 'Regresion')
    ],
    render_kw={
      'style' : 'width:200px;',
    }
  )
  practitest_product_component = SelectField(
    u'Practitest Product Component',
    choices=[
      ('Application System', 'Application System'),
      ('Web Client', 'Web Client'),
      ('Database Server', 'Database Server')
    ],
    render_kw={
      'style' : 'width:200px;',
    }
  )
  practitest_os = SelectField(
    u'Practitest Testing OS',
    choices=[
      ('Mac', 'Mac'),
      ('Windows', 'Windows'),
      ('Linux', 'Linux'),
      ('iOS', 'iOS'),
      ('Android', 'Android')
    ],
    render_kw={
      'style' : 'width:200px;',
    }
  )
  practitest_test_case = SelectField(
    u'Practitest Test Case',
    choices=[
      ('Positive', 'Positive'),
      ('Negative', 'Negative')
    ],
    render_kw={
      'style' : 'width:200px;',
    }
  )
  practitest_release = StringField(
    u'Release',
    render_kw={
      'style' : 'width:200px;',
    }
  )
  robot_type = SelectField(
    u'Robotframework Type',
    choices=[
      ('api', 'API Test'),
      ('web', 'Web / MWEB Test')
    ],
    render_kw={
      'style' : 'width:200px;',
    }
  )
  practitest_testcase = FieldList(FormField(PractitestTestCase), u'Practitest Test Case', min_entries=1)
  save_data = SubmitField(u'Save Data', render_kw={"class": "btn btn-primary"})
  create_run = SubmitField(u'Create File and Run', render_kw={"class": "btn btn-warning"})

  def __init__(self, pivotalData):
    super(PractitestFrom, self).__init__()

    # Rewrite value
    self.pivotal_id.value = pivotalData['pivotal_id']
    self.pivotal_title.value = pivotalData['title']
    self.pivotal_type.value = pivotalData['type'].title()
    self.pivotal_description.value = pivotalData['description']
    self.pivotal_status.value = pivotalData['status'].title()
