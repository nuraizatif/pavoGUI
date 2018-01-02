# Import development class
from var_dump import var_dump

# Import important class.
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextField, SelectField, FieldList, FormField, HiddenField
from wtforms.validators import InputRequired

# Create Field List.
class PractitestTestCase(FlaskForm):
  testcase_id = HiddenField(u'Test Case ID')
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
  practitest_id = HiddenField(u'Practitest ID')
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
    },
    validators=[InputRequired()]
  )
  robot_type = SelectField(
    u'Robotframework Type',
    choices=[
      ('api', 'API Test'),
      ('web', 'Web / MWEB Test'),
      ('android', 'Android'),
    ],
    render_kw={
      'style' : 'width:200px;',
    }
  )
  practitest_testcase = FieldList(FormField(PractitestTestCase), u'Practitest Test Case', min_entries=1)
  save_data = SubmitField(u'Save Data', render_kw={"class": "btn btn-primary"})
  create_run = SubmitField(u'Create File and Run', render_kw={"class": "btn btn-warning"})
  go_practitest = SubmitField(u'Check Summary To Practitest', render_kw={"class": "btn btn-info"})

  def __init__(self, pivotalData):
    super(PractitestFrom, self).__init__()

    # Rewrite value
    self.pivotal_id.value = pivotalData['pivotal_id']
    self.pivotal_title.value = pivotalData['title']
    self.pivotal_type.value = pivotalData['type'].title()
    self.pivotal_description.value = pivotalData['description']
    self.pivotal_status.value = pivotalData['status'].title()

    # Rewrite value practitest
    if pivotalData['practitest']:
      practitestData = pivotalData['practitest']
      self.practitest_id.value = practitestData['id']
      self.practitest_id.data = practitestData['id']
      self.practitest_status.value = practitestData['status']
      self.practitest_testing_phase.value = practitestData['test_phase']
      self.practitest_testing_level.value = practitestData['test_level']
      self.practitest_product_component.value = practitestData['product_component']
      self.practitest_os.value = practitestData['os']
      self.practitest_test_case.value = practitestData['test_case']
      self.practitest_release.value = practitestData['release']
      self.robot_type.value = practitestData['robot_type']

    # Rewrite value Libraries
    if pivotalData['test_library']:
      # Set library data (biar gampangin aja mangil variable).
      libraryData = pivotalData['test_library']
      self.practitest_testcase.min_entries = len(libraryData) + 1

      # Define iteration.
      iteration = 0
      for LibraryValue in reversed(libraryData):
        # Set Value.
        self.practitest_testcase.entries[iteration].form.testcase_id.value = LibraryValue['id']
        self.practitest_testcase.entries[iteration].form.testcase_id.data = LibraryValue['id']
        self.practitest_testcase.entries[iteration].form.testcase_title.value = LibraryValue['title']
        self.practitest_testcase.entries[iteration].form.testcase_gherkin.value = LibraryValue['gherkin']

        if len(self.practitest_testcase.entries) < self.practitest_testcase.min_entries:
          # Append new entry
          self.practitest_testcase.append_entry()

        # Set iteration.
        iteration = iteration + 1

# Create Practitest Form.
class PractitestRequestForm(FlaskForm):
  practitest_request = SubmitField(u'Send Data To Practitest (Create / Update)', render_kw={"class": "btn btn-primary"})
  commend_pivotal = SubmitField(u'Create Commennt To Pivotal', render_kw={"class": "btn btn-warning"})
  commend_pivotal_update = SubmitField(u'Create Commennt To Pivotal And Update Status', render_kw={"class": "btn btn-info"})

  def __init__(self):
    super(PractitestRequestForm, self).__init__()