##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#          Jean-Paul Smets-Solanes <jp@nexedi.com>
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



class Organisation:
  """
    Organisation properties and categories
  """

  _properties = (
    { 'id'          : 'corporate_name',
      'description' : 'The official name of this organisation',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'social_capital',
      'description' : 'The social capital of this organisation',
      'type'        : 'int',
      'mode'        : 'w' },
    { 'id'          : 'social_capital_currency',
      'description' : "The currency in which the social capital is"
                      "expressed",
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'activity_code',
      'description' : 'The activity code of this organisation',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'geographic_incorporate_code',
      'description' : 'The geographic incorporate code of this organisation, sometimes derivated from corporate code',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'ean13_code',
      'description' : 'The EAN 13 code of this organisation',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'vat_code',
      'description' : 'The VAT (Value Added Tax) code of this organisation',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'corporate_registration_code',
      'description' : 'The corporate registration code of this organisation',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'social_code',
      'description' : 'The social code of this organisation',
      'type'        : 'string',
      'mode'        : 'w' },                       
    { 'id'          : 'creation_date',
      'description' : 'Thedate of the creation of this organisation',
      'type'        : 'date',
      'mode'        : 'w' },                          
      
    # Acquisition
    { 'id'          : 'address',
      'storage_id'  : 'default_address',
      'description' : 'The organisations this persons works for',
      'type'        : 'content',
      'portal_type' : ('Address'),
      'acquisition_base_category' : ('region', ),
      'acquisition_portal_type'   : ('Category',),
      'acquisition_copy_value'    : 0,
      'acquisition_mask_value'    : 1,
      'acquisition_sync_value'    : 0,
      'acquisition_accessor_id'   : 'getDefaultAddressValue',
      'acquisition_depends'       : None,
      'mode'        : 'w' },
    { 'id'          : 'telephone',
      'storage_id'  : 'default_telephone',
      'description' : 'The organisations this persons works for',
      'type'        : 'content',
      'portal_type' : ('Telephone'),
      'acquisition_base_category' : ('region', ),
      'acquisition_portal_type'   : ('Category',),
      'acquisition_copy_value'    : 0,
      'acquisition_mask_value'    : 1,
      'acquisition_sync_value'    : 0,
      'acquisition_accessor_id'   : 'getDefaultTelephoneValue',
      'acquisition_depends'       : None,
      'mode'        : 'w' },
    { 'id'          : 'fax',
      'storage_id'  : 'default_fax',
      'description' : 'The organisations this persons works for',
      'type'        : 'content',
      'portal_type' : ('Fax'),
      'acquisition_base_category' : ('region', ),
      'acquisition_portal_type'   : ('Category',),
      'acquisition_copy_value'    : 0,
      'acquisition_mask_value'    : 1,
      'acquisition_sync_value'    : 0,
      'acquisition_accessor_id'   : 'getDefaultFaxValue',
      'acquisition_depends'       : None,
      'mode'        : 'w' },
    { 'id'          : 'email',
      'storage_id'  : 'default_email',
      'description' : 'The organisations this persons works for',
      'type'        : 'content',
      'portal_type' : ('Email'),
      'acquisition_base_category' : ('region', ),
      'acquisition_portal_type'   : ('Category',),
      'acquisition_copy_value'    : 0,
      'acquisition_mask_value'    : 1,
      'acquisition_sync_value'    : 0,
      'acquisition_accessor_id'   : 'getDefaultEmailValue',
      'acquisition_depends'       : None,
      'mode'        : 'w' },
  
    # XXXX Coramy Specific : needs to be transfered in Coramy Organisation
    # as soon as possible
    { 'id'          : 'code_comptable',
      'description' : 'The reference of the organisation for accounting application',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'ean13_code',
      'description' : 'The ean_13 of the organisation',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'eu_vat_code',
      'description' : 'The european vat code of the organisation',
      'type'        : 'string',
      'mode'        : 'w' },
    { 'id'          : 'siren_code',
      'description' : 'The french siren code of the organisation',
      'type'        : 'string',
      'mode'        : 'w' },  
  
  )

  _categories = ( 'role', 'group', 'activity', 'skill', 'market_segment', 'region',
                  'social_form', 'function', 'source', 'destination', 'source_section',
                  'destination_section',)
