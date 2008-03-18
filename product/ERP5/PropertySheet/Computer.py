#############################################################################
#
# Copyright (c) 2008 Nexedi SA and Contributors. All Rights Reserved.
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


class Computer:
  """
  Computer properties and categories
  """

  _properties = (
    { 'id'                       : 'network_address'
    , 'storage_id'               : 'default_network_address'
    , 'description'              : 'The unique identity of the computer in computer network.'
    , 'type'                     : 'content'
    , 'portal_type'              : ( 'Internet Protocol Address', )#'Asynchronous Transfer Mode Address', 'UMTS Address' )
    , 'acquired_property_id'     : ( 'text', 'host_name', 'ip_address', )
    , 'acquisition_base_category': ( 'parent', )
    , 'acquisition_portal_type'  : ( 'Computer', )
    , 'acquisition_copy_value'   : 0
    , 'acquisition_mask_value'   : 1
    , 'acquisition_sync_value'   : 0
    , 'acquisition_accessor_id'  : 'getDefaultNetworkAddressValue'
    , 'acquisition_depends'      : None
    , 'alt_accessor_id'          : ()
    , 'mode'                     : 'w'
    },
  )

  _categories = ('product_line', 'role', 'function',)
