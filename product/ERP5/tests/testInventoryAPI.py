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

TODO: test variation
      test selection_domain, selection_report
"""

import os
import random
import unittest

import transaction
from AccessControl.SecurityManagement import newSecurityManager
from DateTime import DateTime
from Testing import ZopeTestCase

from Products.ERP5.Document.OrderRule import OrderRule
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from Products.ERP5Type.tests.utils import reindex
from Products.DCWorkflow.DCWorkflow import ValidationFailed
from Products.ERP5Type.Base import _aq_reset

class InventoryAPITestCase(ERP5TypeTestCase):
  """Base class for Inventory API Tests {{{
  """

  GROUP_CATEGORIES = ( 'group/test_group/A1/B1/C1',
                       'group/test_group/A1/B1/C2',
                       'group/test_group/A1/B2/C1',
                       'group/test_group/A1/B2/C2',
                       'group/test_group/A2/B1/C1',
                       'group/test_group/A2/B1/C2',
                       'group/test_group/A2/B2/C1',
                       'group/test_group/A2/B2/C2', )

  VARIATION_CATEGORIES = ( 'colour/red',
                           'colour/green',
                           'colour/blue',
                           'size/big',
                           'size/small',
                           'industrial_phase/phase1',
                           'industrial_phase/phase2', )

  def getTitle(self):
    """Title of the test."""
    return 'Inventory API'

  def getPortalName(self):
    """ID of the portal. """
    forced_portal_id = os.environ.get('erp5_tests_portal_id')
    if forced_portal_id:
      return str(forced_portal_id)
    # all test methods here cleanup correctly, so we can use the same portal
    # for all those tests.
    return 'inventory_api_test'

  def getItemModule(self):
    """ the apparel fabric module """
    return getattr(self.getPortal(),'apparel_fabric_item_module')

  def getProductModule(self):
    return getattr(self.getPortal(), 'product',
        getattr(self.getPortal(), 'product_module'))

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
    self.other_section = self._makeOrganisation(title='Other Section')
    self.node = self._makeOrganisation(title='Node')
    self.other_node = self._makeOrganisation(title='Other Node')
    self.payment_node = self.section.newContent(
                                  title='Payment Node',
                                  portal_type='Bank Account')
    self.other_payment_node = self.section.newContent(
                                  title='Other Payment Node',
                                  portal_type='Bank Account')
    self.mirror_section = self._makeOrganisation(title='Mirror Section')
    self.mirror_node = self._makeOrganisation(title='Mirror Node')
    self.project = self._makeProject(title='Project')
    self.other_project = self._makeProject(title='Other Project')
    self.resource = self.getProductModule().newContent(
                                  title='Resource',
                                  portal_type='Product')
    self.other_resource = self.getProductModule().newContent(
                                  title='Other Resource',
                                  portal_type='Product')
    self.item = self.getItemModule().newContent(title='Item')
    self.other_item = self.getItemModule().newContent(title='Other Item')
    # create a dummy Rule, to be able to create simulation movements
    rule_tool = self.portal.portal_rules
    if not hasattr(rule_tool, 'default_order_rule'):
      rule_tool._setObject('default_order_rule',
                           OrderRule('default_order_rule'))

  def _safeTic(self):
    """Like tic, but swallowing errors, usefull for teardown"""
    try:
      transaction.commit()
      self.tic()
    except RuntimeError:
      pass

  def beforeTearDown(self):
    """Clear everything for next test."""
    self._safeTic()
    for module in [ 'organisation_module',
                    'person_module',
                    'product_module',
                    'portal_simulation',
                    'inventory_module',
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
    transaction.commit()

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
              'function/function1',
              'function/function1/function2',
           # we create a huge group category for consolidation tests
           ) + self.GROUP_CATEGORIES + self.VARIATION_CATEGORIES
  
  def getBusinessTemplateList(self):
    """ erp5_trade is required for transit_simulation_state
        erp5_apparel is required for item
    """
    return ('erp5_base', 'erp5_pdm', 'erp5_dummy_movement', 'erp5_trade',
            'erp5_apparel', 'erp5_project')

  # TODO: move this to a base class {{{
  @reindex
  def _makeOrganisation(self, **kw):
    """Creates an organisation."""
    org = self.getPortal().organisation_module.newContent(
          portal_type='Organisation',
          **kw)
    return org

  @reindex
  def _makeProject(self, **kw):
    """Creates an project."""
    prj = self.getPortal().project_module.newContent(
          portal_type='Project',
          **kw)
    return prj

  @reindex
  def _makeSalePackingList(self, **kw):
    """Creates a sale packing list."""
    spl = self.getPortal().sale_packing_list_module.newContent(
          portal_type='Sale Packing List',)
    spl.edit(**kw)
    return spl
  
  @reindex
  def _makeSaleInvoice(self, created_by_builder=0, **kw):
    """Creates a sale invoice."""
    sit = self.getPortal().accounting_module.newContent(
          portal_type='Sale Invoice Transaction',
          created_by_builder=created_by_builder)
    sit.edit(**kw)
    return sit

  @reindex
  def _makeProduct(self, **kw):
    """Creates a product."""
    product = self.getProductModule().newContent(
            portal_type = 'Product', **kw)
    transaction.commit()
    self.tic()
    return product
  _makeResource = _makeProduct
  # }}}

  @reindex
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
    return mvt
  
  @reindex
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
    return mvt

# }}}

class TestInventory(InventoryAPITestCase):
  """Tests getInventory methods.
  """
  def testReturnedTypeIsFloat(self):
    """getInventory returns a float"""
    getInventory = self.getSimulationTool().getInventory
    self.assertEquals(type(getInventory()), type(0.1))
    # default is 0
    self.assertEquals(0, getInventory())

  def test_SimulationMovement(self):
    """Test Simulation Movements works in this testing environnement.
    """
    getInventory = self.getSimulationTool().getInventory
    self._makeSimulationMovement(quantity=100)
    self.assertEquals(100, getInventory(section_uid=self.section.getUid()))
    # mixed with a real movement
    self._makeMovement(quantity=100)
    self.assertEquals(200, getInventory(section_uid=self.section.getUid()))

  def test_SimulationMovementisAccountable(self):
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
    transaction.commit(); self.tic() # (after reindexing of course)
    self.assertEquals(100, getInventory(section_uid=self.section.getUid()))
  
  def test_OmitSimulation(self):
    """Test omit_simulation argument to getInventory.
    """
    getInventory = self.getSimulationTool().getInventory
    self._makeSimulationMovement(quantity=100)
    self._makeMovement(quantity=100)
    self.assertEquals(100, getInventory(section_uid=self.section.getUid(),
                                        omit_simulation=1))

  def test_SectionCategory(self):
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
    transaction.commit()
    self.tic()
    self.assertEquals(getInventory(
                section_category_strict_membership=['group/level1']), 100)
    
    # non existing values to section_category are not silently ignored, but
    # raises an exception
    self.assertRaises(ValueError,
                      getInventory,
                      section_category='group/notexists')

  def test_MirrorSectionCategory(self):
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
    transaction.commit()
    self.tic()
    self.assertEquals(getInventory(
            mirror_section_category_strict_membership=['group/level1']), 100)
    
    # non existing values to section_category are not silently ignored, but
    # raises an exception
    self.assertRaises(ValueError,
                      getInventory,
                      mirror_section_category='group/notexists')

  def test_NodeCategory(self):
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
    transaction.commit()
    self.tic()
    self.assertEquals(getInventory(
                node_category_strict_membership=['group/level1']), 100)
  
  def test_Function(self):
    """Tests inventory on function"""
    getInventory = self.getSimulationTool().getInventory
    self._makeMovement(quantity=100,
                       destination_function='function/function1')
    self.assertEquals(getInventory(
                        function='function/function1'), 100)
    self.assertEquals(getInventory(
                        function='function/function1/function2'), 0)

  def test_FunctionUid(self):
    """Tests inventory on function uid"""
    getInventory = self.getSimulationTool().getInventory
    function = self.portal.portal_categories.function
    self._makeMovement(quantity=100,
                       destination_function='function/function1')
    self.assertEquals(getInventory(
                        function_uid=function.function1.getUid()), 100)
    self.assertEquals(getInventory(
                        function_uid=function.function1.function2.getUid()), 0)

  def test_FunctionCategory(self):
    """Tests inventory on function category"""
    getInventory = self.getSimulationTool().getInventory
    function = self.portal.portal_categories.function
    self._makeMovement(quantity=100,
                       destination_function='function/function1/function2')
    self.assertEquals(getInventory(
                        function_category='function/function1'), 100)
    self.assertEquals(getInventory(
                        function='function/function1/function2'), 100)

  def test_FunctionCategoryStrictMembership(self):
    """Tests inventory on function category strict membership"""
    getInventory = self.getSimulationTool().getInventory
    function = self.portal.portal_categories.function
    self._makeMovement(quantity=100,
                       destination_function='function/function1/function2')
    self.assertEquals(getInventory(
            function_category_strict_membership='function/function1'), 0)
    self.assertEquals(getInventory(
            function_category_strict_membership='function/function1/function2'), 100)
  
  def test_Project(self):
    """Tests inventory on project"""
    getInventory = self.getSimulationTool().getInventory
    self._makeMovement(quantity=100,
                       destination_project_value=self.project)
    self._makeMovement(quantity=100,
                       source_project_value=self.other_project)
    self.assertEquals(getInventory(
                        project=self.project.getRelativeUrl()), 100)
    self.assertEquals(getInventory(
                        project=self.other_project.getRelativeUrl()), -100)

  def test_ProjectUid(self):
    """Tests inventory on project uid"""
    getInventory = self.getSimulationTool().getInventory
    self._makeMovement(quantity=100,
                       destination_project_value=self.project)
    self._makeMovement(quantity=100,
                       source_project_value=self.other_project)
    self.assertEquals(getInventory(
                        project_uid=self.project.getUid()), 100)
    self.assertEquals(getInventory(
                        project_uid=self.other_project.getUid()), -100)

  def test_ProjectCategory(self):
    """Tests inventory on project category"""
    # this test uses unrealistic data
    getInventory = self.getSimulationTool().getInventory
    self.project.setGroup('level1/level2')
    self._makeMovement(quantity=100,
                       destination_project_value=self.project)
    self.assertEquals(getInventory(
                        project_category='group/level1'), 100)
    self.assertEquals(getInventory(
                        project_category='group/level1/level2'), 100)

  def test_ProjectCategoryStrictMembership(self):
    """Tests inventory on project category strict membership"""
    # this test uses unrealistic data
    getInventory = self.getSimulationTool().getInventory
    self.project.setGroup('level1/level2')
    self._makeMovement(quantity=100,
                       destination_project_value=self.project)
    self.assertEquals(getInventory(
                project_category_strict_membership='group/level1'), 0)
    self.assertEquals(getInventory(
                project_category_strict_membership='group/level1/level2'), 100)


  def test_ResourceCategory(self):
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
    transaction.commit()
    self.tic()
    self.assertEquals(getInventory(
            resource_category_strict_membership=['product_line/level1']), 100)

  def test_PaymentCategory(self):
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
    transaction.commit()
    self.tic()
    self.assertEquals(getInventory(
              payment_category_strict_membership=['product_line/level1']), 100)

  def test_OwnershipInventoryByNode(self):
    """Tests ownership inventory by node. """
    getInventory = self.getSimulationTool().getInventory
    self.assertEquals(getInventory(
                        node_uid=self.node.getUid()), 0)
    self.assertEquals(getInventory(
                        node_uid=self.other_node.getUid()), 0)
    # transfer quantity=100 from node to other_node.
    self._makeMovement(quantity=100,
                       source_value=self.node,
                       destination_value=self.other_node)
    transaction.commit()
    self.tic()
    self.assertEquals(getInventory(
                        node_uid=self.node.getUid()), -100)
    self.assertEquals(getInventory(
                        node_uid=self.other_node.getUid()), 100)
    self.assertEquals(getInventory(
                        mirror_node_uid=self.node.getUid()), 100)
    self.assertEquals(getInventory(
                        mirror_node_uid=self.other_node.getUid()), -100)

  def test_OwnershipInventoryBySection(self):
    """Tests ownership inventory by section. """
    getInventory = self.getSimulationTool().getInventory
    self.assertEquals(getInventory(
                        section_uid=self.section.getUid()), 0)
    self.assertEquals(getInventory(
                        section_uid=self.other_section.getUid()), 0)
    # transfer quantity=100 from section to other_section.
    self._makeMovement(quantity=100,
                       source_section_value=self.section,
                       destination_section_value=self.other_section)
    transaction.commit()
    self.tic()
    self.assertEquals(getInventory(
                        section_uid=self.section.getUid()), -100)
    self.assertEquals(getInventory(
                        section_uid=self.other_section.getUid()), 100)
    self.assertEquals(getInventory(
                        mirror_section_uid=self.section.getUid()), 100)
    self.assertEquals(getInventory(
                        mirror_section_uid=self.other_section.getUid()), -100)

  def test_SimulationState(self):
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

  def test_MultipleNodes(self):
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
  def TODO_test_DoubleSectionCategory(self):
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

  def test_NoSection(self):
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
  
  def testPrecision(self):
    # getInventory supports a precision= argument to specify the precision to
    # round
    getInventory = self.getSimulationTool().getInventory
    getInventoryAssetPrice = self.getSimulationTool().getInventoryAssetPrice
    self._makeMovement( quantity=0.1234, price=1 )
    self.assertAlmostEquals(0.123,
                getInventory(precision=3, node_uid=self.node.getUid()),
                places=3)
    self.assertAlmostEquals(0.123,
             getInventoryAssetPrice(precision=3, node_uid=self.node.getUid()),
             places=3)
  
  def testPrecisionAndFloatRoundingIssues(self):
    # sum([0.1] * 10) != 1.0 but this is not a problem here
    getInventory = self.getSimulationTool().getInventory
    getInventoryAssetPrice = self.getSimulationTool().getInventoryAssetPrice
    self._makeMovement( quantity=1, price=1 )
    for i in range(10):
      self._makeMovement( quantity=-0.1, price=1 )
    self.assertEquals(0, getInventory(precision=2, node_uid=self.node.getUid()))
    self.assertEquals(0, getInventoryAssetPrice(precision=2,
                                                node_uid=self.node.getUid()))
    
  def test_OmitInputOmitOutput(self):
    getInventory = self.getSimulationTool().getInventory
    self._makeMovement(quantity=1, price=1)
    self._makeMovement(quantity=-1, price=1)
    # omit input ignores movement comming to this node
    self.assertEquals(-1, getInventory(node_uid=self.node.getUid(),
                                       omit_input=1))
    # omit output ignores movement going to this node
    self.assertEquals(1, getInventory(node_uid=self.node.getUid(),
                                      omit_output=1))
    # omit_output & omit_input return nothing in that case
    self.assertEquals(0, getInventory(node_uid=self.node.getUid(),
                                      omit_input=1,
                                      omit_output=1))
    # this also work with movements without source or without destination
    self._makeMovement(quantity=-2, price=1, source_value=None)
    self.assertEquals(-3, getInventory(node_uid=self.node.getUid(),
                                       omit_input=1))
    self.assertEquals(1, getInventory(node_uid=self.node.getUid(),
                                      omit_output=1))
    # and with movements without source section / desination sections
    self._makeMovement(quantity=2, price=1, source_section_value=None)
    self.assertEquals(-3, getInventory(node_uid=self.node.getUid(),
                                       omit_input=1))
    self.assertEquals(3, getInventory(node_uid=self.node.getUid(),
                                      omit_output=1))
    
  def test_OmitInputOmitOutputWithDifferentSections(self):
    getInventory = self.getSimulationTool().getInventory
    self._makeMovement(quantity=2, price=1)
    self._makeMovement(quantity=-3, price=1,
                       destination_section_value=self.other_section )
    self.assertEquals(0, getInventory(node_uid=self.node.getUid(),
                                      section_uid=self.section.getUid(),
                                      omit_input=1))
    self.assertEquals(-3, getInventory(node_uid=self.node.getUid(),
                                      section_uid=self.other_section.getUid(),
                                      omit_input=1))
    self.assertEquals(2, getInventory(node_uid=self.node.getUid(),
                                      section_uid=self.section.getUid(),
                                      omit_output=1))
    self.assertEquals(0, getInventory(node_uid=self.node.getUid(),
                                      section_uid=self.other_section.getUid(),
                                      omit_output=1))
    
  def test_OmitInputOmitOutputWithDifferentPayment(self):
    getInventory = self.getSimulationTool().getInventory
    # simple case
    self._makeMovement(quantity=2, price=1,
                       destination_payment_value=self.payment_node )
    self._makeMovement(quantity=-3, price=1,
                       destination_payment_value=self.other_payment_node )
    self.assertEquals(0, getInventory(node_uid=self.node.getUid(),
                                      section_uid=self.section.getUid(),
                                      payment_uid=self.payment_node.getUid(),
                                      omit_input=1))
    self.assertEquals(-3, getInventory(node_uid=self.node.getUid(),
                                  section_uid=self.section.getUid(),
                                  payment_uid=self.other_payment_node.getUid(),
                                  omit_input=1))
    self.assertEquals(2, getInventory(node_uid=self.node.getUid(),
                                  section_uid=self.section.getUid(),
                                  payment_uid=self.payment_node.getUid(),
                                  omit_output=1))
    self.assertEquals(0, getInventory(node_uid=self.node.getUid(),
                                  section_uid=self.other_section.getUid(),
                                  payment_uid=self.other_payment_node.getUid(),
                                  omit_output=1))

  def test_OmitInputOmitOutputCancellationAmount(self):
    getInventory = self.getSimulationTool().getInventory
    self._makeMovement(quantity=-1, price=1, cancellation_amount=True)
    self._makeMovement(quantity=2, price=1, cancellation_amount=True)
    self.assertEquals(2, getInventory(node_uid=self.node.getUid(),
                                       omit_input=1))
    self.assertEquals(-1, getInventory(node_uid=self.node.getUid(),
                                      omit_output=1))
    # omit_output & omit_input return nothing in that case
    self.assertEquals(0, getInventory(node_uid=self.node.getUid(),
                                      omit_input=1,
                                      omit_output=1))
    
  def test_OmitInputOmitOutputWithDifferentPaymentSameNodeSameSection(self):
    getInventory = self.getSimulationTool().getInventory
    self._makeMovement(quantity=2, price=1,
                       source_value=self.node,
                       destination_value=self.node,
                       source_section_value=self.section,
                       destination_section_value=self.section,
                       source_payment_value=self.other_payment_node,
                       destination_payment_value=self.payment_node )
    self.assertEquals(2, getInventory(node_uid=self.node.getUid(),
                                       section_uid=self.section.getUid(),
                                       payment_uid=self.payment_node.getUid(),
                                       omit_output=1))
    self.assertEquals(-2, getInventory(node_uid=self.node.getUid(),
                           section_uid=self.section.getUid(),
                           payment_uid=self.other_payment_node.getUid(),
                           omit_input=1))

  def test_TimeZone(self):
    """
    Check that getInventory support DateTime parameter with 
    timezone
    """
    getInventory = self.getSimulationTool().getInventory
    date_gmt_1 = DateTime('2005/12/01 GMT+9')
    date_gmt0 = DateTime('2005/12/01 GMT+10')
    date_gmt1 = DateTime('2005/12/01 GMT+11')
    self._makeMovement(quantity=1, start_date=date_gmt0)
    self.assertEquals(0, getInventory(
                           node_uid=self.node.getUid(),
                           resource=self.resource.getRelativeUrl(),
                           at_date=date_gmt1))
    self.assertEquals(1, getInventory(
                           node_uid=self.node.getUid(),
                           resource=self.resource.getRelativeUrl(),
                           at_date=date_gmt_1))

class TestInventoryList(InventoryAPITestCase):
  """Tests getInventoryList methods.
  """
  def test_ReturnedTypeIsList(self):
    """Inventory List returns a sequence object""" 
    getInventoryList = self.getSimulationTool().getInventoryList
    inventory_list = getInventoryList()
    self.assertEquals(str(inventory_list.__class__),
                    'Shared.DC.ZRDB.Results.Results')
    # the brain is InventoryListBrain
    self.assert_('InventoryListBrain' in
          [c.__name__ for c in inventory_list._class.__bases__])
    # default is an empty list
    self.assertEquals(0, len(inventory_list))

  def test_GroupByNode(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=100)
    self._makeMovement(destination_value=self.other_node, quantity=100)
    self._makeMovement(destination_value=None, quantity=100)
    inventory_list = getInventoryList(group_by_node=1)
    self.assertEquals(3, len(inventory_list))
    self.assertEquals([r for r in inventory_list if r.node_relative_url ==
                  self.node.getRelativeUrl()][0].inventory, 100)
    self.assertEquals([r for r in inventory_list if r.node_relative_url ==
                  self.other_node.getRelativeUrl()][0].inventory, 100)
    self.assertEquals([r for r in inventory_list if r.node_relative_url ==
                  self.mirror_node.getRelativeUrl()][0].inventory, -300)

  def test_GroupByMirrorNode(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=100)
    self._makeMovement(source_value=self.other_node, quantity=100)
    self._makeMovement(source_value=None, quantity=100)
    inventory_list = getInventoryList(section_uid=self.section.getUid(),
                                      group_by_mirror_node=1)
    self.assertEquals(3, len(inventory_list))
    self.assertEquals([r for r in inventory_list if r.mirror_node_uid ==
                  self.mirror_node.getUid()][0].inventory, 100)
    self.assertEquals([r for r in inventory_list if r.mirror_node_uid ==
                  self.other_node.getUid()][0].inventory, 100)
    self.assertEquals([r for r in inventory_list
                       if r.mirror_node_uid is None][0].inventory, 100)

  def test_GroupBySection(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=100)
    self._makeMovement(destination_section_value=self.other_node, quantity=100)
    self._makeMovement(destination_section_value=None, quantity=100)
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      group_by_section=1)
    self.assertEquals(3, len(inventory_list))
    self.assertEquals([r for r in inventory_list if r.section_relative_url ==
                  self.section.getRelativeUrl()][0].inventory, 100)
    self.assertEquals([r for r in inventory_list if r.section_relative_url ==
                  self.other_node.getRelativeUrl()][0].inventory, 100)
    self.assertEquals([r for r in inventory_list if r.section_relative_url is
                  None][0].inventory, 100)

  def test_GroupBySectionCategory(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self.section.setGroup('level1')
    self.other_section.setGroup('level1')
    m1 = self._makeMovement(quantity=2)
    m2 = self._makeMovement(destination_section_value=self.other_section, quantity=3)

    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      section_category='group/level1',
                                      group_by_section_category=1)
    self.assertEquals(1, len(inventory_list))
    self.assertEquals(3+2, inventory_list[0].inventory)

  def test_GroupByFunction(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    function1 = self.portal.portal_categories.restrictedTraverse(
                                      'function/function1')
    function2 = self.portal.portal_categories.restrictedTraverse(
                                      'function/function1/function2')
    self._makeMovement(quantity=2,
                       destination_function_value=function1,)
    self._makeMovement(quantity=3,
                       destination_function_value=function2,)

    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      group_by_function=1)
    self.assertEquals(2, len(inventory_list))
    self.assertEquals([r for r in inventory_list if r.function_uid ==
      function1.getUid()][0].inventory, 2)
    self.assertEquals([r for r in inventory_list if r.function_uid ==
      function2.getUid()][0].inventory, 3)

  def test_GroupByProject(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=2,
                       destination_project_value=self.project,)
    self._makeMovement(quantity=3,
                       destination_project_value=self.other_project,)

    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      group_by_project=1)
    self.assertEquals(2, len(inventory_list))
    self.assertEquals([r for r in inventory_list if r.project_uid ==
      self.project.getUid()][0].inventory, 2)
    self.assertEquals([r for r in inventory_list if r.project_uid ==
      self.other_project.getUid()][0].inventory, 3)

  def test_GroupByResource(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=100)
    self._makeMovement(resource_value=self.other_resource, quantity=100)
    # group_by_resource is implicit when grouping by something ...
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      group_by_node=1)
    self.assertEquals(2, len(inventory_list))
    self.assertEquals([r for r in inventory_list if r.resource_relative_url ==
                  self.resource.getRelativeUrl()][0].inventory, 100)
    self.assertEquals([r for r in inventory_list if r.resource_relative_url ==
                  self.other_resource.getRelativeUrl()][0].inventory, 100)
    # ... but can be disabled
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      group_by_node=1,
                                      group_by_resource=0)
    self.assertEquals(1, len(inventory_list))
    self.assertEquals(inventory_list[0].inventory, 200)

  def test_GroupByPayment(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=100)
    self._makeMovement(destination_payment_value=self.payment_node,
                       quantity=200)
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      group_by_node=1, group_by_payment=1)
    self.assertEquals(2, len(inventory_list))
    self.assertEquals([r for r in inventory_list if r.payment_uid is
                      None][0].inventory, 100)
    self.assertEquals([r for r in inventory_list if r.payment_uid ==
                       self.payment_node.getUid()][0].inventory, 200)

  def test_GroupByDate(self):
    # group by date currently only groups by *exact* date
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=1, start_date=DateTime('2000/1/1 12:00 UTC'))
    self._makeMovement(quantity=1, start_date=DateTime('2000/1/1 12:00 UTC'))
    self._makeMovement(quantity=1, start_date=DateTime('2001/1/1 12:00 UTC'))
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      group_by_date=1)
    self.assertEquals(2, len(inventory_list))
    self.assertEquals([r for r in inventory_list
                        if r.date.year() == 2000][0].inventory, 2)
    self.assertEquals([r for r in inventory_list
                        if r.date.year() == 2001][0].inventory, 1)


  def test_OmitInputOmitOutput(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=1, price=1)
    self._makeMovement(quantity=-1, price=1)
    # omit input ignores movement comming to this node
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      omit_input=1)
    self.assertEquals(1, len(inventory_list))
    self.assertEquals(-1, inventory_list[0].total_price)
    self.assertEquals(-1, inventory_list[0].total_quantity)

    # omit output ignores movement going to this node
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      omit_output=1)
    self.assertEquals(1, len(inventory_list))
    self.assertEquals(1, inventory_list[0].total_price)
    self.assertEquals(1, inventory_list[0].total_quantity)

    # omit_output & omit_input return nothing in that case
    self.assertEquals(0, len(getInventoryList(node_uid=self.node.getUid(),
                                              omit_input=1,
                                              omit_output=1)))
    
  def test_OmitInputOmitOutputWithDifferentPaymentSameNodeSameSection(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=2, price=1,
                       source_value=self.node,
                       destination_value=self.node,
                       source_section_value=self.section,
                       destination_section_value=self.section,
                       source_payment_value=self.other_payment_node,
                       destination_payment_value=self.payment_node )
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      section_uid=self.section.getUid(),
                                      payment_uid=self.payment_node.getUid(),
                                      omit_output=1)
    self.assertEquals(1, len(inventory_list))
    self.assertEquals(2, inventory_list[0].total_price)
    self.assertEquals(2, inventory_list[0].total_quantity)

    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                section_uid=self.section.getUid(),
                                payment_uid=self.other_payment_node.getUid(),
                                omit_input=1)
    self.assertEquals(1, len(inventory_list))
    self.assertEquals(-2, inventory_list[0].total_price)
    self.assertEquals(-2, inventory_list[0].total_quantity)

  def test_OmitInputOmitOutputCancellationAmount(self):
    getInventoryList = self.getSimulationTool().getInventoryList
    self._makeMovement(quantity=-1, price=1, cancellation_amount=True)
    self._makeMovement(quantity=2, price=1, cancellation_amount=True)

    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      omit_input=1)
    self.assertEquals(1, len(inventory_list))
    self.assertEquals(2, inventory_list[0].total_price)
    self.assertEquals(2, inventory_list[0].total_quantity)

    # omit output ignores movement going to this node
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      omit_output=1)
    self.assertEquals(1, len(inventory_list))
    self.assertEquals(-1, inventory_list[0].total_price)
    self.assertEquals(-1, inventory_list[0].total_quantity)

  def test_CurentAvailableFutureInventoryList(self):
    def makeMovement(simulation_state=None, quantity=None):
      self._makeMovement(quantity=quantity, price=1,
                         source_value=self.node,
                         destination_value=self.other_node,
                         #source_section_value=self.section,
                         #destination_section_value=self.other_section,
                         #source_payment_value=self.payment_node,
                         #destination_payment_value=self.other_payment_node,
                         simulation_state=simulation_state)
    def checkInventory(line=0, type='Current', destination=0, source=0, quantity=None):
      method = getattr(self.getSimulationTool(),'get%sInventoryList' % type)
      if source:
        node_uid = self.node.getUid()
      if destination:
        node_uid = self.other_node.getUid()
      inventory_list = method(node_uid=node_uid)
      self.assertEquals(len(inventory_list), line)
      if quantity is not None:
        self.assertEquals(sum([x.total_quantity for x in inventory_list]), 
                          quantity)
    makeMovement(quantity=1, simulation_state='ordered')
    checkInventory(line=0, type='Current', destination=1)
    checkInventory(line=0, type='Available', destination=1)
    checkInventory(line=1, type='Future', source=1, quantity=-1)
    checkInventory(line=1, type='Future', destination=1, quantity=1)
    makeMovement(quantity=3, simulation_state='confirmed')
    checkInventory(line=0, type='Current', source=1)
    checkInventory(line=0, type='Current', destination=1)
    checkInventory(line=1, type='Available', source=1, quantity=-3)
    checkInventory(line=0, type='Available', destination=1)
    checkInventory(line=2, type='Future', source=1, quantity=-4)
    checkInventory(line=2, type='Future', destination=1, quantity=4)
    makeMovement(quantity=5, simulation_state='started')
    checkInventory(line=1, type='Current', source=1, quantity=-5)
    checkInventory(line=0, type='Current', destination=1)
    checkInventory(line=2, type='Available', source=1, quantity=-8)
    checkInventory(line=0, type='Available', destination=1)
    checkInventory(line=3, type='Future', source=1, quantity=-9)
    checkInventory(line=3, type='Future', destination=1, quantity=9)


class TestMovementHistoryList(InventoryAPITestCase):
  """Tests Movement history list methods.
  """
  def testReturnedTypeIsList(self):
    """Movement History List returns a sequence object""" 
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt_history_list = getMovementHistoryList()
    self.assertEquals(str(mvt_history_list.__class__),
                    'Shared.DC.ZRDB.Results.Results')
    # default is an empty list
    self.assertEquals(0, len(mvt_history_list))
  
  def testMovementBothSides(self):
    """Movement History List returns movement from both sides""" 
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
    self.assertEquals('MovementHistoryListBrain', brain_class,
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
  

  def test_BrainDateTimeZone(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=100,
                       start_date=DateTime('2001/02/03 04:05 GMT+3'))
    movement_history_list = getMovementHistoryList(
                                section_uid=self.section.getUid())
    self.assertEquals(len(movement_history_list), 1)
    brain = movement_history_list[0]
    self.assertEquals(DateTime('2001/02/03 04:05 GMT+3'), brain.date)
    self.assertEquals('GMT+3', brain.date.timezone())

  def test_BrainDateTimeZoneStopDate(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=100,
                       start_date=DateTime('2001/02/03 04:05 GMT+2'),
                       stop_date=DateTime('2001/02/03 04:05 GMT+3'))
    movement_history_list = getMovementHistoryList(
                        mirror_section_uid=self.section.getUid())
    self.assertEquals(len(movement_history_list), 1)
    brain = movement_history_list[0]
    self.assertEquals(DateTime('2001/02/03 04:05 GMT+2'), brain.date)
    self.assertEquals('GMT+2', brain.date.timezone())

  def test_BrainEmptyDate(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=100,)
    movement_history_list = getMovementHistoryList(
                                section_uid=self.section.getUid())
    self.assertEquals(len(movement_history_list), 1)
    brain = movement_history_list[0]
    self.assertEquals(None, brain.date)

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

  def test_SortOnCatalogColumn(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=1, title='First')
    self._makeMovement(quantity=2, title='Second')
    
    self.assertEquals(['First', 'Second'], [ x.getObject().getTitle() for x in
          getMovementHistoryList(section_uid=self.section.getUid(),
                                 sort_on=(('title', 'ascending'),)) ])
    self.assertEquals(['Second', 'First'], [ x.getObject().getTitle() for x in
          getMovementHistoryList(section_uid=self.section.getUid(),
                                 sort_on=(('title', 'descending'),)) ])

  def test_Limit(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    for q in range(6):
      self._makeMovement(quantity=1)
    self.assertEquals(3, len(getMovementHistoryList(limit=3)))
    self.assertEquals(4, len(getMovementHistoryList(limit=(1, 4))))
  
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

  def test_SimulationMovement(self):
    """Test simulation movement are listed in getMovementHistoryList
    """
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeSimulationMovement(quantity=100)
    self._makeMovement(quantity=100)
    movement_history_list = getMovementHistoryList(
                                    section_uid=self.section.getUid())
    self.assertEquals(2, len(movement_history_list))
  
  def test_OmitSimulation(self):
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
  
  def test_RunningTotalQuantity(self):
    """Test that a running_total_quantity attribute is set on brains
    """
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    date_and_qty_list = [(DateTime(2006, 01, day), day) for day in range(1, 10)]
    for date, quantity in date_and_qty_list:
      self._makeMovement(stop_date=date, quantity=quantity)
    movement_history_list = getMovementHistoryList(
                                    section_uid=self.section.getUid(),
                                    sort_on=[('stock.date', 'asc'),
                                             ('stock.uid', 'asc')])
    running_total_quantity=0
    for idx, (date, quantity) in enumerate(date_and_qty_list):
      brain = movement_history_list[idx]
      running_total_quantity += quantity
      self.assertEquals(running_total_quantity, brain.running_total_quantity)
      self.assertEquals(date, brain.date)
      self.assertEquals(quantity, brain.quantity)
  
  def test_RunningTotalPrice(self):
    """Test that a running_total_price attribute is set on brains
    """
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    date_and_price_list = [(DateTime(2006, 01, day), day) for day in range(1, 10)]
    for date, price in date_and_price_list:
      self._makeMovement(stop_date=date, quantity=1, price=price)
    movement_history_list = getMovementHistoryList(
                                    section_uid=self.section.getUid(),
                                    sort_on=[('stock.date', 'asc'),
                                             ('stock.uid', 'asc')])
    running_total_price=0
    for idx, (date, price) in enumerate(date_and_price_list):
      brain = movement_history_list[idx]
      running_total_price += price
      self.assertEquals(running_total_price, brain.running_total_price)
      self.assertEquals(date, brain.date)
      self.assertEquals(price, brain.total_price)

  def test_RunningTotalWithInitialValue(self):
    """Test running_total_price and running_total_quantity with an initial
    value.
    """
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    date_and_qty_list = [(DateTime(2006, 01, day), day) for day in range(1, 10)]
    for date, quantity in date_and_qty_list:
      self._makeMovement(stop_date=date, price=quantity, quantity=quantity)
    initial_running_total_price=100
    initial_running_total_quantity=-10
    movement_history_list = getMovementHistoryList(
                                    initial_running_total_quantity=
                                            initial_running_total_quantity,
                                    initial_running_total_price=
                                            initial_running_total_price,
                                    section_uid=self.section.getUid(),
                                    sort_on=[('stock.date', 'asc'),
                                             ('stock.uid', 'asc')])
    running_total_price=initial_running_total_price
    running_total_quantity=initial_running_total_quantity
    for idx, (date, quantity) in enumerate(date_and_qty_list):
      brain = movement_history_list[idx]
      self.assertEquals(date, brain.date)
      running_total_quantity += quantity
      self.assertEquals(running_total_quantity, brain.running_total_quantity)
      running_total_price += quantity * quantity # we've set price=quantity
      self.assertEquals(running_total_price, brain.running_total_price)
  
  def testRunningQuantityWithQuantity0(self):
    # a 0 quantity should not be a problem for running total price
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    date = DateTime()
    quantity = -1
    for i in range(3):
      self._makeMovement( quantity=quantity+i, price=1, start_date=date+i )
    mvt_history_list = getMovementHistoryList(
                            node_uid=self.node.getUid(),
                            sort_on=[['stock.date', 'ASC']])
    self.assertEquals(3, len(mvt_history_list))
    self.assertEquals(-1, mvt_history_list[0].running_total_quantity)
    self.assertEquals(-1, mvt_history_list[0].running_total_price)
    self.assertEquals(-1, mvt_history_list[1].running_total_quantity)
    self.assertEquals(-1, mvt_history_list[1].running_total_price)
    self.assertEquals(0, mvt_history_list[2].running_total_quantity)
    self.assertEquals(0, mvt_history_list[2].running_total_price)

  # bug #352
  def testSameNodeDifferentDates(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    date = DateTime()
    mvt = self._makeMovement( quantity=2,
                              start_date=date,
                              stop_date=date+1,
                              source_value=self.node,
                              destination_value=self.node )
    
    mvt_history_list = getMovementHistoryList(
                            node_uid=self.node.getUid(),)
    self.assertEquals(2, len(mvt_history_list))
    self.assertEquals(0, sum([r.total_quantity for r in mvt_history_list]))

  def testSameNodeSameDates(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt = self._makeMovement( quantity=2,
                              start_date=DateTime(),
                              source_value=self.node,
                              destination_value=self.node )
    mvt_history_list = getMovementHistoryList(
                            node_uid=self.node.getUid(),)
    self.assertEquals(2, len(mvt_history_list))
    self.assertEquals(0, sum([r.total_quantity for r in mvt_history_list]))
 
  def testSameNodeSameDatesSameSections(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    mvt = self._makeMovement( quantity=2,
                              start_date=DateTime(),
                              source_value=self.node,
                              destination_value=self.node,
                              source_section_value=self.section,
                              destination_section_value=self.section,)
    # For now, if you want to get movements from same node, same dates, same
    # sections, you have to pass ignore_group_by=True to ignore default
    # grouping.
    mvt_history_list = getMovementHistoryList(
                            ignore_group_by=True,
                            node_uid=self.node.getUid(),
                            section_uid=self.section.getUid())
    self.assertEquals(2, len(mvt_history_list))
    self.assertEquals(0, sum([r.total_quantity for r in mvt_history_list]))
 
  def testPrecision(self):
    # getMovementHistoryList supports a precision= argument to specify the
    # precision to round
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement( quantity=0.1234, price=1 )
    mvt_history_list = getMovementHistoryList(
                            precision=2,
                            node_uid=self.node.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(0.12, mvt_history_list[0].running_total_quantity)
    self.assertEquals(0.12, mvt_history_list[0].running_total_price)
    self.assertEquals(0.12, mvt_history_list[0].total_quantity)
    self.assertEquals(0.12, mvt_history_list[0].total_price)
    
    mvt_history_list = getMovementHistoryList(
                            precision=3,
                            node_uid=self.node.getUid())
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(0.123, mvt_history_list[0].running_total_quantity)
    self.assertEquals(0.123, mvt_history_list[0].running_total_price)
    self.assertEquals(0.123, mvt_history_list[0].total_quantity)
    self.assertEquals(0.123, mvt_history_list[0].total_price)

  def testPrecisionAndFloatRoundingIssues(self):
    # sum([0.1] * 10) != 1.0 but this is not a problem here
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    date = DateTime()
    self._makeMovement( quantity=1, price=1, start_date=date )
    for i in range(10):
      self._makeMovement( quantity=-0.1, price=1, start_date=date+i )
    mvt_history_list = getMovementHistoryList(
                            precision=2,
                            node_uid=self.node.getUid(),
                            sort_on=[['stock.date', 'ASC']])
    self.assertEquals(11, len(mvt_history_list))
    self.assertEquals(0, mvt_history_list[-1].running_total_quantity)
    self.assertEquals(0, mvt_history_list[-1].running_total_price)

  def test_OmitInputOmitOutput(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=1, price=1)
    self._makeMovement(quantity=-1, price=1)
    # omit input ignores movement comming to this node
    mvt_history_list = getMovementHistoryList(node_uid=self.node.getUid(),
                                              omit_input=1)
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(-1, mvt_history_list[0].total_price)
    self.assertEquals(-1, mvt_history_list[0].total_quantity)

    # omit output ignores movement going to this node
    mvt_history_list = getMovementHistoryList(node_uid=self.node.getUid(),
                                              omit_output=1)
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(1, mvt_history_list[0].total_price)
    self.assertEquals(1, mvt_history_list[0].total_quantity)

    self.assertEquals(0, len(getMovementHistoryList(
                                              node_uid=self.node.getUid(),
                                              omit_input=1,
                                              omit_output=1)))
    
  def test_OmitInputOmitOutputWithDifferentPaymentSameNodeSameSection(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=2, price=1,
                       source_value=self.node,
                       destination_value=self.node,
                       source_section_value=self.section,
                       destination_section_value=self.section,
                       source_payment_value=self.other_payment_node,
                       destination_payment_value=self.payment_node )
    movement_history_list = getMovementHistoryList(
                                      node_uid=self.node.getUid(),
                                      section_uid=self.section.getUid(),
                                      payment_uid=self.payment_node.getUid(),
                                      omit_output=1)
    self.assertEquals(1, len(movement_history_list))
    self.assertEquals(2, movement_history_list[0].total_price)
    self.assertEquals(2, movement_history_list[0].total_quantity)

    movement_history_list = getMovementHistoryList(node_uid=self.node.getUid(),
                                   section_uid=self.section.getUid(),
                                   payment_uid=self.other_payment_node.getUid(),
                                   omit_input=1)
    self.assertEquals(1, len(movement_history_list))
    self.assertEquals(-2, movement_history_list[0].total_price)
    self.assertEquals(-2, movement_history_list[0].total_quantity)

  def test_OmitInputOmitOutputCancellationAmount(self):
    getMovementHistoryList = self.getSimulationTool().getMovementHistoryList
    self._makeMovement(quantity=-1, price=1, cancellation_amount=True)
    self._makeMovement(quantity=2, price=1, cancellation_amount=True)
    mvt_history_list = getMovementHistoryList(node_uid=self.node.getUid(),
                                              omit_input=1)
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(2, mvt_history_list[0].total_price)
    self.assertEquals(2, mvt_history_list[0].total_quantity)

    mvt_history_list = getMovementHistoryList(node_uid=self.node.getUid(),
                                              omit_output=1)
    self.assertEquals(1, len(mvt_history_list))
    self.assertEquals(-1, mvt_history_list[0].total_price)
    self.assertEquals(-1, mvt_history_list[0].total_quantity)

    self.assertEquals(0, len(getMovementHistoryList(
                                              node_uid=self.node.getUid(),
                                              omit_input=1,
                                              omit_output=1)))
    

class TestNextNegativeInventoryDate(InventoryAPITestCase):
  """Tests getInventory methods.
  """
  def testNode(self):
    getNextNegativeInventoryDate = self.getSimulationTool().getNextNegativeInventoryDate
    def makeMovement(start_date=None, quantity=None, change_way=0):
      if not change_way:
        source_value = self.node
        destination_value = self.other_node,
      else:
        source_value = self.other_node
        destination_value = self.node,
      self._makeMovement(quantity=quantity, price=1,
                         source_value=source_value,
                         destination_value=destination_value,
                         start_date=start_date,
                         simulation_state='planned')
    node_uid = self.node.getUid()
    date = DateTime(DateTime().strftime('%Y/%m/%d'))
    self.assertEquals(getNextNegativeInventoryDate(node_uid=node_uid), None)
    makeMovement(quantity=1, change_way=1, start_date=date)
    self.assertEquals(getNextNegativeInventoryDate(node_uid=node_uid), None)
    makeMovement(quantity=3, change_way=0, start_date=date+2)
    self.assertEquals(getNextNegativeInventoryDate(node_uid=node_uid), date+2)
    makeMovement(quantity=5, change_way=1, start_date=date+1)
    self.assertEquals(getNextNegativeInventoryDate(node_uid=node_uid), None)
    makeMovement(quantity=7, change_way=0, start_date=date+5)
    self.assertEquals(getNextNegativeInventoryDate(node_uid=node_uid), date+5)
    makeMovement(quantity=7, change_way=1, start_date=date+4)
    self.assertEquals(getNextNegativeInventoryDate(node_uid=node_uid), None)
    makeMovement(quantity=7, change_way=0, start_date=date+3)
    self.assertEquals(getNextNegativeInventoryDate(node_uid=node_uid), date+3)

class TestInventoryStat(InventoryAPITestCase):
  """Tests Inventory Stat methods.
  """
  def testStockUidQuantity(self):
    getInventoryStat = self.getSimulationTool().getInventoryStat
    def makeMovement(quantity=None):
      self._makeMovement(quantity=quantity, price=1,
                         source_value=self.other_node,
                         destination_value=self.node)
    node_uid = self.node.getUid()
    makeMovement(quantity=1)
    # Test the number of movement for this particular node
    self.assertEquals(getInventoryStat(node_uid=node_uid)[0].stock_uid, 1)
    makeMovement(quantity=3)
    self.assertEquals(getInventoryStat(node_uid=node_uid)[0].stock_uid, 2)
    makeMovement(quantity=5)
    self.assertEquals(getInventoryStat(node_uid=node_uid)[0].stock_uid, 3)

class TestTrackingList(InventoryAPITestCase):
  """Tests Inventory Stat methods.
  """
  def testNodeUid(self):
    getTrackingList = self.getSimulationTool().getTrackingList
    start_date = DateTime()
    def makeMovement(aggregate=None):
      self._makeMovement(quantity=1, price=1,
                         aggregate_value=aggregate,
                         resource_value=self.resource,
                         start_date = start_date,
                         source_value=self.other_node,
                         destination_value=self.node)
    item_uid = self.item.getUid()
    other_item_uid = self.other_item.getUid()
    node_uid = self.node.getUid()
    self.assertEquals(len(getTrackingList(node_uid=node_uid, 
                             at_date=start_date)),0)
    makeMovement(aggregate=self.item)
    result = getTrackingList(node_uid=node_uid,at_date=start_date)
    self.assertEquals(len(result),1)
    self.failIfDifferentSet([x.uid for x in result], [item_uid])
    makeMovement(aggregate=self.other_item)
    result = getTrackingList(node_uid=node_uid,at_date=start_date)
    self.assertEquals(len(result),2)
    self.failIfDifferentSet([x.uid for x in result], [item_uid, other_item_uid])

  def testSeveralAggregateOnMovement(self):
    getTrackingList = self.getSimulationTool().getTrackingList
    start_date = DateTime()
    def makeMovement(aggregate_list=None):
      self._makeMovement(quantity=1, price=1,
                         aggregate_list=aggregate_list,
                         resource_value=self.resource,
                         start_date = start_date,
                         source_value=self.other_node,
                         destination_value=self.node)
    item_uid = self.item.getUid()
    other_item_uid = self.other_item.getUid()
    node_uid = self.node.getUid()
    self.assertEquals(len(getTrackingList(node_uid=node_uid, 
                             at_date=start_date)),0)
    makeMovement(aggregate_list=[self.item.getRelativeUrl(),
                                 self.other_item.getRelativeUrl()])
    result = getTrackingList(node_uid=node_uid,at_date=start_date)
    self.assertEquals(len(result),2)
    self.failIfDifferentSet([x.uid for x in result], [item_uid, other_item_uid])

  def testDates(self):
    """
      Test different dates parameters of getTrackingList.
    """
    getTrackingList = self.getSimulationTool().getTrackingList
    now = DateTime()
    node_1 = self._makeOrganisation(title='Node 1')
    node_2 = self._makeOrganisation(title='Node 2')
    date_0 = now - 4 # Before first movement
    date_1 = now - 3 # First movement
    date_2 = now - 2 # Between both movements
    date_3 = now - 1 # Second movement
    date_4 = now     # After last movement
    self._makeMovement(quantity=1, price=1,
                       aggregate_value=self.item,
                       resource_value=self.resource,
                       start_date=date_1,
                       source_value=None,
                       destination_value=node_1)
    self._makeMovement(quantity=1, price=1,
                       aggregate_value=self.item,
                       resource_value=self.resource,
                       start_date=date_3,
                       source_value=node_1,
                       destination_value=node_2)
    node_1_uid = node_1.getUid()
    node_2_uid = node_2.getUid()
    date_location_dict = {
      date_0: {'at_date': None,       'to_date': None},
      date_1: {'at_date': node_1_uid, 'to_date': None},
      date_2: {'at_date': node_1_uid, 'to_date': node_1_uid},
      date_3: {'at_date': node_2_uid, 'to_date': node_1_uid},
      date_4: {'at_date': node_2_uid, 'to_date': node_2_uid}
    }
    node_uid_to_node_number = {
      node_1_uid: 1,
      node_2_uid: 2
    }
    for date, location_dict in date_location_dict.iteritems():
      for param_id, location_uid in location_dict.iteritems():
        param_dict = {param_id: date}
        uid_list = [x.node_uid for x in getTrackingList(
                            aggregate_uid=self.item.getUid(), **param_dict)]
        if location_uid is None:
          self.assertEqual(len(uid_list), 0)
        else:
          self.assertEqual(len(uid_list), 1)
          self.assertEqual(uid_list[0], location_uid,
                           '%s=now - %i, aggregate should be at node %i but is at node %i' % \
                           (param_id, now - date, node_uid_to_node_number[location_uid], node_uid_to_node_number[uid_list[0]]))

class TestInventoryDocument(InventoryAPITestCase):
  """ Test impact of creating full inventories of stock points on inventory
  lookup. This is an optimisation to regular inventory system to avoid
  reading all stock entries since a node/section/payment is used when
  gathering its amounts of resources.
  """
  def _createAutomaticInventoryAtDate(self, date, override_inventory=None,
                                      full_inventory=False):
    """
      getInventoryList is tested to work in another unit test.
      If full_inventory is false, only inventoriate the first resource
      found.
    """
    self.tic() # Tic so that grabbed inventory is up to date.
    getInventoryList = self.getSimulationTool().getInventoryList
    portal = self.getPortal()
    inventory_module = portal.getDefaultModule(portal_type='Inventory')
    inventory = inventory_module.newContent(portal_type='Inventory')
    inventory.edit(destination_value=self.node,
                   destination_section_value=self.section,
                   start_date=date,
                   full_inventory=full_inventory)
    inventory_list = getInventoryList(node_uid=self.node.getUid(),
                                      at_date=date,
                                      omit_output=1)
    if full_inventory:
      inventory_list = [inventory_list[0]]
    # TODO: Define a second resource which will only be present in full
    # inventories. This will allow testing getInventoryList.
    #else:
    #  inventory_list.append({'resource_relative_url': '','total_quantity': 50,'variation_text': ''})
    for inventory_line in inventory_list:
      line = inventory.newContent(portal_type='Inventory Line')
      if override_inventory is None:
        total_quantity = inventory_line['total_quantity']
      else:
        total_quantity = override_inventory
      line.edit(resource=inventory_line['resource_relative_url'],
                inventory=total_quantity,
                variation_text=inventory_line['variation_text'])
      # TODO: pass more properties through from calculated inventory to
      # inventory lines if needed.
    inventory.deliver()
    return inventory
    
  def _populateInventoryModule(self):
    """
      Create 3 inventories:
         Type     Deviation  Date (see stepCreateInitialMovements)
       - partial  1000       
       - full     10000      
       - full     100000     
    """
    self.BASE_QUANTITY = BASE_QUANTITY = 1
    # TODO: It would be better to strip numbers below seconds instead of below
    # days.
    self.MAX_DATE = MAX_DATE = DateTime(DateTime().Date()) - 1
    self.DUPLICATE_INVENTORY_DATE = MAX_DATE - 8 # Newest
    self.INVENTORY_DATE_3 = INVENTORY_DATE_3 = MAX_DATE - 10 # Newest
    self.INVENTORY_QUANTITY_3 = INVENTORY_QUANTITY_3 = 100000
    self.INVENTORY_DATE_2 = INVENTORY_DATE_2 = INVENTORY_DATE_3 - 10
    self.INVENTORY_QUANTITY_2 = INVENTORY_QUANTITY_2 = 10000
    self.INVENTORY_DATE_1 = INVENTORY_DATE_1 = INVENTORY_DATE_2 - 10 # Oldest
    self.INVENTORY_QUANTITY_1 = INVENTORY_QUANTITY_1 = 1000

    # "actual" quantities are the quantities which will end up in the stock
    # table.
    self.ACTUAL_INVENTORY_QUANTITY_1 = INVENTORY_QUANTITY_1 - \
      BASE_QUANTITY
    self.ACTUAL_INVENTORY_QUANTITY_2 = INVENTORY_QUANTITY_2 - \
      (self.INVENTORY_QUANTITY_1 + BASE_QUANTITY)
    self.ACTUAL_INVENTORY_QUANTITY_3 = INVENTORY_QUANTITY_3 - \
      (self.INVENTORY_QUANTITY_2 + BASE_QUANTITY)
    
    self.movement_uid_list = movement_uid_list = []
    # Initial movement of 1
    movement = self._makeMovement(quantity=BASE_QUANTITY,
      start_date=INVENTORY_DATE_1 - 1,
      simulation_state='delivered')
    movement_uid_list.append(movement.getUid())
    # First (partial) inventory of 1 000
    partial_inventory = self._createAutomaticInventoryAtDate(
      date=INVENTORY_DATE_1, override_inventory=INVENTORY_QUANTITY_1)
    # Second movement of 1
    movement = self._makeMovement(quantity=BASE_QUANTITY,
      start_date=INVENTORY_DATE_2 - 1,
      simulation_state='delivered')
    movement_uid_list.append(movement.getUid())
    # Second (full) inventory of 10 000
    self._createAutomaticInventoryAtDate(date=INVENTORY_DATE_2,
      override_inventory=INVENTORY_QUANTITY_2,
      full_inventory=True)
    # Third movement of 1
    movement = self._makeMovement(quantity=BASE_QUANTITY,
      start_date=INVENTORY_DATE_3 - 1,
      simulation_state='delivered')
    movement_uid_list.append(movement.getUid())
    # Third (full) inventory of 100 000
    self._createAutomaticInventoryAtDate(date=INVENTORY_DATE_3,
      override_inventory=INVENTORY_QUANTITY_3,
      full_inventory=True)
    # Fourth movement of 1
    movement = self._makeMovement(quantity=BASE_QUANTITY,
      start_date=INVENTORY_DATE_3 + 1,
      simulation_state='delivered')
    movement_uid_list.append(movement.getUid())
    self.tic()
    manage_test = self.getPortal().erp5_sql_transactionless_connection.manage_test
    def executeSQL(query):
      manage_test("BEGIN\x00%s\x00COMMIT" % (query, ))
      
    # Make stock table inconsistent with inventory_stock to make sure
    # inventory_stock is actually tested.
    executeSQL("UPDATE stock SET quantity=quantity*2 WHERE uid IN (%s)" %
               (', '.join([str(x) for x in movement_uid_list]), ))
    self.BASE_QUANTITY *= 2
    # Make inventory_stock table inconsistent with stock to make sure
    # inventory_stock is actually not used when checking that partial
    # inventory is not taken into account.
    executeSQL("UPDATE inventory_stock SET quantity=quantity*2 WHERE "\
               "uid IN (%s)" % (', '.join([str(x.getUid()) for x in \
                                           partial_inventory.objectValues()]),
                               ))

  def afterSetUp(self):
    InventoryAPITestCase.afterSetUp(self)
    self._populateInventoryModule()
    simulation_tool = self.getSimulationTool()
    self.getInventory = simulation_tool.getInventory
    self.getInventoryList = simulation_tool.getInventoryList
    self.node_uid = self.node.getUid()

  def _doesInventoryLineMatch(self, criterion_dict, inventory_line):
    """
      True: all values from criterion_dict match given inventory_line.
      False otherwise.
    """
    for criterion_id, criterion_value in criterion_dict.iteritems():
      if criterion_id not in inventory_line \
         or criterion_value != inventory_line[criterion_id]:
        return False
    return True

  def _checkInventoryList(self, inventory_list, criterion_dict_list,
                          ordered_check=False):
    """
      Check that:
        - inventory_list matches length of criterion_dict_list
        - inventory_list contains criterions mentionned in
          criterion_dict_list, line per line.

      If ordered_check is true, chek that lines match in the order they are
      provided.

      Warning: If a criterion can match multiple line, the first encountered
      line is accepted and will not be available for other checks. Sort
      inventory & criterions prior to checking if there is no other way - but
      it's most probable that your test is wrong if such case happens.

      Given inventory must have usable methods:
        __contains__ : to know if a column is present in the inventory
        __getitem__  : to get the value of an inventory column
    """
    if getattr(inventory_list, 'dictionaries', None) is not None:
      inventory_list = inventory_list.dictionaries()
    else:
      inventory_list = inventory_list[:] # That list is modified in this method
    self.assertEquals(len(inventory_list), len(criterion_dict_list))
    for criterion_dict in criterion_dict_list:
      success = False
      for inventory_position in xrange(len(inventory_list)):
        if self._doesInventoryLineMatch(criterion_dict,
                                        inventory_list[inventory_position]):
          del inventory_list[inventory_position]
          success = True
          break
        if ordered_check:
          # We only reach this test if first line of inventory_list didn't
          # match current criterion_dict, which means lines at same initial
          # position do not match.
          break
      # Avoid rendering assertion error messages when no error happened.
      # This is because error messages might causes errors to be thrown if
      # they are rendered in cases where no assertion error would happen...
      # Leads to rasing exception instead of calling self.assert[...] method.
      if not success:
        if ordered_check:
          raise AssertionError, 'Line %r do not match %r' % \
                                (inventory_list[inventory_position],
                                 criterion_dict)
        else:
          raise AssertionError, 'No line in %r match %r' % \
                                (inventory_list, criterion_dict)

  def getInventoryEquals(self, value, inventory_kw):
    """
      Check that optimised getInventory call is equal to given value
      and that unoptimised call is *not* equal to thi value.
    """
    self.assertEquals(value, self.getInventory(**inventory_kw))
    self.assertNotEquals(value,
                         self.getInventory(optimisation__=False,
                                           **inventory_kw))

  def test_01_CurrentInventoryWithFullInventory(self):
    """
      Check that inventory optimisation is executed when querying current
      amount (there is a usable full inventory which is the latest).
    """
    self.getInventoryEquals(value=self.INVENTORY_QUANTITY_3 + \
                                  self.BASE_QUANTITY,
                            inventory_kw={'node_uid': self.node_uid})

  def test_02_InventoryAtLatestFullInventoryDate(self):
    """
      Check that inventory optimisation is executed when querying an amount
      at the exact time of latest usable full inventory.
    """
    self.getInventoryEquals(value=self.INVENTORY_QUANTITY_3,
                            inventory_kw={'node_uid': self.node_uid,
                                          'at_date': self.INVENTORY_DATE_3})

  def test_03_InventoryAtEarlierFullInventoryDate(self):
    """
      Check that inventory optimisation is executed when querying past
      amount (there is a usable full inventory which is not the latest).
    """
    self.getInventoryEquals(value=self.INVENTORY_QUANTITY_2 + \
                                  self.BASE_QUANTITY,
                            inventory_kw={'node_uid': self.node_uid,
                                          'at_date': self.INVENTORY_DATE_3 - \
                                                     1})

  def test_04_InventoryBeforeFullInventoryAfterPartialInventory(self):
    """
      Check that optimisation is not executed when querying past amount
      with no usable full inventory.

      If optimisation was executed,
        self.INVENTORY_QUANTITY_1 * 2 + self.BASE_QUANTITY * 2
      would be found.
    """
    self.assertEquals(self.ACTUAL_INVENTORY_QUANTITY_1 + \
                      self.BASE_QUANTITY * 2,
                      self.getInventory(node_uid=self.node_uid,
                                   at_date=self.INVENTORY_DATE_2 - 1))

  def test_05_InventoryListWithFullInventory(self):
    """
      Check that inventory optimisation is executed when querying current
      amount list (there is a usable full inventory which is the latest).
    """
    inventory = self.getInventoryList(node_uid=self.node_uid)
    reference_inventory = [
      {'date': self.INVENTORY_DATE_3,
       'inventory': self.INVENTORY_QUANTITY_3,
       'node_uid': self.node_uid},
      {'date': self.INVENTORY_DATE_3 + 1,
       'inventory': self.BASE_QUANTITY,
       'node_uid': self.node_uid}
    ]
    self._checkInventoryList(inventory, reference_inventory)

  def test_06_InventoryListAtLatestFullInventoryDate(self):
    """
      Check that inventory optimisation is executed when querying past
      amount list (there is a usable full inventory which is not the latest).
    """
    inventory = self.getInventoryList(node_uid=self.node_uid,
                                      at_date=self.INVENTORY_DATE_3)
    reference_inventory = [
      {'date': self.INVENTORY_DATE_3,
       'inventory': self.INVENTORY_QUANTITY_3,
       'node_uid': self.node_uid}
    ]
    self._checkInventoryList(inventory, reference_inventory)

  def test_07_InventoryListAtEarlierFullInventoryDate(self):
    """
      Check that inventory optimisation is executed when querying past
      amount list (there is a usable full inventory which is not the latest).
    """
    inventory = self.getInventoryList(node_uid=self.node_uid,
                                      at_date=self.INVENTORY_DATE_3 - 1)
    reference_inventory = [
      {'date': self.INVENTORY_DATE_2,
       'inventory': self.INVENTORY_QUANTITY_2,
       'node_uid': self.node_uid},
      {'date': self.INVENTORY_DATE_3 - 1,
       'inventory': self.BASE_QUANTITY,
       'node_uid': self.node_uid}
    ]
    self._checkInventoryList(inventory, reference_inventory)

  def test_08_InventoryListBeforeFullInventoryAfterPartialInventory(self):
    """
      Check that optimisation is not executed when querying past amount list
      with no usable full inventory.
    """
    inventory = self.getInventoryList(node_uid=self.node_uid,
                                      at_date=self.INVENTORY_DATE_2 - 1)
    reference_inventory = [
      {'date': self.INVENTORY_DATE_1 - 1,
       'inventory': self.BASE_QUANTITY,
       'node_uid': self.node_uid},
      {'date': self.INVENTORY_DATE_1,
       'inventory': self.ACTUAL_INVENTORY_QUANTITY_1,
       'node_uid': self.node_uid},
      {'date': self.INVENTORY_DATE_2 - 1,
       'inventory': self.BASE_QUANTITY,
       'node_uid': self.node_uid}
    ]
    self._checkInventoryList(inventory, reference_inventory)

  def test_09_InventoryListGroupedByResource(self):
    """
      Group inventory list by resource explicitely, used inventory is the
      latest.
    """
    inventory = self.getInventoryList(node_uid=self.node_uid,
                                      group_by_resource=1)
    reference_inventory = [
    {'inventory': self.INVENTORY_QUANTITY_3 + self.BASE_QUANTITY,
     'resource_uid': self.resource.getUid(),
     'node_uid': self.node_uid}
    ]
    self._checkInventoryList(inventory, reference_inventory)

  def test_10_InventoryListGroupedByResourceBeforeLatestFullInventoryDate(self):
    """
      Group inventory list by resource explicitely, used inventory is not the
      latest.
    """
    inventory = self.getInventoryList(node_uid=self.node_uid,
                                      group_by_resource=1,
                                      at_date=self.INVENTORY_DATE_3 - 1)
    reference_inventory = [
    {'inventory': self.INVENTORY_QUANTITY_2 + self.BASE_QUANTITY,
     'resource_uid': self.resource.getUid(),
     'node_uid': self.node_uid}
    ]
    self._checkInventoryList(inventory, reference_inventory)

  def test_11_InventoryListAroundLatestInventoryDate(self):
    """
      Test getInventoryList with a min and a max date around latest full
      inventory. A full inventory is used and is not the latest.
    """
    inventory = self.getInventoryList(node_uid=self.node_uid,
                                      from_date=self.INVENTORY_DATE_3 - 1,
                                      at_date=self.INVENTORY_DATE_3 + 1)
    reference_inventory = [
    {'inventory': self.BASE_QUANTITY,
     'resource_uid': self.resource.getUid(),
     'node_uid': self.node_uid,
     'date': self.INVENTORY_DATE_3 - 1},
    {'inventory': self.ACTUAL_INVENTORY_QUANTITY_3,
     'resource_uid': self.resource.getUid(),
     'node_uid': self.node_uid,
     'date': self.INVENTORY_DATE_3},
    {'inventory': self.BASE_QUANTITY,
     'resource_uid': self.resource.getUid(),
     'node_uid': self.node_uid,
     'date': self.INVENTORY_DATE_3 + 1}
    ]
    self._checkInventoryList(inventory, reference_inventory)

  def test_12_InventoryListWithOrderByDate(self):
    """
      Test order_by is preserved by optimisation on date column.
      Also sort on total_quantity column because there are inventory lines
      which are on the same date but with distinct quantities.
    """
    inventory = self.getInventoryList(node_uid=self.node_uid,
                                      from_date=self.INVENTORY_DATE_3 - 1,
                                      at_date=self.INVENTORY_DATE_3 + 1,
                                      sort_on=(('date', 'ASC'),
                                               ('total_quantity', 'DESC')))
    reference_inventory = [
    {'inventory': self.BASE_QUANTITY,
     'resource_uid': self.resource.getUid(),
     'node_uid': self.node_uid,
     'date': self.INVENTORY_DATE_3 - 1},
    {'inventory': self.ACTUAL_INVENTORY_QUANTITY_3,
     'resource_uid': self.resource.getUid(),
     'node_uid': self.node_uid,
     'date': self.INVENTORY_DATE_3},
    {'inventory': self.BASE_QUANTITY,
     'resource_uid': self.resource.getUid(),
     'node_uid': self.node_uid,
     'date': self.INVENTORY_DATE_3 + 1}
    ]
    self._checkInventoryList(inventory, reference_inventory,
                             ordered_check=True)
    inventory = self.getInventoryList(node_uid=self.node_uid,
                                      from_date=self.INVENTORY_DATE_3 - 1,
                                      at_date=self.INVENTORY_DATE_3 + 1,
                                      sort_on=(('date', 'DESC'),
                                               ('total_quantity', 'ASC')))
    reference_inventory.reverse()
    self._checkInventoryList(inventory, reference_inventory,
                             ordered_check=True)

  def test_13_InventoryAfterModificationInPast(self):
    """
    Test inventory after adding a new movement in past and reindex all inventory
    """
    movement = self._makeMovement(quantity=self.BASE_QUANTITY*2,
      start_date=self.INVENTORY_DATE_3 - 2,
      simulation_state='delivered')
    # reindex inventory module, although we modified table by hand
    # everything must be consistent after reindexation
    inventory_module = self.getPortal().getDefaultModule(portal_type='Inventory')
    inventory_module.recursiveReindexObject()
    transaction.commit()
    self.tic()
    inventory_kw={'node_uid': self.node_uid,
                  'at_date': self.INVENTORY_DATE_3}
    value=self.INVENTORY_QUANTITY_3
    # use optimisation
    self.assertEquals(value, self.getInventory(**inventory_kw))
    # without optimisation
    self.assertEquals(value,
                      self.getInventory(optimisation__=False,
                                        **inventory_kw))

  def test_14_TwoInventoryWithSameDateAndResourceAndNode(self):
    """
    It makes no sense to validate two inventories with same date,
    same resource, and same node. The calculation of inventories
    will not work in such case. So here we test that a constraint
    does not allow such things
    """
    portal = self.getPortal()
    self._addPropertySheet('Inventory', 'InventoryConstraint')
    try:
      inventory_module = portal.getDefaultModule(portal_type='Inventory')
      inventory = inventory_module.newContent(portal_type='Inventory')
      date = self.DUPLICATE_INVENTORY_DATE
      inventory.edit(destination_value=self.node,
                     destination_section_value=self.section,
                     start_date=date)
      inventory_line = inventory.newContent(
          resource_value = self.resource,
          quantity = 1)
      self.workflow_tool = portal.portal_workflow
      workflow_id = 'inventory_workflow'
      transition_id = 'deliver_action'
      workflow_id= 'inventory_workflow'
      self.workflow_tool.doActionFor(inventory, transition_id,
              wf_id=workflow_id)
      self.assertEquals('delivered', inventory.getSimulationState())
      transaction.commit()
      self.tic()
      
      # We should detect the previous inventory and fails
      new_inventory = inventory.Base_createCloneDocument(batch_mode=1)
      self.assertRaises(ValidationFailed, self.workflow_tool.doActionFor, 
          new_inventory, transition_id, wf_id=workflow_id)
      workflow_history = self.workflow_tool.getInfoFor(ob=new_inventory, 
          name='history', wf_id=workflow_id)
      workflow_error_message = str(workflow_history[-1]['error_message'])
      self.assertTrue(len(workflow_error_message))
      self.assertTrue(len([x for x in workflow_error_message \
          if x.find('There is already an inventory')]))

      # Add a case in order to check a bug when the other inventory at the
      # same date does not change stock values
      new_inventory = inventory.Base_createCloneDocument(batch_mode=1)
      new_inventory.setStartDate(self.DUPLICATE_INVENTORY_DATE + 1)
      self.workflow_tool.doActionFor(new_inventory, transition_id,
              wf_id=workflow_id)
      self.assertEquals('delivered', new_inventory.getSimulationState())
      transaction.commit()
      self.tic()

      new_inventory = new_inventory.Base_createCloneDocument(batch_mode=1)
      self.assertRaises(ValidationFailed, self.workflow_tool.doActionFor, 
          new_inventory, transition_id, wf_id=workflow_id)
      workflow_history = self.workflow_tool.getInfoFor(ob=new_inventory, 
          name='history', wf_id=workflow_id)
      workflow_error_message = str(workflow_history[-1]['error_message'])
      self.assertTrue(len(workflow_error_message))
      self.assertTrue(len([x for x in workflow_error_message \
          if x.find('There is already an inventory')]))
    finally:
      # remove all property sheets we added to type informations
      ttool = self.getTypesTool()
      for ti_name, psheet_list in self._added_property_sheets.iteritems():
        ti = ttool.getTypeInfo(ti_name)
        property_sheet_set = set(ti.getTypePropertySheetList())
        property_sheet_set.difference_update(psheet_list)
        ti._setTypePropertySheetList(list(property_sheet_set))
      transaction.commit()
      _aq_reset()

  def test_15_InventoryAfterModificationInFuture(self):
    """
    Test inventory after adding a new movement in future 
    """
    movement = self._makeMovement(quantity=self.BASE_QUANTITY*2,
      start_date=self.INVENTORY_DATE_3 + 2,
      simulation_state='delivered')
    transaction.commit()
    self.tic()

    def getCurrentInventoryPathList(resource, **kw):
      # the brain is not a zsqlbrain instance here, so it does not
      # have getPath().
      return [x.path for x in resource.getCurrentInventoryList(**kw)]
    
    # use optimisation
    self.assertEquals(True,movement.getPath() in 
                  [x.path for x in self.resource.getInventoryList(
                                         mirror_uid=self.mirror_node.getUid())])

    # without optimisation
    self.assertEquals(True,movement.getPath() in 
                  [x.path for x in self.resource.getInventoryList(
                                         optimisation__=False,
                                         mirror_uid=self.mirror_node.getUid())])

class BaseTestUnitConversion(InventoryAPITestCase):
  QUANTITY_UNIT_DICT = {}
  METRIC_TYPE_CATEGORY_LIST = ()

  def setUpUnitDefinition(self):

    unit_module = self.portal.quantity_unit_conversion_module
    for base, t in self.QUANTITY_UNIT_DICT.iteritems():
      standard, definition_dict = t

      group = unit_module._getOb(base, None)
      if group is None:
        group = unit_module.newContent(
                 id=base,
                 portal_type='Quantity Unit Conversion Group',
                 quantity_unit="%s/%s" % (base, standard),
                 immediate_reindex=1 )

      for unit, amount in definition_dict.iteritems():
        if group._getOb(unit, None) is None:
          group.newContent(
             id=unit,
             portal_type="Quantity Unit Conversion Definition",
             quantity_unit="%s/%s" % (base, unit),
             quantity=amount,
             immediate_reindex=1)

  def afterSetUp(self):
    InventoryAPITestCase.afterSetUp(self)

    self.setUpUnitDefinition()

  def makeMovement(self, quantity, resource, *variation, **kw):
    m = self._makeMovement(quantity=quantity, resource_value=resource,
      source_value=self.node, destination_value=self.mirror_node, **kw)
    if variation:
      m.setVariationCategoryList(variation)
      self._safeTic()

  def convertedSimulation(self, metric_type, **kw):
    return self.getSimulationTool().getInventory(
      metric_type=metric_type, node_uid=self.node.getUid(),
      **kw)

  def getNeededCategoryList(self):
    category_list = ['metric_type/' + c for c in self.METRIC_TYPE_CATEGORY_LIST]
    for base, t in self.QUANTITY_UNIT_DICT.iteritems():
      standard, definition_dict = t

      quantity = 'quantity_unit/%s/' % base
      category_list.append(quantity + standard)
      category_list.extend(quantity + unit for unit in definition_dict)
    category_list += InventoryAPITestCase.getNeededCategoryList(self)
    return category_list

class TestUnitConversion(BaseTestUnitConversion):
  QUANTITY_UNIT_DICT = {
    # base: (reference, dict_of_others)
    'unit':   ('unit', dict(a_few=None)),
    'length': ('m',    {'in': .0254}),
    'mass':   ('kg',   dict(t=1000, g=.001)),
  }
  METRIC_TYPE_CATEGORY_LIST = (
    'unit',
    'unit/0',
    'unit/1',
    'unit/2',
    'unit/lot',
    'mass/net',
    'mass/nutr/lipid',
  )

  def afterSetUp(self):
    BaseTestUnitConversion.afterSetUp(self)

    self.resource.setQuantityUnitList(('unit/unit', 'length/in'))
    self.other_resource.setQuantityUnit('mass/g')

    keys = ('metric_type', 'quantity_unit', 'quantity', 'default_metric_type')
    for resource, measure_list in {
        self.resource: (
          ('mass/net',        'mass/kg', .123, None),
          ('mass/nutr/lipid', 'mass/g',  45,   True),
        ),
        self.other_resource: (
          # default measure (only useful to set the metric type)
          ('mass/net', None,        1,    True),
          # Bad measures
          ('unit',    'unit/unit',  123,  None), ## duplicate
          ('unit',    'unit/unit',  123,  None), #
          ('unit/0',  'unit/a_few', 123,  None), ## incomplete
          ('unit/1',  'unit/unit',  None, None), #
          ('unit/2',  None,         123,  None), #
          (None,      'mass/kg',    123,  None), #
          (None,      None,         None, None), ## empty
        )}.iteritems():
      for measure in measure_list:
        kw = dict((keys[i], v) for i, v in enumerate(measure) if v is not None)
        resource.newContent(portal_type='Measure', **kw)

    self.resource.setOptionalVariationBaseCategory('industrial_phase')
    self.resource.setVariationBaseCategoryList(('colour', 'size'))
    self.resource.setVariationCategoryList(self.VARIATION_CATEGORIES)
    m = self.resource.getDefaultMeasure('mass/t')

    m.setMeasureVariationBaseCategory('colour')
    for colour, quantity in ('green', 43), ('red', 56):
      m.newContent(portal_type='Measure Cell', quantity=quantity) \
       ._setMembershipCriterionCategory('colour/' + colour)

    self._safeTic()

  def testConvertedInventoryList(self):
    self.makeMovement(2, self.resource, 'colour/green', 'size/big')
    self.makeMovement(789, self.other_resource)
    self.makeMovement(-13, self.resource, 'colour/red', 'size/small',
                 'industrial_phase/phase1', 'industrial_phase/phase2')


    for i in range(3):
      self.assertEquals(None, self.convertedSimulation('unit/%i' % i))

    self.assertEquals(None,
                      self.convertedSimulation('unit',
                                               simulation_period='Current'))
    self.assertEquals(11, self.convertedSimulation('unit'))

    self.assertEquals(11 * .123 - .789, self.convertedSimulation('mass/net'))
    self.assertEquals((11 * 123 - 789) / 1e6,
                      self.convertedSimulation('mass/net',
                                               quantity_unit='mass/t'))

    self.assertEquals(13 * .056 - 2 * .043,
                      self.convertedSimulation('mass/nutr/lipid'))

class TestUnitConversionDefinition(BaseTestUnitConversion):
  QUANTITY_UNIT_DICT = {
    # base: (reference, dict_of_others)
    'unit':   ('unit', dict(lot=1000, pack=6)),
  }
  METRIC_TYPE_CATEGORY_LIST = (
    'unit',
  )

  def afterSetUp(self):
    BaseTestUnitConversion.afterSetUp(self)

    # Aliases for readability
    self.resource_bylot = self.resource
    self.resource_bylot_overriding = self.other_resource

    # And a third resource
    self.resource_byunit = self.getProductModule().newContent(
                                  title='Resource counted By Unit',
                                  portal_type='Product')

    self.resource_bypack = self.getProductModule().newContent(
                                  title='Resource counted By Pack',
                                  portal_type='Product')

    self.resource_bylot.setQuantityUnit('unit/lot')
    self.resource_bypack.setQuantityUnit('unit/pack')
    self.resource_bylot_overriding.setQuantityUnit('unit/lot')
    self.resource_byunit.setQuantityUnit('unit/unit')


    self._safeTic()

    base_unit = self.resource_bylot_overriding.newContent(
                  portal_type='Quantity Unit Conversion Group',
                  quantity_unit='unit/unit',
                  immediate_reindex=1)


    unit = base_unit.newContent(
            portal_type='Quantity Unit Conversion Definition',
            quantity_unit='unit/lot',
            quantity=50,
            immediate_reindex=1)

    self._safeTic()

  def testAggregatedReports(self):
    self.makeMovement(-10, self.resource_bylot)
    self.makeMovement(-1, self.resource_bypack)
    self.makeMovement(2, self.resource_bylot_overriding)
    self.makeMovement(500, self.resource_byunit)

    # Always displayed as quantity*unit_ratio
    self.assertEquals(10*1000 + 1*6 - 2*50 - 500*1,
                      self.convertedSimulation('unit'))
    self.assertEquals(10*1000 + 1*6 - 2*50 - 500*1,
                      self.convertedSimulation('unit',
                                               quantity_unit='unit/unit'))
    self.assertEquals(10*1 + 1*(6*0.001) - 2*1 - 500*(1./1000),
                      self.convertedSimulation('unit',
                                               quantity_unit='unit/lot'))
    # amounts are rounded on the 12th digit.
    self.assertEquals(round(10*(1000./6) + 1*1 - 2*(50./6) - 500*(1./6), 12),
                      self.convertedSimulation('unit',
                                               quantity_unit='unit/pack'))

  def testResourceConvertQuantity(self):
    # First, test without local Unit Definitions
    for resource in (self.resource_bylot,
                     self.resource_bypack,
                     self.resource_byunit):
      # not_reference -> reference quantity
      self.assertEquals(1000,
                        resource.convertQuantity(1,
                                                 "unit/lot",
                                                 "unit/unit"))
      # reference -> not_reference
      self.assertEquals(1,
                        resource.convertQuantity(1000,
                                                 "unit/unit",
                                                 "unit/lot"))
      # not_reference -> not_reference
      self.assertEquals(1*1000./6,
                        resource.convertQuantity(1,
                                                 "unit/lot",
                                                 "unit/pack"))
      self.assertEquals(1*6./1000,
                        resource.convertQuantity(1,
                                                 "unit/pack",
                                                 "unit/lot"))

    # then with local Unit definition
    self.assertEquals(1*50,
                      self.resource_bylot_overriding\
                          .convertQuantity(1, "unit/lot", "unit/unit"))
    self.assertEquals(1./50,
                      self.resource_bylot_overriding\
                          .convertQuantity(1, "unit/unit", "unit/lot"))
    self.assertEquals(1*50./6,
                      self.resource_bylot_overriding\
                          .convertQuantity(1, "unit/lot", "unit/pack"))
    self.assertEquals(1*6./50,
                      self.resource_bylot_overriding\
                          .convertQuantity(1, "unit/pack", "unit/lot"))

  def testResourceConvertQuantityAfterGlobalChange(self):
    """
    after a change in a Global unit definition, definitions should get
    reindexed.
    """
    # Before the global change, global definition reads 1000
    self.assertEquals(1000,
                      self.resource_bylot.convertQuantity(1,
                                                           "unit/lot",
                                                           "unit/unit"))
    # which does not affect resources overriding the definition
    self.assertEquals(1*50,
                      self.resource_bylot_overriding\
                          .convertQuantity(1, "unit/lot", "unit/unit"))

    portal = self.getPortalObject()

    lot_uid = portal.portal_categories.quantity_unit.unit.lot.getUid()
    query = portal.portal_catalog(quantity_unit_uid=lot_uid,
                                                  grand_parent_portal_type= \
                                                    "Quantity Unit Conversion" \
                                                    " Module",
                                                  portal_type= \
                                                    "Quantity Unit Conversion" \
                                                    " Definition")
    self.assertEquals(1, len(query))
    query[0].getObject().setQuantity(500)

    # this change triggers Resource reindexations. Wait for 'em!
    transaction.commit()
    self.tic()

    # SQL tables should have been updated:
    self.assertEquals(500,
                      self.resource_bylot.convertQuantity(1,
                                                           "unit/lot",
                                                           "unit/unit"))
    # without affecting resources that override the definition
    self.assertEquals(1*50,
                      self.resource_bylot_overriding\
                          .convertQuantity(1, "unit/lot", "unit/unit"))

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestInventory))
  suite.addTest(unittest.makeSuite(TestInventoryList))
  suite.addTest(unittest.makeSuite(TestMovementHistoryList))
  suite.addTest(unittest.makeSuite(TestInventoryStat))
  suite.addTest(unittest.makeSuite(TestNextNegativeInventoryDate))
  suite.addTest(unittest.makeSuite(TestTrackingList))
  suite.addTest(unittest.makeSuite(TestInventoryDocument))
  suite.addTest(unittest.makeSuite(TestUnitConversion))
  suite.addTest(unittest.makeSuite(TestUnitConversionDefinition))
  return suite

# vim: foldmethod=marker
