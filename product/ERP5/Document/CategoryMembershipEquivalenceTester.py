# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008-2009 Nexedi SA and Contributors. All Rights Reserved.
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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from AccessControl import ClassSecurityInfo
from Products.ERP5Type.Core.Predicate import Predicate
from Products.ERP5Type import Permissions, PropertySheet
from Products.ERP5.mixin.equivalence_tester import EquivalenceTesterMixin

class CategoryMembershipEquivalenceTester(Predicate, EquivalenceTesterMixin):
  """
  The purpose of this divergence tester is to check the
  consistency between delivery movement and simulation movement
  for a specific category.
  """
  meta_type = 'ERP5 Category Membership Equivalence Tester'
  portal_type = 'Category Membership Equivalence Tester'
  add_permission = Permissions.AddPortalContent

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Declarative properties
  property_sheets = (   PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      , PropertySheet.EquivalenceTester
                      , PropertySheet.SolverSelection
                     )

  @staticmethod
  def _getTestedPropertyValue(movement, property):
    return movement.getPropertyList(property)

  def _compare(self, prevision_movement, decision_movement):
    """
    If prevision_movement and decision_movement don't match, it returns a
    list : (prevision_value, decision_value, message, mapping)
    """
    tested_property = self.getTestedProperty()
    if getattr(decision_movement, 'isPropertyRecorded',
               lambda x:False)(tested_property):
      decision_value = decision_movement.getRecordedProperty(tested_property)
    else:
      decision_value = self._getTestedPropertyValue(decision_movement,
                                                    tested_property)
    prevision_value = self._getTestedPropertyValue(prevision_movement,
                                                   tested_property)

    # XXX do we have configurable parameter for this divergence tester ?
    # like ambiguity...
    if sorted(decision_value) != sorted(prevision_value):
      return (
        prevision_value, decision_value,
        'The values of ${property_name} category are different between decision and prevision.',
        dict(property_name=tested_property))
    return None
