##############################################################################
#
# Copyright (c) 2006 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jerome Perrin <jerome@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

"""Utility functions and classes for unit testing
"""

import os

import transaction
import Products.ERP5Type
from Products.MailHost.MailHost import MailHost
from email import message_from_string
import backportUnittest

class FileUpload(file):
  """Act as an uploaded file.
  """
  __allow_access_to_unprotected_subobjects__ = 1
  def __init__(self, path, name):
    self.filename = name
    file.__init__(self, path)
    self.headers = {}

# dummy objects
class DummyMailHost(MailHost):
  """Dummy Mail Host that doesn't really send messages and keep a copy in
  _last_message attribute.
  To use it, you have to replace existing mailhost in afterSetUp:
    
    if 'MailHost' in portal.objectIds():
      portal.manage_delObjects(['MailHost'])
    portal._setObject('MailHost', DummyMailHost('MailHost'))
  """
  _last_message = ()
  _previous_message = ()
  _message_list = []
  def _send( self, mfrom, mto, messageText ):
    """Record message in _last_message."""
    message_text = messageText
    for part in message_from_string(messageText).walk():
      if part.get_content_type() in ['text/plain', 'text/html' ] \
             and not part.is_multipart():
        message_text = part.get_payload(decode=1)
    self._previous_message = self._last_message
    self._last_message = (mfrom, mto, message_text)
    self._message_list.append(self._last_message)
  def getMessageList(self):
    """ Return message list"""
    return self._message_list

class DummyTranslationService:
  """A dummy translation service where you can access translated msgids and
  mappings in _translated.
  """
  _translated = {}
  def translate(self, domain, msgid, mapping=None, *args, **kw):
    self._translated.setdefault(domain, []).append((msgid, mapping))
    return msgid

class DummyMessageCatalog:
  __allow_access_to_unprotected_subobjects__ = 1
  def __init__(self):
    self._translated = []
  def gettext(self, word, lang=None, add=1, default=None, **kw):
    self._translated.append(word)
    if default is None:
      return word
    else:
      return default

class DummyLocalizer:
  """A replacement for stock cookie - based localizer.

  You can change the current language by calling 'changeLanguage'
  You can access the translated messages in _translated attribute from erp5_ui
  and erp5_content message catalogs. It's a list.
  """
  __allow_access_to_unprotected_subobjects__ = 1
  def __init__(self):
    self.erp5_ui = self.ui = DummyMessageCatalog()
    self.erp5_content = self.content = DummyMessageCatalog()
    self.default = DummyMessageCatalog()
    self.lang = 'en'

  def __getitem__(self, key):
    if hasattr(self, key):
      return getattr(self, key)
    raise KeyError, key

  def get_selected_language(self):
    return self.lang
  
  def get_languages_map(self):
    return [{'selected': True, 'id': 'en', 'title': 'English'},
            {'selected': False, 'id': 'pl', 'title': 'Polish'},
            {'selected': False, 'id': 'fr', 'title': 'French'},]

  def get_supported_languages(self):
    return ('en', 'fr', 'pl')

  get_languages = get_supported_languages

  def changeLanguage(self, lang):
    self.lang = lang

  def translate(self, domain, msgid, lang=None, mapping=None, *args, **kw):
    params = dict()
    for key in ('lang', 'add', 'default'):
      if key in kw:
        params[key] = kw[key]
    if lang is not None:
      params['lang'] = lang
    if 'target_language' in kw:
      params['lang'] = kw['target_language']
    msg = getattr(self, domain, self.default).gettext(msgid, **params)
    if mapping:
      # this is a simpler version that does not handle unicode
      from string import Template
      return Template(msg).substitute(mapping)
    return msg
  
  def __call__(self, request, context):
    # the before traverse hook
    pass


# python scripts
def createZODBPythonScript(container, script_id, script_params,
                           script_content):
  """Creates a Python script `script_id` in the given `container`, with
  `script_params` and `script_content`.
  
  If the container already contains an object with id `script_id`, this
  object is removed first.
  """
  if script_id in container.objectIds():
    container.manage_delObjects([script_id])

  container.manage_addProduct['PythonScripts']\
                .manage_addPythonScript(id = script_id)
  script = container[script_id]
  script.ZPythonScript_edit(script_params, script_content)
  container.portal_url.getPortalObject().changeSkin(None)
  return script

def removeZODBPythonScript(container, script_id):
  """
  Removes a Python script `script_id` in the given `container`.
  """
  container.manage_delObjects([script_id])

# class tool
def installRealClassTool(portal):
  """Replaces portal_classes by a real class tool object.
  """
  Products.ERP5Type.allowClassTool = lambda: 1
  _recreateClassTool(portal)

def installDummyClassTool(portal):
  """Replaces portal_classes by a dummy class tool object.
  """
  Products.ERP5Type.allowClassTool = lambda: 0
  _recreateClassTool(portal)

def _recreateClassTool(portal):
  """Recreate the class tool for this portal.
  """
  from Products.ERP5Type.Tool import ClassTool
  reload(ClassTool)
  portal.manage_delObjects(['portal_classes'])
  portal._setObject('portal_classes', ClassTool.ClassTool())

# memcache tool
def installRealMemcachedTool(portal):
  """Replaces portal_memcached by a real memcached tool object.
  """
  _recreateMemcachedTool(portal)

def _recreateMemcachedTool(portal):
  """Recreate the memcached tool for this portal.
  """
  from Products.ERP5Type.Tool import MemcachedTool
  reload(MemcachedTool)
  portal.manage_delObjects(['portal_memcached'])
  portal._setObject('portal_memcached', MemcachedTool.MemcachedTool())

# test runner shared functions
def getMySQLArguments():
  """Returns arguments to pass to mysql by heuristically converting the
  connection string.
  """
  connection_string = os.environ.get('erp5_sql_connection_string')
  if not connection_string:
    return '-u test test'

  password = ''
  host = ''
  db, user = connection_string.split(' ', 1)

  if ' ' in user: # look for user password
    user, password = user.split()
    password = '-p%s' % password

  if "@" in db: # look for hostname
    db, host = db.split('@')
    host = '-h %s' % host

  return '-u %s %s %s %s' % (user, password, host, db)

# decorators
class reindex(object):
  """Decorator to commit transaction and flush activities after the method is
  called.
  """
  def __init__(self, func):
    self._func = func

  def __get__(self, instance, cls=None):
    self._instance = instance
    return self
  
  def __call__(self, *args, **kw):
    ret = self._func(self._instance, *args, **kw)
    if kw.get('reindex', 1):
      transaction.commit()
      self._instance.tic()
    return ret

# Use this as a method or class decorator to tag it as TODO.
# The test will be skipped:
#  - the fixture itself is not run
#  - if a TODO test is in fact successful, no one will ever know
#
# Test cases using this decorator must extend backportUnittest.TestCase
todo_erp5 = backportUnittest.skip("TODO ERP5")

