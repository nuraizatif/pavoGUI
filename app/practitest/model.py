from app.model import CrudBase

class Steps(CrudBase):
  __table__ = 'steps'
  __primary_key__ = 'id'
  __incrementing__  = True
  __columns__ = [ 'id', 'test_library_id', 'steps', 'status', 'message']
  __fillable__ = ['test_library_id', 'steps', 'status', 'message']

  __searchable__ = [ 'id', 'test_library_id', 'steps', 'status', 'message']

  srcRawQry = ""
  srcQryBind = []
  addNewSchema = {
    'test_library_id': { 'type': 'string', 'required': True },
    'steps': { 'type': 'string', 'required': True },
    'status': { 'type': 'string', 'required': True },
    'message': { 'type': 'string', 'required': False }
  }
  updateSchema = {
    'test_library_id': { 'type': 'string', 'required': True },
    'steps': { 'type': 'string', 'required': True },
    'status': { 'type': 'string', 'required': True },
    'message': { 'type': 'string', 'required': False }
  }

  def __init__(self):
    CrudBase.__init__(self)

class TestLibraries(CrudBase):
  __table__ = 'test_libraries'
  __primary_key__ = 'id'
  __incrementing__  = True
  __columns__ = [ 'id', 'pratitest_lib_id', 'pratitest_id', 'title', 'gherkin', 'status']
  __fillable__ = ['pratitest_lib_id', 'pratitest_id', 'title', 'gherkin', 'status']

  __searchable__ = [ 'id', 'pratitest_lib_id', 'pratitest_id', 'title', 'gherkin', 'status']

  srcRawQry = ""
  srcQryBind = []
  addNewSchema = {
    'pratitest_lib_id': { 'type': 'string', 'required': False },
    'pratitest_id': { 'type': 'string', 'required': True },
    'title': { 'type': 'string', 'required': True },
    'gherkin': { 'type': 'string', 'required': True },
    'status': { 'type': 'string', 'required': True },
  }
  updateSchema = {
    'pratitest_lib_id': { 'type': 'string', 'required': False },
    'pratitest_id': { 'type': 'string', 'required': True },
    'title': { 'type': 'string', 'required': True },
    'gherkin': { 'type': 'string', 'required': True },
    'status': { 'type': 'string', 'required': True },
  }

  def __init__(self):
    CrudBase.__init__(self)

class Practitest(CrudBase):
  __table__ = 'practitest'
  __primary_key__ = 'id'
  __incrementing__  = True
  __columns__ = [
    'id',
    'pratitest_req_id',
    'pratitest_set_id',
    'pivotals_id',
    'status',
    'test_phase',
    'test_level',
    'product_component',
    'os',
    'test_case',
    'test_type',
    'release',
    'test_status'
  ]
  __fillable__ = [
    'pratitest_req_id',
    'pratitest_set_id',
    'pivotals_id',
    'status',
    'test_phase',
    'test_level',
    'product_component',
    'os',
    'test_case',
    'test_type',
    'release',
    'test_status'
  ]

  __searchable__ = [
    'id',
    'pratitest_req_id',
    'pratitest_set_id',
    'pivotals_id',
    'status',
    'test_phase',
    'test_level',
    'product_component',
    'os',
    'test_case',
    'test_type',
    'release',
    'test_status'
  ]

  srcRawQry = ""
  srcQryBind = []
  addNewSchema = {
    'pratitest_req_id': { 'type': 'string', 'required': False },
    'pratitest_set_id': { 'type': 'string', 'required': False },
    'pivotals_id': { 'type': 'string', 'required': True },
    'status': { 'type': 'string', 'required': True },
    'test_phase': { 'type': 'string', 'required': True },
    'test_level': { 'type': 'string', 'required': True },
    'product_component': { 'type': 'string', 'required': True },
    'os': { 'type': 'string', 'required': True },
    'test_case': { 'type': 'string', 'required': True },
    'test_type': { 'type': 'string', 'required': True },
    'release': { 'type': 'string', 'required': True },
    'test_status': { 'type': 'string', 'required': True }
  }
  updateSchema = {
    'pratitest_req_id': { 'type': 'string', 'required': False },
    'pratitest_set_id': { 'type': 'string', 'required': False },
    'pivotals_id': { 'type': 'string', 'required': True },
    'status': { 'type': 'string', 'required': True },
    'test_phase': { 'type': 'string', 'required': True },
    'test_level': { 'type': 'string', 'required': True },
    'product_component': { 'type': 'string', 'required': True },
    'os': { 'type': 'string', 'required': True },
    'test_case': { 'type': 'string', 'required': True },
    'test_type': { 'type': 'string', 'required': True },
    'release': { 'type': 'string', 'required': True },
    'test_status': { 'type': 'string', 'required': True }
  }

  def __init__(self):
    CrudBase.__init__(self)

class Instances(CrudBase):
  __table__ = 'instances'
  __primary_key__ = 'id'
  __incrementing__  = True
  __columns__ = [ 'id', 'pratitest_set_id', 'pratitest_lib_id', 'status']
  __fillable__ = ['pratitest_set_id', 'pratitest_lib_id', 'status']

  __searchable__ = [ 'id', 'pratitest_set_id', 'pratitest_lib_id', 'status']

  srcRawQry = ""
  srcQryBind = []
  addNewSchema = {
    'pratitest_set_id': { 'type': 'string', 'required': True },
    'pratitest_lib_id': { 'type': 'string', 'required': True },
    'status': { 'type': 'string', 'required': True }
  }
  updateSchema = {
    'pratitest_set_id': { 'type': 'string', 'required': True },
    'pratitest_lib_id': { 'type': 'string', 'required': True },
    'status': { 'type': 'string', 'required': True }
  }

  def __init__(self):
    CrudBase.__init__(self)
