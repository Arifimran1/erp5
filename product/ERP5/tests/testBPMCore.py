# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
#          Łukasz Nowak <luke@nexedi.com>
#          Yusuke Muraoka <yusuke@nexedi.com>
#          Fabien Morin <fabien@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
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

import unittest
import transaction

from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.ERP5Type.tests.utils import reindex

class TestBPMMixin(ERP5TypeTestCase):
  """Skeletons for tests which depend on BPM"""

  def getBusinessTemplateList(self):
    return ('erp5_base', 'erp5_pdm', 'erp5_trade', 'erp5_accounting',
      'erp5_invoicing', 'erp5_simplified_invoicing', 'erp5_simulation',
      'erp5_simulation_test')

  business_process_portal_type = 'Business Process'
  business_link_portal_type = 'Business Link'
  trade_model_path_portal_type = 'Trade Model Path'

  normal_resource_use_category_list = ['normal']
  invoicing_resource_use_category_list = ['discount', 'tax']

  def createCategoriesInCategory(self, category, category_id_list):
    for category_id in category_id_list:
      if not category.hasObject(category_id):
        category.newContent(portal_type='Category', id = category_id,
            title = category_id)

  @reindex
  def createCategories(self):
    category_tool = getToolByName(self.portal, 'portal_categories')
    self.createCategoriesInCategory(category_tool.base_amount, ['discount',
      'tax', 'total_tax', 'total_discount', 'total'])
    self.createCategoriesInCategory(category_tool.use,
        self.normal_resource_use_category_list + \
            self.invoicing_resource_use_category_list)
    self.createCategoriesInCategory(category_tool.trade_phase, ['default',])
    self.createCategoriesInCategory(category_tool.trade_phase.default,
        ['accounting', 'delivery', 'invoicing', 'discount', 'tax', 'payment'])
    self.createCategoriesInCategory(category_tool.trade_state,
        ['ordered', 'invoiced', 'delivered', 'taxed',
         'state_a', 'state_b', 'state_c', 'state_d', 'state_e'])

  @reindex
  def createBusinessProcess(self, **kw):
    module = self.portal.getDefaultModule(
        portal_type=self.business_process_portal_type,)
    business_process =  module.newContent(
      portal_type=self.business_process_portal_type,
      specialise_value=module.erp5_default_business_process)
    business_process._edit(**kw)
    self.createTradeModelPath(business_process,
      reference='default_path',
      trade_phase_value_list=('default/payment',
                              'default/discount',
                              'default/tax'),
      trade_date='trade_phase/default/order')
    kw = dict(business_process=business_process,
              trade_phase='default/accounting',
              trade_date='trade_phase/default/order',
              membership_criterion_base_category='resource_use')
    self.createTradeModelPath(reference='acounting_tax1',
      efficiency=-1,
      source_value=self.receivable_account,
      destination_value=self.payable_account,
      membership_criterion_category='resource_use/use/tax',
      **kw)
    self.createTradeModelPath(reference='acounting_tax2',
      efficiency=1,
      source_value=self.collected_tax_account,
      destination_value=self.refundable_tax_account,
      membership_criterion_category='resource_use/use/tax',
      **kw)
    self.createTradeModelPath(reference='acounting_discount1',
      efficiency=-1,
      source_value=self.receivable_account,
      destination_value=self.payable_account,
      membership_criterion_category='resource_use/use/discount',
      **kw)
    self.createTradeModelPath(reference='acounting_discount2',
      efficiency=1,
      source_value=self.income_account,
      destination_value=self.expense_account,
      membership_criterion_category='resource_use/use/discount',
      **kw)
    self.createTradeModelPath(reference='acounting_normal1',
      efficiency=-1,
      source_value=self.receivable_account,
      destination_value=self.payable_account,
      membership_criterion_category='resource_use/use/normal',
      **kw)
    self.createTradeModelPath(reference='acounting_normal2',
      efficiency=1,
      source_value=self.income_account,
      destination_value=self.expense_account,
      membership_criterion_category='resource_use/use/normal',
      **kw)
    return business_process

  @reindex
  def createBusinessLink(self, business_process=None, **kw):
    if business_process is None:
      business_process = self.createBusinessProcess()
    kw['destination_method_id'] = kw.pop('destination_method_id',
        'BusinessLink_getDefaultDestinationList')
    kw['source_method_id'] = kw.pop('source_method_id',
        'BusinessLink_getDefaultSourceList')
    business_link = business_process.newContent(
      portal_type=self.business_link_portal_type, **kw)
    return business_link

  def createTradeModelPath(self, business_process=None, **kw):
    if business_process is None:
      business_process = self.createBusinessProcess()
    return business_process.newContent(
      portal_type=self.trade_model_path_portal_type, **kw)

  def createMovement(self):
    # returns a movement for testing
    applied_rule = self.portal.portal_simulation.newContent(
        portal_type='Applied Rule')
    return applied_rule.newContent(portal_type='Simulation Movement')

  def createAndValidateAccount(self, account_id, account_type):
    account_module = self.portal.account_module
    account = account_module.newContent(portal_type='Account',
          title=account_id,
          account_type=account_type)
    self.assertNotEqual(None, account.getAccountTypeValue())
    account.validate()
    return account

  def createAndValidateAccounts(self):
    self.receivable_account = self.createAndValidateAccount('receivable',
        'asset/receivable')
    self.payable_account = self.createAndValidateAccount('payable',
        'liability/payable')
    self.income_account = self.createAndValidateAccount('income', 'income')
    self.expense_account = self.createAndValidateAccount('expense', 'expense')
    self.collected_tax_account = self.createAndValidateAccount(
        'collected_tax', 'liability/payable/collected_vat')
    self.refundable_tax_account = self.createAndValidateAccount(
        'refundable_tax',
        'asset/receivable/refundable_vat')

  def afterSetUp(self):
    self.validateRules()
    self.createCategories()
    self.createAndValidateAccounts()
    self.stepTic()

  def beforeTearDown(self):
    # abort any transaction
    transaction.abort()
    # put non finished activities into ignored state
    activity_connection = self.portal.cmf_activity_sql_connection
    for table in 'message', 'message_queue':
      activity_connection.manage_test(
          'delete from %s where processing_node=-2' % table)
    self.stepTic()

class TestBPMImplementation(TestBPMMixin):
  """Business Process implementation tests"""
  def test_BusinessProcess_getPathValueList(self):
    business_process = self.createBusinessProcess()

    accounting_business_link = business_process.newContent(
        portal_type=self.business_link_portal_type,
        trade_phase='default/accounting')

    delivery_business_link = business_process.newContent(
        portal_type=self.business_link_portal_type,
        trade_phase='default/delivery')

    accounting_delivery_business_link = business_process.newContent(
        portal_type=self.business_link_portal_type,
        trade_phase=('default/accounting', 'default/delivery'))

    self.stepTic()

    self.assertSameSet(
      (accounting_business_link, accounting_delivery_business_link),
      business_process.getPathValueList(trade_phase='default/accounting')
    )

    self.assertSameSet(
      (delivery_business_link, accounting_delivery_business_link),
      business_process.getPathValueList(trade_phase='default/delivery')
    )

    self.assertSameSet(
      (accounting_delivery_business_link, delivery_business_link,
        accounting_business_link),
      business_process.getPathValueList(trade_phase=('default/delivery',
        'default/accounting'))
    )

  def test_BusinessLinkStandardCategoryAccessProvider(self):
    source_node = self.portal.organisation_module.newContent(
                    portal_type='Organisation')
    source_section_node = self.portal.organisation_module.newContent(
                    portal_type='Organisation')
    business_link = self.createBusinessLink()
    business_link.setSourceValue(source_node)
    business_link.setSourceSectionValue(source_section_node)
    self.assertEquals([source_node], business_link.getSourceValueList())
    self.assertEquals([source_node.getRelativeUrl()], business_link.getSourceList())
    self.assertEquals(source_node.getRelativeUrl(),
        business_link.getSource(default='something'))

  def test_EmptyBusinessLinkStandardCategoryAccessProvider(self):
    business_link = self.createBusinessLink()
    self.assertEquals(None, business_link.getSourceValue())
    self.assertEquals(None, business_link.getSource())
    self.assertEquals('something',
        business_link.getSource(default='something'))

  def test_BuinessPathDynamicCategoryAccessProvider(self):
    source_node = self.portal.organisation_module.newContent(
                    portal_type='Organisation')
    source_section_node = self.portal.organisation_module.newContent(
                    portal_type='Organisation')
    business_link = self.createBusinessLink()
    business_link.setSourceMethodId('BusinessLink_getDefaultSourceList')

    context_movement = self.createMovement()
    context_movement.setSourceValue(source_node)
    context_movement.setSourceSectionValue(source_section_node)
    self.assertEquals(None, business_link.getSourceValue())
    self.assertEquals([source_node],
                      business_link.getSourceValueList(context=context_movement))
    self.assertEquals([source_node.getRelativeUrl()],
                      business_link.getSourceList(context=context_movement))
    self.assertEquals(source_node.getRelativeUrl(),
      business_link.getSource(context=context_movement, default='something'))

  def test_BuinessPathDynamicCategoryAccessProviderBusinessLinkPrecedence(self):
    movement_node = self.portal.organisation_module.newContent(
                    portal_type='Organisation')
    path_node = self.portal.organisation_module.newContent(
                    portal_type='Organisation')
    business_link = self.createBusinessLink()
    business_link.setSourceMethodId('BusinessLink_getDefaultSourceList')
    business_link.setSourceValue(path_node)

    context_movement = self.createMovement()
    context_movement.setSourceValue(movement_node)
    self.assertEquals(path_node, business_link.getSourceValue())
    self.assertEquals(path_node,
                      business_link.getSourceValue(context=context_movement))
    self.assertEquals([path_node],
                      business_link.getSourceValueList(context=context_movement))

  def test_BuinessPathDynamicCategoryAccessProviderEmptyMovement(self):
    business_link = self.createBusinessLink()
    business_link.setSourceMethodId('BusinessLink_getDefaultSourceList')

    context_movement = self.createMovement()
    self.assertEquals(None, business_link.getSourceValue())
    self.assertEquals(None,
                      business_link.getSourceValue(context=context_movement))
    self.assertEquals(None,
                      business_link.getSource(context=context_movement))
    self.assertEquals('something',
      business_link.getSource(context=context_movement, default='something'))

  def test_BusinessState_getRemainingTradePhaseList(self):
    """
    This test case is described for what trade_phase is remaining after the state.
    In this case, root explanation is path of between "b" and "d", and
    path of between "a" and "b" has a condition which simulation state of
    explanation must be "ordered" to pass the path. (*1)
    But this test case will be passed the condition.

                            (root explanation)
       default/discount     default/invoicing     default/accounting
    a ------------------ b ------------------- d -------------------- e
       (cond="ordered")   \                   /
                           \                 /
          default/delivery  \               / default/payment
                             \             /
                              \           /
                               \         /
                                \       /
                                 \     /
                                  \   /
                                   \ /
                                    c
    """
    # define business process
    category_tool = self.getCategoryTool()
    business_process = self.createBusinessProcess()
    business_link_a_b = self.createBusinessLink(business_process)
    business_link_b_c = self.createBusinessLink(business_process)
    business_link_b_d = self.createBusinessLink(business_process)
    business_link_c_d = self.createBusinessLink(business_process)
    business_link_d_e = self.createBusinessLink(business_process)
    business_state_a = category_tool.trade_state.state_a
    business_state_b = category_tool.trade_state.state_b
    business_state_c = category_tool.trade_state.state_c
    business_state_d = category_tool.trade_state.state_d
    business_state_e = category_tool.trade_state.state_e
    business_link_a_b.setPredecessorValue(business_state_a)
    business_link_b_c.setPredecessorValue(business_state_b)
    business_link_b_d.setPredecessorValue(business_state_b)
    business_link_c_d.setPredecessorValue(business_state_c)
    business_link_d_e.setPredecessorValue(business_state_d)
    business_link_a_b.setSuccessorValue(business_state_b)
    business_link_b_c.setSuccessorValue(business_state_c)
    business_link_b_d.setSuccessorValue(business_state_d)
    business_link_c_d.setSuccessorValue(business_state_d)
    business_link_d_e.setSuccessorValue(business_state_e)

    # set title for debug
    business_link_a_b.edit(title="a_b")
    business_link_b_c.edit(title="b_c")
    business_link_b_d.edit(title="b_d")
    business_link_c_d.edit(title="c_d")
    business_link_d_e.edit(title="d_e")
    
    # set trade_phase
    business_link_a_b.edit(trade_phase=['default/discount'],
                           completed_state=['ordered']) # (*1)
    business_link_b_c.edit(trade_phase=['default/delivery'])
    business_link_b_d.edit(trade_phase=['default/invoicing'])
    business_link_c_d.edit(trade_phase=['default/payment'])
    business_link_d_e.edit(trade_phase=['default/accounting'])

    # mock order
    order = self.portal.sale_order_module.newContent(portal_type="Sale Order")
    order_line = order.newContent(portal_type="Sale Order Line")

    # make simulation
    order.order()

    self.stepTic()

    applied_rule = order.getCausalityRelatedValue()
    sm = applied_rule.contentValues(portal_type="Simulation Movement")[0]
    sm.edit(causality_value=business_link_a_b)

    # make other movements for each business path
    applied_rule.newContent(portal_type="Simulation Movement",
                            causality_value=business_link_b_c,
                            order_value=order_line)
    applied_rule.newContent(portal_type="Simulation Movement",
                            causality_value=business_link_b_d,
                            order_value=order_line)
    applied_rule.newContent(portal_type="Simulation Movement",
                            causality_value=business_link_c_d,
                            order_value=order_line)
    applied_rule.newContent(portal_type="Simulation Movement",
                            causality_value=business_link_d_e,
                            order_value=order_line)

    self.stepTic()

    trade_phase = self.portal.portal_categories.trade_phase.default

    # assertion which getRemainingTradePhaseList must return category which will be passed
    # discount is passed, business_link_a_b is already completed, because simulation state is "ordered"
    self.assertEquals(set([trade_phase.delivery,
                           trade_phase.invoicing,
                           trade_phase.payment,
                           trade_phase.accounting]),
                      set(business_process.getRemainingTradePhaseList(order,
                          business_state_a)))
    self.assertEquals(set([trade_phase.delivery,
                           trade_phase.invoicing,
                           trade_phase.payment,
                           trade_phase.accounting]),
                      set(business_process.getRemainingTradePhaseList(order,
                          business_state_b)))
    self.assertEquals(set([trade_phase.payment,
                           trade_phase.accounting]),
                      set(business_process.getRemainingTradePhaseList(order,
                          business_state_c)))
    self.assertEquals(set([trade_phase.accounting]),
                      set(business_process.getRemainingTradePhaseList(order,
                          business_state_d)))

    # when trade_phase_list is defined in arguments, the result is filtered by base category.
    self.assertEquals(set([trade_phase.delivery,
                           trade_phase.accounting]),
                      set(business_process\
                          .getRemainingTradePhaseList(order, business_state_a,
                                                      trade_phase_list=['default/delivery',
                                                                        'default/accounting'])))

  def test_BusinessLink_calculateExpectedDate(self):
    """
    This test case is described for what start/stop date is expected on
    each path by explanation.
    In this case, root explanation is path of between "b" and "d", and
    lead time and wait time is set on each path.
    ("l" is lead time, "w" is wait_time)

    Each path must calculate most early day from getting most longest
    path in the simulation.

    "referential_date" represents for which date have to get of explanation from reality.

                  (root_explanation)
        l:2, w:1         l:3, w:1       l:4, w:2
    a ------------ b -------------- d -------------- e
                    \             /
                     \           /
             l:2, w:1 \         / l:3, w:0
                       \       /
                        \     /
                         \   /
                          \ /
                           c
    """
    # define business process
    category_tool = self.getCategoryTool()
    business_process = self.createBusinessProcess()
    business_link_a_b = self.createBusinessLink(business_process)
    business_link_b_c = self.createBusinessLink(business_process)
    business_link_b_d = self.createBusinessLink(business_process)
    business_link_c_d = self.createBusinessLink(business_process)
    business_link_d_e = self.createBusinessLink(business_process)
    business_state_a = category_tool.trade_state.state_a
    business_state_b = category_tool.trade_state.state_b
    business_state_c = category_tool.trade_state.state_c
    business_state_d = category_tool.trade_state.state_d
    business_state_e = category_tool.trade_state.state_e
    business_link_a_b.setPredecessorValue(business_state_a)
    business_link_b_c.setPredecessorValue(business_state_b)
    business_link_b_d.setPredecessorValue(business_state_b)
    business_link_c_d.setPredecessorValue(business_state_c)
    business_link_d_e.setPredecessorValue(business_state_d)
    business_link_a_b.setSuccessorValue(business_state_b)
    business_link_b_c.setSuccessorValue(business_state_c)
    business_link_b_d.setSuccessorValue(business_state_d)
    business_link_c_d.setSuccessorValue(business_state_d)
    business_link_d_e.setSuccessorValue(business_state_e)

    business_process.edit(referential_date='stop_date')
    business_link_a_b.edit(title='a_b', lead_time=2, wait_time=1)
    business_link_b_c.edit(title='b_c', lead_time=2, wait_time=1)
    business_link_b_d.edit(title='b_d', lead_time=3, wait_time=1)
    business_link_c_d.edit(title='c_d', lead_time=3, wait_time=0)
    business_link_d_e.edit(title='d_e', lead_time=4, wait_time=2)

    # root explanation
    business_link_b_d.edit(deliverable=True)
    self.stepTic()

    """
    Basic test, lead time of reality and simulation are consistent.
    """
    class Mock:
      def __init__(self, date):
        self.date = date
      def getStartDate(self):
        return self.date
      def getStopDate(self):
        return self.date + 3 # lead time of reality

    base_date = DateTime('2009/04/01 GMT+9')
    mock = Mock(base_date)

    # root explanation.
    self.assertEquals(business_link_b_d.getExpectedStartDate(mock), DateTime('2009/04/01 GMT+9'))
    self.assertEquals(business_link_b_d.getExpectedStopDate(mock), DateTime('2009/04/04 GMT+9'))

    # assertion for each path without root explanation.
    self.assertEquals(business_link_a_b.getExpectedStartDate(mock), DateTime('2009/03/27 GMT+9'))
    self.assertEquals(business_link_a_b.getExpectedStopDate(mock), DateTime('2009/03/29 GMT+9'))
    self.assertEquals(business_link_b_c.getExpectedStartDate(mock), DateTime('2009/03/30 GMT+9'))
    self.assertEquals(business_link_b_c.getExpectedStopDate(mock), DateTime('2009/04/01 GMT+9'))
    self.assertEquals(business_link_c_d.getExpectedStartDate(mock), DateTime('2009/04/01 GMT+9'))
    self.assertEquals(business_link_c_d.getExpectedStopDate(mock), DateTime('2009/04/04 GMT+9'))
    self.assertEquals(business_link_d_e.getExpectedStartDate(mock), DateTime('2009/04/06 GMT+9'))
    self.assertEquals(business_link_d_e.getExpectedStopDate(mock), DateTime('2009/04/10 GMT+9'))

    """
    Test of illegal case, lead time of reality and simulation are inconsistent,
    always reality is taken, but it depends on which date(e.g. start_date and stop_date) is referential.

    How we know which is referential, currently implementation of it can be known by
    BusinessProcess.isStartDateReferential and BusinessProcess.isStopDateReferential.

    In this test case, stop_date on business_link_b_d is referential, because business_link_b_d is
    root explanation and business_process refer to stop_date as referential.

    calculation example(when referential date is 2009/04/06 GMT+9):
    start_date of business_link_b_d = referential_date - 3(lead_time of business_link_b_d)
                                    = 2009/04/06 GMT+9 - 3
                                    = 2009/04/03 GMT+9
    """
    class Mock:
      def __init__(self, date):
        self.date = date
      def getStartDate(self):
        return self.date
      def getStopDate(self):
        return self.date + 5 # changed

    base_date = DateTime('2009/04/01 GMT+9')
    mock = Mock(base_date)

    self.assertEquals(business_link_b_d.getExpectedStartDate(mock), DateTime('2009/04/03 GMT+9'))
    # This is base in this context, because referential_date is 'stop_date'
    self.assertEquals(business_link_b_d.getExpectedStopDate(mock), DateTime('2009/04/06 GMT+9'))

    # assertion for each path without root explanation.
    self.assertEquals(business_link_a_b.getExpectedStartDate(mock), DateTime('2009/03/29 GMT+9'))
    self.assertEquals(business_link_a_b.getExpectedStopDate(mock), DateTime('2009/03/31 GMT+9'))
    self.assertEquals(business_link_b_c.getExpectedStartDate(mock), DateTime('2009/04/01 GMT+9'))
    self.assertEquals(business_link_b_c.getExpectedStopDate(mock), DateTime('2009/04/03 GMT+9'))
    self.assertEquals(business_link_c_d.getExpectedStartDate(mock), DateTime('2009/04/03 GMT+9'))
    self.assertEquals(business_link_c_d.getExpectedStopDate(mock), DateTime('2009/04/06 GMT+9'))
    self.assertEquals(business_link_d_e.getExpectedStartDate(mock), DateTime('2009/04/08 GMT+9'))
    self.assertEquals(business_link_d_e.getExpectedStopDate(mock), DateTime('2009/04/12 GMT+9'))

class TestBPMDummyDeliveryMovementMixin(TestBPMMixin):
  def _createDelivery(self, **kw):
    return self.folder.newContent(portal_type='Dummy Delivery', **kw)

  def _createMovement(self, delivery, **kw):
    return delivery.newContent(portal_type='Dummy Movement', **kw)

  def getBusinessTemplateList(self):
    return TestBPMMixin.getBusinessTemplateList(self) \
        + ('erp5_dummy_movement', )

  def afterSetUp(self):
    TestBPMMixin.afterSetUp(self)
    if not hasattr(self.portal, 'testing_folder'):
      self.portal.newContent(portal_type='Folder',
                            id='testing_folder')
    self.folder = self.portal.testing_folder
    self.stepTic()

  def beforeTearDown(self):
    TestBPMMixin.beforeTearDown(self)
    self.portal.deleteContent(id='testing_folder')
    self.stepTic()

  completed_state = 'delivered'
  frozen_state = 'confirmed'

  completed_state_list = [completed_state, frozen_state]
  frozen_state_list = [frozen_state]

  def _createOrderedDeliveredInvoicedBusinessProcess(self):
    # simple business process preparation
    business_process = self.createBusinessProcess()
    category_tool = self.getCategoryTool()
    ordered = category_tool.trade_state.ordered
    delivered = category_tool.trade_state.delivered
    invoiced = category_tool.trade_state.invoiced

    # path which is completed, as soon as related simulation movements are in
    # proper state
    self.order_path = self.createBusinessLink(business_process,
        successor_value = ordered,
        trade_phase='default/order',
        completed_state_list = self.completed_state_list,
        frozen_state_list = self.frozen_state_list)

    self.delivery_path = self.createBusinessLink(business_process,
        predecessor_value = ordered, successor_value = delivered,
        trade_phase='default/delivery',
        completed_state_list = self.completed_state_list,
        frozen_state_list = self.frozen_state_list)

    self.invoice_path = self.createBusinessLink(business_process,
        predecessor_value = delivered, successor_value = invoiced,
        trade_phase='default/invoicing')
    self.stepTic()

  def _createOrderedInvoicedDeliveredBusinessProcess(self):
    business_process = self.createBusinessProcess()
    category_tool = self.getCategoryTool()
    ordered = category_tool.trade_state.ordered
    delivered = category_tool.trade_state.delivered
    invoiced = category_tool.trade_state.invoiced

    self.order_path = self.createBusinessLink(business_process,
        successor_value = ordered,
        trade_phase='default/order',
        completed_state_list = self.completed_state_list,
        frozen_state_list = self.frozen_state_list)

    self.invoice_path = self.createBusinessLink(business_process,
        predecessor_value = ordered, successor_value = invoiced,
        trade_phase='default/invoicing',
        completed_state_list = self.completed_state_list,
        frozen_state_list = self.frozen_state_list)

    self.delivery_path = self.createBusinessLink(business_process,
        predecessor_value = invoiced, successor_value = delivered,
        trade_phase='default/delivery')
    self.stepTic()

class TestBPMisBuildableImplementation(TestBPMDummyDeliveryMovementMixin):
  def test_isBuildable_OrderedDeliveredInvoiced(self):
    """Test isBuildable for ordered, delivered and invoiced sequence

    Here Business Process sequence corresponds simulation tree.

    delivery_path is related to root applied rule, and invoice_path is related
    to rule below, and invoice_path is after delivery_path
    """
    self._createOrderedDeliveredInvoicedBusinessProcess()
    # create order and order line to have starting point for business process
    order = self._createDelivery()
    order_line = self._createMovement(order)

    # first level rule with simulation movement
    applied_rule = self.portal.portal_simulation.newContent(
        portal_type='Applied Rule', causality_value=order)

    simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.order_path
    )

    # second level rule with simulation movement
    delivery_rule = simulation_movement.newContent(
        portal_type='Applied Rule')
    delivery_simulation_movement = delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    # third level rule with simulation movement
    invoicing_rule = delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    invoicing_simulation_movement = invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    # split simulation movement for first level applied rule
    split_simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement', delivery_value = order_line,
      causality_value = self.order_path)

    # second level rule with simulation movement for split parent movement
    split_delivery_rule = split_simulation_movement.newContent(
        portal_type='Applied Rule')
    split_delivery_simulation_movement = split_delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    # third level rule with simulation movement for split parent movement
    split_invoicing_rule = split_delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    split_invoicing_simulation_movement = split_invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    order.setSimulationState(self.completed_state)
    self.stepTic()

    # in the beginning only order related movements shall be buildable
    self.assertEquals(self.delivery_path.isBuildable(order), True)
    self.assertEquals(delivery_simulation_movement.isBuildable(), True)
    self.assertEquals(split_delivery_simulation_movement.isBuildable(), True)

    self.assertEquals(self.invoice_path.isBuildable(order), False)
    self.assertEquals(invoicing_simulation_movement.isBuildable(), False)
    self.assertEquals(split_invoicing_simulation_movement.isBuildable(),
        False)

    # add delivery
    delivery = self._createDelivery(causality_value = order)
    delivery_line = self._createMovement(delivery)

    # relate not split movement with delivery (deliver it)
    delivery_simulation_movement.edit(delivery_value = delivery_line)

    self.stepTic()

    # delivery_path (for order) is still buildable, as split movement is not
    # delivered yet
    #
    # invoice_path is not yet buildable, delivery is in inproper simulation
    # state
    #
    # delivery_path (for delivery) is not buildable - delivery is already
    # built for those movements
    self.assertEquals(self.delivery_path.isBuildable(order), True)
    self.assertEquals(split_delivery_simulation_movement.isBuildable(), True)

    self.assertEquals(self.delivery_path.isBuildable(delivery), False)
    self.assertEquals(self.invoice_path.isBuildable(delivery), False)
    self.assertEquals(delivery_simulation_movement.isBuildable(), False)
    self.assertEquals(invoicing_simulation_movement.isBuildable(), False)
    self.assertEquals(self.invoice_path.isBuildable(order), False)
    self.assertEquals(split_invoicing_simulation_movement.isBuildable(),
        False)

    # put delivery in simulation state configured on path (and this state is
    # available directly on movements)

    delivery.setSimulationState(self.completed_state)

    self.assertEqual(self.completed_state, delivery.getSimulationState())

    self.stepTic()

    # delivery_path (for order) is still buildable, as split movement is not
    # delivered yet
    #
    # invoicing_path (for delivery and order) is buildable - in case of order,
    # because part of tree is buildable
    #
    # split movement for invoicing is not buildable - no proper delivery
    # related for previous path
    self.assertEquals(self.delivery_path.isBuildable(order), True)
    self.assertEquals(invoicing_simulation_movement.isBuildable(), True)
    self.assertEquals(self.invoice_path.isBuildable(delivery), True)

    # XXX look at comments in BusinessLink.isBuildable
    self.assertEquals(self.invoice_path.isBuildable(order), True)

    self.assertEquals(self.delivery_path.isBuildable(delivery), False)
    self.assertEquals(delivery_simulation_movement.isBuildable(), False)
    self.assertEquals(split_invoicing_simulation_movement.isBuildable(),
        False)

  def test_isBuildable_OrderedInvoicedDelivered(self):
    """Test isBuildable for ordered, invoiced and delivered sequence

    Here Business Process sequence do not corresponds simulation tree.

    delivery_path is related to root applied rule, and invoice_path is related
    to rule below, but invoice_path is before delivery_path in seuqence.
    """
    self._createOrderedInvoicedDeliveredBusinessProcess()

    order = self._createDelivery()
    order_line = self._createMovement(order)

    applied_rule = self.portal.portal_simulation.newContent(
        portal_type='Applied Rule', causality_value=order)

    simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.order_path
    )

    delivery_rule = simulation_movement.newContent(
        portal_type='Applied Rule')
    delivery_simulation_movement = delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    invoicing_rule = delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    invoicing_simulation_movement = invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    order.setSimulationState(self.completed_state)
    self.stepTic()

    self.assertEquals(self.delivery_path.isBuildable(order), False)
    self.assertEquals(delivery_simulation_movement.isBuildable(), False)

    self.assertEquals(self.invoice_path.isBuildable(order), True)
    self.assertEquals(invoicing_simulation_movement.isBuildable(), True)

    delivery = self._createDelivery(causality_value = order)
    delivery_line = self._createMovement(delivery)

    invoicing_simulation_movement.edit(delivery_value = delivery_line)

    self.stepTic()

    self.assertEquals(self.delivery_path.isBuildable(order), False)

    self.assertEquals(self.delivery_path.isBuildable(delivery), False)
    self.assertEquals(self.invoice_path.isBuildable(delivery), False)
    self.assertEquals(delivery_simulation_movement.isBuildable(), False)
    self.assertEquals(invoicing_simulation_movement.isBuildable(), False)
    self.assertEquals(self.invoice_path.isBuildable(order), False)

    # put delivery in simulation state configured on path (and this state is
    # available directly on movements)

    delivery.setSimulationState(self.completed_state)

    self.assertEqual(self.completed_state, delivery.getSimulationState())

    self.stepTic()

    self.assertEquals(self.delivery_path.isBuildable(order), True)
    self.assertEquals(self.delivery_path.isBuildable(delivery), True)
    self.assertEquals(invoicing_simulation_movement.isBuildable(), False)
    self.assertEquals(self.invoice_path.isBuildable(delivery), False)
    self.assertEquals(self.invoice_path.isBuildable(order), False)
    self.assertEquals(delivery_simulation_movement.isBuildable(), True)

    # now simulate compensation

    compensated_simulation_movement = delivery_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.delivery_path
    )

    compensated_invoicing_rule = compensated_simulation_movement.newContent(
        portal_type='Applied Rule')

    compensated_invoicing_simulation_movement = compensated_invoicing_rule \
      .newContent(portal_type='Simulation Movement',
          causality_value = self.invoice_path)

    # and delivery some part of tree

    another_delivery = self._createDelivery(causality_value = delivery)
    another_delivery_line = self._createMovement(another_delivery)

    delivery_simulation_movement.edit(delivery_value=another_delivery_line)

    self.stepTic()

    self.assertEquals(self.delivery_path.isBuildable(order), False)

    self.assertEquals(delivery_simulation_movement.isBuildable(), False)
    self.assertEquals(invoicing_simulation_movement.isBuildable(), False)

    self.assertEquals(self.invoice_path.isBuildable(order), True)
    self.assertEquals(compensated_invoicing_simulation_movement.isBuildable(),
        True)

    self.assertEquals(compensated_simulation_movement.isBuildable(), False)

class TestBPMisCompletedImplementation(TestBPMDummyDeliveryMovementMixin):
  def test_isCompleted_OrderedDeliveredInvoiced(self):
    """Test isCompleted for ordered, delivered and invoiced sequence"""
    self._createOrderedDeliveredInvoicedBusinessProcess()

    # create order and order line to have starting point for business process
    order = self._createDelivery()
    order_line = self._createMovement(order)

    # first level rule with simulation movement
    applied_rule = self.portal.portal_simulation.newContent(
        portal_type='Applied Rule', causality_value=order)

    simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.order_path
    )

    # second level rule with simulation movement
    delivery_rule = simulation_movement.newContent(
        portal_type='Applied Rule')
    delivery_simulation_movement = delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    # third level rule with simulation movement
    invoicing_rule = delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    invoicing_simulation_movement = invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    # split simulation movement for first level applied rule
    split_simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement', delivery_value = order_line,
      causality_value = self.order_path)

    # second level rule with simulation movement for split parent movement
    split_delivery_rule = split_simulation_movement.newContent(
        portal_type='Applied Rule')
    split_delivery_simulation_movement = split_delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    # third level rule with simulation movement for split parent movement
    split_invoicing_rule = split_delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    split_invoicing_simulation_movement = split_invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    self.stepTic()

    self.assertEqual(self.delivery_path.isCompleted(order), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(order), False)

    self.assertEqual(self.invoice_path.isCompleted(order), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(order), False)

    # add delivery
    delivery = self._createDelivery(causality_value = order)
    delivery_line = self._createMovement(delivery)

    # relate not split movement with delivery (deliver it)
    delivery_simulation_movement.edit(delivery_value = delivery_line)

    self.stepTic()

    # nothing changes
    self.assertEqual(self.delivery_path.isCompleted(order), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(order), False)

    self.assertEqual(self.invoice_path.isCompleted(order), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(order), False)

    # from delivery point of view everything is same
    self.assertEqual(self.delivery_path.isCompleted(delivery), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(delivery), False)

    self.assertEqual(self.invoice_path.isCompleted(delivery), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(delivery), False)

    # put delivery in simulation state configured on path (and this state is
    # available directly on movements)

    delivery.setSimulationState(self.completed_state)

    self.assertEqual(self.completed_state, delivery.getSimulationState())

    self.stepTic()

    self.assertEqual(self.delivery_path.isCompleted(order), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(order), True)

    self.assertEqual(self.invoice_path.isCompleted(order), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(order), False)

    self.assertEqual(self.delivery_path.isCompleted(delivery), True)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(delivery), True)

    self.assertEqual(self.invoice_path.isCompleted(delivery), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(delivery), False)

  def test_isCompleted_OrderedInvoicedDelivered(self):
    """Test isCompleted for ordered, invoiced and invoiced sequence"""
    self._createOrderedInvoicedDeliveredBusinessProcess()

    order = self._createDelivery()
    order_line = self._createMovement(order)

    applied_rule = self.portal.portal_simulation.newContent(
        portal_type='Applied Rule', causality_value=order)

    simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.delivery_path
    )

    delivery_rule = simulation_movement.newContent(
        portal_type='Applied Rule')
    delivery_simulation_movement = delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    invoicing_rule = delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    invoicing_simulation_movement = invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    self.stepTic()

    self.assertEqual(self.delivery_path.isCompleted(order), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(order), False)

    self.assertEqual(self.invoice_path.isCompleted(order), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(order), False)

    delivery = self._createDelivery(causality_value = order)
    delivery_line = self._createMovement(delivery)

    invoicing_simulation_movement.edit(delivery_value = delivery_line)

    self.stepTic()

    self.assertEqual(self.delivery_path.isCompleted(order), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(order), False)

    self.assertEqual(self.invoice_path.isCompleted(order), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(order), False)

    self.assertEqual(self.delivery_path.isCompleted(delivery), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(delivery), False)

    self.assertEqual(self.invoice_path.isCompleted(delivery), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(delivery), False)

    # put delivery in simulation state configured on path (and this state is
    # available directly on movements)

    delivery.setSimulationState(self.completed_state)

    self.assertEqual(self.completed_state, delivery.getSimulationState())

    self.stepTic()

    self.assertEqual(self.delivery_path.isCompleted(order), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(order), False)

    self.assertEqual(self.invoice_path.isCompleted(order), True)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(order), True)

    self.assertEqual(self.delivery_path.isCompleted(delivery), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(delivery), False)

    self.assertEqual(self.invoice_path.isCompleted(delivery), True)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(delivery), True)

    # now simulate compensation

    compensated_simulation_movement = delivery_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.delivery_path
    )

    compensated_invoicing_rule = compensated_simulation_movement.newContent(
        portal_type='Applied Rule')

    compensated_invoicing_simulation_movement = compensated_invoicing_rule \
        .newContent(portal_type='Simulation Movement',
            causality_value = self.invoice_path)

    # and delivery some part of tree

    another_delivery = self._createDelivery(causality_value = delivery)
    another_delivery_line = self._createMovement(another_delivery)

    delivery_simulation_movement.edit(delivery_value=another_delivery_line)

    self.stepTic()

    self.assertEqual(self.delivery_path.isCompleted(order), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(order), False)

    self.assertEqual(self.invoice_path.isCompleted(order), False)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(order), True)

    self.assertEqual(self.delivery_path.isCompleted(delivery), False)
    self.assertEqual(self.delivery_path.isPartiallyCompleted(delivery), False)

    self.assertEqual(self.invoice_path.isCompleted(delivery), True)
    self.assertEqual(self.invoice_path.isPartiallyCompleted(delivery), True)

class TestBPMisFrozenImplementation(TestBPMDummyDeliveryMovementMixin):
  def test_isFrozen_OrderedDeliveredInvoiced(self):
    """Test isFrozen for ordered, delivered and invoiced sequence"""
    self._createOrderedDeliveredInvoicedBusinessProcess()

    # create order and order line to have starting point for business process
    order = self._createDelivery()
    order_line = self._createMovement(order)

    # first level rule with simulation movement
    applied_rule = self.portal.portal_simulation.newContent(
        portal_type='Applied Rule', causality_value=order)

    simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.delivery_path
    )

    # second level rule with simulation movement
    delivery_rule = simulation_movement.newContent(
        portal_type='Applied Rule')
    delivery_simulation_movement = delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    # third level rule with simulation movement
    invoicing_rule = delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    invoicing_simulation_movement = invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    # split simulation movement for first level applied rule
    split_simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement', delivery_value = order_line,
      causality_value = self.order_path)

    # second level rule with simulation movement for split parent movement
    split_delivery_rule = split_simulation_movement.newContent(
        portal_type='Applied Rule')
    split_delivery_simulation_movement = split_delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    # third level rule with simulation movement for split parent movement
    split_invoicing_rule = split_delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    split_invoicing_simulation_movement = split_invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    self.stepTic()

    self.assertEqual(self.delivery_path.isFrozen(order), False)
    self.assertEqual(self.invoice_path.isFrozen(order), False)

    self.assertEqual(simulation_movement.isFrozen(), False)
    self.assertEqual(invoicing_simulation_movement.isFrozen(), False)
    self.assertEqual(split_simulation_movement.isFrozen(), False)
    self.assertEqual(split_invoicing_simulation_movement.isFrozen(), False)

    # add delivery
    delivery = self._createDelivery(causality_value = order)
    delivery_line = self._createMovement(delivery)

    # relate not split movement with delivery (deliver it)
    delivery_simulation_movement.edit(delivery_value = delivery_line)

    self.stepTic()

    # nothing changes
    self.assertEqual(self.delivery_path.isFrozen(order), False)
    self.assertEqual(self.invoice_path.isFrozen(order), False)

    # from delivery point of view everything is same
    self.assertEqual(self.delivery_path.isFrozen(delivery), False)
    self.assertEqual(self.invoice_path.isFrozen(delivery), False)

    self.assertEqual(simulation_movement.isFrozen(), False)
    self.assertEqual(invoicing_simulation_movement.isFrozen(), False)
    self.assertEqual(split_simulation_movement.isFrozen(), False)
    self.assertEqual(split_invoicing_simulation_movement.isFrozen(), False)

    # put delivery in simulation state configured on path (and this state is
    # available directly on movements)

    delivery.setSimulationState(self.frozen_state)

    self.assertEqual(self.frozen_state, delivery.getSimulationState())

    self.stepTic()

    self.assertEqual(self.delivery_path.isFrozen(order), False)
    self.assertEqual(self.invoice_path.isFrozen(order), False)
    self.assertEqual(self.delivery_path.isFrozen(delivery), False)
    self.assertEqual(self.invoice_path.isFrozen(delivery), False)

    self.assertEqual(delivery_simulation_movement.isFrozen(), True)
    self.assertEqual(invoicing_simulation_movement.isFrozen(), False)
    self.assertEqual(split_simulation_movement.isFrozen(), False)
    self.assertEqual(split_invoicing_simulation_movement.isFrozen(), False)

  def test_isFrozen_OrderedInvoicedDelivered(self):
    """Test isFrozen for ordered, invoiced and invoiced sequence"""
    self._createOrderedInvoicedDeliveredBusinessProcess()

    order = self._createDelivery()
    order_line = self._createMovement(order)

    applied_rule = self.portal.portal_simulation.newContent(
        portal_type='Applied Rule', causality_value=order)

    simulation_movement = applied_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.delivery_path
    )

    delivery_rule = simulation_movement.newContent(
        portal_type='Applied Rule')
    delivery_simulation_movement = delivery_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.delivery_path)

    invoicing_rule = delivery_simulation_movement.newContent(
        portal_type='Applied Rule')
    invoicing_simulation_movement = invoicing_rule.newContent(
        portal_type='Simulation Movement',
        causality_value = self.invoice_path)

    self.stepTic()

    self.assertEqual(self.delivery_path.isFrozen(order), False)
    self.assertEqual(self.invoice_path.isFrozen(order), False)

    self.assertEqual(simulation_movement.isFrozen(), False)
    self.assertEqual(invoicing_simulation_movement.isFrozen(), False)

    delivery = self._createDelivery(causality_value = order)
    delivery_line = self._createMovement(delivery)

    invoicing_simulation_movement.edit(delivery_value = delivery_line)

    self.stepTic()

    self.assertEqual(self.delivery_path.isFrozen(order), False)
    self.assertEqual(self.invoice_path.isFrozen(order), False)
    self.assertEqual(self.delivery_path.isFrozen(delivery), False)
    self.assertEqual(self.invoice_path.isFrozen(delivery), False)

    self.assertEqual(simulation_movement.isFrozen(), False)
    self.assertEqual(invoicing_simulation_movement.isFrozen(), False)

    # put delivery in simulation state configured on path (and this state is
    # available directly on movements)

    delivery.setSimulationState(self.frozen_state)

    self.assertEqual(self.frozen_state, delivery.getSimulationState())

    self.stepTic()

    self.assertEqual(self.delivery_path.isFrozen(order), False)
    self.assertEqual(self.invoice_path.isFrozen(order), True)
    self.assertEqual(self.delivery_path.isFrozen(delivery), False)
    self.assertEqual(self.invoice_path.isFrozen(delivery), True)

    self.assertEqual(simulation_movement.isFrozen(), False)
    self.assertEqual(invoicing_simulation_movement.isFrozen(), True)

    # now simulate compensation

    compensated_simulation_movement = delivery_rule.newContent(
      portal_type = 'Simulation Movement',
      delivery_value = order_line,
      causality_value = self.delivery_path
    )

    compensated_invoicing_rule = compensated_simulation_movement.newContent(
        portal_type='Applied Rule')

    compensated_invoicing_simulation_movement = compensated_invoicing_rule \
        .newContent(portal_type='Simulation Movement',
            causality_value = self.invoice_path)

    # and delivery some part of tree

    another_delivery = self._createDelivery(causality_value = delivery)
    another_delivery_line = self._createMovement(another_delivery)

    delivery_simulation_movement.edit(delivery_value=another_delivery_line)

    self.stepTic()

    self.assertEqual(self.delivery_path.isFrozen(order), False)

    self.assertEqual(self.invoice_path.isFrozen(order), False)

    self.assertEqual(self.delivery_path.isFrozen(delivery), False)

    self.assertEqual(self.invoice_path.isFrozen(delivery), True)

    self.assertEqual(simulation_movement.isFrozen(), False)
    self.assertEqual(invoicing_simulation_movement.isFrozen(), True)

    self.assertEqual(compensated_simulation_movement.isFrozen(), False)
    self.assertEqual(compensated_invoicing_simulation_movement.isFrozen(),
        False)

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestBPMImplementation))
  suite.addTest(unittest.makeSuite(TestBPMisBuildableImplementation))
  suite.addTest(unittest.makeSuite(TestBPMisCompletedImplementation))
  suite.addTest(unittest.makeSuite(TestBPMisFrozenImplementation))
  return suite
