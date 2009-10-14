##############################################################################
#
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#                    Julien Muchembled <jm@nexedi.com>
#
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

import imp, sys, warnings
import zope.interface
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder as OFSFolder
import transaction
from Products.CMFCore import TypesTool as CMFCore_TypesTool
from Products.ERP5Type.Tool.BaseTool import BaseTool
from Products.ERP5Type.Cache import CachingMethod
from Products.ERP5Type import interfaces, Permissions
from Products.ERP5Type.ERP5Type import ERP5TypeInformation
from Products.ERP5Type.UnrestrictedMethod import UnrestrictedMethod
from zLOG import LOG, WARNING, PANIC

class TypesTool(BaseTool, CMFCore_TypesTool.TypesTool):
  """Provides a configurable registry of portal content types
  """
  id = 'portal_types'
  meta_type = 'ERP5 Types Tool'
  portal_type = 'Types Tool'
  allowed_types = ()

  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  zope.interface.implements(interfaces.IActionProvider)

  security.declarePrivate('getActionListFor')
  def getActionListFor(self, ob=None):
    """Return all actions of the object"""
    if ob is not None:
      type_info = self.getTypeInfo(ob)
      if type_info is not None:
        return type_info.getActionListFor(ob)
    return ()

  security.declarePrivate('getFilteredActionListFor')
  def getFilteredActionListFor(self, ob=None):
    """Return all actions applicable to the object"""
    if ob is not None:
      type_info = self.getTypeInfo(ob)
      if type_info is not None:
        return type_info.getFilteredActionListFor(ob)
    return ()

  def getTypeInfo(self, *args):
    if not args:
       return BaseTool.getTypeInfo(self)
    portal_type, = args
    if not isinstance(portal_type, basestring):
      portal_type = aq_base(portal_type).getPortalType()
    return self._getOb(portal_type, None)

  security.declareProtected(Permissions.AddPortalContent,
                            'manage_addTypeInformation')
  def manage_addTypeInformation(self, add_meta_type, id=None,
                                typeinfo_name=None, RESPONSE=None):
    """
    Create a TypeInformation in self.

    This method is mainly a copy/paste of CMF Types Tool
    which means that the entire file is ZPLed for now.
    """
    if add_meta_type != 'ERP5 Type Information' or RESPONSE is not None:
      raise ValueError

    fti = None
    if typeinfo_name:
      info = self.listDefaultTypeInformation()
      # Nasty workaround to stay backwards-compatible
      # This workaround will disappear in CMF 1.7
      if typeinfo_name.endswith(')'):
        # This is a new-style name. Proceed normally.
        for name, ft in info:
          if name == typeinfo_name:
            fti = ft
            break
      else:
        # Attempt to work around the old way
        # This attempt harbors the problem that the first match on
        # meta_type will be used. There could potentially be more
        # than one TypeInformation sharing the same meta_type.
        warnings.warn('Please switch to the new format for typeinfo names '
                      '\"product_id: type_id (meta_type)\", the old '
                      'spelling will disappear in CMF 1.7', DeprecationWarning,
                      stacklevel=2)
        ti_prod, ti_mt = [x.strip() for x in typeinfo_name.split(':')]
        for name, ft in info:
          if name.startswith(ti_prod) and name.endswith('(%s)' % ti_mt):
            fti = ft
            break
      if fti is None:
        raise ValueError('%s not found.' % typeinfo_name)
      if not id:
        id = fti.get('id')
    if not id:
      raise ValueError('An id is required.')
    type_info = self.newContent(id, 'Base Type')
    if fti:
      if 'actions' in fti:
        warnings.warn('manage_addTypeInformation does not create default'
                      ' actions automatically anymore.')
      type_info.__dict__.update((k, v) for k, v in fti.iteritems()
        if k not in ('id', 'actions'))

  def _finalizeMigration(self):
    """Compatibility code to finalize migration from CMF Types Tool"""
    portal = self.getPortalObject()
    old_types_tool = portal.__dict__[OldTypesTool.id]
    #self.Base_setDefaultSecurity()
    trash_tool = getattr(portal, 'portal_trash', None)
    if trash_tool is not None:
      LOG('OldTypesTool', WARNING, 'Move old portal_types into a trash bin.')
      portal._objects = tuple(i for i in portal._objects
                                if i['id'] != old_types_tool.id)
      portal._delOb(old_types_tool.id)
      #old_types_tool.id = self.id # Not possible to keep the original id
                                   # due to limitation of getToolByName
      trashbin = UnrestrictedMethod(trash_tool.newTrashBin)(self.id)
      trashbin._setOb(old_types_tool.id, old_types_tool)

# Compatibility code to access old "ERP5 Role Information" objects.
OldRoleInformation = imp.new_module('Products.ERP5Type.RoleInformation')
sys.modules[OldRoleInformation.__name__] = OldRoleInformation
from OFS.SimpleItem import SimpleItem
OldRoleInformation.RoleInformation = SimpleItem

class OldTypesTool(OFSFolder):

  id = 'cmf_portal_types'

  def _migratePortalType(self, types_tool, old_type):
    if old_type.__class__ is not ERP5TypeInformation:
      LOG('OldTypesTool._migratePortalType', WARNING,
          "Can't convert %r (meta_type is %r)."
          % (old_type, old_type.meta_type))
      return
    new_type = ERP5TypeInformation(old_type.id, uid=None)
    types_tool._setObject(new_type.id, new_type, set_owner=0)
    new_type = types_tool[new_type.id]
    for k, v in  old_type.__dict__.iteritems():
      if k == '_actions':
        for action in v:
          new_type._importOldAction(action)
      elif k == '_roles':
        for role in v:
          new_type._importRole(role.__getstate__())
      else:
        if k == '_property_domain_dict':
          v = dict((k, t.__class__(property_name=t.property_name,
                                   domain_name=t.domain_name))
                   for k, t in v.iteritems())
        setattr(new_type, k, v)

  def _migrateTypesTool(self, parent):
    # 'parent' has no acquisition wrapper so migration must be done without
    # access to physical root. All activities are created with no leading '/'
    # in the path.
    LOG('OldTypesTool', WARNING, "Converting portal_types...")
    for object_info in parent._objects:
      if object_info['id'] == TypesTool.id:
        break
    types_tool = TypesTool()
    types_tool.__ac_local_roles__ = self.__ac_local_roles__.copy()
    try:
      setattr(parent, self.id, self)
      object_info['id'] = self.id
      del parent.portal_types
      parent._setObject(TypesTool.id, types_tool, set_owner=0)
      types_tool = types_tool.__of__(parent)
      if not parent.portal_categories.hasObject('action_type'):
        # Required to generate ActionInformation.getActionType accessor.
        from Products.ERP5Type.Document.BaseCategory import BaseCategory
        action_type = BaseCategory('action_type')
        action_type.uid = None
        parent.portal_categories._setObject(action_type.id, action_type)
      for type_info in self.objectValues():
        self._migratePortalType(types_tool, type_info)
      types_tool.activate()._finalizeMigration()
    except:
      transaction.abort()
      LOG('OldTypesTool', PANIC, 'Could not convert portal_types: ',
          error=sys.exc_info())
      raise # XXX The exception may be hidden by acquisition code
            #     (None returned instead)
    else:
      LOG('OldTypesTool', WARNING, "... portal_types converted.")
      return types_tool

  def __of__(self, parent):
    base_self = aq_base(self) # Is it required ?
    if parent.__dict__.get(TypesTool.id) is not base_self:
      return OFSFolder.__of__(self, parent)
    return UnrestrictedMethod(base_self._migrateTypesTool)(parent)

CMFCore_TypesTool.TypesTool = OldTypesTool
