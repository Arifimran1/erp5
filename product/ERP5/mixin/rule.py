# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

import zope.interface
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.ERP5Type import Permissions, interfaces

def _compare(tester_list, prevision_movement, decision_movement):
  for tester in tester_list:
    if not tester.compare(prevision_movement, decision_movement):
      return False
  return True

class RuleMixin:
  """
  Provides generic methods and helper methods to implement
  IRule and IMovementCollectionUpdater.
  """
  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Declarative interfaces
  zope.interface.implements(interfaces.IRule,
                            interfaces.IDivergenceController,
                            interfaces.IMovementCollectionUpdater,)

  # Portal Type of created children
  movement_type = 'Simulation Movement'

  # Implementation of IRule
  def constructNewAppliedRule(self, context, id=None,
                              activate_kw=None, **kw):
    """
    Create a new applied rule in the context.

    An applied rule is an instantiation of a Rule. The applied rule is
    linked to the Rule through the `specialise` relation. The newly
    created rule should thus point to self.

    context -- usually, a parent simulation movement of the
               newly created applied rule

    activate_kw -- activity parameters, required to control
                   activity constraints

    kw -- XXX-JPS probably wrong interface specification
    """
    portal_types = getToolByName(self, 'portal_types')
    if id is None:
      id = context.generateNewId()
    if getattr(aq_base(context), id, None) is None:
      context.newContent(id=id,
                         portal_type='Applied Rule',
                         specialise_value=self,
                         activate_kw=activate_kw)
    return context.get(id)

  def test(self, *args, **kw):
    """
    If no test method is defined, return False, to prevent infinite loop

    XXX-JPS - I do not understand why 
    """
    if not self.getTestMethodId():
      return False # XXX-JPS - if people are stupid are enough not to configfure predicates, 
                   # it is not our role to be clever for them
                   # Rules have a workflow - make sure applicable rule system works
                   # if you wish, add a test here on workflow state to prevent using 
                   # rules which are no longer applicable
    return Predicate.test(self, *args, **kw)

  def expand(self, applied_rule, **kw):
    """
    Expand this applied rule to create new documents inside the
    applied rule.

    At expand time, we must replace or compensate certain
    properties. However, if some properties were overwritten
    by a decision (ie. a resource if changed), then we
    should not try to compensate such a decision.
    """
    # Update movements
    #  NOTE-JPS: it is OK to make rounding a standard parameter of rules
    #            although rounding in simulation is not recommended at all
    self.updateMovementCollection(applied_rule, movement_generator=self._getMovementGenerator())
    # And forward expand
    for movement in applied_rule.getMovementList():
      movement.expand(**kw)

  # Implementation of IDivergenceController # XXX-JPS move to IDivergenceController only mixin for 
  security.declareProtected( Permissions.AccessContentsInformation,
                            'isDivergent')
  def isDivergent(self, movement, ignore_list=[]):
    """
    Returns true if the Simulation Movement is divergent comparing to
    the delivery value
    """
    delivery = movement.getDeliveryValue()
    if delivery is None:
      return False
    if len(self.getDivergenceList(movement)) == 0:
      return False
    else:
      return True

  security.declareProtected(Permissions.View, 'getDivergenceList')
  def getDivergenceList(self, movement):
    """
    Returns a list of divergences of the movements provided
    in delivery_or_movement.

    movement -- a movement, a delivery, a simulation movement,
                or a list thereof
    """
    result_list = []
    for divergence_tester in self._getDivergenceTesterList(
      exclude_quantity=False):
      result = divergence_tester.explain(movement)
      if isinstance(result, (list, tuple)): # for compatibility
        result_list.extend(result)
      elif result is not None:
        result_list.append(result)
    return result_list

  # Placeholder for methods to override
  def _getMovementGenerator(self):
    """
    Return the movement generator to use in the expand process
    """
    raise NotImplementedError

  def _getMovementGeneratorContext(self, applied_rule):
    """
    Return the movement generator context to use for expand
    """
    raise NotImplementedError

  def _getMovementGeneratorMovementList(self):
    """
    Return the movement lists to provide to the movement generator
    """
    raise NotImplementedError

  def _getDivergenceTesterList(self, exclude_quantity=True):
    """
    Return the applicable divergence testers which must
    be used to test movement divergence. (ie. not all
    divergence testers of the Rule)

     exclude_quantity -- if set to true, do not consider
                         quantity divergence testers
     """
    if exclude_quantity:
      return filter(lambda x:x.isDivergenceProvider() and \
                    x.getTestedProperty() != 'quantity', self.objectValues(
        portal_type=self.getPortalDivergenceTesterTypeList()))
    else:
      return filter(lambda x:x.isDivergenceProvider(), self.objectValues(
        portal_type=self.getPortalDivergenceTesterTypeList()))

  def _getMatchingTesterList(self):
    """
    Return the applicable divergence testers which must
    be used to match movements and build the diff (ie.
    not all divergence testers of the Rule)
    """
    return filter(lambda x:x.isMatchingProvider(), self.objectValues(
      portal_type=self.getPortalDivergenceTesterTypeList()))

  def _getQuantityTesterList(self):
    """
    Return the applicable quantity divergence testers.
    """
    tester_list = self.objectValues(
      portal_type=self.getPortalDivergenceTesterTypeList())
    return [x for x in tester_list if x.getTestedProperty() == 'quantity']

  def _newProfitAndLossMovement(self, prevision_movement):
    """
    Returns a new temp simulation movement which can
    be used to represent a profit or loss in relation
    with prevision_movement

    prevision_movement -- a simulation movement
    """
    raise NotImplementedError

  def _isProfitAndLossMovement(movement):
    """
    Returns True if movement is a profit and loss movement.
    """
    raise NotImplementedError

  def _extendMovementCollectionDiff(self, movement_collection_diff,
                                    prevision_movement, decision_movement_list):
    """
    Compares a prevision_movement to decision_movement_list which
    are part of the matching group and updates movement_collection_diff
    accordingly

    NOTE: this method API implicitely considers that each group of matching 
    movements has 1 prevision_movement (aggregated) for N decision_movement
    It implies that prevision_movement are "more" aggregated than 
    decision_movement.

    TODO:
       - is this asumption appropriate ?
    """
    # Sample implementation - but it actually looks very generic
    # Case 1: movements which are not needed
    if prevision_movement is None:
      # decision_movement_list contains simulation movements which must
      # be deleted
      for decision_movement in decision_movement_list:
        if decision_movement.isDeletable(): # If not frozen and all children are deletable
          # Delete deletable
          movement_collection_diff.addDeletableMovement(decision_movement)
        else:
          # Compensate non deletable
          new_movement = decision_movement.asContext(quantity=-decision_movement.getQuantity())
          movement_collection_diff.addNewMovement(new_movement)
      return
    # Case 2: movements which should be added
    elif len(decision_movement_list) == 0:
      # if decision_movement_list is empty, we can just create a new one.
      movement_collection_diff.addNewMovement(prevision_movement)
      return
    # Case 3: movements which are needed but may need update or compensation_movement_list
    #  let us imagine the case of a forward rule
    #  ie. what comes in must either go out or has been lost
    divergence_tester_list = self._getDivergenceTesterList()
    profit_tester_list = self._getDivergenceTesterList()
    quantity_tester_list = self._getQuantityTesterList()
    compensated_quantity = 0.0
    updatable_movement = None
    not_completed_movement = None
    updatable_compensation_movement = None
    prevision_quantity = prevision_movement.getQuantity()
    decision_quantity = 0.0
    # First, we update all properties (exc. quantity) which could be divergent
    # and if we can not, we compensate them
    for decision_movement in decision_movement_list:
      decision_movement_quantity = decision_movement.getQuantity()
      decision_quantity += decision_movement_quantity
      if self._isProfitAndLossMovement(decision_movement):
        if decision_movement.isFrozen():
          # Record not completed movements
          if not_completed_movement is None and not decision_movement.isCompleted():
            not_completed_movement = decision_movement
          # Frozen must be compensated
          if not _compare(profit_tester_list, prevision_movement, decision_movement):
            new_movement = decision_movement.asContext(quantity=-decision_movement_quantity)
            movement_collection_diff.addNewMovement(new_movement)
            compensated_quantity += decision_movement_quantity
        else:
          updatable_compensation_movement = decision_movement
          # Not Frozen can be updated
          kw = {}
          for tester in profit_tester_list:
            if not tester.compare(prevision_movement, decision_movement):
              kw.update(tester.getUpdatablePropertyDict(prevision_movement, decision_movement))
          if kw:
            movement_collection_diff.addUpdatableMovement(decision_movement, kw)
      else:
        if decision_movement.isFrozen():
          # Frozen must be compensated
          if not _compare(divergence_tester_list, prevision_movement, decision_movement):
            new_movement = decision_movement.asContext(quantity=-decision_movement_quantity)
            movement_collection_diff.addNewMovement(new_movement)
            compensated_quantity += decision_movement_quantity
        else:
          updatable_movement = decision_movement
          # Not Frozen can be updated
          kw = {}
          for tester in divergence_tester_list:
            if not tester.compare(prevision_movement, decision_movement): 
              kw.update(tester.getUpdatablePropertyDict(prevision_movement, decision_movement))
              # XXX-JPS - there is a risk here that quanity is wrongly updated
          if kw:
            movement_collection_diff.addUpdatableMovement(decision_movement, kw)
    # Second, we calculate if the total quantity is the same on both sides
    # after compensation
    quantity_movement = prevision_movement.asContext(quantity=decision_quantity-compensated_quantity)
    if not _compare(quantity_tester_list, prevision_movement, quantity_movement):
      missing_quantity = prevision_quantity - decision_quantity + compensated_quantity
      if updatable_movement is not None:
        # If an updatable movement still exists, we update it
        updatable_movement.setQuantity(updatable_movement.getQuantity() + missing_quantity)
      elif not_completed_movement is not None:
        # It is still possible to add a new movement some movements are not completed
        new_movement = prevision_movement.asContext(quantity=missing_quantity)
        movement_collection_diff.addNewMovement(new_movement)
      elif updatable_compensation_movement is not None:
        # If not, it means that all movements are completed
        # but we can still update a profit and loss movement_collection_diff
        updatable_compensation_movement.setQuantity(updatable_compensation_movement.getQuantity()
                                                  + missing_quantity)
      else:
        # We must create a profit and loss movement
        new_movement = self._newProfitAndLossMovement(prevision_movement)
        movement_collection_diff.addNewMovement(new_movement)
