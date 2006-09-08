##############################################################################
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

"""Unit Tests for Inventory API.
"""

import sys
import random
import os

if __name__ == '__main__':
  execfile(os.path.join(sys.path[0], 'framework.py'))

from AccessControl.SecurityManagement import newSecurityManager
from DateTime import DateTime
from Testing import ZopeTestCase

from Products.ERP5.Document.OrderRule import OrderRule
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase

# Needed in order to have a log file inside the current folder
os.environ.setdefault('EVENT_LOG_FILE', 'zLOG.log')
os.environ.setdefault('EVENT_LOG_SEVERITY', '-300')

class InventoryAPITestCase(ERP5TypeTestCase):
  """Base class for Inventory API Tests {{{
  """
  RUN_ALL_TESTS = 1

  GROUP_CATEGORIES = ( 'group/test_group/A1/B1/C1',
                       'group/test_group/A1/B1/C2',
                       'group/test_group/A1/B2/C1',
                       'group/test_group/A1/B2/C2',
                       'group/test_group/A2/B1/C1',
                       'group/test_group/A2/B1/C2',
                       'group/test_group/A2/B2/C1',
                       'group/test_group/A2/B2/C2', )
  
  def getTitle(self):
    """Title of the test."""
    return self.__class__.__doc__

  def afterSetUp(self):
    """set up """
    self.createCategories()
    self.login()
    self.portal = self.getPortal()
    if not hasattr(self.portal, 'testing_folder'):
      self.portal.newContent(portal_type='Folder',
                                              id='testing_folder')
    self.folder = self.portal.testing_folder
    
    self.section = self._makeOrganisation(title='Section')
    self.node = self._makeOrganisation(title='Node')
    self.payment_node = self.section.newContent(
                                  title='Payment Node',
                                  portal_type='Bank Account')
    self.mirror_section = self._makeOrganisation(title='Mirror Section')
    self.mirror_node = self._makeOrganisation(title='Mirror Node')
    self.resource = self.getCurrencyModule().newContent(
                                  title='Resource',
                                  portal_type='Currency')
    # create a dummy Rule, to be able to create simulation movements
    rule_tool = self.portal.portal_rules
    if not hasattr(rule_tool, 'default_order_rule'):
      rule_tool._setObject('default_order_rule',
                           OrderRule('default_order_rule'))

  def _safeTic(self):
    """Like tic, but swallowing errors, usefull for teardown"""
    try:
      get_transaction().commit()
      self.tic()
    except RuntimeError:
      pass

  def beforeTearDown(self):
    """Clear everything for next test."""
    self._safeTic()
    for module in [ 'organisation_module',
                    'person_module',
                    'currency_module',
                    'portal_simulation',
                    self.folder.getId() ]:
      folder = getattr(self.getPortal(), module, None)
      if folder:
        [x.unindexObject() for x in folder.objectValues()]
        self._safeTic()
        folder.manage_delObjects([x.getId() for x in folder.objectValues()])
    self._safeTic()
    # cancel remaining messages
    activity_tool = self.getPortal().portal_activities
    for message in activity_tool.getMessageList():
      activity_tool.manageCancel(message.object_path, message.method_id)
      ZopeTestCase._print('\nCancelling active message %s.%s()\n'
                          % (message.object_path, message.method_id) )
    get_transaction().commit()

  def login(self, quiet=0, run=1):
    uf = self.getPortal().acl_users
    uf._doAddUser('alex', '', ['Manager', 'Assignee', 'Assignor',
                               'Associate', 'Auditor', 'Author'], [])
    user = uf.getUserById('alex').__of__(uf)
    newSecurityManager(None, user)
  
  def createCategories(self):
    """Create the categories for our test. """
    # create categories
    for cat_string in self.getNeededCategoryList() :
      base_cat = cat_string.split("/")[0]
      path = self.getPortal().portal_categories[base_cat]
      for cat in cat_string.split("/")[1:] :
        if not cat in path.objectIds() :
          path = path.newContent(
                    portal_type='Category',
                    id=cat,
                    immediate_reindex=1 )
        else:
          path = path[cat]
    # check categories have been created
    for cat_string in self.getNeededCategoryList() :
      self.assertNotEquals(None,
                self.getCategoryTool().restrictedTraverse(cat_string),
                cat_string)
                
  def getNeededCategoryList(self):
    """return a list of categories that should be created."""
    return (  'region/level1/level2',
              'group/level1/level2',
              'group/anotherlevel',
              'product_line/level1/level2',
           # we create a huge group category for consolidation tests
           ) + self.GROUP_CATEGORIES
  
  def getBusinessTemplateList(self):
    """ """
    return ('erp5_base', 'erp5_dummy_movement')

  # TODO: move this to a base class {{{
  def _makeOrganisation(self, **kw):
    """Creates an organisation."""
    org = self.getPortal().organisation_module.newContent(
          portal_type='Organisation',
          **kw)
    get_transaction().commit()
    self.tic()
    return org

  def _makeSalePackingList(self, **kw):
    """Creates a sale packing list."""
    spl = self.getPortal().sale_packing_list_module.newContent(
          portal_type='Sale Packing List',)
    spl.edit(**kw)
    get_transaction().commit()
    self.tic()
    return spl
  
  def _makeSaleInvoice(self, created_by_builder=0, **kw):
    """Creates a sale invoice."""
    sit = self.getPortal().accounting_module.newContent(
          portal_type='Sale Invoice Transaction',
          created_by_builder=created_by_builder)
    sit.edit(**kw)
    get_transaction().commit()
    self.tic()
    return sit

  def _makeCurrency(self, **kw):
    """Creates a currency."""
    currency = self.getCurrencyModule().newContent(
            portal_type = 'Currency', **kw)
    get_transaction().commit()
    self.tic()
    return currency
  _makeResource = _makeCurrency
  # }}}

  def _makeMovement(self, **kw):
    """Creates a movement.
    """
    mvt = self.folder.newContent(portal_type='Dummy Movement')
    kw.setdefault('destination_section_value', self.section)
    kw.setdefault('source_section_value', self.mirror_section)
    kw.setdefault('destination_value', self.node)
    kw.setdefault('source_value', self.mirror_node)
    kw.setdefault('resource_value', self.resource)
    mvt.edit(**kw)
    get_transaction().commit()
    self.tic()
    return mvt

  def _makeSimulationMovement(self, **kw):
    """Creates a simulation movement.
    """
    ar = self.getSimulationTool().newContent(portal_type='Applied Rule')
    # we created a default_order_rule in setUp
    ar.setSpecialise('portal_rules/default_order_rule')
    mvt = ar.newContent(portal_type='Simulation Movement')
    kw.setdefault('destination_section_value', self.section)
    kw.setdefault('source_section_value', self.mirror_section)
    kw.setdefault('destination_value', self.node)
    kw.setdefault('source_value', self.mirror_node)
    kw.setdefault('resource_value', self.resource)
    mvt.edit(**kw)
    get_transaction().commit()
    self.tic()
    return mvt

# }}}

class TestInventory(InventoryAPITestCase):
  """Tests getInventory methods.
  """
  RUN_ALL_TESTS = 1
  
  def testReturnedTypeIsFloat(self):
    """getInventory returns a float"""
    # XXX it may return a Decimal some day
    getInventory = self.getSimulationTool().getInventory
    self.assertEquals(type(getInventory()), type(0.1))
    # default is 0
    self.assertEquals(0, getInventory())

  def test_SimulationMovement(self, quiet=0, run=RUN_ALL_TESTS):
    """Test Simulation Movements works in this testing environnement.
    """
    getInventory = self.getSimulationTool().getInventory
    self._makeSimulationMovement(quantity=100)
    self.assertEquals(100, getInventory(section_uid=self.section.getUid()))
    # mixed with a real movement
    self._makeMovement(quantity=100)
    self.assertEquals(200, getInventory(section_uid=self.section.getUid()))

  def test_SimulationMovementisAccountable(self, quiet=0, run=RUN_ALL_TESTS):
    """Test Simulation Movements are not accountable if related to a delivery.
    """
    getInventory = self.getSimulationTool().getInventory
    sim_mvt = self._makeSimulationMovement(quantity=100)
    mvt = self._makeMovement(quantity=100)
    # simulation movement are accountable,
    self.failUnless(sim_mvt.isAccountable())
    # unless connected to a delivery movement
    sim_mvt.setDeliveryValue(mvt)
    self.failIf(sim_mvt.isAccountable())
    # not accountable movement are not counted by getInventory
    get_transaction().commit(); self.tic() # (after reindexing of course)
    self.assertEquals(100, getInventory(section_uid=self.section.getUid()))
  
  def test_OmitSimulation(self, quiet=0, run=RUN_ALL_TESTS):
    """Test omit_simulation argument to getInventory.
    """
    getInventory = self.getSimulationTool().getInventory
    self._makeSimulationMovement(quantity=100)
    self._makeMovement(quantity=100)
    self.assertEquals(100, getInventory(section_uid=self.section.getUid(),
                                        omit_simulation=1))

  def test_SectionCategory(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests inventory on section category. """
    getInventory = self.getSimulationTool().getInventory
    self.section.setGroup('level1/level2')
    self._makeMovement(quantity=100)
    self.assertEquals(getInventory(
                        section_category='group/level1'), 100)
    self.assertEquals(getInventory(
                        section_category='group/level1/level2'), 100)
    self.assertEquals(getInventory(
                        section_category='group/anotherlevel'), 0)
    
    # section category can be a list
    self.assertEquals(getInventory(
            section_category=['group/anotherlevel', 'group/level1']), 100)

    # strict_section_category only takes movement where section is strict
    # member of the category.
    self.assertEquals(getInventory(
                section_category_strict_membership=['group/level1']), 0)
    self.section.setGroup('level1')
    get_transaction().commit()
    self.tic()
    self.assertEquals(getInventory(
                section_category_strict_membership=['group/level1']), 100)
    
    # non existing values to section_category are not silently ignored, but
    # raises an exception
    self.assertRaises(ValueError,
                      getInventory,
                      section_category='group/notexists')

  def test_MirrorSectionCategory(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests inventory on mirror section category. """
    getInventory = self.getSimulationTool().getInventory
    self.mirror_section.setGroup('level1/level2')
    self._makeMovement(quantity=100)
    self.assertEquals(getInventory(
                        mirror_section_category='group/level1'), 100)
    self.assertEquals(getInventory(
                        mirror_section_category='group/level1/level2'), 100)
    self.assertEquals(getInventory(
                        mirror_section_category='group/anotherlevel'), 0)
    
    # section category can be a list
    self.assertEquals(getInventory(
            mirror_section_category=['group/anotherlevel',
                                     'group/level1']), 100)

    # strict_section_category only takes movement where section is strict
    # member of the category.
    self.assertEquals(getInventory(
              mirror_section_category_strict_membership=['group/level1']), 0)
    self.mirror_section.setGroup('level1')
    get_transaction().commit()
    self.tic()
    self.assertEquals(getInventory(
            mirror_section_category_strict_membership=['group/level1']), 100)
    
    # non existing values to section_category are not silently ignored, but
    # raises an exception
    self.assertRaises(ValueError,
                      getInventory,
                      mirror_section_category='group/notexists')

  def test_NodeCategory(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests inventory on node_category """
    getInventory = self.getSimulationTool().getInventory
    self.node.setGroup('level1/level2')
    self._makeMovement(quantity=100,
                       source_value=None)
    self.assertEquals(getInventory(
                        node_category='group/level1'), 100)
    self.assertEquals(getInventory(
                        node_category='group/level1/level2'), 100)
    self.assertEquals(getInventory(
                node_category_strict_membership=['group/level1']), 0)
    self.node.setGroup('level1')
    get_transaction().commit()
    self.tic()
    self.assertEquals(getInventory(
                node_category_strict_membership=['group/level1']), 100)
  
  def test_ResourceCategory(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests inventory on resource_category """
    getInventory = self.getSimulationTool().getInventory
    self.resource.setProductLine('level1/level2')
    self._makeMovement(quantity=100,
                       source_value=None)
    self.assertEquals(getInventory(
                        resource_category='product_line/level1'), 100)
    self.assertEquals(getInventory(
                        resource_category='product_line/level1/level2'), 100)
    self.assertEquals(getInventory(
                resource_category_strict_membership=['product_line/level1']), 0)
    self.resource.setProductLine('level1')
    get_transaction().commit()
    self.tic()
    self.assertEquals(getInventory(
            resource_category_strict_membership=['product_line/level1']), 100)

  def test_PaymentCategory(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests inventory on payment_category """
    getInventory = self.getSimulationTool().getInventory
    # for now, BankAccount have a product_line category, so we can use this for
    # our category membership tests.
    self.payment_node.setProductLine('level1/level2')
    self._makeMovement(quantity=100,
                       destination_payment_value=self.payment_node,
                       source_value=None)
    self.assertEquals(getInventory(
                        payment_category='product_line/level1'), 100)
    self.assertEquals(getInventory(
                        payment_category='product_line/level1/level2'), 100)
    self.assertEquals(getInventory(
                payment_category_strict_membership=['product_line/level1']), 0)
    self.payment_node.setProductLine('level1')
    get_transaction().commit()
    self.tic()
    self.assertEquals(getInventory(
              payment_category_strict_membership=['product_line/level1']), 100)

  def test_SimulationState(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests inventory on simulation state. """
    getInventory = self.getSimulationTool().getInventory
    self.payment_node.setProductLine('level1/level2')
    self._makeMovement(quantity=100,
                       simulation_state='confirmed',
                       source_value=None)
    self.assertEquals(getInventory(), 100)
    self.assertEquals(getInventory(simulation_state='confirmed'), 100)
    self.assertEquals(getInventory(simulation_state='planned'), 0)

    self.assertEquals(getInventory(simulation_state=['planned',
                                                     'confirmed']), 100)

  def test_MultipleNodes(self, quiet=0, run=RUN_ALL_TESTS):
    """Test section category with many nodes. """
    test_group = self.getCategoryTool().resolveCategory('group/test_group')
    self.assertNotEquals(len(test_group.objectValues()), 0)
    # we first create a section for each group category
    quantity_for_node = {}
    for category in test_group.getCategoryChildValueList():
      # we create a member node for each category
      node = self._makeOrganisation(group_value=category)
      # we create a movement to each node
      quantity = random.randint(100, 1000)
      self._makeMovement(quantity=quantity,
                         destination_section_value=node,
                         destination_value=node)
      # and record for later
      quantity_for_node[node] = quantity

    getInventory = self.getSimulationTool().getInventory
    for category in test_group.getCategoryChildValueList():
      node_list = category.getGroupRelatedValueList(portal_type='Organisation')
      self.assertNotEquals(len(node_list), 0)

      # getInventory on node uid for all member of a category ...
      total_quantity = sum([quantity_for_node[node] for node in node_list])
      self.assertEquals(getInventory(
        node_uid=[node.getUid() for node in node_list]), total_quantity)
      # ... is equivalent to node_category
      self.assertEquals(getInventory(
        node_category=category.getRelativeUrl()), total_quantity)
  
  # FIXME: this test is currently broken
  def TODO_test_DoubleSectionCategory(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests inventory on section category, when the section is twice member\
    of the same category like it happens for group and mapping"""
    getInventory = self.getSimulationTool().getInventory
    self.section.setGroup('level1/level2')
    self.section.setMapping('group/level1/level2')
    self._makeMovement(quantity=100)
    # We are twice member of the section_category, but the quantity should not
    # change.
    self.assertEquals(getInventory(
                        section_category='group/level1'), 100)
    self.assertEquals(getInventory(
                        section_category='group/level1/level2'), 100)
    self.assertEquals(getInventory(
            section_category_strict_membership=['group/level1/level2']), 100)

  def test_NoSection(self, quiet=0, run=RUN_ALL_TESTS):
    """Tests inventory on section category / section uid, when the section is\
    empty."""
    getInventory = self.getSimulationTool().getInventory
    self.section.setGroup('level1/level2')
    self._makeMovement(quantity=100, source_section_value=None)
    self.assertEquals(getInventory(
                        section_category='group/level1/level2'), 100)
    self.assertEquals(getInventory(
            section_category_strict_membership=['group/level1/level2']), 100)
    self.assertEquals(getInventory(
                        section_uid=self.section.getUid()), 100)
  
class TestInventoryList(InventoryAPITestCase):
  """Tests getInventoryList methods.
  """
  RUN_ALL_TESTS = 1


class TestMovementHistoryList(InventoryAPITestCase):
  """Tests Movement history list methods.
  """
  RUN_ALL_TESTS = 1
  
  def testReturnedTypeIsList(self):
    """Movement History List returns a sequence object""" 
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt_history_list = getMovementHistoryList()
    self.failUnless(str(mvt_history_list.__class__),
                    'Shared.DC.ZRDB.Results.Results')
    # default is an empty list
    self.assertEquals(0, len(mvt_history_list))
  
  def testMovementBothSides(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=100)
    # we don't filter, so we have the same movement from both sides.
    self.assertEquals(2, len(getMovementHistoryList()))

  def testBrainClass(self):
    """Movement History List uses InventoryListBrain for brains""" 
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=100)
    # maybe this check is too low level (Shared/DC/ZRDB//Results.py, class r) 
    r_bases = getMovementHistoryList()._class.__bases__
    brain_class = r_bases[2].__name__
    self.assertEquals('InventoryListBrain', brain_class,
      "unexpected brain class for getMovementHistoryList InventoryListBrain"
      " != %s (bases %s)" % (brain_class, r_bases))
  
  def testSection(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt = self._makeMovement(quantity=100)
    mvt_history_list = getMovementHistoryList(
                            section_uid = self.section.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(mvt.getUid(), mvt_history_list[0].uid)
    self.assertEquals(100, mvt_history_list[0].total_quantity)
    self.assertEquals(self.section.getRelativeUrl(),
                  mvt_history_list[0].section_relative_url)
  
  def testMirrorSection(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt = self._makeMovement(quantity=100)
    mvt_history_list = getMovementHistoryList(
                            mirror_section_uid = self.section.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(mvt.getUid(), mvt_history_list[0].uid)
    self.assertEquals(-100, mvt_history_list[0].total_quantity)
    self.assertEquals(self.mirror_section.getRelativeUrl(),
                  mvt_history_list[0].section_relative_url)
    self.assertEquals(self.mirror_node.getRelativeUrl(),
                  mvt_history_list[0].node_relative_url)
    
    # if we look from the other side, everything is reverted
    mvt_history_list = getMovementHistoryList(
                            section_uid = self.section.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(100, mvt_history_list[0].total_quantity)
    self.assertEquals(self.section.getRelativeUrl(),
                  mvt_history_list[0].section_relative_url)
    self.assertEquals(self.node.getRelativeUrl(),
                  mvt_history_list[0].node_relative_url)
  
  def testDifferentDatesPerSection(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    start_date = DateTime(2001, 1, 1)
    stop_date = DateTime(2002, 2, 2)
    mvt = self._makeMovement(quantity=100,
                             start_date=start_date,
                             stop_date=stop_date)
    # start_date is for source
    self.assertEquals(start_date, getMovementHistoryList(
                            section_uid=self.mirror_section.getUid())[0].date)
    # stop_date is for destination
    self.assertEquals(stop_date, getMovementHistoryList(
                            section_uid=self.section.getUid())[0].date)
    
  def testNode(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt = self._makeMovement(quantity=100)
    mvt_history_list = getMovementHistoryList(
                            node_uid = self.node.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(mvt.getUid(), mvt_history_list[0].uid)
    self.assertEquals(100, mvt_history_list[0].total_quantity)

  def testMirrorNode(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt = self._makeMovement(quantity=100)
    mvt_history_list = getMovementHistoryList(
                            mirror_node_uid = self.node.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(mvt.getUid(), mvt_history_list[0].uid)
    self.assertEquals(-100, mvt_history_list[0].total_quantity)

  def testResource(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt = self._makeMovement(quantity=100)
    another_resource = self._makeResource()
    another_mvt = self._makeMovement(quantity=3,
                                     resource_value=another_resource)
    # we can query resource directly by uid
    mvt_history_list = getMovementHistoryList(
                            node_uid=self.node.getUid(),
                            resource_uid=self.resource.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(100, mvt_history_list[0].total_quantity)
    # getMovementHistoryList should return only movement for
    mvt_history_list = getMovementHistoryList(
                            node_uid=self.node.getUid(),
                            resource_uid=another_resource.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(3, mvt_history_list[0].total_quantity)

    # wrong value yields an empty list
    self.assertEquals(0, len(getMovementHistoryList(
                            resource_uid = self.node.getUid())))
  
  def testSectionCategory(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self.section.setGroup('level1/level2')
    mvt = self._makeMovement(quantity=100)

    # for section category, both exact category or any parent category works
    # section_category can also be a list.
    for section_category in [ 'group/level1',
                              'group/level1/level2',
                             ['group/level1', 'group/anotherlevel'],
                             ['group/level1', 'group/level1'],
                             ['group/level1', 'group/level1/level2'], ]:
      movement_history_list = getMovementHistoryList(
                                section_category=section_category)
      self.assertEquals(len(movement_history_list), 1)
      self.assertEquals(movement_history_list[0].total_quantity, 100)
    
    # again, bad category raises an exception
    self.assertRaises(ValueError,
                      getMovementHistoryList,
                      section_category='group/notexists')
    # (but other arguments are ignored)
    self.assertEquals(len(getMovementHistoryList(
                        section_category='group/level1',
                        ignored='argument')), 1)
    
  def testNodeCategoryAndSectionCategory(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self.section.setGroup('level1/level2')
    self.node.setGroup('level1')
    mvt = self._makeMovement(quantity=100)

    valid_category_list = [ 'group/level1',
                           ['group/level1', 'group/anotherlevel'],
                           ['group/level1', 'group/level1'],
                           ['group/level1', 'group/level1/level2'], ]
    invalid_category_list = ['group/anotherlevel', 'product_line/level1']

    # both valid
    for section_category in valid_category_list:
      for node_category in valid_category_list:
        movement_history_list = getMovementHistoryList(
                                  node_category=node_category,
                                  section_category=section_category)
        self.assertEquals(len(movement_history_list), 1)
        self.assertEquals(movement_history_list[0].total_quantity, 100)

    # if node category OR section category is not matched, no movement are
    # returned.
    for section_category in valid_category_list:
      for node_category in invalid_category_list:
        movement_history_list = getMovementHistoryList(
                                  node_category=node_category,
                                  section_category=section_category)
        self.assertEquals(len(movement_history_list), 0)

    for section_category in invalid_category_list:
      for node_category in valid_category_list:
        movement_history_list = getMovementHistoryList(
                                  node_category=node_category,
                                  section_category=section_category)
        self.assertEquals(len(movement_history_list), 0)


  # Date tests:
  # ===========
  #
  # For all date tests, we create a list of movements with dates:
  #     start_date (date for source)        stop_date(date for destination)
  #              2006/01/01                       2006/01/02
  #              2006/01/02                       2006/01/03
  #              2006/01/03                       2006/01/04
  #              2006/01/04                       2006/01/05
  # in all those tests, we usually look from the destination, so the first
  # movement is at 2006/01/02
  #

  def test_FromDate(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    for date in [DateTime(2006, 01, day) for day in range(1, 4)]:
      self._makeMovement(quantity=100,
                         start_date=date,
                         stop_date=date+1)
    # from_date takes all movements >= 
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2006, 01, 03),
                        section_uid=self.section.getUid())), 2)
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2006, 01, 02),
                        section_uid=self.mirror_section.getUid())), 2)

  def test_AtDate(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    for date in [DateTime(2006, 01, day) for day in range(1, 4)]:
      self._makeMovement(quantity=100,
                         start_date=date,
                         stop_date=date+1)
    # at_date takes all movements <=
    self.assertEquals(len(getMovementHistoryList(
                        at_date=DateTime(2006, 01, 03),
                        section_uid=self.section.getUid())), 2)
    self.assertEquals(len(getMovementHistoryList(
                        at_date=DateTime(2006, 01, 02),
                        section_uid=self.mirror_section.getUid())), 2)

  def test_ToDate(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    for date in [DateTime(2006, 01, day) for day in range(1, 4)]:
      self._makeMovement(quantity=100,
                         start_date=date,
                         stop_date=date+1)
    # to_date takes all movements <
    self.assertEquals(len(getMovementHistoryList(
                        to_date=DateTime(2006, 01, 03),
                        section_uid=self.section.getUid())), 1)
    self.assertEquals(len(getMovementHistoryList(
                        to_date=DateTime(2006, 01, 02),
                        section_uid=self.mirror_section.getUid())), 1)

  def test_FromDateAtDate(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    for date in [DateTime(2006, 01, day) for day in range(1, 4)]:
      self._makeMovement(quantity=100,
                         start_date=date,
                         stop_date=date+1)
    # both from_date and at_date
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2006, 01, 03),
                        at_date=DateTime(2006, 01, 03),
                        section_uid=self.section.getUid())), 1)
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2006, 01, 02),
                        at_date=DateTime(2006, 01, 03),
                        section_uid=self.section.getUid())), 2)
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2005, 01, 02),
                        at_date=DateTime(2006, 01, 03),
                        section_uid=self.section.getUid())), 2)
    # from other side
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2006, 01, 02),
                        at_date=DateTime(2006, 01, 03),
                        section_uid=self.mirror_section.getUid())), 2)

  def test_FromDateToDate(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    for date in [DateTime(2006, 01, day) for day in range(1, 4)]:
      self._makeMovement(quantity=100,
                         start_date=date,
                         stop_date=date+1)
    # both from_date and to_date
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2006, 01, 03),
                        to_date=DateTime(2006, 01, 03),
                        section_uid=self.section.getUid())), 0)
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2006, 01, 02),
                        to_date=DateTime(2006, 01, 03),
                        section_uid=self.section.getUid())), 1)
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2005, 01, 02),
                        to_date=DateTime(2007, 01, 02),
                        section_uid=self.section.getUid())), 3)
    # from other side
    self.assertEquals(len(getMovementHistoryList(
                        from_date=DateTime(2006, 01, 02),
                        to_date=DateTime(2006, 01, 03),
                        section_uid=self.mirror_section.getUid())), 1)

  def test_SortOnDate(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    date_list = [DateTime(2006, 01, day) for day in range(1, 10)]
    reverse_date_list = date_list[:]
    reverse_date_list.reverse()

    # we create movements with a random order on dates, to have an extra change
    # that they are not sorted accidentally.
    random_date_list = date_list[:]
    random.shuffle(random_date_list)
    for date in random_date_list:
      self._makeMovement(quantity=100,
                         start_date=date - 1,
                         stop_date=date)
    
    movement_date_list = [ x.date for x in getMovementHistoryList(
                              section_uid=self.section.getUid(),
                              sort_on=(('stock.date', 'ascending'),)) ]
    self.assertEquals(movement_date_list, date_list)
    movement_date_list = [ x.date for x in getMovementHistoryList(
                              section_uid=self.section.getUid(),
                              sort_on=(('stock.date', 'descending'),)) ]
    self.assertEquals(movement_date_list, reverse_date_list)
    # minimum test for (('stock.date', 'ASC'), ('stock.uid', 'ASC')) which is
    # what you want to make sure that the last line on a page precedes the
    # first line on the previous page.
    movement_date_list = [x.date for x in getMovementHistoryList(
                              section_uid=self.section.getUid(),
                              sort_on=(('stock.date', 'ascending'),
                                       ('stock.uid', 'ascending'),)) ]
    self.assertEquals(movement_date_list, date_list)

  # FIXME: do we want to include it or no ?
  def test_Limit(self):
    return "is it part of this API ?" # XXX
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    for q in range(10):
      self._makeMovement(quantity=1)
    self.assertEquals(3, len(getMovementHistoryList(list_start=2,
                                                    list_lines=3)))
  
  def test_SimulationState(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=2, simulation_state="confirmed")
    self._makeMovement(quantity=3, simulation_state="planned")
    for simulation_state in ['confirmed', ['confirmed', 'stopped']]:
      movement_history_list = getMovementHistoryList(
                                simulation_state=simulation_state,
                                section_uid=self.section.getUid())
      self.assertEquals(len(movement_history_list), 1)
      self.assertEquals(movement_history_list[0].total_quantity, 2)
    
    movement_history_list = getMovementHistoryList(
                              simulation_state=["confirmed", "planned"],
                              section_uid=self.section.getUid())
    self.assertEquals(len(movement_history_list), 2)

  def test_SimulationMovement(self, quiet=0, run=RUN_ALL_TESTS):
    """Test simulation movement are listed in getMovementHistoryList
    """
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeSimulationMovement(quantity=100)
    self._makeMovement(quantity=100)
    movement_history_list = getMovementHistoryList(
                                    section_uid=self.section.getUid())
    self.assertEquals(2, len(movement_history_list))
  
  def test_OmitSimulation(self, quiet=0, run=RUN_ALL_TESTS):
    """Test omit_simulation argument to getMovementHistoryList.
    """
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeSimulationMovement(quantity=100)
    self._makeMovement(quantity=100)
    movement_history_list = getMovementHistoryList(
                                    section_uid=self.section.getUid(),
                                    omit_simulation=1)
    self.assertEquals(1, len(movement_history_list))
    self.assertEquals(100, movement_history_list[0].quantity)
    
class TestInventoryStat(InventoryAPITestCase):
  """Tests Inventory Stat methods.
  """
  RUN_ALL_TESTS = 1

if __name__ == '__main__':
  framework()
else:
  import unittest
  def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInventory))
    suite.addTest(unittest.makeSuite(TestInventoryList))
    suite.addTest(unittest.makeSuite(TestMovementHistoryList))
    suite.addTest(unittest.makeSuite(TestInventoryStat))
    return suite

# vim: foldmethod=marker
