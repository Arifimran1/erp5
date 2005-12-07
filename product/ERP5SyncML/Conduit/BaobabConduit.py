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

  global property_map

  # Declarative security
  security = ClassSecurityInfo()


  ### This data structure associate a xml property to an ERP5 object property in certain conditions
  property_map = \
    [ { 'xml_property' : 'nom'
      , 'erp5_property': 'first_name'
      , 'conditions'   : {'erp5_portal_type':'Person'}
      }
    , { 'xml_property' : 'nom'
      , 'erp5_property': 'title'
      , 'conditions'   : {'erp5_portal_type':'Organisation'}
      }
    , { 'xml_property' : 'adresse'
      , 'erp5_property': 'default_address_street_address'
      , 'conditions'   : [{'erp5_portal_type':'Organisation'}
                         ,{'erp5_portal_type':'Person'}]
      }
    , { 'xml_property' : 'zone_residence'
      , 'erp5_property': 'default_address_region'
      , 'conditions'   : [{'erp5_portal_type':'Organisation'}
                         ,{'erp5_portal_type':'Person'}]
      }
    , { 'xml_property' : 'titre'
      , 'erp5_property': 'prefix'
      , 'conditions'   : {'erp5_portal_type':'Person'}
      }
    , { 'xml_property' : 'telephone'
      , 'erp5_property': 'default_telephone_number'
      , 'conditions'   : [{'erp5_portal_type':'Organisation'}
                         ,{'erp5_portal_type':'Person'}]
      }
    , { 'xml_property' : 'telex'
      , 'erp5_property': 'default_fax_number'
      , 'conditions'   : [{'erp5_portal_type':'Organisation'}
                         ,{'erp5_portal_type':'Person'}]
      }
    , { 'xml_property' : 'prenom'
      , 'erp5_property': 'last_name'
      , 'conditions'   : {'erp5_portal_type':'Person'}
      }
    , { 'xml_property' : 'date_naissance'
      , 'erp5_property': 'birthday'
      , 'conditions'   : {'erp5_portal_type':'Person'}
      }
    , { 'xml_property' : 'code_bic'
      , 'erp5_property': 'bic_code'
      , 'conditions'   : {'erp5_portal_type':'Organisation'}
      }

    , { 'xml_property' : 'intitule'
      , 'erp5_property': 'title'
      , 'conditions'   : {'erp5_portal_type':'Bank Account'}
      }

    , { 'xml_property' : 'montant_maxi'
      , 'erp5_property': 'operation_upper_limit'
      , 'conditions'   : {'erp5_portal_type':'Agent Privilege'}
      }
    , { 'xml_property' : 'description'
      , 'erp5_property': 'description'
      , 'conditions'   : {'erp5_portal_type':'Agent Privilege'}
      }

    , { 'xml_property' : 'inventory_title'
      , 'erp5_property': 'title'
      , 'conditions'   : {'erp5_portal_type':'Cash Inventory Group'}
      }

    , { 'xml_property' : 'title'
      , 'erp5_property': 'title'
      , 'conditions'   : {'erp5_portal_type':'Bank Account Inventory'}
      }

    , { 'xml_property' : 'amount'
      , 'erp5_property': 'inventory'
      , 'conditions'   : {'erp5_portal_type':'Bank Account Inventory Line'}
      }
    ]



  """
    Methods below are tools to use the property_map.
  """

  security.declarePrivate('buildConditions')
  def buildConditions(self, object):
    """
      Build a condition dictionnary
    """
    dict = {}
    dict['erp5_portal_type'] = object.getPortalType()
    return dict

  security.declarePrivate('findPropertyMapItem')
  def findPropertyMapItem(self, xml_property_name, conditions):
    """
      Find the property_map item that match conditions
    """
    for item in property_map:
      if item['xml_property'] == xml_property_name:
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
    """
    erp5_site_path             = object.absolute_url(relative=1)
    person_module_object       = object.person_module
    organisation_module_object = object.organisation_module

    # Modules below are not always required
    #   (it depends of the nature of objects you want to synchronize)
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
      source_portal_type = special_portal_type.split('_')[0]
      construction_location = '/'.join(special_portal_type.split('_')[1:][::-1])
      parent_object = None
      for search_folder in ('person_module', 'organisation_module'):
        path = '/' + search_folder + '/' + construction_location
        parent_object_path = erp5_site_path + path
        try:
          parent_object = object.restrictedTraverse(parent_object_path)
        except ConflictError:
          raise
        except:
          LOG( 'BaobabConduit:'
             , 100
             , "parent object of '%s' not found in %s" % (source_portal_type, parent_object_path)
             )
      if parent_object == None:
        LOG( 'BaobabConduit:'
           , 100
           , "parent object of '%s' not found !" % (source_portal_type)
           )
      else:
        LOG( 'BaobabConduit:'
           , 0
           , "parent object of '%s' found (%s)" % (source_portal_type, repr(parent_object))
           )
      return parent_object

    ### handle client objects
    if portal_type.startswith('Client'):
      if portal_type[-3:] == 'PER':
        subobject = person_module_object.newContent( portal_type = 'Person'
                                                   , id          = object_id
                                                   )
        subobject.setCareerRole('client')
      else:
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
        new_inventory.setPriceCurrency('currency/' + currency_id)
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

    """
      Write here the code that require to combine more than one property from
      the **kw dictionnary in order to put the right value in object attributes.
    """

    ### Cash Inventory objects needs two properties to generate the vault path
    if object.getPortalType() == 'Cash Inventory Group':
      vault_path = self.getVaultPathFromCodification( object         = object
                                                    , agency_code    = kw['agency_code']
                                                    , inventory_code = kw['inventory_code']
                                                    )
      object.setDestination(vault_path)

    ### Cash Inventory Detail objects needs all properties to create and update the cell matrix
    if object.getPortalType() == 'Cash Inventory':
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
      # search for lines
      inventory_lines = object.contentValues(filter={'portal_type': 'Cash Inventory Line'})
      new_line = None
      for line in inventory_lines:
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
        category_list.append(base_cat_map[base_key] + '/' + category)
      # update the matrix with this cell
      self.updateCashInventoryMatrix( line               = new_line
                                    , cell_category_list = category_list
                                    , quantity           = quantity
                                    , cell_uid           = cell_id
                                    )

    ### Bank Account Inventory Line objects needs two properties to get the right bank account object
    if object.getPortalType() == 'Bank Account Inventory Line':
      currency_id         = None
      bank_account_number = None
      for k,v in kw.items():
        if k == 'currency'      : currency_id         = v
        if k == 'account_number': bank_account_number = v
      # try to find the bank account
      if bank_account_number != None:
        customer_list = object.person_module.contentValues(filter={'portal_type': 'Person'}) + \
                        object.organisation_module.contentValues(filter={'portal_type': 'Organisation'})
        bank_account_object = None
        for customer in customer_list:
          for bank_account in customer.contentValues(filter={'portal_type': 'Bank Account'}):
            if bank_account.getBankAccountNumber() == bank_account_number:
              # found !
              bank_account_object = bank_account
              break
          if bank_account_object != None:
            break
        if bank_account_object != None:
          object.setDestinationValue(bank_account_object)
          if currency_id != None:
            # verify or add the currency
            current_currency_id = bank_account_object.getPriceCurrencyId()
            if current_currency_id in (None, ''):
              bank_account_object.setPriceCurrency('currency/' + currency_id)
            elif current_currency_id != currency_id:
              LOG( 'BaobabConduit inconsistency:'
                 , 200
                 , 'found bank account has not the same currency as expected'
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
        method_id = "set" + convertToUpperCase(map_item['erp5_property'])
        LOG( 'BaobabConduit:'
           , 0
           , "try to call object method %s on %s" % (repr(method_id), repr(object))
           )
        if v not in ('', None):
          if hasattr(object, method_id):
            method = getattr(object, method_id)
            method(v)
          else:
            LOG( 'BaobabConduit:'
               , 100
               , 'property map item don\'t match object properties'
               )

      ### No translation rule found, try to find a hard-coded translation method in the conduit
      else:
        method_id = "edit%s%s" % (kw['type'].replace(' ', ''), convertToUpperCase(k))
        LOG( 'BaobabConduit:'
           , 0
           , "try to call conduit method %s on %s" % (repr(method_id), repr(object))
           )
        if v not in ('', None):
          if hasattr(self, method_id):
            method = getattr(self, method_id)
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



  ### BankAccount-related-properties functions

  def editCompteDevise(self, document, value):
    document.setPriceCurrency('currency/' + value)

  def editCompteDateOuverture(self, document, value):
    if document.getStopDate() in ('', None):
      document.setStopDate(str(datetime.datetime.max))
    document.setStartDate(value)

  def editCompteDateFermeture(self, document, value):
    if document.getStartDate() in ('', None):
      document.setStartDate(str(datetime.datetime.min))
    document.setStopDate(value)

  def editCompteNumero(self, document, value):
    document.setBankCode(value[0])
    document.setBranch(value[1:3])
    document.setBankAccountNumber(value)



  ### Agent-related-properties functions

  def editMandataireNom(self, document, value):
    old_value = document.getAgentValue().getFirstName()
    new_value = value
    if old_value != new_value:
      LOG( 'BaobabConduit:'
         , 200
         , 'old value of agent first name (%s) was replaced by a new one (%s)' % (old_value, new_value)
         )
      document.getAgentValue().setFirstName(new_value)

  def editMandatairePrenom(self, document, value):
    old_value = document.getAgentValue().getLastName()
    new_value = value
    if old_value != new_value:
      LOG( 'BaobabConduit:'
         , 200
         , 'old value of agent last name (%s) was replaced by a new one (%s)' % (old_value, new_value)
         )
      document.getAgentValue().setLastName(new_value)

  def editMandataireService(self, document, value):
    assignment = document.getAgentValue().newContent( portal_type = 'Assignment'
                                                    , id          = 'service'
                                                    )
    assignment.setGroup(value)
    return

  def editMandataireFonction(self, document, value):
    document.getAgentValue().setCareerGrade(value)
    return

  def editMandataireTelephone(self, document, value):
    old_value = document.getAgentValue().getDefaultTelephoneNumber()
    new_value = value
    if old_value != new_value:
      LOG( 'BaobabConduit:'
         , 200
         , "old value of agent's telephone (%s) was replaced by a new one (%s)" % (old_value, new_value)
         )
      document.getAgentValue().setDefaultTelephoneNumber(new_value)

  def editMandataireDateCreation(self, document, value):
    if document.getStopDate() in ('', None):
      document.setStopDate(str(datetime.datetime.max))
    document.setStartDate(value)



  ### AgentPrivilege-related-properties functions

  def editPouvoirCategorie(self, document, value):
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
    if document.getStopDate() in ('', None):
      document.setStopDate(str(datetime.datetime.max))
    document.setStartDate(value)

  def editPouvoirDateFin(self, document, value):
    if document.getStartDate() in ('', None):
      document.setStartDate(str(datetime.datetime.min))
    document.setStopDate(value)



  ### CashInventory-related-properties functions

  def editCashInventoryInventoryDate(self, document, value):
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
    if agency_code in (None, ''):
      return None
    category_tool = object.portal_categories
    # Get the site path to agency
    agency_path = None
    site_base_object = category_tool.resolveCategory('site')
    for site_item in site_base_object.getCategoryChildLogicalPathItemList(base=1)[1:]:
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
    for agency_sub_item in agency_site_object.getCategoryChildLogicalPathItemList(base=1)[1:]:
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
    for vault_sub_item in vault_site_object.getCategoryChildLogicalPathItemList(base=1)[1:]:
      vault_sub_item_path   = vault_sub_item[1]
      vault_sub_item_object = category_tool.resolveCategory(vault_sub_item_path)
      vault_sub_item_code   = vault_sub_item_object.getCodification()
      if vault_sub_item_code not in (None, '') and vault_sub_item_code.upper() == vault_code.upper():
        vault_path = vault_sub_item_path
        break
    if currency_id in (None, ''):
      return vault_path
    # Get the site path corresponding to the currency-related-subvault
    currency_object = category_tool.currency[currency_id]
    currency_title  = currency_object.getTitle()
    currency_vault_path = None
    vault_object = vault_sub_item_object
    for currency_vault_item in vault_object.getCategoryChildLogicalPathItemList(base=1)[1:]:
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
    agency_path = self.getVaultPathFromCodification( object      = document
                                                   , agency_code = value
                                                   )
    document.setDestination(agency_path)

  def editBankAccountInventoryDate(self, document, value):
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
