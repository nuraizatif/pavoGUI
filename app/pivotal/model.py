from app.model import CrudBase

class Pivotal(CrudBase):
  __table__ = 'pivotals'
  __primary_key__ = 'id'
  __incrementing__  = True
  __columns__ = [ 'id', 'pivotal_id', 'title', 'type', 'description', 'status', 'json_data' ]
  __fillable__ = ['pivotal_id', 'title', 'type', 'description', 'status', 'json_data' ]

  __searchable__ = [ 'id', 'pivotal_id', 'title', 'type', 'description', 'status', 'json_data' ]

  srcRawQry = ""
  srcQryBind = []
  addNewSchema = {
    'pivotal_id': { 'type': 'string', 'required': True },
    'title': { 'type': 'string', 'required': True },
    'type': { 'type': 'string', 'required': True },
    'description': { 'type': 'string', 'required': False },
    'status': { 'type': 'string', 'required': True },
    'json_data': { 'type': 'string', 'required': True }
  }
  updateSchema = {
    'pivotal_id': { 'type': 'string', 'required': True },
    'title': { 'type': 'string', 'required': True },
    'type': { 'type': 'string', 'required': True },
    'description': { 'type': 'string', 'required': False },
    'status': { 'type': 'string', 'required': True },
    'json_data': { 'type': 'string', 'required': True }
  }

  def __init__(self):
    CrudBase.__init__(self)