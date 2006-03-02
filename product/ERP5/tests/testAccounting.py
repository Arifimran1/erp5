#############################################################################
#
# Copyright (c) 2004 Nexedi SARL and Contributors. All Rights Reserved.
#          Jerome Perrin <jerome@nexedi.com>
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

"""
  Tests some functionnalities of accounting.

"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Needed in order to have a log file inside the current folder
os.environ['EVENT_LOG_FILE'] = os.path.join(os.getcwd(), 'zLOG.log')
os.environ['EVENT_LOG_SEVERITY'] = '-300'

from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from Products.DCWorkflow.DCWorkflow import ValidationFailed
from AccessControl.SecurityManagement import newSecurityManager
from zLOG import LOG
from testPackingList import TestPackingListMixin
from Products.ERP5Type.tests.Sequence import Sequence, SequenceList
from DateTime import DateTime


class TestAccounting(ERP5TypeTestCase):
  """Test Accounting. """
  
  def getAccountingModule(self):
    return getattr(self.getPortal(), 'accounting_module',
           getattr(self.getPortal(), 'accounting', None))
  
  def getAccountModule(self) :
    return getattr(self.getPortal(), 'account_module',
           getattr(self.getPortal(), 'account', None))
  
  # XXX
  def playSequence(self, sequence_string) :
    sequence_list = SequenceList()
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)
 
  RUN_ALL_TESTS = 1

  account_portal_type           = 'Account'
  accounting_period_portal_type = 'Accounting Period'
  accounting_transaction_portal_type = 'Accounting Transaction'
  accounting_transaction_line_portal_type = 'Accounting Transaction Line'
  currency_portal_type          = 'Currency'
  organisation_portal_type      = 'Organisation'
  sale_invoice_portal_type      = 'Sale Invoice Transaction'
  sale_invoice_line_portal_type = 'Sale Invoice Line' 
  sale_invoice_transaction_line_portal_type = 'Sale Invoice Transaction Line'
  sale_invoice_cell_portal_type = 'Invoice Cell'
  purchase_invoice_portal_type      = 'Purchase Invoice Transaction'
  purchase_invoice_line_portal_type = 'Purchase Invoice Line' 
  purchase_invoice_transaction_line_portal_type = \
                'Purchase Invoice Transaction Line'
  purchase_invoice_cell_portal_type = 'Invoice Cell'

  start_date = DateTime(2004, 01, 01)
  stop_date  = DateTime(2004, 12, 31)

  def getTitle(self):
    return "Accounting"
  
  def login(self) :
    """sets the security manager"""
    uf = self.getPortal().acl_users
    uf._doAddUser('alex', '', ['Member', 'Assignee', 'Assignor',
                               'Auditor', 'Author', 'Manager'], [])
    user = uf.getUserById('alex').__of__(uf)
    newSecurityManager(None, user)
  
  def createCategories(self):
    """Create the categories for our test. """
    TestPackingListMixin.createCategories(self)
    # create categories
    for cat_string in self.getNeededCategoryList() :
      base_cat = cat_string.split("/")[0]
      path = self.getPortal().portal_categories[base_cat]
      for cat in cat_string.split("/")[1:] :
        if not cat in path.objectIds() :
          path = path.newContent(
            portal_type = 'Category',
            id = cat,
            immediate_reindex = 1 )
    # check categories have been created
    for cat_string in self.getNeededCategoryList() :
      self.assertNotEquals(None,
                self.getCategoryTool().restrictedTraverse(cat_string),
                cat_string)
                
  def getNeededCategoryList(self):
    """return a list of categories that should be created."""
    return ('group/client', 'group/vendor' )
  
  def getBusinessTemplateList(self):
    """ """
    return ('erp5_base','erp5_pdm', 'erp5_trade', 'erp5_accounting',)

  def stepTic(self, **kw):
    self.tic()

  def stepCreateEntities(self, sequence, **kw) :
    """Create a vendor and a client. """
    client = self.getOrganisationModule().newContent(
        portal_type = self.organisation_portal_type,
        group = "group/client",
        price_currency = "currency_module/USD")
    vendor = self.getOrganisationModule().newContent(
        portal_type = self.organisation_portal_type,
        group = "group/vendor",
        price_currency = "currency_module/EUR")
    sequence.edit( client = client,
                   vendor = vendor,
                   organisation = vendor )
  
  def stepCreateAccountingPeriod(self, sequence, **kw):
    """Creates an Accounting Period for the Organisation."""
    organisation = sequence.get('organisation')
    start_date = self.start_date
    stop_date = self.stop_date
    accounting_period = organisation.newContent(
      portal_type = self.accounting_period_portal_type,
      start_date = start_date, stop_date = stop_date )
    sequence.edit( accounting_period = accounting_period,
                   valid_date_list = [ start_date, start_date+1, stop_date],
                   invalid_date_list = [start_date-1, stop_date+1] )
  
  def stepUseValidDates(self, sequence, **kw):
    """Puts some valid dates in sequence."""
    sequence.edit(date_list = sequence.get('valid_date_list'))
    
  def stepUseInvalidDates(self, sequence, **kw):
    """Puts some invalid dates in sequence."""
    sequence.edit(date_list = sequence.get('invalid_date_list'))
  
  def stepOpenAccountingPeriod(self, sequence, **kw):
    """Opens the Accounting Period."""
    accounting_period = sequence.get('accounting_period')
    self.getPortal().portal_workflow.doActionFor(
                        accounting_period,
                        'plan_action' )
    self.assertEquals(accounting_period.getSimulationState(),
                      'planned')
                      
  def stepConfirmAccountingPeriod(self, sequence, **kw):
    """Confirm the Accounting Period."""
    accounting_period = sequence.get('accounting_period')
    self.getPortal().portal_workflow.doActionFor(
                        accounting_period,
                        'confirm_action' )
    self.assertEquals(accounting_period.getSimulationState(),
                      'confirmed')

  def stepDeliverAccountingPeriod(self, sequence, **kw):
    """Deliver the Accounting Period."""
    accounting_period = sequence.get('accounting_period')
    self.getPortal().portal_workflow.doActionFor(
                        accounting_period,
                        'close_action' )
    self.assertEquals(accounting_period.getSimulationState(),
                      'closing')
    
  def stepCheckAccountingPeriodDelivered(self, sequence, **kw):
    """Check the Accounting Period is delivered."""
    accounting_period = sequence.get('accounting_period')
    self.assertEquals(accounting_period.getSimulationState(),
                      'delivered')
    
  
  def stepCreateCurrencies(self, sequence, **kw) :
    """Create a some currencies. """
    if hasattr(self.getCurrencyModule(), 'EUR'):
      sequence.edit(
        EUR = self.getCurrencyModule()['EUR'],
        USD = self.getCurrencyModule()['USD'],
        YEN = self.getCurrencyModule()['YEN'],
      )
      return
    EUR = self.getCurrencyModule().newContent(
          portal_type = self.currency_portal_type,
          reference = "EUR",
          id = "EUR" )
    USD = self.getCurrencyModule().newContent(
          portal_type = self.currency_portal_type,
          reference = "USD",
          id = "USD" )
    YEN = self.getCurrencyModule().newContent(
          portal_type = self.currency_portal_type,
          reference = "YEN",
          id = "YEN" )
    sequence.edit( EUR = EUR, USD = USD, YEN = YEN )
  
  def stepCreateAccounts(self, sequence, **kw) :
    """Create necessary accounts. """
    receivable = self.getAccountModule().newContent(
          title = 'receivable',
          portal_type = self.account_portal_type,
          account_type = 'asset/receivable' )
    payable = self.getAccountModule().newContent(
          title = 'payable',
          portal_type = self.account_portal_type,
          account_type = 'liability/payable' )
    expense = self.getAccountModule().newContent(
          title = 'expense',
          portal_type = self.account_portal_type,
          account_type = 'expense' )
    income = self.getAccountModule().newContent(
          title = 'income',
          portal_type = self.account_portal_type,
          account_type = 'income' )
    collected_vat = self.getAccountModule().newContent(
          title = 'collected_vat',
          portal_type = self.account_portal_type,
          account_type = 'liability/payable/collected_vat' )
    refundable_vat = self.getAccountModule().newContent(
          title = 'refundable_vat',
          portal_type = self.account_portal_type,
          account_type = 'asset/receivable/refundable_vat' )
    bank = self.getAccountModule().newContent(
          title = 'bank',
          portal_type = self.account_portal_type,
          account_type = 'asset/cash/bank')
    
    # set mirror accounts.
    receivable.setDestinationValue(payable)
    payable.setDestinationValue(receivable)
    expense.setDestinationValue(income)
    income.setDestinationValue(expense)
    collected_vat.setDestinationValue(refundable_vat)
    refundable_vat.setDestinationValue(collected_vat)
    bank.setDestinationValue(bank)
    
    account_list = [ receivable,
                     payable,
                     expense,
                     income,
                     collected_vat,
                     refundable_vat,
                     bank ]

    for account in account_list :
      account.validate()
      self.assertEquals(account.getValidationState(), 'validated')
      
    sequence.edit( receivable_account = receivable,
                   payable_account = payable,
                   expense_account = expense,
                   income_account = income,
                   collected_vat_account = collected_vat,
                   refundable_vat_account = refundable_vat,
                   bank_account = bank,
                   account_list = account_list )

  
  def stepCreateAccountingTransactionAndCheckMirrorAccount(self,
                                          sequence, **kw):
    """Check that mirror account are set automatically. """
    account_list = sequence.get('account_list')
    
    for account in account_list :
      self.assertNotEquals(account.getDestinationValue(), None)
    
    transaction = self.getAccountingModule().newContent(
      portal_type = self.accounting_transaction_portal_type,
      source_section_value = sequence.get('client'),
      resource_value = sequence.get('EUR'),
      created_by_builder = 1,
    )
    
    # setting both source and destination shouldn't use mirror accounts
    destination = sequence.get('receivable_account')
    for account in account_list :
      transaction_line = transaction.newContent(
        portal_type = self.accounting_transaction_line_portal_type,
        source = account.getRelativeUrl(),
        destination = destination.getRelativeUrl(),
      )
      self.assertEquals( destination.getRelativeUrl(),
                         transaction_line.getDestination() )
    
    # setting only a source must use mirror account as destination
    for account in account_list :
      transaction_line = transaction.newContent(
        portal_type = self.accounting_transaction_line_portal_type,
        source = account.getRelativeUrl(),
      )
      self.assertEquals( account.getDestination(),
                         transaction_line.getDestination() )
    
    # editing the destination later should not change the source once
    # the mirror account has been set.
    account = sequence.get('receivable_account')
    destination = sequence.get('bank_account')
    another_destination = sequence.get('expense_account')
    account.setDestinationValueList(account_list)
    
    transaction_line = transaction.newContent(
      portal_type = self.accounting_transaction_line_portal_type,
      source = account.getRelativeUrl(), )
    automatically_set_destination = transaction_line.getDestinationValue()
    # get another account.
    if automatically_set_destination == destination :
      forced_destination = destination
    else :
      forced_destination = another_destination
    # set all other accounts as mirror account to this one.
    forced_destination.setDestinationValueList(account_list)
    
    # change the destination and check the source didn't change.
    transaction_line.edit(destination = forced_destination.getRelativeUrl())
    self.assertEquals( transaction_line.getSourceValue(), account )
    
  def getInvoicePropertyList(self):
    """Returns the list of properties for invoices, stored as 
      a list of dictionnaries. """
    # source currency is EUR
    # destination currency is USD
    return [
      # in currency of destination, converted for source
      { 'income' : -200,             'source_converted_income' : -180,
        'collected_vat' : -40,       'source_converted_collected_vat' : -36,
        'receivable' : 240,          'source_converted_receivable' : 216,
        'currency' : 'currency_module/USD' },
      
      # in currency of source, converted for destination
      { 'income' : -100,        'destination_converted_expense' : -200,
        'collected_vat' : 10,   'destination_converted_refundable_vat' : 100,
        'receivable' : 90,      'destination_converted_payable' : 100,
        'currency' : 'currency_module/EUR' },
      
      { 'income' : -100,        'destination_converted_expense' : -200,
        'collected_vat' : 10,   'destination_converted_refundable_vat' : 100,
        'receivable' : 90,      'destination_converted_payable' : 100,
        'currency' : 'currency_module/EUR' },
      
      # in an external currency, converted for both source and dest.
      { 'income' : -300,
                    'source_converted_income' : -200,
                    'destination_converted_expense' : -400,
        'collected_vat' : 40,
                    'source_converted_collected_vat' : 36,
                    'destination_converted_refundable_vat' : 50,
        'receivable' : 260,
                    'source_converted_receivable' : 164,
                    'destination_converted_payable': 350,
        'currency' : 'currency_module/YEN' },
      
      # currency of source, not converted for destination -> 0
      # FIXME: validation should be refused by accounting workflow ?
      { 'income' : -100,
        'collected_vat' : -20,
        'receivable' : 120,
        'currency' : 'currency_module/EUR' },
      
    ]
  
  def stepCreateInvoices(self, sequence, **kw) :
    """Create invoices with properties from getInvoicePropertyList. """
    invoice_prop_list = self.getInvoicePropertyList()
    invoice_list = []
    date_list = sequence.get('date_list')
    if not date_list : date_list = [ DateTime(2004, 12, 31) ]
    i = 0
    for invoice_prop in invoice_prop_list :
      i += 1
      date = date_list[i % len(date_list)]
      invoice = self.getAccountingModule().newContent(
          portal_type = self.sale_invoice_portal_type,
          source_section_value = sequence.get('vendor'),
          source_value = sequence.get('vendor'),
          destination_section_value = sequence.get('client'),
          destination_value = sequence.get('client'),
          resource = invoice_prop['currency'],
          start_date = date, stop_date = date,
          created_by_builder = 0,
      )
      
      for line_type in ['income', 'receivable', 'collected_vat'] :
        source_account = sequence.get('%s_account' % line_type)
        line = invoice.newContent(
          portal_type = self.sale_invoice_transaction_line_portal_type,
          quantity = invoice_prop[line_type],
          source_value = source_account
        )
        source_converted = invoice_prop.get(
                          'source_converted_%s' % line_type, None)
        if source_converted is not None :
          line.setSourceTotalAssetPrice(source_converted)
        
        destination_account = source_account.getDestinationValue(
                                                portal_type = 'Account' )
        destination_converted = invoice_prop.get(
                          'destination_converted_%s' %
                          destination_account.getAccountTypeId(), None)
        if destination_converted is not None :
          line.setDestinationTotalAssetPrice(destination_converted)
 
      invoice_list.append(invoice)
    sequence.edit( invoice_list = invoice_list )
  
  def stepCreateOtherSectionInvoices(self, sequence, **kw):
    """Create invoice for other sections."""
    other_source = self.getOrganisationModule().newContent(
                      portal_type = 'Organisation' )
    other_destination = self.getOrganisationModule().newContent(
                      portal_type = 'Organisation' )
    invoice = self.getAccountingModule().newContent(
        portal_type = self.sale_invoice_portal_type,
        source_section_value = other_source,
        source_value = other_source,
        destination_section_value = other_destination,
        destination_value = other_destination,
        resource_value = sequence.get('EUR'),
        start_date = self.start_date,
        stop_date = self.start_date,
        created_by_builder = 0,
    )
    
    line = invoice.newContent(
        portal_type = self.sale_invoice_transaction_line_portal_type,
        quantity = 100, source_value = sequence.get('account_list')[0])
    line = invoice.newContent(
        portal_type = self.sale_invoice_transaction_line_portal_type,
        quantity = -100, source_value = sequence.get('account_list')[1])
    sequence.edit(invoice_list = [invoice])
  
  def stepStopInvoices(self, sequence, **kw) :
    """Validates invoices."""
    invoice_list = sequence.get('invoice_list')
    for invoice in invoice_list:
      self.getPortal().portal_workflow.doActionFor(
          invoice, 'stop_action')
  
  def stepCheckStopInvoicesRefused(self, sequence, **kw) :
    """Checks that invoices cannot be validated."""
    invoice_list = sequence.get('invoice_list')
    for invoice in invoice_list:
      self.assertRaises(ValidationFailed,
          self.getPortal().portal_workflow.doActionFor,
          invoice, 'stop_action')

  def stepCheckInvoicesAreDraft(self, sequence, **kw) :
    """Checks invoices are in draft state."""
    invoice_list = sequence.get('invoice_list')
    for invoice in invoice_list:
      self.assertEquals(invoice.getSimulationState(), 'draft')

  def stepCheckInvoicesAreStopped(self, sequence, **kw) :
    """Checks invoices are in stopped state."""
    invoice_list = sequence.get('invoice_list')
    for invoice in invoice_list:
      self.assertEquals(invoice.getSimulationState(), 'stopped')
      
  def stepCheckInvoicesAreDelivered(self, sequence, **kw) :
    """Checks invoices are in delivered state."""
    invoice_list = sequence.get('invoice_list')
    for invoice in invoice_list:
      self.assertEquals(invoice.getSimulationState(), 'delivered')
      
  def checkAccountBalanceInCurrency(self, section, currency,
                                          sequence, **kw) :
    """ Checks accounts balances in a given currency."""
    invoice_list = sequence.get('invoice_list')
    for account_type in [ 'income', 'receivable', 'collected_vat',
                          'expense', 'payable', 'refundable_vat' ] :
      account = sequence.get('%s_account' % account_type)
      calculated_balance = 0
      for invoice in invoice_list :
        for line in invoice.getMovementList():
          # source
          if line.getSourceValue() == account and\
             line.getResourceValue() == currency and\
             section == line.getSourceSectionValue() :
              calculated_balance += (
                    line.getSourceDebit() - line.getSourceCredit())
          # dest.
          elif line.getDestinationValue() == account and\
             line.getResourceValue() == currency and\
             section == line.getDestinationSectionValue() :
              calculated_balance += (
                    line.getDestinationDebit() - line.getDestinationCredit())
      
      self.assertEquals(calculated_balance,
          self.getPortal().portal_simulation.getInventory(
            node_uid = account.getUid(),
            section_uid = section.getUid(),
            # resource_uid = currency.getUid()   # FIXME: raises a KeyError in SQLCatalog.buildSQLQuery
            resource = currency.getRelativeUrl()
          ))
  
  def stepCheckAccountBalanceLocalCurrency(self, sequence, **kw) :
    """ Checks accounts balances in the organisation default currency."""
    for section in (sequence.get('vendor'), sequence.get('client')) :
      currency = section.getPriceCurrencyValue()
      self.checkAccountBalanceInCurrency(section, currency, sequence)
  
  def stepCheckAccountBalanceExternalCurrency(self, sequence, **kw) :
    """ Checks accounts balances in external currencies ."""
    for section in (sequence.get('vendor'), sequence.get('client')) :
      for currency in (sequence.get('USD'), sequence.get('YEN')) :
        self.checkAccountBalanceInCurrency(section, currency, sequence)
    
  def checkAccountBalanceInConvertedCurrency(self, section, sequence, **kw) :
    """ Checks accounts balances converted in section default currency."""
    invoice_list = sequence.get('invoice_list')
    for account_type in [ 'income', 'receivable', 'collected_vat',
                          'expense', 'payable', 'refundable_vat' ] :
      account = sequence.get('%s_account' % account_type)
      calculated_balance = 0
      for invoice in invoice_list :
        for line in invoice.getMovementList() :
          if line.getSourceValue() == account and \
             section == line.getSourceSectionValue() :
            calculated_balance += line.getSourceInventoriatedTotalAssetPrice()
          elif line.getDestinationValue() == account and\
               section == line.getDestinationSectionValue() :
            calculated_balance += \
                             line.getDestinationInventoriatedTotalAssetPrice()
      self.assertEquals(calculated_balance,
          self.getPortal().portal_simulation.getInventoryAssetPrice(
            node_uid = account.getUid(),
            section_uid = section.getUid(),
          ))
  
  def stepCheckAccountBalanceConvertedCurrency(self, sequence, **kw):
    """Checks accounts balances converted in the organisation default
    currency."""
    for section in (sequence.get('vendor'), sequence.get('client')) :
      self.checkAccountBalanceInConvertedCurrency(section, sequence)
  
  def stepCheckAccountingTransactionDelivered(self, sequence, **kw):
    """Checks all accounting transaction related to `organisation`
      are in delivered state. """
    organisation = sequence.get('organisation').getRelativeUrl()
    accounting_module = self.getPortal().accounting_module
    for transaction in accounting_module.objectValues() :
      if transaction.getSourceSection() == organisation \
          or transaction.getDestinationSection() == organisation :
        if self.start_date <= transaction.getStartDate() <= self.stop_date :
          self.assertEquals(transaction.getSimulationState(), 'delivered')
  
  


  ##############################################################################
  ## Test Methods ##############################################################
  ##############################################################################
  
  def test_MultiCurrencyInvoice(self, quiet=0, run=RUN_ALL_TESTS):
    """Basic test for multi currency accounting"""
    self.playSequence("""
      stepCreateCurrencies
      stepCreateEntities
      stepCreateAccounts
      stepCreateInvoices
      stepTic
      stepCheckAccountBalanceLocalCurrency
      stepCheckAccountBalanceExternalCurrency
      stepCheckAccountBalanceConvertedCurrency
    """)

  def test_AccountingPeriod(self, quiet=0, run=RUN_ALL_TESTS):
    """Basic test for Accounting Periods"""
    self.playSequence("""
      stepCreateCurrencies
      stepCreateEntities
      stepCreateAccounts
      stepCreateAccountingPeriod
      stepOpenAccountingPeriod
      stepTic
      stepUseValidDates
      stepCreateInvoices
      stepStopInvoices
      stepCheckInvoicesAreStopped
      stepTic
      stepConfirmAccountingPeriod
      stepTic
      stepDeliverAccountingPeriod
      stepTic
      stepCheckAccountingPeriodDelivered
      stepCheckInvoicesAreDelivered
      stepTic
      stepCheckAccountingTransactionDelivered
    """)
  
  def test_AccountingPeriodRefusesWrongDateTransactionValidation(
        self, quiet=0, run=RUN_ALL_TESTS):
    """Accounting Periods prevents transactions to be validated
        when there is no oppened accounting period"""
    self.playSequence("""
      stepCreateCurrencies
      stepCreateEntities
      stepCreateAccounts
      stepCreateAccountingPeriod
      stepOpenAccountingPeriod
      stepTic
      stepUseInvalidDates
      stepCreateInvoices
      stepCheckStopInvoicesRefused
      stepTic
      stepCheckInvoicesAreDraft
    """)

  def test_AccountingPeriodNotStoppedTransactions(self, quiet=0,
                                                  run=RUN_ALL_TESTS):
    """Accounting Periods refuse to close when some transactions are
      not stopped"""
    self.playSequence("""
      stepCreateCurrencies
      stepCreateEntities
      stepCreateAccounts
      stepCreateAccountingPeriod
      stepOpenAccountingPeriod
      stepTic
      stepCreateInvoices
      stepTic
      stepCheckAccountingPeriodRefusesClosing
      stepTic
      stepCheckInvoicesAreDraft
    """)

  def test_AccountingPeriodNotStoppedTransactions(self, quiet=0,
                                                  run=RUN_ALL_TESTS):
    """Accounting Periods does not change other section transactions."""
    self.playSequence("""
      stepCreateCurrencies
      stepCreateEntities
      stepCreateAccounts
      stepCreateAccountingPeriod
      stepOpenAccountingPeriod
      stepTic
      stepCreateOtherSectionInvoices
      stepTic
      stepConfirmAccountingPeriod
      stepTic
      stepDeliverAccountingPeriod
      stepTic
      stepCheckAccountingPeriodDelivered
      stepCheckInvoicesAreDraft
    """)

  def test_MirrorAccounts(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests using an account on one sides uses the mirror account
    on the other size. """
    self.playSequence("""
      stepCreateEntities
      stepCreateAccounts
      stepCreateAccountingTransactionAndCheckMirrorAccount
    """)

# TODO:
#  test transaction validation from accounting workflow.

 
if __name__ == '__main__':
  framework()
else:
  import unittest
  def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAccounting))
    return suite

