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

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Needed in order to have a log file inside the current folder
os.environ['EVENT_LOG_FILE'] = os.path.join(os.getcwd(), 'zLOG.log')
os.environ['EVENT_LOG_SEVERITY'] = '-300'

from Testing import ZopeTestCase
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from zLOG import LOG
from DateTime import DateTime

try:
  from transaction import get as get_transaction
except ImportError:
  pass

class TestERP5Catalog(ERP5TypeTestCase):
  """
    Tests for ERP5 Catalog.
  """

  def getTitle(self):
    return "ERP5Catalog"

  def getBusinessTemplateList(self):
    return ('erp5_base',)

  # Different variables used for this test
  run_all_test = 1

  def afterSetUp(self, quiet=1, run=1):
    self.login()
    portal = self.getPortal()
    catalog_tool = self.getCatalogTool()
    # XXX This does not works
    #catalog_tool.reindexObject(portal)

  def login(self, quiet=0, run=run_all_test):
    uf = self.getPortal().acl_users
    uf._doAddUser('seb', '', ['Manager'], [])
    user = uf.getUserById('seb').__of__(uf)
    newSecurityManager(None, user)

  def getSqlPathList(self):
    """
    Give the full list of path in the catalog
    """
    sql_connection = self.getSqlConnection()
    sql = 'select path from catalog'
    result = sql_connection.manage_test(sql)
    path_list = map(lambda x: x['path'],result)
    return path_list

  def checkRelativeUrlInSqlPathList(self,url_list):
    path_list = self.getSqlPathList()
    portal_id = self.getPortalId()
    for url in url_list:
      path = '/' + portal_id + '/' + url
      self.failUnless(path in path_list)
      LOG('checkRelativeUrlInSqlPathList found path:',0,path)

  def checkRelativeUrlNotInSqlPathList(self,url_list):
    path_list = self.getSqlPathList()
    portal_id = self.getPortalId()
    for url in url_list:
      path = '/' + portal_id + '/' + url
      self.failUnless(path not in  path_list)
      LOG('checkRelativeUrlInSqlPathList not found path:',0,path)

  def test_01_HasEverything(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      ZopeTestCase._print('\nTest Has Everything ')
      LOG('Testing... ',0,'testHasEverything')
    self.failUnless(self.getCategoryTool()!=None)
    self.failUnless(self.getSimulationTool()!=None)
    self.failUnless(self.getTypeTool()!=None)
    self.failUnless(self.getSqlConnection()!=None)
    self.failUnless(self.getCatalogTool()!=None)

  def test_02_EverythingCatalogued(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      ZopeTestCase._print('\nTest Everything Catalogued')
      LOG('Testing... ',0,'testEverythingCatalogued')
    portal_catalog = self.getCatalogTool()
    self.tic()
    organisation_module_list = portal_catalog(portal_type='Organisation Module')
    self.assertEquals(len(organisation_module_list),1)

  def test_03_CreateAndDeleteObject(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      message = 'Test Create And Delete Objects'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    portal_catalog = self.getCatalogTool()
    person_module = self.getPersonModule()
    person = person_module.newContent(id='1',portal_type='Person')
    path_list = [person.getRelativeUrl()]
    self.checkRelativeUrlNotInSqlPathList(path_list)
    person.immediateReindexObject()
    self.checkRelativeUrlInSqlPathList(path_list)
    person_module.manage_delObjects('1')
    self.checkRelativeUrlNotInSqlPathList(path_list)
    # Now we will ask to immediatly reindex
    person = person_module.newContent(id='2',
                                      portal_type='Person',
                                      immediate_reindex=1)
    path_list = [person.getRelativeUrl()]
    self.checkRelativeUrlInSqlPathList(path_list)
    person.immediateReindexObject()
    self.checkRelativeUrlInSqlPathList(path_list)
    person_module.manage_delObjects('2')
    self.checkRelativeUrlNotInSqlPathList(path_list)
    # Now we will try with the method deleteContent
    person = person_module.newContent(id='3',portal_type='Person')
    path_list = [person.getRelativeUrl()]
    self.checkRelativeUrlNotInSqlPathList(path_list)
    person.immediateReindexObject()
    self.checkRelativeUrlInSqlPathList(path_list)
    person_module.deleteContent('3')
    self.checkRelativeUrlNotInSqlPathList(path_list)

  def test_04_SearchFolderWithDeletedObjects(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      message = 'Search Folder With Deleted Objects'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    person_module = self.getPersonModule()
    # Now we will try the same thing as previous test and look at searchFolder
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals([],folder_object_list)
    person = person_module.newContent(id='4',portal_type='Person',immediate_reindex=1)
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals(['4'],folder_object_list)
    person.immediateReindexObject()
    person_module.manage_delObjects('4')
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals([],folder_object_list)

  def test_05_SearchFolderWithImmediateReindexObject(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      message = 'Search Folder With Immediate Reindex Object'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    person_module = self.getPersonModule()

    # Now we will try the same thing as previous test and look at searchFolder
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals([],folder_object_list)

    person = person_module.newContent(id='4',portal_type='Person')
    person.immediateReindexObject()
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals(['4'],folder_object_list)
    
    person_module.manage_delObjects('4')
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals([],folder_object_list)

  def test_06_SearchFolderWithRecursiveImmediateReindexObject(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      message = 'Search Folder With Recursive Immediate Reindex Object'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    person_module = self.getPersonModule()

    # Now we will try the same thing as previous test and look at searchFolder
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals([],folder_object_list)

    person = person_module.newContent(id='4',portal_type='Person')
    person_module.recursiveImmediateReindexObject()
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals(['4'],folder_object_list)
    
    person_module.manage_delObjects('4')
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals([],folder_object_list)

  def test_07_ClearCatalogAndTestNewContent(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Clear Catalog And Test New Content'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    person_module = self.getPersonModule()

    # Clear catalog
    portal_catalog = self.getCatalogTool()
    portal_catalog.manage_catalogClear()

    person = person_module.newContent(id='4',portal_type='Person',immediate_reindex=1)
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals(['4'],folder_object_list)

  def test_08_ClearCatalogAndTestRecursiveImmediateReindexObject(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Clear Catalog And Test Recursive Immediate Reindex Object'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    person_module = self.getPersonModule()

    # Clear catalog
    portal_catalog = self.getCatalogTool()
    portal_catalog.manage_catalogClear()

    person = person_module.newContent(id='4',portal_type='Person')
    person_module.recursiveImmediateReindexObject()
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals(['4'],folder_object_list)

  def test_09_ClearCatalogAndTestImmediateReindexObject(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Clear Catalog And Test Immediate Reindex Object'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    person_module = self.getPersonModule()

    # Clear catalog
    portal_catalog = self.getCatalogTool()
    portal_catalog.manage_catalogClear()

    person = person_module.newContent(id='4',portal_type='Person')
    person.immediateReindexObject()
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals(['4'],folder_object_list)

  def test_10_OrderedSearchFolder(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Ordered Search Folder'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    person_module = self.getPersonModule()

    # Clear catalog
    portal_catalog = self.getCatalogTool()
    portal_catalog.manage_catalogClear()

    person = person_module.newContent(id='a',portal_type='Person',title='a',description='z')
    person.immediateReindexObject()
    person = person_module.newContent(id='b',portal_type='Person',title='a',description='y')
    person.immediateReindexObject()
    person = person_module.newContent(id='c',portal_type='Person',title='a',description='x')
    person.immediateReindexObject()
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder(sort_on=[('id','ascending')])]
    self.assertEquals(['a','b','c'],folder_object_list)
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder(sort_on=[('title','ascending'),('description','ascending')])]
    self.assertEquals(['c','b','a'],folder_object_list)
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder(sort_on=[('title','ascending'),('description','descending')])]
    self.assertEquals(['a','b','c'],folder_object_list)

  def test_11_CastStringAsInt(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Cast String As Int With Order By'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    person_module = self.getPersonModule()

    # Clear catalog
    portal_catalog = self.getCatalogTool()
    portal_catalog.manage_catalogClear()

    person = person_module.newContent(id='a',portal_type='Person',title='1')
    person.immediateReindexObject()
    person = person_module.newContent(id='b',portal_type='Person',title='2')
    person.immediateReindexObject()
    person = person_module.newContent(id='c',portal_type='Person',title='12')
    person.immediateReindexObject()
    folder_object_list = [x.getObject().getTitle() for x in person_module.searchFolder(sort_on=[('title','ascending')])]
    self.assertEquals(['1','12','2'],folder_object_list)
    folder_object_list = [x.getObject().getTitle() for x in person_module.searchFolder(sort_on=[('title','ascending','int')])]
    self.assertEquals(['1','2','12'],folder_object_list)

  def test_12_TransactionalUidBuffer(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Transactional Uid Buffer'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    portal_catalog = self.getCatalogTool()
    catalog = portal_catalog.getSQLCatalog()
    self.failUnless(catalog is not None)

    # Clear out the uid buffer.
    if hasattr(catalog, '_v_uid_buffer'):
      del catalog._v_uid_buffer

    # Need to abort a transaction artificially, so commit the current
    # one, first.
    get_transaction().commit()

    catalog.newUid()
    self.failUnless(hasattr(catalog, '_v_uid_buffer'))
    self.failUnless(len(catalog._v_uid_buffer) > 0)

    get_transaction().abort()
    self.failUnless(len(getattr(catalog, '_v_uid_buffer', [])) == 0)

  def test_13_ERP5Site_reindexAll(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'ERP5Site_reindexAll'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # Flush message queue
    get_transaction().commit()
    self.tic()
    # Create some objects
    portal = self.getPortal()
    portal_category = self.getCategoryTool()
    base_category = portal_category.newContent(portal_type='Base Category',
                                               title="GreatTitle1")
    module = portal.getDefaultModule('Organisation')
    organisation = module.newContent(portal_type='Organisation',
                                     title="GreatTitle2")
    # Flush message queue
    get_transaction().commit()
    self.tic()
    # Clear catalog
    portal_catalog = self.getCatalogTool()
    portal_catalog.manage_catalogClear()
    sql_connection = self.getSqlConnection()
    sql = 'select count(*) from catalog where portal_type!=NULL'
    result = sql_connection.manage_test(sql)
    message_count = result[0]['COUNT(*)']
    self.assertEquals(0, message_count)
    # Commit
    get_transaction().commit()
    # Reindex all
    portal.ERP5Site_reindexAll()
    get_transaction().commit()
    self.tic()
    get_transaction().commit()
    # Check catalog
    sql = 'select count(*) from message'
    result = sql_connection.manage_test(sql)
    message_count = result[0]['COUNT(*)']
    self.assertEquals(0, message_count)
    # Check if object are catalogued
    self.checkRelativeUrlInSqlPathList([
                organisation.getRelativeUrl(),
                'portal_categories/%s' % base_category.getRelativeUrl()])

  def test_14_ReindexWithBrokenCategory(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Reindexing an object with 1 broken category must not'\
                ' affect other valid categories '
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ', 0, message)
    # Flush message queue
    get_transaction().commit()
    self.tic()
    # Create some objects
    portal = self.getPortal()
    portal_category = self.getCategoryTool()
    group_nexedi_category = portal_category.group\
                                .newContent( id = 'nexedi', )
    region_europe_category = portal_category.region\
                                .newContent( id = 'europe', )
    module = portal.getDefaultModule('Organisation')
    organisation = module.newContent(portal_type='Organisation',)
    organisation.setGroup('nexedi')
    self.assertEquals(organisation.getGroupValue(), group_nexedi_category)
    organisation.setRegion('europe')
    self.assertEquals(organisation.getRegionValue(), region_europe_category)
    organisation.setRole('not_exists')
    self.assertEquals(organisation.getRoleValue(), None)
    # Flush message queue
    get_transaction().commit()
    self.tic()
    # Clear catalog
    portal_catalog = self.getCatalogTool()
    portal_catalog.manage_catalogClear()
    sql_connection = self.getSqlConnection()
    
    sql = 'SELECT COUNT(*) FROM category '\
        'WHERE uid=%s and category_strict_membership = 1' %\
        organisation.getUid()
    result = sql_connection.manage_test(sql)
    message_count = result[0]['COUNT(*)']
    self.assertEquals(0, message_count)
    # Commit
    get_transaction().commit()
    self.tic()
    # Check catalog
    organisation.reindexObject()
    # Commit
    get_transaction().commit()
    self.tic()
    sql = 'select count(*) from message'
    result = sql_connection.manage_test(sql)
    message_count = result[0]['COUNT(*)']
    self.assertEquals(0, message_count)
    # Check region and group categories are catalogued
    for base_cat, theorical_count in {
                                      'region':1,
                                      'group':1,
                                      'role':0}.items() :
      sql = """SELECT COUNT(*) FROM category
            WHERE category.uid=%s and category.category_strict_membership = 1
            AND category.base_category_uid = %s""" % (organisation.getUid(),
                    portal_category[base_cat].getUid())
      result = sql_connection.manage_test(sql)
      cataloged_obj_count = result[0]['COUNT(*)']
      self.assertEquals(theorical_count, cataloged_obj_count,
            'category %s is not cataloged correctly' % base_cat)

  def test_15_getObject(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'getObject'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # portal_catalog.getObject should return None if the UID parameters
    # is a string
    portal_catalog = self.getCatalogTool()
    self.assertRaises(ValueError, portal_catalog.getObject, "StringUID")
  
  def test_16_newUid(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'newUid'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # newUid should not assign the same uid
    portal_catalog = self.getCatalogTool()
    from Products.ZSQLCatalog.SQLCatalog import UID_BUFFER_SIZE
    uid_dict = {}
    for i in xrange(UID_BUFFER_SIZE * 3):
      uid = portal_catalog.newUid()
      self.failIf(uid in uid_dict)
      uid_dict[uid] = None
  
  def test_17_CreationDate_ModificationDate(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'getCreationDate, getModificationDate'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    portal_catalog = self.getCatalogTool()
    portal = self.getPortal()
    sql_connection = self.getSqlConnection()
    
    module = portal.getDefaultModule('Organisation')
    organisation = module.newContent(portal_type='Organisation',)
    creation_date = organisation.getCreationDate().ISO()
    get_transaction().commit()
    self.tic()
    sql = """select creation_date, modification_date 
             from catalog where uid = %s""" % organisation.getUid()
    result = sql_connection.manage_test(sql)
    self.assertEquals(creation_date, result[0]['creation_date'].ISO())
    self.assertEquals(organisation.getModificationDate().ISO(),
                              result[0]['modification_date'].ISO())
    self.assertEquals(creation_date, result[0]['modification_date'].ISO())
    
    import time; time.sleep(3)
    organisation.edit(title='edited')
    organisation.reindexObject()
    now = DateTime().ISO()
    get_transaction().commit()
    self.tic()
    result = sql_connection.manage_test(sql)
    self.assertEquals(creation_date, result[0]['creation_date'].ISO())
    self.assertNotEquals(organisation.getModificationDate(),
                              organisation.getCreationDate())
    self.assertEquals(organisation.getModificationDate().ISO(), now)
    self.assertEquals(organisation.getModificationDate().ISO(),
                              result[0]['modification_date'].ISO())
    self.assertEquals(now, result[0]['modification_date'].ISO())
    
  def test_18_buildSQLQuery(self, quiet=0, run=0) :#run_all_test):
    """Tests that buildSQLQuery works with another query_table than 'catalog'"""
    if not run: return
    if not quiet:
      message = 'buildSQLQuery with query_table'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    portal = self.getPortal()
    portal_catalog = self.getCatalogTool()
    # clear catalog
    portal_catalog.manage_catalogClear()
    get_transaction().commit()
    
    # create some content to use destination_section_title as related key
    # FIXME: create the related key here ?
    module = portal.getDefaultModule('Organisation')
    source_organisation = module.newContent( portal_type='Organisation',
                                        title = 'source_organisation')
    destination_organisation = module.newContent( portal_type='Organisation',
                                        title = 'destination_organisation')
    source_organisation.setDestinationSectionValue(destination_organisation)
    source_organisation.recursiveReindexObject()
    destination_organisation.recursiveReindexObject()
    get_transaction().commit()
    self.tic()

    # buildSQLQuery can use arbitrary table name.
    query_table = "node"
    sql_squeleton = """
    SELECT %(query_table)s.uid,
           %(query_table)s.id
    FROM
      <dtml-in prefix="table" expr="from_table_list"> 
        <dtml-var table_item> AS <dtml-var table_key>
        <dtml-unless sequence-end>, </dtml-unless>
      </dtml-in>
    <dtml-if where_expression>
    WHERE 
      <dtml-var where_expression>
    </dtml-if>
    <dtml-if order_by_expression>
      ORDER BY <dtml-var order_by_expression>
    </dtml-if>
    """ % {'query_table' : query_table}
    
    portal_skins_custom = portal.portal_skins.custom
    portal_skins_custom.manage_addProduct['ZSQLMethods'].manage_addZSQLMethod(
          id = 'testMethod',
          title = '',
          connection_id = 'erp5_sql_connection',
          arguments = "\n".join([ 'from_table_list',
                                  'where_expression',
                                  'order_by_expression' ]),
          template = sql_squeleton)
    testMethod = portal_skins_custom['testMethod']
    
    default_parametrs = {}
    default_parametrs['portal_type'] = 'Organisation'
    default_parametrs['from_table_list'] = {}
    default_parametrs['where_expression'] = ""
    default_parametrs['order_by_expression'] = None
    
    #import pdb; pdb.set_trace()
    # check that we retrieve our 2 organisations by default.
    kw = default_parametrs.copy()
    kw.update( portal_catalog.buildSQLQuery(
                  query_table = query_table,
                  **kw) )
    LOG('kw', 0, kw)
    LOG('SQL', 0, testMethod(src__=1, **kw))
    self.assertEquals(len(testMethod(**kw)), 2)
    
    # check we can make a simple filter on title.
    kw = default_parametrs.copy()
    kw.update( portal_catalog.buildSQLQuery(
                  query_table = query_table,
                  title = 'source_organisation',
                  **kw) )
    LOG('kw', 1, kw)
    LOG('SQL', 1, testMethod(src__=1, **kw))
    self.assertEquals( len(testMethod(**kw)), 1,
                       testMethod(src__=1, **kw) )
    self.assertEquals( testMethod(**kw)[0]['uid'],
                        source_organisation.getUid(),
                        testMethod(src__=1, **kw) )
    
    # check sort
    kw = default_parametrs.copy()
    kw.update(portal_catalog.buildSQLQuery(
                  query_table = query_table,
                  sort_on = [('id', 'ascending')],
                  **kw))
    LOG('kw', 2, kw)
    LOG('SQL', 2, testMethod(src__=1, **kw))
    brains = testMethod(**kw)
    self.assertEquals( len(brains), 2,
                       testMethod(src__=1, **kw))
    self.failIf( brains[0]['id'] > brains[1]['id'],
                 testMethod(src__=1, **kw) )
    
    # check related keys works
    kw = default_parametrs.copy()
    kw.update(portal_catalog.buildSQLQuery(
                  query_table = query_table,
                  destination_section_title = 'organisation_destination'),
                  **kw)
    LOG('kw', 3, kw)
    LOG('SQL', 3, testMethod(src__=1, **kw))
    brains = testMethod(**kw)
    self.assertEquals( len(brains), 1, testMethod(src__=1, **kw) )
    self.assertEquals( brains[0]['uid'],
                       source_organisation.getUid(),
                       testMethod(src__=1, **kw) )
    
  def test_19_SearchFolderWithNonAsciiCharacter(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      message = 'Search Folder With Non Ascii Character'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    person_module = self.getPersonModule()

    # Now we will try the same thing as previous test and look at searchFolder
    title='S\xc3\xa9bastien'
    person = person_module.newContent(id='5',portal_type='Person',title=title)
    person.immediateReindexObject()
    folder_object_list = [x.getObject().getId() for x in person_module.searchFolder()]
    self.assertEquals(['5'],folder_object_list)
    folder_object_list = [x.getObject().getId() for x in 
                              person_module.searchFolder(title=title)]
    self.assertEquals(['5'],folder_object_list)
    
  def test_20_SearchFolderWithDynamicRelatedKey(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      message = 'Search Folder With Dynamic Related Key'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)

    # Create some objects
    portal = self.getPortal()
    portal_category = self.getCategoryTool()
    portal_category.group.manage_delObjects([x for x in
        portal_category.group.objectIds()])
    group_nexedi_category = portal_category.group\
                                .newContent( id = 'nexedi', title='Nexedi',
                                             description='a')
    group_nexedi_category2 = portal_category.group\
                                .newContent( id = 'storever', title='Storever',
                                             description='b')
    module = portal.getDefaultModule('Organisation')
    organisation = module.newContent(portal_type='Organisation',)
    organisation.setGroup('nexedi')
    self.assertEquals(organisation.getGroupValue(), group_nexedi_category)
    organisation2 = module.newContent(portal_type='Organisation',)
    organisation2.setGroup('storever')
    self.assertEquals(organisation2.getGroupValue(), group_nexedi_category2)
    # Flush message queue
    get_transaction().commit()
    self.tic()

    # Try to get the organisation with the group title Nexedi
    organisation_list = [x.getObject() for x in 
                         module.searchFolder(group_title='Nexedi')]
    self.assertEquals(organisation_list,[organisation])
    # Try to get the organisation with the group id nexedi
    organisation_list = [x.getObject() for x in 
                         module.searchFolder(group_id='storever')]
    self.assertEquals(organisation_list,[organisation2])
    # Try to get the organisation with the group description 'a'
    organisation_list = [x.getObject() for x in 
                         module.searchFolder(group_description='a')]
    self.assertEquals(organisation_list,[organisation])
    # Try to get the organisation with the group description 'c'
    organisation_list = [x.getObject() for x in 
                         module.searchFolder(group_description='c')]
    self.assertEquals(organisation_list,[])
    # Try to get the organisation with the default group description 'c'
    organisation_list = [x.getObject() for x in 
                         module.searchFolder(default_group_description='c')]
    self.assertEquals(organisation_list,[])


