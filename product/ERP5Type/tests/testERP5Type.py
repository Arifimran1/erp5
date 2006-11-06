
import os
import sys
import md5
if __name__ == '__main__':
  execfile(os.path.join(sys.path[0], 'framework.py'))

# Needed in order to have a log file inside the current folder
os.environ['EVENT_LOG_FILE'] = os.path.join(os.getcwd(), 'zLOG.log')
os.environ['EVENT_LOG_SEVERITY'] = '-300'

from random import randint
from Testing import ZopeTestCase
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from zLOG import LOG, INFO
from Products.CMFCore.tests.base.testcase import LogInterceptor
from Products.ERP5Type.Cache import CachingMethod, clearCache
from Products.ERP5Type.Base import _aq_reset
from Products.ERP5Type.tests.utils import installRealClassTool
from Products.ERP5Type.Utils import removeLocalPropertySheet

class PropertySheetTestCase(ERP5TypeTestCase):
  """Base test case class for property sheets tests.
  Inherits from this class to get methods to easily add new property sheets,
  constraints and documents in tests.

  TODO : only property sheets are supported at this time.
  """
  def setUp(self):
    """Set up the fixture. """
    ERP5TypeTestCase.setUp(self)
    installRealClassTool(self.getPortal())
    # keep a mapping type info name -> property sheet list, to remove them in
    # tear down.
    self._added_property_sheets = {}

  def tearDown(self):
    """Clean up """
    ttool = self.getTypesTool()
    class_tool = self.getClassTool()
    # remove all property sheet we added to type informations
    for ti_name, psheet_list in self._added_property_sheets.items():
      ti = ttool.getTypeInfo(ti_name)
      ps_list = ti.property_sheet_list
      for psheet in psheet_list:
        if psheet in ps_list:
          ps_list.remove(psheet)
          # physically remove property sheet, otherwise invalid property sheet
          # could break next tests.
          removeLocalPropertySheet(psheet)
      ti.property_sheet_list = ps_list
    _aq_reset()
    ERP5TypeTestCase.tearDown(self)
    
  def _addProperty(self, portal_type_name, property_definition_code):
    """quickly add a property to a type information."""
    m = md5.new()
    m.update(portal_type_name + property_definition_code)
    property_sheet_name = 'TestPS%s' % m.hexdigest()
    property_sheet_code = """
from Products.CMFCore.Expression import Expression
class %(property_sheet_name)s:
  _properties = ( %(property_definition_code)s, )
""" % locals()
    self._addPropertySheet(portal_type_name,
                           property_sheet_code,
                           property_sheet_name)

  def _addPropertySheet(self, portal_type_name, property_sheet_code,
                       property_sheet_name='TestPropertySheet'):
    """Utility method to add a property sheet to a type information.
    You might be interested in the higer level method _addProperty
    This method registers all added property sheets, to be able to remove
    them in tearDown.
    """
    # install the 'real' class tool
    class_tool = self.getClassTool()

    class_tool.newPropertySheet(property_sheet_name)
    class_tool.editPropertySheet(property_sheet_name, property_sheet_code)
    class_tool.importPropertySheet(property_sheet_name)
    
    # We set the property sheet on the portal type
    ti = self.getTypesTool().getTypeInfo(portal_type_name)
    ti.property_sheet_list = list(ti.property_sheet_list) +\
                                [property_sheet_name]
    # remember that we added a property sheet for tear down
    self._added_property_sheets.setdefault(
                portal_type_name, []).append(property_sheet_name)
    # reset aq_dynamic cache
    _aq_reset()

class TestERP5Type(PropertySheetTestCase, LogInterceptor):

    run_all_test = 1
    quiet = 1

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

    def beforeTearDown(self):
      for module in [ self.getPersonModule(),
                      self.getOrganisationModule(),
                      self.getCategoryTool().region ]:
        module.manage_delObjects(list(module.objectIds()))
      get_transaction().commit()

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
      business_template = self.getTemplateTool().newContent(
                            portal_type="Business Template")
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
      # self.failUnless(hasattr(Base, 'getFirstName'))
      # This test is now useless since methods are portal type based
    
    def test_02_AqDynamic(self):
      portal = self.getPortal()
      module = self.getPersonModule()
      person = module.newContent(id='1', portal_type='Person')
      from Products.ERP5Type import Document
      # Person class should have no method getFirstName
      self.failUnless(not hasattr(Document.Person, 'getFirstName'))
      # Calling getFirstName should produce dynamic methods related to the
      # portal_type
      name = person.getFirstName()
      # Person class should have no method getFirstName
      self.failUnless(not hasattr(Document.Person, 'getFirstName'))
      # Person class should now have method getFirstName
      self.failUnless(hasattr(person, 'getFirstName'))

    def test_03_NewTempObject(self, quiet=quiet, run=run_all_test):
      if not run: return
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

      # Make sure this is a Temp Object
      self.assertEquals(o.isTempObject(), 1)

      # Create a subobject and make sure it is a Temp Object
      a = o.newContent(portal_type = 'Telephone')      
      self.assertEquals(a.isTempObject(), 1)

      # Test newContent with the temp_object parameter
      o = portal.person_module.newContent(id=987, portal_type="Person", temp_object=1)
      o.setTitle('bar')
      self.assertEquals(o.getTitle(), 'bar')
      self.assertEquals(str(o.getId()), str(987))
      self.assertEquals(o.isTempObject(), 1)
      a = o.newContent(id=1, portal_type="Telephone", temp_object=1)
      self.assertEquals(str(a.getId()), str(1))
      self.assertEquals(a.isTempObject(), 1)
      b = o.newContent(id=2, portal_type="Telephone")
      self.assertEquals(b.isTempObject(), 1)
      self.assertEquals(b.getId(), str(2))
      

    def test_04_CategoryAccessors(self, quiet=quiet, run=run_all_test):
      """
        This test provides basic testing of category
        accessors using the region base category.

        setRegion (with base = 0 or base =1)
        setRegionValue
        getRegion
        getRegionId
        getRegionTitle
        getRegionRelatedList
        getRegionRelatedValueList
        getRegionRelatedIdList
        getRegionRelatedTitleList

        This tests also makes sure that the related accessors are
        compatible with acquisition of category. Although region
        is not defined on a Person, Person documents are member
        of a region and should thus be accessible from the region
        category through getRegionRelated accessors
      """
      if not run: return
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
        self.assertEquals( person_object.getRegion(), category_id)
        self.assertEquals( person_object.getRegion(base=1), category_relative_url)
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

      # Test setRegion in default mode (base = 0)
      person_object.setRegion(category_id)
      checkRelationSet(self)
      person_object.setRegion(None)
      checkRelationUnset(self)
      # Test setRegion in default mode (base = 1)
      person_object.setRegion(category_relative_url, base=1)
      checkRelationSet(self)
      person_object.setRegion(None)
      checkRelationUnset(self)
      # Test setRegion in value mode
      person_object.setRegionValue(category_object)
      checkRelationSet(self)
      person_object.setRegionValue(None)
      checkRelationUnset(self)
      
    def test_05_setProperty(self, quiet=quiet, run=run_all_test):
      """
        In this test we create a subobject (ie. a phone number)
        and show the difference between calling getProperty and
        an accessor.

        Accessors can be acquired thus returning a property value
        defined on a parent object whereas getProperty / setProperty
        always act at the level of the object itself.

        We also do some basic tests on the telephone number parser

        XXX I think this is inconsistent because it prevents from
        using getProperty / setProperty as a generic way to use
        accessors from subobjects.
      """
      if not run: return
      portal = self.getPortal()
      module = self.getOrganisationModule()
      organisation = module.newContent(id='1', portal_type='Organisation')
      organisation.setDefaultTelephoneText('+55(0)66-5555')
      self.assertEquals(organisation.default_telephone.getTelephoneCountry(),'55')
      self.assertEquals(organisation.default_telephone.getTelephoneArea(),'66')
      self.assertEquals(organisation.default_telephone.getTelephoneNumber(),'5555')
      organisation.setCorporateName('Nexedi')
      #self.assertEquals(organisation.default_telephone.getProperty('corporate_name'),'Nexedi') # Who is right ? XXX
      organisation.default_telephone.setProperty('corporate_name','Toto')
      self.assertEquals(organisation.corporate_name,'Nexedi')
      self.assertEquals(organisation.default_telephone.getCorporateName(),'Nexedi')
      self.assertEquals(organisation.default_telephone.corporate_name,'Toto')
      self.assertEquals(organisation.default_telephone.getProperty('corporate_name'),'Toto')

    def test_06_CachingMethod(self, quiet=quiet, run=run_all_test):
      """Tests Caching methods."""
      if not run: return
      cached_var = cached_var_orig = 'cached_var1'

      def _cache():
        return cached_var
      
      from Products.ERP5Type.Cache import CachingMethod, clearCache
      cache1 = CachingMethod(_cache, id='testing_cache')
      
      self.assertEquals(cache(), cached_var)
      
      # change the variable
      cached_var = 'cached_var (modified)'
      # cache hit -> still the old variable
      self.assertEquals(cache(), cached_var_orig)
        
      clearCache()
      self.assertEquals(cache(), cached_var)

    def test_07_afterCloneScript(self, quiet=quiet, run=run_all_test):
      """manage_afterClone can call a type based script."""
      if not run: return
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
      
    def test_08_AccessorGeneration(self, quiet=quiet, run=run_all_test):
      """Tests accessor generation doesn't generate error messages.
      """
      if not run: return
      from Products.ERP5Type.Base import _aq_reset
      _aq_reset()
      self._catch_log_errors(ignored_level=INFO)
      folder = self.getOrganisationModule()
      orga = folder.newContent(portal_type='Organisation',)
      # call an accessor, _aq_dynamic will generate accessors
      orga.getId()
      self._ignore_log_errors()
    
    def test_09_RenameObjects(self, quiet=quiet, run=run_all_test):
      """Test object renaming.

         As we overloaded some parts of OFS, it's better to test again some basic
         features.
      """
      if not run: return
      folder = self.getOrganisationModule()
      id_list = [chr(x) for x in range(ord('a'), ord('z')+1)]
      for id_ in id_list:
        folder.newContent(portal_type='Organisation', id=id_)
      # commit a subtransaction, so that we can rename objecs (see
      # OFS.ObjectManager._getCopy)
      get_transaction().commit(1)

      for obj in folder.objectValues():
        new_id = '%s_new' % obj.getId()
        folder.manage_renameObjects([obj.getId()], [new_id])
        self.assertEquals(obj.getId(), new_id)

      for obj_id in folder.objectIds():
        self.failUnless(obj_id.endswith('_new'),
                        'bad object id: %s' % obj_id)
      for id_ in id_list:
        new_id = '%s_new' % id_
        self.assertEquals(folder._getOb(new_id).getId(), new_id)

    def test_10_ConstraintNotFound(self, quiet=quiet, run=run_all_test):
      """
      When a Constraint is not found while importing a PropertySheet,
      AttributeError was raised, and generated a infinite loop.
      This is a test to make sure this will not happens any more
      """
      if not run: return
      text = """
class TestPropertySheet:
    \"\"\"
        TestPropertySheet for this unit test
    \"\"\"

    _properties = (
        {   'id'          : 'strange_property',
            'description' : 'A local property description',
            'type'        : 'string',
            'mode'        : '' },
      )

    _constraints = (
        { 'id'            : 'toto',
          'description'   : 'define a bad constraint',
          'type'          : 'TestConstraintNotFoundClass',
        },
      )

"""
      self._addPropertySheet('Organisation', text)
      folder = self.getOrganisationModule()
      # We check that we raise exception when we create new object
      from Products.ERP5Type.Utils import ConstraintNotFound
      organisation =  self.assertRaises(ConstraintNotFound, folder.newContent,
                                        portal_type='Organisation')

    def test_11_valueAccessor(self, quiet=quiet, run=run_all_test):
      """
        The purpose of this test is to make sure that category accessors
        work as expected.

        List accessors support ordering and multiple entries
        but they are incompatible with default value

        Set accessors preserve the default value but
        they do not preserver order or multiple entries

        The test is implemented for both Category and Value
        accessors.
      """
      if not run: return

      if not quiet:
        message = 'Test Category setters'
        ZopeTestCase._print('\n '+message)
        LOG('Testing... ', 0, message)

      # Create a few categories
      region_category = self.getPortal().portal_categories.region
      alpha = region_category.newContent(
              portal_type = "Category",
              id =          "alpha",
              title =       "Alpha System", )
      beta = region_category.newContent(
              portal_type = "Category",
              id =          "beta",
              title =       "Beta System", )
      zeta = region_category.newContent(
              portal_type = "Category",
              id =          "zeta",
              title =       "Zeta System", )
      function_category = self.getPortal().portal_categories.function
      nofunction = function_category.newContent(
              portal_type = "Category",
              id =          "nofunction",
              title =       "No Function", )

      self.assertEquals(alpha.getRelativeUrl(), 'region/alpha')

      alpha.reindexObject()
      beta.reindexObject()
      zeta.reindexObject()
      nofunction.reindexObject()
      get_transaction().commit()
      self.tic() # Make sure categories are reindexed

      # Create a new person
      module = self.getPersonModule()
      person = module.newContent(portal_type='Person')

      # Value setters (list, set, default)
      person.setFunction('nofunction')  # Fill at least one other category
      person.setDefaultRegionValue(alpha)
      self.assertEquals(person.getDefaultRegion(), 'alpha')
      self.assertEquals(person.getRegion(), 'alpha')
      person.setRegionValue(alpha)
      self.assertEquals(person.getRegion(), 'alpha')
      person.setRegionValueList([alpha, alpha])
      self.assertEquals(person.getRegionList(), ['alpha', 'alpha'])
      person.setRegionValueSet([alpha, alpha])
      self.assertEquals(person.getRegionSet(), ['alpha'])
      person.setRegionValueList([alpha, beta, alpha])
      self.assertEquals(person.getRegionList(), ['alpha', 'beta', 'alpha'])
      person.setRegionValueSet([alpha, beta, alpha])
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      person.setDefaultRegionValue(beta)
      self.assertEquals(person.getDefaultRegion(), 'beta')
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      self.assertEquals(person.getRegionList(), ['beta', 'alpha'])
      person.setDefaultRegionValue(alpha)
      self.assertEquals(person.getDefaultRegion(), 'alpha')
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      self.assertEquals(person.getRegionList(), ['alpha', 'beta'])
      # Test accessor on documents rather than on categories
      person.setDefaultRegionValue(person)
      self.assertEquals(person.getDefaultRegion(), person.getRelativeUrl())
      self.assertEquals(person.getRegionList(), [person.getRelativeUrl(), 'alpha', 'beta'])
      person.setRegionValue([person, alpha, beta])
      self.assertEquals(person.getRegionList(), [person.getRelativeUrl(), 'alpha', 'beta'])

      # Category setters (list, set, default)
      person = module.newContent(portal_type='Person')
      person.setFunction('nofunction')  # Fill at least one other category
      person.setDefaultRegion('alpha')
      self.assertEquals(person.getRegion(), 'alpha')
      self.assertEquals(person.getDefaultRegion(), 'alpha')
      person.setRegion('alpha')
      self.assertEquals(person.getRegion(), 'alpha')
      person.setRegionList(['alpha', 'alpha'])
      self.assertEquals(person.getRegionList(), ['alpha', 'alpha'])
      person.setRegionSet(['alpha', 'alpha'])
      self.assertEquals(person.getRegionSet(), ['alpha'])
      person.setRegionList(['alpha', 'beta', 'alpha'])
      self.assertEquals(person.getRegionList(), ['alpha', 'beta', 'alpha'])
      person.setRegionSet(['alpha', 'beta', 'alpha'])
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      person.setDefaultRegion('beta')
      self.assertEquals(person.getDefaultRegion(), 'beta')
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      self.assertEquals(person.getRegionList(), ['beta', 'alpha'])
      person.setDefaultRegion('alpha')
      self.assertEquals(person.getDefaultRegion(), 'alpha')
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      self.assertEquals(person.getRegionList(), ['alpha', 'beta'])
      # Test accessor on documents rather than on categories
      person.setDefaultRegion(person.getRelativeUrl())
      self.assertEquals(person.getDefaultRegion(), person.getRelativeUrl())
      self.assertEquals(person.getRegionList(), [person.getRelativeUrl(), 'alpha', 'beta'])
      person.setRegion([person.getRelativeUrl(), 'alpha', 'beta'])
      self.assertEquals(person.getRegionList(), [person.getRelativeUrl(), 'alpha', 'beta'])

      # Uid setters (list, set, default)
      person = module.newContent(portal_type='Person')
      person.reindexObject()
      get_transaction().commit()
      self.tic() # Make sure person is reindexed
      person.setFunction('nofunction')  # Fill at least one other category
      person.setDefaultRegionUid(alpha.getUid())
      self.assertEquals(person.getRegion(), 'alpha')
      self.assertEquals(person.getDefaultRegion(), 'alpha')
      person.setRegionUid(alpha.getUid())
      self.assertEquals(person.getRegion(), 'alpha')
      person.setRegionUidList([alpha.getUid(), alpha.getUid()])
      self.assertEquals(person.getRegionList(), ['alpha', 'alpha'])
      person.setRegionUidSet([alpha.getUid(), alpha.getUid()])
      self.assertEquals(person.getRegionSet(), ['alpha'])
      person.setRegionUidList([alpha.getUid(), beta.getUid(), alpha.getUid()])
      self.assertEquals(person.getRegionList(), ['alpha', 'beta', 'alpha'])
      person.setRegionUidSet([alpha.getUid(), beta.getUid(), alpha.getUid()])
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      person.setDefaultRegionUid(beta.getUid())
      self.assertEquals(person.getDefaultRegion(), 'beta')
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      self.assertEquals(person.getRegionList(), ['beta', 'alpha'])
      person.setDefaultRegionUid(alpha.getUid())
      self.assertEquals(person.getDefaultRegion(), 'alpha')
      result = person.getRegionSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      self.assertEquals(person.getRegionList(), ['alpha', 'beta'])
      # Test accessor on documents rather than on categories
      person.setDefaultRegionUid(person.getUid())
      self.assertEquals(person.getDefaultRegion(), person.getRelativeUrl())
      self.assertEquals(person.getRegionList(), [person.getRelativeUrl(), 'alpha', 'beta'])
      person.setRegionUid([person.getUid(), alpha.getUid(), beta.getUid()])
      self.assertEquals(person.getRegionList(), [person.getRelativeUrl(), 'alpha', 'beta'])

    def test_12_listAccessor(self, quiet=quiet, run=run_all_test):
      """
      The purpose of this test is to make sure that accessor for
      sequence types support the same kind of semantics as the
      one on categories. We use 'subject' of the DublinCore propertysheet
      on organisation documents for this test.
      """
      if not run: return

      if not quiet:
        message = 'Test Category setters'
        ZopeTestCase._print('\n '+message)
        LOG('Testing... ', 0, message)

      # Create a new person
      module = self.getPersonModule()
      person = module.newContent(portal_type='Person')

      # Do the same tests as in test_11_valueAccessor 
      person.setSubject('alpha')
      self.assertEquals(person.getSubject(), 'alpha')
      person.setSubjectList(['alpha', 'alpha'])
      self.assertEquals(person.getSubjectList(), ['alpha', 'alpha'])
      person.setSubjectSet(['alpha', 'alpha'])
      self.assertEquals(person.getSubjectSet(), ['alpha'])
      person.setSubjectList(['alpha', 'beta', 'alpha'])
      self.assertEquals(person.getSubjectList(), ['alpha', 'beta', 'alpha'])
      person.setSubjectSet(['alpha', 'beta', 'alpha'])
      result = person.getSubjectSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      person.setDefaultSubject('beta')
      self.assertEquals(person.getDefaultSubject(), 'beta')
      result = person.getSubjectSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      self.assertEquals(person.getSubjectList(), ['beta', 'alpha'])
      person.setDefaultSubject('alpha')
      self.assertEquals(person.getDefaultSubject(), 'alpha')
      result = person.getSubjectSet()
      result.sort()
      self.assertEquals(result, ['alpha', 'beta'])
      self.assertEquals(person.getSubjectList(), ['alpha', 'beta'])

    def test_13_acquiredAccessor(self, quiet=quiet, run=run_all_test):
      """
      The purpose of this test is to make sure that accessor for
      sequence types support the same kind of semantics as the
      one on categories. We use 'subject' of the DublinCore propertysheet
      on organisation documents for this test.
      """

      # If address is updated on subordination, then
      # address is updated on person

      # If address is changed on person, it rem

      # If address not available on one organisation
      # it is found on the mapping related organisation
      # which is one step higher in the site 
      pass

    def test_14_bangAccessor(self, quiet=quiet, run=run_all_test):
      """
      Bang accesors must be triggered each time another accessor is called
      They are useful for centralising events ?
      """
      pass

    def test_15_DefaultValue(self):
      """
      Tests that the default value is returned correctly
      """
      portal = self.getPortal()
      module = self.getPersonModule()
      person = module.newContent(id='1', portal_type='Person')
      
      def getFirstName(default=None):
        "dummy method to check default is passed correctly"
        return default

      person.getFirstName = getFirstName

      # test static method
      self.assertEquals(person.getFirstName(), None)
      self.assertEquals(person.getFirstName('foo'), 'foo')
      self.assertEquals(person.getFirstName(default='foo'), 'foo')
      # test dynamic method
      self.assertEquals(person.getLastName(), None)
      self.assertEquals(person.getLastName('foo'), 'foo')
      #self.assertEquals(person.getLastName(default='foo'), 'foo')
      # test static method through getProperty
      self.assertEquals(person.getProperty('first_name'), None)
      self.assertEquals(person.getProperty('first_name', 'foo'), 'foo')
      self.assertEquals(person.getProperty('first_name', d='foo'), 'foo')
      # test dynamic method through getProperty
      self.assertEquals(person.getProperty('last_name'), None)
      self.assertEquals(person.getProperty('last_name', 'foo'), 'foo')
      self.assertEquals(person.getProperty('last_name', d='foo'), 'foo')
      # test simple property through getProperty
      property_name = 'XXXthis_property_does_not_exist123123'
      self.assertEquals(person.getProperty(property_name), None)
      self.assertEquals(person.getProperty(property_name, 'foo'), 'foo')
      self.assertEquals(person.getProperty(property_name, d='foo'), 'foo')

    def test_15b_DefaultValueDefinedOnPropertySheet(self):
      """Tests that the default value is returned correctly when a default
      value is defined using the property sheet.
      """
      self._addProperty('Person', '''{'id': 'dummy_ps_prop',
                                      'type': 'string',
                                      'mode': 'w',
                                      'default': 'ps_default',}''')
      module = self.getPersonModule()
      person = module.newContent(id='1', portal_type='Person')
      # The default ps value will be returned, when using generated accessor
      self.assertEquals('ps_default', person.getDummyPsProp())
      # (unless you explicitly pass a default value.
      self.assertEquals('default', person.getDummyPsProp('default'))
      # using getProperty
      self.assertEquals('ps_default', person.getProperty('dummy_ps_prop'))
      self.assertEquals('default', person.getProperty('dummy_ps_prop', 'default'))

      # None can be a default value too
      self.assertEquals(None, person.getProperty('dummy_ps_prop', None))
      self.assertEquals(None, person.getDummyPsProp(None))
      
      # once the value has been set, there's no default
      value = 'a value'
      person.setDummyPsProp(value)
      self.assertEquals(value, person.getDummyPsProp())
      self.assertEquals(value, person.getDummyPsProp('default'))
      self.assertEquals(value, person.getProperty('dummy_ps_prop'))
      self.assertEquals(value, person.getProperty('dummy_ps_prop', d='default'))

    def test_16_SimpleStringAccessor(self):
      """Tests a simple string accessor.
      This is also a way to test _addProperty method """
      self._addProperty('Person', '''{'id': 'dummy_ps_prop',
                                      'type': 'string',
                                      'mode': 'w',}''')
      person = self.getPersonModule().newContent(id='1', portal_type='Person')
      self.assertEquals('string', person.getPropertyType('dummy_ps_prop'))
      self.failUnless(hasattr(person, 'getDummyPsProp'))
      self.failUnless(hasattr(person, 'setDummyPsProp'))
      person.setDummyPsProp('a value')
      self.failUnless(person.hasProperty('dummy_ps_prop'))
      self.assertEquals('a value', person.getDummyPsProp())

    def test_17_WorkflowStateAccessor(self):
      """Tests for workflow state. assumes that validation state is chained to
      the Person portal type and that this workflow has 'validation_state' as
      state_variable.
      """
      person = self.getPersonModule().newContent(id='1', portal_type='Person')
      wf = self.getWorkflowTool().validation_workflow
      # those are assumptions for this test.
      self.failUnless(wf.getId() in
                        self.getWorkflowTool().getChainFor('Person'))
      self.assertEquals('validation_state', wf.variables.getStateVar())
      initial_state = wf.states[wf.initial_state]
      other_state = wf.states['validated']

      self.failUnless(hasattr(person, 'getValidationState'))
      self.failUnless(hasattr(person, 'getValidationStateTitle'))
      self.failUnless(hasattr(person, 'getTranslatedValidationStateTitle'))

      self.assertEquals(initial_state.getId(), person.getValidationState())
      self.assertEquals(initial_state.title,
                        person.getValidationStateTitle())
      # XXX we do not have translation system set up at that point
      self.assertEquals(initial_state.title,
                        person.getTranslatedValidationStateTitle())
      
      self.assertEquals(initial_state.getId(),
                        person.getProperty('validation_state'))
      self.assertEquals(initial_state.title,
                        person.getProperty('validation_state_title'))
      # XXX we do not have translation system set up at that point
      self.assertEquals(initial_state.title,
                        person.getProperty('translated_validation_state_title'))
      
      # default parameter is accepted by getProperty for compatibility
      self.assertEquals(initial_state.getId(),
                        person.getProperty('validation_state', 'default'))
      self.assertEquals(initial_state.title,
                        person.getProperty('validation_state_title', 'default'))
      # XXX we do not have translation system set up at that point
      self.assertEquals(initial_state.title,
                        person.getProperty('translated_validation_state_title',
                        'default'))

      # pass a transition and check accessors again.
      person.validate()
      self.assertEquals(other_state.getId(), person.getValidationState())
      self.assertEquals(other_state.title,
                        person.getValidationStateTitle())
      self.assertEquals(other_state.title,
                        person.getTranslatedValidationStateTitle())
      self.assertEquals(other_state.getId(),
                        person.getProperty('validation_state'))
      self.assertEquals(other_state.title,
                        person.getProperty('validation_state_title'))
      self.assertEquals(other_state.title,
                        person.getProperty('translated_validation_state_title'))
    
    DEFAULT_ORGANISATION_TITLE_PROP = '''
                      { 'id':         'organisation',
                        'storage_id': 'default_organisation',
                        'type':       'content',
                        'portal_type': ('Organisation', ),
                        'acquired_property_id': ('title', ),
                        'mode':       'w', }'''

    def test_18_SimpleContentAccessor(self):
      """Tests a simple content accessor.
      """
      # For testing purposes, we add a default_organisation inside a person, 
      # and we add code to generate a 'default_organisation_title' property on
      # this person that will returns the organisation title.
      self._addProperty('Person', self.DEFAULT_ORGANISATION_TITLE_PROP)
      person = self.getPersonModule().newContent(id='1', portal_type='Person')
      self.failUnless(hasattr(person, 'getDefaultOrganisationTitle'))
      self.failUnless(hasattr(person, 'setDefaultOrganisationTitle'))
      person.setDefaultOrganisationTitle('The organisation title')
      # XXX content generated properties are not in propertyMap. is it a bug ?
      #self.failUnless(person.hasProperty('default_organisation_title'))
      
      # an organisation is created inside the person.
      default_organisation = person._getOb('default_organisation', None)
      self.assertNotEquals(None, default_organisation)
      self.assertEquals('Organisation',
                        default_organisation.getPortalTypeName())
      self.assertEquals('The organisation title',
                        default_organisation.getTitle())
    
    def test_18b_ContentAccessorWithIdClash(self):
      """Tests a content setters do not set the property on acquired object
      that may have the same id, using same scenario as test_18
      Note that we only test Setter for now.
      """
      self._addProperty('Person', self.DEFAULT_ORGANISATION_TITLE_PROP)
      person = self.getPersonModule().newContent(id='1', portal_type='Person')
      another_person = self.getPersonModule().newContent(
                                        id='default_organisation',
                                        portal_type='Person')
      another_person_title = 'This is the other person'
      another_person.setTitle(another_person_title)
      person.setDefaultOrganisationTitle('The organisation title')
      # here we want to make sure we didn't modify this 'default_organisation'
      # we could have get by acquisition.
      self.assertNotEquals(another_person_title,
                           person.getDefaultOrganisationTitle())
      # an organisation is created inside the person.
      default_organisation = person._getOb('default_organisation', None)
      self.assertNotEquals(None, default_organisation)
      self.assertEquals('The organisation title',
                        person.getDefaultOrganisationTitle())
    
    DEFAULT_ORGANISATION_TITLE_ACQUIRED_PROP = '''
          { 'id':         'organisation',
            'storage_id': 'default_organisation',
            'type':       'content',
            'portal_type': ('Organisation', ),
            'acquired_property_id': ('title', ),
            'acquisition_base_category': ( 'destination', ),
            'acquisition_portal_type'  : ( 'Person', ),
            'acquisition_accessor_id'  : 'getDefaultOrganisationValue',
            'acquisition_copy_value'   : 0,
            'acquisition_mask_value'   : 1,
            'acquisition_sync_value'   : 0,
            'acquisition_depends'      : None,
            'mode':       'w', }'''
    
    def test_19_AcquiredContentAccessor(self):
      """Tests an acquired content accessor.
      """
      # For testing purposes, we add a default_organisation inside a person, 
      # and we add code to generate a 'default_organisation_title' property on
      # this person that will returns the organisation title. If this is not
      # defined, then we will acquire the default organisation title of the
      # `destination` person. This is a stupid example, but it works with
      # objects we have in our testing environnement
      self._addProperty('Person', self.DEFAULT_ORGANISATION_TITLE_ACQUIRED_PROP)
      # add destination base category to Person TI
      person_ti = self.getTypesTool().getTypeInfo('Person')
      if 'destination' not in person_ti.base_category_list:
          person_ti.base_category_list = tuple(list(
                self.getTypesTool().getTypeInfo('Person').base_category_list) +
                ['destination', ])
      person = self.getPersonModule().newContent(id='1', portal_type='Person')
      other_pers = self.getPersonModule().newContent(id='2', portal_type='Person')
      other_pers_title = 'This is the title we should acquire'
      other_pers.setDefaultOrganisationTitle(other_pers_title)
      person.setDestinationValue(other_pers)
      
      # title is acquired from the other person
      self.assertEquals(other_pers_title,
                        person.getDefaultOrganisationTitle())
      
      # now if we save, it should create a default_organisation inside this
      # person, but do not modify the other_pers.
      person.setDefaultOrganisationTitle('Our organisation title')
      self.assertEquals('Our organisation title',
                        person.getDefaultOrganisationTitle())
      self.assertEquals(other_pers_title,
                        other_pers.getDefaultOrganisationTitle())
      
    def test_19b_AcquiredContentAccessorWithIdClash(self):
      """Tests a content setters do not set the property on acquired object
      that may have the same id, using same scenario as test_19
      Note that we only test Setter for now.
      """
      self._addProperty('Person', self.DEFAULT_ORGANISATION_TITLE_ACQUIRED_PROP)
      # add destination base category to Person TI
      person_ti = self.getTypesTool().getTypeInfo('Person')
      if 'destination' not in person_ti.base_category_list:
          person_ti.base_category_list = tuple(list(
                self.getTypesTool().getTypeInfo('Person').base_category_list) +
                ['destination', ])
      
      person = self.getPersonModule().newContent(id='1', portal_type='Person')
      another_person = self.getPersonModule().newContent(
                                        id='default_organisation',
                                        portal_type='Person')
      another_person_title = 'This is the other person'
      another_person.setTitle(another_person_title)
      person.setDefaultOrganisationTitle('The organisation title')
      # here we want to make sure we didn't modify this 'default_organisation'
      # we could have get by acquisition.
      self.assertNotEquals(another_person_title,
                           person.getDefaultOrganisationTitle())
      # an organisation is created inside the person.
      default_organisation = person._getOb('default_organisation', None)
      self.assertNotEquals(None, default_organisation)
      self.assertEquals('The organisation title',
                        person.getDefaultOrganisationTitle())
    
    def test_AsContext(self):
      """asContext method return a temporary copy of an object.
      Any modification made to the copy does not change the original object.
      """
      obj = self.getPersonModule().newContent(portal_type='Person')
      obj.setTitle('obj title')
      copy = obj.asContext()
      copy.setTitle('copy title')
      self.assertEquals('obj title', obj.getTitle())
      self.assertEquals('copy title', copy.getTitle())

      # asContext method accepts parameters, and edit the copy with those
      # parameters
      obj = self.getPersonModule().newContent(portal_type='Person', id='obj')
      obj.setTitle('obj title')
      copy = obj.asContext(title='copy title')
      self.assertEquals('obj title', obj.getTitle())
      self.assertEquals('copy title', copy.getTitle())
    
      # acquisition context is the same
      self.assertEquals(self.getPersonModule(), obj.aq_parent)
      self.assertEquals(self.getPersonModule(), copy.aq_parent)

if __name__ == '__main__':
  framework()
else:
  import unittest
  def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestERP5Type))
    return suite
