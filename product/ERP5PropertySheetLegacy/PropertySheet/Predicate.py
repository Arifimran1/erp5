##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
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


class Predicate:
    """
        Predicate properties and categories
        
        Predicate in ERP5 use a simplified form based on identity, range and
        set and range operations
        
        Other predicates must be implemented through scripts. Parameters
        can be provides to scripts (this reduces duplication of code)
    """

    _properties = (
        {   'id'          : 'criterion_property',
            'description' : 'The properties to test identity or range on',
            'type'        : 'tokens',
            'default'     : (),
            'mode'        : 'w' },
        {   'id'          : 'membership_criterion_base_category', # OR, we check if we have one
                                                                  # of theses categories
            'description' : 'The base categories to test',
            'type'        : 'tokens',
            'default'     : (),
            'mode'        : 'w' },
        {   'id'          : 'multimembership_criterion_base_category', # AND, we check we have all 
                                                                       # theses categories
            'description' : 'The base categories which allow multiple values and required AND test',
            'type'        : 'tokens',
            'default'     : (),
            'mode'        : 'w' },
        {   'id'          : 'membership_criterion_category',
            'description' : 'The predicate categories',
            'type'        : 'lines',
            'default'     : (),
            'mode'        : 'w' },
        {   'id'          : 'test_tales_expression',
            'description' : 'A Tales expression to implement a simple ' \
                            'condition in Python. Runtime context of this ' \
                            'expression will be the tested document',
            'type'        : 'string',
            'default'     : 'python: True',
            'mode'        : 'w' },
        {   'id'          : 'test_method_id',
            'description' : 'A python method to implement additional tests',
            'type'        : 'lines', # Only a list of method ids is feasable for lines
            'mode'        : 'w' },
        #{   'id'          : 'parameter_string', # XXX Not feasable for AND
        #    'description' : 'A string defining default values for parameters (python syntax)',
        #    'type'        : 'string',
        #    'mode'        : 'w' },                
        )


