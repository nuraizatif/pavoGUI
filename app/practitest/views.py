# Import development class
from var_dump import var_dump

# Import important class.
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# Import model
from app.pivotal.model import Pivotal as pivotalModel

# Import actions
from app.pivotal.actions import PivotalAction
from app.practitest.actions import CreateRobotFile, RunFile 

# Import form
from app.practitest.form import PractitestFrom

# Create Blueprint.
practitest = Blueprint('practitest', __name__)

# Define route for practitest blueprint.
@practitest.route('/practitestForm/<string:id>', methods=['GET', 'POST'])
# Function for this route.
def pratitest_form(id):
  # Define notif.
  notif = {
    'status' : 'danger',
    'msg' : '',
    'data' : {
      'id' : id
    },
    'log' : ''
  }

  # Define file directory.
  fileDir = 'app/practitest/testcase/api'

  # Define log file directory.
  logDir = 'app/practitest/logs/api/' + id + '.txt'

  # Create object run file.
  runFile = RunFile()

  # Define action.
  pivotalAction = PivotalAction(pivotalModel)

  # Get Data.
  pivotalData = pivotalAction.findId(id)

  # Define variable form.
  form = PractitestFrom(pivotalData['data'])

  # Check if form is submitted and validated
  if form.validate_on_submit():
    # Get button value.
    save_button = form.save_data.data
    run_button = form.create_run.data

    if save_button :
      # Logic for insert data to database.
      notif['status'] = 'success'
      notif['msg'] = 'Data Berhasil Dimasukan Ke dalam Databases'

      # Prepare data for table practitests
      data = {
        'pivotals_id' : id,
        'status' : form.practitest_status.data,
        'test_phase': form.practitest_testing_phase.data,
        'test_level': form.practitest_testing_level.data,
        'product_component': form.practitest_product_component.data,
        'os': form.practitest_os.data,
        'test_case': form.practitest_test_case.data,
        'test_type': form.pivotal_type.data.title(),
        'release': form.practitest_release.data,
      }

    elif run_button :
      # Logic for create file robot and run it
      notif['status'] = 'success'
      notif['msg'] = 'Run File, Check log di area paling bawah'

      # Get data test.
      dataTestCase = form.practitest_testcase.data

      # Create Object File.
      fileRobot = CreateRobotFile()

      # Get type robot.
      robotType = form.robot_type.data

      # Set Default Settings.
      fileRobot.createDefaultSettings(robotType)

      # Make iteration.
      for testCase in dataTestCase:
        # Split Lines.
        splitlines = testCase['testcase_gherkin'].splitlines()

        # Create Steps.
        fileRobot.craeteSteps(testCase['testcase_title'], splitlines)

      try:
        # Create File robot.
        fileRobot.createFile(id, fileDir)
      except Exception as e:
        notif['status'] = 'danger'
        notif['msg'] = 'Gagal dalam membuat file, alasan : ' + str(e)
        return render_template('practitestForm.html', form=form, notif=notif)

      try:
        runFile.run(logDir, fileDir + '/' + id + '.robot')
      except Exception as e:
        notif['status'] = 'danger'
        notif['msg'] = 'Gagal dalam menjalankan file, alasan : ' + str(e)
        return render_template('practitestForm.html', form=form, notif=notif)

  try:
    notif['log'] = runFile.getLog(logDir)
  except Exception as e:
    pass

  # Try to load template.
  try:
    return render_template('practitestForm.html', form=form, notif=notif)
  except TemplateNotFound:
    abort(404)