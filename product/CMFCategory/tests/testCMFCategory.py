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
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from zLOG import LOG
import time

try:
  from transaction import get as get_transaction
except ImportError:
  pass

class TestCMFCategory(ERP5TypeTestCase):

  # Different variables used for this test
  run_all_test = 1
  id1 = '1'
  id2 = '2'
  region1 = 'europe/west/france'
  region2 = 'europe/west/germany'
  region_list = [region1, region2]

  def getTitle(self):
    return "CMFCategory"

  def getBusinessTemplateList(self):
    """
      Return the list of business templates.

      the business template crm give the following things :
      modules:
        - person
        - organisation
      base categories:
        - region
        - subordination

      /organisation
    """
    return ('erp5_base',)

  def getCategoriesTool(self):
    return getattr(self.getPortal(), 'portal_categories', None)

  def getPortalId(self):
    return self.getPortal().getId()

  def test_00_HasEverything(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Has Everything ')
      LOG('Testing... ',0,'testHasEverything')
    self.failUnless(self.getCategoriesTool()!=None)
    self.failUnless(self.getPersonModule()!=None)
    self.failUnless(self.getOrganisationModule()!=None)

  def afterSetUp(self, quiet=1, run=1):
    self.login()
    portal = self.getPortal()
    person_module = self.getPersonModule()
    if self.id1 not in person_module.objectIds():
      p1 = person_module.newContent(id=self.id1)
    else:
      p1 = person_module._getOb(self.id1)
    if self.id1 not in p1.objectIds():
      sub_person = p1.newContent(id=self.id1,portal_type='Person')
    if self.id2 not in person_module.objectIds():
      p2 = person_module.newContent(id=self.id2)
    organisation_module = self.getOrganisationModule()
    if self.id1 not in organisation_module.objectIds():
      o1 = organisation_module.newContent(id=self.id1)
    if self.id2 not in organisation_module.objectIds():
      o2 = organisation_module.newContent(id=self.id2)
    portal_categories = self.getCategoriesTool()
    # This set the acquisition for region
    for bc in ('region', ):
      if not hasattr(portal_categories, bc):
        portal_categories.newContent(portal_type='Base Category',id=bc)
      portal_categories[bc].setAcquisitionBaseCategoryList(('subordination','parent'))
      portal_categories[bc].setAcquisitionPortalTypeList("python: ['Address', 'Organisation', 'Person']")
      portal_categories[bc].setAcquisitionMaskValue(1)
      portal_categories[bc].setAcquisitionCopyValue(0)
      portal_categories[bc].setAcquisitionAppendValue(0)
      portal_categories[bc].setAcquisitionObjectIdList(['default_address'])
      if not 'europe' in portal_categories[bc].objectIds():
        portal_categories[bc].newContent(id='europe',portal_type='Category')
      big_region = portal_categories[bc]['europe']
      # Now we have to include by hand no categories
      if not 'west' in big_region.objectIds():
        big_region.newContent(id='west',portal_type='Category')
      region = big_region['west']
      if not 'france' in region.objectIds():
        region.newContent(id='france',portal_type='Category')
      if not 'germany' in region.objectIds():
        region.newContent(id='germany',portal_type='Category')
    for bc in ('subordination', ):
      if not hasattr(portal_categories, bc):
        portal_categories.newContent(portal_type='Base Category',id=bc)
      portal_categories[bc].setAcquisitionPortalTypeList("python: ['Career', 'Organisation']")
      portal_categories[bc].setAcquisitionMaskValue(0)
      portal_categories[bc].setAcquisitionCopyValue(0)
      portal_categories[bc].setAcquisitionAppendValue(0)
      portal_categories[bc].setAcquisitionSyncValue(1)
      portal_categories[bc].setAcquisitionObjectIdList(['default_career'])
    for bc in ('gender', ):
      if not hasattr(portal_categories, bc):
        portal_categories.newContent(portal_type='Base Category',id=bc)
      portal_categories[bc].setAcquisitionPortalTypeList("python: []")
      portal_categories[bc].setAcquisitionMaskValue(0)
      portal_categories[bc].setAcquisitionCopyValue(0)
      portal_categories[bc].setAcquisitionAppendValue(0)
      portal_categories[bc].setAcquisitionSyncValue(1)
      portal_categories[bc].setFallbackBaseCategoryList(['subordination'])

  def beforeTearDown(self):
    """Clean up."""
    # categories
    for bc in ('region', 'subordination', 'gender'):
      bc_obj = self.getPortal().portal_categories[bc]
      bc_obj.manage_delObjects()

  def login(self, quiet=0, run=run_all_test):
    uf = self.getPortal().acl_users
    uf._doAddUser('seb', '', ['Manager'], [])
    user = uf.getUserById('seb').__of__(uf)
    newSecurityManager(None, user)

  def test_01_SingleCategory(self, quiet=0, run=run_all_test):
    # Test if a single category is working
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Single Category ')
      LOG('Testing... ',0,'testSingleCategory')
    o1 = self.getOrganisationModule()._getOb(self.id1)
    LOG('SingleCategory,',0,o1.getGenderRelatedValueList())
    
    p1 = self.getPersonModule()._getOb(self.id1)
    p1.setRegion(self.region1)
    self.assertEqual(p1.getRegion(),self.region1)
    self.assertEqual(p1.getDefaultRegion(),self.region1)
    self.assertEqual(p1.getRegionList(),[self.region1])

  def test_02_MultipleCategory(self, quiet=0, run=run_all_test):
    # Test if multiple categories are working
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Multiple Category ')
      LOG('Testing... ',0,'testMultipleCategory')
    portal = self.getPortal()
    region_value_list = [portal.portal_categories.resolveCategory('region/%s' % self.region1),
                         portal.portal_categories.resolveCategory('region/%s' % self.region2)]
    self.assertNotEqual(None,region_value_list[0])
    self.assertNotEqual(None,region_value_list[1])
    p1 = self.getPersonModule()._getOb(self.id1)
    p1.setRegion(self.region_list)
    self.assertEqual(p1.getRegion(),self.region1)
    self.assertEqual(p1.getDefaultRegion(),self.region1)
    self.assertEqual(p1.getRegionList(),self.region_list)

  def test_03_CategoryValue(self, quiet=0, run=run_all_test):
    # Test if we can get categories values
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Category Value ')
      LOG('Testing... ',0,'testCategoryValue')
    portal = self.getPortal()
    region_value = portal.portal_categories.resolveCategory('region/%s' % self.region1)
    self.assertNotEqual(None,region_value)
    p1 = self.getPersonModule()._getOb(self.id1)
    p1.setRegion(self.region_list)
    self.assertEqual(p1.getRegionValue(),region_value)

  def test_04_ReturnNone(self, quiet=0, run=run_all_test):
    # Test if we getCategory return None if the cat is '' or None
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Return None ')
      LOG('Testing... ',0,'testReturnNone')
    portal = self.getPortal()
    p1 = self.getPersonModule()._getOb(self.id1)
    p1.setRegion(None)
    self.assertEqual(p1.getRegion(),None)
    p1.setRegion('')
    self.assertEqual(p1.getRegion(),None)

  def test_05_SingleAcquisition(self, quiet=0, run=run_all_test):
    # Test if the acquisition for a single value is working
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Single Acquisition ')
      LOG('Testing... ',0,'testSingleAcquisition')
    portal = self.getPortal()
    o1 = self.getOrganisationModule()._getOb(self.id1)
    p1 = self.getPersonModule()._getOb(self.id1)
    o1.setRegion(self.region1)
    p1.setSubordinationValue(o1)
    self.assertEqual(p1.getRegion(),self.region1)
    self.assertEqual(p1.getDefaultRegion(),self.region1)
    self.assertEqual(p1.getRegionList(),[self.region1])

  def test_06_ListAcquisition(self, quiet=0, run=run_all_test):
    # Test if the acquisition for a single value is working
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test List Acquisition ')
      LOG('Testing... ',0,'testListAcquisition')
    portal = self.getPortal()
    o1 = self.getOrganisationModule()._getOb(self.id1)
    p1 = self.getPersonModule()._getOb(self.id1)
    o1.setRegion(self.region_list)
    p1.setSubordinationValue(o1)
    test = p1.getSubordinationValue()
    LOG('Testing... getSubordinationValue',0,test)
    sub = p1.getSubordinationValue()
    self.assertEqual(sub,o1)
    self.assertEqual(p1.getRegion(),self.region1)
    self.assertEqual(p1.getDefaultRegion(),self.region1)
    self.assertEqual(p1.getRegionList(),self.region_list)

  def test_07_SubordinationValue(self, quiet=0, run=run_all_test):
    # Test if an infinite loop of the acquisition for a single value is working
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Subordination Value ')
      LOG('Testing... ',0,'testSubordinationValue')
    portal = self.getPortal()
    p1 = self.getPersonModule()._getOb(self.id1)
    o1 = self.getOrganisationModule()._getOb(self.id1)
    p1.setSubordinationValue(o1)
    p1.setRegion(None)
    self.assertEqual(p1.getSubordinationValue(),o1)
    self.assertEqual(p1.getDefaultSubordinationValue(),o1)
    self.assertEqual(p1.getSubordinationValueList(),[o1])

  def test_08_SubordinationMultipleValue(self, quiet=0, run=run_all_test):
    # Test if an infinite loop of the acquisition for a single value is working
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Subordination Multiple Value ')
      LOG('Testing... ',0,'testSubordinationMultipleValue')
    portal = self.getPortal()
    p1 = self.getPersonModule()._getOb(self.id1)
    o1 = self.getOrganisationModule()._getOb(self.id1)
    o2 = self.getOrganisationModule()._getOb(self.id2)
    subordination_value_list = [o1,o2]
    p1.setSubordinationValueList(subordination_value_list)
    p1.setRegion(None)
    self.assertEqual(p1.getSubordinationValue(),o1)
    self.assertEqual(p1.getDefaultSubordinationValue(),o1)
    self.assertEqual(p1.getSubordinationValueList(),subordination_value_list)

  def test_09_GetCategoryParentUidList(self, quiet=0, run=run_all_test):
    # Test if an infinite loop of the acquisition for a single value is working
    # WARNING: getCategoryParentUidList does not provide a sorted result
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Get Category Parent Uid List ')
      LOG('Testing... ',0,'testGetCategoryParentUidList')
    portal = self.getPortal()
    portal_categories = self.getCategoriesTool()
    # Create a base category basecat
    #portal_categories.manage_addProduct['ERP5'].addBaseCategory('basecat')
    portal_categories.newContent(portal_type='Base Category',id='basecat')
    # Create a category cat1 at basecate
    portal_categories.basecat.newContent(id='cat1',portal_type='Category')
    basecat = portal_categories.basecat
    cat1 = portal_categories.basecat.cat1
    # Create a category cat2 at cat1
    portal_categories.basecat.cat1.newContent(portal_type='Category',id='cat2')
    cat2 = portal_categories.basecat.cat1.cat2
    cat2.newContent(id='cat2',portal_type='Category')
    # Compare result after sorting it
    parent_uid_list = [(cat2.getUid(), basecat.getUid(), 1),
                       (cat1.getUid(), basecat.getUid(), 0),
                       (basecat.getUid(), basecat.getUid(), 0)]
    parent_uid_list.sort()                       
    parent_uid_list2 = cat2.getCategoryParentUidList(relative_url = cat2.getRelativeUrl())
    parent_uid_list2.sort()
    self.assertEqual(parent_uid_list2, parent_uid_list)
    
  def test_10_FallBackBaseCategory(self, quiet=0, run=run_all_test):
    # Test if we can use an alternative base category
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Fallback Base Category ')
      LOG('Testing... ',0,'testFallbackBaseCategory')
    portal = self.getPortal()
    p1 = self.getPersonModule()._getOb(self.id1)
    p2 = self.getPersonModule()._getOb(self.id2)
    o1 = self.getOrganisationModule()._getOb(self.id1)
    self.assertEqual(p1.getGenderValue(),None)
    p1.setSubordinationValue(o1)
    self.assertEqual(p1.getGenderValue(),o1)

  def test_11_ParentAcquisition(self, quiet=0, run=run_all_test):
    # Test if we can use an alternative base category
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Parent Acquisition ')
      LOG('Testing... ',0,'testParentAcquisition')
    portal = self.getPortal()
    p1 = self.getPersonModule()._getOb(self.id1)
    self.assertEqual(p1.getRegion(),None)
    sub_person = p1._getOb(self.id1)
    self.assertEqual(sub_person.getRegion(),None)
    p1.setRegion(self.region1)
    self.assertEqual(p1.getRegion(),self.region1)
    self.assertEqual(sub_person.getRegion(),self.region1)

  def test_12_GetRelatedValueAndValueList(self, quiet=0, run=run_all_test):
    # Test if an infinite loop of the acquisition for a single value is working
    # Typical error results from bad brain (do not copy, use aliases for zsqlbrain.py)
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Get Related Value And Value List ')
      LOG('Testing... ',0,'testGetRelatedValueAndValueList')
    portal = self.getPortal()
    p1 = self.getPersonModule()._getOb(self.id1)
    p2 = self.getPersonModule()._getOb(self.id2)
    o1 = self.getOrganisationModule()._getOb(self.id1)
    p1.setGenderValue(o1)
    get_transaction().commit()
    self.tic() # This is required 

    self.assertEqual(p1.getGenderValue(),o1)
    self.assertEqual(o1.getGenderRelatedValueList(),[p1])
    p2.setGenderValue(o1) # reindex implicit
    get_transaction().commit()
    self.tic()

    self.assertEqual(len(o1.getGenderRelatedValueList()),2)

  def test_13_RenameCategory(self, quiet=0, run=run_all_test) :
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Category Renaming')
      LOG('Testing... ',0,'Category Renaming')
    
    portal = self.getPortal()
    france = portal.portal_categories.resolveCategory(
                                            'region/europe/west/france')
    self.assertNotEqual(france, None)
    
    p1 = self.getPersonModule()._getOb(self.id1)
    p1.setRegion('europe/west/france')
    get_transaction().commit()
    self.tic()
   
    west = portal.portal_categories.resolveCategory('region/europe/west')
    west.setId("ouest")
    get_transaction().commit()
    self.tic()
    
    self.assertEqual(west,
      portal.portal_categories.resolveCategory('region/europe/ouest'))
    self.assertEqual(p1.getRegion(), 'europe/ouest/france')
    self.failUnless(p1 in west.getRegionRelatedValueList())

  def test_13b_RenameCategoryUsingCutAndPaste(self, quiet=0, run=run_all_test) :
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Category Renaming with cut n paste')
      LOG('Testing... ',0,'Category Renaming')
    
    portal = self.getPortal()
    france = portal.portal_categories.resolveCategory(
                                            'region/europe/west/france')
    self.assertNotEqual(france, None)
    
    p1 = self.getPersonModule()._getOb(self.id1)
    p1.setRegion('europe/west/france')
    get_transaction().commit()
    self.tic()
   
    europe = portal.portal_categories.resolveCategory('region/europe')
    west = europe.west
    cb_data = europe.manage_cutObjects(['west'])
    portal.portal_categories.region.manage_pasteObjects(cb_data)
    get_transaction().commit()
    self.tic()
    
    self.assertEqual(west,
      portal.portal_categories.resolveCategory('region/west'))
    self.assertEqual(p1.getRegion(), 'west/france')
    self.failUnless(p1 in west.getRegionRelatedValueList())
    
  def test_13c_RenameCategoryUsingCutAndPasteButNotCopy(
                                        self, quiet=0, run=run_all_test) :
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test Category Renaming with cut n paste, '
                          'copy n paste doesnt change')
      LOG('Testing... ',0,'Category Renaming')
    
    portal = self.getPortal()
    france = portal.portal_categories.resolveCategory(
                                    'region/europe/west/france')
    self.assertNotEqual(france, None)
    
    p1 = self.getPersonModule()._getOb(self.id1)
    p1.setRegion('europe/west/france')
    get_transaction().commit()
    self.tic()
   
    europe = portal.portal_categories.resolveCategory('region/europe')
    west = europe.west
    cb_data = europe.manage_copyObjects(['west'])
    portal.portal_categories.region.manage_pasteObjects(cb_data)
    get_transaction().commit()
    self.tic()
    
    self.assertEqual(west,
      portal.portal_categories.resolveCategory('region/europe/west'))
    self.assertEqual(p1.getRegion(), 'europe/west/france')
    # we are not member of the copy
    self.failUnless('west/france' not in p1.getRegionList())
    self.failUnless(p1 in west.getRegionRelatedValueList())
    

  def test_14_MultiplePortalTypes(self, quiet=0, run=run_all_test) :
    """ Checks that categories support different value per portal_type,
        like a colored graph on portal_type"""
    if not run: return
    if not quiet:
      message = 'Test multiple Portal Types for a same category'
      ZopeTestCase._print('\n '+message)
      LOG('Testing... ', 0, message)
    portal = self.getPortal()
    folder = self.getOrganisationModule()
    
    org_a = folder.newContent(portal_type='Organisation', id="org_a")
    org_b = folder.newContent(portal_type='Organisation', id="org_b")
    
    org_a.setDestinationValue(org_b)
    self.assertEqual(org_a.getDestinationValue(), org_b)

    pers_a = self.getPersonModule().newContent(
                  portal_type='Person', id='pers_a')
 
    for loop in range(3) :
      org_a.setDestinationValue(pers_a, portal_type='Person')
      self.assertEquals(
          org_a.getDestinationValue(portal_type='Person'), pers_a)
      self.assertEquals(
          org_a.getDestinationValue(portal_type='Organisation'), org_b)
      self.assertEquals(len(org_a.getDestinationValueList()), 2)
      
      org_a.setDestinationValue(org_b, portal_type='Organisation')
      self.assertEquals(
          org_a.getDestinationValue(portal_type='Person'), pers_a)
      self.assertEquals(
          org_a.getDestinationValue(portal_type='Organisation'), org_b)
      self.assertEquals(len(org_a.getDestinationValueList()), 2)

  def test_15_SortChildValues(self, quiet=0, run=run_all_test) :
    """ Checks on sorting child categories"""
    if not run: return
    if not quiet:
      message = 'Test Sort Child Values'
      ZopeTestCase._print('\n '+message)
      LOG('Testing... ', 0, message)
    
    pc = self.getCategoriesTool()
    bc = pc.newContent(portal_type='Base Category', id='sort_test')
    self.failUnless(bc is not None)
    bc.newContent(portal_type='Category', id='1', title='a', int_index=3)
    bc.newContent(portal_type='Category', id='2', title='b', int_index=1)
    bc.newContent(portal_type='Category', id='3', title='c', int_index=1)

    # simple sorting    
    category_list = bc.getCategoryChildValueList(sort_on='title')
    self.assertEquals(len(category_list), 3)
    self.assertEquals(category_list[0].getId(), '1')
    self.assertEquals(category_list[1].getId(), '2')
    self.assertEquals(category_list[2].getId(), '3')

    # reverse sorting
    category_list = bc.getCategoryChildValueList(sort_on='title', sort_order='reverse')
    self.assertEquals(len(category_list), 3)
    self.assertEquals(category_list[0].getId(), '3')
    self.assertEquals(category_list[1].getId(), '2')
    self.assertEquals(category_list[2].getId(), '1')

    # another reverse sorting
    category_list = bc.getCategoryChildValueList(sort_on=(('title', 'reverse'),))
    self.assertEquals(len(category_list), 3)
    self.assertEquals(category_list[0].getId(), '3')
    self.assertEquals(category_list[1].getId(), '2')
    self.assertEquals(category_list[2].getId(), '1')

    # multiple sort parameters
    category_list = bc.getCategoryChildValueList(sort_on=('int_index', 'title'))
    self.assertEquals(len(category_list), 3)
    self.assertEquals(category_list[0].getId(), '2')
    self.assertEquals(category_list[1].getId(), '3')
    self.assertEquals(category_list[2].getId(), '1')

    # another multiple sort parameters
    category_list = bc.getCategoryChildValueList(sort_on=(('int_index', 'reverse'), 'title'))
    self.assertEquals(len(category_list), 3)
    self.assertEquals(category_list[0].getId(), '1')
    self.assertEquals(category_list[1].getId(), '2')
    self.assertEquals(category_list[2].getId(), '3')
    
  def test_16_GetRelatedValues(self, quiet=0, run=run_all_test) :
    """ Checks on getting related values"""
    if not run: return
    if not quiet:
      message = 'Test Get Related Values'
      ZopeTestCase._print('\n '+message)
      LOG('Testing... ', 0, message)
    
    pc = self.getCategoriesTool()
    bc = pc.newContent(portal_type='Base Category', id='related_value_test')
    self.failUnless(bc is not None)
    get_transaction().commit()
    self.tic()
    # A newly created base category should be referred to only by itself
    value_list = pc.getRelatedValueList(bc)
    self.assertEquals(len(value_list), 1)
    
    c = bc.newContent(portal_type='Category', id='1')
    self.failUnless(c is not None)
    get_transaction().commit()
    self.tic()
    value_list = pc.getRelatedValueList(bc)
    # Now the base category should be referred to by itself and this sub category
    self.assertEquals(len(value_list), 2)
    # This sub category should be referred to only by itself
    value_list = pc.getRelatedValueList(c)
    self.assertEquals(len(value_list), 1)

  def test_17_CategoriesAndDomainSelection(self, quiet=0,
      run=run_all_test):
    """ Tests Categories and Domain Selection """
    if not run: return
    if not quiet:
      message = 'Test Domain Selection and Categories'
      ZopeTestCase._print('\n '+message)
      LOG('Testing... ', 0, message)
      
    category_tool = self.getCategoryTool()
    base = category_tool.newContent(portal_type = 'Base Category',
                                   id='test_base_cat')
    test = base.newContent(portal_type = 'Category', id = 'test_cat')
    base.recursiveReindexObject()
    obj = self.getOrganisationModule().newContent(
          portal_type = 'Organisation')
    obj.setCategoryList(['test_base_cat/test_cat'])
    get_transaction().commit()
    self.tic()
    self.assert_(obj in [x.getObject() for x in test.getCategoryMemberValueList()])

  def test_18_getCategoryList(self, quiet=0, run=run_all_test):
    """
    check that getCategoryList called on a category does not append self again
    and again
    """
    if not run: return
    if not quiet:
      message = 'Test getCategoryList on Category'
      ZopeTestCase._print('\n ' + message)
      LOG('Testing... ', 0, message)
    portal = self.getPortal()
    region_value = portal.portal_categories.resolveCategory('region/%s' % self.region1)
    category_list = region_value.getCategoryList()
    region_value.setCategoryList(category_list)
    self.assertEqual(category_list, region_value.getCategoryList())

if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestCMFCategory))
        return suite

