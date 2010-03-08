# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2005 Nexedi SARL and Contributors. All Rights Reserved.
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

from AccessControl import ClassSecurityInfo, getSecurityManager
from MethodObject import Method
from Products.ERP5Type.Globals import InitializeClass, DTMLFile
from zLOG import LOG, PROBLEM

from Products.CMFCore.utils import getToolByName
from Products.ERP5Type.Tool.BaseTool import BaseTool
from Products.ERP5Type import Permissions, PropertySheet
from Products.ERP5Type.Cache import CachingMethod
from Products.ERP5Type.Utils import convertToUpperCase
from Products.ERP5Type.Accessor.TypeDefinition import list_types
from Products.ERP5Form import _dtmldir
from Products.ERP5Form.Document.Preference import Priority

_marker = object()

def updatePreferenceClassPropertySheetList():
  # The Preference class should be imported from the common location
  # in ERP5Type since it could be overloaded in another product
  from Products.ERP5Type.Document.Preference import Preference
  # 'Static' property sheets defined on the class
  class_property_sheet_list = Preference.property_sheets
  # Time to lookup for preferences defined on other modules
  property_sheets = list(class_property_sheet_list)
  for id in dir(PropertySheet):
    if id.endswith('Preference'):
      ps = getattr(PropertySheet, id)
      if ps not in property_sheets:
        property_sheets.append(ps)
  class_property_sheet_list = tuple(property_sheets)
  Preference.property_sheets = class_property_sheet_list


def createPreferenceToolAccessorList(portal) :
  """
    Initialize all Preference methods on the preference tool.
    This method must be called on startup.

    This tool is capable of updating the list of Preference
    property sheets by looking at all registered property sheets
    and considering those which name ends with 'Preference'
  """
  property_list = []

  # 'Dynamic' property sheets added by portal_type
  pref_portal_type = portal.portal_types.getTypeInfo('Preference')
  if pref_portal_type is None:
    LOG('ERP5Form.PreferenceTool', PROBLEM,
        'Preference type information is not installed.')
  else:
    pref_portal_type.updatePropertySheetDefinitionDict(
      {'_properties': property_list})

  # 'Static' property sheets defined on the class
  # The Preference class should be imported from the common location
  # in ERP5Type since it could be overloaded in another product
  from Products.ERP5Type.Document.Preference import Preference
  for property_sheet in Preference.property_sheets:
    property_list += property_sheet._properties

  # Generate common method names
  for prop in property_list:
    if prop.get('preference'):
      # only properties marked as preference are used
      attribute = prop['id']
      attr_list = [ 'get%s' % convertToUpperCase(attribute)]
      if prop['type'] in list_types :
        attr_list +=  ['get%sList' % convertToUpperCase(attribute), ]
      for attribute_name in attr_list:
        method = PreferenceMethod(attribute_name, prop.get('default'))
        setattr(PreferenceTool, attribute_name, method)


class func_code: pass

class PreferenceMethod(Method):
  """ A method object that lookup the attribute on preferences. """
  # This is required to call the method form the Web
  func_code = func_code()
  func_code.co_varnames = ('self', )
  func_code.co_argcount = 1
  func_defaults = ()

  def __init__(self, attribute, default):
    self.__name__ = self._preference_getter = attribute
    self._preference_default = default
    self._preference_cache_id = 'PreferenceTool.CachingMethod.%s' % attribute

  def __call__(self, instance, default=_marker, *args, **kw):
    def _getPreference(*args, **kw):
      # XXX: sql_catalog_id is passed when calling getPreferredArchive
      # This is inconsistent with regular accessor API, and indicates that
      # there is a design problem in current archive API.
      sql_catalog_id = kw.pop('sql_catalog_id', None)
      for pref in instance._getSortedPreferenceList(sql_catalog_id=sql_catalog_id):
        value = getattr(pref, self._preference_getter)(_marker, *args, **kw)
        # XXX Due to UI limitation, null value is treated as if the property
        #     was not defined. The drawback is that it is not possible for a
        #     user to mask a non-null global value with a null value.
        if value not in (_marker, None, '', (), []):
          return value
      return _marker
    _getPreference = CachingMethod(_getPreference,
            id='%s.%s' % (self._preference_cache_id,
                          getSecurityManager().getUser().getId()),
            cache_factory='erp5_ui_short')
    value = _getPreference(*args, **kw)
    if value is not _marker:
      return value
    elif default is _marker:
      return self._preference_default
    return default

class PreferenceTool(BaseTool):
  """
    PreferenceTool manages User Preferences / User profiles.

    TODO:
      - make the preference tool an action provider (templates)
  """
  id            = 'portal_preferences'
  meta_type     = 'ERP5 Preference Tool'
  portal_type   = 'Preference Tool'
  title         = 'Preferences'
  allowed_types = ( 'ERP5 Preference',)
  security      = ClassSecurityInfo()

  security.declareProtected(
       Permissions.ManagePortal, 'manage_overview' )
  manage_overview = DTMLFile( 'explainPreferenceTool', _dtmldir )

  security.declarePrivate('manage_afterAdd')
  def manage_afterAdd(self, item, container) :
    """ init the permissions right after creation """
    item.manage_permission(Permissions.AddPortalContent,
          ['Member', 'Author', 'Manager'])
    item.manage_permission(Permissions.AddPortalFolders,
          ['Member', 'Author', 'Manager'])
    item.manage_permission(Permissions.View,
          ['Member', 'Auditor', 'Manager'])
    item.manage_permission(Permissions.CopyOrMove,
          ['Member', 'Auditor', 'Manager'])
    item.manage_permission(Permissions.ManageProperties,
          ['Manager'], acquire=0)
    item.manage_permission(Permissions.SetOwnPassword,
          ['Member', 'Author', 'Manager'])
    BaseTool.inheritedAttribute('manage_afterAdd')(self, item, container)

  security.declarePublic('getPreference')
  def getPreference(self, pref_name, default=_marker) :
    """ get the preference on the most appopriate Preference object. """
    method = getattr(self, 'get%s' % convertToUpperCase(pref_name), None)
    if method is not None:
      return method(default)
    return default

  security.declareProtected(Permissions.ModifyPortalContent, "setPreference")
  def setPreference(self, pref_name, value) :
    """ set the preference on the active Preference object"""
    self.getActivePreference()._edit(**{pref_name:value})

  def _getSortedPreferenceList(self, sql_catalog_id=None):
    """ return the most appropriate preferences objects,
        sorted so that the first in the list should be applied first
    """
    prefs = []
    # XXX will also cause problems with Manager (too long)
    # XXX For manager, create a manager specific preference
    #                  or better solution
    user = getToolByName(self, 'portal_membership').getAuthenticatedMember()
    user_is_manager = 'Manager' in user.getRolesInContext(self)
    for pref in self.searchFolder(portal_type='Preference', sql_catalog_id=sql_catalog_id):
      pref = pref.getObject()
      if pref is not None and pref.getProperty('preference_state',
                                'broken') in ('enabled', 'global'):
        # XXX quick workaround so that manager only see user preference
        # they actually own.
        if user_is_manager and pref.getPriority() == Priority.USER :
          if pref.getOwnerTuple()[1] == user.getId():
            prefs.append(pref)
        else :
          prefs.append(pref)
    prefs.sort(key=lambda x: x.getPriority(), reverse=True)
    # add system preferences before user preferences
    sys_prefs = [x.getObject() for x in self.searchFolder(portal_type='System Preference', sql_catalog_id=sql_catalog_id) \
                 if x.getObject().getProperty('preference_state', 'broken') in ('enabled', 'global')]
    sys_prefs.sort(key=lambda x: x.getPriority(), reverse=True)
    return sys_prefs + prefs

  def _getActivePreferenceByPortalType(self, portal_type):
    enabled_prefs = self._getSortedPreferenceList()
    if len(enabled_prefs) > 0 :
      try:
        return [x for x in enabled_prefs
            if x.getPortalType() == portal_type][0]
      except IndexError:
        pass
    return None

  security.declareProtected(Permissions.View, 'getActivePreference')
  def getActivePreference(self) :
    """ returns the current preference for the user.
       Note that this preference may be read only. """
    return self._getActivePreferenceByPortalType('Preference')

  security.declareProtected(Permissions.View, 'getActiveSystemPreference')
  def getActiveSystemPreference(self) :
    """ returns the current system preference for the user.
       Note that this preference may be read only. """
    return self._getActivePreferenceByPortalType('System Preference')

  security.declareProtected(Permissions.View, 'getDocumentTemplateList')
  def getDocumentTemplateList(self, folder=None) :
    """ returns all document templates that are in acceptable Preferences
        based on different criteria such as folder, portal_type, etc.
    """
    if folder is None:
      # as the preference tool is also a Folder, this method is called by
      # page templates to get the list of document templates for self.
      folder = self

    # We must set the user_id as a parameter to make sure each
    # user can get a different cache
    def _getDocumentTemplateList(user_id, portal_type=None):
      acceptable_templates = []
      for pref in self._getSortedPreferenceList() :
        for doc in pref.contentValues() :
          if doc.getPortalType() == portal_type:
            acceptable_templates.append(doc.getRelativeUrl())
      return acceptable_templates
    _getDocumentTemplateList = CachingMethod(_getDocumentTemplateList,
                          'portal_preferences.getDocumentTemplateList',
                                             cache_factory='erp5_ui_medium')

    allowed_content_types = map(lambda pti: pti.id,
                                folder.allowedContentTypes())
    user_id = getToolByName(self, 'portal_membership').getAuthenticatedMember().getId()
    template_list = []
    for portal_type in allowed_content_types:
      for template_url in _getDocumentTemplateList(user_id, portal_type=portal_type):
        template = self.restrictedTraverse(template_url, None)
        if template is not None:
          template_list.append(template)
    return template_list

InitializeClass(PreferenceTool)

