# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
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

import fnmatch, imp, os, re, shutil, sys
from Shared.DC.ZRDB.Connection import Connection as RDBConnection
from Products.ERP5Type.Globals import Persistent, PersistentMapping
from Acquisition import Implicit, aq_base
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.ERP5Type.Base import WorkflowMethod, _aq_reset
from Products.ERP5Type.Utils import readLocalDocument, \
                                    writeLocalDocument, \
                                    importLocalDocument, \
                                    removeLocalDocument
from Products.ERP5Type.Utils import readLocalPropertySheet, \
                                    writeLocalPropertySheet, \
                                    importLocalPropertySheet, \
                                    removeLocalPropertySheet
from Products.ERP5Type.Utils import readLocalConstraint, \
                                    writeLocalConstraint, \
                                    importLocalConstraint, \
                                    removeLocalConstraint
from Products.ERP5Type.Utils import readLocalExtension, \
                                    writeLocalExtension, \
                                    removeLocalExtension
from Products.ERP5Type.Utils import readLocalTest, \
                                    writeLocalTest, \
                                    removeLocalTest
from Products.ERP5Type.Utils import convertToUpperCase
from Products.ERP5Type import Permissions, PropertySheet
from Products.ERP5Type.XMLObject import XMLObject
from OFS.Traversable import NotFound
from OFS import SimpleItem, XMLExportImport
from cStringIO import StringIO
from copy import deepcopy
from zExceptions import BadRequest
import OFS.XMLExportImport
from Products.ERP5Type.patches.ppml import importXML
customImporters={
    XMLExportImport.magic: importXML,
    }

from zLOG import LOG, WARNING, PROBLEM
from warnings import warn
from gzip import GzipFile
from xml.dom.minidom import parse
from xml.sax.saxutils import escape
from Products.CMFCore.Expression import Expression
from Products.ERP5Type import tarfile
from urllib import quote, unquote
from difflib import unified_diff
import posixpath
import transaction

# those attributes from CatalogMethodTemplateItem are kept for
# backward compatibility
catalog_method_list = ('_is_catalog_list_method_archive',
                       '_is_uncatalog_method_archive',
                       '_is_clear_method_archive',
                       '_is_filtered_archive',)

catalog_method_filter_list = ('_filter_expression_archive',
                              '_filter_expression_instance_archive',
                              '_filter_type_archive',)

INSTALLED_BT_FOR_DIFF = 'installed_bt_for_diff'

def _getCatalog(acquisition_context):
  """
    Return the id of the SQLCatalog which correspond to the current BT.
  """
  catalog_method_id_list = acquisition_context.getTemplateCatalogMethodIdList()
  if len(catalog_method_id_list) == 0:
    try:
      return acquisition_context.getPortalObject().portal_catalog.objectIds('SQLCatalog')[0]
    except IndexError:
      return None
  catalog_method_id = catalog_method_id_list[0]
  return catalog_method_id.split('/')[0]

def _getCatalogValue(acquisition_context):
  """
    Returns the catalog object which correspond to the ZSQLMethods
    stored/to store in the business template.

    NB: acquisition_context must make possible to reach portal object
        and getTemplateCatalogMethodIdList.
  """
  catalog_id = _getCatalog(acquisition_context)
  if catalog_id is None:
    return None
  try:
    return acquisition_context.getPortalObject().portal_catalog[catalog_id]
  except KeyError:
    return None

def _recursiveRemoveUid(obj):
  """Recusivly set uid to None, to prevent (un)indexing.
  This is used to prevent unindexing real objects when we delete subobjects on
  a copy of this object.
  """
  if hasattr(aq_base(obj), 'uid'):
    obj.uid = None
  for subobj in obj.objectValues():
    _recursiveRemoveUid(subobj)

def removeAll(entry):
  warn('removeAll is deprecated; use shutil.rmtree instead.',
       DeprecationWarning)
  shutil.rmtree(entry, True)

def getChainByType(context):
  """
  This is used in order to construct the full list
  of mapping between type and list of workflow associated
  This is only useful in order to use
  portal_workflow.manage_changeWorkflows
  """
  pw = context.portal_workflow
  cbt = pw._chains_by_type
  ti = pw._listTypeInfo()
  types_info = []
  for t in ti:
    id = t.getId()
    title = t.Title()
    if title == id:
      title = None
    if cbt is not None and cbt.has_key(id):
      chain = ', '.join(cbt[id])
    else:
      chain = '(Default)'
    types_info.append({'id': id,
                      'title': title,
                      'chain': chain})
  new_dict = {}
  for item in types_info:
    new_dict['chain_%s' % item['id']] = item['chain']
  default_chain=', '.join(pw._default_chain)
  return (default_chain, new_dict)

def fixZSQLMethod(portal, method):
  """Make sure the ZSQLMethod uses a valid connection.
  """
  if not isinstance(getattr(portal, method.connection_id, None),
                      RDBConnection):
    # if not valid, we assign to the first valid connection found
    sql_connection_list = portal.objectIds(
                          spec=('Z MySQL Database Connection',))
    if (method.connection_id not in sql_connection_list) and \
       (len(sql_connection_list) != 0):
      LOG('BusinessTemplate', WARNING,
          'connection_id for Z SQL Method %s is invalid, using %s' % (
                    method.getId(), sql_connection_list[0]))
      method.connection_id = sql_connection_list[0]

def registerSkinFolder(skin_tool, skin_folder):
  request = skin_tool.REQUEST
  register_skin_selection = request.get('your_register_skin_selection', 1)
  reorder_skin_selection = request.get('your_reorder_skin_selection', 1)
  skin_layer_list = request.get('your_skin_layer_list', 
                                skin_tool.getSkinSelections()) 

  skin_folder_id = skin_folder.getId()

  try:
    skin_selection_list = skin_folder.getProperty(
                 'business_template_registered_skin_selections', 
                 skin_tool.getSkinSelections()
                 )
  except AttributeError:
    skin_selection_list = skin_tool.getSkinSelections()

  if isinstance(skin_selection_list, basestring):
    skin_selection_list = skin_selection_list.split()

  for skin_name in skin_selection_list:

    if (skin_name not in skin_tool.getSkinSelections()) and \
                                          register_skin_selection:
      createSkinSelection(skin_tool, skin_name)
      # add newly created skins to list of skins we care for 
      skin_layer_list.append(skin_name)

    selection = skin_tool.getSkinPath(skin_name) or ''
    selection_list = selection.split(',')
    if (skin_folder_id not in selection_list):
      selection_list.insert(0, skin_folder_id)
    if reorder_skin_selection:
      selection_list.sort(
        key=lambda x: x in skin_tool.objectIds() and skin_tool[x].getProperty(
        'business_template_skin_layer_priority', skin_tool[x].meta_type == 'Filesystem Directory View' and -1 or 0) or 0, reverse=True)
    if (skin_name in skin_layer_list):
      skin_tool.manage_skinLayers(skinpath=selection_list,
                                  skinname=skin_name, add_skin=1)
      skin_tool.getPortalObject().changeSkin(None)

def createSkinSelection(skin_tool, skin_name):
  # This skin selection does not exist, so we create a new one.
  # We'll initialize it with all skin folders, unless:
  #  - they explictly define a list of
  #    "business_template_registered_skin_selections", and we
  #    are not in this list.
  #  - they are not registred in the default skin selection
  skin_path = ''
  for skin_folder in skin_tool.objectValues():
    if skin_name in skin_folder.getProperty(
             'business_template_registered_skin_selections',
             (skin_name, )):
      if skin_folder.getId() in \
          skin_tool.getSkinPath(skin_tool.getDefaultSkin()):
        if skin_path:
          skin_path = '%s,%s' % (skin_path, skin_folder.getId())
        else:
          skin_path= skin_folder.getId()
  # add newly created skins to list of skins we care for 
  skin_tool.addSkinSelection(skin_name, skin_path)
  skin_tool.getPortalObject().changeSkin(None)

def deleteSkinSelection(skin_tool, skin_name):
  # Do not delete default skin
  if skin_tool.getDefaultSkin() != skin_name:

    skin_selection_registered = False
    for skin_folder in skin_tool.objectValues():
      try:
        skin_selection_list = skin_folder.getProperty(
               'business_template_registered_skin_selections', ())
        if skin_name in skin_selection_list:
          skin_selection_registered = True
          break
      except AttributeError:
        pass

    if (not skin_selection_registered):
      skin_tool.manage_skinLayers(chosen=[skin_name], 
                                  del_skin=1)
      skin_tool.getPortalObject().changeSkin(None)

def unregisterSkinFolder(skin_tool, skin_folder, skin_selection_list):
  skin_folder_id = skin_folder.getId()

  for skin_selection in skin_selection_list:
    selection = skin_tool.getSkinPath(skin_selection)
    selection = selection.split(',')
    if (skin_folder_id in selection):
      selection.remove(skin_folder_id)
      skin_tool.manage_skinLayers(skinpath=tuple(selection),
                                  skinname=skin_selection, add_skin=1)
      deleteSkinSelection(skin_tool, skin_selection)
      skin_tool.getPortalObject().changeSkin(None)

class BusinessTemplateArchive:
  """
    This is the base class for all Business Template archives
  """

  def __init__(self, creation=0, importing=0, file=None, path=None, **kw):
    if creation:
      self._initCreation(path=path, **kw)
    elif importing:
      self._initImport(file=file, path=path, **kw)

  def addFolder(self, **kw):
    pass

  def addObject(self, *kw):
    pass

  def finishCreation(self, **kw):
    pass

class BusinessTemplateFolder(BusinessTemplateArchive):
  """
    Class archiving business template into a folder tree
  """
  def _initCreation(self, path):
    self.path = path
    try:
      os.makedirs(self.path)
    except OSError:
      # folder already exists, remove it
      shutil.rmtree(self.path)
      os.makedirs(self.path)

  def addFolder(self, name=''):
    if name != '':
      name = os.path.normpath(name)
      path = os.path.join(self.path, name)
      if not os.path.exists(path):
        os.makedirs(path)
      return path

  def addObject(self, obj, name, path=None, ext='.xml'):
    name = name.replace('\\', '/')
    name = quote(name)
    name = os.path.normpath(name)
    if path is None:
      object_path = os.path.join(self.path, name)
    else:
      if '%' not in path:
        tail, path = os.path.splitdrive(path)
        path = path.replace('\\', '/')
        path = tail + quote(path)
      path = os.path.normpath(path)
      object_path = os.path.join(path, name)
    f = open(object_path+ext, 'wb')
    f.write(str(obj))
    f.close()

  def _initImport(self, file=None, path=None, **kw):
    # Normalize the paths to eliminate the effect of double-slashes.
    root_path_len = len(os.path.normpath(path)) + len(os.sep)
    self.root_path_len = root_path_len
    d = {}
    for f in file:
      f = os.path.normpath(f)
      klass = f[root_path_len:].split(os.sep, 1)[0]
      d.setdefault(klass, []).append(f)
    self.file_list_dict = d

  def importFiles(self, item, **kw):
    """
      Import file from a local folder
    """
    class_name = item.__class__.__name__
    root_path_len = self.root_path_len
    prefix_len = root_path_len + len(class_name) + len(os.sep)
    for file_path in self.file_list_dict.get(class_name, ()):
      if os.path.isfile(file_path):
        file = open(file_path, 'rb')
        try:
          file_name = file_path[prefix_len:]
          if '%' in file_name:
            file_name = unquote(file_name)
          item._importFile(file_name, file)
        finally:
          file.close()

class BusinessTemplateTarball(BusinessTemplateArchive):
  """
    Class archiving businnes template into a tarball file
  """

  def _initCreation(self, path):
    # make tmp dir, must use stringIO instead
    self.path = path
    try:
      os.makedirs(self.path)
    except OSError:
      # folder already exists, remove it
      shutil.rmtree(self.path)
      os.makedirs(self.path)
    # init tarfile obj
    self.fobj = StringIO()
    self.tar = tarfile.open('', 'w:gz', self.fobj)

  def addFolder(self, name=''):
    name = os.path.normpath(name)
    if not os.path.exists(name):
      os.makedirs(name)

  def addObject(self, obj, name, path=None, ext='.xml'):
    name = name.replace('\\', '/')
    name = quote(name)
    name = os.path.normpath(name)
    if path is None:
      object_path = os.path.join(self.path, name)
    else:
      if '%' not in path:
        tail, path = os.path.splitdrive(path)
        path = path.replace('\\', '/')
        path = tail + quote(path)
      path = os.path.normpath(path)
      object_path = os.path.join(path, name)
    f = open(object_path+ext, 'wb')
    f.write(str(obj))
    f.close()

  def finishCreation(self):
    self.tar.add(self.path)
    self.tar.close()
    shutil.rmtree(self.path)
    return self.fobj

  def _initImport(self, file=None, **kw):
    self.f = file

  def importFiles(self, item, **kw):
    """
      Import all file from the archive to the site
    """
    class_name = item.__class__.__name__
    self.f.seek(0)
    data = GzipFile(fileobj=self.f).read()
    io = StringIO(data)
    tar = tarfile.TarFile(fileobj=io)
    for info in tar.getmembers():
      if 'CVS' in info.name.split('/'):
        continue
      if '.svn' in info.name.split('/'):
        continue
      if class_name in info.name.split('/'):
        if info.isreg():
          file = tar.extractfile(info)
          tar_file_name = info.name.startswith('./') and info.name[2:] or \
              info.name
          folders = tar_file_name.split('/')
          file_name = ('/').join(folders[2:])
          if '%' in file_name:
            file_name = unquote(file_name)
          item._importFile(file_name, file)
          file.close()
    tar.close()
    io.close()

class TemplateConditionError(Exception): pass
class TemplateConflictError(Exception): pass
class BusinessTemplateMissingDependency(Exception): pass

class BaseTemplateItem(Implicit, Persistent):
  """
    This class is the base class for all template items.
    is_bt_for_diff means This BT is used to compare self temporary BT with installed BT
  """
  is_bt_for_diff = None

  def __init__(self, id_list, **kw):
    self.__dict__.update(kw)
    self._archive = PersistentMapping()
    self._objects = PersistentMapping()
    for id in id_list:
      if id is not None and id != '':
        self._archive[id] = None

  def build(self, context, **kw):
    pass

  def preinstall(self, context, installed_bt, **kw):
    """
      Build a list of added/removed/changed files between the BusinessTemplate
      being installed (self) and the installed one (installed_bt).
      Note : we compare files between BTs, *not* between the installed BT and
      the objects in the DataFS.

      XXX: -12 used here is -len('TemplateItem')
    """
    modified_object_list = {}
    if context.getTemplateFormatVersion() == 1:
      new_keys = self._objects.keys()
      for path in new_keys:
        if installed_bt._objects.has_key(path):
          # compare objects to see it there are changes
          new_obj_xml = self.generateXml(path=path)
          old_obj_xml = installed_bt.generateXml(path=path)
          if new_obj_xml != old_obj_xml:
            modified_object_list.update({path : ['Modified', self.__class__.__name__[:-12]]})
          # else, compared versions are identical, don't overwrite the old one
        else: # new object
          modified_object_list.update({path : ['New', self.__class__.__name__[:-12]]})
      # list removed objects
      old_keys = installed_bt._objects.keys()
      for path in old_keys:
        if path not in new_keys:
          modified_object_list.update({path : ['Removed', self.__class__.__name__[:-12]]})
    return modified_object_list

  def install(self, context, trashbin, **kw):
    pass

  def uninstall(self, context, **kw):
    pass

  def remove(self, context, **kw):
    """
      If 'remove' is chosen on an object containing subobjects, all the
      subobjects will be removed too, even if 'backup' or 'keep' was chosen for
      the subobjects.
      Likewise, for 'save_and_remove' : subobjects will get saved too.
    """
    remove_dict = kw.get('remove_object_dict', {})
    keys = self._objects.keys()
    keys.sort()
    keys.reverse()
    # if you choose remove, the object and all its subobjects will be removed
    # even if you choose backup or keep for subobjects
    # it is same behaviour for backup_and_remove, all we be save
    for path in keys:
      if remove_dict.has_key(path):
        action = remove_dict[path]
        if action == 'save_and_remove':
          # like trash
          self.uninstall(context, trash=1, object_path=path, **kw)
        elif action == 'remove':
          self.uninstall(context, trash=0, object_path=path, **kw)
        else:
          # As the list of available actions is not strictly defined,
          # prevent mistake if an action is not handled
          raise ValueError, 'Unknown action "%s"' % action


  def trash(self, context, new_item, **kw):
    # trash is quite similar to uninstall.
    return self.uninstall(context, new_item=new_item, trash=1, **kw)

  def export(self, context, bta, **kw):
    pass

  def getKeys(self):
    return self._objects.keys()

  def importFile(self, bta, **kw):
    bta.importFiles(item=self)

  def removeProperties(self, obj):
    """
    Remove unneeded properties for export
    """
    meta_type = getattr(aq_base(obj), 'meta_type', None)

    attr_list = [ '_dav_writelocks', '_filepath', '_owner', 'uid',
                  'workflow_history', '__ac_local_roles__' ]
    attr_list += {
        'Script (Python)': ('_lazy_compilation', 'Python_magic'),
      }.get(meta_type, ())

    for attr in attr_list:
      if attr in obj.__dict__:
        delattr(obj, attr)

    if meta_type == 'ERP5 PDF Form':
      if not obj.getProperty('business_template_include_content', 1):
        obj.deletePdfContent()
    elif meta_type == 'Script (Python)':
      obj._code = None
    return obj

class ObjectTemplateItem(BaseTemplateItem):
  """
    This class is used for generic objects and as a subclass.
  """

  def __init__(self, id_list, tool_id=None, **kw):
    BaseTemplateItem.__init__(self, id_list, tool_id=tool_id, **kw)
    if tool_id is not None:
      id_list = self._archive.keys()
      self._archive.clear()
      for id in id_list :
        if id != '':
          self._archive["%s/%s" % (tool_id, id)] = None

  def export(self, context, bta, **kw):
    """
      Export the business template : fill the BusinessTemplateArchive with
      objects exported as XML, hierarchicaly organised.
    """
    if len(self._objects.keys()) == 0:
      return
    root_path = os.path.join(bta.path, self.__class__.__name__)
    for key, obj in self._objects.iteritems():
      # create folder and subfolders
      folders, id = posixpath.split(key)
      encode_folders = []
      for folder in folders.split('/'):
        if '%' not in folder:
          encode_folders.append(quote(folder))
        else:
          encode_folders.append(folder)
      path = os.path.join(root_path, (os.sep).join(encode_folders))
      bta.addFolder(name=path)
      # export object in xml
      f=StringIO()
      XMLExportImport.exportXML(obj._p_jar, obj._p_oid, f)
      bta.addObject(obj=f.getvalue(), name=id, path=path)

  def build_sub_objects(self, context, id_list, url, **kw):
    # XXX duplicates code from build
    p = context.getPortalObject()
    sub_list = {}
    for id in id_list:
      relative_url = '/'.join([url,id])
      obj = p.unrestrictedTraverse(relative_url)
      obj = obj._getCopy(context)
      obj = self.removeProperties(obj)
      id_list = obj.objectIds() # FIXME duplicated variable name
      if hasattr(aq_base(obj), 'groups'): # XXX should check metatype instead
        # we must keep groups because they are deleted along with subobjects
        groups = deepcopy(obj.groups)
      if id_list:
        self.build_sub_objects(context, id_list, relative_url)
        for id_ in list(id_list):
          obj._delObject(id_)
      if hasattr(aq_base(obj), 'groups'):
        obj.groups = groups
      self._objects[relative_url] = obj
      obj.wl_clearLocks()
    return sub_list

  def build(self, context, **kw):
    BaseTemplateItem.build(self, context, **kw)
    p = context.getPortalObject()
    for relative_url in self._archive.keys():
      try:
        obj = p.unrestrictedTraverse(relative_url)
      except ValueError:
        raise ValueError, "Can not access to %s" % relative_url
      try:
        obj = obj._getCopy(context)
      except AttributeError:
        raise AttributeError, "Could not find object '%s' during business template processing." % relative_url
      _recursiveRemoveUid(obj)
      obj = self.removeProperties(obj)
      id_list = obj.objectIds()
      if hasattr(aq_base(obj), 'groups'): # XXX should check metatype instead
        # we must keep groups because they are deleted along with subobjects
        groups = deepcopy(obj.groups)
      if len(id_list) > 0:
        self.build_sub_objects(context, id_list, relative_url)
        for id_ in list(id_list):
          obj._delObject(id_)
      if hasattr(aq_base(obj), 'groups'):
        obj.groups = groups
      self._objects[relative_url] = obj
      obj.wl_clearLocks()

  def _compileXML(self, file):
      name, ext = os.path.splitext(file.name)
      compiled_file = name + '.zexp'
      if not os.path.exists(compiled_file) or os.path.getmtime(file.name) > os.path.getmtime(compiled_file):
          LOG('Business Template', 0, 'Compiling %s to %s...' % (file.name, compiled_file))
          try:
              from Shared.DC.xml import ppml
              from OFS.XMLExportImport import start_zopedata, save_record, save_zopedata
              import pyexpat
              outfile=open(compiled_file, 'wb')
              try:
                  data=file.read()
                  F=ppml.xmlPickler()
                  F.end_handlers['record'] = save_record
                  F.end_handlers['ZopeData'] = save_zopedata
                  F.start_handlers['ZopeData'] = start_zopedata
                  F.binary=1
                  F.file=outfile
                  p=pyexpat.ParserCreate()
                  p.CharacterDataHandler=F.handle_data
                  p.StartElementHandler=F.unknown_starttag
                  p.EndElementHandler=F.unknown_endtag
                  r=p.Parse(data)
              finally:
                  outfile.close()
          except:
              if os.path.exists(compiled_file):
                  os.remove(compiled_file)
              raise
      return open(compiled_file)

  def _importFile(self, file_name, file_obj):
    # import xml file
    if not file_name.endswith('.xml'):
      if not file_name.endswith('.zexp'):
        LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    obj = self
    connection = None
    while connection is None:
      obj=obj.aq_parent
      connection=obj._p_jar
    __traceback_info__ = 'Importing %s' % file_name
    # The pre-compilation hack is disabled, because the design is not
    # nice. Do not enable it without yo's approval.
    if 0:
      if isinstance(file_obj, file):
        obj = connection.importFile(self._compileXML(file_obj))
      else:
        obj = connection.importFile(file_obj, customImporters=customImporters)
    else:
      # FIXME: Why not use the importXML function directly? Are there any BT5s
      # with actual .zexp files on the wild?
      obj = connection.importFile(file_obj, customImporters=customImporters)
    self.removeProperties(obj)
    self._objects[file_name[:-4]] = obj

  def preinstall(self, context, installed_bt, **kw):
    modified_object_list = {}
    if context.getTemplateFormatVersion() == 1:
      upgrade_list = []
      type_name = self.__class__.__name__.split('TemplateItem')[-2]
      for path in self._objects:
        if installed_bt._objects.has_key(path):
          upgrade_list.append((path,
            self.removeProperties(installed_bt._objects[path])))
        else: # new object
          modified_object_list[path] = 'New', type_name
      # update _p_jar property of objects cleaned by removeProperties
      transaction.savepoint(optimistic=True)
      for path, old_object in upgrade_list:
        # compare object to see it there is changes
        new_object = self._objects[path]
        new_io = StringIO()
        old_io = StringIO()
        OFS.XMLExportImport.exportXML(new_object._p_jar, new_object._p_oid, new_io)
        OFS.XMLExportImport.exportXML(old_object._p_jar, old_object._p_oid, old_io)
        new_obj_xml = new_io.getvalue()
        old_obj_xml = old_io.getvalue()
        new_io.close()
        old_io.close()
        if new_obj_xml != old_obj_xml:
          modified_object_list[path] = 'Modified', type_name
      # get removed object
      for path in set(installed_bt._objects) - set(self._objects):
        modified_object_list[path] = 'Removed', type_name
    return modified_object_list

  def _backupObject(self, action, trashbin, container_path, object_id, **kw):
    """
      Backup the object in portal trash if necessery and return its subobjects
    """
    subobjects_dict = {}
    if trashbin is None: # must return subobjects
      object_path = container_path + [object_id]
      obj = self.unrestrictedTraverse(object_path)
      for subobject_id in list(obj.objectIds()):
        subobject_path = object_path + [subobject_id]
        subobject = self.unrestrictedTraverse(subobject_path)
        subobject_copy = subobject._p_jar.exportFile(subobject._p_oid)
        subobjects_dict[subobject_id] = subobject_copy
      return subobjects_dict
    # XXX btsave is for backward compatibility
    if action == 'backup' or action == 'btsave':
      subobjects_dict = self.portal_trash.backupObject(trashbin, container_path, object_id, save=1, **kw)
    elif action == 'install':
      subobjects_dict = self.portal_trash.backupObject(trashbin, container_path, object_id, save=0, **kw)
    else:
      # As the list of available actions is not strictly defined,
      # prevent mistake if an action is not handled
      raise ValueError, 'Unknown action "%s"' % action
    return subobjects_dict

  def beforeInstall(self):
    """
      Installation hook.
      Called right at the begining of "install" method.
      Can be overridden by subclasses.
    """
    pass

  def afterInstall(self):
    """
      Installation hook.
      Called right before returning in "install" method.
      Can be overridden by subclasses.
    """
    pass

  def onNewObject(self):
    """
      Installation hook.
      Called when installation process determined that object to install is
      new on current site (it's not replacing an existing object).
      Can be overridden by subclasses.
    """
    pass

  def install(self, context, trashbin, **kw):
    self.beforeInstall()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    if context.getTemplateFormatVersion() == 1:
      def recurse(hook, document, prefix=''):
        my_prefix = '%s/%s' % (prefix, document.id)
        if (hook(document, my_prefix)):
          for subdocument in document.objectValues():
            recurse(hook, subdocument, my_prefix)
      def saveHook(document, prefix):
        uid = getattr(document, 'uid', None)
        if uid is None:
          return 0
        else:
          saved_uid_dict[prefix] = uid
          return 1
      def restoreHook(document, prefix):
        uid = saved_uid_dict.get(prefix)
        if uid is None:
          return 0
        else:
          document.uid = uid
          return 1
      groups = {}
      old_groups = {}
      portal = context.getPortalObject()
      # sort to add objects before their subobjects
      keys = self._objects.keys()
      keys.sort()
      # Postpone indexations after unindexations.
      # This avoids alarming error messages about a single uid being used
      # by "deleted" path and reindexed object. This can happen here for
      # objects on which the uid was restored: previous object was deleted,
      # hence the "deleted" path, and new object does have the same uid.
      original_reindex_parameters = context.getPlacelessDefaultReindexParameters()
      if original_reindex_parameters is None:
        original_reindex_parameters = {}
      activate_kw = original_reindex_parameters.get('activate_kw', {}).copy()
      activate_kw['after_method_id'] = 'unindexObject'
      context.setPlacelessDefaultReindexParameters(activate_kw=activate_kw, **original_reindex_parameters)
      for path in keys:
        if update_dict.has_key(path) or force:
          # get action for the oject
          action = 'backup'
          if not force:
            action = update_dict[path]
            if action == 'nothing':
              continue
          # get subobjects in path
          path_list = path.split('/')
          container_path = path_list[:-1]
          object_id = path_list[-1]
          try:
            container = portal.unrestrictedTraverse(container_path)
          except KeyError:
            # parent object can be set to nothing, in this case just go on
            container_url = '/'.join(container_path)
            if update_dict.get(container_url) == 'nothing':
              continue
            # If container's container is portal_catalog,
            # then automatically create the container.
            elif len(container_path) > 1 and container_path[-2] == 'portal_catalog':
              # The id match, but better double check with the meta type
              # while avoiding the impact of systematic check
              container_container = portal.unrestrictedTraverse(container_path[:-1])
              if container_container.meta_type == 'ERP5 Catalog':
                container_container.manage_addProduct['ZSQLCatalog'].manage_addSQLCatalog(id=container_path[-1], title='')
                if len(container_container.objectIds()) == 1:
                  container_container.default_sql_catalog_id = container_path[-1]
                container = portal.unrestrictedTraverse(container_path)
            else:
              raise
          saved_uid_dict = {}
          subobjects_dict = {}
          portal_type_dict = {}
          # Object already exists
          old_obj = container._getOb(object_id, None)
          if old_obj is not None:
            recurse(saveHook, old_obj)
            if getattr(aq_base(old_obj), 'groups', None) is not None:
              # we must keep original order groups
              # from old form in case we keep some
              # old widget, thus we can readd them in
              # the right order group
              old_groups[path] = deepcopy(old_obj.groups)
            subobjects_dict = self._backupObject(action, trashbin,
                                                 container_path, object_id)
            # in case of portal types, we want to keep some properties
            if getattr(old_obj, 'meta_type', None) == 'ERP5 Base Type':
              for attr in ('allowed_content_types',
                           'hidden_content_type_list',
                           'property_sheet_list',
                           'base_category_list'):
                portal_type_dict[attr] = getattr(old_obj, attr, ())
              portal_type_dict['workflow_chain'] = \
                getChainByType(context)[1].get('chain_' + object_id, '')
            container.manage_delObjects([object_id])
          else:
            self.onNewObject()
          # install object
          obj = self._objects[path]
          if getattr(obj, 'meta_type', None) == 'Script (Python)':
            if getattr(obj, '_code') is None:
              obj._compile()
          if getattr(aq_base(obj), 'groups', None) is not None:
            # we must keep original order groups
            # because they change when we add subobjects
            groups[path] = deepcopy(obj.groups)
          # copy the object
          if (getattr(aq_base(obj), '_mt_index', None) is not None and
              obj._count() == 0):
            # some btrees were exported in a corrupted state. They're empty but
            # their metadata-index (._mt_index) contains entries which in
            # Zope 2.12 are used for .objectIds(), .objectValues() and
            # .objectItems(). In these cases, force the 
            LOG('Products.ERP5.Document.BusinessTemplate', WARNING,
                'Cleaning corrupt BTreeFolder2 object at %r.' % (path,))
            obj._initBTrees()
          obj = obj._getCopy(container)
          try:
            container._setObject(object_id, obj)
          except AttributeError:
            LOG("BT, install", 0, object_id)
            raise
          obj = container._getOb(object_id)
          # mark a business template installation so in 'PortalType_afterClone' scripts
          # we can implement logical for reseting or not attributes (i.e reference).
          self.REQUEST.set('is_business_template_installation', 1)
          # We set isIndexable to 0 before calling
          # manage_afterClone in order to not call recursiveReindex, this is
          # useless because we will already reindex every created object, so
          # we avoid duplication of reindexation
          obj.isIndexable = 0
          obj.manage_afterClone(obj)
          del obj.isIndexable
          if getattr(aq_base(obj), 'reindexObject', None) is not None:
            obj.reindexObject()
          obj.wl_clearLocks()
          if portal_type_dict:
            # set workflow chain
            wf_chain = portal_type_dict.pop('workflow_chain')
            chain_dict = getChainByType(context)[1]
            default_chain = ''
            chain_dict['chain_%s' % (object_id)] = wf_chain
            context.portal_workflow.manage_changeWorkflows(default_chain, props=chain_dict)
            # restore some other properties
            obj.__dict__.update(portal_type_dict)
          # import sub objects if there is
          if subobjects_dict:
            # get a jar
            connection = obj._p_jar
            o = obj
            while connection is None:
              o = o.aq_parent
              connection = o._p_jar
            # import subobjects
            for subobject_id, subobject_data in subobjects_dict.iteritems():
              try:
                if obj._getOb(subobject_id, None) is None:
                  subobject_data.seek(0)
                  subobject = connection.importFile(subobject_data)
                  obj._setObject(subobject_id, subobject)
              except AttributeError:
                # XXX this may happen when an object which can contain
                # sub-objects (e.g. ERP5 Form) has been replaced with
                # an object which cannot (e.g. External Method).
                LOG('BusinessTemplate', WARNING,
                    'could not restore %r in %r' % (subobject_id, obj))
          if obj.meta_type in ('Z SQL Method',):
            fixZSQLMethod(portal, obj)
          # portal transforms specific initialization
          elif obj.meta_type in ('Transform', 'TransformsChain'):
            assert container.meta_type == 'Portal Transforms'
            # skip transforms that couldn't have been initialized
            if obj.title != 'BROKEN':
              container._mapTransform(obj)
          elif obj.meta_type in ('ERP5 Ram Cache',
                                 'ERP5 Distributed Ram Cache',):
            assert container.meta_type == 'ERP5 Cache Factory'
            container.getParentValue().updateCache()
          elif (container.meta_type == 'CMF Skins Tool') and \
              (old_obj is not None):
            # Keep compatibility with previous export format of
            # business_template_registered_skin_selections
            # and do not modify exported value
            if obj.getProperty('business_template_registered_skin_selections', 
                               None) is None:
              # Keep previous value of register skin selection for skin folder
              skin_selection_list = old_obj.getProperty(
                  'business_template_registered_skin_selections', None)
              if skin_selection_list is not None:
                if isinstance(skin_selection_list, basestring):
                  skin_selection_list = skin_selection_list.split(' ')
                obj._setProperty(
                    'business_template_registered_skin_selections',
                    skin_selection_list, type='tokens')
           
          recurse(restoreHook, obj)
      # now put original order group
      # we remove object not added in forms
      # we put old objects we have kept
      for path, new_groups_dict in groups.iteritems():
        if not old_groups.has_key(path):
          # installation of a new form
          obj = portal.unrestrictedTraverse(path)
          obj.groups = new_groups_dict
        else:
          # upgrade of a form
          old_groups_dict = old_groups[path]
          obj = portal.unrestrictedTraverse(path)
          # first check that all widgets are in new order
          # excetp the one that had to be removed
          widget_id_list = obj.objectIds()
          for widget_id in widget_id_list:
            widget_path = path+'/'+widget_id
            if update_dict.has_key(widget_path) and update_dict[widget_path] in ('remove', 'save_and_remove'):
              continue
            widget_in_form = 0
            for group_id, group_value_list in new_groups_dict.iteritems():
              if widget_id in group_value_list:
                widget_in_form = 1
                break
            # if not, add it in the same groups
            # defined on the former form
            previous_group_id = None
            if not widget_in_form:
              for old_group_id, old_group_values in old_groups_dict.iteritems():
                if widget_id in old_group_values:
                  previous_group_id = old_group_id
              # if we find same group in new one, add widget to it
              if previous_group_id is not None and new_groups_dict.has_key(previous_group_id):
                new_groups_dict[previous_group_id].append(widget_id)
              # otherwise use a specific group
              else:
                if new_groups_dict.has_key('not_assigned'):
                  new_groups_dict['not_assigned'].append(widget_id)
                else:
                  new_groups_dict['not_assigned'] = [widget_id,]
                  obj.group_list = list(obj.group_list) + ['not_assigned']
          # second check all widget_id in order are in form
          for group_id, group_value_list in new_groups_dict.iteritems():
            for widget_id in tuple(group_value_list):
              if widget_id not in widget_id_list:
                # if we don't find the widget id in the form
                # remove it fro the group
                group_value_list.remove(widget_id)
          # now set new group object
          obj.groups = new_groups_dict
      # Remove after_method_id
      context.setPlacelessDefaultReindexParameters(**original_reindex_parameters)
    else:
      # for old business template format
      BaseTemplateItem.install(self, context, trashbin, **kw)
      portal = context.getPortalObject()
      for relative_url in self._archive.keys():
        obj = self._archive[relative_url]
        container_path = relative_url.split('/')[0:-1]
        object_id = relative_url.split('/')[-1]
        container = portal.unrestrictedTraverse(container_path)
        container_ids = container.objectIds()
        if object_id in container_ids:    # Object already exists
          self._backupObject('backup', trashbin, container_path, object_id)
          container.manage_delObjects([object_id])
        # Set a hard link
        obj = obj._getCopy(container)
        container._setObject(object_id, obj)
        obj = container._getOb(object_id)
        obj.manage_afterClone(obj)
        obj.wl_clearLocks()
        if obj.meta_type in ('Z SQL Method',):
          fixZSQLMethod(portal, obj)
    self.afterInstall()

  def uninstall(self, context, **kw):
    portal = context.getPortalObject()
    trash = kw.get('trash', 0)
    trashbin = kw.get('trashbin', None)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for relative_url in object_keys:
      container_path = relative_url.split('/')[0:-1]
      object_id = relative_url.split('/')[-1]
      try:
        container = portal.unrestrictedTraverse(container_path)
        object = container._getOb(object_id) # We force access to the object to be sure
                                        # that appropriate exception is thrown
                                        # in case object is already backup and/or removed
        if trash and trashbin is not None:
          self.portal_trash.backupObject(trashbin, container_path, object_id, save=1, keep_subobjects=1)
        if container.meta_type == 'CMF Skins Tool':
          # we are removing a skin folder, check and 
          # remove if registered skin selection
          skin_folder = container[object_id]
          unregisterSkinFolder(container, skin_folder,
              container.getSkinSelections())

        container.manage_delObjects([object_id])
        if container.aq_parent.meta_type == 'ERP5 Catalog' and len(container.objectIds()) == 0:
          # We are removing a ZSQLMethod, remove the SQLCatalog if empty
          container.getParentValue().manage_delObjects([container.id])
      except (NotFound, KeyError, BadRequest, AttributeError):
        # object is already backup and/or removed
        pass
    BaseTemplateItem.uninstall(self, context, **kw)

class PathTemplateItem(ObjectTemplateItem):
  """
    This class is used to store objects with wildcards supported.
  """
  def __init__(self, id_list, tool_id=None, **kw):
    BaseTemplateItem.__init__(self, id_list, tool_id=tool_id, **kw)
    id_list = self._archive.keys()
    self._archive.clear()
    self._path_archive = PersistentMapping()
    for id in id_list:
      self._path_archive[id] = None

  def uninstall(self, context, **kw):
    portal = context.getPortalObject()
    trash = kw.get('trash', 0)
    trashbin = kw.get('trashbin', None)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._path_archive.keys()
    object_keys.sort()
    object_keys.reverse()
    p = context.getPortalObject()
    for path in object_keys:
      try:
        path_list = self._resolvePath(p, [], path.split('/'))
      except AttributeError:
        # path seems to not exist anymore
        continue
      path_list.sort()
      path_list.reverse()
      for relative_url in path_list:
        try:
          container_path = relative_url.split('/')[0:-1]
          object_id = relative_url.split('/')[-1]
          container = portal.unrestrictedTraverse(container_path)
          if trash and trashbin is not None:
            self.portal_trash.backupObject(trashbin, container_path,
                                           object_id, save=1,
                                           keep_subobjects=1)
          container.manage_delObjects([object_id])
        except (NotFound, KeyError):
          # object is already backup and/or removed
          pass
    BaseTemplateItem.uninstall(self, context, **kw)

  def _resolvePath(self, folder, relative_url_list, id_list):
    """
      This method calls itself recursively.

      The folder is the current object which contains sub-objects.
      The list of ids are path components. If the list is empty,
      the current folder is valid.
    """
    if len(id_list) == 0:
      return ['/'.join(relative_url_list)]
    id = id_list[0]
    if re.search('[\*\?\[\]]', id) is None:
      # If the id has no meta character, do not have to check all objects.
      obj = folder._getOb(id, None)
      if obj is None:
        raise AttributeError, "Could not resolve '%s' during business template processing." % id
      return self._resolvePath(obj, relative_url_list + [id], id_list[1:])
    path_list = []
    for object_id in fnmatch.filter(folder.objectIds(), id):
      if object_id != "":
        path_list.extend(self._resolvePath(
            folder._getOb(object_id),
            relative_url_list + [object_id], id_list[1:]))
    return path_list

  def build(self, context, **kw):
    BaseTemplateItem.build(self, context, **kw)
    p = context.getPortalObject()
    keys = self._path_archive.keys()
    keys.sort()
    for path in keys:
      include_subobjects = 0
      if '**' in path:
        include_subobjects = 1
      for relative_url in self._resolvePath(p, [], path.split('/')):
        obj = p.unrestrictedTraverse(relative_url)
        obj = obj._getCopy(context)
        obj = obj.__of__(context)
        _recursiveRemoveUid(obj)
        id_list = obj.objectIds()
        obj = self.removeProperties(obj)
        if hasattr(aq_base(obj), 'groups'):
          # we must keep groups because it's ereased when we delete subobjects
          groups = deepcopy(obj.groups)
        if len(id_list) > 0:
          if include_subobjects:
            self.build_sub_objects(context, id_list, relative_url)
          for id_ in list(id_list):
            obj._delObject(id_)
        if hasattr(aq_base(obj), 'groups'):
          obj.groups = groups
        self._objects[relative_url] = obj
        obj.wl_clearLocks()

class ToolTemplateItem(PathTemplateItem):
  """This class is used only for making a distinction between other objects
  and tools, because tools may not be backed up."""
  def _backupObject(self, action, trashbin, container_path, object_id, **kw):
    """Fake as if a trashbin is not available."""
    return PathTemplateItem._backupObject(self, action, None, container_path,
                                          object_id, **kw)

class PreferenceTemplateItem(PathTemplateItem):
  """
  This class is used to store preference objects
  """
  def _resolvePath(self, folder, relative_url_list, id_list):
    """
    This method calls itself recursively.

    The folder is the current object which contains sub-objects.
    The list of ids are path components. If the list is empty,
    the current folder is valid.
    """
    if relative_url_list != []:
      LOG("PreferenceTemplateItem, _resolvePath", WARNING,
          "Should be empty")
    if len(id_list) != 1:
      LOG("PreferenceTemplateItem, _resolvePath", WARNING,
          "Should contain only one element")
    # XXX hardcoded
    return ['portal_preferences/%s' % id_list[0]]

  def install(self, context, trashbin, **kw):
    """
    Enable Preference
    """
    PathTemplateItem.install(self, context, trashbin, **kw)
    portal = context.getPortalObject()
    for object_path in self._objects.keys():
      pref = portal.unrestrictedTraverse(object_path)
      # XXX getPreferenceState is a bad name
      if pref.getPreferenceState() == 'disabled':
        portal.portal_workflow.doActionFor(
                      pref,
                      'enable_action',
                      comment="Initialized during Business Template " \
                              "installation.")

class CategoryTemplateItem(ObjectTemplateItem):

  def __init__(self, id_list, tool_id='portal_categories', **kw):
    ObjectTemplateItem.__init__(self, id_list, tool_id=tool_id, **kw)

  def build_sub_objects(self, context, id_list, url, **kw):
    p = context.getPortalObject()
    for id in id_list:
      relative_url = '/'.join([url,id])
      obj = p.unrestrictedTraverse(relative_url)
      obj = obj._getCopy(context)
      obj = self.removeProperties(obj)
      id_list = obj.objectIds()
      if id_list:
        self.build_sub_objects(context, id_list, relative_url)
        for id_ in list(id_list):
          obj._delObject(id_)
      self._objects[relative_url] = obj
      obj.wl_clearLocks()

  def build(self, context, **kw):
    BaseTemplateItem.build(self, context, **kw)
    p = context.getPortalObject()
    for relative_url in self._archive.keys():
      obj = p.unrestrictedTraverse(relative_url)
      obj = obj._getCopy(context)
      _recursiveRemoveUid(obj)
      obj = self.removeProperties(obj)
      include_sub_categories = obj.__of__(context).getProperty('business_template_include_sub_categories', 0)
      id_list = obj.objectIds()
      if len(id_list) > 0 and include_sub_categories:
        self.build_sub_objects(context, id_list, relative_url)
        for id_ in list(id_list):
          obj._delObject(id_)
      else:
        for id_ in list(id_list):
          obj._delObject(id_)
      self._objects[relative_url] = obj
      obj.wl_clearLocks()

  def beforeInstall(self):
    self._installed_new_category = False

  def onNewObject(self):
    self._installed_new_category = True

  def afterInstall(self):
    if self._installed_new_category:
      # reset accessors if we installed a new category
      _aq_reset()

class SkinTemplateItem(ObjectTemplateItem):

  def __init__(self, id_list, tool_id='portal_skins', **kw):
    ObjectTemplateItem.__init__(self, id_list, tool_id=tool_id, **kw)

  def build(self, context, **kw):
    ObjectTemplateItem.build(self, context, **kw)
    for relative_url in self._objects.keys():
      obj = self._objects[relative_url]
      if (getattr(obj, 'meta_type', None) == 'Folder') and \
        (obj.getProperty('business_template_registered_skin_selections', None) \
            is not None):
          obj._delProperty(
              'business_template_registered_skin_selections')

  def preinstall(self, context, installed_bt, **kw):
    modified_object_list = ObjectTemplateItem.preinstall(self, context, installed_bt, **kw)
    # We must install/update an ERP5 Form if one of its widget is modified.
    # This allow to keep the widget order and the form layout after an update
    #   from a BT to another one.
    for (bt_obj_path, bt_obj) in self._objects.items():
      if getattr(bt_obj, 'meta_type', None) == 'ERP5 Form':
        # search sub-objects of ERP5 Forms that are marked as "modified"
        for upd_obj_path in modified_object_list.keys():
          if upd_obj_path.startswith(bt_obj_path):
            # a child of the ERP5 Form must be updated, so the form too
            if not modified_object_list.has_key(bt_obj_path):
              modified_object_list.update({bt_obj_path: ['Modified', self.__class__.__name__[:-12]]})
    return modified_object_list

  def install(self, context, trashbin, **kw):
    ObjectTemplateItem.install(self, context, trashbin, **kw)
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    p = context.getPortalObject()
    skin_tool = p.portal_skins
    for relative_url in self._archive.keys():
      folder = p.unrestrictedTraverse(relative_url)
      for obj in folder.objectValues(spec=('Z SQL Method',)):
        fixZSQLMethod(p, obj)

      # Do not register skin which were explicitely ask not to be installed
      if context.getTemplateFormatVersion() == 1:
        if update_dict.has_key(relative_url) or force:
          if not force:
            if update_dict[relative_url] == 'nothing':
              continue
      if folder.aq_parent.meta_type == 'CMF Skins Tool':
        registerSkinFolder(skin_tool, folder)

class RegisteredSkinSelectionTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    portal = context.getPortalObject()
    skin_tool = getToolByName(portal, 'portal_skins')

    for key in self._archive.keys():
      skin_folder_id, skin_selection_id = key.split(' | ')

      skin_folder = skin_tool[skin_folder_id]
      selection_list = skin_folder.getProperty(
          'business_template_registered_skin_selections',
          [])
      if skin_selection_id in selection_list:
        if self._objects.has_key(skin_folder_id):
          self._objects[skin_folder_id].append(skin_selection_id)
        else:
          self._objects[skin_folder_id] = [skin_selection_id]
      else:
        raise NotFound, 'No skin selection %s found for skin folder %s.' \
                          % (skin_selection_id, skin_folder_id)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    xml_data = '<registered_skin_selection>'
    keys = self._objects.keys()
    keys.sort()
    for key in keys:
      skin_selection_list = self._objects[key]
      xml_data += '\n <skin_folder_selection>'
      xml_data += '\n  <skin_folder>%s</skin_folder>' % key
      xml_data += '\n  <skin_selection>%s</skin_selection>' \
                      % ','.join(skin_selection_list)
      xml_data += '\n </skin_folder_selection>'
    xml_data += '\n</registered_skin_selection>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    root_path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=root_path)
    # export workflow chain
    xml_data = self.generateXml()
    bta.addObject(obj=xml_data, name='registered_skin_selection',  path=root_path)

  def install(self, context, trashbin, **kw):
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    portal = context.getPortalObject()
    skin_tool = getToolByName(portal, 'portal_skins')

    for skin_folder_id in self._objects.keys():

      if update_dict.has_key(skin_folder_id) or force:
        if not force:
          action = update_dict[skin_folder_id]
          if action == 'nothing':
            continue
        skin_folder = skin_tool[skin_folder_id]
        selection_string = skin_folder.getProperty(
          'business_template_registered_skin_selections', None)

        if selection_string is None:
          create_property = True
          selection_string = self._objects[skin_folder_id].replace(',', ' ')
        else:
          create_property = False
          if not isinstance(selection_string, basestring):
            selection_string = ' '.join(selection_string)
          selection_string += ' %s' % \
            self._objects[skin_folder_id].replace(',', ' ')

        # Remove duplicate
        selection_string = \
            ' '.join(dict([(x, 0) for x in selection_string.split(' ')]).keys())
        if create_property:
          skin_folder._setProperty(
              'business_template_registered_skin_selections',
              selection_string.split(' '), type='tokens')
        else:
          skin_folder._updateProperty(
              'business_template_registered_skin_selections',
              selection_string.split(' '))

        selection_list = selection_string.split(' ')
        unregisterSkinFolder(skin_tool, skin_folder,
            skin_tool.getSkinSelections())
        registerSkinFolder(skin_tool, skin_folder)

  def uninstall(self, context, **kw):
    portal = context.getPortalObject()
    skin_tool = getToolByName(portal, 'portal_skins')

    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._objects.keys()

    for skin_folder_id in object_keys:
      skin_folder = skin_tool[skin_folder_id]
      current_selection_string = skin_folder.getProperty(
        'business_template_registered_skin_selections', [])
      current_selection_set = set(current_selection_string)

      skin_selection = workflow_id = self._objects[skin_folder_id]
      skin_selection_list = skin_selection.split(',')
      for skin_selection in skin_selection_list:
        current_selection_set.remove(skin_selection)

      current_selection_list = list(current_selection_set)
      if current_selection_list:
        skin_folder._updateProperty(
            'business_template_registered_skin_selections',
            current_selection_list)

        # Unregister skin folder from skin selection
        unregisterSkinFolder(skin_tool, skin_folder, skin_selection_list)
      else:
        delattr(skin_folder, 'business_template_registered_skin_selections')

        # Delete all skin selection
        for skin_selection in skin_selection_list:
          deleteSkinSelection(skin_tool, skin_selection)
        # Register to all other skin selection
        registerSkinFolder(skin_tool, skin_folder)

  def preinstall(self, context, installed_bt, **kw):
    modified_object_list = {}
    if context.getTemplateFormatVersion() == 1:
      new_keys = self._objects.keys()
      new_dict = PersistentMapping()
      for path in new_keys:
        if installed_bt._objects.has_key(path):
          # compare object to see it there is changes
          new_object = self._objects[path]
          old_object = installed_bt._objects[path]
          if new_object != old_object:
            modified_object_list.update({path : ['Modified', self.__class__.__name__[:-12]]})
        else: # new object
          modified_object_list.update({path : ['New', self.__class__.__name__[:-12]]})
      # get removed object
      old_keys = installed_bt._objects.keys()
      for path in old_keys:
        if path not in new_keys:
          modified_object_list.update({path : ['Removed', self.__class__.__name__[:-12]]})
    return modified_object_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      if not file_name.endswith('.zexp'):
        LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    # import workflow chain for portal_type
    skin_selection_dict = {}
    xml = parse(file)
    skin_folder_selection_list = xml.getElementsByTagName('skin_folder_selection')
    for skin_folder_selection in skin_folder_selection_list:
      skin_folder_id = skin_folder_selection.getElementsByTagName(
          'skin_folder')[0].childNodes[0].data
      selection_list = skin_folder_selection.getElementsByTagName(
          'skin_selection')[0].childNodes
      if len(selection_list) == 0:
        selection = ''
      else:
        selection = selection_list[0].data
      skin_selection_dict[str(skin_folder_id)] = str(selection)
    self._objects = skin_selection_dict


class WorkflowTemplateItem(ObjectTemplateItem):

  def __init__(self, id_list, tool_id='portal_workflow', **kw):
    return ObjectTemplateItem.__init__(self, id_list, tool_id=tool_id, **kw)

  # When the root object of a workflow is modified, the entire workflow is
  # recreated: all subobjects are discarded and must be reinstalled.
  # So we hide modified subobjects to the user and we always reinstall
  # (or remove) everything.

  def preinstall(self, context, installed_bt, **kw):
    modified_object_dict = ObjectTemplateItem.preinstall(self, context,
                                                         installed_bt, **kw)
    modified_workflow_dict = {}
    for modified_object, state in modified_object_dict.iteritems():
      path = modified_object.split('/')
      if len(path) > 2:
        modified_workflow_dict.setdefault('/'.join(path[:2]), ('Modified', state[1]))
      else:
        modified_workflow_dict[modified_object] = state
    return modified_workflow_dict

  def install(self, context, trashbin, **kw):
    if context.getTemplateFormatVersion() == 1:
      portal = context.getPortalObject()
      update_dict = kw.get('object_to_update')
      force = kw.get('force')
      # sort to add objects before their subobjects
      for path in sorted(self._objects):
          if force:
            action = 'backup'
          else:
            action = update_dict.get('/'.join(path.split('/')[:2]))
            if action in (None, 'nothing'):
              continue
          container_path = path.split('/')[:-1]
          object_id = path.split('/')[-1]
          try:
            container = portal.unrestrictedTraverse(container_path)
          except KeyError:
            # parent object can be set to nothing, in this case just go on
            container_url = '/'.join(container_path)
            if update_dict.has_key(container_url):
              if update_dict[container_url] == 'nothing':
                continue
            raise
          container_ids = container.objectIds()
          if object_id in container_ids:    # Object already exists
            self._backupObject(action, trashbin, container_path, object_id, keep_subobjects=1)
            container.manage_delObjects([object_id])
          obj = self._objects[path]
          if getattr(obj, 'meta_type', None) == 'Script (Python)':
            if getattr(obj, '_code') is None:
              obj._compile()
          obj = obj._getCopy(container)
          container._setObject(object_id, obj)
          obj = container._getOb(object_id)
          obj.manage_afterClone(obj)
          obj.wl_clearLocks()
    else:
      ObjectTemplateItem.install(self, context, trashbin, **kw)


class PortalTypeTemplateItem(ObjectTemplateItem):

  def __init__(self, id_list, tool_id='portal_types', **kw):
    ObjectTemplateItem.__init__(self, id_list, tool_id=tool_id, **kw)
    # XXX : this statement can be removed once all bt5 have separated
    # workflow-chain information
    self._workflow_chain_archive = PersistentMapping()

  def build(self, context, **kw):
    p = context.getPortalObject()
    for relative_url in self._archive.keys():
      obj = p.unrestrictedTraverse(relative_url)
      obj = obj._getCopy(context)
      # obj is in ghost state and an attribute must be accessed
      # so that obj.__dict__ does not return an empty dict
      obj.meta_type
      for attr in obj.__dict__.keys():
        if attr == '_property_domain_dict':
          continue
        if attr[0] == '_' or attr in ('allowed_content_types',
                                      'hidden_content_type_list',
                                      'property_sheet_list',
                                      'base_category_list',
                                      'last_id', 'uid', 'workflow_history'):
          delattr(obj, attr)
      self._objects[relative_url] = obj
      obj.wl_clearLocks()

  # XXX : this method is kept temporarily, but can be removed once all bt5 are
  # re-exported with separated workflow-chain information
  def install(self, context, trashbin, **kw):
    ObjectTemplateItem.install(self, context, trashbin, **kw)
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # We now need to setup the list of workflows corresponding to
    # each portal type
    (default_chain, chain_dict) = getChainByType(context)
    # Set the default chain to the empty string is probably the
    # best solution, by default it is 'default_workflow', which is
    # not very usefull
    default_chain = ''
    if context.getTemplateFormatVersion() == 1:
      object_list = self._objects
    else:
      object_list = self._archive
    for path in object_list.keys():
      if update_dict.has_key(path) or force:
        if not force:
          action = update_dict[path]
          if action == 'nothing':
            continue
        obj = object_list[path]
        portal_type = obj.id
        if self._workflow_chain_archive.has_key(portal_type):
          chain_dict['chain_%s' % portal_type] = \
              self._workflow_chain_archive[portal_type]
    context.portal_workflow.manage_changeWorkflows(default_chain,
                                                   props=chain_dict)

  # XXX : this method is kept temporarily, but can be removed once all bt5 are
  # re-exported with separated workflow-chain information
  def _importFile(self, file_name, file):
    if 'workflow_chain_type.xml' in file_name:
      # import workflow chain for portal_type
      dict = {}
      xml = parse(file)
      chain_list = xml.getElementsByTagName('chain')
      for chain in chain_list:
        ptype = chain.getElementsByTagName('type')[0].childNodes[0].data
        workflow_list = chain.getElementsByTagName('workflow')[0].childNodes
        if len(workflow_list) == 0:
          workflow = ''
        else:
          workflow = workflow_list[0].data
        dict[str(ptype)] = str(workflow)
      self._workflow_chain_archive = dict
    else:
      ObjectTemplateItem._importFile(self, file_name, file)

class PortalTypeWorkflowChainTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    # we can either specify nothing, +, - or = before the chain
    # this is used to know how to manage the chain
    # if nothing or +, chain is added to the existing one
    # if - chain is removed from the exisiting one
    # if = chain replaced the existing one
    p = context.getPortalObject()
    (default_chain, chain_dict) = getChainByType(context)
    for key in self._archive.keys():
      wflist = key.split(' | ')
      if len(wflist) == 2:
        portal_type = wflist[0]
        workflow = wflist[1]
      else:
        # portal type with no workflow defined
        portal_type = wflist[0][:-2]
        workflow = ''
      if chain_dict.has_key('chain_%s' % portal_type):
        if workflow[0] in ['+', '-', '=']:
          workflow_name = workflow[1:]
        else:
          workflow_name = workflow
        if workflow[0] != '-' and \
            workflow_name not in chain_dict['chain_%s' % portal_type].split(', '):
          if not self.is_bt_for_diff:
            # here, we use 'LOG' instead of 'raise', because it can
            # happen when a workflow is removed from the chain by
            # another business template.
            LOG('BusinessTemplate', WARNING, 'workflow %s not found in chain for portal_type %s'\
                % (workflow, portal_type))
        if self._objects.has_key(portal_type):
          # other workflow id already defined for this portal type
          self._objects[portal_type].append(workflow)
        else:
          self._objects[portal_type] = [workflow,]
      elif not self.is_bt_for_diff:
        raise NotFound, 'No workflow chain found for portal type %s. This '\
                        'is probably a sign of a missing dependency.'\
                                                    % portal_type

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    xml_data = '<workflow_chain>'
    keys = self._objects.keys()
    keys.sort()
    for key in keys:
      workflow_list = self._objects[key]
      # XXX Not always a list
      if isinstance(workflow_list, str):
        workflow_list = [workflow_list]
      xml_data += '\n <chain>'
      xml_data += '\n  <type>%s</type>' %(key,)
      xml_data += '\n  <workflow>%s</workflow>' %(', '.join(sorted(workflow_list)))
      xml_data += '\n </chain>'
    xml_data += '\n</workflow_chain>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    root_path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=root_path)
    # export workflow chain
    xml_data = self.generateXml()
    bta.addObject(obj=xml_data, name='workflow_chain_type',  path=root_path)

  def install(self, context, trashbin, **kw):
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # We now need to setup the list of workflows corresponding to
    # each portal type
    (default_chain, chain_dict) = getChainByType(context)
    # Set the default chain to the empty string is probably the
    # best solution, by default it is 'default_workflow', which is
    # not very usefull
    default_chain = ''
    for path in self._objects.keys():
      if update_dict.has_key(path) or force:
        if not force:
          action = update_dict[path]
          if action == 'nothing':
            continue
        path_splitted = path.split('/', 1)
        # XXX: to avoid crashing when no portal_type
        if len(path_splitted) < 1:
          continue
        portal_type = path_splitted[-1]
        if chain_dict.has_key('chain_%s' % portal_type):
          old_chain_dict = chain_dict['chain_%s' % portal_type]
          # XXX we don't use the chain (Default) in erp5 so don't keep it
          if old_chain_dict != '(Default)' and old_chain_dict != '':
            old_chain_workflow_id_set = {}
            # get existing workflow id list
            for wf_id in old_chain_dict.split(', '):
              old_chain_workflow_id_set[wf_id] = 1
            # get new workflow id list
            for wf_id in self._objects[path].split(', '):
              if wf_id[0] == '-':
                # remove wf id if already present
                if old_chain_workflow_id_set.has_key(wf_id[1:]):
                  old_chain_workflow_id_set.pop(wf_id[1:])
              elif wf_id[0] == '=':
                # replace existing chain by this one
                old_chain_workflow_id_set = {}
                old_chain_workflow_id_set[wf_id[1:]] = 1
              # then either '+' or nothing, add wf id to the list
              elif wf_id[0] == '+':
                old_chain_workflow_id_set[wf_id[1:]] = 1
              else:
                old_chain_workflow_id_set[wf_id] = 1
            # create the new chain
            chain_dict['chain_%s' % portal_type] = ', '.join(
                                              old_chain_workflow_id_set.keys())
          else:
            # Check if it has normally to remove a workflow chain, in order to
            # improve the error message
            for wf_id in self._objects[path].split(', '):
              if wf_id.startswith('-'):
                raise ValueError, '"%s" is not a workflow ID for %s' % \
                                  (wf_id, portal_type)
            chain_dict['chain_%s' % portal_type] = self._objects[path]
        else:
          if portal_type not in context.portal_types.objectIds():
            raise ValueError('Cannot chain workflow %r to non existing '
                           'portal type %r' % (self._objects[path],
                                               portal_type))
          chain_dict['chain_%s' % portal_type] = self._objects[path]
    context.portal_workflow.manage_changeWorkflows(default_chain,
                                                   props=chain_dict)

  def uninstall(self, context, **kw):
    (default_chain, chain_dict) = getChainByType(context)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._objects.keys()
    for path in object_keys:
      path_splitted = path.split('/', 1)
      if len(path_splitted) < 2:
        continue
      portal_type = path_splitted[1]
      id = 'chain_%s' % portal_type
      if id in chain_dict.keys():
        chain = chain_dict[id]
        # It should be better to use regexp
        chain = chain.replace(' ', '')
        workflow_list = chain.split(',')
        workflow_id = self._objects[path]
        for i in range(workflow_list.count(workflow_id)):
          workflow_list.remove(workflow_id)
        chain = ', '.join(workflow_list)
        if chain == '':
          del chain_dict[id]
        else:
          chain_dict[id] = chain
    context.portal_workflow.manage_changeWorkflows('', props=chain_dict)

  def preinstall(self, context, installed_bt, **kw):
    modified_object_list = {}
    if context.getTemplateFormatVersion() == 1:
      new_keys = self._objects.keys()
      new_dict = PersistentMapping()
      # Fix key from installed bt if necessary
      for key in installed_bt._objects.keys():
        if not "portal_type_workflow_chain/" in key:
          new_key = 'portal_type_workflow_chain/%s' %key
          new_dict[new_key] = installed_bt._objects[key]
        else:
          new_dict[key] = installed_bt._objects[key]
      if len(new_dict):
        installed_bt._objects = new_dict
      for path in new_keys:
        if installed_bt._objects.has_key(path):
          # compare object to see it there is changes
          new_object = self._objects[path]
          old_object = installed_bt._objects[path]
          # compare same type of object
          if isinstance(old_object, list) or isinstance(old_object, tuple):
            old_object = ', '.join(old_object)
          if new_object != old_object:
            modified_object_list.update({path : ['Modified', self.__class__.__name__[:-12]]})
        else: # new object
          modified_object_list.update({path : ['New', self.__class__.__name__[:-12]]})
      # get removed object
      old_keys = installed_bt._objects.keys()
      for path in old_keys:
        if path not in new_keys:
          modified_object_list.update({path : ['Removed', self.__class__.__name__[:-12]]})
    return modified_object_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      if not file_name.endswith('.zexp'):
        LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    # import workflow chain for portal_type
    dict = {}
    xml = parse(file)
    chain_list = xml.getElementsByTagName('chain')
    for chain in chain_list:
      ptype = chain.getElementsByTagName('type')[0].childNodes[0].data
      workflow_list = chain.getElementsByTagName('workflow')[0].childNodes
      if len(workflow_list) == 0:
        workflow = ''
      else:
        workflow = workflow_list[0].data
      if 'portal_type_workflow_chain/' not in str(ptype):
        ptype = 'portal_type_workflow_chain/' + str(ptype)
      dict[str(ptype)] = str(workflow)
    self._objects = dict

# just for backward compatibility
PortalTypeTemplateWorkflowChainItem = PortalTypeWorkflowChainTemplateItem

class PortalTypeAllowedContentTypeTemplateItem(BaseTemplateItem):
  # XXX This class is subclassed for hidden types, propertysheets, base
  # categories ...
  name = 'Allowed Content Type'
  xml_tag = 'allowed_content_type_list'
  class_property = 'allowed_content_types'
  business_template_class_property = '_portal_type_allowed_content_type_item'

  def build(self, context, **kw):
    types_tool = self.getPortalObject().portal_types
    types_list = list(types_tool.objectIds())
    for key in self._archive.keys():
      try:
        portal_type, allowed_type = key.split(' | ')
      except ValueError:
        raise ValueError('Invalid item %r in %s' % (key, self.name))
      # check properties corresponds to what is defined in site
      if not portal_type in types_list:
        raise ValueError, "Portal Type %s not found in site" %(portal_type,)
      ob = types_tool._getOb(portal_type)
      prop_value = getattr(ob, self.class_property, ())
      if not allowed_type in prop_value and not self.is_bt_for_diff:
        raise ValueError, "%s %s not found in portal type %s" % (
                             getattr(self, 'name', self.__class__.__name__),
                             allowed_type, portal_type)

      if self._objects.has_key(portal_type):
        allowed_list = self._objects[portal_type]
        allowed_list.append(allowed_type)
        self._objects[portal_type] = allowed_list
      else:
        self._objects[portal_type] = [allowed_type]

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    dictio = self._objects
    xml_data = '<%s>' %(self.xml_tag,)
    keys = dictio.keys()
    keys.sort()
    for key in keys:
      allowed_list = sorted(dictio[key])
      xml_data += '\n <portal_type id="%s">' %(key,)
      for allowed_item in allowed_list:
        xml_data += '\n  <item>%s</item>' %(allowed_item,)
      xml_data += '\n </portal_type>'
    xml_data += '\n</%s>' %(self.xml_tag,)
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    path = self.__class__.__name__+os.sep+self.class_property
    xml_data = self.generateXml(path=None)
    bta.addObject(obj=xml_data, name=path, path=None)

  def preinstall(self, context, installed_bt, **kw):
    modified_object_list = {}
    if context.getTemplateFormatVersion() == 1:
      portal = context.getPortalObject()
      new_keys = self._objects.keys()
      new_dict = PersistentMapping()
      # fix key if necessary in installed bt for diff
      for key in installed_bt._objects.keys():
        if self.class_property not in key:
          new_key = '%s/%s' % (self.class_property, key)
          new_dict[new_key] = installed_bt._objects[key]
        else:
          new_dict[key] = installed_bt._objects[key]
      if len(new_dict):
        installed_bt._objects = new_dict
      for path in new_keys:
        if installed_bt._objects.has_key(path):
          # compare object to see it there is changes
          new_object = self._objects[path]
          old_object = installed_bt._objects[path]
          if new_object != old_object:
            modified_object_list.update({path : ['Modified', self.__class__.__name__[:-12]]})
        else: # new object
          modified_object_list.update({path : ['New', self.__class__.__name__[:-12]]})
      # get removed object
      old_keys = installed_bt._objects.keys()
      for path in old_keys:
        if path not in new_keys:
          modified_object_list.update({path : ['Removed', self.__class__.__name__[:-12]]})
    return modified_object_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      if not file_name.endswith('.zexp'):
        LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    path, name = posixpath.split(file_name)
    xml = parse(file)
    portal_type_list = xml.getElementsByTagName('portal_type')
    for portal_type in portal_type_list:
      id = portal_type.getAttribute('id')
      item_type_list = []
      item_list = portal_type.getElementsByTagName('item')
      for item in item_list:
        item_type_list.append(str(item.childNodes[0].data))
      self._objects[self.class_property+'/'+id] = item_type_list

  def install(self, context, trashbin, **kw):
    p = context.getPortalObject()
    pt = p.unrestrictedTraverse('portal_types')
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    installed_bt = kw.get('installed_bt')
    if installed_bt is not None:
      old_objects = getattr(installed_bt,
                            self.business_template_class_property)._objects
    else:
      old_objects = {}
    for key in set(self._objects.keys()).union(set(old_objects.keys())):
      if update_dict.has_key(key) or force:
        if not force:
          action = update_dict[key]
          if action == 'nothing':
            continue
        try:
          portal_id = key.split('/')[-1]
          portal_type = pt._getOb(portal_id)
        except (AttributeError, KeyError):
          raise AttributeError, "Portal type '%s' not found while " \
              "installing %s" % (portal_id, self.getTitle())
        property_list = self._objects.get(key, [])
        old_property_list = old_objects.get(key, ())
        object_property_list = getattr(portal_type, self.class_property, ())
        if len(object_property_list) > 0:
          # merge differences between portal types properties
          # for example:
          # * current value : [A,B,C]
          # * in new BT : [A,D]
          # * in old BT : [A,B]
          # -> [A,D,C] i.e. C is merged but B is not merged
          for id in object_property_list:
            if id not in property_list and id not in old_property_list:
              property_list.append(id)
        setattr(portal_type, self.class_property, tuple(property_list))

  def uninstall(self, context, **kw):
    object_path = kw.get('object_path', None)
    p = context.getPortalObject()
    pt = p.unrestrictedTraverse('portal_types')
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._objects.keys()
    for key in object_keys:
      try:
        portal_id = key.split('/')[-1]
        portal_type = pt._getOb(portal_id)
      except (AttributeError,  KeyError):
        LOG("portal types not found : ", 100, portal_id)
        continue
      property_list = self._objects[key]
      original_property_list = list(getattr(portal_type,
                                    self.class_property, ()))
      for id in property_list:
        if id in original_property_list:
          original_property_list.remove(id)
      setattr(portal_type, self.class_property, tuple(original_property_list))


class PortalTypeHiddenContentTypeTemplateItem(PortalTypeAllowedContentTypeTemplateItem):

  name = 'Hidden Content Type'
  xml_tag = 'hidden_content_type_list'
  class_property = 'hidden_content_type_list'
  business_template_class_property = '_portal_type_hidden_content_type_item'


class PortalTypePropertySheetTemplateItem(PortalTypeAllowedContentTypeTemplateItem):

  name = 'Property Sheet'
  xml_tag = 'property_sheet_list'
  class_property = 'property_sheet_list'
  business_template_class_property = '_portal_type_property_sheet_item'


class PortalTypeBaseCategoryTemplateItem(PortalTypeAllowedContentTypeTemplateItem):

  name = 'Base Category'
  xml_tag = 'base_category_list'
  class_property = 'base_category_list'
  business_template_class_property = '_portal_type_base_category_item'


class CatalogMethodTemplateItem(ObjectTemplateItem):
  """Template Item for catalog methods.

    This template item stores catalog method and install them in the
    default catalog.
    The use Catalog makes for methods is saved as well and recreated on
    installation.
  """

  def __init__(self, id_list, tool_id='portal_catalog', **kw):
    ObjectTemplateItem.__init__(self, id_list, tool_id=tool_id, **kw)
    # a mapping to store properties of methods.
    # the mapping contains an entry for each method, and this entry is
    # another mapping having the id of the catalog property as key and a
    # boolean value to say wether the method is part of this catalog
    # configuration property.
    self._method_properties = PersistentMapping()

    self._is_filtered_archive = PersistentMapping()
    self._filter_expression_archive = PersistentMapping()
    self._filter_expression_instance_archive = PersistentMapping()
    self._filter_type_archive = PersistentMapping()

  def _extractMethodProperties(self, catalog, method_id):
    """Extracts properties for a given method in the catalog.
    Returns a mapping of property name -> boolean """
    method_properties = PersistentMapping()
    for prop in catalog._properties:
      if prop.get('select_variable') == 'getCatalogMethodIds':
        if prop['type'] == 'selection' and \
            getattr(catalog, prop['id']) == method_id:
          method_properties[prop['id']] = 1
        elif prop['type'] == 'multiple selection' and \
            method_id in getattr(catalog, prop['id']):
          method_properties[prop['id']] = 1
    return method_properties

  def build(self, context, **kw):
    ObjectTemplateItem.build(self, context, **kw)

    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate build', 0, 'catalog not found')
      return

    # upgrade old
    if not hasattr(self, '_method_properties'):
      self._method_properties = PersistentMapping()

    for obj in self._objects.values():
      method_id = obj.id
      self._method_properties[method_id] = self._extractMethodProperties(
                                                          catalog, method_id)
      self._is_filtered_archive[method_id] = 0
      if catalog.filter_dict.has_key(method_id):
        if catalog.filter_dict[method_id]['filtered']:
          self._is_filtered_archive[method_id] = \
                      catalog.filter_dict[method_id]['filtered']
          self._filter_expression_archive[method_id] = \
                      catalog.filter_dict[method_id]['expression']
          self._filter_expression_instance_archive[method_id] = \
                      catalog.filter_dict[method_id]['expression_instance']
          self._filter_type_archive[method_id] = \
                      catalog.filter_dict[method_id]['type']

  def export(self, context, bta, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate, export', 0, 'no SQL catalog was available')
      return

    if len(self._objects.keys()) == 0:
      return
    root_path = os.path.join(bta.path, self.__class__.__name__)
    for key in self._objects.keys():
      obj = self._objects[key]
      # create folder and subfolders
      folders, id = posixpath.split(key)
      path = os.path.join(root_path, folders)
      bta.addFolder(name=path)
      # export object in xml
      f=StringIO()
      XMLExportImport.exportXML(obj._p_jar, obj._p_oid, f)
      bta.addObject(obj=f.getvalue(), name=id, path=path)
      # add all datas specific to catalog inside one file
      method_id = obj.id
      object_path = os.path.join(path, method_id+'.catalog_keys.xml')

      f = open(object_path, 'wb')
      xml_data = '<catalog_method>'

      for method_property, value in self._method_properties[method_id].items():
        xml_data += '\n <item key="%s" type="int">' %(method_property,)
        xml_data += '\n  <value>%s</value>' %(value,)
        xml_data += '\n </item>'

      if catalog.filter_dict.has_key(method_id):
        if catalog.filter_dict[method_id]['filtered']:
          xml_data += '\n <item key="_is_filtered_archive" type="int">'
          xml_data += '\n  <value>1</value>'
          xml_data += '\n </item>'
          for method in catalog_method_filter_list:
            value = getattr(self, method, '')[method_id]
            if method != '_filter_expression_instance_archive':
              if type(value) in (type(''), type(u'')):
                xml_data += '\n <item key="%s" type="str">' %(method,)
                xml_data += '\n  <value>%s</value>' %(str(value))
                xml_data += '\n </item>'
              elif type(value) in (type(()), type([])):
                xml_data += '\n <item key="%s" type="tuple">'%(method)
                for item in value:
                  xml_data += '\n  <value>%s</value>' %(str(item))
                xml_data += '\n </item>'
      xml_data += '\n</catalog_method>'
      f.write(xml_data)
      f.close()

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def install(self, context, trashbin, **kw):
    ObjectTemplateItem.install(self, context, trashbin, **kw)
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    # Make copies of attributes of the default catalog of portal_catalog.
    sql_catalog_object_list = list(catalog.sql_catalog_object_list)
    sql_uncatalog_object = list(catalog.sql_uncatalog_object)
    sql_clear_catalog = list(catalog.sql_clear_catalog)

    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    values = []
    new_bt_format = context.getTemplateFormatVersion()

    if force: # get all objects
      if new_bt_format:
        values = self._objects.values()
      else:
        values = self._archive.values()
    else: # get only selected object
      if new_bt_format == 1:
        keys = self._objects.keys()
      else:
        keys = self._archive.keys()
      for key in keys:
        if update_dict.has_key(key) or force:
          if not force:
            action = update_dict[key]
            if action == 'nothing':
              continue
          if new_bt_format:
            values.append(self._objects[key])
          else:
            values.append(self._archive[key])

    for obj in values:
      method_id = obj.id

      # Restore catalog properties for methods
      if hasattr(self, '_method_properties'):
        for key in self._method_properties.get(method_id, {}).keys():
          old_value = getattr(catalog, key, None)
          if isinstance(old_value, str):
            setattr(catalog, key, method_id)
          elif isinstance(old_value, list) or isinstance(old_value, tuple):
            if method_id not in old_value:
              new_value = list(old_value) + [method_id]
              new_value.sort()
              setattr(catalog, key, tuple(new_value))

      # Restore filter
      if self._is_filtered_archive.get(method_id, 0):
        expression = self._filter_expression_archive[method_id]
        if context.getTemplateFormatVersion() == 1:
          expr_instance = Expression(expression)
        else:
          expr_instance = self._filter_expression_instance_archive[method_id]
        filter_type = self._filter_type_archive[method_id]
        catalog.filter_dict[method_id] = PersistentMapping()
        catalog.filter_dict[method_id]['filtered'] = 1
        catalog.filter_dict[method_id]['expression'] = expression
        catalog.filter_dict[method_id]['expression_instance'] = expr_instance
        catalog.filter_dict[method_id]['type'] = filter_type
      elif method_id in catalog.filter_dict.keys():
        catalog.filter_dict[method_id]['filtered'] = 0

      # backward compatibility
      if hasattr(self, '_is_catalog_list_method_archive'):
        LOG("BusinessTemplate.CatalogMethodTemplateItem", 0,
            "installing old style catalog method configuration")
        is_catalog_list_method = int(
                  self._is_catalog_list_method_archive[method_id])
        is_uncatalog_method = int(
                  self._is_uncatalog_method_archive[method_id])
        is_clear_method = int(
                  self._is_clear_method_archive[method_id])

        if is_catalog_list_method and method_id not in sql_catalog_object_list:
          sql_catalog_object_list.append(method_id)
        elif not is_catalog_list_method and\
                        method_id in sql_catalog_object_list:
          sql_catalog_object_list.remove(method_id)

        if is_uncatalog_method and method_id not in sql_uncatalog_object:
          sql_uncatalog_object.append(method_id)
        elif not is_uncatalog_method and method_id in sql_uncatalog_object:
          sql_uncatalog_object.remove(method_id)

        if is_clear_method and method_id not in sql_clear_catalog:
          sql_clear_catalog.append(method_id)
        elif not is_clear_method and method_id in sql_clear_catalog:
          sql_clear_catalog.remove(method_id)

        sql_catalog_object_list.sort()
        catalog.sql_catalog_object_list = tuple(sql_catalog_object_list)
        sql_uncatalog_object.sort()
        catalog.sql_uncatalog_object = tuple(sql_uncatalog_object)
        sql_clear_catalog.sort()
        catalog.sql_clear_catalog = tuple(sql_clear_catalog)

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    values = []
    object_path = kw.get('object_path', None)
    # get required values
    if object_path is None:
      if context.getTemplateFormatVersion() == 1:
        values = self._objects.values()
      else:
        values = self._archive.values()
    else:
      try:
        value = self._archive[object_path]
      except KeyError:
        value = None
      if value is not None:
        values.append(value)
    for obj in values:
      method_id = obj.id
      # remove method references in portal_catalog
      for catalog_prop in catalog._properties:
        if catalog_prop.get('select_variable') == 'getCatalogMethodIds'\
            and catalog_prop['type'] == 'multiple selection':
          old_value = getattr(catalog, catalog_prop['id'], ())
          if method_id in old_value:
            new_value = list(old_value)
            new_value.remove(method_id)
            setattr(catalog, catalog_prop['id'], new_value)

      if catalog.filter_dict.has_key(method_id):
        del catalog.filter_dict[method_id]

    # uninstall objects
    ObjectTemplateItem.uninstall(self, context, **kw)

  def _importFile(self, file_name, file):
    if file_name.endswith('.catalog_keys.xml'):
      # recreate data mapping specific to catalog method
      name = os.path.basename(file_name)
      id = name.split('.', 1)[0]
      xml = parse(file)
      method_list = xml.getElementsByTagName('item')
      for method in method_list:
        key = method.getAttribute('key')
        key_type = str(method.getAttribute('type'))
        if key_type == "str":
          if len(method.getElementsByTagName('value')[0].childNodes):
            value = str(method.getElementsByTagName('value')[0].childNodes[0].data)
          else:
            value = ''
          key = str(key)
        elif key_type == "int":
          value = int(method.getElementsByTagName('value')[0].childNodes[0].data)
          key = str(key)
        elif key_type == "tuple":
          value = []
          value_list = method.getElementsByTagName('value')
          for item in value_list:
            value.append(item.childNodes[0].data)
        else:
          LOG('BusinessTemplate import CatalogMethod, type unknown', 0, key_type)
          continue
        if key in catalog_method_list or key in catalog_method_filter_list:
          dict = getattr(self, key, {})
          dict[id] = value
        else:
          # new style key
          self._method_properties.setdefault(id, PersistentMapping())[key] = 1
    elif file_name.endswith('.xml'):
      # just import xml object
      obj = self
      connection = None
      while connection is None:
        obj=obj.aq_parent
        connection=obj._p_jar
      obj = connection.importFile(file, customImporters=customImporters)
      self.removeProperties(obj)
      self._objects[file_name[:-4]] = obj
    else:
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))

class ActionTemplateItem(ObjectTemplateItem):

  def __init__(self, id_list, **kw):
    # XXX It's look like ObjectTemplateItem __init__
    BaseTemplateItem.__init__(self, id_list, **kw)
    id_list = self._archive.keys()
    self._archive.clear()
    for id in id_list:
      self._archive["%s/%s" % ('portal_types', id)] = None

  def _splitPath(self, path):
    """
      Split path tries to split a complexe path such as:

      "foo/bar[id=zoo]"

      into

      "foo/bar", "id", "zoo"

      This is used mostly for generic objects
    """
    # Add error checking here
    if path.find('[') >= 0 and path.find(']') > path.find('=') and path.find('=') > path.find('['):
      relative_url = path[0:path.find('[')]
      id_block = path[path.find('[')+1:path.find(']')]
      key = id_block.split('=')[0]
      value = id_block.split('=')[1]
      return relative_url, key, value
    return path, None, None

  def build(self, context, **kw):
    BaseTemplateItem.build(self, context, **kw)
    p = context.getPortalObject()
    for id in self._archive.keys():
      url, value = id.split(' | ')
      url = posixpath.split(url)
      obj = p.unrestrictedTraverse(url)
      # Several tools still use CMF actions
      is_new_action = obj.getParentId() == 'portal_types'
      id_id = is_new_action and 'reference' or 'id'
      for action in (is_new_action and obj.getActionInformationList
                                    or obj.listActions)():
        if getattr(action, id_id, None) == value:
          break
      else:
        if self.is_bt_for_diff:
          continue
        raise NotFound('Action %r not found' % id)
      if is_new_action:
        action = obj._exportOldAction(action)
      else:
        action = action._getCopy(context)
      key = posixpath.join(url[-2], url[-1], value)
      self._objects[key] = self.removeProperties(action)
      self._objects[key].wl_clearLocks()

  def install(self, context, trashbin, **kw):
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    if context.getTemplateFormatVersion() == 1:
      portal_type_dict = {}
      p = context.getPortalObject()
      for id in self._objects.keys():
        if update_dict.has_key(id) or force:
          if not force:
            action = update_dict[id]
            if action == 'nothing':
              continue
          obj = self._objects[id]
          path, id = id.rsplit('/', 1)
          container = p.unrestrictedTraverse(path)

          if container.getParentId() == 'portal_types':
            # XXX future BT should use 'reference' instead of 'id'
            reference = getattr(obj, 'reference', None) or obj.id
            portal_type_dict.setdefault(path, {})[reference] = obj
            continue

          # Following code is for actions outside Types Tool.
          # It will be removed when they are also converted to ERP5 actions.
          try:
            from Products.CMFCore.interfaces import IActionProvider
          except ImportError:
              # we still don't load ZCML on tests on 2.8, but on 2.8 we don't
              # need to redirect actions to portal_actions.
              pass
          else:
            if not IActionProvider.providedBy(container):
              # some tools stopped being ActionProviders in CMF 2.x. Drop the
              # action into portal_actions.
              LOG('Products.ERP5.Document.BusinessTemplate', WARNING,
                  'Misplaced action',
                  'Attempted to store action %r in %r which is no longer an '
                  'IActionProvided. Storing action on portal_actions instead' %
                  (id, path))
              container = p.portal_actions
          obj, action = container, obj
          action_list = obj.listActions()
          for index in range(len(action_list)):
            if action_list[index].id == id:
              # remove previous action
              obj.deleteActions(selections=(index,))
          action_text = action.action
          if isinstance(action_text, Expression):
            action_text = action_text.text
          obj.addAction(
                        id = action.id
                      , name = action.title
                      , action = action_text
                      , condition = action.getCondition()
                      , permission = action.permissions
                      , category = action.category
                      , visible = action.visible
                      , icon = getattr(action, 'icon', None)\
                                and action.icon.text or ''
                      , priority = action.priority
                      , description = action.description
                    )
          # sort action based on the priority define on it
          # XXX suppose that priority are properly on actions
          new_priority = action.priority
          action_list = obj.listActions()
          move_down_list = []
          for index in range(len(action_list)):
            action = action_list[index]
            if action.priority > new_priority:
              move_down_list.append(str(index))
          obj.moveDownActions(selections=tuple(move_down_list))
      for path, action_dict in portal_type_dict.iteritems():
        container = p.unrestrictedTraverse(path)
        container.manage_delObjects([obj.id
          for obj in container.getActionInformationList()
          if obj.getReference() in action_dict])
        for obj in action_dict.itervalues():
          container._importOldAction(obj)
    else:
      BaseTemplateItem.install(self, context, trashbin, **kw)
      p = context.getPortalObject()
      for id in self._archive.keys():
        action = self._archive[id]
        relative_url, key, value = self._splitPath(id)
        obj = p.unrestrictedTraverse(relative_url)
        for ai in obj.listActions():
          if getattr(ai, key) == value:
            raise TemplateConflictError, 'the portal type %s already has the action %s' % (obj.id, value)
        action_text = action.action
        if isinstance(action_text, Expression):
          action_text = action_text.text
        obj.addAction(
                      id = action.id
                    , name = action.title
                    , action = action_text
                    , condition = action.getCondition()
                    , permission = action.permissions
                    , category = action.category
                    , visible = action.visible
                    , icon = getattr(action, 'icon', None) \
                                      and action.icon.text or ''
                    )
        new_priority = action.priority
        action_list = obj.listActions()
        move_down_list = []
        for index in range(len(action_list)):
          action = action_list[index]
          if action.priority > new_priority:
            move_down_list.append(str(index))
          obj.moveDownActions(selections=tuple(move_down_list))

  def uninstall(self, context, **kw):
    p = context.getPortalObject()
    object_path = kw.get("object_path", None)
    if object_path is not None:
      if '/' in object_path:
        # here object_path is the path of the actions, something like
        # portal_type/Person/view
        ti, action_id = object_path.rsplit('/', 1)
        keys = ['%s | %s' % (ti, action_id)]
      else:
        # compatibility ?
        keys = [object_path]
    else:
      keys = self._archive.keys()
    for id in keys:
      if  '|' in id:
        relative_url, value = id.split(' | ')
        obj = p.unrestrictedTraverse(relative_url, None)
        # Several tools still use CMF actions
        if obj is not None:
          is_new_action = obj.getParentId() == 'portal_types'
          key = is_new_action and 'reference' or 'id'
      else:
        relative_url, key, value = self._splitPath(id)
        obj = p.unrestrictedTraverse(relative_url, None)
      if obj is not None:
        action_list = obj.listActions()
        for index in range(len(action_list)):
          if getattr(action_list[index], key, None) == value:
            obj.deleteActions(selections=(index,))
            break
      LOG('BusinessTemplate', 100,
          'unable to uninstall action at %s, ignoring' % relative_url )
    BaseTemplateItem.uninstall(self, context, **kw)

class PortalTypeRolesTemplateItem(BaseTemplateItem):

  def __init__(self, id_list, **kw):
    id_list = ['portal_type_roles/%s' % id for id in id_list if id != '']
    BaseTemplateItem.__init__(self, id_list, **kw)

  def build(self, context, **kw):
    p = context.getPortalObject()
    for relative_url in self._archive.keys():
      obj = p.unrestrictedTraverse("portal_types/%s" %
          relative_url.split('/', 1)[1])
      self._objects[relative_url] = type_role_list = []
      for role in obj.getRoleInformationList():
        type_role_dict = {}
        for k, v in aq_base(role).__getstate__().iteritems():
          if k == 'condition':
            if not v:
              continue
            v = v.text
          elif k in ('role_base_category', 'role_category'):
            k = k[5:]
          elif k == 'role_name':
            k, v = 'id', '; '.join(v)
          elif k not in ('title', 'description'):
            k = {'id': 'object_id', # for stable sort
                 'role_base_category': 'base_category',
                 'role_base_category_script_id': 'base_category_script',
                 'role_category': 'category'}.get(k)
            if not k:
              continue
          type_role_dict[k] = v
        type_role_list.append(type_role_dict)
      type_role_list.sort(key=lambda x: (x.get('title'), x['object_id'],))

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    type_role_list = self._objects[path]
    xml_data = '<type_roles>'
    for role in type_role_list:
      xml_data += "\n  <role id='%s'>" % role['id']
      # uniq
      for property in ('title', 'description', 'condition',
          'base_category_script'):
        prop_value = role.get(property)
        if prop_value:
          if isinstance(prop_value, str):
            prop_value = prop_value.decode('utf-8')
          xml_data += "\n   <property id='%s'>%s</property>" % \
              (property, prop_value)
      # multi
      for property in ('category', 'base_category'):
        for prop_value in role.get(property, []):
          if isinstance(prop_value, str):
            prop_value = prop_value.decode('utf-8')
          xml_data += "\n   <multi_property "\
          "id='%s'>%s</multi_property>" % (property, prop_value)
      xml_data += "\n  </role>"
    xml_data += '\n</type_roles>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    root_path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=root_path)
    for key in self._objects.keys():
      xml_data = self.generateXml(key)
      if isinstance(xml_data, unicode):
        xml_data = xml_data.encode('utf-8')
      name = key.split('/', 1)[1]
      bta.addObject(obj=xml_data, name=name, path=root_path)

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    type_roles_list = []
    xml = parse(file)
    xml_type_roles_list = xml.getElementsByTagName('role')
    for role in xml_type_roles_list:
      id = role.getAttribute('id').encode('utf_8', 'backslashreplace')
      type_role_property_dict = {'id':id}
      # uniq
      property_list = role.getElementsByTagName('property')
      for property in property_list:
        property_id = property.getAttribute('id').encode()
        if property.hasChildNodes():
          property_value = property.childNodes[0].data.encode('utf_8', 'backslashreplace')
          type_role_property_dict[property_id] = property_value
      # multi
      multi_property_list = role.getElementsByTagName('multi_property')
      for property in multi_property_list:
        property_id = property.getAttribute('id').encode()
        if not type_role_property_dict.has_key(property_id):
          type_role_property_dict[property_id] = []
        if property.hasChildNodes():
          property_value = property.childNodes[0].data.encode('utf_8', 'backslashreplace')
          type_role_property_dict[property_id].append(property_value)
      type_roles_list.append(type_role_property_dict)
    self._objects['portal_type_roles/'+file_name[:-4]] = type_roles_list

  def install(self, context, trashbin, **kw):
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    p = context.getPortalObject()
    for roles_path in self._objects.keys():
      if update_dict.has_key(roles_path) or force:
        if not force:
          action = update_dict[roles_path]
          if action == 'nothing':
            continue
        path = 'portal_types/%s' % roles_path.split('/', 1)[1]
        obj = p.unrestrictedTraverse(path, None)
        if obj is not None:
          # reset roles before applying
          obj.manage_delObjects([x.id for x in obj.getRoleInformationList()])
          type_roles_list = self._objects[roles_path] or []
          for role_property_dict in type_roles_list:
            obj._importRole(role_property_dict)

  def uninstall(self, context, **kw):
    p = context.getPortalObject()
    object_path = kw.get('object_path', None)
    if object_path is not None:
      keys = [object_path]
    else:
      keys = self._objects.keys()
    for roles_path in keys:
      path = 'portal_types/%s' % roles_path.split('/', 1)[1]
      try:
        obj = p.unrestrictedTraverse(path)
        setattr(obj, '_roles', [])
      except (NotFound, KeyError):
        pass

class SitePropertyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    BaseTemplateItem.build(self, context, **kw)
    p = context.getPortalObject()
    for id in self._archive.keys():
      for property in p.propertyMap():
        if property['id'] == id:
          obj = p.getProperty(id)
          prop_type = property['type']
          break
      else:
        obj = None
      if obj is None and not self.is_bt_for_diff:
        raise NotFound, 'the property %s is not found' % id
      self._objects[id] = (prop_type, obj)

  def _importFile(self, file_name, file):
    # recreate list of site property from xml file
    if not file_name.endswith('.xml'):
      if not file_name.endswith('.zexp'):
        LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    xml = parse(file)
    property_list = xml.getElementsByTagName('property')
    for prop in property_list:
      id = prop.getElementsByTagName('id')[0].childNodes[0].data
      prop_type = prop.getElementsByTagName('type')[0].childNodes[0].data
      if prop_type in ('lines', 'tokens'):
        value = []
        values = prop.getElementsByTagName('value')[0]
        items = values.getElementsByTagName('item')
        for item in items:
          i = item.childNodes[0].data
          value.append(str(i))
      else:
        value = str(prop.getElementsByTagName('value')[0].childNodes[0].data)
      self._objects[str(id)] = (str(prop_type), value)

  def install(self, context, trashbin, **kw):
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    if context.getTemplateFormatVersion() == 1:
      p = context.getPortalObject()
      for path in self._objects.keys():
        if update_dict.has_key(path) or force:
          if not force:
            action = update_dict[path]
            if action == 'nothing':
              continue
          dir, id = posixpath.split(path)
          prop_type, property = self._objects[path]
          if p.hasProperty(id):
            if p.getPropertyType(id) != prop_type:
              p._delProperty(id)
              p._setProperty(id, property, type=prop_type)
            else:
              p._updateProperty(id, property)
          else:
            p._setProperty(id, property, type=prop_type)
    else:
      BaseTemplateItem.install(self, context, trashbin, **kw)
      p = context.getPortalObject()
      for id, property in self._archive.keys():
        property = self._archive[id]
        if p.hasProperty(id):
          if p.getPropertyType(id) != property['type']:
            p._delProperty(id)
            p._setProperty(id, property['value'], type=property['type'])
          else:
            p._updateProperty(id, property['value'])
        else:
          p._setProperty(id, property['value'], type=property['type'])

  def uninstall(self, context, **kw):
    p = context.getPortalObject()
    object_path = kw.get('object_path', None)
    if object_path is not None:
      keys = [object_path]
    else:
      keys = self._archive.keys()
    for id in keys:
      if p.hasProperty(id):
        p._delProperty(id)
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    xml_data = ''
    prop_type, obj = self._objects[path]
    xml_data += '\n <property>'
    xml_data += '\n  <id>%s</id>' % escape(str(path))
    xml_data += '\n  <type>%s</type>' % escape(str(prop_type))
    if prop_type in ('lines', 'tokens'):
      xml_data += '\n  <value>'
      for item in obj:
        if item != '':
          xml_data += '\n   <item>%s</item>' % escape(str(item))
      xml_data += '\n  </value>'
    else:
      xml_data += '\n  <value>%s</value>' % escape(str(obj))
    xml_data += '\n </property>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    root_path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=root_path)
    xml_data = '<site_property>'
    keys = self._objects.keys()
    keys.sort()
    for path in keys:
      xml_data += self.generateXml(path)
    xml_data += '\n</site_property>'
    bta.addObject(obj=xml_data, name='properties', path=root_path)

class ModuleTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    BaseTemplateItem.build(self, context, **kw)
    p = context.getPortalObject()
    for id in self._archive.keys():
      module = p.unrestrictedTraverse(id)
      dict = {}
      dict['id'] = module.getId()
      dict['title'] = module.getTitle()
      dict['portal_type'] = module.getPortalType()
      permission_list = []
      # use show permission
      dict['permission_list'] = module.showPermissions()
      self._objects[id] = dict

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    dict = self._objects[path]
    xml_data = '<module>'
    # sort key
    keys = dict.keys()
    keys.sort()
    for key in keys:
      if key =='permission_list':
        # separe permission dict into xml
        xml_data += '\n <%s>' %(key,)
        permission_list = dict[key]
        for perm in permission_list:
          # the type of the permission defined if we use acquired or not
          if type(perm[1]) == type([]):
            ptype = "list"
          else:
            ptype = "tuple"
          role_list = list(perm[1])
          # Skip if permission is not configured (i.e. no role at all
          # with acquire permission, or Manager only without acquire
          # permission).
          if (not len(role_list) and ptype == 'list') or \
                 (role_list == ['Manager'] and ptype == 'tuple'):
            continue
          role_list.sort()
          xml_data += "\n  <permission type='%s'>" %(ptype,)
          xml_data += '\n   <name>%s</name>' %(perm[0])
          for role in role_list:
            xml_data += '\n   <role>%s</role>' %(role)
          xml_data += '\n  </permission>'
        xml_data += '\n </%s>' %(key,)
      else:
        xml_data += '\n <%s>%s</%s>' %(key, dict[key], key)
    xml_data += '\n</module>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(path)
    keys = self._objects.keys()
    keys.sort()
    for id in keys:
      # export modules one by one
      xml_data = self.generateXml(path=id)
      bta.addObject(obj=xml_data, name=id, path=path)

  def install(self, context, trashbin, **kw):
    portal = context.getPortalObject()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    if context.getTemplateFormatVersion() == 1:
      items = self._objects
    else:
      items = self._archive

    valid_permissions = dict.fromkeys([x[0] for x in
                                       context.ac_inherited_permissions(all=1)])
    for id in items.keys():
      if update_dict.has_key(id) or force:
        if not force:
          action = update_dict[id]
          if action == 'nothing':
            continue
        mapping = items[id]
        path, id = posixpath.split(id)
        if id in portal.objectIds():
          module = portal._getOb(id)
          module.portal_type = str(mapping['portal_type'])
        else:
          module = portal.newContent(id=id, portal_type=str(mapping['portal_type']))
        module.setTitle(str(mapping['title']))
        for name in valid_permissions.keys():
          # By default, Manager only without acquire permission
          role_list = dict(mapping['permission_list']).get(name, ('Manager',))
          acquire = (type(role_list) == type([]))
          module.manage_permission(name, roles=role_list, acquire=acquire)

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    dict = {}
    xml = parse(file)
    for id in ('portal_type', 'id', 'title', 'permission_list'):
      elt = xml.getElementsByTagName(id)[0]
      if id == 'permission_list':
        plist = []
        perm_list = elt.getElementsByTagName('permission')
        for perm in perm_list:
          perm_type = perm.getAttribute('type').encode() or None
          name_elt = perm.getElementsByTagName('name')[0]
          name_node = name_elt.childNodes[0]
          name = name_node.data
          role_list = perm.getElementsByTagName('role')
          rlist = []
          for role in role_list:
            role_node = role.childNodes[0]
            role = role_node.data
            rlist.append(str(role))
          if perm_type == "list" or perm_type is None:
            perm_tuple = (str(name), list(rlist))
          else:
            perm_tuple = (str(name), tuple(rlist))
          plist.append(perm_tuple)
        dict[id] = plist
      else:
        node_list = elt.childNodes
        if len(node_list) == 0:
          value=''
        else:
          value = node_list[0].data
        dict[id] = str(value)
    self._objects[file_name[:-4]] = dict

  def uninstall(self, context, **kw):
    trash = kw.get('trash', 0)
    if trash:
      return
    object_path = kw.get('object_path', None)
    trashbin = kw.get('trashbin', None)
    if object_path is None:
      keys = self._archive.keys()
    else:
      keys = [object_path]
    p = context.getPortalObject()
    id_list = p.objectIds()
    for id in keys:
      if id in id_list:
        try:
          if trash and trashbin is not None:
            container_path = id.split('/')
            self.portal_trash.backupObject(trashbin, container_path, id, save=1, keep_subobjects=1)
          p.manage_delObjects([id])
        except NotFound:
          pass
    BaseTemplateItem.uninstall(self, context, **kw)

  def trash(self, context, new_item, **kw):
    # Do not remove any module for safety.
    pass

class DocumentTemplateItem(BaseTemplateItem):
  local_file_reader_name = 'readLocalDocument'
  local_file_writer_name = 'writeLocalDocument'
  local_file_importer_name = 'importLocalDocument'
  local_file_remover_name = 'removeLocalDocument'

  def build(self, context, **kw):
    BaseTemplateItem.build(self, context, **kw)
    for id in self._archive.keys():
      self._objects[self.__class__.__name__+'/'+id] = globals()[self.local_file_reader_name](id)

  def preinstall(self, context, installed_bt, **kw):
    modified_object_list = {}
    if context.getTemplateFormatVersion() == 1:
      new_keys = self._objects.keys()
      new_dict = PersistentMapping()
      # fix key if necessary in installed bt for diff
      for key in installed_bt._objects.keys():
        if self.__class__.__name__ in key:
          new_key = key[len('%s/' % self.__class__.__name__):]
          new_dict[new_key] = installed_bt._objects[key]
        else:
          new_dict[key] = installed_bt._objects[key]
      if len(new_dict):
        installed_bt._objects = new_dict
      for path in new_keys:
        if installed_bt._objects.has_key(path):
          # compare object to see if there is changes
          new_obj_code = self._objects[path]
          old_obj_code = installed_bt._objects[path]
          if new_obj_code != old_obj_code:
            modified_object_list.update(
                {path : ['Modified', self.__class__.__name__[:-12]]})
        else: # new object
          modified_object_list.update(
                {path : ['New', self.__class__.__name__[:-12]]})
          # get removed object
      old_keys = installed_bt._objects.keys()
      for path in old_keys:
        if path not in new_keys:
          modified_object_list.update(
                {path : ['Removed', self.__class__.__name__[:-12]]})
    return modified_object_list

  def install(self, context, trashbin, **kw):
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    if context.getTemplateFormatVersion() == 1:
      for id in self._objects.keys():
        if update_dict.has_key(id) or force:
          if not force:
            action = update_dict[id]
            if action == 'nothing':
              continue
          text = self._objects[id]
          path, name = posixpath.split(id)
          # This raises an exception if the file already exists.
          try:
            globals()[self.local_file_writer_name](name, text, create=0)
          except IOError, error:
            LOG("BusinessTemplate.py", WARNING, "Cannot install class %s on file system" %(name,))
            if error.errno :
              raise
            continue
          if self.local_file_importer_name is not None:
            globals()[self.local_file_importer_name](name)
    else:
      BaseTemplateItem.install(self, context, trashbin, **kw)
      for id in self._archive.keys():
        text = self._archive[id]
        # This raises an exception if the file exists.
        globals()[self.local_file_writer_name](id, text, create=1)
        if self.local_file_importer_name is not None:
          globals()[self.local_file_importer_name](id)

  def uninstall(self, context, **kw):
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for id in object_keys:
      globals()[self.local_file_remover_name](id)
    BaseTemplateItem.uninstall(self, context, **kw)

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      obj = self._objects[path]
      bta.addObject(obj=obj, name=path, path=None, ext='.py')

  def _importFile(self, file_name, file):
    if not file_name.endswith('.py'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    text = file.read()
    self._objects[file_name[:-3]]=text

class PropertySheetTemplateItem(DocumentTemplateItem):
  local_file_reader_name = 'readLocalPropertySheet'
  local_file_writer_name = 'writeLocalPropertySheet'
  local_file_importer_name = 'importLocalPropertySheet'
  local_file_remover_name = 'removeLocalPropertySheet'

class ConstraintTemplateItem(DocumentTemplateItem):
  local_file_reader_name = 'readLocalConstraint'
  local_file_writer_name = 'writeLocalConstraint'
  local_file_importer_name = 'importLocalConstraint'
  local_file_remover_name = 'removeLocalConstraint'

class ExtensionTemplateItem(DocumentTemplateItem):
  local_file_reader_name = 'readLocalExtension'
  local_file_writer_name = 'writeLocalExtension'
  # Extension needs no import
  local_file_importer_name = None
  local_file_remover_name = 'removeLocalExtension'

class TestTemplateItem(DocumentTemplateItem):
  local_file_reader_name = 'readLocalTest'
  local_file_writer_name = 'writeLocalTest'
  # Test needs no import
  local_file_importer_name = None
  local_file_remover_name = 'removeLocalTest'


class ProductTemplateItem(BaseTemplateItem):
  # XXX Not implemented yet
  pass

class RoleTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    role_list = []
    for key in self._archive.keys():
      role_list.append(key)
    if len(role_list) > 0:
      self._objects[self.__class__.__name__+'/'+'role_list'] = role_list

  def preinstall(self, context, installed_bt, **kw):
    modified_object_list = {}
    if context.getTemplateFormatVersion() == 1:
      new_roles = self._objects.keys()
      if installed_bt.id == INSTALLED_BT_FOR_DIFF:
        #must rename keys in dict if reinstall
        new_dict = PersistentMapping()
        old_keys = ()
        if len(installed_bt._objects.values()) > 0:
          old_keys = installed_bt._objects.values()[0]
        for key in old_keys:
          new_dict[key] = ''
        installed_bt._objects = new_dict
      for role in new_roles:
        if installed_bt._objects.has_key(role):
          continue
        else: # only show new roles
          modified_object_list.update({role : ['New', 'Role']})
      # get removed roles
      old_roles = installed_bt._objects.keys()
      for role in old_roles:
        if role not in new_roles:
          modified_object_list.update({role : ['Removed', self.__class__.__name__[:-12]]})
    return modified_object_list

  def install(self, context, trashbin, **kw):
    p = context.getPortalObject()
    # get roles
    if context.getTemplateFormatVersion() == 1:
      role_list = self._objects.keys()
    else:
      role_list = self._archive.keys()
    # set roles in PAS
    if p.acl_users.meta_type == 'Pluggable Auth Service':
      role_manager_list = p.acl_users.objectValues('ZODB Role Manager')
      for role_manager in role_manager_list:
        existing_role_list = role_manager.listRoleIds()
        for role in role_list:
          if role not in existing_role_list:
            role_manager.addRole(role)
    # set roles on portal
    roles = {}
    for role in p.__ac_roles__:
      roles[role] = 1
    for role in role_list:
      roles[role] = 1
    p.__ac_roles__ = tuple(roles.keys())

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      if not file_name.endswith('.zexp'):
        LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    xml = parse(file)
    role_list = xml.getElementsByTagName('role')
    for role in role_list:
      node = role.childNodes[0]
      value = node.data
      self._objects[str(value)] = 1

  def uninstall(self, context, **kw):
    p = context.getPortalObject()
    roles = {}
    for role in p.__ac_roles__:
      roles[role] = 1
    for role in self._archive.keys():
      if role in roles:
        del roles[role]
    p.__ac_roles__ = tuple(roles.keys())
    BaseTemplateItem.uninstall(self, context, **kw)

  def trash(self, context, new_item, **kw):
    p = context.getPortalObject()
    new_roles = {}
    for role in new_item._archive.keys():
      new_roles[role] = 1
    roles = {}
    for role in p.__ac_roles__:
      roles[role] = 1
    for role in self._archive.keys():
      if role in roles and role not in new_roles:
        del roles[role]
    p.__ac_roles__ = tuple(roles.keys())

  # Function to generate XML Code Manually
  def generateXml(self, path):
    obj = self._objects[path]
    xml_data = '<role_list>'
    obj.sort()
    for role in obj:
      xml_data += '\n <role>%s</role>' %(role)
    xml_data += '\n</role_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None,)

class CatalogResultKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_search_result_keys = list(catalog.sql_search_result_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_search_result_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Result key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'result_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_search_result_keys = list(catalog.sql_search_result_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX same as related key
    if update_dict.has_key('result_key_list') or force:
      if not force:
        action = update_dict['result_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_search_result_keys:
          sql_search_result_keys.append(key)
      catalog.sql_search_result_keys = sql_search_result_keys

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_search_result_keys = list(catalog.sql_search_result_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_search_result_keys:
        sql_search_result_keys.remove(key)
    catalog.sql_search_result_keys = sql_search_result_keys
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

class CatalogRelatedKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_search_related_keys = list(catalog.sql_catalog_related_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_search_related_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Related key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'related_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_catalog_related_keys = list(catalog.sql_catalog_related_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX must a find a better way to manage related key
    if update_dict.has_key('related_key_list') or update_dict.has_key('key_list') or force:
      if not force:
        if update_dict.has_key('related_key_list'):
          action = update_dict['related_key_list']
        else: # XXX for backward compatibility
          action = update_dict['key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_catalog_related_keys:
          sql_catalog_related_keys.append(key)
      catalog.sql_catalog_related_keys = tuple(sql_catalog_related_keys)

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_related_keys = list(catalog.sql_catalog_related_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_catalog_related_keys:
        sql_catalog_related_keys.remove(key)
    catalog.sql_catalog_related_keys = sql_catalog_related_keys
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

class CatalogResultTableTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_search_result_tables = list(catalog.sql_search_tables)
    key_list = []
    for key in self._archive.keys():
      if key in sql_search_result_tables:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Result table "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'result_table_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_search_tables = list(catalog.sql_search_tables)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX same as related keys
    if update_dict.has_key('result_table_list') or force:
      if not force:
        action = update_dict['result_table_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_search_tables:
          sql_search_tables.append(key)
      catalog.sql_search_tables = tuple(sql_search_tables)

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_search_tables = list(catalog.sql_search_tables)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_search_tables:
        sql_search_tables.remove(key)
    catalog.sql_search_tables = sql_search_tables
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

# keyword
class CatalogKeywordKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_keyword_keys = list(catalog.sql_catalog_keyword_search_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_keyword_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Keyword key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'keyword_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_keyword_keys = list(catalog.sql_catalog_keyword_search_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX same as related key
    if update_dict.has_key('keyword_key_list') or force:
      if not force:
        action = update_dict['keyword_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_keyword_keys:
          sql_keyword_keys.append(key)
      catalog.sql_catalog_keyword_search_keys = sql_keyword_keys

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_keyword_keys = list(catalog.sql_catalog_keyword_search_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_keyword_keys:
        sql_keyword_keys.remove(key)
    catalog.sql_catalog_keyword_search_keys = sql_keyword_keys
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

# datetime
class CatalogDateTimeKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_datetime_keys = list(getattr(catalog, 'sql_catalog_datetime_search_keys', []))
    key_list = []
    for key in self._archive.keys():
      if key in sql_datetime_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'DateTime key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'datetime_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(context)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_datetime_keys = list(getattr(catalog, 'sql_catalog_datetime_search_keys', []))
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX same as related key
    if update_dict.has_key('datetime_key_list') or force:
      if not force:
        action = update_dict['datetime_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_datetime_keys:
          sql_datetime_keys.append(key)
      catalog.sql_catalog_datetime_search_keys = sql_datetime_keys

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(context)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available - uninstall')
      return
    sql_datetime_keys = list(getattr(catalog, 'sql_catalog_datetime_search_keys', []))
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_datetime_keys:
        sql_datetime_keys.remove(key)
    catalog.sql_catalog_datetime_search_keys = sql_datetime_keys
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)      
      
# full text
class CatalogFullTextKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_full_text_keys = list(catalog.sql_catalog_full_text_search_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_full_text_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Fulltext key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'full_text_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_full_text_keys = list(catalog.sql_catalog_full_text_search_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX same as related key
    if update_dict.has_key('full_text_key_list') or force:
      if not force:
        action = update_dict['full_text_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_full_text_keys:
          sql_full_text_keys.append(key)
      catalog.sql_catalog_full_text_search_keys = sql_full_text_keys

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_full_text_keys = list(catalog.sql_catalog_full_text_search_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_full_text_keys:
        sql_full_text_keys.remove(key)
    catalog.sql_catalog_full_text_search_keys = sql_full_text_keys
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)


# request
class CatalogRequestKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_request_keys = list(catalog.sql_catalog_request_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_request_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Request key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'request_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_catalog_request_keys = list(catalog.sql_catalog_request_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX must a find a better way to manage related key
    if update_dict.has_key('request_key_list') or force:
      if not force:
        action = update_dict['request_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_catalog_request_keys:
          sql_catalog_request_keys.append(key)
      catalog.sql_catalog_request_keys = tuple(sql_catalog_request_keys)

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_request_keys = list(catalog.sql_catalog_request_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_catalog_request_keys:
        sql_catalog_request_keys.remove(key)
    catalog.sql_catalog_request_keys = sql_catalog_request_keys
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

# multivalue
class CatalogMultivalueKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_multivalue_keys = list(catalog.sql_catalog_multivalue_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_multivalue_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Multivalue key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'multivalue_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_catalog_multivalue_keys = list(catalog.sql_catalog_multivalue_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    if update_dict.has_key('multivalue_key_list') or force:
      if not force:
        action = update_dict['multivalue_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_catalog_multivalue_keys:
          sql_catalog_multivalue_keys.append(key)
      catalog.sql_catalog_multivalue_keys = tuple(sql_catalog_multivalue_keys)

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_multivalue_keys = list(catalog.sql_catalog_multivalue_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_catalog_multivalue_keys:
        sql_catalog_multivalue_keys.remove(key)
    catalog.sql_catalog_multivalue_keys = sql_catalog_multivalue_keys
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

# topic
class CatalogTopicKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_topic_search_keys = list(catalog.sql_catalog_topic_search_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_catalog_topic_search_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Topic key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'topic_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_catalog_topic_search_keys = list(catalog.sql_catalog_topic_search_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX same as related key
    if update_dict.has_key('topic_key_list') or force:
      if not force:
        action = update_dict['topic_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_catalog_topic_search_keys:
          sql_catalog_topic_search_keys.append(key)
      catalog.sql_catalog_topic_search_keys = sql_catalog_topic_search_keys

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_topic_search_keys = list(catalog.sql_catalog_topic_search_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_catalog_topic_search_keys:
        sql_catalog_topic_search_keys.remove(key)
    catalog.sql_catalog_topic_search_keys = sql_catalog_topic_search_keys
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

class CatalogScriptableKeyTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_scriptable_keys = list(catalog.sql_catalog_scriptable_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_catalog_scriptable_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Scriptable key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'scriptable_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_catalog_scriptable_keys = list(catalog.sql_catalog_scriptable_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX must a find a better way to manage scriptable key
    if update_dict.has_key('scriptable_key_list') or force:
      if not force:
        if update_dict.has_key('scriptable_key_list'):
          action = update_dict['scriptable_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_catalog_scriptable_keys:
          sql_catalog_scriptable_keys.append(key)
      catalog.sql_catalog_scriptable_keys = tuple(sql_catalog_scriptable_keys)

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_scriptable_keys = list(catalog.sql_catalog_scriptable_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_catalog_scriptable_keys:
        sql_catalog_scriptable_keys.remove(key)
    catalog.sql_catalog_scriptable_keys = tuple(sql_catalog_scriptable_keys)
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

class CatalogRoleKeyTemplateItem(BaseTemplateItem):
  # XXX Copy/paste from CatalogScriptableKeyTemplateItem

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_role_keys = list(catalog.sql_catalog_role_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_catalog_role_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'Role key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'role_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_catalog_role_keys = list(catalog.sql_catalog_role_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX must a find a better way to manage scriptable key
    if update_dict.has_key('role_key_list') or force:
      if not force:
        if update_dict.has_key('role_key_list'):
          action = update_dict['role_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_catalog_role_keys:
          sql_catalog_role_keys.append(key)
      catalog.sql_catalog_role_keys = tuple(sql_catalog_role_keys)

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_role_keys = list(catalog.sql_catalog_role_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_catalog_role_keys:
        sql_catalog_role_keys.remove(key)
    catalog.sql_catalog_role_keys = tuple(sql_catalog_role_keys)
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

class CatalogLocalRoleKeyTemplateItem(BaseTemplateItem):
  # XXX Copy/paste from CatalogScriptableKeyTemplateItem

  def build(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_local_role_keys = list(catalog.sql_catalog_local_role_keys)
    key_list = []
    for key in self._archive.keys():
      if key in sql_catalog_local_role_keys:
        key_list.append(key)
      elif not self.is_bt_for_diff:
        raise NotFound, 'LocalRole key "%r" not found in catalog' %(key,)
    if len(key_list) > 0:
      self._objects[self.__class__.__name__+'/'+'local_role_key_list'] = key_list

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    list = []
    xml = parse(file)
    key_list = xml.getElementsByTagName('key')
    for key in key_list:
      node = key.childNodes[0]
      value = node.data
      list.append(str(value))
    self._objects[file_name[:-4]] = list

  def install(self, context, trashbin, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return

    sql_catalog_local_role_keys = list(catalog.sql_catalog_local_role_keys)
    if context.getTemplateFormatVersion() == 1:
      if len(self._objects.keys()) == 0: # needed because of pop()
        return
      keys = []
      for k in self._objects.values().pop(): # because of list of list
        keys.append(k)
    else:
      keys = self._archive.keys()
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    # XXX must a find a better way to manage scriptable key
    if update_dict.has_key('local_role_key_list') or force:
      if not force:
        if update_dict.has_key('local_role_key_list'):
          action = update_dict['local_role_key_list']
        if action == 'nothing':
          return
      for key in keys:
        if key not in sql_catalog_local_role_keys:
          sql_catalog_local_role_keys.append(key)
      catalog.sql_catalog_local_role_keys = tuple(sql_catalog_local_role_keys)

  def uninstall(self, context, **kw):
    catalog = _getCatalogValue(self)
    if catalog is None:
      LOG('BusinessTemplate', 0, 'no SQL catalog was available')
      return
    sql_catalog_local_role_keys = list(catalog.sql_catalog_local_role_keys)
    object_path = kw.get('object_path', None)
    if object_path is not None:
      object_keys = [object_path]
    else:
      object_keys = self._archive.keys()
    for key in object_keys:
      if key in sql_catalog_local_role_keys:
        sql_catalog_local_role_keys.remove(key)
    catalog.sql_catalog_local_role_keys = tuple(sql_catalog_local_role_keys)
    BaseTemplateItem.uninstall(self, context, **kw)

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    obj = self._objects[path]
    xml_data = '<key_list>'
    obj.sort()
    for key in obj:
      xml_data += '\n <key>%s</key>' %(key)
    xml_data += '\n</key_list>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=path)
    for path in self._objects.keys():
      xml_data = self.generateXml(path=path)
      bta.addObject(obj=xml_data, name=path, path=None)

class MessageTranslationTemplateItem(BaseTemplateItem):

  def build(self, context, **kw):
    localizer = context.getPortalObject().Localizer
    for lang_key in self._archive.keys():
      if '|' in lang_key:
        lang, catalog = lang_key.split(' | ')
      else: # XXX backward compatibility
        lang = lang_key
        catalog = 'erp5_ui'
      path = posixpath.join(lang, catalog)
      mc = localizer._getOb(catalog)
      self._objects[path] = mc.manage_export(lang)

  def preinstall(self, context, installed_bt, **kw):
    modified_object_list = {}
    if context.getTemplateFormatVersion() == 1:
      new_keys = self._objects.keys()
      for path in new_keys:
        if installed_bt._objects.has_key(path):
          # compare object to see if there is changes
          new_obj_code = self._objects[path]
          old_obj_code = installed_bt._objects[path]
          if new_obj_code != old_obj_code:
            modified_object_list.update({path : ['Modified', self.__class__.__name__[:-12]]})
        else: # new object
          modified_object_list.update({path : ['New', self.__class__.__name__[:-12]]})
      # get removed object
      old_keys = installed_bt._objects.keys()
      for path in old_keys:
        if path not in new_keys:
          modified_object_list.update({path : ['Removed', self.__class__.__name__[:-12]]})
    return modified_object_list

  def install(self, context, trashbin, **kw):
    localizer = context.getPortalObject().Localizer
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    if context.getTemplateFormatVersion() == 1:
      for path, po in self._objects.items():
        if update_dict.has_key(path) or force:
          if not force:
            action = update_dict[path]
            if action == 'nothing':
              continue
          path = path.split('/')
          if len(path) == 2:
            lang = path[0]
            catalog = path[1]
          else:
            lang = path[-3]
            catalog = path[-2]
          if lang not in localizer.get_languages():
            localizer.manage_addLanguage(lang)
          mc = localizer._getOb(catalog)
          if lang not in mc.get_languages():
            mc.manage_addLanguage(lang)
          mc.manage_import(lang, po)
    else:
      BaseTemplateItem.install(self, context, trashbin, **kw)
      for lang, catalogs in self._archive.items():
        if lang not in localizer.get_languages():
          localizer.manage_addLanguage(lang)
        for catalog, po in catalogs.items():
          mc = localizer._getOb(catalog)
          if lang not in mc.get_languages():
            mc.manage_addLanguage(lang)
          mc.manage_import(lang, po)

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    root_path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=root_path)
    for key in self._objects.keys():
      obj = self._objects[key]
      path = os.path.join(root_path, key)
      bta.addFolder(name=path)
      f = open(path+os.sep+'translation.po', 'wb')
      f.write(str(obj))
      f.close()

  def _importFile(self, file_name, file):
    if posixpath.split(file_name)[1] == 'translation.po':
      text = file.read()
      self._objects[file_name[:-3]] = text

class LocalRolesTemplateItem(BaseTemplateItem):

  def __init__(self, id_list, **kw):
    id_list = ['local_roles/%s' % id for id in id_list if id != '']
    BaseTemplateItem.__init__(self, id_list, **kw)

  def build(self, context, **kw):
    p = context.getPortalObject()
    for path in self._archive.keys():
      obj = p.unrestrictedTraverse(path.split('/', 1)[1])
      local_roles_dict = getattr(obj, '__ac_local_roles__',
                                        {}) or {}
      self._objects[path] = (local_roles_dict, )

  # Function to generate XML Code Manually
  def generateXml(self, path=None):
    local_roles_dict = self._objects[path][0]
    # local roles
    xml_data = '<local_roles_item>'
    xml_data += '\n <local_roles>'
    for key in sorted(local_roles_dict):
      xml_data += "\n  <role id='%s'>" %(key,)
      tuple = local_roles_dict[key]
      for item in tuple:
        xml_data += "\n   <item>%s</item>" %(item,)
      xml_data += '\n  </role>'
    xml_data += '\n </local_roles>'
    xml_data += '\n</local_roles_item>'
    return xml_data

  def export(self, context, bta, **kw):
    if len(self._objects.keys()) == 0:
      return
    root_path = os.path.join(bta.path, self.__class__.__name__)
    bta.addFolder(name=root_path)
    for key in self._objects.keys():
      xml_data = self.generateXml(key)

      folders, id = posixpath.split(key)
      encode_folders = []
      for folder in folders.split('/')[1:]:
        if '%' not in folder:
          encode_folders.append(quote(folder))
        else:
          encode_folders.append(folder)
      path = os.path.join(root_path, (os.sep).join(encode_folders))
      bta.addFolder(name=path)
      bta.addObject(obj=xml_data, name=id, path=path)

  def _importFile(self, file_name, file):
    if not file_name.endswith('.xml'):
      LOG('Business Template', 0, 'Skipping file "%s"' % (file_name, ))
      return
    xml = parse(file)
    # local roles
    local_roles = xml.getElementsByTagName('local_roles')[0]
    local_roles_list = local_roles.getElementsByTagName('role')
    local_roles_dict = {}
    for role in local_roles_list:
      id = role.getAttribute('id')
      if isinstance(id, unicode):
        id = id.encode('utf-8')
      item_type_list = []
      item_list = role.getElementsByTagName('item')
      for item in item_list:
        item_type_list.append(str(item.childNodes[0].data))
      local_roles_dict[id] = item_type_list
    self._objects['local_roles/'+file_name[:-4]] = (local_roles_dict, )

  def install(self, context, trashbin, **kw):
    update_dict = kw.get('object_to_update')
    force = kw.get('force')
    p = context.getPortalObject()
    for roles_path in self._objects.keys():
      if update_dict.has_key(roles_path) or force:
        if not force:
          action = update_dict[roles_path]
          if action == 'nothing':
            continue
        path = roles_path.split('/')[1:]
        obj = p.unrestrictedTraverse(path)
        local_roles_dict = self._objects[roles_path][0]
        setattr(obj, '__ac_local_roles__', local_roles_dict)

  def uninstall(self, context, **kw):
    p = context.getPortalObject()
    for roles_path in self._objects.keys():
      path = roles_path.split('/')[1:]
      obj = p.unrestrictedTraverse(path)
      setattr(obj, '__ac_local_roles__', {})

class BusinessTemplate(XMLObject):
    """
    A business template allows to construct ERP5 modules
    in part or completely. Each object is separated from its
    subobjects and exported in xml format.
    It may include:

    - catalog definition
      - SQL method objects
      - SQL methods including:
        - purpose (catalog, uncatalog, etc.)
        - filter definition

    - portal_types definition
      - object without optimal actions
      - list of relation between portal type and workflow

    - module definition
      - id
      - title
      - portal type
      - roles/security

    - site property definition
      - id
      - type
      - value

    - document/propertysheet/extension/test definition
      - copy of the local file

    - message transalation definition
      - .po file

    The Business Template properties are exported to the bt folder with
    one property per file

    Technology:

    - download a gzip file or folder tree (from the web, from a CVS repository,
      from local file system) (import/donwload)

    - install files to the right location (install)

    Use case:

    - install core ERP5 (the minimum)

    - go to "BT" menu. Import BT. Select imported BT. Click install.

    - go to "BT" menu. Create new BT.
      Define BT elements (workflow, methods, attributes, etc.).
      Build BT and export or save it
      Done.
    """

    meta_type = 'ERP5 Business Template'
    portal_type = 'Business Template'
    add_permission = Permissions.AddPortalContent
    isPortalContent = 1
    isRADContent = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Declarative properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.SimpleItem
                      , PropertySheet.CategoryCore
                      , PropertySheet.Version
                      , PropertySheet.BusinessTemplate
                      , PropertySheet.Comment
                      )

    # Factory Type Information
    factory_type_information = \
      {    'id'             : portal_type
         , 'meta_type'      : meta_type
         , 'description'    : """\
Business Template is a set of definitions, such as skins, portal types and categories. This is used to set up a new ERP5 site very efficiently."""
         , 'icon'           : 'file_icon.gif'
         , 'product'        : 'ERP5Type'
         , 'factory'        : 'addBusinessTemplate'
         , 'immediate_view' : 'BusinessTemplate_view'
         , 'allow_discussion'     : 1
         , 'allowed_content_types': (
                                      )
         , 'filter_content_types' : 1
      }

    # This is a global variable
    # Order is important for installation
    # We want to have:
    #  * path after module, because path can be module content
    #  * path after categories, because path can be categories content
    #  * skin after paths, because we can install a custom connection string as
    #       path and use it with SQLMethods in a skin.
    #    ( and more )
    _item_name_list = [
      '_product_item',
      '_property_sheet_item',
      '_constraint_item',
      '_document_item',
      '_extension_item',
      '_test_item',
      '_role_item',
      '_tool_item',
      '_message_translation_item',
      '_workflow_item',
      '_site_property_item',
      '_portal_type_item',
      '_portal_type_workflow_chain_item',
      '_portal_type_allowed_content_type_item',
      '_portal_type_hidden_content_type_item',
      '_portal_type_property_sheet_item',
      '_portal_type_base_category_item',
      '_category_item',
      '_module_item',
      '_path_item',
      '_skin_item',
      '_registered_skin_selection_item',
      '_preference_item',
      '_action_item',
      '_portal_type_roles_item',
      '_local_roles_item',
      '_catalog_method_item',
      '_catalog_result_key_item',
      '_catalog_related_key_item',
      '_catalog_result_table_item',
      '_catalog_keyword_key_item',
      '_catalog_datetime_key_item',
      '_catalog_full_text_key_item',
      '_catalog_request_key_item',
      '_catalog_multivalue_key_item',
      '_catalog_topic_key_item',
      '_catalog_scriptable_key_item',
      '_catalog_role_key_item',
      '_catalog_local_role_key_item',
    ]

    def __init__(self, *args, **kw):
      XMLObject.__init__(self, *args, **kw)
      self._clean()

    def getTemplateFormatVersion(self, **kw):
      """This is a workaround, because template_format_version was not set even for the new format.
      """
      if self.hasProperty('template_format_version'):
        self._baseGetTemplateFormatVersion()

      # the attribute _objects in BaseTemplateItem was added in the new format.
      if hasattr(self._path_item, '_objects'):
        return 1

      return 0

    security.declareProtected(Permissions.ManagePortal, 'manage_afterAdd')
    def manage_afterAdd(self, item, container):
      """
        This is called when a new business template is added or imported.
      """
      portal_workflow = getToolByName(self, 'portal_workflow')
      if portal_workflow is not None:
        # Make sure that the installation state is "not installed".
        if portal_workflow.getStatusOf(
                'business_template_installation_workflow', self) is not None:
          # XXX Not good to access the attribute directly,
          # but there is no API for clearing the history.
          self.workflow_history[
                            'business_template_installation_workflow'] = None

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getRevision')
    def getRevision(self):
      """returns the revision property.
      This is a workaround for #461.
      """
      return self._baseGetRevision()

    def updateRevisionNumber(self):
        """Increment bt revision number.
        """
        revision_number = self.getRevision()
        if revision_number is None or revision_number.strip() == '':
          revision_number = 1
        else:
          revision_number = int(revision_number)+1
        self.setRevision(revision_number)

    security.declareProtected(Permissions.ManagePortal, 'build')
    def build(self, no_action=0):
      """
        Copy existing portal objects to self
      """
      if no_action: return
        # this is use at import of Business Template to get the status built
      # Make sure that everything is sane.
      self.clean()

      self.updateRevisionNumber()

      self._setTemplateFormatVersion(1)

      # Store all data
      self._portal_type_item = \
          PortalTypeTemplateItem(self.getTemplatePortalTypeIdList())
      self._portal_type_workflow_chain_item = \
          PortalTypeWorkflowChainTemplateItem(self.getTemplatePortalTypeWorkflowChainList())
      self._workflow_item = \
          WorkflowTemplateItem(self.getTemplateWorkflowIdList())
      self._skin_item = \
          SkinTemplateItem(self.getTemplateSkinIdList())
      self._registered_skin_selection_item = \
          RegisteredSkinSelectionTemplateItem(
              self.getTemplateRegisteredSkinSelectionList())
      self._category_item = \
          CategoryTemplateItem(self.getTemplateBaseCategoryList())
      self._catalog_method_item = \
          CatalogMethodTemplateItem(self.getTemplateCatalogMethodIdList())
      self._action_item = \
          ActionTemplateItem(self.getTemplateActionPathList())
      self._portal_type_roles_item = \
          PortalTypeRolesTemplateItem(self.getTemplatePortalTypeRoleList())
      self._site_property_item = \
          SitePropertyTemplateItem(self.getTemplateSitePropertyIdList())
      self._module_item = \
          ModuleTemplateItem(self.getTemplateModuleIdList())
      self._document_item = \
          DocumentTemplateItem(self.getTemplateDocumentIdList())
      self._property_sheet_item = \
          PropertySheetTemplateItem(self.getTemplatePropertySheetIdList())
      self._constraint_item = \
          ConstraintTemplateItem(self.getTemplateConstraintIdList())
      self._extension_item = \
          ExtensionTemplateItem(self.getTemplateExtensionIdList())
      self._test_item = \
          TestTemplateItem(self.getTemplateTestIdList())
      self._product_item = \
          ProductTemplateItem(self.getTemplateProductIdList())
      self._role_item = \
          RoleTemplateItem(self.getTemplateRoleList())
      self._catalog_result_key_item = \
          CatalogResultKeyTemplateItem(
               self.getTemplateCatalogResultKeyList())
      self._catalog_related_key_item = \
          CatalogRelatedKeyTemplateItem(
               self.getTemplateCatalogRelatedKeyList())
      self._catalog_result_table_item = \
          CatalogResultTableTemplateItem(
               self.getTemplateCatalogResultTableList())
      self._message_translation_item = \
          MessageTranslationTemplateItem(
               self.getTemplateMessageTranslationList())
      self._portal_type_allowed_content_type_item = \
           PortalTypeAllowedContentTypeTemplateItem(
               self.getTemplatePortalTypeAllowedContentTypeList())
      self._portal_type_hidden_content_type_item = \
           PortalTypeHiddenContentTypeTemplateItem(
               self.getTemplatePortalTypeHiddenContentTypeList())
      self._portal_type_property_sheet_item = \
           PortalTypePropertySheetTemplateItem(
               self.getTemplatePortalTypePropertySheetList())
      self._portal_type_base_category_item = \
           PortalTypeBaseCategoryTemplateItem(
               self.getTemplatePortalTypeBaseCategoryList())
      self._path_item = \
               PathTemplateItem(self.getTemplatePathList())
      self._preference_item = \
               PreferenceTemplateItem(self.getTemplatePreferenceList())
      self._catalog_keyword_key_item = \
          CatalogKeywordKeyTemplateItem(
               self.getTemplateCatalogKeywordKeyList())
      self._catalog_datetime_key_item = \
          CatalogDateTimeKeyTemplateItem(
               self.getTemplateCatalogDatetimeKeyList())
      self._catalog_full_text_key_item = \
          CatalogFullTextKeyTemplateItem(
               self.getTemplateCatalogFullTextKeyList())
      self._catalog_request_key_item = \
          CatalogRequestKeyTemplateItem(
               self.getTemplateCatalogRequestKeyList())
      self._catalog_multivalue_key_item = \
          CatalogMultivalueKeyTemplateItem(
               self.getTemplateCatalogMultivalueKeyList())
      self._catalog_topic_key_item = \
          CatalogTopicKeyTemplateItem(
               self.getTemplateCatalogTopicKeyList())
      self._local_roles_item = \
          LocalRolesTemplateItem(
               self.getTemplateLocalRoleList())
      self._tool_item = \
          ToolTemplateItem(
               self.getTemplateToolIdList())
      self._catalog_scriptable_key_item = \
          CatalogScriptableKeyTemplateItem(
               self.getTemplateCatalogScriptableKeyList())
      self._catalog_role_key_item = \
          CatalogRoleKeyTemplateItem(
               self.getTemplateCatalogRoleKeyList())
      self._catalog_local_role_key_item = \
          CatalogLocalRoleKeyTemplateItem(
               self.getTemplateCatalogLocalRoleKeyList())

      # Build each part
      for item_name in self._item_name_list:
        item = getattr(self, item_name)
        if self.getBtForDiff():
          item.is_bt_for_diff = 1
        item.build(self)

    build = WorkflowMethod(build)

    def publish(self, url, username=None, password=None):
      """
        Publish in a format or another
      """
      return self.portal_templates.publish(self, url, username=username,
                                           password=password)

    def update(self):
      """
        Update template: download new template definition
      """
      return self.portal_templates.update(self)

    def isCatalogUpdatable(self):
      """
      Return if catalog will be updated or not by business template installation
      """
      catalog_method = getattr(self, '_catalog_method_item', None)
      default_catalog = self.getPortalObject().portal_catalog.getSQLCatalog()
      my_catalog = _getCatalogValue(self)
      if default_catalog is not None and my_catalog is not None \
             and catalog_method is not None and self.getTemplateFormatVersion() == 1:
        if default_catalog.getId() == my_catalog.getId():
          # It is needed to update the catalog only if the default SQLCatalog is modified.
          for method_id in catalog_method._objects.keys():
            if 'related' not in method_id:
              # must update catalog
              return True
      return False

    def preinstall(self, check_dependencies=1, **kw):
      """
        Return the list of modified/new/removed object between a Business Template
        and the one installed if exists
      """
      if check_dependencies:
        # required because in multi installation, dependencies has already
        # been checked before and it will failed here as dependencies can be
        # installed at the same time
        self.checkDependencies()

      modified_object_list = {}
      bt_title = self.getTitle()

      #  can be call to diff two Business Template in template tool
      bt2 = kw.get('compare_to', None)
      if  bt2 is not None:
        installed_bt = bt2
      else:
        installed_bt = self.portal_templates.getInstalledBusinessTemplate(title=bt_title)
      if installed_bt is None:
        installed_bt_format = 0 # that will not check for modification
      else:
        installed_bt_format = installed_bt.getTemplateFormatVersion()

      # if reinstall business template, must compare to object in ZODB
      # and not to those in the installed Business Template because it is itself.
      # same if we make a diff and select only one business template
      reinstall = 0
      if installed_bt == self:
        reinstall = 1
        if self.portal_templates._getOb(INSTALLED_BT_FOR_DIFF, None) is None:
          bt2 = self.portal_templates.manage_clone(ob=installed_bt, id=INSTALLED_BT_FOR_DIFF)
          # update portal types properties to get last modifications
          bt2.getPortalTypesProperties()
          bt2.edit(description='tmp bt generated for diff', bt_for_diff=1)
          bt2.build()
          installed_bt = bt2
        else:
          installed_bt = self.portal_templates._getOb(INSTALLED_BT_FOR_DIFF)

      new_bt_format = self.getTemplateFormatVersion()
      if installed_bt_format == 0 and new_bt_format == 0:
        # still use old format, so install everything, no choice
        return modified_object_list
      elif installed_bt_format == 0 and new_bt_format == 1:
        # return list of all object in bt
        for item_name in self._item_name_list:
          item = getattr(self, item_name, None)
          if item is not None:
            for path in item._objects.keys():
              modified_object_list.update({path : ['New', item.__class__.__name__[:-12]]})
        return modified_object_list

      for item_name in self._item_name_list:
        new_item = getattr(self, item_name, None)
        old_item = getattr(installed_bt, item_name, None)
        if new_item is not None:
          if old_item is not None and hasattr(old_item, '_objects'):
            modified_object = new_item.preinstall(context=self, installed_bt=old_item)
            if len(modified_object) > 0:
              modified_object_list.update(modified_object)
          else:
            for path in new_item._objects.keys():
              modified_object_list.update({path : ['New', new_item.__class__.__name__[:-12]]})

      if reinstall:
        self.portal_templates.manage_delObjects(ids=[INSTALLED_BT_FOR_DIFF])

      return modified_object_list

    def _install(self, force=1, object_to_update=None, update_translation=0,
                 update_catalog=0, **kw):
      """
        Install a new Business Template, if force, all will be upgraded or installed
        otherwise depends of dict object_to_update
      """
      if object_to_update is not None:
        force=0
      else:
        object_to_update = {}

      installed_bt = self.portal_templates.getInstalledBusinessTemplate(
                                                           self.getTitle())
      # When reinstalling, installation state should not change to replaced
      if installed_bt not in [None, self]:
        if installed_bt.getTemplateFormatVersion() == 0:
          force = 1
        installed_bt.replace(self)

      trash_tool = getToolByName(self, 'portal_trash', None)
      if trash_tool is None and self.getTemplateFormatVersion() == 1:
        raise AttributeError, 'Trash Tool is not installed'

      # Check the format of business template, if old, force install
      if self.getTemplateFormatVersion() == 0:
        force = 1

      if not force:
        self.checkDependencies()

      site = self.getPortalObject()
      custom_generator_class = getattr(site, '_generator_class', None)
      if custom_generator_class is not None:
        gen = custom_generator_class()
      else:
        from Products.ERP5.ERP5Site import ERP5Generator
        gen = ERP5Generator()
      # update activity tool first if necessary
      if self.getTitle() == 'erp5_core' and self.getTemplateUpdateTool():
        LOG('Business Template', 0, 'Updating Activity Tool')
        gen.setupLastTools(site, update=1, create_activities=1)
      if not force:
        if len(object_to_update) == 0:
          # check if we have to update tools
          if self.getTitle() == 'erp5_core' and self.getTemplateUpdateTool():
            LOG('Business Template', 0, 'Updating Tools')
            gen.setup(site, 0, update=1)
          if self.getTitle() == 'erp5_core' and self.getTemplateUpdateBusinessTemplateWorkflow():
            LOG('Business Template', 0, 'Updating Business Template Workflows')
            gen.setupWorkflow(site)
          return

      # always created a trash bin because we may to save object already present
      # but not in a previous business templates apart at creation of a new site
      if trash_tool is not None and (len(object_to_update) > 0 or len(self.portal_templates) > 1):
        trashbin = trash_tool.newTrashBin(self.getTitle(), self)
      else:
        trashbin = None

      # Install everything
      if len(object_to_update) or force:
        for item_name in self._item_name_list:
          item = getattr(self, item_name, None)
          if item is not None:
            item.install(self, force=force, object_to_update=object_to_update, trashbin=trashbin, installed_bt=installed_bt)

      # update catalog if necessary
      if force and self.isCatalogUpdatable():
        update_catalog = 1
      if update_catalog:
        catalog = _getCatalogValue(self)
        if (catalog is None) or (not site.isIndexable):
          LOG('Business Template', 0, 'no SQL Catalog available')
          update_catalog = 0
        else:
          LOG('Business Template', 0, 'Updating SQL Catalog')
          catalog.manage_catalogClear()

      # get objects to remove
      # do remove after because we may need backup object from installation
      remove_object_dict = {}
      for path, action in object_to_update.iteritems():
        if action in ('remove', 'save_and_remove'):
          remove_object_dict[path] = action

      # remove object from old business template
      if len(remove_object_dict):
        # XXX: this code assumes that there is an installed_bt
        for item_name in reversed(installed_bt._item_name_list):
          item = getattr(installed_bt, item_name, None)
          if item is not None:
            item.remove(self, remove_object_dict=remove_object_dict, trashbin=trashbin)


      # update tools if necessary
      if self.getTitle() == 'erp5_core' and self.getTemplateUpdateTool():
        LOG('Business Template', 0, 'Updating Tools')
        gen.setup(site, 0, update=1)

      # check if we have to update business template workflow
      if self.getTitle() == 'erp5_core' and self.getTemplateUpdateBusinessTemplateWorkflow():
        LOG('Business Template', 0, 'Updating Business Template Workflows')
        gen.setupWorkflow(site)
        # XXX keep TM in case update of workflow doesn't work
        #         self._v_txn = WorkflowUpdateTM()
        #         self._v_txn.register(update=1, gen=gen, site=site)

      # remove trashbin if empty
      if trashbin is not None:
        if len(trashbin) == 0:
          trash_tool.manage_delObjects([trashbin.getId(),])

      if update_catalog:
        site.ERP5Site_reindexAll()

      # Update translation table, in case we added new portal types or
      # workflow states.
      if update_translation:
        site.ERP5Site_updateTranslationTable()

      # Clear cache to avoid reusing cached values with replaced objects.
      site.portal_caches.clearAllCache()

    security.declareProtected(Permissions.ManagePortal, 'install')
    def install(self, **kw):
      """
        For install based on paramaters provided in **kw
      """
      return self._install(**kw)

    install = WorkflowMethod(install)

    security.declareProtected(Permissions.ManagePortal, 'reinstall')
    def reinstall(self, **kw):
      """Reinstall Business Template.
      """
      return self._install(**kw)

    reinstall = WorkflowMethod(reinstall)

    security.declareProtected(Permissions.ManagePortal, 'trash')
    def trash(self, new_bt, **kw):
      """
        Trash unnecessary items before upgrading to a new business
        template.
        This is similar to uninstall, but different in that this does
        not remove all items.
      """
      # Trash everything
      for item_name in self._item_name_list[::-1]:
        item = getattr(self, item_name, None)
        if item is not None:
          item.trash(
                self,
                getattr(new_bt, item_name))

    security.declareProtected(Permissions.ManagePortal, 'uninstall')
    def uninstall(self, **kw):
      """
        For uninstall based on paramaters provided in **kw
      """
      # Uninstall everything
      # Trash everything
      for item_name in self._item_name_list[::-1]:
        item = getattr(self, item_name, None)
        if item is not None:
          item.uninstall(self)
      # It is better to clear cache because the uninstallation of a
      # template deletes many things from the portal.
      self.getPortalObject().portal_caches.clearAllCache()

    uninstall = WorkflowMethod(uninstall)

    security.declareProtected(Permissions.ManagePortal, 'clean')
    def _clean(self):
      """
        Clean built information.
      """
      # First, remove obsolete attributes if present.
      for attr in ( '_action_archive',
                    '_document_archive',
                    '_extension_archive',
                    '_test_archive',
                    '_module_archive',
                    '_object_archive',
                    '_portal_type_archive',
                    '_property_archive',
                    '_property_sheet_archive'):
        if hasattr(self, attr):
          delattr(self, attr)
      # Secondly, make attributes empty.
      for item_name in self._item_name_list:
        item = setattr(self, item_name, None)

    clean = WorkflowMethod(_clean)

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getBuildingState')
    def getBuildingState(self, default=None, id_only=1):
      """
        Returns the current state in building
      """
      portal_workflow = getToolByName(self, 'portal_workflow')
      wf = portal_workflow.getWorkflowById(
                          'business_template_building_workflow')
      return wf._getWorkflowStateOf(self, id_only=id_only )

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getInstallationState')
    def getInstallationState(self, default=None, id_only=1):
      """
        Returns the current state in installation
      """
      portal_workflow = getToolByName(self, 'portal_workflow')
      wf = portal_workflow.getWorkflowById(
                           'business_template_installation_workflow')
      return wf._getWorkflowStateOf(self, id_only=id_only )

    security.declareProtected(Permissions.AccessContentsInformation, 'toxml')
    def toxml(self):
      """
        Return this Business Template in XML
      """
      portal_templates = getToolByName(self, 'portal_templates')
      export_string = portal_templates.manage_exportObject(
                                               id=self.getId(),
                                               toxml=1,
                                               download=1)
      return export_string

    def _getOrderedList(self, id):
      """
        We have to set this method because we want an
        ordered list
      """
      method_id = '_baseGet%sList' % convertToUpperCase(id)
      result = getattr(self, method_id)(())
      if result is None: result = ()
      if result != ():
        result = list(result)
        result.sort()
        # XXX Why do we need to return a tuple ?
        result = tuple(result)
      return result

    def getTemplateCatalogMethodIdList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_catalog_method_id')

    def getTemplateBaseCategoryList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_base_category')

    def getTemplateWorkflowIdList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_workflow_id')

    def getTemplatePortalTypeIdList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_portal_type_id')

    def getTemplatePortalTypeWorkflowChainList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_portal_type_workflow_chain')

    def getTemplatePathList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_path')

    def getTemplatePreferenceList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_preference')

    def getTemplatePortalTypeAllowedContentTypeList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_portal_type_allowed_content_type')

    def getTemplatePortalTypeHiddenContentTypeList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_portal_type_hidden_content_type')

    def getTemplatePortalTypePropertySheetList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_portal_type_property_sheet')

    def getTemplatePortalTypeBaseCategoryList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_portal_type_base_category')

    def getTemplateActionPathList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_action_path')

    def getTemplatePortalTypeRoleList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_portal_type_role')

    def getTemplateLocalRoleList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_local_role')

    def getTemplateSkinIdList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_skin_id')

    def getTemplateRegisteredSkinSelectionList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_registered_skin_selection')

    def getTemplateModuleIdList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_module_id')

    def getTemplateMessageTranslationList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_message_translation')

    def getTemplateToolIdList(self):
      """
      We have to set this method because we want an
      ordered list
      """
      return self._getOrderedList('template_tool_id')

    security.declareProtected(Permissions.ManagePortal, 'export')
    def export(self, path=None, local=0, **kw):
      """
        Export this Business Template
      """
      if self.getBuildingState() != 'built':
        raise TemplateConditionError, \
              'Business Template must be built before export'

      if local:
        # we export into a folder tree
        bta = BusinessTemplateFolder(creation=1, path=path)
      else:
        # We export BT into a tarball file
        bta = BusinessTemplateTarball(creation=1, path=path)

      # export bt
      bta.addFolder(path+os.sep+'bt')
      for prop in self.propertyMap():
        prop_type = prop['type']
        id = prop['id']
        if id in ('id', 'uid', 'rid', 'sid', 'id_group', 'last_id',
                  'install_object_list_list', 'id_generator', 'bt_for_diff'):
          continue
        value = self.getProperty(id)
        if prop_type in ('text', 'string', 'int', 'boolean'):
          bta.addObject(obj=value, name=id, path=path+os.sep+'bt', ext='')
        elif prop_type in ('lines', 'tokens'):
          bta.addObject(obj=str('\n').join(value), name=id,
                        path=path+os.sep+'bt', ext='')

      # Export each part
      for item_name in self._item_name_list:
        getattr(self, item_name).export(context=self, bta=bta)

      return bta.finishCreation()

    security.declareProtected(Permissions.ManagePortal, 'importFile')
    def importFile(self, dir = 0, file=None, root_path=None):
      """
        Import all xml files in Business Template
      """
      if dir:
        bta = BusinessTemplateFolder(importing=1, file=file, path=root_path)
      else:
        bta = BusinessTemplateTarball(importing=1, file=file)
      self._portal_type_item = \
          PortalTypeTemplateItem(self.getTemplatePortalTypeIdList())
      self._portal_type_workflow_chain_item = \
          PortalTypeWorkflowChainTemplateItem(self.getTemplatePortalTypeWorkflowChainList())
      self._workflow_item = \
          WorkflowTemplateItem(self.getTemplateWorkflowIdList())
      self._skin_item = \
          SkinTemplateItem(self.getTemplateSkinIdList())
      self._registered_skin_selection_item = \
          RegisteredSkinSelectionTemplateItem(
              self.getTemplateRegisteredSkinSelectionList())
      self._category_item = \
          CategoryTemplateItem(self.getTemplateBaseCategoryList())
      self._catalog_method_item = \
          CatalogMethodTemplateItem(self.getTemplateCatalogMethodIdList())
      self._action_item = \
          ActionTemplateItem(self.getTemplateActionPathList())
      self._portal_type_roles_item = \
          PortalTypeRolesTemplateItem(self.getTemplatePortalTypeRolesList())
      self._site_property_item = \
          SitePropertyTemplateItem(self.getTemplateSitePropertyIdList())
      self._module_item = \
          ModuleTemplateItem(self.getTemplateModuleIdList())
      self._document_item = \
          DocumentTemplateItem(self.getTemplateDocumentIdList())
      self._property_sheet_item = \
          PropertySheetTemplateItem(self.getTemplatePropertySheetIdList())
      self._constraint_item = \
          ConstraintTemplateItem(self.getTemplateConstraintIdList())
      self._extension_item = \
          ExtensionTemplateItem(self.getTemplateExtensionIdList())
      self._test_item = \
          TestTemplateItem(self.getTemplateTestIdList())
      self._product_item = \
          ProductTemplateItem(self.getTemplateProductIdList())
      self._role_item = \
          RoleTemplateItem(self.getTemplateRoleList())
      self._catalog_result_key_item = \
          CatalogResultKeyTemplateItem(
               self.getTemplateCatalogResultKeyList())
      self._catalog_related_key_item = \
          CatalogRelatedKeyTemplateItem(
               self.getTemplateCatalogRelatedKeyList())
      self._catalog_result_table_item = \
          CatalogResultTableTemplateItem(
               self.getTemplateCatalogResultTableList())
      self._message_translation_item = \
          MessageTranslationTemplateItem(
               self.getTemplateMessageTranslationList())
      self._path_item = \
               PathTemplateItem(self.getTemplatePathList())
      self._preference_item = \
               PreferenceTemplateItem(self.getTemplatePreferenceList())
      self._portal_type_allowed_content_type_item = \
           PortalTypeAllowedContentTypeTemplateItem(
               self.getTemplatePortalTypeAllowedContentTypeList())
      self._portal_type_hidden_content_type_item = \
           PortalTypeHiddenContentTypeTemplateItem(
               self.getTemplatePortalTypeHiddenContentTypeList())
      self._portal_type_property_sheet_item = \
           PortalTypePropertySheetTemplateItem(
               self.getTemplatePortalTypePropertySheetList())
      self._portal_type_base_category_item = \
           PortalTypeBaseCategoryTemplateItem(
               self.getTemplatePortalTypeBaseCategoryList())
      self._catalog_keyword_key_item = \
          CatalogKeywordKeyTemplateItem(
               self.getTemplateCatalogKeywordKeyList())
      self._catalog_datetime_key_item = \
          CatalogDateTimeKeyTemplateItem(
               self.getTemplateCatalogDatetimeKeyList())
      self._catalog_full_text_key_item = \
          CatalogFullTextKeyTemplateItem(
               self.getTemplateCatalogFullTextKeyList())
      self._catalog_request_key_item = \
          CatalogRequestKeyTemplateItem(
               self.getTemplateCatalogRequestKeyList())
      self._catalog_multivalue_key_item = \
          CatalogMultivalueKeyTemplateItem(
               self.getTemplateCatalogMultivalueKeyList())
      self._catalog_topic_key_item = \
          CatalogTopicKeyTemplateItem(
               self.getTemplateCatalogTopicKeyList())
      self._local_roles_item = \
          LocalRolesTemplateItem(
               self.getTemplateLocalRoleList())
      self._tool_item = \
          ToolTemplateItem(
               self.getTemplateToolIdList())
      self._catalog_scriptable_key_item = \
          CatalogScriptableKeyTemplateItem(
               self.getTemplateCatalogScriptableKeyList())
      self._catalog_role_key_item = \
          CatalogRoleKeyTemplateItem(
               self.getTemplateCatalogRoleKeyList())
      self._catalog_local_role_key_item = \
          CatalogLocalRoleKeyTemplateItem(
               self.getTemplateCatalogLocalRoleKeyList())

      # Create temporary modules/classes for classes defined by this BT.
      # This is required if the BT contains instances of one of these classes.
      module_id_list = []
      for template_type in ('Constraint', 'Document', 'PropertySheet'):
        for template_id in getattr(self,
                                   'getTemplate%sIdList' % template_type)():
          module_id = 'Products.ERP5Type.%s.%s' % (template_type, template_id)
          if module_id not in sys.modules:
            module_id_list.append(module_id)
            sys.modules[module_id] = module = imp.new_module(module_id)
            module.SimpleItem = SimpleItem.SimpleItem
            exec "class %s(SimpleItem): pass" % template_id in module.__dict__

      for item_name in self._item_name_list:
        getattr(self, item_name).importFile(bta)

      # Remove temporary modules created above to allow import of real modules
      # (during the installation).
      for module_id in module_id_list:
        del sys.modules[module_id]

    def getItemsList(self):
      """Return list of items in business template
      """
      items_list = []
      for item_name in self._item_name_list:
        item = getattr(self, item_name, None)
        if item is not None:
          items_list.extend(item.getKeys())
      return items_list

    def checkDependencies(self):
      """
       Check if all the dependencies of the business template
       are installed. Raise an exception with the list of
       missing dependencies if some are missing
      """
      missing_dep_list = []
      dependency_list = self.getDependencyList()
      if len(dependency_list)!=0:
        for dependency_couple in dependency_list:
          dependency_couple_list = dependency_couple.strip().split(' ', 1)
          dependency = dependency_couple_list[0]
          if dependency in (None, ''):
            continue
          version_restriction = None
          if len(dependency_couple_list) > 1:
            version_restriction = dependency_couple_list[1]
            if version_restriction.startswith('('):
              # Something like "(>= 1.0rc6)".
              version_restriction = version_restriction[1:-1]
          installed_bt = self.portal_templates.getInstalledBusinessTemplate(dependency)
          if (not self.portal_templates.IsOneProviderInstalled(dependency)) \
             and ((installed_bt is None) \
                  or (version_restriction not in (None, '') and
                     (not self.portal_templates.compareVersionStrings(installed_bt.getVersion(), version_restriction)))):
            missing_dep_list.append((dependency, version_restriction or ''))
      if len(missing_dep_list) != 0:
        raise BusinessTemplateMissingDependency, 'Impossible to install, please install the following dependencies before: %s'%repr(missing_dep_list)

    def diffObject(self, REQUEST, **kw):
      """
        Make a diff between an object in the Business Template
        and the same in the Business Template installed in the site
      """

      class_name_dict = {
        'Product' : '_product_item',
        'PropertySheet' : '_property_sheet_item',
        'Constraint' : '_constraint_item',
        'Document' : '_document_item',
        'Extension' : '_extension_item',
        'Test' : '_test_item',
        'Role' : '_role_item',
        'MessageTranslation' : '_message_translation_item',
        'Workflow' : '_workflow_item',
        'CatalogMethod' : '_catalog_method_item',
        'SiteProperty' : '_site_property_item',
        'PortalType' : '_portal_type_item',
        'PortalTypeWorkflowChain' : '_portal_type_workflow_chain_item',
        'PortalTypeAllowedContentType' : '_portal_type_allowed_content_type_item',
        'PortalHiddenAllowedContentType' : '_portal_type_hidden_content_type_item',
        'PortalTypePropertySheet' : '_portal_type_property_sheet_item',
        'PortalTypeBaseCategory' : '_portal_type_base_category_item',
        'Category' : '_category_item',
        'Module' : '_module_item',
        'Skin' : '_skin_item',
        'RegisteredSkinSelection' : '_registered_skin_selection_item',
        'Path' : '_path_item',
        'Preference' : '_preference_item',
        'Action' : '_action_item',
        'PortalTypeRoles' : '_portal_type_roles_item',
        'LocalRoles' : '_local_roles_item',
        'CatalogResultKey' : '_catalog_result_key_item',
        'CatalogRelatedKey' : '_catalog_related_key_item',
        'CatalogResultTable' : '_catalog_result_table_item',
        'CatalogKeywordKey' : '_catalog_keyword_key_item',
        'CatalogDateTimeKey' : '_catalog_datetime_key_item',
        'CatalogFullTextKey' : '_catalog_full_text_key_item',
        'CatalogRequestKey' : '_catalog_request_key_item',
        'CatalogMultivalueKey' : '_catalog_multivalue_key_item',
        'CatalogTopicKey' : '_catalog_topic_key_item',
        'Tool': '_tool_item',
        'CatalogScriptableKey' : '_catalog_scriptable_key_item',
        'CatalogRoleKey' : '_catalog_role_key_item',
        'CatalogLocalRoleKey' : '_catalog_local_role_key_item',
        }

      object_id = REQUEST.object_id
      object_class = REQUEST.object_class

      # Get objects
      item_name = class_name_dict[object_class]

      new_bt =self
      # Compare with a given business template
      compare_to_zodb = 0
      bt2_id = kw.get('compare_with', None)
      if bt2_id is not None:
        if bt2_id == self.getId():
          compare_to_zodb = 1
          installed_bt = self.getInstalledBusinessTemplate(title=self.getTitle())
        else:
          installed_bt = self.portal_templates._getOb(bt2_id)
      else:
        installed_bt = self.getInstalledBusinessTemplate(title=self.getTitle())
        if installed_bt == new_bt:
          compare_to_zodb = 1
      if compare_to_zodb:
        bt2 = self.portal_templates.manage_clone(ob=installed_bt, id=INSTALLED_BT_FOR_DIFF)
        # Update portal types properties to get last modifications
        bt2.getPortalTypesProperties()
        bt2.edit(description='tmp bt generated for diff')
        installed_bt = bt2

      new_item = getattr(new_bt, item_name)
      installed_item = getattr(installed_bt, item_name)
      if compare_to_zodb:
        # XXX maybe only build for the given object to gain time
        installed_item.build(self)
      new_object = new_item._objects[object_id]
      installed_object = installed_item._objects[object_id]
      diff_msg = ''

      # Real Zope Objects (can be exported into XML directly by Zope)
      # XXX Bad naming
      item_list_1 = ['_product_item', '_workflow_item', '_portal_type_item',
                     '_category_item', '_path_item', '_preference_tem',
                     '_skin_item', '_action_item', '_tool_item', ]

      # Not considered as objects by Zope (will be exported into XML manually)
      # XXX Bad naming
      item_list_2 = ['_site_property_item', '_module_item',
                     '_catalog_result_key_item', '_catalog_related_key_item',
                     '_catalog_result_table_item',
                     '_catalog_keyword_key_item',
                     '_catalog_datetime_key_item',
                     '_catalog_full_text_key_item',
                     '_catalog_request_key_item',
                     '_catalog_multivalue_key_item',
                     '_catalog_topic_key_item',
                     '_catalog_scriptable_key_item',
                     '_catalog_role_key_item',
                     '_catalog_local_role_key_item',
                     '_portal_type_allowed_content_type_item',
                     '_portal_type_hidden_content_type_item',
                     '_portal_type_property_sheet_item',
                     '_portal_type_roles_item',
                     '_portal_type_base_category_item',
                     '_local_roles_item',
                     '_portal_type_workflow_chain_item',]

      # Text objects (no need to export them into XML)
      # XXX Bad naming
      item_list_3 = ['_document_item', '_property_sheet_item',
                     '_constraint_item', '_extension_item',
                     '_test_item', '_message_translation_item',]

      if item_name in item_list_1:
        f1 = StringIO() # for XML export of New Object
        f2 = StringIO() # For XML export of Installed Object
        # Remove unneeded properties
        new_object = new_item.removeProperties(new_object)
        installed_object = installed_item.removeProperties(installed_object)
        # XML Export in memory
        OFS.XMLExportImport.exportXML(new_object._p_jar, new_object._p_oid, f1)
        OFS.XMLExportImport.exportXML(installed_object._p_jar, installed_object._p_oid, f2)
        new_obj_xml = f1.getvalue()
        f1.close()
        installed_obj_xml = f2.getvalue()
        f2.close()
        new_ob_xml_lines = new_obj_xml.splitlines()
        installed_ob_xml_lines = installed_obj_xml.splitlines()
        # End of XML export

        # Diff between XML objects
        diff_list = list(unified_diff(installed_ob_xml_lines, new_ob_xml_lines, tofile=new_bt.getId(), fromfile=installed_bt.getId(), lineterm=''))
        if len(diff_list) != 0:
          diff_msg += '\n\nObject %s diff :\n' % (object_id,)
          diff_msg += '\n'.join(diff_list)
        else:
          diff_msg = 'No diff'

      elif item_name in item_list_2:
        # Generate XML code manually
        new_obj_xml = new_item.generateXml(path= object_id)
        installed_obj_xml = installed_item.generateXml(path= object_id)
        new_obj_xml_lines = new_obj_xml.splitlines()
        installed_obj_xml_lines = installed_obj_xml.splitlines()
        # End of XML Code Generation

        # Diff between XML objects
        diff_list = list(unified_diff(installed_obj_xml_lines, new_obj_xml_lines, tofile=new_bt.getId(), fromfile=installed_bt.getId(), lineterm=''))
        if len(diff_list) != 0:
          diff_msg += '\n\nObject %s diff :\n' % (object_id,)
          diff_msg += '\n'.join(diff_list)
        else:
          diff_msg = 'No diff'

      elif item_name in item_list_3:
        # Diff between text objects
        new_obj_lines = new_object.splitlines()
        installed_obj_lines = installed_object.splitlines()
        diff_list = list(unified_diff(installed_obj_lines, new_obj_lines, tofile=new_bt.getId(), fromfile=installed_bt.getId(), lineterm=''))
        if len(diff_list) != 0:
          diff_msg += '\n\nObject %s diff :\n' % (object_id,)
          diff_msg += '\n'.join(diff_list)
        else:
          diff_msg = 'No diff'

      else:
        diff_msg += 'Unsupported file !'

      if compare_to_zodb:
        self.portal_templates.manage_delObjects(ids=[INSTALLED_BT_FOR_DIFF])

      return diff_msg


    def getPortalTypesProperties(self, **kw):
      """
      Fill field about properties for each portal type
      """
      wtool = self.getPortalObject().portal_workflow
      ttool = self.getPortalObject().portal_types
      bt_allowed_content_type_list = list(getattr(self, 'template_portal_type_allowed_content_type', []) or [])
      bt_hidden_content_type_list = list(getattr(self, 'template_portal_type_hidden_content_type', []) or [])
      bt_property_sheet_list = list(getattr(self, 'template_portal_type_property_sheet', []) or [])
      bt_base_category_list = list(getattr(self, 'template_portal_type_base_category', []) or [])
      bt_action_list = list(getattr(self, 'template_action_path', []) or [])
      bt_portal_types_id_list = list(self.getTemplatePortalTypeIdList())
      bt_portal_type_roles_list =  list(getattr(self, 'template_portal_type_roles', []) or [])
      bt_wf_chain_list = list(getattr(self, 'template_portal_type_workflow_chain', []) or [])

      p = self.getPortalObject()
      for id in bt_portal_types_id_list:
        portal_type = ttool.getTypeInfo(id)
        if portal_type is None:
          continue
        if portal_type.getRoleInformationList():
          if id not in bt_portal_type_roles_list:
            bt_portal_type_roles_list.append(id)

        allowed_content_type_list = []
        hidden_content_type_list = []
        property_sheet_list = []
        base_category_list = []
        action_list = []
        if hasattr(portal_type, 'allowed_content_types'):
          allowed_content_type_list = portal_type.allowed_content_types
        if hasattr(portal_type, 'hidden_content_type_list'):
          hidden_content_type_list = portal_type.hidden_content_type_list
        if hasattr(portal_type, 'property_sheet_list'):
          property_sheet_list = portal_type.property_sheet_list
        if hasattr(portal_type, 'base_category_list'):
          base_category_list = portal_type.base_category_list
        for action in portal_type.getActionInformationList():
          action_list.append(action.getReference())

        for a_id in allowed_content_type_list:
          allowed_id = id+' | '+a_id
          if allowed_id not in bt_allowed_content_type_list:
            bt_allowed_content_type_list.append(allowed_id)

        for h_id in hidden_content_type_list:
          hidden_id = id+' | '+h_id
          if hidden_id not in bt_hidden_content_type_list:
            bt_hidden_content_type_list.append(hidden_id)

        for ps_id in property_sheet_list:
          p_sheet_id = id+' | '+ps_id
          if p_sheet_id not in bt_property_sheet_list:
            bt_property_sheet_list.append(p_sheet_id)

        for bc_id in base_category_list:
          base_cat_id = id+' | '+bc_id
          if base_cat_id not in bt_base_category_list:
            bt_base_category_list.append(base_cat_id)

        for act_id in action_list:
          action_id = id+' | '+act_id
          if action_id not in bt_action_list:
            bt_action_list.append(action_id)

        for workflow_id in [chain for chain in wtool.getChainFor(id)
                                    if chain != '(Default)']:
          wf_id = id+' | '+workflow_id
          if wf_id not in bt_wf_chain_list:
            bt_wf_chain_list.append(wf_id)

      bt_allowed_content_type_list.sort()
      bt_hidden_content_type_list.sort()
      bt_property_sheet_list.sort()
      bt_base_category_list.sort()
      bt_action_list.sort()
      bt_wf_chain_list.sort()

      self.setProperty('template_portal_type_workflow_chain', bt_wf_chain_list)
      self.setProperty('template_portal_type_roles', bt_portal_type_roles_list)
      self.setProperty('template_portal_type_allowed_content_type', bt_allowed_content_type_list)
      self.setProperty('template_portal_type_hidden_content_type', bt_hidden_content_type_list)
      self.setProperty('template_portal_type_property_sheet', bt_property_sheet_list)
      self.setProperty('template_portal_type_base_category', bt_base_category_list)
      self.setProperty('template_action_path', bt_action_list)
      return


    def guessPortalTypes(self, **kw):
      """
      This method guesses portal types based on modules define in the Business Template
      """
      bt_module_id_list = list(self.getTemplateModuleIdList())
      if len(bt_module_id_list) == 0:
        raise TemplateConditionError, 'No module defined in business template'

      bt_portal_types_id_list = list(self.getTemplatePortalTypeIdList())

      def getChildPortalType(type_id):
        type_list = {}
        p = self.getPortalObject()
        try:
          portal_type = p.unrestrictedTraverse('portal_types/'+type_id)
        except KeyError:
          return type_list

        allowed_content_type_list = []
        hidden_content_type_list = []
        if hasattr(portal_type, 'allowed_content_types'):
          allowed_content_type_list = portal_type.allowed_content_types
        if hasattr(portal_type, 'hidden_content_type_list'):
          hidden_content_type_list = portal_type.hidden_content_type_list
        type_list[type_id] = ()
        # get same info for allowed portal types and hidden portal types
        for allowed_ptype_id in allowed_content_type_list:
          if allowed_ptype_id not in type_list.keys():
            type_list.update(getChildPortalType(allowed_ptype_id))
        for hidden_ptype_id in hidden_content_type_list:
          if hidden_ptype_id not in type_list.keys():
            type_list.update(getChildPortalType(hidden_ptype_id))
        return type_list

      p = self.getPortalObject()
      portal_dict = {}
      for module_id in bt_module_id_list:
        module = p.unrestrictedTraverse(module_id)
        portal_type_id = module.getPortalType()
        try:
          portal_type = p.unrestrictedTraverse('portal_types/'+portal_type_id)
        except KeyError:
          continue
        allowed_content_type_list = []
        hidden_content_type_list = []
        if hasattr(portal_type, 'allowed_content_types'):
          allowed_content_type_list = portal_type.allowed_content_types
        if hasattr(portal_type, 'hidden_content_type_list'):
          hidden_content_type_list = portal_type.hidden_content_type_list

        portal_dict[portal_type_id] = ()

        for allowed_type_id in allowed_content_type_list:
          if allowed_type_id not in portal_dict.keys():
            portal_dict.update(getChildPortalType(allowed_type_id))

        for hidden_type_id in hidden_content_type_list:
          if hidden_type_id not in portal_dict.keys():
            portal_dict.update(getChildPortalType(hidden_type_id))

      # construct portal type list, keep already present portal types
      for id in portal_dict.keys():
        if id not in bt_portal_types_id_list:
          bt_portal_types_id_list.append(id)

      bt_portal_types_id_list.sort()

      setattr(self, 'template_portal_type_id', bt_portal_types_id_list)
      return

    def clearPortalTypes(self, **kw):
      """
      clear id list register for portal types
      """
      setattr(self, 'template_portal_type_id', ())
      setattr(self, 'template_portal_type_allowed_content_type', ())
      setattr(self, 'template_portal_type_hidden_content_type', ())
      setattr(self, 'template_portal_type_property_sheet', ())
      setattr(self, 'template_portal_type_base_category', ())
      return

# Block acquisition on all _item_name_list properties by setting
# a default class value to None
for key in BusinessTemplate._item_name_list:
  setattr(BusinessTemplate, key, None)

# Transaction Manager used for update of business template workflow
# XXX update seems to works without it

# from Shared.DC.ZRDB.TM import TM

# class WorkflowUpdateTM(TM):

#   _p_oid=_p_changed=_registered=None
#   _update = 0

#   def __init__(self, ):
#     LOG('init TM', 0, '')

#   def register(self, update=0, gen=None, site=None):
#     LOG('register TM', 0, update)
#     self._gen = gen
#     self._site = site
#     self._update = update
#     self._register()

#   def tpc_prepare(self, *d, **kw):
#     LOG("tpc_prepare", 0, self._update)
#     if self._update:
#       # do it one time
#       self._update = 0
#       LOG('call update of wf', 0, '')
#       self._gen.setupWorkflow(self._site)


#   def _finish(self, **kw):
#     LOG('finish TM', 0, '')
#     pass

#   def _abort(self, **kw):
#     LOG('abort TM', 0, '')
#     pass

