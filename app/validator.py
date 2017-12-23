import re
from cerberus import Validator
from var_dump import var_dump
from werkzeug.datastructures import FileStorage

class MyValidator(Validator):

  def __init__(self, *args, **kwargs):
      if 'additional_context' in kwargs:
          self.additional_context = kwargs['additional_context']
      super(MyValidator, self).__init__(*args, **kwargs)

  # """
  # Validate URL
  # """
  # def _validate_isurl(self, isurl, field, value):
  #   valid = re.match("([a-z]([a-z]|\d|\+|-|\.)*):(\/\/(((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?((\[(|(v[\da-f]{1,}\.(([a-z]|\d|-|\.|_|~)|[!\$&'\(\)\*\+,;=]|:)+))\])|((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=])*)(:\d*)?)(\/(([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*|(\/((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)|((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)|((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)){0})(\?((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\xE000-\xF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?", value)
  #   if valid==None:
  #       self._error(field, "Invalid URL format")

  """
  Type Validator : File
  """
  def _validate_type_file(self, value):
      if isinstance(value, FileStorage):
          return True
      return False

  # """
  # Email validator
  # """
  # def _validate_email(self, email, field, value):
  #   """
  #   Validate URL
  #   """
  #   valid = re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value)
  #   if valid==None:
  #       self._error(field, "Invalid email format")

  """Wrapper validate

  Validate and return messages if not TRUE
  """
  def wrp_validate(self, document, schema=None, update=False, normalize=True):
      # schema = { 'rp': { 'type': 'integer' }, 'q': { 'type': 'string' }, 'f': { 'type': 'dict' } }
      # v = Validator()
      self.schema = schema
      self.normalized(document, schema)
      if self.validate(document)==False:
          numsg = []
          for attr,msgs in self.errors.items():
              for msg in msgs:
                  numsg.append(str(attr) + ' : ' + str(msg))
          return { 'status': False, 'messages': numsg }
      else:
          return { 'status': True, 'messages': [] }
