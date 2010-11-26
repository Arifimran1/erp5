##############################################################################
#
# Copyright (c) 2010 Nexedi SARL and Contributors. All Rights Reserved.
#                    Arnaud Fontaine <arnaud.fontaine@nexedi.com>
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

class PropertyExistenceConstraint:
    """
    Define a Property Existence Constraint for ZODB Property Sheets
    """
    _properties = (
        {   'id': 'constraint_property',
            'type': 'lines',
            'description' : 'Properties to check the existence for',
            'default': () },
        {   'id': 'message_no_such_property',
            'type': 'string',
            'description' : 'Error message when there is no such property',
            'default': 'Property existence error for property ${property_id}, '\
                       'this document has no such property' },
        {   'id': 'message_property_not_set',
            'type': 'string',
            'description' : 'Error message when the property is not set',
            'default': 'Property existence error for property ${property_id}, '\
                       'this property is not defined' },
        )
