##############################################################################
#
# Copyright (c) 2002-2005 Nexedi SARL and Contributors. All Rights Reserved.
#                    Sebastien Robin <seb@nexedi.com>
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
from Acquisition import aq_base, aq_parent, aq_inner, aq_acquire
from Products.CMFCore.utils import getToolByName

from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5.Document.Rule import Rule
#from Products.ERP5Type.Base import TempBase

from zLOG import LOG

class InvoicingRule(Rule):
  """
    Invoicing Rule expand simulation created by a order or delivery rule.
  """

  # CMF Type Definition
  meta_type = 'ERP5 Invoicing Rule'
  portal_type = 'Invoicing Rule'
  add_permission = Permissions.AddPortalContent
  isPortalContent = 1
  isRADContent = 1

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  __implements__ = ( Interface.Predicate,
                     Interface.Rule )

  # Default Properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.CategoryCore
                    , PropertySheet.DublinCore
                    )

  security.declareProtected(Permissions.AccessContentsInformation,
                            'isAccountable')
  def isAccountable(self, movement):
    """
    Tells wether generated movement needs to be accounted or not.

    Invoice movement are never accountable, so simulation movement for
    invoice movements should not be accountable either.
    """
    return 0

  def _test(self, movement):
    """
    Tests if the rule (still) applies
    """
    parent = movement.getParentValue()
    result = 0
    if (parent.getPortalType() == 'Applied Rule') and \
       (parent.getSpecialiseId() in ('default_order_rule',
                                     'default_delivery_rule' )):
      result = 1
    return result

#### Helper method for expand
  def _generatePrevisionList(self, applied_rule, **kw):
    """
    Generate a list of movements, that should be children of this rule,
    based on its context (parent movement, delivery, configuration ...)

    These previsions are acrually returned as dictionaries.
    """
    # XXX Isn't it better to share the code with expand method
    context_movement = applied_rule.getParentValue()

    # Do not invoice within the same entity or whenever entities are not all
    # defined.
    # It could be OK to invoice within different entities of the same
    # company if we wish to get some internal analytical accounting but that
    # requires some processing to produce a balance sheet.
    source_section = context_movement.getSourceSection()
    destination_section = context_movement.getDestinationSection()
    if source_section == destination_section or source_section is None \
        or destination_section is None:
      return []
    
    invoice_line = {}
    invoice_line.update(
        price=context_movement.getPrice(),
        quantity=context_movement.getCorrectedQuantity(),
        quantity_unit=context_movement.getQuantityUnit(),
        efficiency=context_movement.getEfficiency(),
        resource=context_movement.getResource(),
        variation_category_list=context_movement.getVariationCategoryList(),
        variation_property_dict=context_movement.getVariationPropertyDict(),
        start_date=context_movement.getStartDate(),
        stop_date=context_movement.getStopDate(),
        source=context_movement.getSource(), source_section=source_section,
        destination=context_movement.getDestination(),
        destination_section=destination_section,
        # We do need to collect invoice lines to build invoices
        deliverable=1
    )
    return [invoice_line]

  security.declareProtected(Permissions.ModifyPortalContent, 'expand')
  def expand(self, applied_rule, force=0, **kw):
    """
    Expands the rule:
    - generate a list of previsions
    - compare the prevision with existing children
      - get the list of existing movements (immutable, mutable, deletable)
      - compute the difference between prevision and existing (add,
        modify, remove)
    - add/modify/remove child movements to match prevision
    """
    parent_movement = applied_rule.getParentValue()
    if parent_movement is not None: 
      if not parent_movement.isFrozen():
        add_list, modify_dict, \
          delete_list = self._getCompensatedMovementList(applied_rule, **kw)

        for movement_id in delete_list:
          applied_rule._delObject(movement_id)
      
        for movement, prop_dict in modify_dict.items():
          #XXX ignore start_date and stop_date if the difference is smaller than a
          # rule defined value
          for prop in ('start_date', 'stop_date'):
           if prop in prop_dict.keys():
              prop_dict.pop(prop)
          applied_rule[movement].edit(**prop_dict)

        for movement_dict in add_list:
          if 'id' in movement_dict.keys():
            mvmt_id = applied_rule._get_id(movement_dict.pop('id'))
            new_mvmt = applied_rule.newContent(id=mvmt_id,
                portal_type=self.movement_type)
          else:
            new_mvmt = applied_rule.newContent(portal_type=self.movement_type)
          new_mvmt.edit(**movement_dict)

    # Pass to base class
    Rule.expand(self, applied_rule, force=force, **kw)

  def isDeliverable(self, movement):
    return movement.getResource() is not None


