import logging, hashlib
from var_dump import var_dump

from app import db, config
from orator import Model, Schema
# from app.exceptions import InvalidResponseException

db.connection().enable_query_log()

Model.set_connection_resolver(db)
schema = Schema(db)

class CrudBase(Model):

  __searchable__ = []
  
  srcRawQry = ''
  srcQryBind = []

  @classmethod
  def setSrcRawQry(self, strSearch):
    self.srcRawQry = ''
    self.srcQryBind = []
    if len(self.__searchable__):
      for col in self.__searchable__:
        self.srcRawQry += "`%s` LIKE %s OR " % (col, '%s')
        self.srcQryBind.append("%"+strSearch+"%")
      self.srcRawQry = self.srcRawQry.rstrip(" OR ")
      self.srcRawQry = "(%s)" % self.srcRawQry

  @classmethod
  def getList(self, recPerPage=25, search=None, filter={}, page=1, order={}, rfilter={}):
    me = self
    table = me.__table__

    if recPerPage==None:
      recPerPage = int(config.Config.APP_RECPERPAGE)

    # Search
    if search != None and search != '':
      self.setSrcRawQry(search)
      me = me.where_raw(self.srcRawQry, self.srcQryBind)

    # Filter
    if len(filter):
      for k, v in filter.items():
        if schema.has_column(table, k) and (v != None and v != ''):
          me = me.where(k, v)
    
    # Ranges Filter
    if len(rfilter):
      for k, v in rfilter.items():
        if schema.has_column(table, k):
          try:
            if v['start']!=None: me = me.where(k, '>=', v['start'])
          except Exception as e:
            pass
          try:
            if v['end']!=None: me = me.where(k, '<=', v['end'])
          except Exception as e:
            pass

    # Order
    if order!=None and len(order):
      for k, v in order.items():
        if schema.has_column(table, k) and (v.lower() == 'asc' or v.lower() == 'desc'):
          me = me.order_by(k, v)

    paged = me.paginate(recPerPage,page)
    result = {
      "total": paged.total,
      "per_page": paged.per_page,
      "current_page": paged.current_page,
      "last_page": paged.last_page,
      "prev_page": paged.previous_page,
      "next_page": paged.next_page,
      "data": paged.serialize()
    }
    return result

  @classmethod
  def getById(self, id):
    result = self.find(id)
    return result

  @classmethod
  def getByColumn(self, column, op, value):
    result = self.where(column, op, value).order_by('created_at', 'DESC').first()
    return result

  @classmethod
  def addNew(self, data):
    me = self()
    cols = schema.get_column_listing(me.__table__)
    for v in me.__fillable__:
      try:
        setattr(me, v, data[v])
      except Exception as e:
        pass
    me.save()
    savedId = getattr(me, me.__primary_key__)
    return me.getById(savedId)

  @classmethod
  def doUpdate(self, id, data):
    me = self.find(id)
    if(me == None):
      # raise InvalidResponseException("Data not found", 422)
      return 'Data not found'
    for v in schema.get_column_listing(self.__table__):
      try:
        setattr(me, v, data[v])
      except Exception as e:
        pass
    me.save()
    savedId = getattr(me, self.__primary_key__)
    return self.getById(savedId)


class AuthenticableBase(Model):

  __attemptWith = 'email'

  @classmethod
  def setAttemptWith(self, strType):
    self.__attemptWith = strType

  @classmethod
  def validate(self, dcData):
    authSubject = None
    if self.__attemptWith=='email':
      hashed = self.hashPassword(dcData['password'])
      authSubject = self.where('email', dcData['email']).where('password', hashed).first()
    elif self.__attemptWith=='username':
      hashed = self.hashPassword(dcData['password'])
      authSubject = self.where('username', dcData['username']).where('password', hashed).first()
    elif self.__attemptWith=='clientid':
      authSubject = self.where('client_id', dcData['client_id']).where('client_secret', dcData['client_secret']).first()
    else:
      hashed = self.hashPassword(dcData['password'])
      authSubject = self.where('email', dcData['email']).where('password', hashed).first()

    if authSubject==None:
      return False
    else:
      return authSubject.to_dict()

  @classmethod
  def hashPassword(self, strPassword):
    return hashlib.sha256(strPassword).hexdigest()

class Schema(Model):
  @classmethod
  def getSchema(self):
    return schema
