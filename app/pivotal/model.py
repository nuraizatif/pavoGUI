from app.model import CrudBase, AuthenticableBase

class Pivotal(CrudBase, AuthenticableBase):
	__table__ = 'pivotals'
	__primary_key__ = 'id'
	__incrementing__  = False
	__columns__ = [ 'pivotal_id', 'title', 'type', 'description', 'status', 'json_data' ]
	__fillable__ = [ 'pivotal_id', 'title', 'type', 'description', 'status', 'json_data' ]

	__searchable__ = [ 'pivotal_id', 'title', 'type', 'description', 'status', 'json_data' ]

	srcRawQry = ""
	srcQryBind = []
	addNewSchema = {
		'pivotal_id': { 'type': 'string', 'required': True },
		'title': { 'type': 'string', 'required': True },
		'type': { 'type': 'string', 'required': True },
		'description': { 'type': 'string', 'required': True },
		'status': { 'type': 'string', 'required': True },
		'json_data': { 'type': 'string', 'required': True }
	}
	updateSchema = {
		'pivotal_id': { 'type': 'string', 'required': True },
		'title': { 'type': 'string', 'required': True },
		'type': { 'type': 'string', 'required': True },
		'description': { 'type': 'string', 'required': True },
		'status': { 'type': 'string', 'required': True },
		'json_data': { 'type': 'string', 'required': True }
	}

	def __init__(self):
		CrudBase.__init__(self)
	
