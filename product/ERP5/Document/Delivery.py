##############################################################################
#
# Copyright (c) 2002, 2005 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#                    Romain Courteaud <romain@nexedi.com>
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

from Globals import InitializeClass, PersistentMapping
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowMethod
from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5Type.XMLObject import XMLObject
from Products.ERP5Type.Base import Base
from Products.ERP5.Document.DeliveryCell import DeliveryCell
from Acquisition import Explicit, Implicit
from Products.PythonScripts.Utility import allow_class
from DateTime import DateTime

from zLOG import LOG

class Delivery(XMLObject):
    """
        Each time delivery is modified, it MUST launch a reindexing of
        inventories which are related to the resources contained in the Delivery
    """
    # CMF Type Definition
    meta_type = 'ERP5 Delivery'
    portal_type = 'Delivery'
    isPortalContent = 1
    isRADContent = 1
    isDelivery = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.View)

    # Default Properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      , PropertySheet.Task
                      , PropertySheet.Arrow
                      , PropertySheet.Movement
                      , PropertySheet.Delivery
                      , PropertySheet.Reference
                      )

    security.declareProtected(Permissions.AccessContentsInformation, 'isAccountable')
    def isAccountable(self):
      """
        Returns 1 if this needs to be accounted
        Only account movements which are not associated to a delivery
        Whenever delivery is there, delivery has priority
      """
      return 1

    # Pricing methods
    def _getTotalPrice(self, context):
      return 2.0

    def _getDefaultTotalPrice(self, context):
      return 3.0

    def _getSourceTotalPrice(self, context):
      return 4.0

    def _getDestinationTotalPrice(self, context):
      return 5.0

    security.declareProtected(Permissions.AccessContentsInformation, 'getDefaultTotalPrice')
    def getDefaultTotalPrice(self, context=None, REQUEST=None, **kw):
      """
      """
      return self._getDefaultTotalPrice(self.asContext(context=context, REQUEST=REQUEST, **kw))

    security.declareProtected(Permissions.AccessContentsInformation, 'getSourceTotalPrice')
    def getSourceTotalPrice(self, context=None, REQUEST=None, **kw):
      """
      """
      return self._getSourceTotalPrice(self.asContext(context=context, REQUEST=REQUEST, **kw))

    security.declareProtected(Permissions.AccessContentsInformation, 'getDestinationTotalPrice')
    def getDestinationTotalPrice(self, context=None, REQUEST=None, **kw):
      """
      """
      return self._getDestinationTotalPrice(self.asContext(context=context, REQUEST=REQUEST, **kw))

    # Pricing
    security.declareProtected( Permissions.ModifyPortalContent, 'updatePrice' )
    def updatePrice(self):
      for c in self.objectValues():
        if hasattr(aq_base(c), 'updatePrice'):
          c.updatePrice()

    security.declareProtected(Permissions.AccessContentsInformation, 'getTotalPrice')
    def getTotalPrice(self,  src__=0, **kw):
      """
        Returns the total price for this order
      """
      kw['explanation_uid'] = self.getUid()
      kw.update(self.portal_catalog.buildSQLQuery(**kw))
      if src__:
        return self.Delivery_zGetTotal(src__=1, **kw)
      aggregate = self.Delivery_zGetTotal(**kw)[0]
      return aggregate.total_price or 0

    security.declareProtected(Permissions.AccessContentsInformation, 'getTotalQuantity')
    def getTotalQuantity(self, src__=0, **kw):
      """
        Returns the quantity if no cell or the total quantity if cells
      """
      kw['explanation_uid'] = self.getUid()
      kw.update(self.portal_catalog.buildSQLQuery(**kw))
      if src__:
        return self.Delivery_zGetTotal(src__=1, **kw)
      aggregate = self.Delivery_zGetTotal(**kw)[0]
      return aggregate.total_quantity or 0

    security.declareProtected(Permissions.AccessContentsInformation, 'getDeliveryUid')
    def getDeliveryUid(self):
      return self.getUid()

    security.declareProtected(Permissions.AccessContentsInformation, 'getDeliveryValue')
    def getDeliveryValue(self):
      """
      Deprecated, we should use getRootDeliveryValue instead
      """
      return self

    security.declareProtected(Permissions.AccessContentsInformation, 'getRootDeliveryValue')
    def getRootDeliveryValue(self):
      """
      This method returns the delivery, it is usefull to retrieve the delivery
      from a line or a cell
      """
      return self

    security.declareProtected(Permissions.AccessContentsInformation, 'getDelivery')
    def getDelivery(self):
      return self.getRelativeUrl()

    security.declareProtected(Permissions.AccessContentsInformation,
                             'getMovementList')
    def getMovementList(self, portal_type=None, **kw):
      """
        Return a list of movements.
      """
      if portal_type is None:
        portal_type = self.getPortalMovementTypeList()
      movement_list = []
      for m in self.contentValues(filter={'portal_type': portal_type}):
        if m.hasCellContent():
          for c in m.contentValues(filter={'portal_type': portal_type}):
            movement_list.append(c)
        else:
          movement_list.append(m)
      return movement_list

    security.declareProtected(Permissions.AccessContentsInformation, 'getSimulatedMovementList')
    def getSimulatedMovementList(self):
      """
        Return a list of simulated movements.
        This does not contain Container Line or Container Cell.
      """
      return self.getMovementList(portal_type=self.getPortalSimulatedMovementTypeList())

    security.declareProtected(Permissions.AccessContentsInformation, 'getInvoiceMovementList')
    def getInvoiceMovementList(self):
      """
        Return a list of simulated movements.
        This does not contain Container Line or Container Cell.
      """
      return self.getMovementList(portal_type=self.getPortalInvoiceMovementTypeList())

    security.declareProtected(Permissions.AccessContentsInformation, 'getContainerList')
    def getContainerList(self):
      """
        Return a list of root containers.
        This does not contain sub-containers.
      """
      container_list = []
      for m in self.contentValues(filter={'portal_type': self.getPortalContainerTypeList()}):
        container_list.append(m)
      return container_list

    def applyToDeliveryRelatedMovement(self, portal_type='Simulation Movement', method_id = 'expand'):
      for my_simulation_movement in self.getDeliveryRelatedValueList(
                                                portal_type = 'Simulation Movement'):
          # And apply
          getattr(my_simulation_movement.getObject(), method_id)()
      for m in self.contentValues(filter={'portal_type': self.getPortalMovementTypeList()}):
        # Find related in simulation
        for my_simulation_movement in m.getDeliveryRelatedValueList(
                                                portal_type = 'Simulation Movement'):
          # And apply
          getattr(my_simulation_movement.getObject(), method_id)()
        for c in m.contentValues(filter={'portal_type': 'Delivery Cell'}):
          for my_simulation_movement in c.getDeliveryRelatedValueList(
                                                portal_type = 'Simulation Movement'):
            # And apply
            getattr(my_simulation_movement.getObject(), method_id)()


    #######################################################
    # Causality computation
    security.declareProtected(Permissions.View, 'isConvergent')
    def isConvergent(self,**kw):
      """
        Returns 0 if the target is not met
      """
      return int(not self.isDivergent(**kw))

    security.declareProtected(Permissions.View, 'isSimulated')
    def isSimulated(self):
      """
        Returns 1 if all movements have a delivery or order counterpart
        in the simulation
      """
      #LOG('Delivery.isSimulated getMovementList',0,self.getMovementList())
      for m in self.getMovementList():
        #LOG('Delivery.isSimulated m',0,m.getPhysicalPath())
        #LOG('Delivery.isSimulated m.isSimulated',0,m.isSimulated())
        if not m.isSimulated():
          #LOG('Delivery.isSimulated m.getQuantity',0,m.getQuantity())
          #LOG('Delivery.isSimulated m.getSimulationQuantity',0,m.getSimulationQuantity())
          if m.getQuantity() != 0.0 or m.getSimulationQuantity() != 0:
            return 0
          # else Do we need to create a simulation movement ? XXX probably not
      return 1

    security.declareProtected(Permissions.View, 'isDivergent')
    def isDivergent(self,fast=0,**kw):
      """
        Returns 1 if the target is not met according to the current information
        After and edit, the isOutOfTarget will be checked. If it is 1,
        a message is emitted

        emit targetUnreachable !
      """
      # Delivery_zIsDivergent only works when object and simulation is
      # reindexed, so if an user change the delivery, he must wait
      # until everything is indexed, this is not acceptable for users
      # so we should not use it by default (and may be we should remove)
      if fast==1 and len(self.Delivery_zIsDivergent(uid=self.getUid())) > 0:
        return 1
      # Check if the total quantity equals the total of each simulation movement quantity
      for movement in self.getMovementList():
        if movement.isDivergent():
          return 1
      return 0

    def updateCausalityState(self,**kw):
      """
      This is often called as an activity, it will check if the
      deliver is convergent, and if so it will put the delivery
      in a solved state, if not convergent in a diverged state
      """
      if hasattr(self,'diverge') and hasattr(self,'converge'):
        if self.isDivergent():
          self.diverge()
        else:
          self.converge()

    #######################################################
    # Defer indexing process
    def reindexObject(self, *k, **kw):
      """
        Reindex children and simulation
      """
      self.recursiveReindexObject()
      # NEW: we never rexpand simulation - This is a task for DSolver / TSolver
      # Make sure expanded simulation is still OK (expand and reindex)
      # self.activate().applyToDeliveryRelatedMovement(method_id = 'expand')

    #######################################################
    # Stock Management
    def _getMovementResourceList(self):
      resource_dict = {}
      for m in self.contentValues(filter={'portal_type': self.getPortalMovementTypeList()}):
        r = m.getResource()
        if r is not None:
          resource_dict[r] = 1
      return resource_dict.keys()

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventory')
    def getInventory(self, **kw):
      """
      Returns inventory
      """
      kw['resource'] = self._getMovementResourceList()
      return self.portal_simulation.getInventory(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getCurrentInventory')
    def getCurrentInventory(self, **kw):
      """
      Returns current inventory
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getCurrentInventory(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getAvailableInventory')
    def getAvailableInventory(self, **kw):
      """
      Returns available inventory
      (current inventory - deliverable)
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getAvailableInventory(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getFutureInventory')
    def getFutureInventory(self, **kw):
      """
      Returns inventory at infinite
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getFutureInventory(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventoryList')
    def getInventoryList(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getInventoryList(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getCurrentInventoryList')
    def getCurrentInventoryList(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getCurrentInventoryList(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getFutureInventoryList')
    def getFutureInventoryList(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getFutureInventoryList(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventoryStat')
    def getInventoryStat(self, **kw):
      """
      Returns statistics of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getInventoryStat(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getCurrentInventoryStat')
    def getCurrentInventoryStat(self, **kw):
      """
      Returns statistics of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getCurrentInventoryStat(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getFutureInventoryStat')
    def getFutureInventoryStat(self, **kw):
      """
      Returns statistics of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getFutureInventoryStat(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventoryChart')
    def getInventoryChart(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getInventoryChart(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getCurrentInventoryChart')
    def getCurrentInventoryChart(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getCurrentInventoryChart(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getFutureInventoryChart')
    def getFutureInventoryChart(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getFutureInventoryChart(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventoryHistoryList')
    def getInventoryHistoryList(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getInventoryHistoryList(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventoryHistoryChart')
    def getInventoryHistoryChart(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getInventoryHistoryChart(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getMovementHistoryList')
    def getMovementHistoryList(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getMovementHistoryList(**kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getMovementHistoryStat')
    def getMovementHistoryStat(self, **kw):
      """
      Returns list of inventory grouped by section or site
      """
      kw['category'] = self._getMovementResourceList()
      return self.portal_simulation.getMovementHistoryStat(**kw)

    security.declarePrivate( '_edit' )
    def _edit(self, REQUEST=None, force_update = 0, **kw):
      """
      call propagateArrowToSimulation
      """
      XMLObject._edit(self,REQUEST=REQUEST,force_update=force_update,**kw)
      #self.propagateArrowToSimulation()
      # We must expand our applied rule only if not confirmed
      #if self.getSimulationState() in planned_order_state:
      #  self.updateAppliedRule() # This should be implemented with the interaction tool rather than with this hard coding

    security.declareProtected(Permissions.ModifyPortalContent, 'notifySimulationChange')
    def notifySimulationChange(self):
      """
        WorkflowMethod used to notify the causality workflow that the simulation
        has changed, so we have to check if the delivery is divergent or not
      """
      pass
    notifySimulationChange = WorkflowMethod(notifySimulationChange)

    ##########################################################################
    # Applied Rule stuff
    def updateAppliedRule(self, rule_id):
      """
        Create a new Applied Rule is none is related, or call expand
        on the existing one.
      """
      if (rule_id is not None) and\
         (self.getSimulationState() not in \
                                       self.getPortalDraftOrderStateList()):
        # Nothing to do if we are already simulated
        self._createAppliedRule(rule_id)

    def _createAppliedRule(self, rule_id):
      """
        Create a new Applied Rule is none is related, or call expand
        on the existing one.
      """
      # Return if draft or cancelled simulation_state
      if self.getSimulationState() in ('cancelled',):
        # The applied rule should be cleaned up 
        # ie. empty all movements which have no confirmed children
        return
      # Otherwise, expand
      # Look up if existing applied rule
      my_applied_rule_list = self.getCausalityRelatedValueList(\
                                            portal_type='Applied Rule')
      if len(my_applied_rule_list) == 0:
        if self.isSimulated(): 
          # No need to create a DeliveryRule 
          # if we are already in the simulation process
          return 
        # Create a new applied order rule (portal_rules.order_rule)
        portal_rules = getToolByName(self, 'portal_rules')
        portal_simulation = getToolByName(self, 'portal_simulation')
        my_applied_rule = portal_rules[rule_id].\
                                    constructNewAppliedRule(portal_simulation)
        # Set causality
        my_applied_rule.setCausalityValue(self)
        # We must make sure this rule is indexed
        # now in order not to create another one later
        my_applied_rule.reindexObject()
      elif len(my_applied_rule_list) == 1:
        # Re expand the rule if possible
        my_applied_rule = my_applied_rule_list[0]
      else:
        raise "SimulationError", 'Delivery %s has more than one applied'\
                                 ' rule.' % self.getRelativeUrl()

      # We are now certain we have a single applied rule
      # It is time to expand it
      self.activate(
        after_path_and_method_id=(
                my_applied_rule.getPath(),
               ['immediateReindexObject', 'recursiveImmediateReindexObject'])
        ).expand(my_applied_rule.getId())

    security.declareProtected(Permissions.ModifyPortalContent, 'expand')
    def expand(self, applied_rule_id, force=0, **kw):
      """
        Reexpand applied rule
      """
      my_applied_rule = self.portal_simulation.get(applied_rule_id, None)
      if my_applied_rule is not None:
        my_applied_rule.expand(force=force, **kw)
      else:
        LOG("ERP5 Error:", 100,
            "Could not expand applied rule %s for delivery %s" %\
                (applied_rule_id, self.getId()))

