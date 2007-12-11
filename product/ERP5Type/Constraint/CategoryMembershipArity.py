##############################################################################
#
# Copyright (c) 2002, 2005 Nexedi SARL and Contributors. All Rights Reserved.
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

from Constraint import Constraint

class CategoryMembershipArity(Constraint):
  """
    This method check and fix if an object respects the arity.
    For example we can check if every Order has at
    least one source.
    Configuration exemple:
    { 'id'            : 'source',
      'description'   : '',
      'type'          : 'CategoryMembershipArity',
      'min_arity'     : '1',
      'max_arity'     : '1',
      'portal_type'   : ('Organisation', ),
      'base_category' : ('source',)
      'condition'     : 'python: object.getPortalType() == 'Foo',
    },
  """

  def _calculateArity(self, obj):
    base_category = self.constraint_definition['base_category']
    portal_type = self.constraint_definition['portal_type']
    return len(obj.getCategoryMembershipList(base_category,
                                              portal_type=portal_type))

  def checkConsistency(self, obj, fixit=0):
    """
      This is the check method, we return a list of string,
      each string corresponds to an error.
      We are looking the definition of the constraing where
      are defined the minimum and the maximum arity, and the
      list of objects we wants to check the arity.
    """
    if not self._checkConstraintCondition(obj):
      return []
    errors = []
    # Retrieve values inside de PropertySheet (_constraints)
    base_category = self.constraint_definition['base_category']
    min_arity = int(self.constraint_definition['min_arity'])
    max_arity = None
    if 'max_arity' in self.constraint_definition:
      max_arity = int(self.constraint_definition['max_arity'])
    portal_type = self.constraint_definition['portal_type']
    # Check arity and compare it with the min and max
    arity = self._calculateArity(obj)
    if not (max_arity is None and (min_arity <= arity)
        or (min_arity <= arity <= max_arity)):
      # Generate error message
      error_message = "Arity error for relation '%s'" % \
                      base_category
      if portal_type is not ():
        error_message += " and portal_type: '%s'" % str(portal_type)
      if max_arity is None:
        error_message += \
          ", arity is equal to %i but should be at least %i" % \
          (arity, min_arity)
      else:
        error_message += \
          ", arity is equal to %i but should be between %i and %i" % \
          (arity, min_arity, max_arity)
      # Add error
      errors.append(self._generateError(obj, error_message))
    return errors
