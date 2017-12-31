from app.model import CrudBase

class Elementweb(CrudBase):
  __table__ = 'element_web'
  __primary_key__ = 'id'
  __incrementing__  = True
  __columns__ = [ 'id', 'name', 'type', 'value']
  __fillable__ = ['name', 'type', 'value']

  __searchable__ = [ 'id', 'name', 'type', 'value']

  srcRawQry = ""
  srcQryBind = []
  addNewSchema = {
    'name': { 'type': 'string', 'required': True },
    'type': { 'type': 'string', 'required': True },
    'value': { 'type': 'string', 'required': True }
  }
  updateSchema = {
    'name': { 'type': 'string', 'required': False },
    'type': { 'type': 'string', 'required': False },
    'value': { 'type': 'string', 'required': False }
  }

  def __init__(self):
    CrudBase.__init__(self)