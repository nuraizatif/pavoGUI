# Import Request, ast
import requests, ast

# Import model
from app.pivotal.model import Pivotal as pivotalModel

# Import parent
from app import app, view

class PivotalAction(view.BaseCrud):
  """docstring for PivotalAction"""
  def __init__(self, Model):
    super(PivotalAction, self).__init__(Model)

  def findId(self, id):
    # Find data in database.
    result = self.get(id)
    return result

  def findByPivotalID(self, pivotal_id):
    # Find data in database.
    result = self.getByColoumn('pivotal_id', '=', pivotal_id)
    return result

  def getDataPivotal(self, pivotal_id):
    # Find data in Pivotal use Pivotal API.
    ## Define URL.
    url = str(app.config['PIVOTAL_API_URL']) + '/projects/' + str(app.config['PIVOTAL_PRONGHORN_PROJECT_ID']) + '/stories/' + str(pivotal_id)
    ## Define header.
    headers = {
      'X-TrackerToken': str(app.config['PIVOTAL_USER_TOKEN'])
    }
    # Request to url.
    r = requests.get(url, headers=headers)
    # Get data json.
    json_data = r.json()
    # Check error.
    if json_data['kind'] == 'error' and json_data['error']:
      self.response['message'] = json_data['error']
    else :
      self.response['status'] = True
      self.response['message'] = u'Data Ditemukan.'
      self.response['data'] = json_data
    return self.response

  def updatePivotal(self, pivotal_id):
    # Request New Data.
    new_result = self.getDataPivotal(pivotal_id)
    # Check status.
    if new_result['status'] == True:
      # Prepare Data to update.
      data ={
        'pivotal_id': str(new_result['data']['id']),
        'title': new_result['data']['name'],
        'type': new_result['data']['story_type'],
        'status': new_result['data']['current_state'],
        'json_data': str(new_result['data'])
      }
      if 'description' in new_result['data']:
        data['description'] = new_result['data']['description']

      # Get Current ID.
      dataDatabase = self.findByPivotalID(new_result['data']['id'])

      # Update data.
      self.response = self.updateData(dataDatabase['data']['id'], data)
    return self.response
    

  def insertData(self, data):
    # Insert data.
    result = self.post(data)
    return result

  def updateData(self, id, data):
    # Insert data.
    result = self.put(id, data)
    return result

  def parsingData(self, data):
    data['type'] = data['type'].title()
    data['status'] = data['status'].title()
    data['updated_at'] = data['updated_at'].replace('T', ' ')
    dict_data = ast.literal_eval(data['json_data'])
    data['url'] = dict_data['url']
    data['url_to_practitest'] = request.base_url + '/practitest/' + str(data['id'])
    return data
