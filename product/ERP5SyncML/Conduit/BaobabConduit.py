##############################################################################
#
# Copyright (c) 2005 Nexedi SARL and Contributors. All Rights Reserved.
#                    Kevin Deldycke <kevin@nexedi.com>
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################

from Products.ERP5SyncML.Conduit.ERP5Conduit import ERP5Conduit
from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions
from Products.ERP5Type.Utils import convertToUpperCase
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_inner, aq_chain, aq_acquire
from ZODB.POSException import ConflictError

import datetime

from zLOG import LOG



class BaobabConduit(ERP5Conduit):
  """
  A conduit is in charge to read data from a particular structure,
  and then to save this data in another structure.

  In baobab, the data is read from some sql tables and it will stored
  with ERP5 objects. The difficult parts are :
  - for one sql table we have several kind of objects in ERP5
  - for each properties that comes from sql, we have one ore more
    properties in ERP5

  Most importants method defined here are :
  - constructContent : it is used when a new set of data comes from
                       the sql table, then constructContent must decide
                       wich kind of object must be created in ERP5
  - editDocument : after constructContent, editDocument is called with
                   all properties that comes from the set of data from
                   sql. Each property must be converted to ERP5 property.

  If you need to handle a new property, the most important thing to know
  is what will be the property used in ERP5. Then you have to enter a
  new dictionary in the property_map variable.

  # New changes on october 2006:
  * on Compte
    - numero become numero_interne
    - add code_pays (ex K)
    - add code etab (code etablissement), ex 0101
    - add code_guichet
    - add numero_compte : international account number
    - add rib : ex 52
    - add code_bic : ex SGBSSND0
    - add overdraft_facility O/N (Yes/No)
    - add swift_registered  O/N (Yes/No)
  * on Client
    - remove code_bic
    - zone_residence is now well completed, we should find country
         information. We should be a corresponding dictionary in order
         to set the right region
  """

  global property_map

  # Declarative security
  security = ClassSecurityInfo()


  ### This data structure associate a xml property to an ERP5 object property in certain conditions
  property_map = {
    # For example, in the sql export, we use for the first name of a person the
    # property 'nom', in ERP5 we use the property first_name
    'nom':[{
          'erp5_property': 'first_name'
        , 'conditions'   : {'erp5_portal_type':'Person'}
        }
      , {
         'erp5_property': 'title'
        , 'conditions'   : {'erp5_portal_type':'Organisation'}
        }],
    # For example, in the sql export, we use for the name of an organisation the
    # property 'nom', in ERP5 we use the property title
    'adresse': [{
        'erp5_property': 'default_address_street_address'
      , 'conditions'   : [{'erp5_portal_type':'Organisation'}
                         ,{'erp5_portal_type':'Person'}]
      }],
    'zone_residence': [{
        'erp5_property': 'default_address_region'
      , 'conditions'   : [{'erp5_portal_type':'Organisation'}
                         ,{'erp5_portal_type':'Person'}]
      }],
    'titre': [{
        'erp5_property': 'prefix'
      , 'conditions'   : {'erp5_portal_type':'Person'}
      }],
    'telephone': [{
        'erp5_property': 'default_telephone_number'
      , 'conditions'   : [{'erp5_portal_type':'Organisation'}
                         ,{'erp5_portal_type':'Person'}]
      }],
    'telex': [{
        'erp5_property': 'default_fax_number'
      , 'conditions'   : [{'erp5_portal_type':'Organisation'}
                         ,{'erp5_portal_type':'Person'}]
      }],
    'prenom': [{
        'erp5_property': 'last_name'
      , 'conditions'   : {'erp5_portal_type':'Person'}
      }],
    'date_naissance': [{
        'erp5_property': 'birthday'
      , 'conditions'   : {'erp5_portal_type':'Person'}
      }],
    'code_bic': [{
        'erp5_property': 'bic_code'
      , 'conditions'   : {'erp5_portal_type':'Organisation'}
      }],
    'intitule': [{
        'erp5_property': 'title'
      , 'conditions'   : {'erp5_portal_type':'Bank Account'}
      }],
    'montant_maxi': [{
        'erp5_property': 'operation_upper_limit'
      , 'conditions'   : {'erp5_portal_type':'Agent Privilege'}
      }],
    'description': [{
        'erp5_property': 'description'
      , 'conditions'   : {'erp5_portal_type':'Agent Privilege'}
      }],
    'inventory_title': [{
        'erp5_property': 'title'
      , 'conditions'   : {'erp5_portal_type':'Cash Inventory Group'}
      }],
    'title': [{
        'erp5_property': 'title'
      , 'conditions'   : {'erp5_portal_type':'Bank Account Inventory'}
      }],
    'amount': [{
        'erp5_property': 'inventory'
      , 'conditions'   : {'erp5_portal_type':'Bank Account Inventory Line'}
      }],
    'cle': [{
        'erp5_property': 'bank_account_key'
      , 'conditions'   : {'erp5_portal_type':'Bank Account'}
      }],
    }



  """
    Methods below are tools to use the property_map.
  """

  security.declarePrivate('buildConditions')
  def buildConditions(self, object):
    """
      Build a condition dictionnary based on the portal type.
      For example it will returns :
      {'erp5_portal_type':'Agent Privilege'}
    """
    dict = {}
    dict['erp5_portal_type'] = object.getPortalType()
    return dict

  security.declarePrivate('findPropertyMapItem')
  def findPropertyMapItem(self, xml_property_name, conditions):
    """
      Find the property_map item that match conditions
      It will returns for example :
     { 'xml_property' : 'nom'
      , 'erp5_property': 'first_name'
      , 'conditions'   : {'erp5_portal_type':'Person'} }
    """
    if property_map.has_key(xml_property_name):
      for item in property_map[xml_property_name]:
        c = item['conditions']
        if type(c) == type([]):
          if conditions in c:
            return item
        else:
          if conditions == c:
            return item
    return None



  security.declareProtected(Permissions.ModifyPortalContent, 'constructContent')
  def constructContent(self, object, object_id, docid, portal_type):
    """
      This is a redefinition of the original ERP5Conduit.constructContent function to
      create Baobab objects.

      This method is in charge to create a new object.
    """
    # Register some path in some variables
    erp5_site_path             = object.absolute_url(relative=1)
    person_module_object       = object.person_module
    organisation_module_object = object.organisation_module

    # Modules below are not always required
    #   (it depends of the nature of objects you want to synchronize)
    # So if a module to not exist, we set the value to None
    try:    cash_inventory_module = object.cash_inventory_module
    except AttributeError: cash_inventory_module = None
    try:    bank_account_inventory_module = object.bank_account_inventory_module
    except AttributeError: bank_account_inventory_module = None
    try:    currency_cash_module = object.currency_cash_module
    except AttributeError: currency_cash_module  = None

    subobject = None

    # Function to search the parent object where the new content must be construct.
    # Given parameter is the special encoded portal type that represent the path to
    #   the wanted destination.
    def findObjectFromSpecialPortalType(special_portal_type):
      # The first part or portal type, for example "Mandataire"
      source_portal_type = special_portal_type.split('_')[0]
      # The place where we should build,
      # [1:] is used to takes the full list except the first element
      # [::-1] is used in order to reverse the order
      # construction_location will be for example 40/Z000900001
      # (person with id 40 and account with id Z000900001
      construction_location = '/'.join(special_portal_type.split('_')[1:][::-1])
      parent_object = None
      for search_folder in ('person_module', 'organisation_module'):
        # full path : /person_module/40/Z000900001
        path = '/' + search_folder + '/' + construction_location
        parent_object_path = erp5_site_path + path
        try:
          # Get the object with the path
          parent_object = object.restrictedTraverse(parent_object_path)
	  if parent_object is not None:
	    break
        except ConflictError:
          raise
        except:
          LOG( 'BaobabConduit:'
             , 0
             , "expected %s parent object (%s) not found in %s" % ( source_portal_type
                                                                  , construction_location
                                                                  , search_folder
                                                                  )
             )
      if parent_object == None:
        LOG( 'BaobabConduit:'
           , 100
           , "expected %s parent object (%s) not found !" % (source_portal_type, construction_location)
           )
      else:
        LOG( 'BaobabConduit:'
           , 0
           , "%s parent object found at %s" % (source_portal_type, parent_object_path)
           )
      return parent_object

    ### handle client objects
    if portal_type.startswith('Client'):
      # This is a person object
      if portal_type[-3:] == 'PER':
        subobject = person_module_object.newContent( portal_type = 'Person'
                                                   , id          = object_id
                                                   )
        subobject.setCareerRole('client')
      else: # This is an organisation object
        subobject = organisation_module_object.newContent( portal_type = 'Organisation'
                                                         , id          = object_id
                                                         )
        subobject.setRole('client')

    ### handle bank account objects
    elif portal_type.startswith('Compte'):
      owner = findObjectFromSpecialPortalType(portal_type)
      if owner == None: return None
      subobject = owner.newContent( portal_type = 'Bank Account'
                                  , id          = object_id
                                  )
      # set the bank account owner as agent with no-limit privileges (only for persons)
      if owner.getPortalType() == 'Person':
        new_agent = subobject.newContent( portal_type = 'Agent'
                                        , id          = 'owner'
                                        )
        new_agent.setAgent(owner.getRelativeUrl())
        privileges = ( 'circularization'
                     , 'cash_out'
                     , 'withdrawal_and_payment'
                     , 'account_document_view'
                     , 'signature'
                     , 'treasury'
                     )
        for privilege in privileges:
          new_priv = new_agent.newContent(portal_type = 'Agent Privilege')
          new_priv.setAgentPrivilege(privilege)

    ### handle agent objects
    elif portal_type.startswith('Mandataire'):
      # Get the person or organisation thanks to the portal_type
      dest = findObjectFromSpecialPortalType(portal_type)
      if dest == None: return None
      subobject = dest.newContent( portal_type = 'Agent'
                                 , id          = object_id
                                 )
      # try to get the agent in the person module
      person = findObjectFromSpecialPortalType('Person_' + object_id)
      if person == None:
        person = person_module_object.newContent( portal_type = 'Person'
                                                , id          = object_id + 'a'
                                                )
      subobject.setAgent(person.getRelativeUrl())

    ### handle privilege objects
    elif portal_type.startswith('Pouvoir'):
      # Get the person or organisation thanks to the portal_type
      dest = findObjectFromSpecialPortalType(portal_type)
      if dest == None: return None
      subobject = dest.newContent( portal_type = 'Agent Privilege'
                                 , id          = object_id
                                 )

    ### handle inventory objects
    elif portal_type == 'Cash Inventory':
      if cash_inventory_module == None: return None
      subobject = cash_inventory_module.newContent( portal_type = 'Cash Inventory Group'
                                                  , id          = object_id
                                                  )

    ### handle inventory details objects
    elif portal_type == 'Cash Inventory Detail':
      if currency_cash_module == None: return None
      # get currency and vault informations by analizing the id
      id_items = object_id.split('_')
      if len(id_items) != 5:
        LOG( 'BaobabConduit:'
           , 100
           , "Cash Inventory Detail object has a wrong id (%s) !" % (object_id)
           )
        return None
      cell_id        = id_items[0]
      agency_code    = id_items[1]
      inventory_code = id_items[2]
      vault_code     = id_items[3]
      currency_id    = id_items[4]
      # get the path to the vault_code
      vault_path = self.getVaultPathFromCodification( object         = object
                                                    , agency_code    = agency_code
                                                    , inventory_code = inventory_code
                                                    , vault_code     = vault_code
                                                    , currency_id    = currency_id
                                                    )
      if vault_path in (None, ''):
        LOG( 'BaobabConduit:'
           , 100
           , "can't find a path to the vault '%s/%s/%s' !" % (agency_code, inventory_code, vault_code)
           )
        return None
      # try to find an existing inventory with the same price currency and vault
      inventory_list = object.contentValues(filter={'portal_type': 'Cash Inventory'})
      new_inventory = None
      for inventory in inventory_list:
        inventory_currency = inventory.getPriceCurrencyId()
        inventory_vault    = inventory.getDestination()
        if inventory_currency not in (None, '') and \
           inventory_vault    not in (None, '') and \
           inventory_currency == currency_id    and \
           inventory_vault    == vault_path     :
          new_inventory = inventory
          LOG( 'BaobabConduit:'
             , 0
             , "previous Cash Inventory found (%s) !" % (repr(new_inventory))
             )
          break
      # no previous inventory found, create one
      if new_inventory == None:
        new_inventory = object.newContent(portal_type = 'Cash Inventory')
        new_inventory.setPriceCurrency('currency_module/' + currency_id)
        new_inventory.setDestination(vault_path)
      subobject = new_inventory

    ### handle bank account inventory objects
    elif portal_type == 'Bank Account Inventory':
      if bank_account_inventory_module == None: return None
      subobject = bank_account_inventory_module.newContent( portal_type = 'Bank Account Inventory'
                                                          , id          = object_id
                                                          )

    ### handle bank account inventory line objects
    elif portal_type == 'Bank Account Inventory Line':
      subobject = object.newContent( portal_type = 'Bank Account Inventory Line'
                                   , id          = object_id
                                   )

    return subobject



  security.declareProtected(Permissions.ModifyPortalContent, 'editDocument')
  def editDocument(self, object=None, **kw):
    """
      This function transfer datas from the dictionary to the baobab document
      object given in parameters.
    """

    if object == None: return

    ### Cash Inventory objects needs two properties to generate the vault path
    if object.getPortalType() == 'Cash Inventory Group':
      vault_path = self.getVaultPathFromCodification( object         = object
                                                    , agency_code    = kw['agency_code']
                                                    , inventory_code = kw['inventory_code']
                                                    )
      object.setDestination(vault_path)

    ### Cash Inventory Detail objects needs all properties to create and update the cell matrix
    # This part is only usefull for cash inventory, it is not used for most portal types
    if object.getPortalType() == 'Cash Inventory':
      # Make sure all variables will be defined
      quantity      = None
      cell_id       = None
      resource_type = None
      base_price    = None
      currency_name = None
      for k,v in kw.items():
        if k == 'quantity'     : quantity      = float(v)
        if k == 'cell_id'      : cell_id       = v
        if k == 'currency_type': resource_type = v
        if k == 'price'        : base_price    = float(v)
        if k == 'currency'     : currency_name = v
      # try to find an existing line with the same resource as the current cell
      if resource_type in ['BIL']:
        currency_portal_type = 'Banknote'
      elif resource_type in ['MON']:
        currency_portal_type = 'Coin'
      else:
        LOG( 'BaobabConduit:'
           , 100
           , "Cash Inventory Detail resource type can't be guess (%s) !" % (resource_type)
           )
        return None
      # get the list of existing currency to find the currency of the line
      line_currency_cash = None
      currency_cash_list = object.currency_cash_module.contentValues(filter={'portal_type': currency_portal_type})
      for currency_cash in currency_cash_list:
        # Check the price_currency_id and the base price to make sure
        # we have the right currency
        if base_price    not in (None, '')                    and \
           currency_name not in (None, '')                    and \
           currency_cash.getBasePrice()       == base_price   and \
           currency_cash.getPriceCurrencyId() == currency_name:
          line_currency_cash = currency_cash
          break
      # no currency found
      if line_currency_cash == None:
        LOG( 'BaobabConduit:'
           , 100
           , "Currency '%s %s' not found for the Cash Inventory Detail !" % (base_price, currency_name)
           )
        return None
      # We are looking for an existing line
      inventory_lines = object.contentValues(filter={'portal_type': 'Cash Inventory Line'})
      new_line = None
      for line in inventory_lines:
        # getResourceValue returns the currency_cash, so if it is
        # equivalent to the currency_cash we have found, then we can
        # update the line
        if line.getResourceValue() == line_currency_cash:
          new_line = line
          break
      # no previous line found, create one
      if new_line == None:
        new_line = object.newContent(portal_type = 'Cash Inventory Line')
        new_line.setResourceValue(line_currency_cash)
        new_line.setPrice(line_currency_cash.getBasePrice())
      # get matrix variation values
      category_list = []
      # This is the 3 variation axes of the matrix
      base_cat_map = { 'variation'  : 'variation'
                     , 'letter_code': 'emission_letter'
                     , 'status_code': 'cash_status'
                     }
      for base_key in base_cat_map.keys():
        if base_key in kw.keys() and kw[base_key] not in ('', None):
          if base_key == 'status_code':
            status_table = { 'TVA' : 'valid'
                           , 'NEE' : 'new_emitted'
                           , 'NEU' : 'new_not_emitted'
                           , 'RTC' : 'retired'
                           , 'ATR' : 'to_sort'
                           , 'MUT' : 'mutilated'
                           , 'EAV' : 'to_ventilate'
                           }
            category = status_table[kw[base_key]]
          else:
            category = kw[base_key]
        else:
          category = 'not_defined'
        # We must have at least a category for each axis
        category_list.append(base_cat_map[base_key] + '/' + category)
      # update the matrix with this cell
      self.updateCashInventoryMatrix( line               = new_line
                                    , cell_category_list = category_list
                                    , quantity           = quantity
                                    , cell_uid           = cell_id
                                    )

    ### Bank Account Inventory Line objects needs two properties to get the right bank account object
    # This part is only usefull for bank account inventory line, it is not used for most portal types
    if object.getPortalType() == 'Bank Account Inventory Line':
      # Make sure variables will be defined
      currency_id         = None
      bank_account_number = None
      for k,v in kw.items():
        if k == 'currency'      : currency_id         = v
        if k == 'account_number': bank_account_number = v
      # try to find the bank account
      LOG( 'bank_account_number:'
                 , 200
                 , bank_account_number
                 )
      if bank_account_number != None:
        bank_account_object = None
        # We use here the catalog in order to find very quickly
        # all bank with a particular reference, so most of the time
        # we should get only 1 bank account
        bank_account_list = [x.getObject() for x in object.portal_catalog(
                               portal_type=('Bank Account'),
                               reference='%%%s%%' % bank_account_number)]
        LOG( 'bank_account_list:'
                 , 200
                 , bank_account_list
                 )
        # Make sure we have found the right bank account
        for bank_account in bank_account_list:
           if bank_account.getBankAccountNumber() == bank_account_number:
             bank_account_object = bank_account
             break
        if bank_account_object != None:
          # Se the right account on the inventory line
          object.setDestinationValue(bank_account_object)
          if currency_id != None:
            # verify or add the currency
            current_currency_id = bank_account_object.getPriceCurrencyId()
            # Make sure that the bank account will have a currency defined
            if current_currency_id in (None, ''):
              bank_account_object.setPriceCurrency('currency_module/' + currency_id)
            elif current_currency_id != currency_id:
              LOG( 'BaobabConduit inconsistency:'
                 , 200
                 , 'found bank account has not the same currency as expected'
                 )
        else:
            LOG( 'BaobabConduit inconsistency:'
               , 200
               , 'no bank account found'
               )


    """
      Here we use 2 generic way to update object properties :
        1. We try to use the property_map mapping to migrate a value from a property
             to another;
        2. If the latter fail, we try to find a method with a pre-defined name in
             this script to handle the value.
    """

    # Set properties of the destination baobab object
    for k,v in kw.items():
      # Try to find a translation rule in the property_map
      cond = self.buildConditions(object)
      map_item = self.findPropertyMapItem(k, cond)

      ### There is a translation rule, so call the right setProperty() method
      if map_item != None:
        # The method id can be for example 'setTitle'
        method_id = "set" + convertToUpperCase(map_item['erp5_property'])
        LOG( 'BaobabConduit:'
           , 0
           , "try to call object method %s on %s" % (repr(method_id), repr(object))
           )
        if v not in ('', None):
           # We look if the method exist
          if hasattr(object, method_id):
            # get the method itself
            method = getattr(object, method_id)
            # This call the method, this exactly the same thing
            # as calling directly : object.setTitle(v)
            method(v)
          else:
            LOG( 'BaobabConduit:'
               , 100
               , 'property map item don\'t match object properties'
               )

      ### No translation rule found, try to find a hard-coded translation method in the conduit
      else:
        # The method is generated with the type of the document and with the
        # name of the property. If the type of the document is 'Client' and the
        # property is nature_economique, then it will try to find a method
        # defined in this conduit 'editClientNatureEconomique'. This is very
        # usefull if we must do some particular conversion or some calculation
        # before editing an object. This is used when there is no simple
        # equivalent between sql table and ERP5.
        method_id = "edit%s%s" % (kw['type'].replace(' ', ''), convertToUpperCase(k))
        LOG( 'BaobabConduit:'
           , 0
           , "try to call conduit method %s on %s" % (repr(method_id), repr(object))
           )
        if v not in ('', None):
          if hasattr(self, method_id):
            # get the method itself
            method = getattr(self, method_id)
            # This call the method, this exactly the same thing
            # as calling directly : self.editClientNatureEconomique(object,v)
            method(object, v)
          else:
            LOG( 'BaobabConduit:'
               , 100
               , "there is no method to handle <%s>%s</%s> data" % (k,repr(v),k)
               )




  """
    All functions below are defined to set a document's property to a value
    given in parameters.
    The name of those functions are chosen to help the transfert of datas
    from a given XML format to standard Baobab objects.
  """

  ### Client-related-properties functions

  def editClientCategorie(self, document, value):
    if document.getPortalType() == 'Organisation':
      id_table = { 'BIF': 'institution/world/bank'
                 , 'PFR': 'institution/world/institution'
                 , 'ICU': 'institution/local/common'
                 , 'BET': 'institution/local/institution'
                 , 'ETF': 'institution/local/bank'
                 , 'BTR': 'treasury/national'
                 , 'ORP': 'treasury/other'
                 , 'ORI': 'organism/international'
                 , 'ORR': 'organism/local'
                 , 'COR': 'intermediaries'
                 , 'DIV': 'depositories/various'
                 , 'DER': 'depositories/savings'
                 , 'DAU': 'depositories/other'
                 }
      document.setActivity('banking_finance/' + id_table[value])
    else:
      LOG('BaobabConduit:', 0, 'Person\'s category ignored')

  def editClientNatureEconomique(self, document, value):
    if document.getPortalType() == 'Organisation':
      # build the economical class category path
      c = ''
      path = ''
      for i in value[1:]:
        c += i
        if c == '13':
          path += '/S13'
          if value != 'S13':
            path += '/' + value
          break
        path += '/S' + c
      document.setEconomicalClass(path)
    else:
      LOG( 'BaobabConduit inconsistency:'
         , 200
         , 'a non-Organisation client can\'t have an economical class'
         )

  def editClientSituationMatrimoniale(self, document, value):
    """
    Here we can convert data from sql to data in ERP5 thanks
    to a simple dictionnary: the id_table.
    """
    if document.getPortalType() == 'Person':
      id_table = { 'VEU' : 'widowed'
                 , 'DIV' : 'divorced'
                 , 'MAR' : 'married'
                 , 'CEL' : 'never_married'
                 }
      document.setMaritalStatus(id_table[value])
    else:
      LOG( 'BaobabConduit inconsistency:'
         , 200
         , 'a non-Person client can\'t have a marital status'
         )

  def editClientCode(self, document, value):
    pass




  ### BankAccount-related-properties functions

  def editCompteDevise(self, document, value):
    # Convert compte_devise to price_currency
    document.setPriceCurrency('currency_module/' + value)

  def editCompteDateOuverture(self, document, value):
    # Convert date_ouverture to start_date and stop_date
    if document.getStopDate() in ('', None):
      document.setStopDate(str(datetime.datetime.max))
    document.setStartDate(value)

  def editCompteDateFermeture(self, document, value):
    # Convert date_firemeture to start_date and stop_date
    if document.getStartDate() in ('', None):
      document.setStartDate(str(datetime.datetime.min))
    document.setStopDate(value)

  def editCompteNumero(self, document, value):
    # Here we have several properties in ERP5 for only
    # one property in sql, so we need this particular method.
    document.setBankCode(value[0])
    document.setBranch(value[1:3])
    document.setBankAccountNumber(value)



  ### Agent-related-properties functions

  def editMandataireNom(self, document, value):
    # Convert mandataire_nom to first_name
    old_value = document.getAgentValue().getFirstName()
    new_value = value
    if old_value != new_value:
      LOG( 'BaobabConduit:'
         , 200
         , 'old value of agent first name (%s) was replaced by a new one (%s)' % (old_value, new_value)
         )
      document.getAgentValue().setFirstName(new_value)

  def editMandatairePrenom(self, document, value):
    # Convert mandataire_prenom to last_name
    old_value = document.getAgentValue().getLastName()
    new_value = value
    if old_value != new_value:
      LOG( 'BaobabConduit:'
         , 200
         , 'old value of agent last name (%s) was replaced by a new one (%s)' % (old_value, new_value)
         )
      document.getAgentValue().setLastName(new_value)

  def editMandataireService(self, document, value):
    # Convert mandataire_service to an assignment
    assignment = document.getAgentValue().newContent( portal_type = 'Assignment'
                                                    , id          = 'service'
                                                    )
    assignment.setGroup(value)
    return

  def editMandataireFonction(self, document, value):
    # Convert mandataire_function to a career grade
    document.getAgentValue().setCareerGrade(value)
    return

  def editMandataireTelephone(self, document, value):
    # Convert mandataire_telephone to default_telephone_number
    old_value = document.getAgentValue().getDefaultTelephoneNumber()
    new_value = value
    if old_value != new_value:
      LOG( 'BaobabConduit:'
         , 200
         , "old value of agent's telephone (%s) was replaced by a new one (%s)" % (old_value, new_value)
         )
      document.getAgentValue().setDefaultTelephoneNumber(new_value)

  def editMandataireDateCreation(self, document, value):
    # Convert mandataire_date_creation to stop_date and start_date
    if document.getStopDate() in ('', None):
      document.setStopDate(str(datetime.datetime.max))
    document.setStartDate(value)



  ### AgentPrivilege-related-properties functions

  def editPouvoirCategorie(self, document, value):
    # Convert pouvoir_categorie to agent_privilege property
    id_table = { 'COM' : 'clearing'
               , 'CIR' : 'circularization'
               , 'REM' : 'cash_out'
               , 'RET' : 'withdrawal_and_payment'
               , 'RTE' : 'account_document_view'
               , 'SIG' : 'signature'
               , 'TRE' : 'treasury'
               }
    document.setAgentPrivilege(id_table[value])

  def editPouvoirDateDebut(self, document, value):
    # Convert pouvoir_date_debut to start_date and stop_date properties
    if document.getStopDate() in ('', None):
      document.setStopDate(str(datetime.datetime.max))
    document.setStartDate(value)

  def editPouvoirDateFin(self, document, value):
    # Convert pouvoir_date_fin to start_date and stop_date properties
    if document.getStartDate() in ('', None):
      document.setStartDate(str(datetime.datetime.min))
    document.setStopDate(value)



  ### CashInventory-related-properties functions

  def editCashInventoryInventoryDate(self, document, value):
    # Convert cash_inventory_inventory_date to stop_date property
    if value in ('', None):
      date = str(datetime.datetime.max)
    else:
      # Convert french date to strandard date
      date_items = value.split('/')
      day   = date_items[0]
      month = date_items[1]
      year  = date_items[2]
      date  = '/'.join([year, month, day])
    document.setStopDate(date)

  def getVaultPathFromCodification( self, object, agency_code=None, inventory_code=None, vault_code=None, currency_id=None):
    """
    This method get many parameters and try to find a category
    corresponding with parameters.

    For example if agency_code=A00, this function will returns
    site/aaa/bbb/ccc
    """
    if agency_code in (None, ''):
      return None
    category_tool = object.portal_categories
    # Get the site path to agency
    agency_path = None
    site_base_object = category_tool.resolveCategory('site')
    # XXX Warning, we should use the catalog in order to retrieve this
    # first level. It will go faster. But we need the codification in
    # the catalog table

    # Parse the category tree in order to find the category corresponding
    # to the agency
    for site_item in site_base_object.getCategoryChildItemList(base=1)[1:]:
      site_path = site_item[1]
      site_object = category_tool.resolveCategory(site_path)
      if site_object.getPortalType() == 'Category':
        site_code = site_object.getCodification()
        if site_code not in (None, '') and site_code.upper() == agency_code.upper():
          agency_path = site_path
          break
    if inventory_code in (None, ''):
      return agency_path
    # Get the site path corresponding to the inventory type
    inventory_path = None
    agency_site_object = site_object
    # Parse the category tree (from the level of the agency) in order to
    # find the category corresponding to the inventory
    for agency_sub_item in agency_site_object.getCategoryChildItemList(base=1)[1:]:
      agency_sub_item_path   = agency_sub_item[1]
      agency_sub_item_object = category_tool.resolveCategory(agency_sub_item_path)
      agency_sub_item_vault  = agency_sub_item_object.getVaultType()
      if agency_sub_item_vault not in (None, ''):
        vault_type_path        = 'vault_type/' + agency_sub_item_vault
        vault_type_object      = category_tool.resolveCategory(vault_type_path)
        vault_type_code        = vault_type_object.getCodification()
        if vault_type_code not in (None, '') and vault_type_code.upper() == inventory_code.upper():
          inventory_path = agency_sub_item_path
          break
    if vault_code in (None, ''):
      return inventory_path
    # Get the site path corresponding to the vault code
    vault_path = None
    vault_site_object = agency_sub_item_object
    # Parse the category tree (from the level of the inventory) in order to
    # find the category corresponding to the vault
    for vault_sub_item in vault_site_object.getCategoryChildItemList(base=1)[1:]:
      vault_sub_item_path   = vault_sub_item[1]
      vault_sub_item_object = category_tool.resolveCategory(vault_sub_item_path)
      vault_sub_item_code   = vault_sub_item_object.getCodification()
      if vault_sub_item_code not in (None, '') and vault_sub_item_code.upper() == vault_code.upper():
        vault_path = vault_sub_item_path
        break
    if currency_id in (None, ''):
      return vault_path
    # Get the site path corresponding to the currency-related-subvault
    currency_object = category_tool.currency_module[currency_id]
    currency_title  = currency_object.getTitle()
    currency_vault_path = None
    vault_object = vault_sub_item_object
    # Parse the category tree (from the level of the vault) in order to
    # find the category corresponding to the currency
    for currency_vault_item in vault_object.getCategoryChildItemList(base=1)[1:]:
      currency_vault_item_path   = currency_vault_item[1]
      currency_vault_item_object = category_tool.resolveCategory(currency_vault_item_path)
      currency_vault_item_title  = currency_vault_item_object.getTitle()
      if currency_vault_item_title not in (None, '') and currency_vault_item_title.upper() == currency_title.upper():
        currency_vault_path = currency_vault_item_path
        break
    if currency_vault_path == None:
      return vault_path
    return currency_vault_path



  ### CashInventoryDetail-related-properties functions

  def updateCashInventoryMatrix(self, line, cell_category_list, quantity, cell_uid):
    base_id = 'movement'
    base_category_list = [ 'emission_letter'
                         , 'variation'
                         , 'cash_status'
                         ]

    old_line_category_list   = line.getVariationCategoryList()
    messy_line_category_list = cell_category_list + old_line_category_list

    sorted_line_base_category_list = []
    sorted_line_category_list = []
    sorted_cell_category_list = []
    sorted_cell_range = []

    # cell_category_list must have the same base category order of cell_range base category
    for base_category in base_category_list:

      # generate the sorted line categories
      for category in messy_line_category_list:
        if category.startswith(base_category + '/') and category not in sorted_line_category_list:
          sorted_line_category_list.append(category)

      # generate the sorted cell range
      base_group = []
      for category in messy_line_category_list:
        if category.startswith(base_category + '/') and category not in base_group:
          base_group.append(category)
      sorted_cell_range.append(base_group)
      # generate the sorted base category
      if len(base_group) > 0:
        sorted_line_base_category_list.append(base_category)

      # generate the sorted cell variation categories
      for category in cell_category_list:
        if category.startswith(base_category + '/') and category not in sorted_cell_category_list:
          sorted_cell_category_list.append(category)

    # update line variation categories
    line.setVariationBaseCategoryList(sorted_line_base_category_list)
    line.setVariationCategoryList(sorted_line_category_list)
    line.setCellRange(base_id = base_id, *sorted_cell_range)
    # create the cell
    kwd = { 'base_id'    : base_id
          , 'portal_type': 'Cash Inventory Cell'
          }
    new_cell = line.newCell(*sorted_cell_category_list, **kwd)
    new_cell.edit( mapped_value_property_list         = ('price', 'inventory')
                 , force_update                       = 1
                 , inventory                          = quantity
                 , membership_criterion_category_list = sorted_cell_category_list
                 , category_list                      = sorted_cell_category_list
                 , title                              = cell_uid
                 )



  ### BankAccountInventory-related-properties functions

  def editBankAccountInventoryAgencyCode(self, document, value):
    # Convert bank_account_inventory_agency_code to a destination
    agency_path = self.getVaultPathFromCodification( object      = document
                                                   , agency_code = value
                                                   )
    document.setDestination(agency_path)

  def editBankAccountInventoryDate(self, document, value):
    # Convert bank_account_inventory_date to stop_date property
    if value in ('', None):
      date = str(datetime.datetime.max)
    else:
      # Convert french date to strandard date
      date_items = value.split('/')
      day   = date_items[0]
      month = date_items[1]
      year  = date_items[2]
      date  = '/'.join([year, month, day])
    document.setStopDate(date)

