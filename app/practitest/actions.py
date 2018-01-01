# Import development class
from var_dump import var_dump

# Import parent
from app import app, view

# Import subprocess, request
import subprocess
import requests
import json

class CreateRobotFile():
  """docstring for ClassName"""
  def __init__(self):
    # Set default value for Settings and Test Cases
    self.settings = '*** Settings ***\r\n'
    self.steps = '*** Test Cases ***\r\n'

  # Function to create space in file.
  def space(self, count):
    space = ''
    for x in iter(range(count)):
      space = space + ' '
    return space

  # Build unit settings.
  def unitSettings(self, type, value):
    self.settings = self.settings + type + self.space(5) + value + '\r\n'

  # Build default settings.
  def createDefaultSettings(self, testingType = 'api'):
    # Api settings.
    if testingType == 'api':
      self.unitSettings('Library', 'Collections')
      self.unitSettings('Library', 'RequestsLibrary')
      self.unitSettings('Resource', '../../keyword/api.robot')
    elif testingType == 'web':
      self.unitSettings('Resource', '../../keyword/web.robot')
      self.unitSettings('Suite Setup', 'Connect Database')
      self.unitSettings('Suite Teardown', 'Disconnect Database')
      pass

  # Return settings.
  def getSettings(self):
    return self.settings

  # Build Unit Step.
  def unitStep(self, step):
    self.steps = self.steps + self.space(5) + step + '\r\n'

  # Create complete step with title and steps.
  def craeteSteps(self, title, steps):
    self.steps = self.steps + title + '\r\n'
    for step in steps:
      self.unitStep(step)

  # Get all steps.
  def getSteps(self):
    return self.steps

  # Create File Robot.
  def createFile(self, fileName, fileDir = ''):
    fileContent = self.settings + '\r\n' + self.steps
    fileUrl = fileName + '.robot'
    if fileDir :
      fileUrl = fileDir + '/' + fileName + '.robot'
    with open(fileUrl, 'w+') as f:
      f.write(fileContent)
      f.close()

class RunFile():
  """docstring for runFile"""
  def __init__(self):
    super(RunFile, self).__init__()

  # Run file.
  def run(self, logDir, robotDir):
    process = subprocess.Popen(['robot ' + robotDir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    with open(logDir, 'w+') as f:
      f.write('Log for robotframework running : \r\n')
      f.write('OUPUT : \r\n')
      f.write(out.decode('utf-8') + '\r\n')
      if err:
        f.write('Error : \r\n')
        f.write(err.decode('utf-8') + '\r\n')
      f.close()

  def getLog(self, logDir):
    f = open(logDir,"r")
    log = f.read()
    f.close()
    return log

class PractitestAction(view.BaseCrud):
  """docstring for PractitestAction"""
  def __init__(self, Model):
    super(PractitestAction, self).__init__(Model)

  def findId(self, id):
    # Find data in database.
    result = self.get(id)
    return result

  def findByColumn(self, column, op, value):
    # Find data in database.
    result = self.getByColoumn(column, op, value)
    return result

  def findAllByColumn(self, column, op, value):
    # Find data in database.
    result = self.getAllByColoumn(column, op, value)
    return result

  def deleteAllByColumn(self, column, op, value):
    result = self.delAllByColoumn(column, op, value)
    return result

  def insertData(self, data):
    # Insert data.
    result = self.post(data)
    return result

  def updateData(self, id, data):
    # Insert data.
    result = self.put(id, data)
    return result

  def deleteData(self, id):
    # Insert data.
    result = self.delete(id)
    return result

class PractitestRequest():
  """docstring for PractitestRequest"""
  def __init__(self, dataPivotal, dataPracitest):
    ## Set dataPivotal.
    self.dataPivotal = dataPivotal
    ## Set dataPractitest.
    self.dataPractitest = dataPracitest
    ## Set Mail Url.
    self.mainUrl = app.config['PRACTITEST_API_URL'] + '/projects/' + app.config['PRACTITEST_PROJECT_ID']
    ## Set Auth.
    self.auth = (app.config['PRACTITEST_USER'], app.config['PRACTITEST_USER_TOKEN'])
    ## Set Header.
    self.header = {
      'Content-Type': 'application/json'
    }
    ## Set Default return.
    self.returnData = {
      'status' : False,
      'msg' : '',
      'data' : ''
    }

  def createTestLibrary(self, data = {}):
    """
    Example input :
    {
      "data": {
        "type": "tests",
        "attributes": {
          "name": "Test Aizat",
          "description": "Test Aizat",
          "author-id": 8933,
          "status": "Ready", # status
          "custom-fields": {
            "---f-20267": "Unit", # test_phase
            "---f-20269": "Sanity", # test_phase_level
            "---f-20270": "Application System", # product_component
            "---f-20272": "Mac", # OS
            "---f-20289": "Positive", # test_case
            "---f-20290": "Feature"# test_type
          },
        },
        "steps": {
          "data": [
            {
              "name": "step one",
              "description": "Step 1 description",
              "expected-results": "result"
            },
            {
              "name": "step two",
              "expected-results": "result2"
            }
          ]
        }
      }
    }

    Output : tests id for createRequrement, createTestSet
    [112345, 567890]
    """
    # Define steps.
    steps = []

    arrayStep = data['gherkin'].splitlines()

    # looping Split line.
    for stepVal in arrayStep:
      tempStep = {
        "name": stepVal,
        "expected-results": stepVal
      }
      steps.append(tempStep)

    # Define Data.
    data = {
      "data": {
        "type": "tests",
        "attributes": {
          "name": data['title'],
          "description": self.dataPivotal['description'] + '\r\n with pivotal id : ' + self.dataPivotal['pivotal_id'],
          "author-id": 8933,
          "status": self.dataPractitest['status'], # status
          "custom-fields": {
            "---f-20267": self.dataPractitest['test_phase'], # test_phase
            "---f-20269": self.dataPractitest['test_level'], # test_level
            "---f-20270": self.dataPractitest['product_component'], # product_component
            "---f-20272": self.dataPractitest['os'], # OS
            "---f-20289": self.dataPractitest['test_case'], # test_case
            "---f-20290": self.dataPractitest['test_type']# test_type
          },
        },
        "steps": {
          "data": steps
        }
      }
    }

    dataText = json.dumps(data)

    # Define URL.
    url = self.mainUrl + '/tests.json'
    res = requests.post(
      url,
      auth=self.auth,
      data=dataText,
      headers=self.header
    )

    # Get response.
    jsonData = res.json()

    # Check valid response.
    if res.status_code == 200 and 'data' in jsonData:
      self.returnData['status'] = True
      self.returnData['msg'] = ''
      self.returnData['data'] = jsonData['data']
    else :
      # Set Default msg.
      self.returnData['msg'] = 'POST Request Practitest (Test Library) Gagal'
      # Set error msg from response.
      if 'errors' in jsonData:
        self.returnData['msg'] = jsonData['errors'][0]['title']
      # Set data.
      self.returnData['data'] = jsonData
    
    return self.returnData

  def createRequrement(self, testId):
    """
    Example input :
    {
      "data": {
        "type": "requirements",
        "attributes": {
          "name": "test Aizat",
          "author-id": 8933,
          "custom-fields": {
            "---f-20270": "Application System",
            "---f-20290": "Feature",
            "---f-20313": "i20171101"
          },
        },
        "traceability": {
          "test-ids": [
            32222,
            53333
          ]
        }
      }
    }

    Output : reqirement id for insert to database.
    1234151
    """
    # Define Data.
    data ={
      "data": {
        "type": "requirements",
        "attributes": {
          "name": self.dataPivotal['title'],
          "description": self.dataPivotal['description'] + '\r\n with pivotal id : ' + self.dataPivotal['pivotal_id'],
          "author-id": 8933,
          "custom-fields": {
            "---f-20270": self.dataPractitest['product_component'], # product_component
            "---f-20290": self.dataPractitest['test_type'], # test_type
            "---f-20313": self.dataPractitest['release'] # release
          },
        },
        "traceability": {
          "test-ids": testId
        }
      }
    }

    dataText = json.dumps(data)

    # Define URL.
    url = self.mainUrl + '/requirements.json'
    res = requests.post(
      url,
      auth=self.auth,
      data=dataText,
      headers=self.header
    )

    # Get response.
    jsonData = res.json()

    # Check valid response.
    if res.status_code == 200 and 'data' in jsonData:
      self.returnData['status'] = True
      self.returnData['msg'] = ''
      self.returnData['data'] = jsonData['data']
    else :
      # Set Default msg.
      self.returnData['msg'] = 'POST Request Practitest (Requirement) Gagal'
      # Set error msg from response.
      if 'errors' in jsonData:
        self.returnData['msg'] = jsonData['errors'][0]['title']
      # Set data.
      self.returnData['data'] = jsonData
    
    return self.returnData

  def createTestSet(self, testId):
    """
    Example input = {
      "data": {
        "type": "sets",
        "attributes": {
          "name": "one",
          "custom-fields": {
            "---f-20267": "Unit",
            "---f-20268": "Chrome",
            "---f-20269": "Sanity",
            "---f-20270": "Application System",
            "---f-20271": "Staging (UAT)",
            "---f-20274": "Topup Pulsa",
            "---f-20289": "Positive",
            "---f-20313": "20171207"
          },
        },
        "instances": {
          "test-ids": [
            32222,
            53333
          ]
        }
      }
    }

    Output : test set id for insert to database.
    1234151
    """
    # Define Data.
    data ={
      "data": {
        "type": "sets",
        "attributes": {
          "name": self.dataPivotal['title'],
          "custom-fields": {
            "---f-20267": self.dataPractitest['test_phase'], # test_phase
            "---f-20269": self.dataPractitest['test_level'], # test_level
            "---f-20270": self.dataPractitest['product_component'], # product_component
            "---f-20272": self.dataPractitest['os'], # OS
            "---f-20289": self.dataPractitest['test_case'], # test_case
            "---f-20290": self.dataPractitest['test_type'], # test_type
            "---f-20313": self.dataPractitest['release'] # release
          },
        },
        "instances": {
          "test-ids": testId
        }
      }
    }

    dataText = json.dumps(data)

    # Define URL.
    url = self.mainUrl + '/sets.json'
    res = requests.post(
      url,
      auth=self.auth,
      data=dataText,
      headers=self.header
    )

    # Get response.
    jsonData = res.json()

    # Check valid response.
    if res.status_code == 200 and 'data' in jsonData:
      self.returnData['status'] = True
      self.returnData['msg'] = ''
      self.returnData['data'] = jsonData['data']
    else :
      # Set Default msg.
      self.returnData['msg'] = 'POST Request Practitest (Test Set) Gagal'
      # Set error msg from response.
      if 'errors' in jsonData:
        self.returnData['msg'] = jsonData['errors'][0]['title']
      # Set data.
      self.returnData['data'] = jsonData
    
    return self.returnData

  def getInstances(self, setId):
    # Define URL.
    url = self.mainUrl + '/instances.json' + '?set-ids=' + setId
    res = requests.get(
      url,
      auth=self.auth,
      headers=self.header
    )

    # Get response.
    jsonData = res.json()

    # Check valid response.
    if res.status_code == 200 and 'data' in jsonData:
      self.returnData['status'] = True
      self.returnData['msg'] = ''
      self.returnData['data'] = jsonData['data']
    else :
      # Set Default msg.
      self.returnData['msg'] = 'Get Request Practitest (Instances) Gagal'
      # Set error msg from response.
      if 'errors' in jsonData:
        self.returnData['msg'] = jsonData['errors'][0]['title']
      # Set data.
      self.returnData['data'] = jsonData
    
    return self.returnData

  def runStep(self, instanceId, steps):
    """
    Example Input :
    {
      "data": {
        "type": "instances",
        "attributes": {
          "instance-id": 98142
        },
        "steps": {
          "data": [
            {
              "name": "step one",
              "expected-results": "result",
              "status": "FAILED"
            },
            {
              "name": "step two",
              "expected-results": "result2",
              "status": "PASSED"
            }
          ]
        }
      }
    }
    """
    # Define data
    data = {
      "data": {
        "type": "instances",
        "attributes": {
          "instance-id": instanceId
        },
        "steps": {
          "data": steps
        }
      }
    }

    dataText = json.dumps(data)

    # Define URL.
    url = self.mainUrl + '/runs.json'
    res = requests.post(
      url,
      auth=self.auth,
      data=dataText,
      headers=self.header
    )

    # Get response.
    jsonData = res.json()

    # Check valid response.
    if res.status_code == 200 and 'data' in jsonData:
      self.returnData['status'] = True
      self.returnData['msg'] = ''
      self.returnData['data'] = jsonData['data']
    else :
      # Set Default msg.
      self.returnData['msg'] = 'POST Request Practitest (Run) Gagal'
      # Set error msg from response.
      if 'errors' in jsonData:
        self.returnData['msg'] = jsonData['errors'][0]['title']
      # Set data.
      self.returnData['data'] = jsonData
    
    return self.returnData