##############################################################################
#
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
""" Portal class

$Id$
"""

import Globals
from Globals import package_home
#from Products.ERP5 import content_classes
from AccessControl import ClassSecurityInfo
from Products.CMFDefault.Portal import CMFSite, PortalGenerator
from Products.CMFCore.utils import getToolByName, _getAuthenticatedUser
from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5Type.Document.Folder import FolderMixIn
from Products.ERP5Type.Document import addFolder
from Acquisition import aq_base, aq_parent, aq_inner, aq_acquire
from Products.ERP5Type import allowClassTool
from Products.ERP5Type.Cache import CachingMethod
from Products.ERP5Type.ERP5Type import ERP5TypeInformation
from Products.ERP5.Document.BusinessTemplate import BusinessTemplate

import ERP5Defaults
from os import path

from zLOG import LOG
from string import join

import os

# Site Creation DTML
manage_addERP5SiteForm = Globals.HTMLFile('dtml/addERP5Site', globals())
manage_addERP5SiteForm.__name__ = 'addERP5Site'

# ERP5Site Constructor
def manage_addERP5Site(self, id, title='ERP5', description='',
                         create_userfolder=1,
                         create_activities=1,
                         email_from_address='postmaster@localhost',
                         email_from_name='Portal Administrator',
                         validate_email=0,
                         erp5_sql_connection_type='Z MySQL Database Connection',
                         erp5_sql_connection_string='test test',
                         cmf_activity_sql_connection_type='Z MySQL Database Connection',
                         cmf_activity_sql_connection_string='test test',
                         light_install=0,reindex=1,
                         RESPONSE=None):
    '''
    Adds a portal instance.
    '''
    #LOG('manage_addERP5Site, create_activities',0,create_activities)
    #LOG('manage_addERP5Site, create_activities==1',0,create_activities==1)
    gen = ERP5Generator()
    from string import strip
    id = strip(id)
    p = gen.create(self, id, create_userfolder,
                   erp5_sql_connection_type,erp5_sql_connection_string,
                   cmf_activity_sql_connection_type,cmf_activity_sql_connection_string,
                   create_activities=create_activities,light_install=light_install,
                   reindex=reindex)
    gen.setupDefaultProperties(p, title, description,
                               email_from_address, email_from_name,
                               validate_email)
    if RESPONSE is not None:
        RESPONSE.redirect(p.absolute_url())

class ERP5Site ( FolderMixIn, CMFSite ):
    """
        The *only* function this class should have is to help in the setup
        of a new ERP5.  It should not assist in the functionality at all.
    """
    meta_type = 'ERP5 Site'
    constructors = (manage_addERP5SiteForm, manage_addERP5Site, )
    uid = 0
    last_id = 0
    icon = 'portal.gif'

    _properties = (
        {'id':'title', 'type':'string'},
        {'id':'description', 'type':'text'},
        )
    title = ''
    description = ''

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    security.declareProtected(Permissions.View, 'view')
    def view(self):
        """
          Returns the default view.
          Implemented for consistency
        """
        return self.index_html()

    def hasObject(self, id):
      """Check if the portal has an id.
      """
      return id in self.objectIds()

    security.declareProtected(Permissions.AccessContentsInformation, 'getPortalObject')
    def getPortalObject(self):
      return self

    security.declareProtected(Permissions.AccessContentsInformation, 'getTitle')
    def getTitle(self):
      """
        Return the title.
      """
      return self.title

    security.declareProtected(Permissions.AccessContentsInformation, 'getUid')
    def getUid(self):
      """
        Returns the UID of the object. Eventually reindexes
        the object in order to make sure there is a UID
        (useful for import / export).

        WARNING : must be updates for circular references issues
      """
      #if not hasattr(self, 'uid'):
      #  self.reindexObject()
      return getattr(self, 'uid', 0)

    security.declareProtected(Permissions.AccessContentsInformation, 'getParentUid')
    def getParentUid(self):
      """
        A portal has no parent
      """
      return self.getUid()

    # Required to allow content creation outside folders
    security.declareProtected(Permissions.View, 'getIdGroup')
    def getIdGroup(self):
      return None

    # Required to allow content creation outside folders
    security.declareProtected(Permissions.View, 'setLastId')
    def setLastId(self, id):
      self.last_id = id

    security.declareProtected(Permissions.AccessContentsInformation, 'getPath')
    def getPath(self, REQUEST=None):
      """
        Returns the absolute path of an object
      """
      return join(self.getPhysicalPath(),'/')

    security.declareProtected(Permissions.AccessContentsInformation, 'searchFolder')
    def searchFolder(self, **kw):
      """
        Search the content of a folder by calling
        the portal_catalog.
      """
      if not kw.has_key('parent_uid'):
        kw['parent_uid'] = self.uid
      kw2 = {}
      # Remove useless matter before calling the
      # catalog. In particular, consider empty
      # strings as None values
      for cname in kw.keys():
        if kw[cname] != '' and kw[cname]!=None:
          kw2[cname] = kw[cname]
      # The method to call to search the folder
      # content has to be called z_search_folder
      method = self.portal_catalog.searchResults
      return method(**kw2)

    security.declareProtected(Permissions.AccessContentsInformation, 'countFolder')
    def countFolder(self, **kw):
      """
        Count the content of a folder by calling
        the portal_catalog.
      """
      if not kw.has_key('parent_uid'):
        kw['parent_uid'] = self.uid
      kw2 = {}
      # Remove useless matter before calling the
      # catalog. In particular, consider empty
      # strings as None values
      for cname in kw.keys():
        if kw[cname] != '' and kw[cname]!=None:
          kw2[cname] = kw[cname]
      # The method to call to search the folder
      # content has to be called z_search_folder
      method = self.portal_catalog.countResults
      return method(**kw2)

    # Proxy methods for security reasons
    def getOwnerInfo(self):
      return self.owner_info()

    # Make sure fixConsistency is recursive - ERROR - this creates recursion errors
    # checkConsistency = Folder.checkConsistency
    # fixConsistency = Folder.fixConsistency

    security.declarePublic('getOrderedGlobalActionList')
    def getOrderedGlobalActionList(self, action_list):
      """
      Returns a dictionnary of actions, sorted by type of object

      This should absolutely be rewritten by using clean concepts to separate worklists XXX
      """
      #LOG("getOrderedGlobalActionList", 0, str(action_list))
      sorted_workflow_actions = {}
      sorted_global_actions = []
      other_global_actions = []
      for action in action_list:
        action['disabled'] = 0
        if action.has_key('workflow_title'):
          if not sorted_workflow_actions.has_key(action['workflow_title']):
            sorted_workflow_actions[action['workflow_title']] = []
          sorted_workflow_actions[action['workflow_title']].append(action)
        else:
          other_global_actions.append(action)
      workflow_title_list = sorted_workflow_actions.keys()
      workflow_title_list.sort()
      for key in workflow_title_list:
        sorted_global_actions.append({'title': key, 'disabled': 1})
        sorted_global_actions.extend(sorted_workflow_actions[key])
      sorted_global_actions.append({'title': 'Others', 'disabled': 1})
      sorted_global_actions.extend(other_global_actions)
      return sorted_global_actions

    def setupDefaultProperties(self, p, title, description,
                               email_from_address, email_from_name,
                               validate_email
                               ):
        CMFSite.setupDefaultProperties(self, p, title, description,
                               email_from_address, email_from_name,
                               validate_email)

    # Portal methods are based on the concept of having portal-specific parameters
    # for customization. In the past, we used global parameters, but it was not very good
    # because it was very difficult to customize the settings for each portal site.
    def _getPortalConfiguration(self, id):
      """
        Get a portal-specific configuration.

        Current implementation is using properties in a portal object.
        If not found, try to get a default value for backward compatibility.

        This implementation can be improved by gathering information from appropriate places,
        such as portal_types, portal_categories and portal_workflow.
      """
      if self.hasProperty(id):
        return self.getProperty(id)

      # Fall back to the default.
      return getattr(ERP5Defaults, id, None)

    def _getPortalGroupedTypeList(self, group):
      """Return a list of portal types classified to a specific group.
      """
      def getTypeList(group):
        type_list = []
        for pt in self.portal_types.objectValues():
          if group in getattr(pt, 'group_list', ()):
            type_list.append(pt.getId())
        return tuple(type_list)

      getTypeList = CachingMethod(getTypeList,
          id=('_getPortalGroupedTypeList', group), cache_duration=3600)
      return getTypeList(group)

    def _getPortalGroupedCategoryList(self, group):
      """Return a list of base categories classified to a specific group.
      """
      def getCategoryList(group):
        category_list = []
        for bc in self.portal_categories.objectValues():
          if group in bc.getCategoryTypeList():
            category_list.append(bc.getId())
        return tuple(category_list)

      getCategoryList = CachingMethod(getCategoryList,
            id=('_getPortalGroupedCategoryList', group), cache_duration=3600)
      return getCategoryList(group)

    def _getPortalGroupedStateList(self, group):
      """Return a list of workflow states classified to a specific group.
      """
      def getStateList(group):
        state_dict = {}
        for wf in self.portal_workflow.objectValues():
          if getattr(wf, 'states', None):
            for state in wf.states.objectValues():
              if group in getattr(state, 'type_list', ()):
                state_dict[state.getId()] = None
        return tuple(state_dict.keys())

      getStateList = CachingMethod(getStateList,
          id=('_getPortalGroupedStateList', group), cache_duration=3600)
      return getStateList(group)

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalDefaultSectionCategory')
    def getPortalDefaultSectionCategory(self):
      """
        Return a default section category. This method is deprecated.
      """
      LOG('ERP5Site', 0, 'getPortalDefaultSectionCategory is deprecated;'+
          ' use portal_preferences.getPreferredSectionCategory instead.')
      section_category = self.portal_preferences.getPreferredSectionCategory()

      # XXX This is only for backward-compatibility.
      if not section_category:
        section_category = self._getPortalConfiguration(
                                  'portal_default_section_category')

      return section_category

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalResourceTypeList')
    def getPortalResourceTypeList(self):
      """
        Return resource types.
      """
      return self._getPortalGroupedTypeList('resource') or\
             self._getPortalConfiguration('portal_resource_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalSubVariationTypeList')
    def getPortalSubVariationTypeList(self):
      """
        Return resource types.
      """
      return self._getPortalGroupedTypeList('sub_variation')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalSubVariationBaseCategoryList')
    def getPortalSubVariationBaseCategoryList(self):
      """
        Return variation base categories.
      """
      return self._getPortalGroupedCategoryList('sub_variation')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalVariationTypeList')
    def getPortalVariationTypeList(self):
      """
        Return variation types.
      """
      return self._getPortalGroupedTypeList('variation') or\
             self._getPortalConfiguration('portal_variation_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalNodeTypeList')
    def getPortalNodeTypeList(self):
      """
        Return node types.
      """
      return self._getPortalGroupedTypeList('node') or\
             self._getPortalConfiguration('portal_node_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalPaymentNodeTypeList')
    def getPortalPaymentNodeTypeList(self):
      """
        Return payment node types.
      """
      return self._getPortalGroupedTypeList('payment_node') or\
             self._getPortalConfiguration('portal_payment_node_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalInvoiceTypeList')
    def getPortalInvoiceTypeList(self):
      """
        Return invoice types.
      """
      return self._getPortalGroupedTypeList('invoice') or\
             self._getPortalConfiguration('portal_invoice_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalOrderTypeList')
    def getPortalOrderTypeList(self):
      """
        Return order types.
      """
      return self._getPortalGroupedTypeList('order') or\
             self._getPortalConfiguration('portal_order_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalDeliveryTypeList')
    def getPortalDeliveryTypeList(self):
      """
        Return delivery types.
      """
      return self._getPortalGroupedTypeList('delivery') or\
             self._getPortalConfiguration('portal_delivery_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalTransformationTypeList')
    def getPortalTransformationTypeList(self):
      """
        Return transformation types.
      """
      return self._getPortalGroupedTypeList('transformation') or\
             self._getPortalConfiguration('portal_transformation_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalVariationBaseCategoryList')
    def getPortalVariationBaseCategoryList(self):
      """
        Return variation base categories.
      """
      return self._getPortalGroupedCategoryList('variation') or\
             self._getPortalConfiguration('portal_variation_base_category_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalOptionBaseCategoryList')
    def getPortalOptionBaseCategoryList(self):
      """
        Return option base categories.
      """
      return self._getPortalGroupedCategoryList('option') or\
             self._getPortalConfiguration('portal_option_base_category_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalInvoiceMovementTypeList')
    def getPortalInvoiceMovementTypeList(self):
      """
        Return invoice movement types.
      """
      return self._getPortalGroupedTypeList('invoice_movement') or\
             self._getPortalConfiguration('portal_invoice_movement_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalOrderMovementTypeList')
    def getPortalOrderMovementTypeList(self):
      """
        Return order movement types.
      """
      return self._getPortalGroupedTypeList('order_movement') or\
             self._getPortalConfiguration('portal_order_movement_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalDeliveryMovementTypeList')
    def getPortalDeliveryMovementTypeList(self):
      """
        Return delivery movement types.
      """
      return self._getPortalGroupedTypeList('delivery_movement') or\
             self._getPortalConfiguration('portal_delivery_movement_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                               'getPortalSupplyTypeList')
    def getPortalSupplyTypeList(self):
      """
        Return supply types.
      """
      return self._getPortalGroupedTypeList('supply') or\
             self._getPortalConfiguration('portal_supply_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                               'getPortalSupplyPathTypeList')
    def getPortalSupplyPathTypeList(self):
      """
        Return supply movement types.
      """
      return self._getPortalGroupedTypeList('supply_path') or\
             self._getPortalConfiguration('portal_supply_path_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalAcquisitionMovementTypeList')
    def getPortalAcquisitionMovementTypeList(self):
      """
        Return acquisition movement types.
      """
      return tuple(list(self.getPortalOrderMovementTypeList()) +
                   list(self.getPortalDeliveryMovementTypeList()) +
                   list(self.getPortalInvoiceMovementTypeList()))

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalMovementTypeList')
    def getPortalMovementTypeList(self):
      """
        Return movement types.
      """
      return tuple(list(self.getPortalOrderMovementTypeList()) +
                   list(self.getPortalDeliveryMovementTypeList()) +
                   list(self.getPortalInvoiceMovementTypeList()) +
                   ['Simulation Movement'])

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalSimulatedMovementTypeList')
    def getPortalSimulatedMovementTypeList(self):
      """
        Return simulated movement types.
      """
      return tuple([x for x in self.getPortalMovementTypeList()\
                     if x not in self.getPortalContainerTypeList()])

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalContainerTypeList')
    def getPortalContainerTypeList(self):
      """
        Return container types.
      """
      return self._getPortalGroupedTypeList('container') or\
             self._getPortalConfiguration('portal_container_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalContainerLineTypeList')
    def getPortalContainerLineTypeList(self):
      """
        Return container line types.
      """
      return self._getPortalGroupedTypeList('container_line') or\
             self._getPortalConfiguration('portal_container_line_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalItemTypeList')
    def getPortalItemTypeList(self):
      """
        Return item types.
      """
      return self._getPortalGroupedTypeList('item') or\
             self._getPortalConfiguration('portal_item_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalDiscountTypeList')
    def getPortalDiscountTypeList(self):
      """
        Return discount types.
      """
      return self._getPortalGroupedTypeList('discount') or\
             self._getPortalConfiguration('portal_discount_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalAlarmTypeList')
    def getPortalAlarmTypeList(self):
      """
        Return alarm types.
      """
      return self._getPortalGroupedTypeList('alarm') or\
             self._getPortalConfiguration('portal_alarm_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalPaymentConditionTypeList')
    def getPortalPaymentConditionTypeList(self):
      """
        Return payment condition types.
      """
      return self._getPortalGroupedTypeList('payment_condition') or\
             self._getPortalConfiguration('portal_payment_condition_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalBalanceTransactionLineTypeList')
    def getPortalBalanceTransactionLineTypeList(self):
      """
        Return balance transaction line types.
      """
      return self._getPortalGroupedTypeList('balance_transaction_line') or\
             self._getPortalConfiguration(
                    'portal_balance_transaction_line_type_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalCurrentInventoryStateList')
    def getPortalCurrentInventoryStateList(self):
      """
        Return current inventory states.
      """
      return self._getPortalGroupedStateList('current_inventory') or\
            self._getPortalConfiguration('portal_current_inventory_state_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalDraftOrderStateList')
    def getPortalDraftOrderStateList(self):
      """
        Return draft order states.
      """
      return self._getPortalGroupedStateList('draft_order') or\
             self._getPortalConfiguration('portal_draft_order_state_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalPlannedOrderStateList')
    def getPortalPlannedOrderStateList(self):
      """
        Return planned order states.
      """
      return self._getPortalGroupedStateList('planned_order') or\
             self._getPortalConfiguration('portal_planned_order_state_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalReservedInventoryStateList')
    def getPortalReservedInventoryStateList(self):
      """
        Return reserved inventory states.
      """
      return self._getPortalGroupedStateList('reserved_inventory') or\
          self._getPortalConfiguration('portal_reserved_inventory_state_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalFutureInventoryStateList')
    def getPortalFutureInventoryStateList(self):
      """
        Return future inventory states.
      """
      return self._getPortalGroupedStateList('future_inventory') or\
             self._getPortalConfiguration('portal_future_inventory_state_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalColumnBaseCategoryList')
    def getPortalColumnBaseCategoryList(self):
      """
        Return column base categories.
      """
      return self._getPortalGroupedCategoryList('column') or\
             self._getPortalConfiguration('portal_column_base_category_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalLineBaseCategoryList')
    def getPortalLineBaseCategoryList(self):
      """
        Return line base categories.
      """
      return self._getPortalGroupedCategoryList('line') or\
             self._getPortalConfiguration('portal_line_base_category_list')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPortalTabBaseCategoryList')
    def getPortalTabBaseCategoryList(self):
      """
        Return tab base categories.
      """
      return self._getPortalGroupedCategoryList('tab') or\
             self._getPortalConfiguration('portal_tab_base_category_list')

    def getPortalDefaultGapRoot(self):
      """
        Return the Accounting Plan to use by default (return the root node)
      """
      LOG('ERP5Site', 0, 'getPortalDefaultGapRoot is deprecated;'+
       ' use portal_preferences.getPreferredAccountingTransactionGap instead.')

      return self.portal_preferences.getPreferredAccountingTransactionGap() or\
             self._getPortalConfiguration('portal_default_gap_root')

    def getPortalAccountingMovementTypeList(self) :
      """
        Return accounting movement type list.
      """
      return self._getPortalGroupedTypeList('accounting_movement') or\
          self._getPortalConfiguration('portal_accounting_movement_type_list')

    def getPortalAccountingTransactionTypeList(self) :
      """
        Return accounting transaction movement type list.
      """
      return self._getPortalGroupedTypeList('accounting_transaction') or\
        self._getPortalConfiguration('portal_accounting_transaction_type_list')

    def getPortalAssignmentBaseCategoryList(self):
      """
        Return List of category values to generate security groups.
      """
      ### Here is the filter patch waiting bug #124 to be corrected
      category_list = self._getPortalGroupedCategoryList('assignment') or\
          self._getPortalConfiguration('portal_assignment_base_category_list')
      clean_list = []
      for cat in category_list:
        if cat.find("_btsave") == -1:
          clean_list.append(cat)
      return clean_list

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getDefaultModuleId')
    def getDefaultModuleId(self, portal_type):
      """
        Return default module id where a object with portal_type can
        be created.
      """
      # Very dummy method, but it works with today name convention.
      module_name = portal_type.lower().replace(' ','_')
      portal_object = self
      if not hasattr(portal_object, module_name):
        module_name += '_module'
        if not hasattr(portal_object, module_name):
          LOG('ERP5Site, getDefaultModuleId', 0,
              'Unable to find default module for portal_type: %s' % \
                  portal_type)
          raise ValueError, 'Unable to find module for portal_type: %s' % \
                            portal_type
      return module_name

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getDefaultModule')
    def getDefaultModule(self, portal_type):
      """
        Return default module where a object with portal_type can be created
      """
      return getattr(self, self.getDefaultModuleId(portal_type), None)

    security.declareProtected(Permissions.AddPortalContent, 'newContent')
    def newContent(self, id=None, portal_type=None, immediate_reindex=0, **kw):
      """
        Creates a new content
      """
      if id is None:
        raise ValueError, 'The id should not be None'
      if portal_type is None:
        raise ValueError, 'The portal_type should not be None'
      self.portal_types.constructContent(type_name=portal_type,
                                         container=self,
                                         id=id,
                                         ) # **kw) removed due to CMF bug
      new_instance = self[id]
      if kw is not None: new_instance._edit(force_update=1, **kw)
      if immediate_reindex: new_instance.immediateReindexObject()
      return new_instance

    def log(self,description,content):
      """
      Put a log message
      """
      LOG(description,0,content)


Globals.InitializeClass(ERP5Site)

class ERP5Generator(PortalGenerator):

    klass = ERP5Site

    def getBootstrapDirectory(self):
        """
          Return the name of the bootstrap directory
        """
        product_path = package_home(globals())
        return os.path.join(product_path, 'bootstrap')

    def create(self, parent, id, create_userfolder,
               erp5_sql_connection_type, erp5_sql_connection_string,
               cmf_activity_sql_connection_type,cmf_activity_sql_connection_string,
               reindex=1,**kw):
        LOG('setupTools, create',0,kw)
        id = str(id)
        portal = self.klass(id=id)
        if reindex==0:
          setattr(portal,'isIndexable',0)
        parent._setObject(id, portal)
        # Return the fully wrapped object.
        p = parent.this()._getOb(id)
        p._setProperty('erp5_sql_connection_type', erp5_sql_connection_type, 'string')
        p._setProperty('erp5_sql_connection_string', erp5_sql_connection_string, 'string')
        p._setProperty('cmf_activity_sql_connection_type', cmf_activity_sql_connection_type, 'string')
        p._setProperty('cmf_activity_sql_connection_string', cmf_activity_sql_connection_string, 'string')
        p._setProperty('management_page_charset', 'UTF-8', 'string') # XXX hardcoded charset
        self.setup(p, create_userfolder,**kw)
        return p

    def setupLastTools(self, p, **kw):
        """Set up finals tools
           We want to set the activity tool only at the end to
           make sure that we do not put un the queue the full reindexation
        """
        # Add Activity Tool
        #LOG('setupTools, kw',0,kw)
        if kw.has_key('create_activities') and int(kw['create_activities'])==1:
          if not p.hasObject('portal_activities'):
            addTool = p.manage_addProduct['CMFActivity'].manage_addTool
            addTool('CMF Activity Tool', None) # Allow user to select active/passive
          # Initialize Activities
          portal_activities = getToolByName(p, 'portal_activities', None)
          if portal_activities is not None:
            if kw.get('update', 0):
              keep = 1
            else:
              keep = 0
            portal_activities.manageClearActivities(keep=keep)

    def setupTemplateTool(self, p, **kw):
      """Setup the Template Tool. Security must be set strictly.
      """
      addTool = p.manage_addProduct['ERP5'].manage_addTool
      addTool('ERP5 Template Tool', None)
      context = p.portal_templates
      permission_list = context.possible_permissions()
      for permission in permission_list:
        context.manage_permission(permission, ['Manager'], 0)

    def setupTools(self, p,**kw):
        """Set up initial tools"""

        if not 'portal_actions' in p.objectIds():
          PortalGenerator.setupTools(self, p)

        # It is better to remove portal_catalog which is ZCatalog as soon as possible,
        # because the API is not the completely same as ERP5Catalog, and ZCatalog is
        # useless for ERP5 after all.
        update = kw.get('update', 0)
        portal_catalog = getToolByName(p, 'portal_catalog', None)
        if portal_catalog is not None and portal_catalog.meta_type != 'ZSQLCatalog' and not update:
          p._delObject('portal_catalog')

        # Add CMF Report Tool
        if not p.hasObject('portal_report'):
          addTool = p.manage_addProduct['CMFReportTool'].manage_addTool
          addTool('CMF Report Tool', None)

        # Add ERP5 Tools
        addTool = p.manage_addProduct['ERP5'].manage_addTool
        if not p.hasObject('portal_categories'):
          addTool('ERP5 Categories', None)
        if not p.hasObject('portal_rules'):
          addTool('ERP5 Rule Tool', None)
        if not p.hasObject('portal_ids'):
          addTool('ERP5 Id Tool', None)
        if not p.hasObject('portal_simulation'):
          addTool('ERP5 Simulation Tool', None)
        if not p.hasObject('portal_templates'):
          self.setupTemplateTool(p)
        if not p.hasObject('portal_trash'):
          addTool('ERP5 Trash Tool', None)
        if not p.hasObject('portal_alarms'):
          addTool('ERP5 Alarm Tool', None)
        if not p.hasObject('portal_domains'):
          addTool('ERP5 Domain Tool', None)
        if not p.hasObject('portal_deliveries'):
          addTool('ERP5 Delivery Tool', None)
        if not p.hasObject('portal_orders'):
          addTool('ERP5 Order Tool', None)

        # Add ERP5Type Tools
        addTool = p.manage_addProduct['ERP5Type'].manage_addTool
        if not p.hasObject('portal_classes'):
          if allowClassTool():
            addTool('ERP5 Class Tool', None)
          else:
            addTool('ERP5 Dummy Class Tool', None)

        # Add ERP5 SQL Catalog Tool
        addTool = p.manage_addProduct['ERP5Catalog'].manage_addTool
        if not p.hasObject('portal_catalog'):
          addTool('ERP5 Catalog', None)
        # Add Default SQL connection
        if p.erp5_sql_connection_type == 'Z MySQL Database Connection':
          if not p.hasObject('erp5_sql_connection'):
            addSQLConnection = p.manage_addProduct['ZSQLMethods'].manage_addZMySQLConnection
            addSQLConnection('erp5_sql_connection', 'ERP5 SQL Server Connection', p.erp5_sql_connection_string)
        elif p.erp5_sql_connection_type == 'Z Gadfly':
          pass
        if p.cmf_activity_sql_connection_type == 'Z MySQL Database Connection':
          if not p.hasObject('cmf_activity_sql_connection'):
            addSQLConnection = p.manage_addProduct['ZSQLMethods'].manage_addZMySQLConnection
            addSQLConnection('cmf_activity_sql_connection', 'CMF Activity SQL Server Connection', p.cmf_activity_sql_connection_string)
        elif p.cmf_activity_sql_connection_type == 'Z Gadfly':
          pass
        # Create default methods in Catalog XXX
        portal_catalog = getToolByName(p, 'portal_catalog')
        if not portal_catalog.getSQLCatalog('erp5_mysql') and not update:
            # FIXME: addDefaultSQLMethods should be removed.
            portal_catalog.addDefaultSQLMethods('erp5_mysql')

            # Clear Catalog
            portal_catalog.manage_catalogClear()

        # Add ERP5Form Tools
        addTool = p.manage_addProduct['ERP5Form'].manage_addTool
        if not p.hasObject('portal_selections'):
          addTool('ERP5 Selections', None)
        if not p.hasObject('portal_preferences'):
          addTool('ERP5 Preference Tool', None)

        # Add ERP5SyncML Tools
        addTool = p.manage_addProduct['ERP5SyncML'].manage_addTool
        if not p.hasObject('portal_synchronizations'):
          addTool('ERP5 Synchronizations', None)

        # Add Message Catalog
        #if 'Localizer' in p.objectIds():
          #p._delObject('Localizer') # Why delete it, we should keep for ERP5/CPS
        if not 'Localizer' in p.objectIds():
          #p._delObject('Localizer') # Why delete it, we should keep for ERP5/CPS
          addLocalizer = p.manage_addProduct['Localizer'].manage_addLocalizer
          addLocalizer('', ('en',))
        localizer = getToolByName(p, 'Localizer')
        addMessageCatalog = localizer.manage_addProduct['Localizer'].manage_addMessageCatalog
        if 'erp5_ui' not in localizer.objectIds():
          if 'default' in localizer.objectIds():
            localizer.manage_delObjects('default')
          addMessageCatalog('default', 'ERP5 Localized Messages', ('en',))
          addMessageCatalog('erp5_ui', 'ERP5 Localized Interface', ('en',))
          addMessageCatalog('erp5_content', 'ERP5 Localized Content', ('en',))


    def setupMembersFolder(self, p):
        """
          ERP5 is not a CMS
        """
        pass

    def setupDefaultSkins(self, p):
        from Products.CMFCore.DirectoryView import addDirectoryViews
        from Products.CMFDefault import cmfdefault_globals
        from Products.CMFActivity import cmfactivity_globals
        ps = getToolByName(p, 'portal_skins')
        # Do not use filesystem skins for ERP5 any longer.
        # addDirectoryViews(ps, 'skins', globals())
        # addDirectoryViews(ps, path.join('skins','pro'), globals())
        addDirectoryViews(ps, 'skins', cmfdefault_globals)
        addDirectoryViews(ps, 'skins', cmfactivity_globals)
        ps.manage_addProduct['OFSP'].manage_addFolder(id='external_method')
        ps.manage_addProduct['OFSP'].manage_addFolder(id='custom')
        # set the 'custom' layer a high priority, so it remains the first
        # layer when installing new business templates
        ps['custom'].manage_addProperty(
            "business_template_skin_layer_priority", 100.0, "float")
        ps.addSkinSelection('View', 'custom, external_method, activity, '
                                  + 'zpt_content, zpt_generic,'
                                  + 'zpt_control, content, generic, control, Images',
                            make_default=1)
        ps.addSkinSelection('Print', 'custom, external_method, activity, '
                                  + 'zpt_content, zpt_generic,'
                                  + 'zpt_control, content, generic, control, Images',
                            make_default=0)
        ps.addSkinSelection('CSV', 'custom, external_method, activity, '
                                  + 'zpt_content, zpt_generic,'
                                  + 'zpt_control, content, generic, control, Images',
                            make_default=0)
        p.setupCurrentSkin()

    def setupWorkflow(self, p):
        """
          Set up workflows for business templates
        """
        tool = getToolByName(p, 'portal_workflow', None)
        if tool is None:
            return
        for wf_id in ('business_template_building_workflow', 'business_template_installation_workflow'):
          if wf_id in tool.objectIds():
            tool.manage_delObjects([wf_id])
        bootstrap_dir = self.getBootstrapDirectory()
        business_template_building_workflow = os.path.join(bootstrap_dir,
                                                           'business_template_building_workflow.xml')
        tool._importObjectFromFile(business_template_building_workflow)
        business_template_installation_workflow = os.path.join(bootstrap_dir,
                                                               'business_template_installation_workflow.xml')
        tool._importObjectFromFile(business_template_installation_workflow)
        tool.setChainForPortalTypes( ( 'Business Template', ),
                                     ( 'business_template_building_workflow',
                                       'business_template_installation_workflow' ) )
        pass

    def setupIndex(self, p, **kw):
        # Make sure all tools and folders have been indexed
        if kw.has_key('reindex') and kw['reindex']==0:
          return
        skins_tool = getToolByName(p, 'portal_skins', None)
        if skins_tool is None:
          return
        portal_catalog = p.portal_catalog
        portal_catalog.manage_catalogClear()
        skins_tool["erp5_core"].ERP5Site_reindexAll()

    def setupUserFolder(self, p):
        # We use if possible ERP5Security, then NuxUserGroups
        try:
          from Products import ERP5Security
          from Products import PluggableAuthService
        except ImportError:
          ERP5Security = None
          try:
            import Products.NuxUserGroups
            withnuxgroups = 1
          except:
            withnuxgroups = 0
        if ERP5Security is not None:
          # Use Pluggable Auth Service instead of the standard acl_users.
          p.manage_addProduct['PluggableAuthService'].addPluggableAuthService()
          # Add legacy ZODB support
          p.acl_users.manage_addProduct['PluggableAuthService'].addZODBUserManager('zodb_users')
          p.acl_users.manage_addProduct['PluggableAuthService'].addZODBGroupManager('zodb_groups')
          p.acl_users.manage_addProduct['PluggableAuthService'].addZODBRoleManager('zodb_roles')
          # Add CMF Portal Roles
          #XXX Maybe it will no longer be required once PAS is the standard
          p.acl_users.zodb_roles.addRole('Member')
          p.acl_users.zodb_roles.addRole('Reviewer')
          # Register ZODB Interface
          p.acl_users.zodb_users.manage_activateInterfaces(('IAuthenticationPlugin',
                                                        'IUserEnumerationPlugin','IUserAdderPlugin'))
          p.acl_users.zodb_groups.manage_activateInterfaces(('IGroupsPlugin',
                                                        'IGroupEnumerationPlugin'))
          p.acl_users.zodb_roles.manage_activateInterfaces(('IRoleEnumerationPlugin',
                                                        'IRolesPlugin', 'IRoleAssignerPlugin'))
          # Add ERP5UserManager
          p.acl_users.manage_addProduct['ERP5Security'].addERP5UserManager('erp5_users')
          p.acl_users.manage_addProduct['ERP5Security'].addERP5GroupManager('erp5_groups')
          p.acl_users.manage_addProduct['ERP5Security'].addERP5RoleManager('erp5_roles')
          # Register ERP5UserManager Interface
          p.acl_users.erp5_users.manage_activateInterfaces(('IAuthenticationPlugin',
                                                            'IUserEnumerationPlugin',))
          p.acl_users.erp5_groups.manage_activateInterfaces(('IGroupsPlugin',))
          p.acl_users.erp5_roles.manage_activateInterfaces(('IRolesPlugin',))
        elif withnuxgroups:
          # NuxUserGroups user folder
          p.manage_addProduct['NuxUserGroups'].addUserFolderWithGroups()
        else:
          # Standard user folder
          PortalGenerator.setupUserFolder(self, p)

    def setupPermissions(self, p):
      permission_dict = {
        'Access Transient Objects'     : ('Manager', 'Anonymous'),
        'Access contents information'  : ('Manager', 'Member', 'Anonymous'),
        'Access future portal content' : ('Manager', 'Reviewer'),
        'Access session data'          : ('Manager', 'Anonymous'),
        'AccessContentsInformation'    : ('Manager', 'Member'),
        'Add portal content'           : ('Manager', 'Owner'),
        'Add portal folders'           : ('Manager', 'Owner'),
        'Delete objects'               : ('Manager', 'Owner'),
        'FTP access'                   : ('Manager', 'Owner'),
        'List folder contents'         : ('Manager', 'Member'),
        'List portal members'          : ('Manager', 'Member'),
        'List undoable changes'        : ('Manager', 'Member'),
        'Manage properties'            : ('Manager', 'Owner'),
        'Modify portal content'        : ('Manager', 'Owner'),
        'Reply to item'                : ('Manager', 'Member'),
        'Review portal content'        : ('Manager', 'Reviewer'),
        'Search ZCatalog'              : ('Manager', 'Member'),
        'Set own password'             : ('Manager', 'Member'),
        'Set own properties'           : ('Manager', 'Member'),
        'Undo changes'                 : ('Manager', 'Owner'),
        'View'                         : ('Manager', 'Member', 'Owner', 'Anonymous'),
        'View management screens'      : ('Manager', 'Owner')
      }

      for permission in p.ac_inherited_permissions(1):
        name = permission[0]
        role_list = permission_dict.get(name, ('Manager',))
        p.manage_permission(name, roles=role_list, acquire=0)

    def setup(self, p, create_userfolder, **kw):
        update = kw.get('update', 0)

        self.setupTools(p, **kw)

        if not p.hasObject('MailHost'):
          self.setupMailHost(p)

        if int(create_userfolder) != 0 and not p.hasObject('acl_users'):
            self.setupUserFolder(p)

        if not p.hasObject('cookie_authentication'):
          self.setupCookieAuth(p)

        if 'Member' not in getattr(p, '__ac_roles__', ()):
          self.setupRoles(p)

        if not update:
          self.setupPermissions(p)
          self.setupDefaultSkins(p)

        self.setupLastTools(p, **kw)

        # Finish setup
        if not p.hasObject('Members'):
          self.setupMembersFolder(p)

        # ERP5 Design Choice is that all content should be user defined
        # Content is disseminated through business templates
        self.setupBusinessTemplate(p)

        if not p.hasObject('content_type_registry'):
          self.setupMimetypes(p)
        if not update:
          self.setupWorkflow(p)

        if not update:
          self.setupERP5Core(p,**kw)

        # Make sure tools are cleanly indexed with a uid before creating children
        # XXX for some strange reason, member was indexed 5 times
        if not update:
          self.setupIndex(p, **kw)

    def setupBusinessTemplate(self,p):
        """
        Install the portal_type of Business Template
        """
        tool = getToolByName(p, 'portal_types', None)
        if tool is None:
          return
        if 'Business Template' not in tool.objectIds():
          t = BusinessTemplate.factory_type_information
          ti = apply(ERP5TypeInformation, (), t)
          tool._setObject(t['id'], ti)

    def setupERP5Core(self,p,**kw):
        """
        Install the core part of ERP5
        """
        template_tool = getToolByName(p, 'portal_templates', None)
        if template_tool is None:
          return
        if template_tool.getInstalledBusinessTemplate('erp5_core') is None:
          bootstrap_dir = self.getBootstrapDirectory()
          template = os.path.join(bootstrap_dir, 'erp5_core')
          if not os.path.exists(template):
            template = os.path.join(bootstrap_dir, 'erp5_core.bt5')

          id = template_tool.generateNewId()
          template_tool.download(template, id=id)
          template_tool[id].install(**kw)

# Patch the standard method
CMFSite.getPhysicalPath = ERP5Site.getPhysicalPath
