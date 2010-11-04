# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Nexedi SA and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
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
# Foundation, Inc., 51 Franklin Street - Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

import zope.interface
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from Products.ERP5Type import Permissions, PropertySheet, interfaces
from Products.ERP5Type.Core.Predicate import Predicate
from Products.ERP5.mixin.rule import RuleMixin, MovementGeneratorMixin
from Products.ERP5.mixin.movement_collection_updater import \
     MovementCollectionUpdaterMixin

class TradeModelSimulationRule(RuleMixin, MovementCollectionUpdaterMixin, Predicate):
  """
    Rule for Trade Model
  """
  # CMF Type Definition
  meta_type = 'ERP5 Trade Model Simulation Rule'
  portal_type = 'Trade Model Simulation Rule'

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Declarative interfaces
  zope.interface.implements(interfaces.IRule,
                            interfaces.IDivergenceController,
                            interfaces.IMovementCollectionUpdater,)

  # Default Properties
  property_sheets = (
    PropertySheet.Base,
    PropertySheet.XMLObject,
    PropertySheet.CategoryCore,
    PropertySheet.DublinCore,
    PropertySheet.Task,
    PropertySheet.Predicate,
    PropertySheet.Reference,
    PropertySheet.Version,
    PropertySheet.Rule
    )

  def _getMovementGenerator(self, context):
    """
    Return the movement generator to use in the expand process
    """
    return TradeModelRuleMovementGenerator(applied_rule=context, rule=self)

  def _getMovementGeneratorContext(self, context):
    """
    Return the movement generator context to use for expand
    """
    return context

  def _getMovementGeneratorMovementList(self, context):
    """
    Return the movement lists to provide to the movement generator
    """
    return []

  def _isProfitAndLossMovement(self, movement):
    # For a kind of trade rule, a profit and loss movement lacks source
    # or destination.
    return (movement.getSource() is None or movement.getDestination() is None)

class TradeModelRuleMovementGenerator(MovementGeneratorMixin):

  def _getUpdatePropertyDict(self, input_movement):
    return {'causality_list': input_movement.getCausalityList(),
            'delivery': None,
            # XXX shouldn't we create a tester for price instead ?
            'price': input_movement.getPrice()}

  def _getInputMovementList(self, movement_list=None, rounding=False):
    simulation_movement = self._applied_rule.getParentValue()
    input_movement = aq_base(simulation_movement).__of__(self._applied_rule)
    for amount in simulation_movement.getAggregatedAmountList(
        # XXX add a 'trade_amount_generator' group type
        amount_generator_type_list=('Purchase Trade Condition',
                                    'Sale Trade Condition',
                                    'Trade Model Line')):
      if amount.getResource():
        # FIXME: Is it the right way to have source/destination and other
        #        non-Amount properties set on the generated movement ?
        movement = input_movement.asContext(**dict((k, v)
            for k, v in amount.__dict__.iteritems()
            if k[0] != '_' and k != 'categories'))
        base_category_set = set(amount.getBaseCategoryList())
        base_category_set.remove('price_currency') # XXX
        movement._setCategoryMembership(base_category_set,
                                        amount.getCategoryList(),
                                        base=True)
        yield movement
