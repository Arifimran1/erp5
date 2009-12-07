# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2006-2008 Nexedi SA and Contributors. All Rights Reserved.
#               Rafael Monnerat <rafael@nexedi.com>
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


class DivergenceTester:
  """
    Divergence Tester are use for the divergence testers.
  """

  _properties = (
    {  'id'          : 'tested_property',
       'description' : 'Property used to Test',
       'type'        : 'lines',
       'default'     : (),
       'mode'        : 'w' },
    {  'id'          : 'testing_provider',
       'description' : 'Defines whether a divergence tester acts as a testing provider.',
       'type'        : 'boolean',
       'default'     : 0,
       'mode'        : 'rw' },
    {  'id'          : 'matching_provider',
       'description' : 'Defines whether a divergence tester acts as a matching provider.',
       'type'        : 'boolean',
       'default'     : 0,
       'mode'        : 'rw' },
  )
