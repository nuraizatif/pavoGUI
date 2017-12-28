# Import development class
from var_dump import var_dump

# Import parent
from app import app, view

# Import subprocess.
import subprocess

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
