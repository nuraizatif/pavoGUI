import logging, json, var_dump

from flask import request

from app.validator import MyValidator

class BaseCrud():
  """Base CRUD View

  Handling view for Get By Id, Add New, Update, Delete
  """
  def __init__(self, Model):
    self.Orm = Model
    self.response = {
      'status' : False,
      'message' : ''
    }

  def get(self, id=None):
    result = self.Orm.getById(id)
    if result != None:
      self.response['status'] = True
      self.response['data'] = result.serialize()
    else:
      self.response['message'] = u'Data Tidak Ditemukan'
      return self.response
    return self.response

  def post(self, data):
    args = data
    validator = MyValidator()
    dovalidate = validator.wrp_validate(args, self.Orm.addNewSchema)
    if(dovalidate['status']==False):
      self.response['message'] = dovalidate['messages']
      return self.response
    else :
      result = self.Orm.addNew(args)
      self.response['status'] = True
      self.response['data'] = result.serialize()
    return self.response

  def put(self, id, data):
    args = data
    validator = MyValidator()
    dovalidate = validator.wrp_validate(args, self.Orm.updateSchema)
    if(dovalidate['status']==False):
      return self.my_response(valid_status=False, code=422, messages=dovalidate['messages'])
    result = self.Orm.doUpdate(id, args)
    return self.my_response(data=result.serialize())

  def delete(self, id):
    me = self.Orm.find(id)
    if me!=None:
      me.delete()
      return 'Deleted'
    else:
      return 'Data not found.'