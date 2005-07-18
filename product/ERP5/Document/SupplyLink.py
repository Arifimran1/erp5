##############################################################################
#
# Copyright (c) 2005 Nexedi SARL and Contributors. All Rights Reserved.
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
from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5Type.XMLMatrix import XMLMatrix

from Products.ERP5.Document.DeliveryLine import DeliveryLine
from Products.ERP5.Document.Movement import Movement
from Products.ERP5Type.XMLObject import XMLObject
from Products.ERP5.Document.Path import Path

from zLOG import LOG

class SupplyLink(Path, XMLObject):
    """
      A DeliveryLine object allows to implement lines in
      Deliveries (packing list, order, invoice, etc.)

      It may include a price (for insurance, for customs, for invoices,
      for orders)
    """

    meta_type = 'ERP5 Supply Link'
    portal_type = 'Supply Link'

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.View)

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
                      , PropertySheet.Path
                      , PropertySheet.FlowCapacity
                      , PropertySheet.TransformedResource
                      , PropertySheet.Delivery
                      , PropertySheet.Simulation
                      )

    security.declareProtected(Permissions.View, 'isProductionSupplyLink')
    def isProductionSupplyLink(self):
      """
        Return 1 if the SupplyLink represents a production.
      """
      return (self.getSourceValue() is None)

    security.declareProtected(Permissions.View, 'isPackingListSupplyLink')
    def isPackingListSupplyLink(self):
      """
        Return 1 if the SupplyLink represents a packing list.
      """
      return not(self.isProductionSupplyLink())

    security.declareProtected(Permissions.View, 'getCurrentNodeValue')
    def getCurrentNodeValue(self):
      """
        Return the node used to find the previous SupplyLink
      """
      if self.isProductionSupplyLink():
        node = self.getDestinationValue()
      else:
        node = self.getSourceValue()
      return node

    security.declareProtected(Permissions.View, 'test')
    def test(self, movement, concurrent_supply_link_list):
      """
        Test if the current link can expand this movement.
        Futur implementation have to return properties value
        (like quantity) calculated.
      """
      # XXX This method has to be rewritten.
      # Predicate must be used.
      # Current implementation is enough now for customers.
      result = 0
      resource = movement.getResource()
      if resource.find('operation/') == -1:
        # XXX reject operation
        if concurrent_supply_link_list == []:
          result = 1
        else:
          # Test if the movement correspond to the resource to produced
          ind_phase_list = movement.getIndustrialPhaseValueList()
          if ind_phase_list != []:
            # Is this SupplyLink in the route to the previous production node ?
            supply_chain = self.getParent()
            previous_ind_phase_list =\
                  supply_chain.getPreviousProductionIndustrialPhaseList(self)
            for ind_phase in ind_phase_list:
              if ind_phase in previous_ind_phase_list:
                result = 1
                break
          else:
            # How to delivered raw materials ?
            # First dirty implementation...
            if len(concurrent_supply_link_list) > 1:
              raise "SupplyChainError",\
                    "SupplyChain unable to find route."
            else:
              supply_chain = self.getParent()
              previous_ind_phase_list =\
                    supply_chain.getPreviousProductionIndustrialPhaseList(self)
              if len(previous_ind_phase_list) == 0:
                result = 1
      return result

    security.declareProtected(Permissions.View, 'getStartDate')
    def getStartDate(self, stop_date):
      """
        Calculate the start date, depending on the delay.
      """
      max_delay = self.getMaxDelay()
      min_delay = self.getMinDelay()
      for delay in [max_delay, min_delay, 0]:
        if type(delay) in (type(1), type(1.0)):
          start_date = stop_date - delay
          break
      return start_date
