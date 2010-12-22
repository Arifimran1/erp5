##############################################################################
#
# Copyright (c) 2006 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
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


class Event:
    """
    Event properties and categories
    """

    _properties = (
        # XXX Copy/Paste from ERP5/PropertySheet/Order.py
        { 'id'          : 'received_date',
          'description' : 'Received date',
          'type'        : 'date',
          'mode'        : 'w' },
       # Source properties
        { 'id'          : 'organisation_title',
          'description' : 'The organisations this persons works for',
          'type'        : 'string',
          'acquisition_base_category' : ('subordination',),
          'acquisition_portal_type'   : ('Organisation',),
          'acquisition_copy_value'    : 0,
          'acquisition_mask_value'    : 0,
          'acquisition_sync_value'    : 0,
          'acquisition_accessor_id'   : 'getTitle',
          'acquisition_depends'       : None,
          'mode'        : 'w' },
        # Source properties
        { 'id'          : 'person_title',
          'description' : 'The person this event come from',
          'type'        : 'string',
          'acquisition_base_category' : ('source',),
          'acquisition_portal_type'   : ('Person',),
          'acquisition_copy_value'    : 0,
          'acquisition_mask_value'    : 0,
          'acquisition_sync_value'    : 0,
          'acquisition_accessor_id'   : 'getTitle',
          'acquisition_depends'       : None,
          'mode'        : 'w' },
        )

    # XXX Source, Destination are duplicated...
    _categories = ('source', 'destination', 'subordination', 'follow_up')
