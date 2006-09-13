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

from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5.Document.Rule import Rule
from Products.ERP5.Document.OrderRule import OrderRule
from Products.ERP5.Document.TransformationSourcingRule import\
                                            TransformationSourcingRuleMixin

from zLOG import LOG, WARNING

class ProductionOrderRule(OrderRule):
    """
      Prouction Order Rule object use a Supply Chain to expand a 
      Production Order.
    """

    # CMF Type Definition
    meta_type = 'ERP5 Production Order Rule'
    portal_type = 'Production Order Rule'

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    __implements = ( Interface.Predicate,
                     Interface.Rule )

    # Default Properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      )

    # Simulation workflow
    security.declareProtected(Permissions.AccessContentsInformation,
                              '_getExpandablePropertyDict')
    def _getExpandablePropertyDict(self, applied_rule, movement, 
                                   default_property_list=None, **kw):
      """
      Return a Dictionary with the Properties used to edit 
      the simulation movement.
      """
      property_dict = {}

      if default_property_list is None:
        LOG("Order Rule , _getExpandablePropertyDict", WARNING,
            "Hardcoded properties set")
        default_property_list = (
          'destination_section',
          'destination', 'resource', 
          'variation_category_list',
          'aggregate_list',
          'start_date', 'stop_date')
    
      supply_chain = self.getSupplyChain(applied_rule)
      # We got a supply chain
      # Try to get the last SupplyLink
      last_link = supply_chain.getLastLink()
      # We got a valid industrial_phase
      # Now, we have to generate Simulation Movement, in order to
      # create a ProductionPackingList.
      destination_node = last_link.getDestinationValue()
      source_value = destination_node.getDestination()
      source_section_value = last_link.getDestinationSection()
      if source_value is not None:
        property_dict["source"] = source_value
      if source_section_value is not None:
        property_dict["source_section"] = source_section_value
    
      for prop in default_property_list:
        property_dict[prop] = movement.getProperty(prop)
    
      return property_dict

from Products.ERP5Type.Utils import monkeyPatch
monkeyPatch(TransformationSourcingRuleMixin, ProductionOrderRule)
