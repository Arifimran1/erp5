##############################################################################
#
# Copyright (c) 2005-2006 Nexedi SARL and Contributors. All Rights Reserved.
#                    Yoshinori Okuji <yo@nexedi.com>
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
from zLOG import LOG
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
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


class TestERP5BankingCheckDeposit(TestERP5BankingMixin, ERP5TypeTestCase):
  """
  Unit test class for the check deposit module
  """
  
  login = PortalTestCase.login

  # pseudo constants
  RUN_ALL_TEST = 1 # we want to run all test
  QUIET = 0 # we don't want the test to be quiet

  def getTitle(self):
    """
      Return the title of the test
    """
    return "ERP5BankingCheckDeposit"

  def getCheckDepositModule(self):
    """
    Return the check deposit module
    """
    return getattr(self.getPortal(), 'check_deposit_module', None)

  def afterSetUp(self):
    """
      Method called before the launch of the test to initialize some data
    """
    # Set some variables :
    self.initDefaultVariable()

    self.check_deposit_module = self.getCheckDepositModule()

    self.createManagerAndLogin()
    # create categories
    self.createFunctionGroupSiteCategory(site_list=['paris',])
    # create resources
    self.createBanknotesAndCoins()
    # define the user, a site is needed for accouting event
    self.checkUserFolderType()
    self.organisation = self.organisation_module.newContent(id='baobab_org', portal_type='Organisation',
                                                            function='banking', group='baobab',  site='testsite/paris',role='internal')
    user_dict = {
      'super_user' : [['Manager'], self.organisation, 'banking/comptable', 'baobab', 'testsite/paris/surface/banque_interne/guichet_1']
      }
    # call method to create this user
    self.createERP5Users(user_dict)
    self.logout()
    self.login('super_user')
    # create a person with a bank account
    self.person_1 = self.createPerson(id='person_1',
                                      first_name='toto',
                                      last_name='titi',
                                      site='testsite/paris')
    self.bank_account_1 = self.createBankAccount(person=self.person_1,
                                                 account_id='bank_account_1',
                                                 reference = 'bank_account_1',
                                                 currency=self.currency_1,
                                                 amount=100000,
                                                 bic_code='',
                                                 swift_registered=0,
                                                 internal_bank_account_number="343434343434")
    # create a second person with a bank account
    self.person_2 = self.createPerson(id='person_2',
                                      first_name='foo',
                                      last_name='bar',
                                      site='testsite/paris')
    self.bank_account_2 = self.createBankAccount(person=self.person_2,
                                                 account_id='bank_account_2',
                                                 reference = 'bank_account_2',
                                                 currency=self.currency_1,
                                                 amount=50000,
                                                 bic_code='',
                                                 swift_registered=0,
                                                 internal_bank_account_number="878787878787")
    # create a bank account for the organisation
    self.bank_account_3 = self.createBankAccount(person=self.organisation,
                                                 account_id='bank_account_3',
                                                 reference = 'bank_account_3',
                                                 currency=self.currency_1,
                                                 amount=50000,
                                                 bic_code='BICAGENCPARIS',
                                                 swift_registered=1,
                                                 internal_bank_account_number="121212121212")

    # the checkbook module
    self.checkbook_module = self.getCheckbookModule()
    # create a check
    self.checkbook_1 = self.createCheckbook(id= 'checkbook_1',
                                            vault=None,
                                            bank_account=self.bank_account_2,
                                            min=50,
                                            max=100,
                                            )

    self.check_1 = self.createCheck(id='check_1',
                                    reference='CHKNB1',
                                    checkbook=self.checkbook_1)


  def stepLogout(self, sequence=None, sequence_list=None, **kwd):
    self.logout()

  def stepLoginAsSuperUser(self, sequence=None, sequence_list=None, **kwd):
    self.login('super_user')

  def stepCheckInitialInventory(self, sequence=None, sequence_list=None, **kwd):
    """
    Check the initial inventory before any operations
    """
    self.simulation_tool = self.getSimulationTool()
    # check the inventory of the bank account
    self.assertEqual(self.simulation_tool.getCurrentInventory(payment=self.bank_account_1.getRelativeUrl()), 100000)
    self.assertEqual(self.simulation_tool.getFutureInventory(payment=self.bank_account_1.getRelativeUrl()), 100000)
    # check the inventory of the bank account
    self.assertEqual(self.simulation_tool.getCurrentInventory(payment=self.bank_account_2.getRelativeUrl()), 50000)
    self.assertEqual(self.simulation_tool.getFutureInventory(payment=self.bank_account_2.getRelativeUrl()), 50000)

  def stepCheckObjects(self, sequence=None, sequence_list=None, **kwd):
    """
    Check that all the objects we created in afterSetUp or
    that were added by the business template and that we rely
    on are really here.
    """
    self.checkResourceCreated()
    self.assertEqual(self.check_deposit_module.getPortalType(),
                     'Check Deposit Module')
    self.assertEqual(len(self.check_deposit_module.objectValues()), 0)

  def stepCreateCheckDepositOperation(self, sequence=None, sequence_list=None, **kw):
    """
    Create a first check deposite that used a ban account which has no bic code
    """

    self.check_deposit = self.check_deposit_module.newContent(id = 'check_deposit',
                                                              portal_type = 'Check Deposit',
                                                              destination_payment_value = self.bank_account_1,
                                                              start_date = DateTime().Date(),
                                                              source_total_asset_price = 2000.0,
                                                              resource_value=self.currency_1,
                                                              external_software_value=None,)
    self.assertNotEqual(self.check_deposit, None)
    self.assertEqual(self.check_deposit.getTotalPrice(), 0.0)
    self.assertEqual(self.check_deposit.getDestinationPayment(), self.bank_account_1.getRelativeUrl())
    self.assertEqual(self.check_deposit.getSourceTotalAssetPrice(), 2000.0)
    # the initial state must be draft
    self.assertEqual(self.check_deposit.getSimulationState(), 'draft')
    # set source reference
    self.setDocumentSourceReference(self.check_deposit)
    # check source reference
    self.assertNotEqual(self.check_deposit.getSourceReference(), '')
    self.assertNotEqual(self.check_deposit.getSourceReference(), None)

  def stepAddCheckOperationLine(self, sequence=None, sequence_list=None, **kwd):
    """
    Add a check to the check deposit
    """
    self.check_operation_line_1 = self.check_deposit.newContent(id='check_operation_line_1',
                                                                portal_type="Check Operation Line",
                                                                aggregate_free_text="CHKNB1",
                                                                source_payment_value = self.bank_account_2,
                                                                price=2000,
                                                                quantity=1,
                                                                quantity_unit_value=self.unit)
    self.assertNotEqual(self.check_operation_line_1, None)
    self.assertEqual(len(self.check_deposit.objectIds()), 1)

  def stepPlanCheckDepositOperation(self, sequence=None, sequence_list=None, **kwd):
    """
    Send the check deposit document to first validation level
    """
    self.assertEqual(self.check_deposit.getTotalPrice(portal_type="Check Operation Line"), 2000.0)
    self.workflow_tool.doActionFor(self.check_deposit, 'plan_action', wf_id='check_deposit_workflow')
    self.assertEqual(self.check_deposit.getSimulationState(), 'planned')

  def stepOrderCheckDepositOperation(self, sequence=None, sequence_list=None, **kwd):
    """
    Send the check deposit document to second validation level
    """
    self.workflow_tool.doActionFor(self.check_deposit, 'order_action', wf_id='check_deposit_workflow')
    self.assertEqual(self.check_deposit.getSimulationState(), 'ordered')

  def stepDeliverCheckDepositOperation(self, sequence=None, sequence_list=None, **kwd):
    """
    Deliver the check deposit
    """
    self.workflow_tool.doActionFor(self.check_deposit, 'deliver_action', wf_id='check_deposit_workflow')
    self.assertEqual(self.check_deposit.getSimulationState(), 'delivered')

  def stepRejectCheckDepositOperation(self, sequence=None, sequence_list=None, **kwd):
    """
    Cancel the check deposit
    """
    self.workflow_tool.doActionFor(self.check_deposit, 'cancel_action', wf_id='check_deposit_workflow')
    self.assertEqual(self.check_deposit.getSimulationState(), 'cancelled')

  def stepCheckBankAccountInventoryAfterCheckDepositDelivered(self, sequence=None, sequence_list=None, **kw):
    """
    Check inventory of the bank account changed after validation of operation
    """
    # check the inventory of the bank account
    self.assertEqual(self.simulation_tool.getCurrentInventory(payment=self.bank_account_1.getRelativeUrl()), 102000)
    self.assertEqual(self.simulation_tool.getFutureInventory(payment=self.bank_account_1.getRelativeUrl()), 102000)
    # check the inventory of the bank account
    self.assertEqual(self.simulation_tool.getCurrentInventory(payment=self.bank_account_2.getRelativeUrl()), 48000)
    self.assertEqual(self.simulation_tool.getFutureInventory(payment=self.bank_account_2.getRelativeUrl()), 48000)

  def stepCheckBankAccountInventoryAfterCheckDepositRejected(self, sequence=None, sequence_list=None, **kw):
    """
    Check inventory of the bank account doesn't changed after reject of operation
    """
    # check the inventory of the bank account
    self.assertEqual(self.simulation_tool.getCurrentInventory(payment=self.bank_account_1.getRelativeUrl()), 100000)
    self.assertEqual(self.simulation_tool.getFutureInventory(payment=self.bank_account_1.getRelativeUrl()), 100000)
    # check the inventory of the bank account
    self.assertEqual(self.simulation_tool.getCurrentInventory(payment=self.bank_account_2.getRelativeUrl()), 50000)
    self.assertEqual(self.simulation_tool.getFutureInventory(payment=self.bank_account_2.getRelativeUrl()), 50000)

  def stepClearCheck(self, sequence=None, sequence_list=None, **kw):
    """
    Remove previous check and create a new one with same reference
    """
    self.checkbook_1.manage_delObjects([self.check_1.getId(),])
    self.check_1 = self.createCheck(id='check_1',
                                    reference='CHKNB1',
                                    checkbook=self.checkbook_1)

  def stepClearCheckDepositModule(self, sequence=None, sequence_list=None, **kw):
    """
    Clear the check deposit module
    """
    if hasattr(self, 'check_deposit'):
      self.check_deposit_module.manage_delObjects([self.check_deposit.getId(),])

  def test_01_ERP5BankingCheckDeposit(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
    Define the sequence of step that will be play
    """
    if not run: return
    sequence_list = SequenceList()
    # define the sequence
    sequence_string1 = 'Tic CheckObjects Tic CheckInitialInventory ' \
                       + 'CreateCheckDepositOperation Tic ' \
                       + 'AddCheckOperationLine Tic ' \
                       + 'PlanCheckDepositOperation Tic OrderCheckDepositOperation ' \
                       + 'Tic DeliverCheckDepositOperation Tic ' \
                       + 'CheckBankAccountInventoryAfterCheckDepositDelivered'

    sequence_string2 = 'Tic ClearCheck ClearCheckDepositModule Tic '\
                       + 'CheckObjects Tic CheckInitialInventory ' \
                       + 'CreateCheckDepositOperation Tic ' \
                       + 'AddCheckOperationLine Tic ' \
                       + 'PlanCheckDepositOperation Tic OrderCheckDepositOperation ' \
                       + 'Tic RejectCheckDepositOperation Tic ' \
                       + 'CheckBankAccountInventoryAfterCheckDepositRejected'

    sequence_list.addSequenceString(sequence_string1)
    sequence_list.addSequenceString(sequence_string2)
    # play the sequence
    sequence_list.play(self)

# define how we launch the unit test
if __name__ == '__main__':
  framework()
else:
  import unittest
  def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestERP5BankingCheckDeposit))
    return suite
