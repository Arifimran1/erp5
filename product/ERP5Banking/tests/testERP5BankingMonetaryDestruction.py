##############################################################################
#
# Copyright (c) 2005-2006 Nexedi SARL and Contributors. All Rights Reserved.
#                    Alexandre Boeglin <alex_AT_nexedi_DOT_com>
#                    Kevin Deldycke <kevin_AT_nexedi_DOT_com>
#                    Aurelien Calonne <aurel@nexedi.com>
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


# import requested python module
import os
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from Products.ERP5Type.tests.Sequence import SequenceList
from Products.DCWorkflow.DCWorkflow import Unauthorized, ValidationFailed
from Testing.ZopeTestCase.PortalTestCase import PortalTestCase
from Products.ERP5Banking.tests.TestERP5BankingMixin import TestERP5BankingMixin

# Needed in order to have a log file inside the current folder
os.environ['EVENT_LOG_FILE']     = os.path.join(os.getcwd(), 'zLOG.log')
# Define the level of log we want, here is all
os.environ['EVENT_LOG_SEVERITY'] = '-300'

# Define how to launch the script if we don't use runUnitTest script
if __name__ == '__main__':
  execfile(os.path.join(sys.path[0], 'framework.py'))
  

class TestERP5BankingMonetaryDestruction(TestERP5BankingMixin, ERP5TypeTestCase):
  """
    This class is a unit test to check the module of Monetary Destruction

    Here are the following step that will be done in the test :
  
    - before the test, we need to create some movements that will put resources in the source

    - create a monetary destruction
    - check it has been created correctly
    - check source and destination (current == future)

    - create a "Note Line" (billetage)
    - check it has been created correctly
    - check the total amount

    - create a second Line
    - check it has been created correctly
    - check the total amount

    - create an invalid Line (quantity > available at source)
    - check that the system behaves correctly

    - pass "confirm_action" transition
    - check that the new state is confirmed
    - check that the source has been debited correctly (current < future)
    - check amount, lines, ...

    - pass "deliver_action" transition
    - check that the new state is delivered
    - check that the destination has been credited correctly (current == future)
  """

  login = PortalTestCase.login

  # pseudo constants
  RUN_ALL_TEST = 1 # we want to run all test
  QUIET = 0 # we don't want the test to be quiet

  def getTitle(self):
    """
      Return the title of the test
    """
    return "ERP5BankingMonetaryDestruction"


  def getBusinessTemplateList(self):
    """
      Return the list of business templates we need to run the test.
      This method is called during the initialization of the unit test by
      the unit test framework in order to know which business templates
      need to be installed to run the test on.
    """
    return ('erp5_base'
            , 'erp5_trade'
            , 'erp5_accounting'
            , 'erp5_banking_core' # erp5_banking_core contains all generic methods for banking
            , 'erp5_banking_inventory'
            , 'erp5_banking_cash'
           )

  def getMonetaryDestructionModule(self):
    """
    Return the Monetary Destruction Module
    """
    return getattr(self.getPortal(), 'monetary_destruction_module', None)


  def afterSetUp(self):
    """
      Method called before the launch of the test to initialize some data
    """
    # Set some variables : 
    self.initDefaultVariable()
    # the monetary destruction module
    self.monetary_destruction_module = self.getMonetaryDestructionModule()
    
    self.createManagerAndLogin()

    # create categories
    self.createFunctionGroupSiteCategory()

    # create resources
    self.createBanknotesAndCoins()

    # Before the test, we need to input the inventory
    
    inventory_dict_line_1 = {'id' : 'inventory_line_1',
                             'resource': self.billet_10000,
                             'variation_id': ('emission_letter', 'cash_status', 'variation'),
                             'variation_value': ('emission_letter/p', 'cash_status/cancelled') + self.variation_list,
                             'quantity': self.quantity_10000}
    
    inventory_dict_line_2 = {'id' : 'inventory_line_2',
                             'resource': self.billet_5000,
                             'variation_id': ('emission_letter', 'cash_status', 'variation'),
                             'variation_value': ('emission_letter/p', 'cash_status/cancelled') + self.variation_list,
                             'quantity': self.quantity_5000}
    
    inventory_dict_line_for_externe_1 = {'id' : 'inventory_line_1',
                             'resource': self.billet_10000,
                             'variation_id': ('emission_letter', 'cash_status', 'variation'),
                             'variation_value': ('emission_letter/s', 'cash_status/cancelled') + self.variation_list,
                             'quantity': self.quantity_10000}
    
    inventory_dict_line_for_externe_2 = {'id' : 'inventory_line_2',
                             'resource': self.billet_5000,
                             'variation_id': ('emission_letter', 'cash_status', 'variation'),
                             'variation_value': ('emission_letter/s', 'cash_status/cancelled') + self.variation_list,
                             'quantity': self.quantity_5000}

    
    line_list = [inventory_dict_line_1, inventory_dict_line_2]    
    line_list_for_externe = [inventory_dict_line_for_externe_1, inventory_dict_line_for_externe_2]    
    self.source = self.paris.caveau.serre.encaisse_des_billets_retires_de_la_circulation
    self.source_for_externe = self.paris.caveau.externes.encaisse_des_externes
    ###self.destinat = self.paris.caveau.serre.encaisse_des_billets_detruits
    self.createCashInventory(source=None, destination=self.source, currency=self.currency_1,
                             line_list=line_list)
    self.createCashInventory(source=None, destination=self.source_for_externe, currency=self.currency_1,
                             line_list=line_list_for_externe)
    
    # now we need to create a user as Manager to do the test
    # in order to have an assigment defined which is used to do transition
    # Create an Organisation that will be used for users assignment
    self.checkUserFolderType()
    self.organisation = self.organisation_module.newContent(id='baobab_org', portal_type='Organisation',
                          function='banking', group='baobab',  site='testsite/paris')

    self.organisation_externe = self.organisation_module.newContent(id='baobab_org_externe', portal_type='Organisation',
                          function='banking', group='baobab',  site='testsite/madrid')

    # define the user
    user_dict = {
        'super_user' : [['Manager'], self.organisation, 'banking/comptable', 'baobab', 'testsite/paris']
    }
    # call method to create this user
    self.createERP5Users(user_dict)
    self.logout()
    self.login('super_user')

	


  def stepCheckObjects(self, sequence=None, sequence_list=None, **kwd):
    """
    Check that all the objects we created in afterSetUp or
    that were added by the business template and that we rely
    on are really here.
    """
    self.checkResourceCreated()
    # check that Monetary Destruction Module was created
    self.assertEqual(self.monetary_destruction_module.getPortalType(), 'Monetary Destruction Module')
    # check monetary destruction module is empty
    self.assertEqual(len(self.monetary_destruction_module.objectValues()), 0)


  def stepCheckInitialInventory(self, sequence=None, sequence_list=None, **kwd):
    """
    Check the initial inventory before any operations
    """
    self.simulation_tool = self.getSimulationTool()
    # check we have 5 banknotes of 10000 in source
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    # check we have 24 banknotes of 5000 in source
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)


  def stepCheckInitialInventoryForExterne(self, sequence=None, sequence_list=None, **kwd):
    """
    Check the initial inventory before any operations
    """
    self.simulation_tool = self.getSimulationTool()
    # check we have 5 banknotes of 10000 in source
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    # check we have 24 banknotes of 5000 in source
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)



  def stepCheckSource(self, sequence=None, sequence_list=None, **kwd):
    """
    Check inventory in source vault (source) before a confirm
    """
    # check we have 5 banknotes of 10000
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    # check we have 24 banknotes of 5000
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)
    
    

  def stepCheckSourceForExterne(self, sequence=None, sequence_list=None, **kwd):
    """
    Check inventory in source vault (source) before a confirm
    """
    # check we have 5 banknotes of 10000
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    # check we have 24 banknotes of 5000
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)



  def stepCreateMonetaryDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Create a monetary destruction document and check it
    """
    #print self.portal.portal_categories.objectIds()
    # Monetary Destruction has source(serre) for source, destinat (serre) for destination, and a price coresponding to the sum of banknote of 10000 and of 5000 ( (2*3) * 10000 + (5*7) * 5000 )
    self.monetary_destruction = self.monetary_destruction_module.newContent(id='monetary_destruction_1',
                                                                            portal_type='Monetary Destruction',
                                                                            source_value=self.source,
                                                                            destination_value=None,
                                                                            source_total_asset_price=110000.0,
                                                                            source_section_value=self.paris)
    # execute tic
    self.stepTic()
    # set source reference
    self.setDocumentSourceReference(self.monetary_destruction)
    # check source reference
    self.assertNotEqual(self.monetary_destruction.getSourceReference(), '')
    self.assertNotEqual(self.monetary_destruction.getSourceReference(), None)
    # check we have only one monetary destruction
    self.assertEqual(len(self.monetary_destruction_module.objectValues()), 1)
    # get the monetary destruction document
    self.monetary_destruction = getattr(self.monetary_destruction_module, 'monetary_destruction_1')
    # check its portal type
    self.assertEqual(self.monetary_destruction.getPortalType(), 'Monetary Destruction')
    # check that its source is source
    self.assertEqual(self.monetary_destruction.getSource(), 'site/testsite/paris/caveau/serre/encaisse_des_billets_retires_de_la_circulation')
    # check that its destination is destinat
    ##self.assertEqual(self.monetary_destruction.getDestination(), 'site/testsite/paris/caveau/serre/encaisse_des_billets_detruits')
    
    
  def stepCreateMonetaryDestructionForExterne(self, sequence=None, sequence_list=None, **kwd):
    """
    Create a monetary destruction document and check it
    """
    # Monetary Destruction has source(serre) for source, destinat (serre) for destination, and a price coresponding to the sum of banknote of 10000 and of 5000 ( (2*3) * 10000 + (5*7) * 5000 )
    self.monetary_destruction = self.monetary_destruction_module.newContent(id='monetary_destruction_1',
                                                                            portal_type='Monetary Destruction',
                                                                            source_value=self.source_for_externe,
                                                                            destination_value=None,
                                                                            source_total_asset_price=110000.0,
                                                                            source_section_value=self.madrid)
    # execute tic
    self.stepTic()
    # set source reference
    self.setDocumentSourceReference(self.monetary_destruction)
    # check source reference
    self.assertNotEqual(self.monetary_destruction.getSourceReference(), '')
    self.assertNotEqual(self.monetary_destruction.getSourceReference(), None)
    # check we have only one monetary destruction
    self.assertEqual(len(self.monetary_destruction_module.objectValues()), 1)
    # get the monetary destruction document
    self.monetary_destruction = getattr(self.monetary_destruction_module, 'monetary_destruction_1')
    # check its portal type
    self.assertEqual(self.monetary_destruction.getPortalType(), 'Monetary Destruction')
    # check that its source is source
    self.assertEqual(self.monetary_destruction.getSource(), 'site/testsite/paris/caveau/externes/encaisse_des_externes')
    # check that its destination is destinat
    ##self.assertEqual(self.monetary_destruction.getDestination(), 'site/testsite/paris/caveau/serre/encaisse_des_billets_detruits')    


  def stepCreateValidLine1(self, sequence=None, sequence_list=None, **kwd):
    """
    Create the monetary destruction line 1 with banknotes of 10000 and check it has been well created
    """
    # create the monetary destruction line
    self.addCashLineToDelivery(self.monetary_destruction, 'valid_line_1', 'Cash Delivery Line', self.billet_10000,
            ('emission_letter', 'cash_status', 'variation'), ('emission_letter/p', 'cash_status/cancelled') + self.variation_list,
            self.quantity_10000)
    # execute tic
    self.stepTic()
    # check there is only one line created
    self.assertEqual(len(self.monetary_destruction.objectValues()), 1)
    # get the monetary destruction line
    self.valid_line_1 = getattr(self.monetary_destruction, 'valid_line_1')
    # check its portal type
    self.assertEqual(self.valid_line_1.getPortalType(), 'Cash Delivery Line')
    # check the resource is banknotes of 10000
    self.assertEqual(self.valid_line_1.getResourceValue(), self.billet_10000)
    # chek the value of the banknote
    self.assertEqual(self.valid_line_1.getPrice(), 10000.0)
    # check the unit of banknote
    self.assertEqual(self.valid_line_1.getQuantityUnit(), 'quantity_unit/unit')
    # check we have two delivery cells: (one for year 1992 and one for 2003)
    self.assertEqual(len(self.valid_line_1.objectValues()), 2)
    # now check for each variation (years 1992 and 2003)
    for variation in self.variation_list:
      # get the delivery cell
      cell = self.valid_line_1.getCell('emission_letter/p', variation, 'cash_status/cancelled')
      # chek portal types
      self.assertEqual(cell.getPortalType(), 'Cash Delivery Cell')
      # check the banknote of the cell is banknote of 10000
      self.assertEqual(cell.getResourceValue(), self.billet_10000)
      # check the source vault is source
      self.assertEqual(cell.getSourceValue(), self.source)
      # check the destination vault is counter
      #self.assertEqual(cell.getDestinationValue(), self.destinat)
      if cell.getId() == 'movement_0_0_0':
        # check the quantity of banknote for year 1992 is 2
        self.assertEqual(cell.getQuantity(), 2.0)
      elif cell.getId() == 'movement_0_1_0':
        # check the quantity of banknote for year 2003 is 3
        self.assertEqual(cell.getQuantity(), 3.0)
      else:
        self.fail('Wrong cell created : %s' % cell.getId())


  def stepCreateValidLineForExterne1(self, sequence=None, sequence_list=None, **kwd):
    """
    Create the monetary destruction line 1 with banknotes of 10000 and check it has been well created
    """
    # create the monetary destruction line
    self.addCashLineToDelivery(self.monetary_destruction, 'valid_line_1', 'Cash Delivery Line', self.billet_10000,
            ('emission_letter', 'cash_status', 'variation'), ('emission_letter/s', 'cash_status/cancelled') + self.variation_list,
            self.quantity_10000)
    # execute tic
    self.stepTic()
    # check there is only one line created
    self.assertEqual(len(self.monetary_destruction.objectValues()), 1)
    # get the monetary destruction line
    self.valid_line_1 = getattr(self.monetary_destruction, 'valid_line_1')
    # check its portal type
    self.assertEqual(self.valid_line_1.getPortalType(), 'Cash Delivery Line')
    # check the resource is banknotes of 10000
    self.assertEqual(self.valid_line_1.getResourceValue(), self.billet_10000)
    # chek the value of the banknote
    self.assertEqual(self.valid_line_1.getPrice(), 10000.0)
    # check the unit of banknote
    self.assertEqual(self.valid_line_1.getQuantityUnit(), 'quantity_unit/unit')
    # check we have two delivery cells: (one for year 1992 and one for 2003)
    self.assertEqual(len(self.valid_line_1.objectValues()), 2)
    # now check for each variation (years 1992 and 2003)
    for variation in self.variation_list:
      # get the delivery cell
      cell = self.valid_line_1.getCell('emission_letter/s', variation, 'cash_status/cancelled')
      # chek portal types
      self.assertEqual(cell.getPortalType(), 'Cash Delivery Cell')
      # check the banknote of the cell is banknote of 10000
      self.assertEqual(cell.getResourceValue(), self.billet_10000)
      # check the source vault is source
      self.assertEqual(cell.getSourceValue(), self.source_for_externe)
      # check the destination vault is counter
      #self.assertEqual(cell.getDestinationValue(), self.destinat)
      if cell.getId() == 'movement_0_0_0':
        # check the quantity of banknote for year 1992 is 2
        self.assertEqual(cell.getQuantity(), 2.0)
      elif cell.getId() == 'movement_0_1_0':
        # check the quantity of banknote for year 2003 is 3
        self.assertEqual(cell.getQuantity(), 3.0)
      else:
        self.fail('Wrong cell created : %s' % cell.getId())



  def stepCheckSubTotal(self, sequence=None, sequence_list=None, **kwd):
    """
    Check the amount after the creation of monetary destruction line 1
    """
    # Check number of lines
    self.assertEqual(len(self.monetary_destruction.objectValues()), 1)
    # Check quantity of banknotes (2 for 1992 and 3 for 2003)
    self.assertEqual(self.monetary_destruction.getTotalQuantity(), 5.0)
    # Check the total price
    self.assertEqual(self.monetary_destruction.getTotalPrice(), 10000 * 5.0)


  def stepCreateValidLine2(self, sequence=None, sequence_list=None, **kwd):
    """
    Create the monetary destruction line 2 wiht banknotes of 5000 and check it has been well created
    """
    # create the line
    self.addCashLineToDelivery(self.monetary_destruction, 'valid_line_2', 'Cash Delivery Line', self.billet_5000,
            ('emission_letter', 'cash_status', 'variation'), ('emission_letter/p', 'cash_status/cancelled') + self.variation_list,
            self.quantity_5000)
    # execute tic
    self.stepTic()
    # check the number of lines (line1 + line2)
    self.assertEqual(len(self.monetary_destruction.objectValues()), 2)
    # get the second monetary destruction line
    self.valid_line_2 = getattr(self.monetary_destruction, 'valid_line_2')
    # check portal types
    self.assertEqual(self.valid_line_2.getPortalType(), 'Cash Delivery Line')
    # check the resource is banknotes of 5000
    self.assertEqual(self.valid_line_2.getResourceValue(), self.billet_5000)
    # check the value of banknote
    self.assertEqual(self.valid_line_2.getPrice(), 5000.0)
    # check the unit of banknote
    self.assertEqual(self.valid_line_2.getQuantityUnit(), 'quantity_unit/unit')
    # check we have two delivery cells: (one for year 1992 and one for 2003)
    self.assertEqual(len(self.valid_line_2.objectValues()), 2)
    for variation in self.variation_list:
      # get the delivery  cell
      cell = self.valid_line_2.getCell('emission_letter/p', variation, 'cash_status/cancelled')
      # check the portal type
      self.assertEqual(cell.getPortalType(), 'Cash Delivery Cell')
      if cell.getId() == 'movement_0_0_0':
        # check the quantity for banknote for year 1992 is 5
        self.assertEqual(cell.getQuantity(), 11.0)
      elif cell.getId() == 'movement_0_1_0':
        # check the quantity for banknote for year 2003 is 7
        self.assertEqual(cell.getQuantity(), 13.0)
      else:
        self.fail('Wrong cell created : %s' % cell.getId())


  def stepCreateValidLineForExterne2(self, sequence=None, sequence_list=None, **kwd):
    """
    Create the monetary destruction line 2 wiht banknotes of 5000 and check it has been well created
    """
    # create the line
    self.addCashLineToDelivery(self.monetary_destruction, 'valid_line_2', 'Cash Delivery Line', self.billet_5000,
            ('emission_letter', 'cash_status', 'variation'), ('emission_letter/s', 'cash_status/cancelled') + self.variation_list,
            self.quantity_5000)
    # execute tic
    self.stepTic()
    # check the number of lines (line1 + line2)
    self.assertEqual(len(self.monetary_destruction.objectValues()), 2)
    # get the second monetary destruction line
    self.valid_line_2 = getattr(self.monetary_destruction, 'valid_line_2')
    # check portal types
    self.assertEqual(self.valid_line_2.getPortalType(), 'Cash Delivery Line')
    # check the resource is banknotes of 5000
    self.assertEqual(self.valid_line_2.getResourceValue(), self.billet_5000)
    # check the value of banknote
    self.assertEqual(self.valid_line_2.getPrice(), 5000.0)
    # check the unit of banknote
    self.assertEqual(self.valid_line_2.getQuantityUnit(), 'quantity_unit/unit')
    # check we have two delivery cells: (one for year 1992 and one for 2003)
    self.assertEqual(len(self.valid_line_2.objectValues()), 2)
    for variation in self.variation_list:
      # get the delivery  cell
      cell = self.valid_line_2.getCell('emission_letter/s', variation, 'cash_status/cancelled')
      # check the portal type
      self.assertEqual(cell.getPortalType(), 'Cash Delivery Cell')
      if cell.getId() == 'movement_0_0_0':
        # check the quantity for banknote for year 1992 is 5
        self.assertEqual(cell.getQuantity(), 11.0)
      elif cell.getId() == 'movement_0_1_0':
        # check the quantity for banknote for year 2003 is 7
        self.assertEqual(cell.getQuantity(), 13.0)
      else:
        self.fail('Wrong cell created : %s' % cell.getId())



  def stepCreateInvalidLine(self, sequence=None, sequence_list=None, **kwd):
    """
    Create an invalid monetary destruction line and
    check the total with the invalid monetary destruction line
    """
    # create a line in which quanity of coin of 200 is higher that quantity available at source
    # here create a line with 12 (5+7) coin of 200 although the vault source has no coin of 200
    self.addCashLineToDelivery(self.monetary_destruction, 'invalid_line', 'Cash Delivery Line', self.piece_200,
            ('emission_letter', 'cash_status', 'variation'), ('emission_letter/p', 'cash_status/cancelled') + self.variation_list,
            self.quantity_200)
    # execute tic
    self.stepTic()
    # Check number of monetary destruction lines (line1 + line2 +invalid_line)
    self.assertEqual(len(self.monetary_destruction.objectValues()), 3)
    # Check quantity, same as checkTotal + coin of 200: 5 for 1992 and 7 for 2003
    self.assertEqual(self.monetary_destruction.getTotalQuantity(), 5.0 + 24.0 + 12)
    # chect the total price
    self.assertEqual(self.monetary_destruction.getTotalPrice(), 10000 * 5.0 + 5000 * 24.0 + 200 * 12)

  def stepTryPlannedMonetaryDestructionWithBadInventory(self, sequence=None, sequence_list=None, **kwd):
    """
    Try to confirm the monetary destruction with a bad monetary destruction line and
    check the try of confirm the monetary destruction with the invalid line has failed
    """
    # fix amount (10000 * 5.0 + 5000 * 24.0 + 200 * 12)
    
    self.monetary_destruction.setSourceTotalAssetPrice('172400.0')
    # try to do the workflow action "confirm_action', cath the exception ValidationFailed raised by workflow transition 
    self.assertRaises(ValidationFailed, self.workflow_tool.doActionFor, self.monetary_destruction, 'plan_action',  wf_id='monetary_destruction_workflow')
    # execute tic
    self.stepTic()
    # get state of the monetary destruction
    state = self.monetary_destruction.getSimulationState()
    # check the state is draft
    self.assertEqual(state, 'draft')
    # get workflow history
    workflow_history = self.workflow_tool.getInfoFor(ob=self.monetary_destruction, name='history', wf_id='monetary_destruction_workflow')
    # check its len is 2
    self.assertEqual(len(workflow_history), 2)
    # check we get an "Insufficient balance" message in the workflow history because of the invalid line
    msg = workflow_history[-1]['error_message']
    self.assertEqual('Insufficient Balance.', "%s" %(msg,))


  def stepDelInvalidLine(self, sequence=None, sequence_list=None, **kwd):
    """
    Delete the invalid monetary destruction line previously create
    """
    self.monetary_destruction.deleteContent('invalid_line')
    
  def stepDelMonetrayDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Delete the invalid monetary_destruction line previously create
    """
    self.monetary_destruction.deleteContent('monetary_destruction_1')


  def stepCheckTotal(self, sequence=None, sequence_list=None, **kwd):
    """
    Check the total after the creation of the two monetary destruction lines
    """
    # Check number of lines (line1 + line2)
    self.assertEqual(len(self.monetary_destruction.objectValues()), 2)
    # Check quantity, banknotes : 2 for 1992 and 3 for 2003, banknotes : 5 for 1992 and 7 for 2003
    self.assertEqual(self.monetary_destruction.getTotalQuantity(), 5.0 + 24.0)
    # check the total price
    self.assertEqual(self.monetary_destruction.getTotalPrice(), 10000 * 5.0 + 5000 * 24.0)


  def stepPlannedMonetaryDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Confirm the monetary destruction and check it
    """
    # fix amount (10000 * 5.0 + 5000 * 24.0)
    self.monetary_destruction.setSourceTotalAssetPrice('170000.0')
    # do the Workflow action
    self.workflow_tool.doActionFor(self.monetary_destruction, 'plan_action', wf_id='monetary_destruction_workflow')
    # execute tic
    self.stepTic()
    # get state
    state = self.monetary_destruction.getSimulationState()
    # check state is confirmed
    self.assertEqual(state, 'planned')
    # get workflow history
    workflow_history = self.workflow_tool.getInfoFor(ob=self.monetary_destruction, name='history', wf_id='monetary_destruction_workflow')
    # check len of workflow history is 4
    self.assertEqual(len(workflow_history), 4)


  def stepCheckSourceDebitPlanned(self, sequence=None, sequence_list=None, **kwd):
    """
    Check that compution of inventory at vault source is right after confirm and before deliver 
    """
    # check we have 5 banknotes of 10000 currently
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    # check we will have 0 banknote of 10000 after deliver
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 0.0)
    # check we have 24 banknotes of 5000 currently
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)
    # check we will have 0 banknote of 5000 after deliver
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 0.0)


  def stepCheckSourceDebitPlannedForExterne(self, sequence=None, sequence_list=None, **kwd):
    """
    Check that compution of inventory at vault source is right after confirm and before deliver 
    """
    # check we have 5 banknotes of 10000 currently
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 5.0)
    # check we will have 0 banknote of 10000 after deliver
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 0.0)
    # check we have 24 banknotes of 5000 currently
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 24.0)
    # check we will have 0 banknote of 5000 after deliver
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 0.0)



  def stepValidateMonetaryDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Validate the monetary destruction with a good user
    and check that the validation of a monetary destruction have achieved
    """
    # do the workflow transition "deliver_action"
    self.workflow_tool.doActionFor(self.monetary_destruction, 'plan_to_deliver_action', wf_id='monetary_destruction_workflow')
    # execute tic
    self.stepTic()
    # get state of monetary destruction
    state = self.monetary_destruction.getSimulationState()
    # check that state is delivered
    self.assertEqual(state, 'delivered')
    # get workflow history
    workflow_history = self.workflow_tool.getInfoFor(ob=self.monetary_destruction, name='history', wf_id='monetary_destruction_workflow')
    # check len of len workflow history is 6
    self.assertEqual(len(workflow_history), 6)
    

  def stepCheckSourceDebit(self, sequence=None, sequence_list=None, **kwd):
    """
    Check inventory at source (vault source) after validation of the monetary destruction
    """
    # check we have 0 banknote of 10000
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 0.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 0.0)
    # check we have 0 banknote of 5000
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 0.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 0.0)


  def stepCheckSourceDebitForExterne(self, sequence=None, sequence_list=None, **kwd):
    """
    Check inventory at source (vault source) after validation of the monetary destruction
    """
    # check we have 0 banknote of 10000
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 0.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_10000.getRelativeUrl()), 0.0)
    # check we have 0 banknote of 5000
    self.assertEqual(self.simulation_tool.getCurrentInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 0.0)
    self.assertEqual(self.simulation_tool.getFutureInventory(node=self.source_for_externe.getRelativeUrl(), resource = self.billet_5000.getRelativeUrl()), 0.0)




  def stepPlanMonetaryDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Confirm the monetary_destruction and check it
    """
    # fix amount (10000 * 5.0 + 200 * 12.0)
    self.monetary_destruction.setSourceTotalAssetPrice('170000.0')
    # do the Workflow action
    self.workflow_tool.doActionFor(self.monetary_destruction, 'plan_action', wf_id='monetary_destruction_workflow')
    # execute tic
    self.stepTic()
    # get state
    state = self.monetary_destruction.getSimulationState()
    # check state is planned
    self.assertEqual(state, 'planned')
    # get workflow history
    workflow_history = self.workflow_tool.getInfoFor(ob=self.monetary_destruction, name='history', wf_id='monetary_destruction_workflow')
    # check len of workflow history is 4
    self.assertEqual(len(workflow_history), 4)
    

  def stepOrderMonetaryDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Confirm the monetary_destruction and check it
    """
    # fix amount (10000 * 5.0 + 200 * 12.0)
    self.monetary_destruction.setSourceTotalAssetPrice('170000.0')
    # do the Workflow action
    self.workflow_tool.doActionFor(self.monetary_destruction, 'order_action', wf_id='monetary_destruction_workflow')
    # execute tic
    self.stepTic()
    # get state
    state = self.monetary_destruction.getSimulationState()
    # check state is ordered
    self.assertEqual(state, 'ordered')
    # get workflow history
    workflow_history = self.workflow_tool.getInfoFor(ob=self.monetary_destruction, name='history', wf_id='monetary_destruction_workflow')
    # check len of workflow history is 4
    self.assertEqual(len(workflow_history), 6)
    
  def stepConfirmMonetaryDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Confirm the monetary_destruction and check it
    """
    # fix amount (10000 * 5.0 + 200 * 12.0)
    self.monetary_destruction.setSourceTotalAssetPrice('52400.0')
    # do the Workflow action
    self.workflow_tool.doActionFor(self.monetary_destruction, 'confirm_action', wf_id='monetary_destruction_workflow')
    # execute tic
    self.stepTic()
    # get state
    state = self.monetary_destruction.getSimulationState()
    # check state is confirmed
    self.assertEqual(state, 'confirmed')
    # get workflow history
    workflow_history = self.workflow_tool.getInfoFor(ob=self.monetary_destruction, name='history', wf_id='monetary_destruction_workflow')
    # check len of workflow history is 8
    self.assertEqual(len(workflow_history), 8)

  def stepConfirmToDeliverMonetaryDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Deliver the monetary_destruction with a good user
    and check that the deliver of a cash tranfer have achieved
    """
    # do the workflow transition "deliver_action"
    self.workflow_tool.doActionFor(self.monetary_destruction, 'deliver_action', wf_id='monetary_destruction_workflow')
    # execute tic
    self.stepTic()
    # get state of monetary_destruction
    state = self.monetary_destruction.getSimulationState()
    # check that state is delivered
    self.assertEqual(state, 'delivered')
    # get workflow history
    workflow_history = self.workflow_tool.getInfoFor(ob=self.monetary_destruction, name='history', wf_id='monetary_destruction_workflow')
    # check len of len workflow history is 10
    self.assertEqual(len(workflow_history), 10)


  def stepDelMonetaryDestruction(self, sequence=None, sequence_list=None, **kwd):
    """
    Delete the invalid vault_transfer line previously create
    """
    self.monetary_destruction_module.deleteContent('monetary_destruction_1')

  ##################################
  ##  Tests
  ##################################

  def test_01_ERP5BankingMonetaryDestruction(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
    Define the sequence of step that will be play
    """
    if not run: return
    sequence_list = SequenceList()
    # define the sequence
    sequence_string = 'Tic CheckObjects Tic CheckInitialInventory CheckSource ' \
                    + 'CreateMonetaryDestruction ' \
                    + 'CreateValidLine1 CheckSubTotal ' \
                    + 'CreateValidLine2 CheckTotal ' \
                    + 'CheckSource ' \
                    + 'CreateInvalidLine ' \
                    + 'TryPlannedMonetaryDestructionWithBadInventory ' \
                    + 'DelInvalidLine Tic CheckTotal ' \
                    + 'PlannedMonetaryDestruction ' \
                    + 'CheckSourceDebitPlanned ' \
                    + 'ValidateMonetaryDestruction ' \
                    + 'CheckSourceDebit '
    sequence_list.addSequenceString(sequence_string)
    
    # define the sequence
    another_sequence_string = 'Tic DelMonetaryDestruction Tic CheckObjects Tic CheckInitialInventoryForExterne CheckSourceForExterne ' \
                    + 'CreateMonetaryDestructionForExterne ' \
                    + 'CreateValidLineForExterne1 CheckSubTotal ' \
                    + 'CreateValidLineForExterne2 CheckTotal ' \
                    + 'CheckSourceForExterne ' \
                    + 'CreateInvalidLine ' \
                    + 'TryPlannedMonetaryDestructionWithBadInventory ' \
                    + 'DelInvalidLine Tic CheckTotal ' \
                    + 'PlanMonetaryDestruction ' \
                    + 'CheckSourceDebitPlannedForExterne ' \
                    + 'OrderMonetaryDestruction ' \
                    + 'ConfirmMonetaryDestruction ' \
                    + 'ConfirmToDeliverMonetaryDestruction ' \
                    + 'CheckSourceDebitForExterne '		    
		    
    sequence_list.addSequenceString(another_sequence_string)
    
    
    # play the sequence
    sequence_list.play(self)

# define how we launch the unit test
if __name__ == '__main__':
  framework()
else:
  import unittest
  def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestERP5BankingMonetaryDestruction))
    return suite
