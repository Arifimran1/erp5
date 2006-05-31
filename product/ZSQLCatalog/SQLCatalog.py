##############################################################################
#
# Copyright (c) 2002 Nexedi SARL. All Rights Reserved.
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

from Persistence import Persistent
import Acquisition
import ExtensionClass
import Globals
from Globals import DTMLFile, PersistentMapping
from string import lower, split, join
from thread import allocate_lock, get_ident
from OFS.Folder import Folder
from AccessControl import ClassSecurityInfo, getSecurityManager
from BTrees.OIBTree import OIBTree
from App.config import getConfiguration
from BTrees.Length import Length
from Shared.DC.ZRDB.TM import TM

from DateTime import DateTime
from Products.PluginIndexes.common.randid import randid
from Acquisition import aq_parent, aq_inner, aq_base, aq_self
from zLOG import LOG, WARNING, INFO, TRACE
from ZODB.POSException import ConflictError
from DocumentTemplate.DT_Var import sql_quote

import time
import sys
import urllib
import string
from cStringIO import StringIO
from xml.dom.minidom import parse, parseString, getDOMImplementation
from xml.sax.saxutils import escape, quoteattr
import os
import md5
import threading

try:
  from Products.PageTemplates.Expressions import SecureModuleImporter
  from Products.CMFCore.Expression import Expression
  from Products.PageTemplates.Expressions import getEngine
  from Products.CMFCore.utils import getToolByName
  withCMF = 1
except ImportError:
  withCMF = 0

try:
  import psyco
except ImportError:
  psyco = None

try:
  from Products.ERP5Type.Cache import enableReadOnlyTransactionCache, disableReadOnlyTransactionCache
except ImportError:
  def doNothing(context):
    pass
  enableReadOnlyTransactionCache = doNothing
  disableReadOnlyTransactionCache = doNothing

UID_BUFFER_SIZE = 300

valid_method_meta_type_list = ('Z SQL Method', 'Script (Python)')

manage_addSQLCatalogForm=DTMLFile('dtml/addSQLCatalog',globals())

def manage_addSQLCatalog(self, id, title,
             vocab_id='create_default_catalog_',
             REQUEST=None):
  """Add a Catalog object
  """
  id=str(id)
  title=str(title)
  vocab_id=str(vocab_id)
  if vocab_id == 'create_default_catalog_':
    vocab_id = None

  c=Catalog(id, title, self)
  self._setObject(id, c)
  if REQUEST is not None:
    return self.manage_main(self, REQUEST,update_menu=1)


class UidBuffer(TM):
  """Uid Buffer class caches a list of reserved uids in a transaction-safe way."""

  def __init__(self):
    """Initialize some variables.

      temporary_buffer is used to hold reserved uids created by non-committed transactions.

      finished_buffer is used to hold reserved uids created by committed-transactions.

      This distinction is important, because uids by non-committed transactions might become
      invalid afterwards, so they may not be used by other transactions."""
    self.temporary_buffer = {}
    self.finished_buffer = []

  def _finish(self):
    """Move the uids in the temporary buffer to the finished buffer."""
    tid = get_ident()
    try:
      self.finished_buffer.extend(self.temporary_buffer[tid])
      del self.temporary_buffer[tid]
    except KeyError:
      pass

  def _abort(self):
    """Erase the uids in the temporary buffer."""
    tid = get_ident()
    try:
      del self.temporary_buffer[tid]
    except KeyError:
      pass

  def __len__(self):
    tid = get_ident()
    l = len(self.finished_buffer)
    try:
      l += len(self.temporary_buffer[tid])
    except KeyError:
      pass
    return l

  def remove(self, value):
    self._register()
    for uid_list in self.temporary_buffer.values():
      try:
        uid_list.remove(value)
      except ValueError:
        pass
    try:
      self.finished_buffer.remove(value)
    except ValueError:
      pass

  def pop(self):
    self._register()
    tid = get_ident()
    try:
      uid = self.temporary_buffer[tid].pop()
    except (KeyError, IndexError):
      uid = self.finished_buffer.pop()
    return uid

  def extend(self, iterable):
    self._register()
    tid = get_ident()
    self.temporary_buffer.setdefault(tid, []).extend(iterable)

class Catalog(Folder, Persistent, Acquisition.Implicit, ExtensionClass.Base):
  """ An Object Catalog

  An Object Catalog maintains a table of object metadata, and a
  series of manageable indexes to quickly search for objects
  (references in the metadata) that satisfy a search where_expression.

  This class is not Zope specific, and can be used in any python
  program to build catalogs of objects.  Note that it does require
  the objects to be Persistent, and thus must be used with ZODB3.

  uid -> the (local) universal ID of objects
  path -> the (local) path of objects


  bgrain defined in meyhods...

  TODO:

    - optmization: indexing objects should be deferred
      until timeout value or end of transaction
  """
  meta_type = "SQLCatalog"
  icon='misc_/ZCatalog/ZCatalog.gif' # FIXME: use a different icon
  security = ClassSecurityInfo()

  manage_options = (
    {'label': 'Contents',       # TAB: Contents
     'action': 'manage_main',
     'help': ('OFSP','ObjectManager_Contents.stx')},
    {'label': 'Catalog',      # TAB: Catalogged Objects
     'action': 'manage_catalogView',
     'target': 'manage_main',
     'help':('ZCatalog','ZCatalog_Cataloged-Objects.stx')},
    {'label': 'Properties',     # TAB: Properties
     'action': 'manage_propertiesForm',
     'help': ('OFSP','Properties.stx')},
    {'label': 'Filter',     # TAB: Filter
     'action': 'manage_catalogFilter',},
    {'label': 'Find Objects',     # TAB: Find Objects
     'action': 'manage_catalogFind',
     'target':'manage_main',
     'help':('ZCatalog','ZCatalog_Find-Items-to-ZCatalog.stx')},
    {'label': 'Advanced',       # TAB: Advanced
     'action': 'manage_catalogAdvanced',
     'target':'manage_main',
     'help':('ZCatalog','ZCatalog_Advanced.stx')},
    {'label': 'Undo',         # TAB: Undo
     'action': 'manage_UndoForm',
     'help': ('OFSP','Undo.stx')},
    {'label': 'Security',       # TAB: Security
     'action': 'manage_access',
     'help': ('OFSP','Security.stx')},
    {'label': 'Ownership',      # TAB: Ownership
     'action': 'manage_owner',
     'help': ('OFSP','Ownership.stx'),}
    )

  __ac_permissions__=(

    ('Manage ZCatalog Entries',
     ['manage_catalogObject', 'manage_uncatalogObject',

      'manage_catalogView', 'manage_catalogFind',
      'manage_catalogSchema', 'manage_catalogFilter',
      'manage_catalogAdvanced', 'manage_objectInformation',

      'manage_catalogReindex', 'manage_catalogFoundItems',
      'manage_catalogClear', 'manage_editSchema',
      'manage_reindexIndex', 'manage_main',
      'manage_editFilter',
      ],
     ['Manager']),

    ('Search ZCatalog',
     ['searchResults', '__call__', 'uniqueValuesFor',
      'getpath', 'schema', 'names', 'columns', 'indexes', 'index_objects',
      'all_meta_types', 'valid_roles', 'resolve_url',
      'getobject', 'getObject', 'getObjectList', 'getCatalogSearchTableIds',
      'getFilterableMethodList', ],
     ['Anonymous', 'Manager']),

    ('Import/Export objects',
     ['manage_exportProperties', 'manage_importProperties', ],
     ['Manager']),

    )

  _properties = (
    { 'id'      : 'title',
      'description' : 'The title of this catalog',
      'type'    : 'string',
      'mode'    : 'w' },

    # Z SQL Methods
    { 'id'      : 'sql_catalog_produce_reserved',
      'description' : 'A method to produce new uid values in advance',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_clear_reserved',
      'description' : 'A method to clear reserved uid values',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_reserve_uid',
      'description' : 'A method to reserve a uid value',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_object_list',
      'description' : 'Methods to be called to catalog the list of objects',
      'type'    : 'multiple selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_uncatalog_object',
      'description' : 'Methods to be called to uncatalog an object',
      'type'    : 'multiple selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_translation_list',
      'description' : 'Methods to be called to catalog the list of translation objects',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_delete_translation_list',
      'description' : 'Methods to be called to delete translations',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_clear_catalog',
      'description' : 'The methods which should be called to clear the catalog',
      'type'    : 'multiple selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_record_object_list',
      'description' : 'Method to record catalog information',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_read_recorded_object_list',
      'description' : 'Method to get recorded information',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_delete_recorded_object_list',
      'description' : 'Method to delete recorded information',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_search_results',
      'description' : 'Main method to search the catalog',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_search_tables',
      'description' : 'Tables to join in the result',
      'type'    : 'multiple selection',
      'select_variable' : 'getTableIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_search_result_keys',
      'description' : 'Keys to display in the result',
      'type'    : 'multiple selection',
      'select_variable' : 'getResultColumnIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_count_results',
      'description' : 'Main method to search the catalog',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_getitem_by_path',
      'description' : 'Get a catalog brain by path',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_getitem_by_uid',
      'description' : 'Get a catalog brain by uid',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_tables',
      'description' : 'Method to get the main catalog tables',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_schema',
      'description' : 'Method to get the main catalog schema',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_unique_values',
      'description' : 'Find unique disctinct values in a column',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_paths',
      'description' : 'List all object paths in catalog',
      'type'    : 'selection',
      'select_variable' : 'getCatalogMethodIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_keyword_search_keys',
      'description' : 'Columns which should be considered as full text search',
      'type'    : 'multiple selection',
      'select_variable' : 'getColumnIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_full_text_search_keys',
      'description' : 'Columns which should be considered as full text search',
      'type'    : 'multiple selection',
      'select_variable' : 'getColumnIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_request_keys',
      'description' : 'Columns which should be ignore in the REQUEST in order to accelerate caching',
      'type'    : 'multiple selection',
      'select_variable' : 'getColumnIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_multivalue_keys',
      'description' : 'Keys which hold multiple values',
      'type'    : 'multiple selection',
      'select_variable' : 'getColumnIds',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_topic_search_keys',
      'description' : 'Columns which should be considered as topic index',
      'type'    : 'lines',
      'mode'    : 'w' },
    { 'id'      : 'sql_catalog_related_keys',
      'title'   : 'Related keys',
      'description' : 'Additional columns obtained through joins',
      'type'    : 'lines',
      'mode'    : 'w' },
  )

  sql_catalog_produce_reserved = 'z_produce_reserved_uid_list'
  sql_catalog_clear_reserved = 'z_clear_reserved'
  sql_catalog_reserve_uid = 'z_reserve_uid'
  sql_catalog_object_list = ('z_catalog_object_list',)
  sql_uncatalog_object = ('z_uncatalog_object',)
  sql_clear_catalog = ('z_drop_catalog', 'z_create_catalog')
  sql_catalog_translation_list = 'z_catalog_translation_list'
  sql_delete_translation_list = 'z_delete_translation_list'
  sql_record_object_list = 'z_record_object_list'
  sql_read_recorded_object_list = 'z_read_recorded_object_list'
  sql_delete_recorded_object_list = 'z_delete_recorded_object_list'
  sql_search_results = 'z_search_results'
  sql_count_results = 'z_count_results'
  sql_getitem_by_path = 'z_getitem_by_path'
  sql_getitem_by_uid = 'z_getitem_by_uid'
  sql_catalog_tables = 'z_catalog_tables'
  sql_search_tables = ('catalog',)
  sql_catalog_schema = 'z_catalog_schema'
  sql_unique_values = 'z_unique_values'
  sql_catalog_paths = 'z_catalog_paths'
  sql_catalog_keyword_search_keys =  ('Description', 'Title', 'SearchableText')
  sql_catalog_full_text_search_keys = ()
  sql_catalog_request_keys = ()
  sql_search_result_keys = ()
  sql_catalog_topic_search_keys = ()
  sql_catalog_multivalue_keys = ()
  sql_catalog_related_keys = ()

  # These are ZODB variables, so shared by multiple Zope instances.
  # This is set to the last logical time when clearReserved is called.
  _last_clear_reserved_time = 0
  # This is to record the maximum value of uids. Because this uses the class Length
  # in BTrees.Length, this does not generate conflict errors.
  _max_uid = None

  # These are class variable on memory, so shared only by threads in the same Zope instance.
  # This is set to the time when reserved uids are cleared in this Zope instance.
  _local_clear_reserved_time = None
  # This is used for exclusive access to the list of reserved uids.
  _reserved_uid_lock = allocate_lock()
  # This is an instance id which specifies who owns which reserved uids.
  _instance_id = getattr(getConfiguration(), 'instance_id', None)

  manage_catalogView = DTMLFile('dtml/catalogView',globals())
  manage_catalogFilter = DTMLFile('dtml/catalogFilter',globals())
  manage_catalogFind = DTMLFile('dtml/catalogFind',globals())
  manage_catalogAdvanced = DTMLFile('dtml/catalogAdvanced', globals())

  def __init__(self, id, title='', container=None):
    if container is not None:
      self=self.__of__(container)
    self.id=id
    self.title=title
    self.schema = {}  # mapping from attribute name to column
    self.names = {}   # mapping from column to attribute name
    self.indexes = {}   # empty mapping

  def manage_exportProperties(self, REQUEST=None, RESPONSE=None):
    """
      Export properties to an XML file.
    """
    f = StringIO()
    f.write('<?xml version="1.0"?>\n<SQLCatalogData>\n')
    property_id_list = self.propertyIds()
    # Get properties and values
    property_list = []
    for property_id in property_id_list:
      value = self.getProperty(property_id)
      if value is not None:
        property_list.append((property_id, value))
    # Sort for easy diff
    property_list.sort(lambda x, y: cmp(x[0], y[0]))
    for property in property_list:
      property_id = property[0]
      value       = property[1]
      if type(value) in (type(''), type(u'')):
        f.write('  <property id=%s type="str">%s</property>\n' % (quoteattr(property_id), escape(value)))
      elif type(value) in (type(()), type([])):
        f.write('  <property id=%s type="tuple">\n' % quoteattr(property_id))
        # Sort for easy diff
        item_list = []
        for item in value:
          if type(item) in (type(""), type(u"")):
            item_list.append(item)
        item_list.sort()
        for item in item_list:
          f.write('    <item type="str">%s</item>\n' % escape(str(item)))
        f.write('  </property>\n')
    # XXX Although filters are not properties, output filters here.
    # XXX Ideally, filters should be properties in Z SQL Methods, shouldn't they?
    if hasattr(self, 'filter_dict'):
      filter_list = []
      for filter_id in self.filter_dict.keys():
        filter_definition = self.filter_dict[filter_id]
        filter_list.append((filter_id, filter_definition))
      # Sort for easy diff
      filter_list.sort(lambda x, y: cmp(x[0], y[0]))
      for filter_item in filter_list:
        filter_id  = filter_item[0]
        filter_def = filter_item[1]
        if not filter_def['filtered']:
          # If a filter is not activated, no need to output it.
          continue
        if not filter_def['expression']:
          # If the expression is not specified, meaningless to specify it.
          continue
        f.write('  <filter id=%s expression=%s />\n' % (quoteattr(filter_id), quoteattr(filter_def['expression'])))
        # For now, portal types are not exported, because portal types are too specific to each site.
    f.write('</SQLCatalogData>\n')

    if RESPONSE is not None:
      RESPONSE.setHeader('Content-type','application/data')
      RESPONSE.setHeader('Content-Disposition',
                          'inline;filename=properties.xml')
    return f.getvalue()

  def manage_importProperties(self, file):
    """
      Import properties from an XML file.
    """
    f = open(file)
    try:
      doc = parse(f)
      root = doc.documentElement
      try:
        for prop in root.getElementsByTagName("property"):
          id = prop.getAttribute("id")
          type = prop.getAttribute("type")
          if not id or not hasattr(self, id):
            raise CatalogError, 'unknown property id %r' % (id,)
          if type not in ('str', 'tuple'):
            raise CatalogError, 'unknown property type %r' % (type,)
          if type == 'str':
            value = ''
            for text in prop.childNodes:
              if text.nodeType == text.TEXT_NODE:
                value = str(text.data)
                break
          else:
            value = []
            for item in prop.getElementsByTagName("item"):
              item_type = item.getAttribute("type")
              if item_type != 'str':
                raise CatalogError, 'unknown item type %r' % (item_type,)
              for text in item.childNodes:
                if text.nodeType == text.TEXT_NODE:
                  value.append(str(text.data))
                  break
            value = tuple(value)

          setattr(self, id, value)

        if not hasattr(self, 'filter_dict'):
          self.filter_dict = PersistentMapping()
        for filt in root.getElementsByTagName("filter"):
          id = str(filt.getAttribute("id"))
          expression = filt.getAttribute("expression")
          if not self.filter_dict.has_key(id):
            self.filter_dict[id] = PersistentMapping()
          self.filter_dict[id]['filtered'] = 1
          self.filter_dict[id]['type'] = []
          if expression:
            expr_instance = Expression(expression)
            self.filter_dict[id]['expression'] = expression
            self.filter_dict[id]['expression_instance'] = expr_instance
          else:
            self.filter_dict[id]['expression'] = ""
            self.filter_dict[id]['expression_instance'] = None
      finally:
        doc.unlink()
    finally:
      f.close()

  def _clearSecurityCache(self):
    self.security_uid_dict = OIBTree()
    self.security_uid_index = 0

  security.declarePrivate('getSecurityUid')
  def getSecurityUid(self, wrapped_object):
    """
      Cache a uid for each security permission

      We try to create a unique security (to reduce number of lines)
      and to assign security only to root document
    """
    # Get security information
    allowed_roles_and_users = wrapped_object.allowedRolesAndUsers()
    # Sort it
    allowed_roles_and_users = list(allowed_roles_and_users)
    allowed_roles_and_users.sort()
    allowed_roles_and_users = tuple(allowed_roles_and_users)
    # Make sure no duplicates
    if getattr(aq_base(self), 'security_uid_dict', None) is None:
      self._clearSecurityCache()
    if self.security_uid_dict.has_key(allowed_roles_and_users):
      return (self.security_uid_dict[allowed_roles_and_users], None)
    self.security_uid_index = self.security_uid_index + 1
    self.security_uid_dict[allowed_roles_and_users] = self.security_uid_index
    return (self.security_uid_index, allowed_roles_and_users)

  def clear(self):
    """
    Clears the catalog by calling a list of methods
    """
    methods = self.sql_clear_catalog
    for method_name in methods:
      method = getattr(self, method_name)
      try:
        method()
      except ConflictError:
        raise
      except:
        LOG('SQLCatalog', WARNING,
            'could not clear catalog with %s' % method_name, error=sys.exc_info())
        pass

    # Reserved uids have been removed.
    self.clearReserved()

    # Add a dummy item so that SQLCatalog will not use existing uids again.
    if self._max_uid is not None and self._max_uid() != 0:
      method_id = self.sql_catalog_reserve_uid
      method = getattr(self, method_id)
      self._max_uid.change(1)
      method(uid = [self._max_uid()])

    # Remove the cache of catalog schema.
    if hasattr(self, '_v_catalog_schema_dict') :
      del self._v_catalog_schema_dict

    self._clearSecurityCache()

  def clearReserved(self):
    """
    Clears reserved uids
    """
    method_id = self.sql_catalog_clear_reserved
    method = getattr(self, method_id)
    try:
      method()
    except ConflictError:
      raise
    except:
      LOG('SQLCatalog', WARNING,
          'could not clear reserved catalog with %s' % \
              method_id, error=sys.exc_info())
      raise
    self._last_clear_reserved_time += 1

  def __getitem__(self, uid):
    """
    Get an object by UID
    Note: brain is defined in Z SQL Method object
    """
    method = getattr(self,  self.sql_getitem_by_uid)
    search_result = method(uid = uid)
    if len(search_result) > 0:
      return search_result[0]
    else:
      return None

  def editSchema(self, names_list):
    """
    Builds a schema from a list of strings
    Splits each string to build a list of attribute names
    Columns on the database should not change during this operations
    """
    i = 0
    schema = {}
    names = {}
    for cid in self.getColumnIds():
      name_list = []
      for name in names_list[i].split():
        schema[name] = cid
        name_list += [name,]
      names[cid] = tuple(name_list)
      i += 1
    self.schema = schema
    self.names = names

  def getCatalogSearchTableIds(self):
    """Return selected tables of catalog which are used in JOIN.
       catalaog is always first
    """
    search_tables = self.sql_search_tables
    if len(search_tables) > 0:
      if search_tables[0] != 'catalog':
        result = ['catalog']
        for t in search_tables:
          if t != 'catalog':
            result.append(t)
        self.sql_search_tables = result
    else:
      self.sql_search_tables = ['catalog']

    return self.sql_search_tables

  security.declarePublic('getCatalogSearchResultKeys')
  def getCatalogSearchResultKeys(self):
    """Return search result keys.
    """
    return self.sql_search_result_keys

  def _getCatalogSchema(self, table=None):
    catalog_schema_dict = getattr(aq_base(self), '_v_catalog_schema_dict', {})

    if table not in catalog_schema_dict:
      result_list = []
      try:
        method_name = self.sql_catalog_schema
        method = getattr(self, method_name)
        #LOG('_getCatalogSchema', 0, 'method_name = %r, method = %r, table = %r' % (method_name, method, table))
        search_result = method(table=table)
        for c in search_result:
          result_list.append(c.Field)
      except ConflictError:
        raise
      except:
        LOG('SQLCatalog', WARNING, '_getCatalogSchema failed with the method %s' % method_name, error=sys.exc_info())
        pass
      catalog_schema_dict[table] = tuple(result_list)
      self._v_catalog_schema_dict= catalog_schema_dict

    return catalog_schema_dict[table]

  def getColumnIds(self):
    """
    Calls the show column method and returns dictionnary of
    Field Ids

    XXX This should be cached
    """
    keys = {}
    for table in self.getCatalogSearchTableIds():
      field_list = self._getCatalogSchema(table=table)
      for field in field_list:
        keys[field] = 1
        keys['%s.%s' % (table, field)] = 1  # Is this inconsistent ?
    for related in self.getSqlCatalogRelatedKeyList():
      related_tuple = related.split('|')
      related_key = related_tuple[0].strip()
      keys[related_key] = 1
    keys = keys.keys()
    keys.sort()
    return keys

  def getColumnMap(self):
    """
    Calls the show column method and returns dictionnary of
    Field Ids

    XXX This should be cached
    """
    keys = {}
    for table in self.getCatalogSearchTableIds():
      field_list = self._getCatalogSchema(table=table)
      for field in field_list:
        key = field
        if not keys.has_key(key): keys[key] = []
        keys[key].append(table)
        key = '%s.%s' % (table, key)
        if not keys.has_key(key): keys[key] = []
        keys[key].append(table) # Is this inconsistent ?
    return keys

  def getResultColumnIds(self):
    """
    Calls the show column method and returns dictionnary of
    Field Ids
    """
    keys = {}
    for table in self.getCatalogSearchTableIds():
      field_list = self._getCatalogSchema(table=table)
      for field in field_list:
        keys['%s.%s' % (table, field)] = 1
    keys = keys.keys()
    keys.sort()
    return keys

  def getTableIds(self):
    """
    Calls the show table method and returns dictionnary of
    Field Ids
    """
    keys = []
    method_name = self.sql_catalog_tables
    try:
      method = getattr(self,  method_name)
      search_result = method()
      for c in search_result:
        keys.append(c[0])
    except ConflictError:
      raise
    except:
      pass
    return keys

  # the cataloging API
  def produceUid(self):
    """
      Produces reserved uids in advance
    """
    klass = self.__class__
    assert klass._reserved_uid_lock.locked()
    # This checks if the list of local reserved uids was cleared after clearReserved
    # had been called.
    if klass._local_clear_reserved_time != self._last_clear_reserved_time:
      self._v_uid_buffer = UidBuffer()
      klass._local_clear_reserved_time = self._last_clear_reserved_time
    elif getattr(self, '_v_uid_buffer', None) is None:
      self._v_uid_buffer = UidBuffer()
    if len(self._v_uid_buffer) == 0:
      method_id = self.sql_catalog_produce_reserved
      method = getattr(self, method_id)
      # Generate an instance id randomly. Note that there is a small possibility that this
      # would conflict with others.
      random_factor_list = [time.time(), os.getpid(), os.times()]
      try:
        random_factor_list.append(os.getloadavg())
      except (OSError, AttributeError): # AttributeError is required under cygwin
        pass
      instance_id = md5.new(str(random_factor_list)).hexdigest()
      uid_list = [x.uid for x in method(count = UID_BUFFER_SIZE, instance_id = instance_id) if x.uid != 0]
      self._v_uid_buffer.extend(uid_list)

  def newUid(self):
    """
      This is where uid generation takes place. We should consider a multi-threaded environment
      with multiple ZEO clients on a single ZEO server.

      The main risk is the following:

      - objects a/b/c/d/e/f are created (a is parent of b which is parent of ... of f)

      - one reindexing node N1 starts reindexing f

      - another reindexing node N2 starts reindexing e

      - there is a strong risk that N1 and N2 start reindexing at the same time
        and provide different uid values for a/b/c/d/e

      Similar problems may happen with relations and acquisition of uid values (ex. order_uid)
      with the risk of graph loops
    """
    if withCMF:
      zope_root = getToolByName(self, 'portal_url').getPortalObject().aq_parent
      site_root = getToolByName(self, 'portal_url').getPortalObject()
    else:
      zope_root = self.getPhysicalRoot()
      site_root = self.aq_parent

    root_indexable = int(getattr(zope_root, 'isIndexable', 1))
    site_indexable = int(getattr(site_root, 'isIndexable', 1))
    if not (root_indexable and site_indexable):
      return None

    klass = self.__class__
    try:
      klass._reserved_uid_lock.acquire()
      self.produceUid()
      if len(self._v_uid_buffer) > 0:
        uid = self._v_uid_buffer.pop()
        # Vincent added this 2006/01/25
        #if uid > 4294967296: # 2**32
        #if uid > 10000000: # arbitrary level : below it's normal, above it's suspicious
        #   LOG('SQLCatalog', WARNING, 'Newly generated UID (%s) seems too big ! - vincent' % (uid,))
        #   raise RuntimeError, 'Newly generated UID (%s) seems too big ! - vincent' % (uid,)
        # end
        if self._max_uid is None:
          self._max_uid = Length()
        if uid > self._max_uid():
          self._max_uid.set(uid)
        return uid
      else:
        raise CatalogError("Could not retrieve new uid")
    finally:
      klass._reserved_uid_lock.release()

  def manage_catalogObject(self, REQUEST, RESPONSE, URL1, urls=None):
    """ index Zope object(s) that 'urls' point to """
    if urls:
      if isinstance(urls, types.StringType):
        urls=(urls,)

      for url in urls:
        obj = self.resolve_path(url)
        if not obj:
          obj = self.resolve_url(url, REQUEST)
        if obj is not None:
          self.aq_parent.catalog_object(obj, url, sql_catalog_id=self.id)

    RESPONSE.redirect(URL1 + '/manage_catalogView?manage_tabs_message=Object%20Cataloged')

  def manage_uncatalogObject(self, REQUEST, RESPONSE, URL1, urls=None):
    """ removes Zope object(s) 'urls' from catalog """

    if urls:
      if isinstance(urls, types.StringType):
        urls=(urls,)

      for url in urls:
        self.aq_parent.uncatalog_object(url, sql_catalog_id=self.id)

    RESPONSE.redirect(URL1 + '/manage_catalogView?manage_tabs_message=Object%20Uncataloged')

  def manage_catalogReindex(self, REQUEST, RESPONSE, URL1):
    """ clear the catalog, then re-index everything """
    elapse = time.time()
    c_elapse = time.clock()

    self.aq_parent.refreshCatalog(clear=1, sql_catalog_id=self.id)

    elapse = time.time() - elapse
    c_elapse = time.clock() - c_elapse

    RESPONSE.redirect(URL1 +
              '/manage_catalogAdvanced?manage_tabs_message=' +
              urllib.quote('Catalog Updated<br>'
                     'Total time: %s<br>'
                     'Total CPU time: %s' % (`elapse`, `c_elapse`)))

  def manage_catalogClear(self, REQUEST=None, RESPONSE=None,
                          URL1=None, sql_catalog_id=None):
    """ clears the whole enchilada """
    self.clear()

    if RESPONSE and URL1:
      RESPONSE.redirect('%s/manage_catalogAdvanced?' \
                        'manage_tabs_message=Catalog%%20Cleared' % URL1)

  def manage_catalogClearReserved(self, REQUEST=None, RESPONSE=None, URL1=None):
    """ clears the whole enchilada """
    self.clearReserved()

    if RESPONSE and URL1:
      RESPONSE.redirect('%s/manage_catalogAdvanced?' \
                        'manage_tabs_message=Catalog%20Cleared' % URL1)

  def manage_catalogFoundItems(self, REQUEST, RESPONSE, URL2, URL1,
                 obj_metatypes=None,
                 obj_ids=None, obj_searchterm=None,
                 obj_expr=None, obj_mtime=None,
                 obj_mspec=None, obj_roles=None,
                 obj_permission=None):
    """ Find object according to search criteria and Catalog them
    """
    elapse = time.time()
    c_elapse = time.clock()

    words = 0
    obj = REQUEST.PARENTS[1]
    path = string.join(obj.getPhysicalPath(), '/')

    results = self.aq_parent.ZopeFindAndApply(obj,
                    obj_metatypes=obj_metatypes,
                    obj_ids=obj_ids,
                    obj_searchterm=obj_searchterm,
                    obj_expr=obj_expr,
                    obj_mtime=obj_mtime,
                    obj_mspec=obj_mspec,
                    obj_permission=obj_permission,
                    obj_roles=obj_roles,
                    search_sub=1,
                    REQUEST=REQUEST,
                    apply_func=self.aq_parent.catalog_object,
                    apply_path=path,
                    sql_catalog_id=self.id)

    elapse = time.time() - elapse
    c_elapse = time.clock() - c_elapse

    RESPONSE.redirect(URL1 + '/manage_catalogView?manage_tabs_message=' +
              urllib.quote('Catalog Updated<br>Total time: %s<br>Total CPU time: %s' % (`elapse`, `c_elapse`)))

  def catalogObject(self, object, path, is_object_moved=0):
    """
    Adds an object to the Catalog by calling
    all SQL methods and providing needed arguments.

    'object' is the object to be cataloged

    'uid' is the unique Catalog identifier for this object

    """
    self.catalogObjectList([object])

  def catalogObjectList(self, object_list, method_id_list=None, disable_cache=0,
                              check_uid=1):
    """
      Add objects to the Catalog by calling
      all SQL methods and providing needed arguments.

      method_id_list : specify which method should be used. If not
                       set it will take the default value of portal_catalog

      disable_cache : do not use cache, so values will be computed each time,
                      only usefull in some particular cases, most of the time
                      you don't need to use it

      Each element of 'object_list' is an object to be cataloged

      'uid' is the unique Catalog identifier for this object

      WARNING: This method assumes that currently all objects are being reindexed from scratch.

      XXX: For now newUid is used to allocated UIDs. Is this good? Is it better to INSERT then SELECT?
    """
    LOG('SQLCatalog', TRACE, 'catalogging %d objects' % len(object_list))
    #LOG('catalogObjectList', 0, 'called with %r' % (object_list,))

    if withCMF:
      zope_root = getToolByName(self, 'portal_url').getPortalObject().aq_parent
      site_root = getToolByName(self, 'portal_url').getPortalObject()
    else:
      zope_root = self.getPhysicalRoot()
      site_root = self.aq_parent

    root_indexable = int(getattr(zope_root, 'isIndexable', 1))
    site_indexable = int(getattr(site_root, 'isIndexable', 1))
    if not (root_indexable and site_indexable):
      return

    for object in object_list:
      path = object.getPath()
      if not getattr(aq_base(object), 'uid', None):
        try:
          object.uid = self.newUid()
        except ConflictError:
          raise
        except:
          raise RuntimeError, 'could not set missing uid for %r' % (object,)
      elif check_uid:
        uid = object.uid
        path = object.getPath()
        index = self.getUidForPath(path)
        try:
          index = int(index)
        except TypeError:
          pass
        if index is not None and index < 0:
          raise CatalogError, 'A negative uid %d is used for %s. Your catalog is broken. Recreate your catalog.' % (index, path)
        if index:
          if uid != index:
            LOG('SQLCatalog', WARNING, 'uid of %r changed from %r to %r !!! This can be fatal. You should reindex the whole site immediately.' % (object, uid, index))
            uid = index
            object.uid = uid
        else:
          # Make sure no duplicates - ie. if an object with different path has same uid, we need a new uid
          # This can be very dangerous with relations stored in a category table (CMFCategory)
          # This is why we recommend completely reindexing subobjects after any change of id
          catalog_path = self.getPathForUid(uid)
          #LOG('catalogObject', 0, 'uid = %r, catalog_path = %r' % (uid, catalog_path))
          if catalog_path == "reserved":
            # Reserved line in catalog table
            klass = self.__class__
            try:
              klass._reserved_uid_lock.acquire()
              if getattr(self, '_v_uid_buffer', None) is not None:
                # This is the case where:
                #   1. The object got an uid.
                #   2. The catalog was cleared.
                #   3. The catalog produced the same reserved uid.
                #   4. The object was reindexed.
                # In this case, the uid is not reserved any longer, but
                # SQLCatalog believes that it is still reserved. So it is
                # necessary to remove the uid from the list explicitly.
                try:
                  self._v_uid_buffer.remove(uid)
                except ValueError:
                  pass
            finally:
              klass._reserved_uid_lock.release()
          elif catalog_path is not None:
            # An uid conflict happened... Why?
            # can be due to path length
            if len(path) > 255:
              LOG('SQLCatalog', WARNING, 'path of object %r is too long for catalog. You should use a shorter path.' %(object,))

            object.uid = self.newUid()
            LOG('SQLCatalog', WARNING,
                'uid of %r changed from %r to %r !!! This can be fatal. You should reindex the whole site immediately.' % (object, uid, object.uid))

    if method_id_list is None:
      method_id_list = self.sql_catalog_object_list
    econtext_cache = {}
    argument_cache = {}
    expression_cache = {}

    try:
      if not disable_cache:
        enableReadOnlyTransactionCache(self)

      method_kw_dict = {}
      for method_name in method_id_list:
        kw = {}
        if self.isMethodFiltered(method_name) and self.filter_dict.has_key(method_name):
          catalogged_object_list = []
          type_list = self.filter_dict[method_name]['type']
          expression = self.filter_dict[method_name]['expression_instance']
          for object in object_list:
            # We will check if there is an filter on this
            # method, if so we may not call this zsqlMethod
            # for this object
            portal_type = object.getPortalType()
            if type_list and portal_type not in type_list:
              continue
            elif expression is not None:
              expression_key = (object.uid, self.filter_dict[method_name]['expression'])
              try:
                result = expression_cache[expression_key]
              except KeyError:
                try:
                  econtext = econtext_cache[object.uid]
                except KeyError:
                  econtext = econtext_cache[object.uid] = self.getExpressionContext(object)
                result = expression_cache[expression_key] = expression(econtext)
              if not result:
                continue
            catalogged_object_list.append(object)
        else:
          catalogged_object_list = object_list

        if len(catalogged_object_list) == 0:
          continue

        method_kw_dict[method_name] = kw

        #LOG('catalogObjectList', 0, 'method_name = %s' % (method_name,))
        method = getattr(self, method_name)
        if method.meta_type == "Z SQL Method":
          # Build the dictionnary of values
          arguments = method.arguments_src
          for arg in split(arguments):
            value_list = []
            append = value_list.append
            for object in catalogged_object_list:
              try:
                value = argument_cache[(object.uid, arg)]
              except KeyError:
                try:
                  value = getattr(object, arg, None)
                  if callable(value):
                    value = value()
                except ConflictError:
                  raise
                except:
                  value = None
                if not disable_cache:
                  argument_cache[(object.uid, arg)] = value
              append(value)
            kw[arg] = value_list

      for method_name in method_id_list:
        if method_name not in method_kw_dict:
          continue
        kw = method_kw_dict[method_name]
        method = getattr(self, method_name)
        method = aq_base(method).__of__(site_root.portal_catalog) # Use method in
                # the context of portal_catalog
        # Alter/Create row
        try:
          #start_time = DateTime()
          #LOG('catalogObjectList', 0, 'kw = %r, method_name = %r' % (kw, method_name))
          method(**kw)
          #end_time = DateTime()
          #if method_name not in profile_dict:
          #  profile_dict[method_name] = end_time.timeTime() - start_time.timeTime()
          #else:
          #  profile_dict[method_name] += end_time.timeTime() - start_time.timeTime()
          #LOG('catalogObjectList', 0, '%s: %f seconds' % (method_name, profile_dict[method_name]))
        except ConflictError:
          raise
        except:
          LOG('SQLCatalog', WARNING, 'could not catalog objects %s with method %s' % (object_list, method_name),
              error=sys.exc_info())
          raise
    finally:
      if not disable_cache:
        disableReadOnlyTransactionCache(self)

  if psyco is not None: psyco.bind(catalogObjectList)

  def uncatalogObject(self, path):
    """
    Uncatalog and object from the Catalog.

    Note, the uid must be the same as when the object was
    catalogued, otherwise it will not get removed from the catalog

    This method should not raise an exception if the uid cannot
    be found in the catalog.

    XXX Add filter of methods

    """
    #LOG('Uncatalog object:',0,str(path))

    uid = self.getUidForPath(path)
    methods = self.sql_uncatalog_object
    for method_name in methods:
      method = getattr(self, method_name)
      try:
        #if 1:
        method(uid = uid)
      except ConflictError:
        raise
      except:
        # This is a real LOG message
        # which is required in order to be able to import .zexp files
        LOG('SQLCatalog', WARNING,
            'could not uncatalog object %s uid %s with method %s' % (path, uid, method_name))

  def catalogTranslationList(self, object_list):
    """Catalog translations.
    """
    method_name = self.sql_catalog_translation_list
    return self.catalogObjectList(object_list, method_id_list = (method_name,))

  def deleteTranslationList(self):
    """Delete translations.
    """
    method_name = self.sql_delete_translation_list
    method = getattr(self, method_name)
    try:
      method()
    except ConflictError:
      raise
    except:
      LOG('SQLCatalog', WARNING, 'could not delete translations', error=sys.exc_info())

  def uniqueValuesFor(self, name):
    """ return unique values for FieldIndex name """
    method = getattr(self, self.sql_unique_values)
    return method()

  def getPaths(self):
    """ Returns all object paths stored inside catalog """
    method = getattr(self, self.sql_catalog_paths)
    return method()

  def getUidForPath(self, path):
    """ Looks up into catalog table to convert path into uid """
    try:
      if path is None:
        return None
      # Get the appropriate SQL Method
      method = getattr(self, self.sql_getitem_by_path)
      search_result = method(path = path, uid_only=1)
      # If not emptyn return first record
      if len(search_result) > 0:
        return search_result[0].uid
      else:
        return None
    except ConflictError:
      raise
    except:
      # This is a real LOG message
      # which is required in order to be able to import .zexp files
      LOG('SQLCatalog', WARNING, "could not find uid from path %s" % (path,))
      return None

  def hasPath(self, path):
    """ Checks if path is catalogued """
    return self.getUidForPath(path) is not None

  def getPathForUid(self, uid):
    """ Looks up into catalog table to convert uid into path """
    try:
      if uid is None:
        return None
      try:
        int(uid)
      except ValueError:
        return None
      # Get the appropriate SQL Method
      method = getattr(self, self.sql_getitem_by_uid)
      search_result = method(uid = uid)
      # If not empty return first record
      if len(search_result) > 0:
        return search_result[0].path
      else:
        return None
    except ConflictError:
      raise
    except:
      # This is a real LOG message
      # which is required in order to be able to import .zexp files
      LOG('SQLCatalog', WARNING, "could not find path from uid %s" % (uid,))
      return None

  def getMetadataForUid(self, uid):
    """ Accesses a single record for a given uid """
    if uid is None:
      return None
    # Get the appropriate SQL Method
    method = getattr(self, self.sql_getitem_by_uid)
    brain = method(uid = uid)[0]
    result = {}
    for k in brain.__record_schema__.keys():
      result[k] = getattr(brain,k)
    return result

  def getIndexDataForUid(self, uid):
    """ Accesses a single record for a given uid """
    return self.getMetadataForUid(uid)

  def getMetadataForPath(self, path):
    """ Accesses a single record for a given path """
    try:
      if uid is None:
        return None
      # Get the appropriate SQL Method
      method = getattr(self, self.sql_getitem_by_path)
      brain = method(path = path)[0]
      result = {}
      for k in brain.__record_schema__.keys():
        result[k] = getattr(brain,k)
      return result
    except ConflictError:
      raise
    except:
      # This is a real LOG message
      # which is required in order to be able to import .zexp files
      LOG('SQLCatalog', WARNING, "could not find uid from path %s" % (path,))
      return None

  def getIndexDataForPath(self, path):
    """ Accesses a single record for a given path """
    return self.getMetadataForPath(path)

  def getCatalogMethodIds(self):
    """Find Z SQL methods in the current folder and above
    This function return a list of ids.
    """
    ids={}
    have_id=ids.has_key
    StringType=type('')

    while self is not None:
      if hasattr(self, 'objectValues'):
        for o in self.objectValues(valid_method_meta_type_list):
          if hasattr(o,'id'):
            id=o.id
            if type(id) is not StringType: id=id()
            if not have_id(id):
              if hasattr(o,'title_and_id'): o=o.title_and_id()
              else: o=id
              ids[id]=id
      if hasattr(self, 'aq_parent'): self=self.aq_parent
      else: self=None

    ids=map(lambda item: (item[1], item[0]), ids.items())
    ids.sort()
    return ids

  def _quoteSQLString(self, value):
    """Return a quoted string of the value.
    """
    if hasattr(value, 'ISO'):
      value = value.ISO()
    elif hasattr(value, 'strftime'):
      value = value.strftime('%Y-%m-%d %H:%M:%S')
    else:
      value = sql_quote(str(value))
    return value

  def getSqlCatalogRelatedKeyList(self, **kw):
    """
    Return the list of related keys.
    This method can be overidden in order to implement
    dynamic generation of some related keys.
    """
    # Do not generate dynamic related key for acceptable_keys
    dynamic_key_list = kw.keys()
    dynamic_key_list = [k for k in dynamic_key_list \
        if k not in self.getColumnMap().keys()]
    dynamic_kw = {}
    for key in dynamic_key_list:
      dynamic_kw[key] = kw[key]

    dynamic_list = self.getDynamicRelatedKeyList(**dynamic_kw)
    full_list = list(dynamic_list) + list(self.sql_catalog_related_keys)
    return full_list

  def buildSQLQuery(self, query_table='catalog', REQUEST=None,
                          ignore_empty_string=1,**kw):
    """ Builds a complex SQL query to simulate ZCalatog behaviour """
    # Get search arguments:
    if REQUEST is None and (kw is None or kw == {}):
      # We try to get the REQUEST parameter
      # since we have nothing handy
      try: REQUEST=self.REQUEST
      except AttributeError: pass

    #LOG('SQLCatalog.buildSQLQuery, kw',0,kw)
    # If kw is not set, then use REQUEST instead
    if kw is None or kw == {}:
      kw = REQUEST

    acceptable_key_map = self.getColumnMap()
    acceptable_keys = acceptable_key_map.keys()
    full_text_search_keys = list(self.sql_catalog_full_text_search_keys)
    keyword_search_keys = list(self.sql_catalog_keyword_search_keys)
    topic_search_keys = self.sql_catalog_topic_search_keys
    multivalue_keys = self.sql_catalog_multivalue_keys

    # Define related maps
    # each tuple has the form (key, 'table1,table2,table3/column/where_expression')
    related_tuples = self.getSqlCatalogRelatedKeyList(**kw)
    #LOG('related_tuples', 0, str(related_tuples))
    related_keys = []
    related_method = {}
    related_table_map = {}
    related_column = {}
    related_table_list = {}
    table_rename_index = 0
    related_methods = {} # related methods which need to be used
    for t in related_tuples:
      t_tuple = t.split('|')
      key = t_tuple[0].strip()
      join_tuple = t_tuple[1].strip().split('/')
      #LOG('related_tuples', 0, str(join_tuple))
      related_keys.append(key)
#       LOG('buildSqlQuery, join_tuple',0,join_tuple)
      method_id = join_tuple[2]
      table_list = tuple(join_tuple[0].split(','))
      related_method[key] = method_id
      related_table_list[key] = table_list
      related_column[key] = join_tuple[1]
      # Rename tables to prevent conflicts
      if not related_table_map.has_key((table_list,method_id)):
        map_list = []
        for table_id in table_list:
          map_list.append((table_id,
             "related_%s_%s" % (table_id, table_rename_index))) # We add an index in order to alias tables in the join
          table_rename_index += 1 # and prevent name conflicts
        related_table_map[(table_list,method_id)] = map_list

    # We take additional parameters from the REQUEST
    # and give priority to the REQUEST
    if REQUEST is not None:
      for key in acceptable_keys:
        if REQUEST.has_key(key):
          # Only copy a few keys from the REQUEST
          if key in self.sql_catalog_request_keys:
            kw[key] = REQUEST[key]
      # Let us try first not to use this
      #for key in related_keys:
      #  if REQUEST.has_key(key):
      #    kw[key] = REQUEST[key]

    # Let us start building the where_expression
    if kw:
      where_expression = []
      from_table_dict = {'catalog' : 'catalog'} # Always include catalog table


      # Compute "sort_index", which is a sort index, or none:
      if kw.has_key('sort-on'):
        sort_index=kw['sort-on']
      elif hasattr(self, 'sort-on'):
        sort_index=getattr(self, 'sort-on')
      elif kw.has_key('sort_on'):
        sort_index=kw['sort_on']
      else: sort_index=None

      # Compute the sort order
      if kw.has_key('sort-order'):
        so=kw['sort-order']
      elif hasattr(self, 'sort-order'):
        so=getattr(self, 'sort-order')
      elif kw.has_key('sort_order'):
        so=kw['sort_order']
      else: so=None

      # We must now turn sort_index into
      # a dict with keys as sort keys and values as sort order
      if type(sort_index) is type('a'):
        sort_index = [(sort_index, so)]
      elif type(sort_index) is not type(()) and type(sort_index) is not type([]):
        sort_index = None


      # If sort_index is a dictionnary
      # then parse it and change it
      sort_on = None
      #LOG('sorting', 0, str(sort_index))
      if sort_index is not None:
        new_sort_index = []
        for sort in sort_index:
          if len(sort)==2:
            new_sort_index.append((sort[0],sort[1],None))
          elif len(sort)==3:
            new_sort_index.append(sort)
        sort_index = new_sort_index
        try:
          new_sort_index = []
          for (key , so, as_type) in sort_index:
            key_is_acceptable = key in acceptable_keys # Only calculate once
            key_is_related = key in related_keys
            if key_is_acceptable or key_is_related:
              if key_is_related: # relation system has priority (ex. security_uid)
                # We must rename the key
                method_id = related_method[key]
                table_list = related_table_list[key]
                if not related_methods.has_key((table_list,method_id)):
                  related_methods[(table_list,method_id)] = 1
                # Prepend renamed table name
                key = "%s.%s" % (related_table_map[(table_list,method_id)][-1][-1], related_column[key])
              elif key_is_acceptable:
                if key.find('.') < 0:
                  # if the key is only used by one table, just append its name
                  if len(acceptable_key_map[key]) == 1 :
                    key = '%s.%s' % (acceptable_key_map[key][0], key)
                  # query_table specifies what table name should be used by default
                  elif query_table:
                    key = '%s.%s' % (query_table, key)
                  elif key == 'uid':
                    # uid is always ambiguous so we can only change it here
                    key = 'catalog.uid'
                # Add table to table dict
                from_table_dict[acceptable_key_map[key][0]] = acceptable_key_map[key][0] # We use catalog by default
              if as_type == 'int':
                key = 'CAST(' + key + ' AS SIGNED)'
              if so in ('descending', 'reverse', 'DESC'):
                new_sort_index += ['%s DESC' % key]
              else:
                new_sort_index += ['%s' % key]
          sort_index = join(new_sort_index,',')
          sort_on = str(sort_index)
        except ConflictError:
          raise
        except:
          LOG('SQLCatalog', WARNING, 'buildSQLQuery could not build the new sort index', error=sys.exc_info())
          pass

      # Rebuild keywords to behave as new style query (_usage='toto:titi' becomes {'toto':'titi'})
      new_kw = {}
      usage_len = len('_usage')
      for k, v in kw.items():
        if k.endswith('_usage'):
          new_k = k[0:-usage_len]
          if not new_kw.has_key(new_k): new_kw[new_k] = {}
          if type(new_kw[new_k]) is not type({}): new_kw[new_k] = {'query': new_kw[new_k]}
          split_v = v.split(':')
          new_kw[new_k] = {split_v[0]: split_v[1]}
        else:
          if not new_kw.has_key(k):
            new_kw[k] = v
          else:
            new_kw[k]['query'] = v
      kw = new_kw
      #LOG('new kw', 0, str(kw))
      # We can now consider that old style query is changed into new style
      for key in kw.keys(): # Do not use kw.items() because this consumes much more memory
        value = kw[key]
        if key not in ('where_expression', 'sort-on', 'sort_on', 'sort-order', 'sort_order', 'limit'):
          # Make sure key belongs to schema
          key_is_acceptable = key in acceptable_keys # Only calculate once
          key_is_related = key in related_keys
          if key_is_acceptable or key_is_related:
            if key_is_related: # relation system has priority (ex. security_uid)
              # We must rename the key
              method_id = related_method[key]
              table_list = related_table_list[key]
              if not related_methods.has_key((table_list,method_id)):
                related_methods[(table_list,method_id)] = 1
              # Prepend renamed table name
              base_key = key
              key = "%s.%s" % (related_table_map[(table_list,method_id)][-1][-1], related_column[key])
              if base_key in keyword_search_keys:
                keyword_search_keys.append(key)
              if base_key in full_text_search_keys:
                full_text_search_keys.append(key)
            elif key_is_acceptable:
              if key.find('.') < 0:
                # if the key is only used by one table, just append its name
                if len(acceptable_key_map[key]) == 1 :
                  key = acceptable_key_map[key][0] + '.' + key
                # query_table specifies what table name should be used by default
                elif query_table and \
                    '%s.%s' % (query_table, key) in acceptable_keys:
                  key = query_table + '.' + key
                elif key == 'uid':
                  # uid is always ambiguous so we can only change it here
                  key = 'catalog.uid'
              # Add table to table dict
              from_table_dict[acceptable_key_map[key][0]] = acceptable_key_map[key][0] # We use catalog by default
            # Default case: variable equality
            if type(value) is type('') or isinstance(value, DateTime):
              # For security.
              value = self._quoteSQLString(value)
              if value != '' or not ignore_empty_string:
                # we consider empty string as Non Significant
                if value == '=':
                  # But we consider the sign = as empty string
                  value=''
                if '%' in value:
                  where_expression += ["%s LIKE '%s'" % (key, value)]
                elif value.startswith('>='):
                  where_expression += ["%s >= '%s'" % (key, value[2:])]
                elif value.startswith('<='):
                  where_expression += ["%s <= '%s'" % (key, value[2:])]
                elif value.startswith('>'):
                  where_expression += ["%s > '%s'" % (key, value[1:])]
                elif value.startswith('<'):
                  where_expression += ["%s < '%s'" % (key, value[1:])]
                elif value.startswith('!='):
                  where_expression += ["%s != '%s'" % (key, value[2:])]
                elif key in keyword_search_keys:
                  # We must add % in the request to simulate the catalog
                  where_expression += ["%s LIKE '%%%s%%'" % (key, value)]
                elif key in full_text_search_keys:
                  # We must add % in the request to simulate the catalog
                  where_expression += ["MATCH %s AGAINST ('%s')" % (key, value)]
                else:
                  where_expression += ["%s = '%s'" % (key, value)]
            elif type(value) is type([]) or type(value) is type(()):
              # We have to create an OR from tuple or list
              query_item = []
              for value_item in value:
                if value_item != '' or not ignore_empty_string:
                  # we consider empty string as Non Significant
                  # also for lists
                  if type(value_item) in (type(1), type(1.0),
                                          type(1991643034L)):
                    query_item += ["%s = %s" % (key, value_item)]
                  else:
                    # For security.
                    value_item = self._quoteSQLString(value_item)
                    if '%' in value_item:
                      query_item += ["%s LIKE '%s'" % (key, value_item)]
                    elif key in keyword_search_keys:
                      # We must add % in the request to simulate the catalog
                      query_item += ["%s LIKE '%%%s%%'" % (key, value_item)]
                    elif key in full_text_search_keys:
                      # We must add % in the request to simulate the catalog
                      query_item +=  ["MATCH %s AGAINST ('%s')" % (key, value)]
                    else:
                      query_item += ["%s = '%s'" % (key, value_item)]
              if len(query_item) > 0:
                where_expression += ['(%s)' % join(query_item, ' OR ')]
            elif type(value) is type({}):
              # We are in the case of a complex query
              query_item = []
              query_value = value['query']
              if type(query_value) != type([]) and type(query_value) != type(()) :
                query_value = [query_value]
              operator_value = sql_quote(value.get('operator', 'or'))
              range_value = value.get('range')

              if range_value :
                query_min = self._quoteSQLString(min(query_value))
                query_max = self._quoteSQLString(max(query_value))
                if range_value == 'min' :
                  query_item += ["%s >= '%s'" % (key, query_min) ]
                elif range_value == 'max' :
                  query_item += ["%s < '%s'" % (key, query_max) ]
                elif range_value == 'minmax' :
                  query_item += ["%s >= '%s' and %s < '%s'" % (key, query_min, key, query_max) ]
                elif range_value == 'minngt' :
                  query_item += ["%s >= '%s' and %s <= '%s'" % (key, query_min, key, query_max) ]
                elif range_value == 'ngt' :
                  query_item += ["%s <= '%s'" % (key, query_max) ]
              else :
                for query_value_item in query_value :
                  query_item += ['%s = %s' % (key, self._quoteSQLString(query_value_item))]
              if len(query_item) > 0:
                where_expression += ['(%s)' % join(query_item, ' %s ' % operator_value)]
            else:
              where_expression += ["%s = %s" % (key, self._quoteSQLString(value))]
          elif key in topic_search_keys:
            # ERP5 CPS compatibility
            topic_operator = 'or'
            if type(value) is type({}):
              topic_operator = sql_quote(value.get('operator', 'or'))
              value = value['query']
            if type(value) is type(''):
              topic_value = [value]
            else:
              topic_value = value # list or tuple
            query_item = []
            for topic_key in topic_value:
              if topic_key in acceptable_keys:
                if topic_key.find('.') < 0:
                  # if the key is only used by one table, just append its name
                  if len(acceptable_key_map[topic_key]) == 1 :
                    topic_key = '%s.%s' % (acceptable_key_map[topic_key][0], topic_key)
                  # query_table specifies what table name should be used
                  elif query_table:
                    topic_key = '%s.%s' % (query_table, topic_key)
                # Add table to table dict
                from_table_dict[acceptable_key_map[topic_key][0]] = acceptable_key_map[topic_key][0] # We use catalog by default
                query_item += ["%s = 1" % topic_key]
            # Join
            if len(query_item) > 0:
              where_expression += ['(%s)' % join(query_item, ' %s ' % topic_operator)]
      # Calculate extra where_expression based on required joins
      for k, tid in from_table_dict.items():
        if k != query_table:
          where_expression.append('%s.uid = %s.uid' % (query_table, tid))
      # Calculate extra where_expressions based on related definition
      for (table_list,method_id) in related_methods.keys():
        related_method = getattr(self, method_id, None)
        if related_method is not None:
          table_id = {'src__' : 1} # Return query source, do not evaluate
          table_id['query_table'] = query_table
          table_index = 0
          for t_tuple in related_table_map[(table_list,method_id)]:
            table_id['table_%s' % table_index] = t_tuple[1] # table_X is set to mapped id
            from_table_dict[t_tuple[1]] = t_tuple[0]
            table_index += 1
          where_expression.append(related_method(**table_id))
      # Concatenate where_expressions
      if kw.get('where_expression'):
        if len(where_expression) > 0:
          where_expression = "(%s) AND (%s)" % (kw['where_expression'], join(where_expression, ' AND ') )
      else:
        where_expression = join(where_expression, ' AND ')

      limit_expression = kw.get('limit', None)
      if type(limit_expression) in (type(()), type([])):
        limit_expression = '%s,%s' % (limit_expression[0], limit_expression[1])
      elif limit_expression is not None:
        limit_expression = str(limit_expression)

    # Use a dictionary at the moment.
    return { 'from_table_list' : from_table_dict.items(),
             'order_by_expression' : sort_on,
             'where_expression' : where_expression,
             'limit_expression' : limit_expression }

  def queryResults(self, sql_method, REQUEST=None, used=None, src__=0, **kw):
    """ Returns a list of brains from a set of constraints on variables """
    query = self.buildSQLQuery(REQUEST=REQUEST, **kw)
    kw['where_expression'] = query['where_expression']
    kw['sort_on'] = query['order_by_expression']
    kw['from_table_list'] = query['from_table_list']
    kw['limit_expression'] = query['limit_expression']
    # Return the result

    #LOG('acceptable_keys',0,'acceptable_keys: %s' % str(acceptable_keys))
    #LOG('acceptable_key_map',0,'acceptable_key_map: %s' % str(acceptable_key_map))
    #LOG('queryResults',0,'kw: %s' % str(kw))
    #LOG('queryResults',0,'from_table_list: %s' % str(from_table_dict.keys()))
    return sql_method(src__=src__, **kw)

  def searchResults(self, REQUEST=None, used=None, **kw):
    """ Builds a complex SQL where_expression to simulate ZCalatog behaviour """
    """ Returns a list of brains from a set of constraints on variables """
    # The used argument is deprecated and is ignored
    try:
      # Get the search method
      method = getattr(self, self.sql_search_results)
      # Return the result
      kw['used'] = used
      kw['REQUEST'] = REQUEST
      return self.queryResults(method, **kw)
    except ConflictError:
      raise
    except:
      LOG('SQLCatalog', WARNING, "could not search catalog", error=sys.exc_info())
      return []

  __call__ = searchResults

  def countResults(self, REQUEST=None, used=None, **kw):
    """ Builds a complex SQL where_expression to simulate ZCalatog behaviour """
    """ Returns the number of items which satisfy the where_expression """
    try:
      # Get the search method
      method = getattr(self, self.sql_count_results)
      # Return the result
      kw['used'] = used
      kw['REQUEST'] = REQUEST
      return self.queryResults(method, **kw)
    except ConflictError:
      raise
    except:
      LOG('SQLCatalog', WARNING, "could not count catalog", error=sys.exc_info())
      return [[0]]

  def recordObjectList(self, path_list, catalog=1):
    """
      Record the path of an object being catalogged or uncatalogged.
    """
    method = getattr(self, self.sql_record_object_list)
    method(path_list=path_list, catalog=catalog)

  def deleteRecordedObjectList(self, uid_list=()):
    """
      Delete all objects which contain any path.
    """
    method = getattr(self, self.sql_delete_recorded_object_list)
    method(uid_list=uid_list)

  def readRecordedObjectList(self, catalog=1):
    """
      Read objects. Note that this might not return all objects since ZMySQLDA limits the max rows.
    """
    method = getattr(self, self.sql_read_recorded_object_list)
    return method(catalog=catalog)

  # Filtering
  def manage_editFilter(self, REQUEST=None, RESPONSE=None, URL1=None):
    """
    This methods allows to set a filter on each zsql method called,
    so we can test if we should or not call a zsql method, so we can
    increase a lot the speed.
    """
    if withCMF:
      method_id_list = [zsql_method.id for zsql_method in self.getFilterableMethodList()]

      # Remove unused filters.
      for id in self.filter_dict.keys():
        if id not in method_id_list:
          del self.filter_dict[id]

      for id in method_id_list:
        # We will first look if the filter is activated
        if not self.filter_dict.has_key(id):
          self.filter_dict[id] = PersistentMapping()
          self.filter_dict[id]['filtered']=0
          self.filter_dict[id]['type']=[]
          self.filter_dict[id]['expression']=""
        if REQUEST.has_key('%s_box' % id):
          self.filter_dict[id]['filtered'] = 1
        else:
          self.filter_dict[id]['filtered'] = 0

        if REQUEST.has_key('%s_expression' % id):
          expression = REQUEST['%s_expression' % id]
          if expression == "":
            self.filter_dict[id]['expression'] = ""
            self.filter_dict[id]['expression_instance'] = None
          else:
            expr_instance = Expression(expression)
            self.filter_dict[id]['expression'] = expression
            self.filter_dict[id]['expression_instance'] = expr_instance
        else:
          self.filter_dict[id]['expression'] = ""
          self.filter_dict[id]['expression_instance'] = None

        if REQUEST.has_key('%s_type' % id):
          list_type = REQUEST['%s_type' % id]
          if type(list_type) is type('a'):
            list_type = [list_type]
          self.filter_dict[id]['type'] = list_type
        else:
          self.filter_dict[id]['type'] = []

    if RESPONSE and URL1:
      RESPONSE.redirect(URL1 + '/manage_catalogFilter?manage_tabs_message=Filter%20Changed')

  def isMethodFiltered(self, method_name):
    """
    Returns 1 if the method is already filtered,
    else it returns 0
    """
    if withCMF:
      # Reset Filtet dict
      # self.filter_dict= PersistentMapping()
      if not hasattr(self,'filter_dict'):
        self.filter_dict = PersistentMapping()
        return 0
      if self.filter_dict.has_key(method_name):
        return self.filter_dict[method_name]['filtered']
    return 0

  def getExpression(self, method_name):
    """
    Returns 1 if the method is already filtered,
    else it returns 0
    """
    if withCMF:
      if not hasattr(self,'filter_dict'):
        self.filter_dict = PersistentMapping()
        return ""
      if self.filter_dict.has_key(method_name):
        return self.filter_dict[method_name]['expression']
    return ""

  def getExpressionInstance(self, method_name):
    """
    Returns 1 if the method is already filtered,
    else it returns 0
    """
    if withCMF:
      if not hasattr(self,'filter_dict'):
        self.filter_dict = PersistentMapping()
        return None
      if self.filter_dict.has_key(method_name):
        return self.filter_dict[method_name]['expression_instance']
    return None

  def isPortalTypeSelected(self, method_name,portal_type):
    """
    Returns 1 if the method is already filtered,
    else it returns 0
    """
    if withCMF:
      if not hasattr(self,'filter_dict'):
        self.filter_dict = PersistentMapping()
        return 0
      if self.filter_dict.has_key(method_name):
        result = portal_type in (self.filter_dict[method_name]['type'])
        return result
    return 0


  def getFilterableMethodList(self):
    """
    Returns only zsql methods wich catalog or uncatalog objets
    """
    method_dict = {}
    if withCMF:
      methods = getattr(self,'sql_catalog_object',()) + \
                getattr(self,'sql_uncatalog_object',()) + \
                getattr(self,'sql_update_object',()) + \
                getattr(self,'sql_catalog_object_list',())
      for method_id in methods:
        method_dict[method_id] = 1
    method_list = map(lambda method_id: getattr(self, method_id, None), method_dict.keys())
    return filter(lambda method: method is not None, method_list)

  def getExpressionContext(self, ob):
      '''
      An expression context provides names for TALES expressions.
      '''
      if withCMF:
        data = {
            'here':         ob,
            'container':    aq_parent(aq_inner(ob)),
            'nothing':      None,
            #'root':         ob.getPhysicalRoot(),
            #'request':      getattr( ob, 'REQUEST', None ),
            #'modules':      SecureModuleImporter,
            #'user':         getSecurityManager().getUser(),
            'isDelivery':   ob.isDelivery, # XXX
            'isMovement':   ob.isMovement, # XXX
            'isPredicate':  ob.isPredicate, # XXX
            }
        return getEngine().getContext(data)


Globals.default__class_init__(Catalog)

class CatalogError(Exception): pass
