# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008-2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Rafael Monnerat <rafael@nexedi.com>
#                    Jean-Paul Smets <jp@nexedi.com>
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
from Products.ERP5.Document.Predicate import Predicate
from Products.ERP5Type import Permissions, PropertySheet
from Products.ERP5.mixin.equivalence_tester import EquivalenceTesterMixin

class FloatEquivalenceTester(Predicate, EquivalenceTesterMixin):
  """ Compare float values, with support for rounding.
  """
  meta_type = 'ERP5 Float Equivalence Tester'
  portal_type = 'Float Equivalence Tester'
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
                      , PropertySheet.DecimalOption
                     )

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
                                                    tested_property) or 0.0
    prevision_value = self._getTestedPropertyValue(prevision_movement,
                                                   tested_property) or 0.0

    # use delivery_ratio if specified
    if self.getProperty('use_delivery_ratio') and \
        prevision_movement.getDelivery() == decision_movement.getRelativeUrl():
      decision_value *= prevision_movement.getDeliveryRatio()

    if self.isDecimalAlignmentEnabled():
      decision_value = self._round(decision_value)
      prevision_value = self._round(prevision_value)

    delta = decision_value - prevision_value
    # XXX we should use appropriate property sheets and getter methods
    # for these properties.
    # Maybe, but beware of default values of quantity when doing so
    absolute_tolerance_min = self.getProperty('quantity_range_min')
    if absolute_tolerance_min is not None and \
       delta < absolute_tolerance_min:
      return (
        prevision_value, decision_value,
        'The difference of ${property_name} between decision and prevision is less than ${value}.',
        dict(property_name=tested_property,
             value=absolute_tolerance_min))
    absolute_tolerance_max = self.getProperty('quantity_range_max')
    if absolute_tolerance_max is not None and \
       delta > absolute_tolerance_max:
      return (
        prevision_value, decision_value,
        'The difference of ${property_name} between decision and prevision is larger than ${value}.',
        dict(property_name=tested_property,
             value=absolute_tolerance_max))

    tolerance_base = self.getProperty('tolerance_base')
    base = None
    if tolerance_base == 'resource_quantity_precision':
      # Precision of this movement's resource base unit quantity
      resource = prevision_movement.getResourceValue()
      if resource is not None:
        base = resource.getBaseUnitQuantity()
    elif tolerance_base == 'resource_price_precision':
      # Precision of this movement's resource base unit price
      base = prevision_movement.getBaseUnitPrice()
      # fallback to price currency, like in Amount.getPricePrecision
      if base is None:
        currency = prevision_movement.getPriceCurrencyValue()
        if currency is not None:
          base = currency.getBaseUnitQuantity()
    elif tolerance_base == 'price_currency_precision':
      # Precision of this movement's price currency
      currency = prevision_movement.getPriceCurrencyValue()
      if currency is not None:
        base = currency.getBaseUnitQuantity()
    elif tolerance_base == 'source_section_currency_precision':
      # Precision of this source section's accounting currency
      section = prevision_movement.getSourceSectionValue()
      if section is not None:
        currency = section.getPriceCurrencyValue()
        if currency is not None:
          base = currency.getBaseUnitQuantity()
    elif tolerance_base == 'destination_section_currency_precision':
      # Precision of this destination section's accounting currency
      section = prevision_movement.getDestinationSectionValue()
      if section is not None:
        currency = section.getPriceCurrencyValue()
        if currency is not None:
          base = currency.getBaseUnitQuantity()
    elif tolerance_base == 'tested_property':
      base = prevision_value

    if base is not None:
      relative_tolerance_min = self.getProperty('tolerance_range_min')
      if relative_tolerance_min is not None and \
             delta < relative_tolerance_min * base:
        return (
            prevision_value, decision_value,
            'The difference of ${property_name} between decision and prevision is less than ${value} times of the prevision value.',
            dict(property_name=tested_property,
                 value=relative_tolerance_min))
      relative_tolerance_max = self.getProperty('tolerance_range_max')
      if relative_tolerance_max is not None and \
             delta < relative_tolerance_max * base:
        return (
            prevision_value, decision_value,
            'The difference of ${property_name} between decision and prevision is less than ${value} times of the prevision value.',
            dict(property_name=tested_property,
                 value=relative_tolerance_max))

  def _round(self, value):
    from decimal import (Decimal, ROUND_DOWN, ROUND_UP, ROUND_CEILING,
                         ROUND_FLOOR, ROUND_HALF_DOWN, ROUND_HALF_EVEN,
                         ROUND_HALF_UP)
    # Python2.4 did not support ROUND_05UP yet.
    rounding_option_dict = {'ROUND_DOWN':ROUND_DOWN,
                            'ROUND_UP':ROUND_UP,
                            'ROUND_CEILING':ROUND_CEILING,
                            'ROUND_FLOOR':ROUND_FLOOR,
                            'ROUND_HALF_DOWN':ROUND_HALF_DOWN,
                            'ROUND_HALF_EVEN':ROUND_HALF_EVEN,
                            'ROUND_HALF_UP':ROUND_HALF_UP}
    rounding_option = rounding_option_dict.get(self.getDecimalRoundingOption(),
                                               ROUND_DOWN)
    return Decimal(str(value)).quantize(Decimal(self.getDecimalExponent()),
                                    rounding=rounding_option)
