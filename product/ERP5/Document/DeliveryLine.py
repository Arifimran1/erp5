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

from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5Type.XMLMatrix import XMLMatrix
from Products.ERP5Type.XMLObject import XMLObject

from Products.ERP5.Document.Movement import Movement
from Products.ERP5.Variated import Variated
from Products.ERP5.Document.ImmobilisationMovement import ImmobilisationMovement

from zLOG import LOG

class DeliveryLine(Movement, XMLObject, XMLMatrix, Variated, 
                   ImmobilisationMovement):
    """
      A DeliveryLine object allows to implement lines in
      Deliveries (packing list, order, invoice, etc.)

      It may include a price (for insurance, for customs, for invoices,
      for orders)
    """

    meta_type = 'ERP5 Delivery Line'
    portal_type = 'Delivery Line'

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Declarative interfaces
    __implements__ = ( Interface.Variated, )

    # Declarative properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.Amount
                      , PropertySheet.Task
                      , PropertySheet.Arrow
                      , PropertySheet.Movement
                      , PropertySheet.Price
                      , PropertySheet.VariationRange
                      , PropertySheet.ItemAggregation
                      )

    # Multiple inheritance definition
    updateRelatedContent = XMLMatrix.updateRelatedContent

    # Explicit acquisition of aq_dynamic generated method
    security.declareProtected(Permissions.AccessContentsInformation,
                              'getSimulationState')
    def getSimulationState(self):
      """
        Explicitly acquire simulation_state from parent
      """
      method = getattr(self.getParentValue(),'getSimulationState', None)
      if method is not None:
        return method()
    
    # Force in _edit to modify variation_base_category_list first
    security.declarePrivate( '_edit' )
    def _edit(self, REQUEST=None, force_update = 0, **kw):
      # XXX FIXME For now, special cases are handled in _edit methods in many
      # documents : DeliveryLine, DeliveryCell ... Ideally, to prevent code
      # duplication, it should be handled in a _edit method present only in
      # Amount.py

      # If variations and resources are set at the same time, resource must be
      # set before any variation.
      if kw.has_key('resource_value'):
        self._setResourceValue( kw['resource_value'] )
      # We must first prepare the variation_base_category_list before we do the edit of the rest
      #LOG('in edit', 0, str(kw))
      if kw.has_key('variation_base_category_list'):
        self._setVariationBaseCategoryList( kw['variation_base_category_list'] )
      if kw.has_key('variation_category_list'):
        self._setVariationCategoryList( kw['variation_category_list'] )
      Movement._edit(self, REQUEST=REQUEST,
                       force_update = force_update, **kw)
      # This one must be the last
      if kw.has_key('item_id_list'):
        self._setItemIdList( kw['item_id_list'] )

    # We must check if the user has changed the resource of particular line
    security.declareProtected( Permissions.ModifyPortalContent, 'edit' )
    def edit(self, REQUEST=None, force_update = 0, reindex_object=1, **kw):
      return self._edit(REQUEST=REQUEST, force_update=force_update, reindex_object=reindex_object, **kw)

    security.declareProtected(Permissions.AccessContentsInformation, 
                              'isAccountable')
    def isAccountable(self):
      """
        Returns 1 if this needs to be accounted
        Only account movements which are not associated to a delivery
        Whenever delivery is there, delivery has priority
      """
      return self.aq_parent.isAccountable() and (not self.hasCellContent())

    def _getTotalPrice(self, context, fast=1):
      """ Returns the total price for this line or the cells it contains. """
      base_id = 'movement'
      if not self.hasCellContent(base_id=base_id):
        quantity = self.getQuantity() or 0.0
        price = self.getPrice(context=context) or 0.0
        return quantity * price
      else:
        if fast : # Use MySQL
          aggregate = self.DeliveryLine_zGetTotal()[0]
          return aggregate.total_price or 0.0
        return sum([ ( (cell.getQuantity() or 0) *
                       (cell.getPrice(context=context) or 0))
                        for cell in self.getCellValueList()])

    security.declareProtected( Permissions.AccessContentsInformation,
                               'getTotalQuantity')
    def getTotalQuantity(self, fast=1):
      """
        Returns the quantity if no cell or the total quantity if cells
      """
      base_id = 'movement'
      if not self.hasCellContent(base_id=base_id):
        return self.getQuantity()
      else:
        if fast : # Use MySQL
          aggregate = self.DeliveryLine_zGetTotal()[0]
          return aggregate.total_quantity or 0.0
        return sum([cell.getQuantity() for cell in self.getCellValueList()])

    security.declareProtected(Permissions.AccessContentsInformation,
                              'hasCellContent')
    def hasCellContent(self, base_id='movement'):
      """Return true if the object contains cells.
      """
      # Do not use XMLMatrix.hasCellContent, because it can generate
      # inconsistency in catalog
      # Exemple: define a line and set the matrix cell range, but do not create
      # cell.
      # Line was in this case consider like a movement, and was catalogued.
      # But, getVariationText of the line was not empty.
      # So, in ZODB, resource as without variation, but in catalog, this was
      # the contrary...
      cell_range = XMLMatrix.getCellRange(self, base_id=base_id)
      return (cell_range is not None and len(cell_range) > 0)
      # DeliveryLine can be a movement when it does not content any cell and 
      # matrix cell range is not empty.
      # Better implementation is needed.
      # We want to define a line without cell, defining a variated resource.
      # If we modify the cell range, we need to move the quantity to a new
      # cell, which define the same variated resource.
#       return XMLMatrix.hasCellContent(self, base_id=base_id)

    security.declareProtected( Permissions.AccessContentsInformation, 'getCellValueList' )
    def getCellValueList(self, base_id='movement'):
      """
          This method can be overriden
      """
      return XMLMatrix.getCellValueList(self, base_id=base_id)

    security.declareProtected( Permissions.View, 'getCell' )
    def getCell(self, *kw , **kwd):
      """
          This method can be overriden
      """
      if 'base_id' not in kwd:
        kwd['base_id'] = 'movement'

      return XMLMatrix.getCell(self, *kw, **kwd)

    security.declareProtected( Permissions.ModifyPortalContent, 'newCell' )
    def newCell(self, *kw, **kwd):
      """
          This method creates a new cell
      """
      if 'base_id' not in kwd:
        kwd['base_id'] = 'movement'

      return XMLMatrix.newCell(self, *kw, **kwd)

    security.declareProtected(Permissions.View, 'isDivergent')
    def isDivergent(self):
      """
        Returns 1 if the target is not met according to the current information
        After and edit, the isOutOfTarget will be checked. If it is 1,
        a message is emitted

        emit targetUnreachable !
      """
      if self.hasCellContent():
        for cell in self.contentValues(filter={'portal_type': self.getPortalDeliveryMovementTypeList()}):
          if cell.isDivergent():
            return 1
      else:
         return Movement.isDivergent(self)

    def applyToDeliveryLineRelatedMovement(self, portal_type='Simulation Movement', method_id = 'expand'):
      # Find related in simulation
      for my_simulation_movement in self.getDeliveryRelatedValueList(
                                              portal_type = 'Simulation Movement'):
        # And apply
        getattr(my_simulation_movement.getObject(), method_id)()
      for c in self.contentValues(filter={'portal_type': 'Delivery Cell'}):
        for my_simulation_movement in c.getDeliveryRelatedValueList(
                                              portal_type = 'Simulation Movement'):
          # And apply
          getattr(my_simulation_movement.getObject(), method_id)()

    def reindexObject(self, *k, **kw):
      """Reindex children"""
      self.recursiveReindexObject(*k, **kw)

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventoriatedQuantity')
    def getInventoriatedQuantity(self):
      """
      """
      return Movement.getInventoriatedQuantity(self)

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventoriatedStartDate')
    def getInventoriatedStartDate(self):
      """
      """
      return Movement.getStartDate(self)

    security.declareProtected(Permissions.AccessContentsInformation, 'getInventoriatedStopDate')
    def getInventoriatedStopDate(self):
      """
      """
      return Movement.getStopDate(self)

#     security.declarePrivate('_checkConsistency')
#     def _checkConsistency(self, fixit=0, mapped_value_property_list = ('quantity', 'price')):
#       """
#         Check the constitency of transformation elements
#       """
#       error_list = XMLMatrix._checkConsistency(self, fixit=fixit)
# 
#       # First quantity
#       # We build an attribute equality and look at all cells
#       q_constraint = Constraint.AttributeEquality(
#         domain_base_category_list = self.getVariationBaseCategoryList(),
#         predicate_operator = 'SUPERSET_OF',
#         mapped_value_property_list = mapped_value_property_list )
#       for k in self.getCellKeys(base_id = 'movement'):
#         kw={}
#         kw['base_id'] = 'movement'
#         c = self.getCell(*k, **kw)
#         if c is not None:
#           predicate_value = []
#           for p in k:
#             if p is not None: predicate_value += [p]
#           q_constraint.edit(predicate_value_list = predicate_value)
#           if fixit:
#             error_list += q_constraint.fixConsistency(c)
#           else:
#             error_list += q_constraint.checkConsistency(c)
#           if list(c.getVariationCategoryList()) != predicate_value:
#             error_message =  "Variation %s but sould be %s" % (c.getVariationCategoryList(),predicate_value)
#             if fixit:
#               c.setVariationCategoryList(predicate_value)
#               error_message += " (Fixed)"
#             error_list += [(c.getRelativeUrl(), 'VariationCategoryList inconsistency', 100, error_message)]
# 
#       return error_list

    # Simulation Consistency Check
    def getSimulationQuantity(self):
      """
          Computes the quantities in the simulation
      """
      if not self.hasCellContent():
        result = self.DeliveryLine_zGetRelatedQuantity(uid=self.getUid())
        if len(result) > 0:
          return result[0].quantity
      return None

    def getSimulationSourceList(self):
      """
          Computes the sources in the simulation
      """
      result = self.DeliveryLine_zGetRelatedSource(uid=self.getUid())
      return map(lambda x: x.source, result)

    def getSimulationDestinationList(self):
      """
          Computes the destinations in the simulation
      """
      result = self.DeliveryLine_zGetRelatedDestination(uid=self.getUid())
      return map(lambda x: x.destination, result)

    def getSimulationSourceSectionList(self):
      """
          Computes the source sections in the simulation
      """
      result = self.DeliveryLine_zGetRelatedSourceSection(uid=self.getUid())
      return map(lambda x: x.source_section, result)

    def getSimulationDestinationSectionList(self):
      """
          Computes the destination sections in the simulation
      """
      result = self.DeliveryLine_zGetRelatedDestinationSection(uid=self.getUid())
      return map(lambda x: x.destination_section, result)

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getRootDeliveryValue')
    def getRootDeliveryValue(self):
      """
      Returns the root delivery responsible of this line
      """
      return self.getParentValue().getRootDeliveryValue()

    security.declareProtected(Permissions.ModifyPortalContent,
                              'updateSimulationDeliveryProperties')
    def updateSimulationDeliveryProperties(self, movement_list = None):
      """
      Set properties delivery_ratio and delivery_error for each
      simulation movement in movement_list (all movements by default),
      according to this delivery calculated quantity
      """
      parent = self.getParentValue()
      if parent is not None:
        parent.updateSimulationDeliveryProperties(movement_list, self)
