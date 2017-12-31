# Import parent
from app import app, view

class ElementWebAction(view.BaseCrud):
  """docstring for ElementWebActions"""
  def __init__(self, Model):
    super(ElementWebAction, self).__init__(Model)

  def findId(self, id):
    # Find data in database.
    result = self.get(id)
    return result

  def findAll(self):
    # Find data in database.
    result = self.getAll()
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