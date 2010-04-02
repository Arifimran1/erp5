# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009 Nexedi KK and Contributors. All Rights Reserved.
#                    Yusei TAHARA <yusei@nexedi.com>
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

from Products.ERP5.PropertySheet.DecimalOption import DecimalOption


class RoundingModel(DecimalOption):
  """Rounding Model properties and categories.
  """
  _properties = DecimalOption._properties+(
    { 'id'          : 'rounding_method_id',
      'description' : 'The name of a python script which implements custom rounding routine.',
      'type'        : 'string',
      'mode'        : 'w',
      'default'     : None,
    },
    { 'id'          : 'rounded_property_id',
      'description' : 'The property name which value is rounded. Note that some property is virtual, like total_price.',
      'type'        : 'tokens',
      'mode'        : 'w',
      'default'     : None,
    },
    { 'id'          : 'precision',
      'description' : 'Precision value to be used for rounding. Rounding model accepts negative precision value as same as built-in round function.',
      'type'        : 'int',
      'mode'        : 'w',
      'default'     : None,
    },
  )
