##############################################################################
#
# Copyright (c) 2004 Nexedi SARL and Contributors. All Rights Reserved.
#          Sebastien Robin <seb@nexedi.com>
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



#
# Skeleton ZopeTestCase
#

from random import randint

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Needed in order to have a log file inside the current folder
os.environ['EVENT_LOG_FILE'] = os.path.join(os.getcwd(), 'zLOG.log')
os.environ['EVENT_LOG_SEVERITY'] = '-300'

from Testing import ZopeTestCase
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from DateTime import DateTime
from Products.ERP5.Document.Person import Person
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from Products.ERP5SyncML.Conduit.ERP5Conduit import ERP5Conduit
from Products.ERP5SyncML.SyncCode import SyncCode
from zLOG import LOG
import time

class Test(ERP5TypeTestCase):

  # Different variables used for this test
  run_all_test = 1
  resource_type='Apparel Component'
  resource_variation_type='Apparel Component Variation'
  resource_module = 'apparel_component_module'

  def getTitle(self):
    """
    """
    return "Domain Tool"

  def enableHotReindexing(self):
    """
    You can override this. Return if we should create (1) or not (0) an activity tool
    """
    return 0

  def getBusinessTemplateList(self):
    """
      Return the list of business templates.

    """
    return ('erp5_trade','erp5_apparel_depend','erp5_apparel')

  def getPortalId(self):
    return self.getPortal().getId()

  def getResourceModule(self):
    return getattr(self.getPortal(), self.resource_module, None)

  def logMessage(self,message):
    ZopeTestCase._print('\n%s ' % message)
    LOG('Testing... ',0,message)

  def afterSetUp(self):
    self.login()

  def login(self, quiet=0):
    uf = self.getPortal().acl_users
    uf._doAddUser('seb', '', ['Manager'], [])
    user = uf.getUserById('seb').__of__(uf)
    newSecurityManager(None, user)

  def getSaleOrderModule(self):
    return getattr(self.getPortal(),'sale_order_module',None)

  def getOrderLine(self):
    return self.getSaleOrderModule()['1']['1']

  def getPredicate(self):
    return self.getOrganisationModule()['1']

  def createData(self):
    # We have no place to put a Predicate, we will put it in a
    # Organisation Module
    portal = self.getPortal()
    type_tool = self.getTypeTool()
    module_type = type_tool['Organisation Module']
    module_type.allowed_content_types += ('Mapped Value',)
    organisation_module = self.getOrganisationModule()
    predicate = organisation_module.newContent(id='1',portal_type='Mapped Value')
    predicate.setCriterion('quantity',identity=None,min=None,max=None)
    predicate.immediateReindexObject()
    
    resource_module = self.getResourceModule()
    self.resource = resource = resource_module.newContent(id='1',portal_type=self.resource_type)
    resource.newContent(id='blue',portal_type=self.resource_variation_type,immediate_reindex=1)
    resource.newContent(id='red',portal_type=self.resource_variation_type,immediate_reindex=1)
    resource.setVariationBaseCategoryList(['variation'])
    self.supply_line = supply_line = resource.newContent(id='default_supply_line',portal_type='Supply Line')

    # Then create an order with a particular line
    order_module = self.getSaleOrderModule()
    order =  order_module.newContent(id='1',portal_type='Sale Order')
    line = order.newContent(id='1',portal_type='Sale Order Line')
    line.immediateReindexObject()

    # Then create a base category
    portal_categories = self.getCategoryTool()
    for bc in ('region', ):
      if not hasattr(portal_categories, bc):
        portal_categories.newContent(portal_type='Base Category',id=bc)
      portal_categories[bc].setAcquisitionMaskValue(1)
      portal_categories[bc].setAcquisitionCopyValue(0)
      portal_categories[bc].setAcquisitionAppendValue(0)
      if not 'europe' in portal_categories[bc].objectIds():
        big_region = portal_categories[bc].newContent(id='europe',portal_type='Category')
      if not 'africa' in portal_categories[bc].objectIds():
        big_region = portal_categories[bc].newContent(id='africa',portal_type='Category')
      if not 'asia' in portal_categories[bc].objectIds():
        big_region = portal_categories[bc].newContent(id='asia',portal_type='Category')
      portal_categories[bc].recursiveImmediateReindexObject()

  def checkPredicate(self, test=None):

    predicate = self.getPredicate()
    #predicate.setMembershipCriterionBaseCategoryList([])
    #predicate.setMembershipCriterionCategoryList([])
    #predicate.setCriterion('quantity',identity=45,min=None,max=None)
    predicate.immediateReindexObject()


    order_line = self.getOrderLine()
    domain_tool = self.getDomainTool()

    # Test with order line and predicate to none
    predicate_list = domain_tool.searchPredicateList(order_line,test=test)
    self.assertEquals(len(predicate_list),1) # Actually, a predicate where
                                             # nothing is defined is ok

    # Test with order line not none and predicate to none
    order_line.setQuantity(45)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test)
    self.assertEquals(len(predicate_list),1)

    # Test with order line not none and predicate to identity
    order_line.setQuantity(45)
    kw = {'portal_type':'Mapped Value'}
    predicate.setCriterion('quantity',identity=45,min=None,max=None)
    predicate.immediateReindexObject()
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),1)
    order_line.setQuantity(40)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),0)

    # Test with order line not none and predicate to min
    order_line.setQuantity(45)
    predicate = self.getPredicate()
    predicate.setCriterion('quantity',identity=None,min=30,max=None)
    predicate.immediateReindexObject()
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),1)
    order_line.setQuantity(10)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test)
    self.assertEquals(len(predicate_list),0)

    # Test with order line not none and predicate to max
    order_line.setQuantity(45)
    predicate = self.getPredicate()
    predicate.setCriterion('quantity',identity=None,min=None,max=50)
    predicate.immediateReindexObject()
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),1)
    order_line.setQuantity(60)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),0)

    # Test with order line not none and predicate to min max
    order_line.setQuantity(20)
    predicate = self.getPredicate()
    predicate.setCriterion('quantity',identity=None,min=30,max=50)
    predicate.immediateReindexObject()
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),0)
    order_line.setQuantity(60)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),0)
    order_line.setQuantity(45)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),1)

    # Test with order line not none and predicate to min max
    # and also predicate to a category
    predicate.setMembershipCriterionBaseCategoryList(['region'])
    predicate.setMembershipCriterionCategoryList(['region/europe'])
    predicate.immediateReindexObject()
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),0)
    order_line.setCategoryList(['region/africa'])
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),0)
    order_line.setCategoryList(['region/europe'])
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),1)
    order_line.setQuantity(60)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),0)

    # Test with order line not none and predicate to date min and date max
    kw = {'portal_type':'Supply Line'}
    self.supply_line.setBasePrice(23)
    self.supply_line.setPricedQuantity(1)
    self.supply_line.setDefaultResourceValue(self.resource)
    order_line.setDefaultResourceValue(self.resource)
    date1 = DateTime('2005/04/08 10:47:26.388 GMT-4')
    date2 = DateTime('2005/04/10 10:47:26.388 GMT-4')
    self.supply_line.setStartDateRangeMin(date1)
    self.supply_line.setStartDateRangeMax(date2)
    self.supply_line.immediateReindexObject()
    current_date = DateTime('2005/04/1 10:47:26.388 GMT-4')
    order_line.setStartDate(current_date)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),0)
    current_date = DateTime('2005/04/09 10:47:26.388 GMT-4')
    order_line.setStartDate(current_date)
    predicate_list = domain_tool.searchPredicateList(order_line,test=test,**kw)
    self.assertEquals(len(predicate_list),1)

  def test_01_SearchPredidateListWithNoTest(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      self.logMessage('Search Predicate List With No Test')
    self.createData()
    self.checkPredicate(test=0)

  def test_02_SearchPredidateListWithTest(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      self.logMessage('Search Predicate List With Test')
    self.createData()
    self.checkPredicate(test=1)

  def test_03_GenerateMappedValue(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      self.logMessage('Generate Mapped Value')
    self.createData()
    self.supply_line.setVariationBaseCategoryList(['colour'])
    self.supply_line.setBasePrice(23)
    self.supply_line.setPricedQuantity(1)
    self.supply_line.setDefaultResourceValue(self.resource)
    #self.supply_line.setMultimembershipCriterionBaseCategoryList(['resource'])
    self.supply_line.setMappedValuePropertyList(['base_price','priced_quantity'])
    #self.supply_line.setMembershipCriterionCategoryList(['resource/%s' % self.resource.getRelativeUrl()])
    self.supply_line.recursiveImmediateReindexObject()
    domain_tool = self.getDomainTool()
    context = self.resource.asContext(categories=['resource/%s' % self.resource.getRelativeUrl()])
    mapped_value = domain_tool.generateMappedValue(context)
    self.assertEquals(mapped_value.getBasePrice(),23)

  def test_04_GenerateMappedValueWithRanges(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      self.logMessage('Generate Mapped Value With Ranges')
    self.createData()
    self.supply_line.setBasePrice(23)
    self.supply_line.setPricedQuantity(1)
    self.supply_line.setDefaultResourceValue(self.resource)
    date1 = DateTime('2005/04/08')
    date2 = DateTime('2005/04/10')
    self.supply_line.setStartDateRangeMin(date1)
    self.supply_line.setStartDateRangeMax(date2)
    LOG('Test04, supply_line.getStartDateRangeMin',0,self.supply_line.getStartDateRangeMin())
    LOG('Test04, supply_line.getStartDateRangeMax',0,self.supply_line.getStartDateRangeMax())
    self.supply_line.setMappedValuePropertyList(['base_price','priced_quantity'])
    self.supply_line.recursiveImmediateReindexObject()
    domain_tool = self.getDomainTool()
    order_line = self.getOrderLine()
    order_line.setDefaultResourceValue(self.resource)
    current_date = DateTime('2005/04/01')
    order_line.setStartDate(current_date)
    kw = {'portal_type':('Supply Line','Supply Cell')}
    mapped_value = domain_tool.generateMappedValue(order_line,**kw)
    self.assertEquals(mapped_value,None)
    current_date = DateTime('2005/04/09')
    order_line.setStartDate(current_date)
    mapped_value = domain_tool.generateMappedValue(order_line,**kw)
    self.assertEquals(mapped_value.getBasePrice(),23)

  def test_05_GenerateMappedValueWithVariation(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      self.logMessage('Generate Mapped Value With Variation')
    self.createData()
    self.supply_line.setVariationBaseCategoryList(['colour'])
    self.supply_line.setBasePrice(23)
    self.supply_line.setPricedQuantity(1)
    self.supply_line.setDefaultResourceValue(self.resource)
    #self.supply_line.setMultimembershipCriterionBaseCategoryList(['resource']) # Do we need to add 'variation' ???
    self.supply_line.setMappedValuePropertyList(['base_price','priced_quantity'])
    #self.supply_line.setMembershipCriterionCategoryList(['resource/%s' % self.resource.getRelativeUrl()])
    self.supply_line.setPVariationBaseCategoryList(['variation'])
    self.supply_line.updateCellRange(base_id='path')
    cell_range = self.supply_line.SupplyLine_asCellRange()
    for range in cell_range[0]:
      cell = self.supply_line.newCell(range,base_id='path')
      cell.setMappedValuePropertyList(['base_price','priced_quantity'])
      cell.setMultimembershipCriterionBaseCategoryList(['resource','variation'])
      LOG('test, range',0,range)
      cell.setPricedQuantity(1)
      if range.find('blue')>=0:
        cell.setMembershipCriterionCategoryList([range])
        cell.setBasePrice(45)
      if range.find('red')>=0:
        cell.setMembershipCriterionCategoryList([range])
        cell.setBasePrice(26)

    def sort_method(x,y):
      # make sure we get cell before
      if hasattr(x,'hasCellContent'):
        x_cell = x.hasCellContent(base_id='path')
        if x_cell:
          return 1
      if hasattr(y,'hasCellContent'):
        y_cell = y.hasCellContent(base_id='path')
        if y_cell:
          return -1
      return 0

    self.supply_line.recursiveImmediateReindexObject()
    domain_tool = self.getDomainTool()
    context = self.resource.asContext(categories=['resource/%s' % self.resource.getRelativeUrl(),'variation/%s/blue' % self.resource.getRelativeUrl()])
    mapped_value = domain_tool.generateMappedValue(context,sort_method=sort_method)
    self.assertEquals(mapped_value.getProperty('base_price'),45)
    context = self.resource.asContext(categories=['resource/%s' % self.resource.getRelativeUrl(),'variation/%s/red' % self.resource.getRelativeUrl()])
    mapped_value = domain_tool.generateMappedValue(context,sort_method=sort_method)
    self.assertEquals(mapped_value.getProperty('base_price'),26)
    # Now check the price
    self.assertEquals(self.resource.getPrice( self.resource.asContext(categories=['resource/%s' % self.resource.getRelativeUrl(),'variation/%s/blue' % self.resource.getRelativeUrl()]),sort_method=sort_method),45)


if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(Test))
        return suite

