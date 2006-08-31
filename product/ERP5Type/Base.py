##############################################################################
#
# Copyright (c) 2002-2003 Nexedi SARL and Contributors. All Rights Reserved.
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

import warnings
import ExtensionClass
from Globals import InitializeClass, DTMLFile, PersistentMapping
from AccessControl import ClassSecurityInfo
from AccessControl.Permission import pname, Permission
from Acquisition import aq_base, aq_inner, aq_acquire, aq_chain

from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName, _getViewFor

from Products.DCWorkflow.Transitions import TRIGGER_WORKFLOW_METHOD

from Products.ERP5Type import _dtmldir
from Products.ERP5Type import PropertySheet
from Products.ERP5Type import Permissions
from Products.ERP5Type.Utils import UpperCase
from Products.ERP5Type.Utils import convertToUpperCase, convertToMixedCase
from Products.ERP5Type.Utils import createExpressionContext
from Products.ERP5Type.Accessor.TypeDefinition import list_types
from Products.ERP5Type.Accessor import Base as BaseAccessor
from Products.ERP5Type.XMLExportImport import Base_asXML
from Products.ERP5Type.Cache import CachingMethod, clearCache, getReadOnlyTransactionCache
from Products.CMFCore.WorkflowCore import ObjectDeleted
from Accessor import WorkflowState

from ZopePatch import ERP5PropertyManager

from CopySupport import CopyContainer, CopyError,\
    tryMethodCallWithTemporaryPermission
from Errors import DeferredCatalogError
from Products.CMFActivity.ActiveObject import ActiveObject
from Products.ERP5Type.Accessor.Accessor import Accessor as Method
from Products.ERP5Type.Accessor.TypeDefinition import asDate

from string import join
import sys
import pickle
import copy
import psyco

from cStringIO import StringIO
from email.MIMEBase import MIMEBase
from email import Encoders
from socket import gethostname, gethostbyaddr
import random

from DateTime import DateTime

import inspect
from pprint import pformat

try:
  from transaction import get as get_transaction
except ImportError:
  pass

from ZODB.POSException import ConflictError
from zLOG import LOG, INFO, ERROR, WARNING

class WorkflowMethod(Method):

  def __init__(self, method, id=None, reindex=1):
    self._m = method
    if id is None:
        id = method.__name__
    self._id = id

  def _setId(self, id) :
    self._id = id

  def __call__(self, instance, *args, **kw):
    """
      Invoke the wrapped method, and deal with the results.
    """
    wf = getToolByName(instance, 'portal_workflow', None)
    if wf is None or not hasattr(wf, 'wrapWorkflowMethod'):
      # No workflow tool found.
      try:
        res = apply(self._m, (instance,) + args, kw)
      except ObjectDeleted, ex:
        res = ex.getResult()
      else:
        if hasattr(aq_base(instance), 'reindexObject'):
            instance.reindexObject()
    else:
      res = wf.wrapWorkflowMethod(instance, self._id, self.__dict__['_m'],
                                  (instance,) + args, kw)
    return res

def _aq_reset():
  Base.aq_method_generated = {}
  Base.aq_portal_type = {}
  Base.aq_related_generated = 0
  Base.aq_preference_generated = 0

  # Some method generations are based on portal methods, and portal methods cache results.
  # So it is safer to invalidate the cache.
  clearCache()

class PropertyHolder:
  isRADContent = 1
  def __init__(self):
    self.__name__ = 'PropertyHolder'

def getClassPropertyList(klass):
  ps_list = getattr(klass, 'property_sheets', ())
  ps_list = tuple(ps_list)
  for super_klass in klass.__bases__:
    if getattr(super_klass, 'isRADContent', 0): ps_list = ps_list + tuple(filter(lambda p: p not in ps_list,
                                                         getClassPropertyList(super_klass)))
  return ps_list

def initializeClassDynamicProperties(self, klass):
  if not Base.aq_method_generated.has_key(klass):
    # Recurse to superclasses
    for super_klass in klass.__bases__:
      if getattr(super_klass, 'isRADContent', 0):
        initializeClassDynamicProperties(self, super_klass)
    # Initialize default properties
    from Utils import initializeDefaultProperties
    if not getattr(klass, 'isPortalContent', None):
      initializeDefaultProperties([klass], object=self)
      # Mark as generated
      Base.aq_method_generated[klass] = 1

def initializePortalTypeDynamicProperties(self, klass, ptype):
  id = ''
  #LOG('before aq_portal_type %s' % id, 0, str(ptype))
  if not Base.aq_portal_type.has_key(ptype):
    # Mark as generated
    #prop_holder = Base.aq_portal_type[ptype] = PropertyHolder()
    prop_holder = PropertyHolder()
    # Recurse to parent object
    parent_object = self.aq_inner.aq_parent
    parent_klass = parent_object.__class__
    parent_type = parent_object.portal_type
    if getattr(parent_klass, 'isRADContent', 0) and \
       (ptype != parent_type or klass != parent_klass) and \
       not Base.aq_portal_type.has_key(parent_type):
      initializePortalTypeDynamicProperties(parent_object, parent_klass,
                                            parent_type)
    # Initiatise portal_type properties (XXX)
    ptype_object = getattr(aq_base(self.portal_types), ptype, None)
    cat_list = []
    prop_list = []
    constraint_list = []
    if (ptype_object is not None) and \
       (ptype_object.meta_type == 'ERP5 Type Information'):
      # Make sure this is an ERP5Type object
      ps_list = map(lambda p: getattr(PropertySheet, p, None),
                    ptype_object.property_sheet_list)
      ps_list = filter(lambda p: p is not None, ps_list)
      # Always append the klass.property_sheets to this list (for compatibility)
      # Because of the order we generate accessors, it is still possible
      # to overload data access for some accessors
      ps_list = tuple(ps_list) + getClassPropertyList(klass)
      #LOG('ps_list',0, str(ps_list))
    else:
      ps_list = getClassPropertyList(klass)
    for base in ps_list:
      property_sheet_definition_dict = {
        '_properties': prop_list,
        '_categories': cat_list,
        '_constraints': constraint_list
      }
      for ps_property_name, current_list in \
                                    property_sheet_definition_dict.items():
        if hasattr(base, ps_property_name):
          ps_property = getattr(base, ps_property_name)
          if isinstance(ps_property, (tuple, list)):
            current_list += ps_property
          else :
            raise ValueError, "%s is not a list for %s" % (ps_property_name,
                                                           base)

    if (ptype_object is not None) and \
       (ptype_object.meta_type == 'ERP5 Type Information'):
      cat_list += ptype_object.base_category_list
    prop_holder._properties = prop_list
    prop_holder._categories = cat_list
    prop_holder._constraints = constraint_list
    prop_holder.security = ClassSecurityInfo() # We create a new security info object
    from Utils import initializeDefaultProperties
    initializeDefaultProperties([prop_holder], object=self)
    #LOG('initializeDefaultProperties: %s' % ptype, 0, str(prop_holder.__dict__))
#     initializePortalTypeDynamicWorkflowMethods(self,
    initializePortalTypeDynamicWorkflowMethods(self, klass, prop_holder)
    # We can now associate it after initialising security
    InitializeClass(prop_holder)
    prop_holder.__propholder__ = prop_holder
    # For now, this line below is commented, because this breaks
    # _aq_dynamic without JP's patch to Zope for an unknown reason.
    #klass.__ac_permissions__ = prop_holder.__ac_permissions__
    Base.aq_portal_type[ptype] = prop_holder

def initializePortalTypeDynamicWorkflowMethods(self, klass, prop_holder):
  # We should now make sure workflow methods are defined
  # and also make sure simulation state is defined
  portal_workflow = getToolByName(self, 'portal_workflow')
#   LOG('getWorkflowsFor', 0,
#       str((self, [wf.id for wf in portal_workflow.getWorkflowsFor(self)])))
  for wf in portal_workflow.getWorkflowsFor(self):
#     LOG('in aq_portal_type %s' % id, 0,
#         "found state workflow %s" % wf.id)
    if wf.__class__.__name__ in ('DCWorkflowDefinition', ):
      wf_id = wf.id
      # Create state var accessor
      # and generate methods that support the translation of workflow states
      state_var = wf.variables.getStateVar()
      for method_id, getter in (
          ('get%s' % UpperCase(state_var), WorkflowState.Getter),
          ('get%sTitle' % UpperCase(state_var), WorkflowState.TitleGetter),
          ('getTranslated%s' % UpperCase(state_var),
                                     WorkflowState.TranslatedGetter),
          ('getTranslated%sTitle' % UpperCase(state_var),
                                     WorkflowState.TranslatedTitleGetter)):
        if not hasattr(prop_holder, method_id):
          method = getter(method_id, wf_id)
          # Attach to portal_type
          setattr(prop_holder, method_id, method)
          prop_holder.security.declareProtected(
                                 Permissions.AccessContentsInformation,
                                 method_id )
  for wf in portal_workflow.getWorkflowsFor(self):
    wf_id = wf.id
    if wf.__class__.__name__ in ('DCWorkflowDefinition', ):
      for tr_id in wf.transitions.objectIds():
        tdef = wf.transitions.get(tr_id, None)
        if tdef.trigger_type == TRIGGER_WORKFLOW_METHOD:
          method_id = convertToMixedCase(tr_id)
          # We have to make a difference between a method which is on
          # the prop_holder or on the klass, if the method is on the
          # klass, then the WorkflowMethod created also need to be on the klass
          if (not hasattr(prop_holder, method_id)) and \
             (not hasattr(klass, method_id)):
            method = WorkflowMethod(klass._doNothing, tr_id)
            # Attach to portal_type
            setattr(prop_holder, method_id, method)
            prop_holder.security.declareProtected(
                                     Permissions.AccessContentsInformation,
                                     method_id )
          else:
            # Wrap method into WorkflowMethod is needed
            try:
              method = getattr(klass, method_id)
            except AttributeError:
              method = getattr(prop_holder, method_id)
              work_method_holder = prop_holder
            else:
              work_method_holder = klass
            # Wrap method
            if callable(method):
              if not isinstance(method, WorkflowMethod):
                setattr(work_method_holder, method_id,
                        WorkflowMethod(method, method_id))
              else :
                # some methods (eg. set_ready) doesn't have the same name
                # (setReady) as the workflow transition (set_ready).
                # If they are associated with both an InteractionWorkflow
                # and a DCWorkflow, and the WorkflowMethod is created for
                # the InterractionWorkflow, then it may be associated with
                # a wrong transition name (setReady).
                # Here we force it's id to be the transition name (set_ready).
                method._setId(tr_id)
            else:
              LOG('initializePortalTypeDynamicWorkflowMethods', 100,
                  'WARNING! Can not initialize %s on %s' % \
                    (method_id, str(work_method_holder)))
    # XXX This part is (more or less...) a copy and paste
    elif wf.__class__.__name__ in ('InteractionWorkflowDefinition', ):
      for tr_id in wf.interactions.objectIds():
        tdef = wf.interactions.get(tr_id, None)
        if tdef.trigger_type == TRIGGER_WORKFLOW_METHOD:
          for imethod_id in tdef.method_id:
            method_id = imethod_id
            if (not hasattr(prop_holder, method_id)) and \
               (not hasattr(klass,method_id)):
              method = WorkflowMethod(klass._doNothing, imethod_id)
              # Attach to portal_type
              setattr(prop_holder, method_id, method)
              prop_holder.security.declareProtected(
                                      Permissions.AccessContentsInformation,
                                      method_id)
            else:
              # Wrap method into WorkflowMethod is needed
              if getattr(klass,method_id,None) is not None:
                method = getattr(klass, method_id)
                if callable(method):
                  if not isinstance(method, WorkflowMethod):
                    method = WorkflowMethod(method, method_id)
                    setattr(klass, method_id, method)
              else:
                method = getattr(prop_holder, method_id)
                if callable(method):
                  if not isinstance(method, WorkflowMethod):
                    method = WorkflowMethod(method, method_id)
                    setattr(prop_holder, method_id, method)


class Base( CopyContainer, PortalContent, ActiveObject, ERP5PropertyManager ):
  """
    This is the base class for all ERP5 Zope objects.
    It defines object attributes which are necessary to implement
    relations and data synchronisation

    id  --  the standard object id
    rid --  the standard object id in the master ODB the object was
        subsribed from
    uid --  a global object id which is unique to each ZODB
    sid --  the id of the subscribtion/syncrhonisation object which
        this object was generated from

    sync_status -- The status of this document in the synchronization
             process (NONE, SENT, ACKNOWLEDGED, SYNCHRONIZED)
             could work as a workflow but CPU expensive


    TODO:

      - assess / fix atomicity

      - assess / fix uid during synchronisation / import
  """
  meta_type = 'ERP5 Base Object'
  portal_type = 'Base Object'
  #_local_properties = () # no need since getattr
  isPortalContent = 1 # All those attributes should become a methods
  isRADContent = 1    #
  isCapacity = 0      #
  isCategory = 0      #
  isBaseCategory = 0  #
  isMovement = 0      #
  isDelivery = 0      #
  isIndexable = 1     # If set to 0, reindexing will not happen (useful for optimization)
  isPredicate = 0     #
  isTemplate = 0      #

  # Dynamic method acquisition system (code generation)
  aq_method_generated = {}
  aq_portal_type = {}
  aq_related_generated = 0

  aq_preference_generated = 0
  # FIXME: Preference should not be included in ERP5Type

  # Declarative security
  security = ClassSecurityInfo()

  # Declarative properties
  property_sheets = ( PropertySheet.Base, )

  # We want to use a default property view
  manage_propertiesForm = DTMLFile( 'dtml/properties', _dtmldir )

  security.declareProtected( Permissions.ModifyPortalContent, 'setTitle' )
  def setTitle(self, value):
    """ sets the title. (and then reindexObject)"""
    self._setTitle(value)
    self.reindexObject()

  security.declareProtected( Permissions.AccessContentsInformation, 'test_dyn' )
  def test_dyn(self):
    """
    """
    initializeClassDynamicProperties(self, self.__class__)

  def _propertyMap(self):
    """ Method overload - properties are now defined on the ptype """
    ptype = self.portal_type
    #LOG('_propertyMap',0,ptype)
    self._aq_dynamic('id') # Make sure aq_dynamic has been called once
    if Base.aq_portal_type.has_key(ptype):
      #LOG('_propertyMap ptype',0,list(getattr(aq_portal_type[ptype], '_properties', ())))
      return tuple(list(getattr(Base.aq_portal_type[ptype], '_properties', ())) +
                   list(getattr(self, '_local_properties', ())))
    return ERP5PropertyManager._propertyMap(self)

  def _aq_dynamic_pmethod(self, id):
    ptype = self.portal_type

    #LOG("In _aq_dynamic_pmethod", 0, str((id, ptype, self)))

    if Base.aq_portal_type.has_key(ptype):
      return getattr(Base.aq_portal_type[ptype], id, None).__of__(self)

    return None

  def _aq_dynamic(self, id):
    ptype = self.portal_type

    #LOG('_aq_dynamic', 0, 'self = %r, id = %r, ptype = %r' % (self, id, ptype))
    #LOG("In _aq_dynamic", 0, str((id, ptype, self)))

    # If this is a portal_type property and everything is already defined
    # for that portal_type, try to return a value ASAP
    if Base.aq_portal_type.has_key(ptype):
      accessor = getattr(Base.aq_portal_type[ptype], id, None)
      #LOG('_aq_dynamic', 0, 'self = %r, id = %r, accessor = %r' % (self, id, accessor))
      if accessor is not None:
        # Clearly this below has a bad effect in CMFCategory.
        # Someone must investigate why. -yo
        #return accessor.__of__(self) # XXX - JPS: I have no idea if we should __of__ before returning
        return accessor
      return None
    elif id in ('portal_types', 'portal_url', 'portal_workflow'):
      # This is required to precent infinite loop (we need to access portal_types tool)
      return None

    # Proceed with property generation
    klass = self.__class__
    generated = 0 # Prevent infinite loops

    # Generate class methods
    if not Base.aq_method_generated.has_key(klass):
      initializeClassDynamicProperties(self, klass)
      generated = 1

    # Generate portal_type methods
    if not Base.aq_portal_type.has_key(ptype):
      initializePortalTypeDynamicProperties(self, klass, ptype)
      generated = 1

    # Generate Related Accessors
    if not Base.aq_related_generated:
      from Utils import createRelatedValueAccessors
      generated = 1
      portal_types = getToolByName(self, 'portal_types', None)
      generated_bid = {}
      econtext = createExpressionContext(self.getPortalObject())
      for pid, ps in PropertySheet.__dict__.items():
        if pid[0] != '_':
          base_category_list = []
          for cat in getattr(ps, '_categories', ()):
            if isinstance(cat, Expression):
              result = cat(econtext)
              if isinstance(result, (list, tuple)):
                base_category_list.extend(result)
              else:
                base_category_list.append(result)
            else:
              base_category_list.append(cat)
          for bid in base_category_list:
            if bid not in generated_bid:
              #LOG( "Create createRelatedValueAccessors %s" % bid,0,'')
              createRelatedValueAccessors(Base, bid)
              generated_bid[bid] = 1
      for ptype in portal_types.objectValues('ERP5 Type Information') :
        for bid in ptype.base_category_list :
          if bid not in generated_bid :
            createRelatedValueAccessors(Base, bid)
            generated_bid[bid] = 1

      Base.aq_related_generated = 1

    if not Base.aq_preference_generated:
      try :
        from Products.ERP5Form.PreferenceTool import createPreferenceMethods
        createPreferenceMethods(self.getPortalObject())
      except ImportError, e :
        LOG('Base._aq_dynamic', WARNING,
            'unable to create methods for PreferenceTool', e)
        raise
      Base.aq_preference_generated = 1

    # Always try to return something after generation
    if generated:
      # We suppose that if we reach this point
      # then it means that all code generation has succeeded
      # (no except should hide that). We can safely return None
      # if id does not exist as a dynamic property
      # Baseline: accessor generation failures should always
      #           raise an exception up to the user
      #LOG('_aq_dynamic', 0, 'getattr self = %r, id = %r' % (self, id))
      return getattr(self, id, None)

    # Proceed with standard acquisition
    #LOG('_aq_dynamic', 0, 'not generated; return None for id = %r, self = %r' % (id, self))
    return None

  psyco.bind(_aq_dynamic)


  # Constructor
  def __init__(self, id, uid=None, rid=None, sid=None, **kw):
    self.id = id
    if uid is not None :
      self.uid = uid # Else it will be generated when we need it
    self.sid = sid

  # XXX This is necessary to override getId which is also defined in SimpleItem.
  security.declareProtected( Permissions.AccessContentsInformation, 'getId' )
  for prop in PropertySheet.Base._properties:
    if prop['id'] == 'id':
      getId = BaseAccessor.Getter('getId', 'id', prop['type'],
                                  default = prop.get('default'), storage_id = prop.get('storage_id'))
      break

  # Debug
  def getOid(self):
    """
      Return ODB oid
    """
    return self._p_oid

  def getOidRepr(self):
    """
      Return ODB oid, in an 'human' readable form.
    """
    from ZODB.utils import oid_repr
    return oid_repr(self._p_oid)

  # Utils
  def _getCategoryTool(self):
    return aq_inner(self.getPortalObject().portal_categories)

  def _getTypesTool(self):
    return aq_inner(self.getPortalObject().portal_types)

  def _doNothing(self, *args, **kw):
    # A method which does nothing (and can be used to build WorkflowMethods which trigger worklow transitions)
    pass

  # Generic accessor
  def _getDefaultAcquiredProperty(self, key, default_value, null_value,
        base_category=None, portal_type=None, copy_value=0, mask_value=0, sync_value=0,
        accessor_id=None, depends=None, storage_id=None, alt_accessor_id=None,
        is_list_type=0, is_tales_type=0):
    """
      This method implements programmable acquisition of values in ERP5.

      The principle is that some object attributes should be looked up,
      copied or synchronized from the values of another object which relates
      to the first thereof.

      The parameters which define value acquisition are:

      base_category --    a single base category or a list of base categories
                          to look up related objects

      portal_type   --    a single portal type or a list of portal types to filter the
                          list of related objects

      copy_value    --    if set to 1, the looked up value will be copied
                          as an attribute of self

      mask_value    --    if set to 1, the value of the attribute of self
                          has priority on the looked up value

      sync_value    --    if set to 1, keep self and looked up value in sync

      accessor_id   --    the id of the accessor to call on the related filtered objects

      depends       --    a list of parameters to propagate in the look up process

      The purpose of copy_value / mask_value / sync_value is to solve issues
      related to relations and synchronisation of data. copy_value determines
      if a value should be copied as an attribute of self. Copying a value is
      useful for example when we do invoices and want to remember the price at
      a given point of time. mask_value allows to give priority to the value
      holded by self, rather than to the lookup through related objects.
      This is for example useful for invoices (again) for which we want the value
      not to change in time.

      Another case is the case of independent modules on multiple Zope. If for example
      a sales opportunity modules runs on a Zope No1 and an Organisation module runs
      on a Zope No 2. We want to enter peoples's names on the Zope No1. They will be entered
      as strings and stored as such in attributes. When such opportunities are synchronized
      on the Zope No 2, we want to be able to augment content locally by adding some
      category information (in order to say for example that M. Lawno is client/person/23)
      and eventually want M. Lawno to be displayed as "James Lawno". So, we want to give
      priority to the looked up attribute rather than to the attribute. However,
      we may want Zope No 1 to still display "James Lawno" as "M. Lawno". This means
      that we do not want to synchronize back this attribute.

      Other case : we add relation after entering information...

      Other case : we want to change the phone number of a related object without
      going to edit the related object

    """
    # Push context to prevent loop
    # We use TRANSACTION but should use REQUEST
    from Globals import get_request
    TRANSACTION = get_transaction()
    if not hasattr(TRANSACTION, '_erp5_acquisition_stack'): TRANSACTION._erp5_acquisition_stack = {}
    if isinstance(portal_type, list):
      portal_type = tuple(portal_type)
    acquisition_key = ('_getDefaultAcquiredProperty', self.getPath(), key, base_category,
                       portal_type, copy_value, mask_value, sync_value,
                       accessor_id, depends, storage_id, alt_accessor_id, is_list_type, is_tales_type)
    if TRANSACTION._erp5_acquisition_stack.has_key(acquisition_key): return null_value
    TRANSACTION._erp5_acquisition_stack[acquisition_key] = 1

    if storage_id is None: storage_id=key
    #LOG("Get Acquired Property storage_id",0,str(storage_id))
    # If we hold an attribute and mask_value is set, return the attribute
    value = getattr(self, storage_id, None)
    if mask_value and value is not None:
      # Pop context
      del TRANSACTION._erp5_acquisition_stack[acquisition_key]
      if is_tales_type:
        expression = Expression(value)
        econtext = createExpressionContext(self)
        return expression(econtext)
      else:
        return value
    # Retrieve the list of related objects
    #LOG("Get Acquired Property self",0,str(self))
    #LOG("Get Acquired Property portal_type",0,str(portal_type))
    #LOG("Get Acquired Property base_category",0,str(base_category))
    #super_list = self._getValueList(base_category, portal_type=portal_type) # We only do a single jump
    super_list = self._getAcquiredValueList(base_category, portal_type=portal_type) # Full acquisition
    super_list = filter(lambda o: o.getPhysicalPath() != self.getPhysicalPath(), super_list) # Make sure we do not create stupid loop here
    #LOG("Get Acquired Property super_list",0,str(super_list))
    #LOG("Get Acquired Property accessor_id",0,str(accessor_id))
    if len(super_list) > 0:
      super = super_list[0]
      # Retrieve the value
      if accessor_id is None:
        value = super.getProperty(key)
      else:
        method = getattr(super, accessor_id)
        value = method() # We should add depends here XXXXXX
                         # There is also a strong risk here of infinite loop
      if copy_value:
        if getattr(self, storage_id, None) is None:
          # Copy the value if it does not already exist as an attribute of self
          # Like in the case of orders / invoices
          setattr(self, storage_id, value)
      if is_list_type:
        # We must provide the first element of the acquired list
        if value is None:
          result = None
        else:
          if isinstance(value, (list, tuple)):
            if len(value) is 0:
              result = None
            else:
              result = value[0]
          else:
            result = value
      else:
        # Value is a simple type
        result = value
    else:
      result = None
    if result is not None:
      # Pop context
      del TRANSACTION._erp5_acquisition_stack[acquisition_key]
      return result
    else:
      #LOG("alt_accessor_id",0,str(alt_accessor_id))
      if alt_accessor_id is not None:
        for id in alt_accessor_id:
          #LOG("method",0,str(id))
          method = getattr(self, id, None)
          if callable(method):
            result = method()
            if result is not None:
              if is_list_type:
                if isinstance(result, (list, tuple)):
                  # We must provide the first element of the alternate result
                  if len(result) > 0:
                    # Pop context
                    del TRANSACTION._erp5_acquisition_stack[acquisition_key]
                    return result[0]
                else:
                  # Pop context
                  del TRANSACTION._erp5_acquisition_stack[acquisition_key]
                  return result
              else:
                # Pop context
                del TRANSACTION._erp5_acquisition_stack[acquisition_key]
                # Result is a simple type
                return result

      if copy_value:
        # Pop context
        del TRANSACTION._erp5_acquisition_stack[acquisition_key]
        return getattr(self,storage_id, default_value)
      else:
        # Pop context
        del TRANSACTION._erp5_acquisition_stack[acquisition_key]
        # Return the default value defined at the class level XXXXXXXXXXXXXXX
        return default_value

  def _getAcquiredPropertyList(self, key, default_value, null_value,
     base_category, portal_type=None, copy_value=0, mask_value=0, sync_value=0, append_value=0,
     accessor_id=None, depends=None, storage_id=None, alt_accessor_id=None,
     is_list_type=0, is_tales_type=0):
    """
      Default accessor. Implements the default
      attribute accessor.

      portal_type
      copy_value
      depends

    """
    # Push context to prevent loop
    from Globals import get_request
    TRANSACTION = get_transaction()
    if not hasattr(TRANSACTION, '_erp5_acquisition_stack'): TRANSACTION._erp5_acquisition_stack = {}
    acquisition_key = ('_getAcquiredPropertyList', self.getPath(), key, base_category,
                       portal_type, copy_value, mask_value, sync_value,
                       accessor_id, depends, storage_id, alt_accessor_id, is_list_type, is_tales_type)
    if TRANSACTION._erp5_acquisition_stack.has_key(acquisition_key): return null_value
    TRANSACTION._erp5_acquisition_stack[acquisition_key] = 1

    if storage_id is None: storage_id=key
    value = getattr(self, storage_id, None)
    if mask_value and value is not None:
      # Pop context
      del TRANSACTION._erp5_acquisition_stack[acquisition_key]
      if is_tales_type:
        expression = Expression(value)
        econtext = createExpressionContext(self)
        return expression(econtext)
      else:
        return value
    super_list = self._getAcquiredValueList(base_category, portal_type=portal_type) # Full acquisition
    super_list = filter(lambda o: o.getPhysicalPath() != self.getPhysicalPath(), super_list) # Make sure we do not create stupid loop here
    if len(super_list) > 0:
      value = []
      for super in super_list:
        if accessor_id is None:
          if is_list_type:
            result = super.getPropertyList(key)
            if isinstance(result, (list, tuple)):
              value += result
            else:
              value += [result]
          else:
            value += [super.getProperty(key)]
        else:
          method = getattr(super, accessor_id)
          if is_list_type:
            result = method() # We should add depends here
            if isinstance(result, (list, tuple)):
              value += result
            else:
              value += [result]
          else:
            value += [method()] # We should add depends here
      if copy_value:
        if not hasattr(self, storage_id):
          setattr(self, value)
      # Pop context
      del TRANSACTION._erp5_acquisition_stack[acquisition_key]
      return value
    else:
      # ?????
      if copy_value:
        # Pop context
        del TRANSACTION._erp5_acquisition_stack[acquisition_key]
        return getattr(self,storage_id, default_value)
      else:
        # Pop context
        del TRANSACTION._erp5_acquisition_stack[acquisition_key]
        return default_value

  security.declareProtected( Permissions.AccessContentsInformation, 'getProperty' )
  def getProperty(self, key, d=None, **kw):
    """
      Previous Name: getValue

      Generic accessor. Calls the real accessor
    """
    accessor_name = 'get' + UpperCase(key)
    aq_self = aq_base(self)
    if hasattr(aq_self, accessor_name):
      method = getattr(self, accessor_name)
      return method(**kw)
    # Try to get a portal_type property (Implementation Dependent)
    if not Base.aq_portal_type.has_key(self.portal_type):
      try:
        self._aq_dynamic(accessor_name)
      except AttributeError:
        pass
    if hasattr(Base.aq_portal_type[self.portal_type], accessor_name):
      method = getattr(self, accessor_name)
      return method(**kw)
    else:
      return ERP5PropertyManager.getProperty(self, key, d=d, **kw)

  security.declareProtected( Permissions.AccessContentsInformation, 'getPropertyList' )
  def getPropertyList(self, key, d=None):
    """
      Previous Name: getValue

      Generic accessor. Calls the real accessor
    """
    return self.getProperty('%s_list' % key)

  security.declareProtected( Permissions.ModifyPortalContent, 'setProperty' )
  def setProperty(self, key, value, type='string', **kw):
    """
      Previous Name: setValue

      New Name: we use the naming convention of
      /usr/lib/zope/lib/python/OFS/PropertySheets.py

      TODO: check possible conflicts

      Generic accessor. Calls the real accessor
    """
    self._setProperty(key,value, type=type, **kw)
    self.reindexObject()

  security.declareProtected( Permissions.ModifyPortalContent, '_setProperty' )
  def _setProperty(self, key, value, type='string', **kw):
    """
      Previous Name: _setValue

      Generic accessor. Calls the real accessor

      **kw allows to call setProperty as a generic setter (ex. setProperty(value_uid, portal_type=))
    """
    if type is not 'string': # Speed
      if type in list_types: # Patch for OFS PropertyManager
        key += '_list'
    accessor_name = '_set' + UpperCase(key)
    aq_self = aq_base(self)
    # We must use aq_self
    # since we will change the value on self
    # rather than through implicit aquisition
    if hasattr(aq_self, accessor_name):
      method = getattr(self, accessor_name)
      method(value, **kw)
      return
    public_accessor_name = 'set' + UpperCase(key)
    if hasattr(aq_self, public_accessor_name):
      method = getattr(self, public_accessor_name)
      method(value, **kw)
      return
    # Try to get a portal_type property (Implementation Dependent)
    if not Base.aq_portal_type.has_key(self.portal_type):
      self._aq_dynamic('id') # Make sure _aq_dynamic has been called once
    if hasattr(Base.aq_portal_type[self.portal_type], accessor_name):
      method = getattr(self, accessor_name)
      method(value, **kw)
      return
    if hasattr(Base.aq_portal_type[self.portal_type], public_accessor_name):
      method = getattr(self, public_accessor_name)
      method(value, **kw)
      return
    # Finaly use standard PropertyManager
    #LOG("Changing attr: ",0, key)
    try:
      ERP5PropertyManager._setProperty(self, key, value, type=type)
    except ConflictError:
      raise
    except:
      # This should be removed if we want strict property checking
      setattr(self, key, value)

  def _setPropValue(self, key, value, **kw):
    #LOG('_setPropValue', 0, 'self = %r, key = %r, value = %r, kw = %r' % (self, key, value, kw))
    self._wrapperCheck(value)
    if isinstance(value, list):
      value = tuple(value)
    accessor_name = '_set' + UpperCase(key)
    aq_self = aq_base(self)
    # We must use aq_self
    # since we will change the value on self
    # rather than through implicit aquisition
    if hasattr(aq_self, accessor_name):
      method = getattr(self, accessor_name)
      method(value, **kw)
      return
    public_accessor_name = 'set' + UpperCase(key)
    if hasattr(aq_self, public_accessor_name):
      method = getattr(self, public_accessor_name)
      method(value, **kw)
      return
    # Try to get a portal_type property (Implementation Dependent)
    if not Base.aq_portal_type.has_key(self.portal_type):
      self._aq_dynamic('id') # Make sure _aq_dynamic has been called once
    if hasattr(Base.aq_portal_type[self.portal_type], accessor_name):
      method = getattr(self, accessor_name)
      method(value, **kw)
      return
    if hasattr(Base.aq_portal_type[self.portal_type], public_accessor_name):
      method = getattr(self, public_accessor_name)
      method(value, **kw)
      return
    # Finaly use standard PropertyManager
    #LOG("Changing attr: ",0, key)
    try:
      ERP5PropertyManager._setPropValue(self, key, value)
    except ConflictError:
      raise
    except:
      # This should be removed if we want strict property checking
      setattr(self, key, value)

  security.declareProtected( Permissions.View, 'hasProperty' )
  def hasProperty(self, key):
    """
      Previous Name: hasValue

      Generic accessor. Calls the real accessor
      and returns 0 if it fails
    """
    accessor_name = 'has' + UpperCase(key)
    if hasattr(self, accessor_name):
      method = getattr(self, accessor_name)
      try:
        return method()
      except ConflictError:
        raise
      except:
        return 0
    else:
      for p_id in self.propertyIds():
        if key==p_id:
          return 1
      return 0

  security.declareProtected( Permissions.View, 'hasCategory' )
  def hasCategory(self, key):
    """
      Previous Name: hasValue

      Generic accessor. Calls the real accessor
      and returns 0 if it fails
    """
    return key in self.getCategoryList()

  # Accessors are not workflow methods by default
  # Ping provides a dummy method to trigger automatic methods
  # XXX : maybe an empty edit is enough (self.edit())
  def ping(self):
    pass

  ping = WorkflowMethod( ping )

  # Object attributes update method
  security.declarePrivate( '_edit' )
  def _edit(self, REQUEST=None, force_update=0, reindex_object=0, **kw):
    """
      Generic edit Method for all ERP5 object
      The purpose of this method is to update attributed, eventually do
      some kind of type checking according to the property sheet and index
      the object.

      Each time attributes of an object are updated, they should
      be updated through this generic edit method
    """
    self._v_modified_property_dict = {}
    for key in kw.keys():
      if key != 'id':
        # We only change if the value is different
        # This may be very long...
        old_value = None
        if not force_update:
          try:
            old_value = self.getProperty(key, evaluate=0)
          except TypeError:
            old_value = self.getProperty(key)


        if old_value != kw[key] or force_update:
          # We keep in a thread var the previous values
          # this can be useful for interaction workflow to implement lookups
          self._v_modified_property_dict[key] = old_value
          self._setProperty(key, kw[key])
      elif self.id != kw['id']:
        self.setId(kw['id'], reindex=reindex_object)
    # Modification date is supported by edit_workflow in ERP5
    # There is no need to change it here
    if reindex_object:
      # We do not want to reindex the object if nothing is changed
      if (self._v_modified_property_dict != {}):
        self.reindexObject()

  security.declareProtected( Permissions.ModifyPortalContent, 'setId' )
  def setId(self, id, reindex = 1):
    """
        changes id of an object by calling the Zope machine
    """
    # Do not rename until everything flushed
    self.recursiveFlushActivity(invoke=1)
    tryMethodCallWithTemporaryPermission(self, 'Copy or Move',
        self.aq_inner.aq_parent.manage_renameObject, (self.id, id), {}, CopyError)
    if reindex:
      # Required if we wish that news ids appear instantly
      self.flushActivity(invoke=1)

  security.declareProtected( Permissions.ModifyPortalContent,
                             'updateRelatedContent' )
  def updateRelatedContent(self, previous_category_url, new_category_url):
    """
        updateRelatedContent is implemented by portal_categories
    """
    self._getCategoryTool().updateRelatedContent(self,
                                previous_category_url, new_category_url)

  security.declareProtected(Permissions.ModifyPortalContent, 'edit')
  def edit(self, REQUEST=None, force_update=0, reindex_object=1, **kw):
    """
      Generic edit Method for all ERP5 object
    """
    return self._edit(REQUEST=REQUEST, force_update=force_update,
                      reindex_object=reindex_object, **kw)

  # XXX Is this useful ? (Romain)
  edit = WorkflowMethod(edit)

  # Accessing object property through ERP5ish interface
  security.declareProtected( Permissions.View, 'getPropertyIdList' )
  def getPropertyIdList(self):
    return self.propertyIds()

  security.declareProtected( Permissions.View, 'getPropertyValueList' )
  def getPropertyValueList(self):
    return self.propertyValues()

  security.declareProtected( Permissions.View, 'getPropertyItemList' )
  def getPropertyItemList(self):
    return self.propertyItems()

  security.declareProtected( Permissions.View, 'getPropertyMap' )
  def getPropertyMap(self):
    return self.propertyMap()

  # Catalog Related
  security.declareProtected( Permissions.View, 'getObject' )
  def getObject(self, relative_url = None, REQUEST=None):
    """
      Returns self - useful for ListBox when we do not know
      if the getObject is called on a brain object or on the actual object
    """
    return self

  def getDocumentInstance(self):
    """
      Returns self
      Returns instance if category through document_instance relation
    """
    return self

  def asSqlExpression(self, strict_membership=0, table='category', base_category = None):
    """
      Any document can be used as a Category. It can therefore
      serve in a Predicate and must be rendered as an sql expression. This
      can be useful to create reporting trees based on the
      ZSQLCatalog whenever documents are used rather than categories

      TODO:
        - strict_membership is not implemented
    """
    if isinstance(base_category, str):
      base_category = self.portal_categories[base_category]
    if base_category is None:
      sql_text = '(%s.category_uid = %s)' % \
          (table, self.getUid())
    else:
      sql_text = '(%s.category_uid = %s AND %s.base_category_uid = %s)' % \
          (table, self.getUid(), table, base_category.getBaseCategoryUid())
    return sql_text

  security.declareProtected( Permissions.AccessContentsInformation,
                             'getParentSqlExpression' )
  def getParentSqlExpression(self, table = 'catalog', strict_membership = 0):
    """
      Builds an SQL expression to search children and subclidren
    """
    return "%s.parent_uid = %s" % (table, self.getUid())

  security.declareProtected( Permissions.AccessContentsInformation,
                             'getParentUid' )
  def getParentUid(self):
    """
      Returns the UID of the parent of the current object. Used
      for the implementation of the ZSQLCatalog based listing
      of objects.
    """
    parent = self.aq_inner.aq_parent
    uid = getattr(aq_base(parent), 'uid', None)
    if uid is None:
      parent.immediateReindexObject() # Required with deferred indexing
      uid = getattr(aq_base(parent), 'uid', None)
      if uid is None:
        LOG('Failed twice getParentUid', 0, str((self.getPhysicalPath(),parent.getPhysicalPath())))
        raise DeferredCatalogError('Could neither access parent uid nor generate it', self)
    return uid

  security.declareProtected( Permissions.AccessContentsInformation,
                             'getParentTitleOrId' )
  def getParentTitleOrId(self):
    """
      Returns the title or the id of the parent
    """
    return self.aq_inner.aq_parent.getTitleOrId()

  security.declareProtected( Permissions.AccessContentsInformation,
                             'getParentRelativeUrl' )
  def getParentRelativeUrl(self):
    """
      Returns the title or the id of the parent
    """
    return self.aq_inner.aq_parent.getRelativeUrl()

  security.declareProtected( Permissions.AccessContentsInformation,
                             'getParentId' )
  def getParentId(self):
    """
      Returns the id of the parent
    """
    return self.aq_inner.aq_parent.getId()

  security.declareProtected( Permissions.AccessContentsInformation,
                             'getParentTitle' )
  def getParentTitle(self):
    """
      Returns the title or of the parent
    """
    return self.aq_inner.aq_parent.getTitle()

  security.declareProtected( Permissions.AccessContentsInformation,
                             'getParentValue' )
  def getParentValue(self):
    """
      Returns the parent of the current object.
    """
    return self.aq_inner.aq_parent

  security.declareProtected( Permissions.AccessContentsInformation, 'getParent' )
  def getParent(self):
    """Returns the parent of the current object (whereas it should return the
    relative_url of the parent for consistency with CMFCategory.

    This method still uses this behaviour, because some part of the code still
    uses getParent instead of getParentValue. This may change in the future.
    """
    warnings.warn("getParent implementation still returns the parent object, "\
                  "which is inconsistant with CMFCategory API. "\
                  "Use getParentValue instead", FutureWarning)
    return self.getParentValue() # Compatibility

  security.declareProtected( Permissions.AccessContentsInformation, 'getUid' )
  def getUid(self):
    """
      Returns the UID of the object. Eventually reindexes
      the object in order to make sure there is a UID
      (useful for import / export).

      WARNING : must be updated for circular references issues
    """
    uid = getattr(aq_base(self), 'uid', None)
    if uid is None:
      self.uid = self.portal_catalog.newUid()
      uid = getattr(aq_base(self), 'uid', None)
      if uid is None:
        raise DeferredCatalogError('Could neither access uid nor generate it', self)
    return uid

  security.declareProtected(Permissions.AccessContentsInformation, 'getLogicalPath')
  def getLogicalPath(self, REQUEST=None) :
    """
      Returns the absolute path of an object, using titles when available
    """
    pathlist = self.getPhysicalPath()
    objectlist = [self.getPhysicalRoot()]
    for element in pathlist[1:] :
      objectlist.append(objectlist[-1][element])
    return '/' + join([object.getTitle() for object in objectlist[1:]], '/')

  security.declareProtected(Permissions.AccessContentsInformation, 'getPath')
  def getPath(self, REQUEST=None):
    """
      Returns the absolute path of an object
    """
    return join(self.getPhysicalPath(),'/')

  # This should be the new name
  security.declareProtected(Permissions.AccessContentsInformation, 'getUrl')
  getUrl = getPath

  security.declareProtected(Permissions.AccessContentsInformation, 'getRelativeUrl')
  def getRelativeUrl(self):
    """
      Returns the absolute path of an object
    """
    return self.portal_url.getRelativeUrl(self)

  security.declareProtected(Permissions.AccessContentsInformation, 'getPortalObject')
  def getPortalObject(self):
    """
      Returns the portal object
    """
    cache = getReadOnlyTransactionCache(self)
    if cache is not None:
      key = 'getPortalObject'
      try:
        return cache[key]
      except KeyError:
        pass

    result = self.portal_url.getPortalObject()

    if cache is not None:
      cache[key] = result

    return result

  security.declareProtected(Permissions.AccessContentsInformation, 'getWorkflowIds')
  def getWorkflowIds(self):
    """
      Returns the list of workflows
    """
    return self.portal_workflow.getWorkflowIds()

  # Object Database Management
  security.declareProtected( Permissions.ManagePortal, 'upgrade' )
  def upgrade(self, REQUEST=None):
    """
      Upgrade an object and do whatever necessary
      to make sure it is compatible with the latest
      version of a class
    """
    pass

  # For Debugging
  security.declareProtected( Permissions.ManagePortal, 'showDict' )
  def showDict(self):
    """
      Returns the dictionnary of the object
      Only for debugging
    """
    return self.__dict__

  security.declareProtected( Permissions.ManagePortal, 'showPermissions' )
  def showPermissions(self, all=1):
    """
      Return the tuple of permissions
      Only for debugging
    """
    permission_list = []
    for permission in self.ac_inherited_permissions(all=all):
      name, value = permission[:2]
      role_list = Permission(name, value, self).getRoles(default=[])
      permission_list.append((name, role_list))

    return tuple(permission_list)

  # Private accessors for the implementation of relations based on
  # categories
  security.declareProtected( Permissions.ModifyPortalContent, '_setValue' )
  def _setValue(self, id, target, spec=(), filter=None, portal_type=()):
    if target is None :
      path = target
    elif isinstance(target, str):
      # We have been provided a string
      path = target
    elif isinstance(target, (tuple, list)):
      # We have been provided a list or tuple
      path_list = []
      for target_item in target:
        if isinstance(target_item, str):
          path_list += [target_item]
        else:
          path = target_item.getRelativeUrl()
          path_list += [path]
      path = path_list
    else:
      # We have been provided an object
      # Find the object
      path = target.getRelativeUrl()
    self._setCategoryMembership(id, path, spec=spec, filter=filter, portal_type=portal_type)

  security.declareProtected( Permissions.ModifyPortalContent, '_setDefaultValue' )
  _setDefaultValue = _setValue

  security.declareProtected( Permissions.ModifyPortalContent, '_setValueList' )
  _setValueList = _setValue

  security.declareProtected( Permissions.ModifyPortalContent, 'setValue' )
  def setValue(self, id, target, spec=(), filter=None, portal_type=()):
    self._setValue(id, target, spec=spec, filter=filter, portal_type=portal_type)
    self.reindexObject()

  security.declareProtected( Permissions.ModifyPortalContent, 'setDefaultValue' )
  setDefaultValue = setValue

  security.declareProtected( Permissions.ModifyPortalContent, 'setValueList' )
  setValueList = setValue

  security.declareProtected( Permissions.View, '_getDefaultValue' )
  def _getDefaultValue(self, id, spec=(), filter=None, portal_type=()):
    path = self._getDefaultCategoryMembership(id, spec=spec, filter=filter,
                                      portal_type=portal_type,base=1)
    if path is None:
      return None
    else:
      return self._getCategoryTool().resolveCategory(path)

  security.declareProtected( Permissions.View, 'getDefaultValue' )
  getDefaultValue = _getDefaultValue

  security.declareProtected( Permissions.View, '_getValueList' )
  def _getValueList(self, id, spec=(), filter=None, portal_type=()):
    ref_list = []
    for path in self._getCategoryMembershipList(id, spec=spec, filter=filter,
                                                  portal_type=portal_type, base=1):
      # LOG('_getValueList',0,str(path))
      try:
        value = self._getCategoryTool().resolveCategory(path)
        if value is not None: ref_list.append(value)
      except ConflictError:
        raise
      except:
        LOG("ERP5Type WARNING",0,"category %s has no object value" % path, error=sys.exc_info())
    return ref_list

  security.declareProtected( Permissions.View, 'getValueList' )
  getValueList = _getValueList

  security.declareProtected( Permissions.View, '_getDefaultAcquiredValue' )
  def _getDefaultAcquiredValue(self, id, spec=(), filter=None, portal_type=(),
                               evaluate=1):
    path = self._getDefaultAcquiredCategoryMembership(id, spec=spec, filter=filter,
                                                  portal_type=portal_type, base=1)
    # LOG("_getAcquiredDefaultValue",0,str(path))
    if path is None:
      return None
    else:
      return self._getCategoryTool().resolveCategory(path)

  security.declareProtected( Permissions.View, 'getDefaultAcquiredValue' )
  getDefaultAcquiredValue = _getDefaultAcquiredValue

  security.declareProtected( Permissions.View, '_getAcquiredValueList' )
  def _getAcquiredValueList(self, id, spec=(), filter=None, **kw):
    ref_list = []
    for path in self._getAcquiredCategoryMembershipList(id, base=1,
                                                spec=spec,  filter=filter, **kw):
      try:
        value = self._getCategoryTool().resolveCategory(path)
        if value is not None: ref_list.append(value)
      except ConflictError:
        raise
      except:
        LOG("ERP5Type WARNING",0,"category %s has no object value" % path, error=sys.exc_info())
    return ref_list

  security.declareProtected( Permissions.View, 'getAcquiredValueList' )
  getAcquiredValueList = _getAcquiredValueList

  security.declareProtected( Permissions.View, '_getDefaultRelatedValue' )
  def _getDefaultRelatedValue(self, id, spec=(), filter=None, portal_type=(),
                              strict_membership=0, strict="deprecated"):
    # backward compatibility to keep strict keyword working
    if strict != "deprecated" : strict_membership = strict
    value_list =self._getRelatedValueList(id, spec=spec, filter=filter,
                                portal_type=portal_type,
                                strict_membership=strict_membership)
    try:
      return value_list[0]
    except IndexError:
      return None

  security.declareProtected( Permissions.View, 'getDefaultRelatedValue' )
  getDefaultRelatedValue = _getDefaultRelatedValue

  security.declareProtected( Permissions.View, '_getRelatedValueList' )
  def _getRelatedValueList(self, id, spec=(), filter=None, portal_type=(),
                           strict_membership=0, strict="deprecated"):
    # backward compatibility to keep strict keyword working
    if strict != "deprecated" : strict_membership = strict
    return self._getCategoryTool().getRelatedValueList(self, id,
                          spec=spec, filter=filter, portal_type=portal_type,
                          strict_membership=strict_membership)

  security.declareProtected( Permissions.View, 'getRelatedValueList' )
  getRelatedValueList = _getRelatedValueList

  security.declareProtected( Permissions.AccessContentsInformation,
                             '_getRelatedPropertyList' )
  def _getRelatedPropertyList(self, id, property_name, spec=(), filter=None,
                                      portal_type=(), strict_membership=0):
    return self._getCategoryTool().getRelatedPropertyList(self, id,
                          property_name=property_name,
                          spec=spec, filter=filter,
                          portal_type=portal_type,
                          strict_membership=strict_membership)

  security.declareProtected( Permissions.AccessContentsInformation,
                             'getRelatedPropertyList' )
  getRelatedPropertyList = _getRelatedPropertyList

  security.declareProtected( Permissions.View, 'getValueUids' )
  def getValueUids(self, id, spec=(), filter=None, portal_type=()):
    uid_list = []
    for o in self._getValueList(id, spec=spec, filter=filter, portal_type=portal_type):
      uid_list.append(o.getUid())
    return uid_list

  security.declareProtected( Permissions.ModifyPortalContent, '_setValueUids' )
  def _setValueUids(self, id, uids, spec=(), filter=None, portal_type=()):
    # We must do an ordered list so we can not use the previous method
    # self._setValue(id, self.portal_catalog.getObjectList(uids), spec=spec)
    references = []
    for uid in uids:
      references.append(self.portal_catalog.getObject(uid))
    self._setValue(id, references, spec=spec, filter=filter, portal_type=portal_type)

  security.declareProtected( Permissions.ModifyPortalContent, 'setValueUids' )
  def setValueUids(self, id, uids, spec=(), filter=None, portal_type=()):
    self._setValueUids(id, uids, spec=spec, filter=filter, portal_type=portal_type)
    self.reindexObject()

  security.declareProtected( Permissions.ModifyPortalContent, '_addValue' )
  def _addValue(self, id, value, spec=(), filter=None, portal_type=()):
    pass

  security.declareProtected( Permissions.ModifyPortalContent, '_delValue' )
  def _delValue(self, id, value, spec=(), filter=None, portal_type=()):
    pass

  security.declareProtected( Permissions.ModifyPortalContent, 'updateRelation' )
  def updateRelation(self, key, value, REQUEST):
    return REQUEST

  # Private accessors for the implementation of categories
  security.declareProtected( Permissions.ModifyPortalContent, '_addToCategory' )
  def _addToCategory(self, category, node):
    pass

  security.declareProtected( Permissions.ModifyPortalContent, '_delFomCategory' )
  def _delFomCategory(self, category, node):
    pass

  security.declareProtected( Permissions.ModifyPortalContent, '_setCategoryMembership' )
  def _setCategoryMembership(self, category, node_list, spec=(),
                                             filter=None, portal_type=(), base=0):
    self._getCategoryTool().setCategoryMembership(self, category, node_list,
                       spec=spec, filter=filter, portal_type=portal_type, base=base)
    #self.activate().edit() # Do nothing except call workflow method
    # XXX This is a problem - it is used to circumvent a lack of edit

  security.declareProtected( Permissions.ModifyPortalContent, 'setCategoryMembership' )
  def setCategoryMembership(self, category, node_list, spec=(), portal_type=(), base=0):
    self._setCategoryMembership(category,
                      node_list, spec=spec, filter=filter, portal_type=portal_type, base=base)
    self.reindexObject()

  security.declareProtected( Permissions.ModifyPortalContent, '_setDefaultCategoryMembership' )
  def _setDefaultCategoryMembership(self, category, node_list,
                                    spec=(), filter=None, portal_type=(), base=0):
    self._getCategoryTool().setDefaultCategoryMembership(self, category,
                     node_list, spec=spec, filter=filter, portal_type=portal_type, base=base)

  security.declareProtected( Permissions.ModifyPortalContent, 'setDefaultCategoryMembership' )
  def setDefaultCategoryMembership(self, category, node_list,
                                           spec=(), filter=None, portal_type=(), base=0):
    self._setCategoryMembership(category, node_list, spec=spec, filter=filter,
                                                  portal_type=portal_type, base=base)
    self.reindexObject()

  security.declareProtected( Permissions.AccessContentsInformation, '_getCategoryMembershipList' )
  def _getCategoryMembershipList(self, category, spec=(), filter=None, portal_type=(), base=0 ):
    """
      This returns the list of categories for an object
    """
    return self._getCategoryTool().getCategoryMembershipList(self, category, spec=spec,
                                                   filter=filter, portal_type=portal_type, base=base)

  security.declareProtected( Permissions.AccessContentsInformation, 'getCategoryMembershipList' )
  getCategoryMembershipList = _getCategoryMembershipList

  security.declareProtected( Permissions.AccessContentsInformation,
                                               '_getAcquiredCategoryMembershipList' )
  def _getAcquiredCategoryMembershipList(self, category, base=0 , spec=(),
                                              filter=None, **kw ):
    """
      Returns the list of acquired categories
    """
    return self._getCategoryTool().getAcquiredCategoryMembershipList(self,
                             category, base=base, spec=spec, filter=filter, **kw )

  security.declareProtected( Permissions.AccessContentsInformation,
                                           'getAcquiredCategoryMembershipList' )
  getAcquiredCategoryMembershipList = _getAcquiredCategoryMembershipList

  security.declareProtected( Permissions.AccessContentsInformation, '_getCategoryMembershipItemList' )
  def _getCategoryMembershipItemList(self, category, spec=(), filter=None, portal_type=(), base=0):
    membership_list = self._getCategoryMembershipList(category,
                            spec = spec, filter=filter, portal_type=portal_type, base=base)
    return [(x, x) for x in membership_list]

  security.declareProtected( Permissions.AccessContentsInformation,
                                          '_getAcquiredCategoryMembershipItemList' )
  def _getAcquiredCategoryMembershipItemList(self, category, spec=(),
             filter=None, portal_type=(), base=0, method_id=None, sort_id='default'):
    # Standard behaviour - should be OK
    # sort_id should be None for not sort - default behaviour in other methods
    if method_id is None and sort_id in (None, 'default'):
      membership_list = self._getAcquiredCategoryMembershipList(category,
                           spec = spec, filter=filter, portal_type=portal_type, base=base)
      if sort_id == 'default':
        membership_list.sort()
      return [(x, x) for x in membership_list]
    # Advanced behaviour XXX This is new and needs to be checked
    membership_list = self._getAcquiredCategoryMembershipList(category,
                           spec = spec, filter=filter, portal_type=portal_type, base=1)
    result = []
    for path in membership_list:
      value = self._getCategoryTool().resolveCategory(path)
      if value is not None:
        result += [value]
    result.sort(lambda x, y: cmp(getattr(x,sort_id)(),getattr(y,sort_id)()))
    if method_id is None:
      return [(x, x) for x in membership_list]
    return map(lambda x: (x,getattr(x, method_id)()), membership_list)

  security.declareProtected( Permissions.View, '_getDefaultCategoryMembership' )
  def _getDefaultCategoryMembership(self, category, spec = (), filter=None, portal_type=(), base = 0 ):
    membership = self._getCategoryTool().getCategoryMembershipList(self,
                     category, spec = spec, filter=filter, portal_type=portal_type, base = base)
    if len(membership) > 0:
      return membership[0]
    else:
      return None

  security.declareProtected( Permissions.View, '_getDefaultAcquiredCategoryMembership' )
  def _getDefaultAcquiredCategoryMembership(self, category,
                                        spec=(), filter=None, portal_type=(), base=0, default=None):
    membership = self._getAcquiredCategoryMembershipList(category,
                spec=spec, filter=filter, portal_type=portal_type, base=base)
    if len(membership) > 0:
      return membership[0]
    else:
      return default

  security.declareProtected( Permissions.View, 'getDefaultAcquiredCategoryMembership' )
  getDefaultAcquiredCategoryMembership = _getDefaultAcquiredCategoryMembership

  security.declareProtected( Permissions.View, 'getCategoryList' )
  def getCategoryList(self):
    """
      Returns the list of local categories
    """
    return self._getCategoryTool().getCategoryList(self)

  security.declareProtected( Permissions.View, '_getCategoryList' )
  def _getCategoryList(self):
    return self._getCategoryTool()._getCategoryList(self)

  security.declareProtected( Permissions.View, 'getAcquiredCategoryList' )
  def getAcquiredCategoryList(self):
    """
      Returns the list of acquired categories
    """
    return self._getCategoryTool().getAcquiredCategoryList(self)

  security.declareProtected( Permissions.View, '_getAcquiredCategoryList' )
  def _getAcquiredCategoryList(self):
    return self._getCategoryTool()._getAcquiredCategoryList(self)

  security.declareProtected( Permissions.ModifyPortalContent, 'setCategoryList' )
  def setCategoryList(self, path_list):
    self._setCategoryList(path_list)
    self.reindexObject()

  security.declareProtected( Permissions.ModifyPortalContent, '_setCategoryList' )
  def _setCategoryList(self, path_list):
    self.portal_categories._setCategoryList(self, path_list)

  security.declareProtected( Permissions.View, 'getBaseCategoryList' )
  def getBaseCategoryList(self):
    """
      Lists the base_category ids which apply to this instance
    """
    return self._getCategoryTool().getBaseCategoryList(context=self)

  security.declareProtected( Permissions.View, 'getBaseCategoryIds' )
  getBaseCategoryIds = getBaseCategoryList

  security.declareProtected( Permissions.View, 'getBaseCategoryValueList' )
  def getBaseCategoryValueList(self):
    return self._getCategoryTool().getBaseCategoryValues(context=self)

  security.declareProtected( Permissions.View, 'getBaseCategoryValues' )
  getBaseCategoryValues = getBaseCategoryValueList

  security.declareProtected( Permissions.ModifyPortalContent, '_cleanupCategories' )
  def _cleanupCategories(self):
    self._getCategoryTool()._cleanupCategories()

  # Category testing
  security.declareProtected( Permissions.View, 'isMemberOf' )
  def isMemberOf(self, category):
    """
      Tests if an object if member of a given category
    """
    return self._getCategoryTool().isMemberOf(self, category)

  security.declareProtected( Permissions.View, 'isAcquiredMemberOf' )
  def isAcquiredMemberOf(self, category):
    """
      Tests if an object if member of a given category
    """
    return self._getCategoryTool().isAcquiredMemberOf(self, category)

  # Aliases
  security.declareProtected(Permissions.AccessContentsInformation,
                            'getTitleOrId')
  def getTitleOrId(self):
    """
      Returns the title or the id if the id is empty
    """
    if self.getTitle()is not None:
      title = str(self.getTitle())
      if title == '' or title is None:
        return self.getId()
      else:
        return title
    return self.getId()

  security.declareProtected( Permissions.View, 'Title' )
  Title = getTitleOrId

  # This method allows to sort objects in list is a more reasonable way
  security.declareProtected(Permissions.View, 'getIntId')
  def getIntId(self):
    try:
      return int(self.getId())
    except TypeError:
      return None

  # Default views
  security.declareProtected(Permissions.View, 'list')
  def list(self,reset=0):
        '''
        Returns the default list even if folder_contents is overridden.
        '''
        list_action = _getViewFor(self, view='list')
        if getattr(aq_base(list_action), 'isDocTemp', 0):
            return apply(list_action, (self, self.REQUEST),reset=reset)
        else:
            return list_action(reset=reset)

  # Proxy methods for security reasons
  security.declareProtected(Permissions.AccessContentsInformation, 'getOwnerInfo')
  def getOwnerInfo(self):
    """
    this returns the Owner Info
    """
    return self.owner_info()

  # Missing attributes
  security.declareProtected(Permissions.AccessContentsInformation, 'getPortalType')
  def getPortalType(self):
    """
    This returns the portal_type
    """
    return self.portal_type

  security.declareProtected(Permissions.AccessContentsInformation,
                            'getTranslatedPortalType')
  def getTranslatedPortalType(self):
    """
      This returns the translated portal_type
    """
    portal_type = self.portal_type
    localizer = getToolByName(self, 'Localizer')
    return localizer.erp5_ui.gettext(portal_type).encode('utf8')

  security.declareProtected(Permissions.ModifyPortalContent, 'setPortalType')
  def setPortalType(self, portal_type = None):
    """
    This allows to set the portal_type
    """
    if portal_type is not None:
      self.portal_type = portal_type


  security.declareProtected(Permissions.AccessContentsInformation, 'getMetaType')
  def getMetaType(self):
    """
    This returns the Meta Type
    """
    return self.meta_type

#   def _recursiveApply(self,f):
#     """
#     """
#     error_list = []
#     for o in self.objectValues():
#       try:
#         error_list += f(o)
#         error_list += o.recursiveApply(f)
#       except:
#         LOG('ERP5Type.Base',0,"error in recursiveApply : %s, %s on %s"
#           % (str(sys.exc_type),str(sys.exc_value),o.getPath()))
#
#     return error_list
#
#   def recursiveApply(self,f):
#     """
#       This allows to apply a function, f, on the current object
#       and all subobjects.
#
#       This function can be created inside a python script on the
#       zope management interface, then we just have to call recursiveApply.
#     """
#     return self._recursiveApply(f)

  # Content consistency implementation
  security.declarePrivate('_checkConsistency')
  def _checkConsistency(self, fixit=0):
    """
    Check the constitency of objects.

    Private method.
    """
    return []

  security.declarePrivate('_fixConsistency')
  def _fixConsistency(self):
    """
    Fix the constitency of objects.

    Private method.
    """
    return self._checkConsistency(fixit=1)

  security.declareProtected(Permissions.AccessContentsInformation, 'checkConsistency')
  def checkConsistency(self, fixit=0):
    """
    Check the constitency of objects.

    For example we can check if every Organisation has at least
    one Address.

    This method looks the constraints defines inside the propertySheets
    then check each of them

    constraint_list -- the list of constraint we have to check
    """
    error_list = self._checkConsistency(fixit = fixit)
    # We are looking inside all instances in constraints, then we check
    # the consistency for all of them

    for constraint_instance in self.constraints:
      if fixit:
        error_list += constraint_instance.fixConsistency(object=self)
      else:
        error_list += constraint_instance.checkConsistency(object=self)

    if len(error_list) > 0 and fixit:
      self.reindexObject()

    return error_list

  security.declareProtected(Permissions.ManagePortal, 'fixConsistency')
  def fixConsistency(self):
    """
    Fix the constitency of objects.
    """
    return self.checkConsistency(fixit=1)

  # Context related methods
  security.declarePublic('asContext')
  def asContext(self, context=None, REQUEST=None, **kw):
    if context is None:
      # Make a copy
      context = self.__class__(self.getId())
      context.__dict__.update(self.__dict__)
      # Copy REQUEST properties to self
      if REQUEST is not None:
        context.__dict__.update(REQUEST)
      # Define local properties
      if kw is not None: context.__dict__.update(kw)
      # Make it a temp content
      temp_object = TempBase(self.getId())
      for k in ('isIndexable', 'reindexObject', 'recursiveReindexObject', 'activate', 'setUid', ):
        setattr(context, k, getattr(temp_object,k))
      # Return result
      return context.__of__(self.aq_parent)
    else:
      return context.asContext(REQUEST=REQUEST, **kw)

  # Workflow Related Method
  security.declarePublic('getWorkflowStateItemList')
  def getWorkflowStateItemList(self):
    """
      Returns a list of tuples {id:workflow_id, state:workflow_state}
    """
    result = []
    for wf in self.portal_workflow.getWorkflowsFor(self):
      result += [(wf.id, wf._getWorkflowStateOf(self, id_only=1))]
    return result

  security.declarePublic('getWorkflowInfo')
  def getWorkflowInfo(self, name='state', wf_id=None):
    """
      Returns a list of tuples {id:workflow_id, state:workflow_state}
    """
    portal_workflow = self.portal_workflow
    return portal_workflow.getInfoFor(self, name, wf_id=wf_id)

  security.declareProtected(Permissions.AccessContentsInformation,
                            'objectCount')
  def objectCount(self):
    """
      Returns number of objects
    """
    return len(self.objectIds())

  # Hide Acquisition to prevent loops (ex. in cells)
  # Another approach is to use XMLObject everywhere
  # DIRTY TRICK XXX
#   def objectValues(self, *args, **kw):
#     return []
#
#   def contentValues(self, *args, **kw):
#     return []
#
#   def objectIds(self, *args, **kw):
#     return []
#
#   def contentIds(self, *args, **kw):
#     return []


  security.declarePublic('immediateReindexObject')
  def immediateReindexObject(self, *args, **kw):
    """
      Reindexes an object - also useful for testing
    """
    root_indexable = int(getattr(self.getPortalObject(),'isIndexable',1))
    if self.isIndexable and root_indexable:
      #LOG("immediateReindexObject",0,self.getRelativeUrl())
      PortalContent.reindexObject(self, *args, **kw)
    else:
      pass
      #LOG("No reindex now",0,self.getRelativeUrl())

  security.declarePublic('recursiveImmediateReindexObject')
  recursiveImmediateReindexObject = immediateReindexObject

  security.declarePublic('reindexObject')
  def reindexObject(self, *args, **kw):
    """
      Reindexes an object
      args / kw required since we must follow API
    """
    self._reindexObject(*args, **kw)

  def _reindexObject(self, *args, **kw):
    # When the activity supports group methods, portal_catalog/catalogObjectList is called instead of
    # immediateReindexObject.
    root_indexable = int(getattr(self.getPortalObject(),'isIndexable',1))
    if self.isIndexable and root_indexable:
      self.activate(group_method_id='portal_catalog/catalogObjectList', alternate_method_id='alternateReindexObject', **kw).immediateReindexObject(*args, **kw)

  security.declarePublic('recursiveReindexObject')
  recursiveReindexObject = reindexObject

  security.declareProtected( Permissions.AccessContentsInformation, 'getIndexableChildValueList' )
  def getIndexableChildValueList(self):
    """
      Get indexable childen recursively.
    """
    if self.isIndexable:
      return [self]
    return []

  security.declareProtected(Permissions.ModifyPortalContent, 'reindexObjectSecurity')
  def reindexObjectSecurity(self):
    """
        Reindex security-related indexes on the object
        (and its descendants).
    """
    # In ERP5, simply reindex all objects.
    #LOG('reindexObjectSecurity', 0, 'self = %r, self.getPath() = %r' % (self, self.getPath()))
    self.reindexObject()

  security.declareProtected( Permissions.AccessContentsInformation, 'asXML' )
  def asXML(self, ident=0):
    """
        Generate an xml text corresponding to the content of this object
    """
    return Base_asXML(self, ident=ident)

  # Optimized Menu System
  security.declarePublic('allowedContentTypes')
  def allowedContentTypes( self ):
    """
      List portal_types which can be added in this folder / object.
    """
    return []

  security.declareProtected(Permissions.View, 'getBinaryData')
  def getBinaryData(self):
    """
      Return the binary data
    """
    bin = None
    if hasattr(self,'_original'):
      bin = self._original._data()
    elif hasattr(self,'_data'):
      bin = self._data
    elif hasattr(self,'data'):
      bin = self.data
    if bin is not None:
      return StringIO(str(bin))
    return None

  security.declareProtected(Permissions.ModifyPortalContent, 'setBinaryData')
  def setBinaryData(self, data):
    """
      Set the binary data, data must be a cStringIO
    """
    self.edit(file=data)
    #LOG('Base.setBinaryData',0,'data: %s' % str(data))
    #obj=''
    #if hasattr(self,'_original'):
    #  LOG('Base.setBinaryData',0,'_original for : %s' % str(self))
    #  self._original.data = data
    #elif hasattr(self,'_data'):
    #  LOG('Base.setBinaryData',0,'_data for : %s' % str(self))
    #  self._data = data
    #elif hasattr(self,'data'):
    #  LOG('Base.setBinaryData',0,'data for : %s' % str(self))
    #  self.data = data

  security.declarePublic('commitTransaction')
  def commitTransaction(self):
    # Commit a zope transaction (to reduce locks)
    get_transaction().commit()

  security.declareProtected(Permissions.ModifyPortalContent, 'abortTransaction')
  def abortTransaction(self):
    # Abort a zope transaction (to reduce locks)
    get_transaction().abort()

  # Hash method
  def __hash__(self):
    return hash(self.getUid())

  security.declareProtected(Permissions.ModifyPortalContent, 'setGuid')
  def setGuid(self):
    """
    This generate a global and unique id
    It will be defined like this :
     full dns name + portal_name + uid + random
     the guid should be defined only one time for each object
    """
    if not hasattr(self, 'guid'):
      guid = ''
      # Set the dns name
      guid += gethostbyaddr(gethostname())[0]
      guid += '_' + self.portal_url.getPortalPath()
      guid += '_' + str(self.uid)
      guid += '_' + str(random.randrange(1,2147483600))
    setattr(self,'guid',guid)

  security.declareProtected(Permissions.AccessContentsInformation, 'getGuid')
  def getGuid(self):
    """
    Get the global and unique id
    """
    return getattr(self,'guid',None)

  # Type Casting
  security.declarePrivate( '_getTypeBasedMethod' )
  def _getTypeBasedMethod(self, method_id, script_id=None):
    """
      Looks up for
    """
    # Look at local and acquired categories and make it criterion membership
    script_name = ''
    script = None
    script_name_end = '_%s' % method_id
    # Look at a local script which
    # can return a new predicate.
    if script_id is not None:
      script = getattr(self, script_id)
    else:
      for script_name_begin in [self.getPortalType(), self.getMetaType(), self.__class__.__name__]:
        script_name = join([script_name_begin.replace(' ',''), script_name_end ], '')
        if hasattr(self, script_name):
          script = getattr(self, script_name)
          break
    return script

  # Predicate handling
  security.declareProtected(Permissions.AccessContentsInformation, 'asPredicate')
  def asPredicate(self, script_id=None):
    """
      This method tries to convert the current Document into a predicate
      looking up methods named Class_asPredictae, MetaType_asPredicate, PortalType_asPredicate
    """
    script = self._getTypeBasedMethod('asPredicate', script_id=script_id)
    if script is not None:
      return script()
    return None

  def _getAcquireLocalRoles(self):
    """
    This methods the value of acquire_local_roles of the object's portal_type
    True means, local roles are acquired, which is the standard behavior of
    Zope objects. False means that the role acquisition chain is cut.

    The code to support this is in the user folder.
    """
    def cashed_getAcquireLocalRoles(portal_type):
      return self._getTypesTool()[self.getPortalType()].acquire_local_roles

    cashed_getAcquireLocalRoles = CachingMethod(cashed_getAcquireLocalRoles,
                                                id='Base__getAcquireLocalRoles')
    return cashed_getAcquireLocalRoles(portal_type=self.getPortalType())

  security.declareProtected(Permissions.View, 'get_local_permissions')
  def get_local_permissions(self):
    """
    This works like get_local_roles. It allows to get all
    permissions defined locally
    """
    local_permission_list = ()
    for permission in self.possible_permissions():
      permission_role = getattr(self,pname(permission),None)
      if permission_role is not None:
        local_permission_list += ((permission,permission_role),)
    return local_permission_list

  security.declareProtected(Permissions.ManagePortal, 'manage_setLocalPermissions')
  def manage_setLocalPermissions(self,permission,local_permission_list=None):
    """
    This works like manage_setLocalRoles. It allows to set all
    permissions defined locally
    """
    permission_name = pname(permission)
    if local_permission_list is None:
      if hasattr(self,permission_name):
        delattr(self,permission_name)
    else:
      if isinstance(local_permission_list, str):
        local_permission_list = (local_permission_list,)
      setattr(self,permission_name,tuple(local_permission_list))

  ### Content accessor methods
  security.declareProtected(Permissions.View, 'getSearchableText')
  def getSearchableText(self, md=None):
      """\
      Used by the catalog for basic full text indexing
      We should try to do some kind of file conversion here
      """
      searchable_text = "%s %s %s" %  (self.getTitle(), self.getDescription(),
                                    self.getId())
      return searchable_text

  # Compatibility with CMF Catalog / CPS sites
  SearchableText = getSearchableText

  security.declareProtected(Permissions.View, 'newError')
  def newError(self, **kw):
    """
    Create a new Error object
    """
    from Products.ERP5Type.Error import Error
    return Error(**kw)


  _temp_isIndexable = 0

  def _temp_reindexObject(self, *args, **kw):
    pass

  def _temp_recursiveReindexObject(self, *args, **kw):
    pass

  def _temp_activate(self):
    return self

  def _temp_setUid(self, value):
    self.uid = value # Required for Listbox so that no casting happens when we use TempBase to create new objects

  def _temp_setTitle(self, value):
    """
    Required so that getProperty('title') will work on tempBase objects
    The dynamic acquisition work very well for a lot of properties, but
    not for title. For example, if we do setProperty('organisation_url'), then
    even if organisation_url is not in a propertySheet, the method getOrganisationUrl
    will be generated. But this does not work for title, because I(seb)'m almost sure
    there is somewhere a method '_setTitle' or 'setTitle' with no method getTitle on Base.
    That why setProperty('title') and getProperty('title') does not work.
    """
    self.title = value

  def _temp_getTitle(self):
    return getattr(self,'title',None)

  security.declarePublic('log')
  def log(self, subsystem, message, level=INFO):
    """Put a log message """
    LOG(subsystem, level, message)

  # Dublin Core Emulation for CMF interoperatibility
  # CMF Dublin Core Compatibility
  def Subject(self):
    return self.getSubjectList()

  def Description(self):
    return self.getDescription('')

  def Contributors(self):
    return self.getContributorList('')

  def EffectiveDate(self):
    return self.getEffectiveDate('None')

  def ExpirationDate(self):
    return self.getExpirationDate('None')

  def Contributors(self):
    return self.getContributorList()

  def Format(self):
    return self.getFormat('')

  def Language(self):
    return self.getLanguage('')

  def Rights(self):
    return self.getRight('')

  # Creation and modification date support through workflow
  security.declareProtected(Permissions.AccessContentsInformation, 'getCreationDate')
  def getCreationDate(self):
    """
      Returns the creation date of the document based on workflow information
    """
    # Check if edit_workflow defined
    portal_workflow = getToolByName(self, 'portal_workflow')
    wf = portal_workflow.getWorkflowById('edit_workflow')
    wf_list = list(portal_workflow.getWorkflowsFor(self))
    if wf is not None: wf_list = [wf] + wf_list
    for wf in wf_list:
      history = wf.getInfoFor(self, 'history', None)
      if history is not None:
        if len(history):
          # Then get the first line of edit_workflow
          return history[0].get('time', None)
    if hasattr(self, 'CreationDate') :
      return asDate(self.CreationDate())
    return None

  security.declareProtected(Permissions.AccessContentsInformation, 'getModificationDate')
  def getModificationDate(self):
    """
      Returns the modification date of the document based on workflow information
    """
    # Check if edit_workflow defined
    portal_workflow = getToolByName(self, 'portal_workflow')
    wf = portal_workflow.getWorkflowById('edit_workflow')
    wf_list = list(portal_workflow.getWorkflowsFor(self))
    if wf is not None: wf_list = [wf] + wf_list
    for wf in wf_list:
      history = wf.getInfoFor(self, 'history', None)
      if history is not None:
        if len(history):
          # Then get the last line of edit_workflow
          return history[-1].get('time', None)
    return None

  # Layout management
  security.declareProtected(Permissions.AccessContentsInformation, 'getApplicableLayout')
  def getApplicableLayout(self):
    """
      Return applicable layout in this acquisition context by
      browsing context parents.

      We have to take into account context before containment. This
      is why standard acquisition must be circumvented here.
    """
    current = self
    # First try to get a container layout
    if hasattr(current, 'getContainerLayout') and current.getContainerLayout() not in ('', None):
      return current.getContainerLayout()
    # First try to get a content layout
    while current is not None:
      if hasattr(current, 'getContentLayout') and current.getContentLayout() not in ('', None):
        return current.getContentLayout()
      current = current.getParentValue()
      if not hasattr(current, 'getApplicableLayout'):
        return None
    return None


  security.declareProtected(Permissions.ChangeLocalRoles,
                            'updateLocalRolesOnSecurityGroups')
  def updateLocalRolesOnSecurityGroups(self, **kw):
    """Assign Local Roles to Groups on self, based on Portal Type Role
    Definitions and "ERP5 Role Definition" objects contained inside self.
    """
    self._getTypesTool().getTypeInfo(self)\
                          .updateLocalRolesOnSecurityGroups(self, **kw)

  security.declareProtected(Permissions.ModifyPortalContent,
                            'assignRoleToSecurityGroup')
  def assignRoleToSecurityGroup(self, **kw):
    """This is basically the same as `updateLocalRolesOnSecurityGroups`, but
    with a different permission.
    """
    warnings.warn('assignRoleToSecurityGroup is a deprecated alias to '
                  'updateLocalRolesOnSecurityGroups. Please note that the '
                  'permission changed to "Change Local Roles".',
                  DeprecationWarning)
    self.updateLocalRolesOnSecurityGroups(**kw)

  # Template Management
  security.declareProtected(Permissions.View, 'getDocumentTemplateList')
  def getDocumentTemplateList(self) :
    """
      Returns an empty list of allowed templates
      (this is not a folder)
    """
    return []

  security.declareProtected(Permissions.ModifyPortalContent,'makeTemplate')
  def makeTemplate(self):
    """
      Make document behave as a template.
      A template is no longer indexable

      TODO:
         - stronger security model
         - prevent from changing templates or invoking workflows
    """
    parent = self.getParentValue()
    if parent.getPortalType() != "Preference" and not parent.isTemplate:
      raise ValueError, "Template documents can not be created outside Preferences"
    # Make sure this object is not in the catalog
    catalog = getToolByName(self, 'portal_catalog', None)
    if catalog is not None:
       catalog.unindexObject(self)
    self.isIndexable = 0
    self.isTemplate = 1

  security.declareProtected(Permissions.ModifyPortalContent,'makeTemplateInstance')
  def makeTemplateInstance(self):
    """
      Make document behave as standard document (indexable)
    """
    if self.getParentValue().getPortalType() == "Preference":
      raise ValueError, "Template instances can not be created within Preferences"
    # We remove attributes from the instance
    # We do this rather than self.isIndexable = 0 because we want to
    # go back to previous situation (class based definition)
    if self.__dict__.has_key('isIndexable'): delattr(self, 'isIndexable')
    if self.__dict__.has_key('isTemplate'): delattr(self, 'isTemplate')

    # Add to catalog
    self.reindexObject()

  security.declarePublic('serialize')
  def serialize(self):
    """Make the transaction accessing to this object atomic
    """
    self.id = self.id

  security.declareProtected( Permissions.ManagePortal, 'asDocumentationHelper' )
  def asDocumentationHelper(self, item_id=None):
    """
      Fills and return a DocHelper object from context.
      Overload this in any object the has to fill the DocHelper in its own way.

      item_id : If specified, the documented item will be
                getattr(self, item_title) if it exists, otherwise None will
                be returned.

      TODO:
       - Check that filtering is correct : display only and every things
         defined on the class itself.
       - Add a list of all accessible things in the documented item context
         (heritated methods & attributes) in a light way that still allows to
         link directly to the corresponding documentation.
       - Rewrite accessor generation system so that it can generate accessor
         names when given a property/category.

       KEEPMEs:
         There are pieces of code in this function that can have interesting
         results, but who are also very verbose. They are disabled (commented
         out) by default, but they should be kept.
         Explanation of the interest :
         The accessors are gathered from 2 sources : the ones defined on the
         PortalType, and systematically generated names, and tested for
         presence on the documented item.
         There are 4 cases then :
         -Accessor whose name was generated exists both on the PortalType and
          on the documented item. That's normal.
         -Accessor whose name was generated exists neither on the PortalType
          nor on the documented item. That's normal, but could mean that the
          accessor name generator isn't optimal.
         -Accessor whose name was generated is found on the object but not on
          the PortalType. This is a problem.
         -Accessors gathered from PortalType aren't all found by guessing
          systematically the names. That means that the accessor name
          generation is not perfect and requires improvement.

         nb: the accessors are gathered from 2 sources, the first is somehow
         accidental when searching for workflow methods defined on the
         PortalType, and are browsed a second time to be able to group them
         by property or category.
    """
    if item_id is None:
      documented_item = self
      item_id = documented_item.getTitle()
    elif getattr(self, item_id, None) is not None:
      documented_item = getattr(self, item_id)
    else:
      return None

    # The documented object is an instance (or not) of this class.
    item_class = getattr(documented_item, '__bases__', None) is None \
                 and documented_item.__class__ \
                 or documented_item

    static_method_list = []    # Class methods
    static_property_list = []  # Class attributes
    dynamic_method_list = []   # Workflow methods
    dynamic_property_list = [] # Document properties
    dynamic_category_list = [] # Categories
    dynamic_accessor_list = [] # Accessors
    found_accessors = {}       # Accessor names : filled by PortalType-level
                               # scan, and used in PropertySheet-level scan.
    dochelper = newTempDocumentationHelper(self.getParentValue(), self.getId(),
                  title=item_id, type=item_class.__name__,
                  description=inspect.getdoc(documented_item),
                )
    dochelper.setInheritanceList([x.__name__ for x in item_class.__bases__])
    try:
      dochelper.setSourcePath(inspect.getsourcefile(item_class))
    except (IOError, TypeError):
      pass
    # dochelper.setSecurity() # (maybe) TODO: Add class instance security gthering.

    # Class-level method & properties
    for k, v in item_class.__dict__.items():
      subdochelper = newTempDocumentationHelper(dochelper, k,
                  title=k, description=inspect.getdoc(v),
                  security=repr(getattr(documented_item, '%s__roles__' % (k,),None)))
      try:
        subdochelper.setType(v.__class__.__name__)
      except AttributeError:
        pass
      try:
        subdochelper.setSourcePath(inspect.getsourcefile(v))
      except (IOError, TypeError), err:
        pass
      try:
        subdochelper.setSourceCode(inspect.getsource(v))
      except (IOError, TypeError), err:
        pass
      try:
        subdochelper.setArgumentList(inspect.getargspec(v))
      except (IOError, TypeError), err:
        pass
      if subdochelper.getType() in ('function',): # This is a method
        static_method_list.append(subdochelper)
      elif subdochelper.getType() in ('int', 'float', 'long', 'str', 'tuple', 'dict', 'list') \
           and not subdochelper.getTitle().startswith('__'): # This is a property
        subdochelper.setContent(pformat(v))
        static_property_list.append(subdochelper)
      # FIXME: Is there any other interesting type ?

    # PortalType-level methods
    # XXX: accessing portal_type directly because accessors are not generated on instances
    if getattr(documented_item, 'portal_type', None) is not None:
      for k, v in Base.aq_portal_type[documented_item.portal_type].__dict__.items():
        if callable(v) and not (k.startswith('_base') or k.startswith('_category')):
          subdochelper = newTempDocumentationHelper(dochelper, k,
                    title=k, description=inspect.getdoc(v),
                    security=repr(getattr(documented_item, '%s__roles__' % (k,),None)))
          try:
            my_type = v.__class__.__name__
            subdochelper.setType(my_type)
          except AttributeError:
            pass
          if 'Setter' not in my_type and \
             'Getter' not in my_type and \
             'Tester' not in my_type: # Accessors are handled separatelly.
            dynamic_method_list.append(subdochelper)
# KEEPME: usefull to track the differences between accessors defined on
# PortalType and the one detected on the documented item.
#          else:
#            found_accessors[k] = v

    def generatePropertyAccessorNameList(property):
      """
        Generates the possible accessor names for given property.

        FIXME: Should not exist here, but as accessor generation system.
      """
      from Products.ERP5Type.Utils import UpperCase
      res=[]
      cased_id = UpperCase(property['id'])
      for hidden in ('', '_'):
        for getset in ('get', 'set', 'has'): # 'is',
          for default in ('', 'Default', 'Translated'):
            for value in ('', 'Value', 'TranslationDomain'):
              for multivalued in ('', 'List', 'Set'):
                res.append('%s%s%s%s%s%s' % (hidden, getset, default, cased_id, value, multivalued))
      if property.has_key('acquired_property_id') and \
         property['type'] == 'content':
        for aq_property_id in property['acquired_property_id']:
          cased_id = UpperCase('%s_%s' % (property['id'], aq_property_id))
          for hidden in ('', '_'):
            for getset in ('get', 'set'):
              for default in ('', 'Default'):
                for multivalued in ('', 'List'):
                  res.append('%s%s%s%s%s' % (hidden, getset, default, cased_id, multivalued))
      return res

    def generateCategoryAccessorNameList(category):
      """
        Generates the possible accessor names for given category.

        FIXME: Should not exist here, but as accessor generation system.
      """
      from Products.ERP5Type.Utils import UpperCase
      cased_id=UpperCase(category)
      res=['%s%sIds' % (cased_id[0].lower(), cased_id[1:]),
           '%s%sValues' % (cased_id[0].lower(), cased_id[1:])]
      for hidden in ('', '_'):
        for default in ('', 'Default'):
          for multivalued in ('', 'List', 'Set'):
            for attribute in ('', 'TranslatedTitle', 'Uid', 'LogicalPath', 'Id', 'TitleOrId', 'Reference', 'Title'):
              res.append('%sget%s%s%s%s' % (hidden, default, cased_id, attribute, multivalued))
            for attribute in ('', 'Value', 'Uid'):
              res.append('%sset%s%s%s%s' % (hidden, default, cased_id, attribute, multivalued))
      return res

    def accessorAsDocumentationHelper(accessor):
      """
        Generates a documentation helper about a given accessor.
      """
      accessor_dochelper = newTempDocumentationHelper(subdochelper, accessor_name,
                                                      title=accessor_name,
                                                      description=inspect.getdoc(accessor))
      try:
        accessor_dochelper.setSourcePath(inspect.getsourcefile(accessor))
      except (IOError, TypeError), err:
        pass
      try:
        accessor_dochelper.setSourceCode(inspect.getsource(accessor))
      except (IOError, TypeError), err:
        pass
# KEEPME: usefull to track the differences between accessors defined on
# PortalType and the one detected on the documented item.
#      if found_accessors.has_key(accessor_name):
#        del(found_accessors[accessor_name])
#      else:
#        LOG('asDocumentationHelper', 0,
#            'Found but not in the accessor list : %s of type %s' % \
#            (accessor_name, accessor.__class__.__name__))
      return accessor_dochelper

    # PropertySheet-level properties & categories
    # Also handles accessors.
    seen_properties=[]
    seen_categories=[]
    if getattr(documented_item, 'property_sheets', None) is not None:
      for property_sheet in documented_item.property_sheets:
        if getattr(property_sheet, '_properties', None) is not None:
          for property in property_sheet._properties:
            if property in seen_properties:
              continue
            seen_properties.append(property)
            subdochelper = newTempDocumentationHelper(dochelper, k,
                      title=property['id'], description=property['description'],
                      type=property['type'], security=property['mode'],
                      content=pformat(documented_item.getProperty(property['id'])))
            subdochelper_dynamic_accessor_list = []
            for accessor_name in generatePropertyAccessorNameList(property):
              accessor = getattr(item_class, accessor_name, getattr(documented_item, accessor_name, None))
              # First get it on the class, and if not on the instance, thereby among dynamic accessors.
              if accessor is not None:
                subdochelper_dynamic_accessor_list.append(accessorAsDocumentationHelper(accessor))
            subdochelper_dynamic_accessor_list.sort()
            subdochelper.setDynamicAccessorList(subdochelper_dynamic_accessor_list)
            dynamic_accessor_list.append(subdochelper)
            if getattr(documented_item, property['id'], None) is not None:
              dynamic_property_list.append(subdochelper)
        if getattr(property_sheet, '_categories', None) is not None:
          for category in property_sheet._categories:
            if category in seen_categories:
              continue
            seen_categories.append(category)
            subdochelper = newTempDocumentationHelper(dochelper, category, title=category,
                      content=pformat(documented_item.getCategoryMembershipList(category)))
            subdochelper_dynamic_accessor_list = []
            for accessor_name in generateCategoryAccessorNameList(category):
              accessor = getattr(item_class, accessor_name, getattr(documented_item, accessor_name, None))
              # First get it on the class, and if not on the instance, thereby among dynamic accessors.
              if accessor is not None:
                subdochelper_dynamic_accessor_list.append(accessorAsDocumentationHelper(accessor))
            subdochelper_dynamic_accessor_list.sort()
            subdochelper.setDynamicAccessorList(subdochelper_dynamic_accessor_list)
            dynamic_accessor_list.append(subdochelper)
            dynamic_category_list.append(subdochelper)

# KEEPME: usefull to track the differences between accessors defined on
# PortalType and the one detected on the documented item.
#    LOG('asDocumentationHelper', 0, found_accessors)
    static_method_list.sort()
    dochelper.setStaticMethodList(static_method_list)
    static_property_list.sort()
    dochelper.setStaticPropertyList(static_property_list)
    dynamic_method_list.sort()
    dochelper.setDynamicMethodList(dynamic_method_list)
    dynamic_accessor_list.sort()
    dochelper.setDynamicAccessorList(dynamic_accessor_list)
    dynamic_category_list.sort()
    dochelper.setDynamicCategoryList(dynamic_category_list)
    dynamic_property_list.sort()
    dochelper.setDynamicPropertyList(dynamic_property_list)
    return dochelper

InitializeClass(Base)

class TempBase(Base):
  """
    If we need Base services (categories, edit, etc) in temporary objects
    we shoud used TempBase
  """
  isIndexable = 0

  # Declarative security
  security = ClassSecurityInfo()

  def reindexObject(self, *args, **kw):
    pass

  def recursiveReindexObject(self, *args, **kw):
    pass

  def activate(self):
    return self

  def setUid(self, value):
    self.uid = value # Required for Listbox so that no casting happens when we use TempBase to create new objects

  def setTitle(self, value):
    """
    Required so that getProperty('title') will work on tempBase objects
    The dynamic acquisition work very well for a lot of properties, but
    not for title. For example, if we do setProperty('organisation_url'), then
    even if organisation_url is not in a propertySheet, the method getOrganisationUrl
    will be generated. But this does not work for title, because I(seb)'m almost sure
    there is somewhere a method '_setTitle' or 'setTitle' with no method getTitle on Base.
    That why setProperty('title') and getProperty('title') does not work.
    """
    self.title = value

  def getTitle(self):
    """
      Returns the title of this document
    """
    return getattr(self,'title',None)

  security.declarePublic('setProperty')

def newTempDocumentationHelper(folder, id, REQUEST=None, **kw):
  o = TempDocumentationHelper(id)
  o = o.__of__(folder)
  if kw is not None:
    o._edit(force_update=1, **kw)
  return o

class TempDocumentationHelper(TempBase):
  """
    Contains information about a documentable item.
    Documentable item can be any python type, instanciated or not.
  """

  meta_type = "ERP5 Documentation Helper"
  portal_type = "Documentation Helper"

  property_sheets = ( PropertySheet.Base
                    , PropertySheet.DublinCore
                    , PropertySheet.DocumentationHelper
                    , )

  def _funcname_cmp_prepare(self, funcname):
    for pos in range(len(funcname)):
      if funcname[pos] != '_':
        break
    return '%s%s' % (funcname[pos:], funcname[:pos])

  def __cmp__(self, documentationhelper):
    my_title = self._funcname_cmp_prepare(self.getTitle())
    his_title = self._funcname_cmp_prepare(documentationhelper.getTitle())
    if my_title < his_title:
      return -1
    if my_title > his_title:
      return 1
    return 0
