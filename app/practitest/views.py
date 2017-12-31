# Import development class
from var_dump import var_dump

# Import important class.
from flask import Blueprint, render_template, abort, redirect, url_for, request
from jinja2 import TemplateNotFound
import xmltodict, json, os

# Import model
from app.pivotal.model import Pivotal as pivotalModel
from app.practitest.model import Steps, TestLibraries, Practitest, Instances

# Import actions
from app.pivotal.actions import PivotalAction
from app.practitest.actions import CreateRobotFile, RunFile, PractitestAction, PractitestRequest

# Import form
from app.practitest.form import PractitestFrom, PractitestRequestForm

# Create Blueprint.
practitest = Blueprint('practitest', __name__)

def renderForm(id):
  # Define action.
  pivotalAction = PivotalAction(pivotalModel)
  practitestAction = PractitestAction(Practitest)
  libraryAction = PractitestAction(TestLibraries)

  # Get Data.
  pivotalData = pivotalAction.findId(id)
  if pivotalData['status'] == False:
    return redirect(url_for('pivotal.pivotal_form', msg=pivotalData['message'], status='danger'))

  # Get Data practitest.
  practitestData = practitestAction.findByColumn('pivotals_id', '=', id)

  pivotalData['data']['practitest'] = {}
  pivotalData['data']['test_library'] = {}

  # Check status
  if practitestData['status'] == True:
    pivotalData['data']['practitest'] = practitestData['data']
    # Get Data Test Libraries.
    libraryData = libraryAction.findAllByColumn('pratitest_id', '=', practitestData['data']['id'])

    # Check status
    if libraryData['status'] == True:
      pivotalData['data']['test_library'] = libraryData['data']

  # Define variable form.
  form = PractitestFrom(pivotalData['data'])
  return form

def updateStatusTest(ouputdir, pivotal_id):
  f = open(ouputdir,"r")
  log = f.read()
  f.close()

  dic = xmltodict.parse(log)
  output = json.loads(json.dumps(dic))

  # Check variable type of test. (dict or list)
  outputTest = output['robot']['suite']['test']
  typeTest = type(outputTest).__name__
  arrayOutput = []

  if typeTest == 'list' :
    for robotTest in outputTest:
      testTemp = {}
      testTemp['status'] = robotTest['status']['@status']
      testTemp['step'] = []
      for robotStep in robotTest['kw']:
        stepTemp = {}
        stepStatus = robotStep['status']['@status']
        stepTemp['status'] = stepStatus
        stepTemp['msg'] = ''
        if stepStatus == 'FAIL':
          if 'kw' in robotStep:
            stepMsg = robotStep['kw']['msg']
            typeMsg = type(stepMsg).__name__
            if typeMsg == 'list' :
              lengMsg = len(stepMsg)
              stepTemp['msg'] = stepMsg[lengMsg-1]['#text']
            else :
              stepTemp['msg'] = stepMsg['#text']
          else :
            stepMsg = robotStep['msg']
            typeMsg = type(stepMsg).__name__
            if typeMsg == 'list' :
              lengMsg = len(robotStep['msg'])
              stepTemp['msg'] = stepMsg[lengMsg-1]['#text']
            else :
              stepTemp['msg'] = stepMsg['#text']
        testTemp['step'].append(stepTemp)
      arrayOutput.append(testTemp)
  else :
    testTemp = {}
    testTemp['status'] = outputTest['status']['@status']
    testTemp['step'] = []
    for robotStep in outputTest['kw']:
      stepTemp = {}
      stepStatus = robotStep['status']['@status']
      stepTemp['status'] = stepStatus
      stepTemp['msg'] = ''
      if stepStatus == 'FAIL':
        if 'kw' in robotStep:
          stepMsg = robotStep['kw']['msg']
          typeMsg = type(stepMsg).__name__
          if typeMsg == 'list' :
            lengMsg = len(stepMsg)
            stepTemp['msg'] = stepMsg[lengMsg-1]['#text']
          else :
            stepTemp['msg'] = stepMsg['msg']['#text']
        else :
          stepMsg = robotStep['msg']
          typeMsg = type(stepMsg).__name__
          if typeMsg == 'list' :
            lengMsg = len(robotStep['msg'])
            stepTemp['msg'] = robotStep['msg'][lengMsg-1]['#text']
          else :
            stepTemp['msg'] = robotStep['msg']['#text']
      testTemp['step'].append(stepTemp)
    arrayOutput.append(testTemp)

  # Get Practitest Data.
  practitestAction = PractitestAction(Practitest)
  practitestData = practitestAction.findByColumn('pivotals_id', '=', pivotal_id)

  # Get All Test Library.
  libraryAction = PractitestAction(TestLibraries)
  libraryData = libraryAction.findAllByColumn('pratitest_id', '=', practitestData['data']['id'])

  # Update practitest status
  practitestStatus = 'PASS'

  itLib = 0
  for library in reversed(libraryData['data']):
    if arrayOutput[itLib]['status'] == 'FAIL':
      practitestStatus = 'FAIL'

    updateLib = {
      'status' : arrayOutput[itLib]['status']
    }
    # Update status lib.
    resultLibrary = libraryAction.updateData(library['id'], updateLib)

    # Get All Step.
    stepAction = PractitestAction(Steps)
    stepGet = stepAction.findAllByColumn('test_library_id', '=', resultLibrary['data']['id'])

    itStep = 0
    for step in reversed(stepGet['data']):
      try:
        updateStep = {
          'status' : arrayOutput[itLib]['step'][itStep]['status'],
          'message' : arrayOutput[itLib]['step'][itStep]['msg'],
        }
        
        resultStep = stepAction.updateData(step['id'], updateStep)
      except Exception as e:
        updateStep = {
          'status' : 'No Run',
          'message' : '',
        }

        resultStep = stepAction.updateData(step['id'], updateStep)
      itStep = itStep + 1
    itLib = itLib + 1

  # Update practitest.
  dataPractitest = {
    'test_status' : practitestStatus
  }
  doUpdate = practitestAction.updateData(practitestData['data']['id'], dataPractitest)

  # os.remove(ouputdir)

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

  if 'status' in request.args:
    notif['status'] = request.args["status"]

  if 'msg' in request.args:
    notif['msg'] = request.args["msg"]

  # Define file directory.
  fileDir = 'app/practitest/testcase/api'

  # Define log file directory.
  logDir = 'app/practitest/logs/api/' + id + '.txt'

  # Create object run file.
  runFile = RunFile()

  # Define action.
  practitestAction = PractitestAction(Practitest)
  libraryAction = PractitestAction(TestLibraries)

  # Define variable form.
  form = renderForm(id)

  # Check if form is submitted and validated
  if form.validate_on_submit():
    # Get button value.
    save_button = form.save_data.data
    run_button = form.create_run.data
    go_practitest = form.go_practitest.data

    if save_button :
      # Logic for insert data to database.
      notif['status'] = 'success'
      notif['msg'] = 'Data Berhasil Dimasukan Ke dalam Databases'

      # Prepare data for table practitests.
      data = {
        'pivotals_id' : id,
        'status' : form.practitest_status.data,
        'test_phase': form.practitest_testing_phase.data,
        'test_level': form.practitest_testing_level.data,
        'product_component': form.practitest_product_component.data,
        'os': form.practitest_os.data,
        'test_case': form.practitest_test_case.data,
        'test_type': form.pivotal_type.value,
        'release': form.practitest_release.data,
        'robot_type': form.robot_type.data,
      }

      # Insert data to table practitest.
      try:
        if form.practitest_id.data != '':
          result = practitestAction.updateData(int(form.practitest_id.data), data)
        else:
          result = practitestAction.insertData(data)
      except Exception as e:
        notif['status'] = 'danger'
        notif['msg'] = 'Gagal dalam membuat record di tabel practitest, alasan : ' + str(e)
        return render_template('practitestForm.html', form=form, notif=notif)

      # Get data test.
      dataTestCase = form.practitest_testcase.data

      # Define action.
      stepAction = PractitestAction(Steps)

      # Make iteration.
      for testCase in dataTestCase:
        if testCase['testcase_title'] != '' and testCase['testcase_gherkin'] != '':
          practitestId = str(result['data']['id'])
          # Prepare data library.
          dataLibrary = {
            'pratitest_id': '15',
            'title': testCase['testcase_title'],
            'gherkin': testCase['testcase_gherkin'],
          }

          try:
            if testCase['testcase_id'] != '':
              resultLibrary = libraryAction.updateData(int(testCase['testcase_id']), dataLibrary)
              # Delet Step Data.
              stepDel = stepAction.deleteAllByColumn('test_library_id', '=', resultLibrary['data']['id'])
            else :
              resultLibrary = libraryAction.insertData(dataLibrary)
          except Exception as e:
            notif['status'] = 'danger'
            notif['msg'] = 'Gagal dalam membuat record di tabel test library, alasan : ' + str(e)
            return render_template('practitestForm.html', form=form, notif=notif)


          # Split Lines.
          splitlines = testCase['testcase_gherkin'].splitlines()

          # Iteration step.
          for step in splitlines:
            # Prepare data for steps.
            dataStep = {
              'test_library_id': str(resultLibrary['data']['id']),
              'steps': step,
            }

            try:
              resultSteps = stepAction.insertData(dataStep)
            except Exception as e:
              notif['status'] = 'danger'
              notif['msg'] = 'Gagal dalam membuat record di tabel steps, alasan : ' + str(e)
              return render_template('practitestForm.html', form=form, notif=notif)

      # Rerender Form.
      form = renderForm(id)

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

      # Update Database status
      updateStatusTest('output.xml', id)

    elif go_practitest :
      # Get data practitest.
      practitestData = practitestAction.findByColumn('pivotals_id', '=', id)

      if practitestData['status']:
        if practitestData['data']['test_status'] != 'No Run':
          return redirect(url_for('practitest.practitestSummary', id=id))
        else :
          notif['status'] = 'danger'
          notif['msg'] = 'Status Practitest : ' + practitestData['data']['test_status'] + ' Silahkan menjalankan robot file terlebih dahulu.'
      else :
        notif['msg'] = practitestData['message']
  try:
    notif['log'] = runFile.getLog(logDir)
  except Exception as e:
    pass

  # Try to load template.
  try:
    return render_template('practitestForm.html', form=form, notif=notif)
  except TemplateNotFound:
    abort(404)

# Define route for practitest blueprint.
@practitest.route('/summaryPractitest/<string:id>', methods=['GET', 'POST'])
# Function for this route.
def practitestSummary(id):
  # Define notif.
  notif = {
    'status' : 'danger',
    'msg' : '',
    'data' : {
      'id' : id
    },
  }

  info = {
    'pivotal' : [],
    'practitest' : [],
    'testlibrary' : [],
  }

  # Define action.
  pivotalAction = PivotalAction(pivotalModel)
  practitestAction = PractitestAction(Practitest)
  libraryAction = PractitestAction(TestLibraries)

  # Get Data.
  pivotalData = pivotalAction.findId(id)
  if pivotalData['status'] == False:
    return redirect(url_for('pivotal.pivotal_form', msg=pivotalData['message'], status='danger'))
  else :
    # Prepare data Summary Pivotal
    tempPivotal = {
      'title' : u'Pivotal ID',
      'value' : pivotalData['data']['pivotal_id'],
      'status' : '',
    }
    info['pivotal'].append(tempPivotal)
    tempPivotal = {
      'title' : u'Title',
      'value' : pivotalData['data']['title'],
      'status' : '',
    }
    info['pivotal'].append(tempPivotal)
    tempPivotal = {
      'title' : u'Description',
      'value' : pivotalData['data']['description'],
      'status' : '',
    }
    info['pivotal'].append(tempPivotal)
    tempPivotal = {
      'title' : u'Task Type',
      'value' : pivotalData['data']['type'].title(),
      'status' : '',
    }
    info['pivotal'].append(tempPivotal)
    tempPivotal = {
      'title' : u'Task Status',
      'value' : pivotalData['data']['status'],
      'status' : 'info',
    }
    if pivotalData['data']['status'] == 'accepted':
      tempPivotal['status'] = 'success'
    elif pivotalData['data']['status'] == 'rejected':
      tempPivotal['status'] = 'danger'
    info['pivotal'].append(tempPivotal)

  # Get Data Practitest.
  practitestData = practitestAction.findByColumn('pivotals_id', '=', id)
  if practitestData['status'] == False:
    return redirect(url_for('practitest.pratitest_form', msg=practitestData['message'], status='danger'))
  else :
    # Prepare data Summary Practitest
    tempPractitest = {
      'title' : u'Requirement ID',
      'value' : practitestData['data']['pratitest_req_id'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Test Set ID',
      'value' : practitestData['data']['pratitest_set_id'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Status',
      'value' : practitestData['data']['status'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Test Phase',
      'value' : practitestData['data']['test_phase'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Test Level',
      'value' : practitestData['data']['test_level'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Product Component',
      'value' : practitestData['data']['product_component'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'OS',
      'value' : practitestData['data']['os'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Test Case',
      'value' : practitestData['data']['test_case'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Test Type',
      'value' : practitestData['data']['test_type'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Release',
      'value' : practitestData['data']['release'],
      'status' : '',
    }
    info['practitest'].append(tempPractitest)
    tempPractitest = {
      'title' : u'Run Status',
      'value' : practitestData['data']['test_status'],
      'status' : 'info',
    }
    if practitestData['data']['test_status'] == 'PASS':
      tempPractitest['status'] = 'success'
    elif practitestData['data']['test_status'] == 'FAIL':
      tempPractitest['status'] = 'danger'
    info['practitest'].append(tempPractitest)

  # Get Data Test Libraries.
  libraryData = libraryAction.findAllByColumn('pratitest_id', '=', practitestData['data']['id'])
  if libraryData['status'] == False:
    return redirect(url_for('practitest.pratitest_form', msg=libraryData['message'], status='danger'))
  else :
    for value in reversed(libraryData['data']):
      # Prepare data Summary Test Library
      sumTestLibrary = {
        'title' : value['title'],
        'summary' : [],
        'step' : [],
      }

      tempSumTestLibrary = {
        'title' : u'Test Library ID',
        'value' : value['pratitest_lib_id'],
        'status' : '',
      }
      sumTestLibrary['summary'].append(tempSumTestLibrary)
      tempSumTestLibrary = {
        'title' : u'Test Status',
        'value' : value['status'],
        'status' : 'info',
      }
      if value['status'] == 'PASS':
        tempSumTestLibrary['status'] = 'success'
      elif value['status'] == 'FAIL':
        tempSumTestLibrary['status'] = 'danger'
      sumTestLibrary['summary'].append(tempSumTestLibrary)

      # Get All Step.
      stepAction = PractitestAction(Steps)
      stepGet = stepAction.findAllByColumn('test_library_id', '=', value['id'])

      for step in reversed(stepGet['data']):
        testStep = {
          'id' : step['id'],
          'step' : step['steps'],
          'status' : step['status'],
          'message' : step['message'],
          'style' : 'warning',
        }
        if step['status'] == 'PASS':
          testStep['style'] = 'success'
        elif step['status'] == 'FAIL':
          testStep['style'] = 'danger'
        sumTestLibrary['step'].append(testStep)

      # Append all data library and step.
      info['testlibrary'].append(sumTestLibrary)

  # Create Form
  form = PractitestRequestForm()

  # Check if form is submitted and validated
  if form.validate_on_submit():
    # Get button value.
    practitest_request = form.practitest_request.data
    commend_pivotal = form.commend_pivotal.data
    commend_pivotal_update = form.commend_pivotal_update.data

    if practitest_request :
      # Define test Id.
      testSetId = ''

      # Create Object PractitestRequest
      practitestReq = PractitestRequest(pivotalData['data'], practitestData['data'])

      # Check pratitest_set_id.
      if str(practitestData['data']['pratitest_set_id']) == 'None':
        # Create Practitest Data and update database.

        # Define testList.
        testIdList = []

        ## Create Test Library.
        for value in reversed(libraryData['data']):
          ### Looping test_library.
          stepAdd = practitestReq.createTestLibrary(value)

          ### Get id.
          if stepAdd['status'] == False:
            notif['status'] = 'danger'
            notif['msg'] = stepAdd['msg']
            return render_template('summaryPractitest.html', notif=notif, info=info, form=form)
          tempId = str(stepAdd['data']['id'])

          updateData = {
            'pratitest_lib_id' : tempId
          }

          ### Update id in test_library.
          updateData = libraryAction.updateData(value['id'], updateData)

          ### Append to array testList.
          testIdList.append(tempId)

        ## Create requrement.
        ### Use array testList.
        requirementAdd = practitestReq.createRequrement(testIdList)

        ### Get id.
        if requirementAdd['status'] == False:
          notif['status'] = 'danger'
          notif['msg'] = requirementAdd['msg']
          return render_template('summaryPractitest.html', notif=notif, info=info, form=form)

        ## Create Test Set.
        testSetAdd = practitestReq.createTestSet(testIdList)

        ### Get id.
        if testSetAdd['status'] == False:
          notif['status'] = 'danger'
          notif['msg'] = testSetAdd['msg']
          return render_template('summaryPractitest.html', notif=notif, info=info, form=form)

        ### Update to database.
        updateData = {
          'pratitest_req_id' : requirementAdd['data']['id'],
          'pratitest_set_id' : testSetAdd['data']['id'],
        }
        updateData = practitestAction.updateData(practitestData['data']['id'], updateData)

        testSetId = testSetAdd['data']['id']
      else :
        # Set Test Set Id.
        testSetId = practitestData['data']['pratitest_set_id']

      ## Do Run.
      ## Get Instance id.
      instanceGet = practitestReq.getInstances(testSetId)
      ### Get id.
      if instanceGet['status'] == False:
        notif['status'] = 'danger'
        notif['msg'] = instanceGet['msg']
        return render_template('summaryPractitest.html', notif=notif, info=info, form=form)
      ### Iteration instance id.
      for value in instanceGet['data']:
        #### Get library id according to test id (pratitest_lib_id).
        libraryData = libraryAction.findByColumn('pratitest_lib_id', '=', value['attributes']['test-id'])

        #### Iteration All Step.
        stepData = stepAction.findAllByColumn('test_library_id', '=', libraryData['data']['id'])

        #### Define array step.
        arrayStep = []

        #### Prepare Steps.
        for step in reversed(stepGet['data']):
          testStep = {
            'name' : step['steps'],
            'expected-results' : step['steps'],
            'status' : 'NO RUN'
          }

          if step['status'] == 'PASS':
            testStep['actual-results'] = step['steps']
            testStep['status'] = 'PASSED'
          elif step['status'] == 'FAIL':
            testStep['actual-results'] = step['message']
            testStep['status'] = 'FAILED'
          arrayStep.append(testStep)

        #### Request Run.
        runTest = practitestReq.runStep(value['id'], arrayStep)

      # Reload this page.
      return redirect(url_for('practitest.practitestSummary', id=id))
    elif commend_pivotal :
      # Create Pivotal Action
      commentPivotalAction = PivotalAction(pivotalModel)
      practitestAction = PractitestAction(Practitest)

      # Get data pivotal.
      pivotalData = pivotalAction.findId(id)
      if pivotalData['status'] == False:
        return redirect(url_for('pivotal.pivotal_form', msg=pivotalData['message'], status='danger'))

      # Get Data practitest.
      practitestData = practitestAction.findByColumn('pivotals_id', '=', id)

      # Test Comment.
      commentPivotal = commentPivotalAction.sendCommentPivotal(pivotalData['data']['pivotal_id'], practitestData['data'])

      if commentPivotal['status'] == False:
        notif['msg'] = commentPivotal['message']

      notif['status'] = 'success'
      notif['msg'] = 'Comment berhasil ditambahkan'
    elif commend_pivotal_update : 
      # Create Pivotal Action
      commentPivotalAction = PivotalAction(pivotalModel)
      practitestAction = PractitestAction(Practitest)

      # Get data pivotal.
      pivotalData = pivotalAction.findId(id)
      if pivotalData['status'] == False:
        return redirect(url_for('pivotal.pivotal_form', msg=pivotalData['message'], status='danger'))

      # Get Data practitest.
      practitestData = practitestAction.findByColumn('pivotals_id', '=', id)

      # Test Comment.
      commentPivotal = commentPivotalAction.sendCommentPivotal(pivotalData['data']['pivotal_id'], practitestData['data'], True)

      notif['status'] = 'success'
      notif['msg'] = 'Comment berhasil ditambahkan dan status pivotal berhasil di ubah'

      if commentPivotal['status'] == False:
        notif['status'] = 'danger'
        notif['msg'] = commentPivotal['message']


  # Try to load template.
  try:
    return render_template('summaryPractitest.html', notif=notif, info=info, form=form)
  except TemplateNotFound:
    abort(404)

