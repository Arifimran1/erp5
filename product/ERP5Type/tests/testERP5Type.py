#
# Skeleton ZopeTestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Needed in order to have a log file inside the current folder
os.environ['EVENT_LOG_FILE'] = os.path.join(os.getcwd(), 'zLOG.log')
os.environ['EVENT_LOG_SEVERITY'] = '-300'

from random import randint
from Testing import ZopeTestCase
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from zLOG import LOG

class TestERP5Type(ERP5TypeTestCase):

    # Some helper methods

    def getTitle(self):
      return "ERP5Type"

    def getBusinessTemplateList(self):
      """
        Return the list of business templates.
      """
      return ('erp5_base',)

    def afterSetUp(self):
      self.login()

    def getRandomString(self):
      return str(randint(-10000000,100000000))

    def getTemplateTool(self):
      return getattr(self.getPortal(), 'portal_templates', None)

    def getCategoryTool(self):
      return getattr(self.getPortal(), 'portal_categories', None)

    def getTypeTool(self):
      return getattr(self.getPortal(), 'portal_types', None)

    # Here are the tests
    def testHasTemplateTool(self):
      # Test if portal_templates was created
      self.failUnless(self.getTemplateTool()!=None)

    def testHasCategoryTool(self):
      # Test if portal_categories was created
      self.failUnless(self.getCategoryTool()!=None)

    def testTemplateToolHasGetId(self):
      # Test if portal_templates has getId method (RAD)
      self.failUnless(self.getTemplateTool().getId() == 'portal_templates')

    def testCategoryToolHasGetId(self):
      # Test if portal_categories has getId method (RAD)
      self.failUnless(self.getCategoryTool().getId() == 'portal_categories')

    # erp5_common tests
    def testCommonHasParentBaseCategory(self):
      # Test if erp5_common parent base category was imported successfully
      self.failUnless(getattr(self.getCategoryTool(), 'parent', None) != None)

    def testCommonHasImageType(self):
      # Test if erp5_common parent base category was imported successfully
      self.failUnless(getattr(self.getTypeTool(), 'Image', None) != None)

    # Business Template Tests
    def testBusinessTemplate(self):
      # Create a business template and test if portal_type matches
      # Make a extension tests on basic accessors
      portal_templates = self.getTemplateTool()
      business_template = self.getTemplateTool().newContent(portal_type="Business Template") # Fails Why ?
                                                                               # may be because there is
                                                                               # no "Business Template"
                                                                               # in portal_types, it may
                                                                               # be added to erp5_common
      self.failUnless(business_template.getPortalType() == 'Business Template')
      # Test simple string accessor
      test_string = self.getRandomString()
      business_template.setTitle(test_string)
      self.failUnless(business_template.getTitle()==test_string)
    
    # Test Dynamic Code Generation
    def test_01_AqDynamic(self):
      portal = self.getPortal()
      #module = portal.person
      from Products.ERP5Type.Base import initializeClassDynamicProperties
      from Products.ERP5Type.Base import initializePortalTypeDynamicProperties
      from Products.ERP5Type.Base import Base
      from Products.ERP5Type import Document
      initializeClassDynamicProperties(portal, Base)
      # Base class should now have a state method
      #self.failUnless(hasattr(Base, 'getFirstName'))
    
    def test_02_AqDynamic(self):
      portal = self.getPortal()
      module = self.getPersonModule()
      person = module.newContent(id='1', portal_type='Person')
      from Products.ERP5Type import Document
      # Person class should have no method getFirstName
      self.failUnless(not hasattr(Document.Person, 'getFirstName'))
      # Calling getFirstName should produce dynamic methods related to the portal_type
      name = person.getFirstName()
      # Person class should have no method getFirstName
      self.failUnless(not hasattr(Document.Person, 'getFirstName'))
      # Person class should now have method getFirstName
      self.failUnless(hasattr(person, 'getFirstName'))

    def test_03_NewTempObject(self):
      portal = self.getPortal()

      from Products.ERP5Type.Document import newTempPerson
      o = newTempPerson(portal, 1.2)
      o.setTitle('toto')
      self.assertEquals(o.getTitle(), 'toto')
      self.assertEquals(str(o.getId()), str(1.2))

      from Products.ERP5Type.Document import newTempOrganisation
      o = newTempOrganisation(portal, -123)
      o.setTitle('toto')
      self.assertEquals(o.getTitle(), 'toto')
      self.assertEquals(str(o.getId()), str(-123))

      # Try to edit with any property and then get it with getProperty
      o = newTempOrganisation(portal,'a') 
      o.edit(tutu='toto')
      self.assertEquals(o.getProperty('tutu'), 'toto')

      # Same thing with an integer
      o = newTempOrganisation(portal,'b') 
      o.edit(tata=123)
      self.assertEquals(o.getProperty('tata'), 123)

    def test_04_CategoryAccessors(self):
      portal = self.getPortal()
      region_category = self.getPortal().portal_categories.region
      
      category_title = "Solar System"
      category_id = "solar_system"
      category_object = region_category.newContent(
              portal_type = "Category",
              id = category_id,
              title = category_title, )
      category_relative_url = category_object.getRelativeUrl()
      
      person_title = "Toto"
      person_id = "toto"
      person_object = self.getPersonModule().newContent(
              portal_type = "Person",
              id = person_id,
              title = person_title,)
      person_relative_url = person_object.getRelativeUrl()
      
      def checkRelationSet(self):
        get_transaction().commit()
        person_object.reindexObject()
        category_object.reindexObject()
        self.tic()
        self.assertEquals( person_object.getRegion(), category_relative_url)
        self.assertEquals( person_object.getRegionValue(), category_object)
        self.assertEquals( person_object.getRegionId(), category_id)
        self.assertEquals( person_object.getRegionTitle(), category_title)
        self.assertEquals( category_object.getRegionRelatedValueList(
                            portal_type = "Person"), [person_object] )
        self.assertEquals( category_object.getRegionRelatedTitleList(
                            portal_type = "Person"), [person_title] )
        self.assertEquals( category_object.getRegionRelatedList(
                            portal_type = "Person"), [person_relative_url] )
        self.assertEquals( category_object.getRegionRelatedIdList(
                            portal_type = "Person"), [person_id] )
      def checkRelationUnset(self):
        get_transaction().commit()
        person_object.reindexObject()
        category_object.reindexObject()
        self.tic()
        self.assertEquals( person_object.getRegion(), None)
        self.assertEquals( person_object.getRegionValue(), None)
        self.assertEquals( person_object.getRegionId(), None)
        self.assertEquals( person_object.getRegionTitle(), None)
        self.assertEquals( category_object.getRegionRelatedValueList(
                            portal_type = "Person"), [] )
        self.assertEquals( category_object.getRegionRelatedTitleList(
                            portal_type = "Person"), [] )
        self.assertEquals( category_object.getRegionRelatedList(
                            portal_type = "Person"), [] )
        self.assertEquals( category_object.getRegionRelatedIdList(
                            portal_type = "Person"), [] )
      
      person_object.setRegion(category_relative_url)
      checkRelationSet(self)
      person_object.setRegion(None)
      checkRelationUnset(self)
      person_object.setRegionValue(category_object)
      checkRelationSet(self)
      person_object.setRegionValue(None)
      checkRelationUnset(self)
      
    def test_04_setProperty(self):
      portal = self.getPortal()
      module = self.getOrganisationModule()
      organisation = module.newContent(id='1', portal_type='Organisation')
      organisation.setDefaultTelephoneText('55 55 5555')
      organisation.setCorporateName('Nexedi')
      organisation.default_telephone.setProperty('corporate_name','Toto')
      self.assertEquals(organisation.corporate_name,'Nexedi')
      self.assertEquals(organisation.default_telephone.corporate_name,'Toto')

    def test_06_CachingMethod(self):
      """Tests Caching methods."""
      cached_var1 = cached_var1_orig = 'cached_var1'
      cached_var2 = cached_var2_orig = 'cached_var2'

      def _cache1():
        return cached_var1
      def _cache2():
        return cached_var2
      
      from Products.ERP5Type.Cache import CachingMethod, clearCache
      cache1 = CachingMethod(_cache1, id='_cache1')
      cache2 = CachingMethod(_cache2, id='_cache2')
      
      self.assertEquals(cache1(), cached_var1)
      self.assertEquals(cache2(), cached_var2)
      
      cached_var1 = 'cached_var1 (modified)'
      cached_var2 = 'cached_var2 (modified)'
      self.assertEquals(cache1(), cached_var1_orig)
        
      # clearCache with a method argument only clear this cache
      clearCache(method_id = '_cache1')
      self.assertEquals(cache1(), cached_var1)
      self.assertEquals(cache2(), cached_var2_orig)
      
      # clearCache with no arguments clear all caches
      clearCache()
      self.assertEquals(cache2(), cached_var2)

    def test_afterCloneScript(self):
      """manage_afterClone can call a type based script."""
      # setup the script for Person portal type
      custom_skin = self.getPortal().portal_skins.custom
      method_id = 'Person_afterClone'
      if method_id in custom_skin.objectIds():
        custom_skin.manage_delObjects([method_id])
      
      custom_skin.manage_addProduct['PythonScripts']\
                    .manage_addPythonScript(id = method_id)
      script = custom_skin[method_id]
      script.ZPythonScript_edit('', "context.setTitle('reseted')")
      self.getPortal().changeSkin(None)
    
      # copy / pasted person have their title reseted
      folder = self.getPersonModule()
      pers = folder.newContent(portal_type='Person',
                              title='something', )
      copy_data = folder.manage_copyObjects([pers.getId()])
      new_id = folder.manage_pasteObjects(copy_data)[0]['new_id']
      new_pers = folder[new_id]
      self.assertEquals(new_pers.getTitle(), 'reseted')
      
      # we can even change subobjects in the script
      if not hasattr(pers, 'default_address'):
        pers.newContent(portal_type='Address', id='default_address')
      pers.default_address.setTitle('address_title')
      # modify script to update subobject title
      script.ZPythonScript_edit('',
          "context.default_address.setTitle('address_title_reseted')")
      copy_data = folder.manage_copyObjects([pers.getId()])
      new_id = folder.manage_pasteObjects(copy_data)[0]['new_id']
      new_pers = folder[new_id]
      self.assertEquals(new_pers.default_address.getTitle(),
                        'address_title_reseted')
      
      # of course, other portal types are not affected
      folder = self.getOrganisationModule()
      orga = folder.newContent(portal_type='Organisation',
                              title='something', )
      copy_data = folder.manage_copyObjects([orga.getId()])
      new_id = folder.manage_pasteObjects(copy_data)[0]['new_id']
      new_orga = folder[new_id]
      self.assertEquals(new_orga.getTitle(), 'something')
      

if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestERP5Type))
        return suite
