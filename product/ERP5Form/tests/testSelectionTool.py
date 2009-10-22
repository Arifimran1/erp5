##############################################################################
#
# Copyright (c) 2007 Nexedi SARL and Contributors. All Rights Reserved.
#                    Kazuhiko <kazuhiko@nexedi.com>
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
from threading import Thread
from thread import get_ident

import transaction
from Testing import ZODButil

from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from Products.ERP5Form.Selection import Selection
from Products.ERP5Form.Tool.SelectionTool import SelectionTool


class TestSelectionTool(ERP5TypeTestCase):

  def getTitle(self):
    return "SelectionTool"

  def getBusinessTemplateList(self):
    return tuple()

  def afterSetUp(self):
    uf = self.getPortal().acl_users
    uf._doAddUser('manager', '', ['Manager', 'Assignor'], [])
    user = uf.getUserById('manager').__of__(uf)
    newSecurityManager(None, user)
    self.portal_selections = self.getPortal().portal_selections
    self.portal_selections.setSelectionFor('test_selection', Selection())
    self.portal_selections.setSelectionParamsFor('test_selection', {'key':'value'})

  def testGetSelectionContainer(self):
    self.assertEquals(['test_selection'],
                      self.portal_selections.getSelectionNameList())
    self.assertEquals(['test_selection'],
                      self.portal_selections.getSelectionNames())
    self.assert_(self.portal_selections._getPersistentContainer('manager')
                 is not None)
    self.assert_(getattr(self.portal_selections, 'selection_data', None)
                 is not None)

  def testGetSelectionFor(self):
    selection = self.portal_selections.getSelectionFor('test_selection')
    self.assert_(isinstance(selection, Selection))
    self.assertEquals('test_selection', selection.name)

  def testGetSelectionParamsFor(self):
    self.assertEquals({'key':'value'},
                      self.portal_selections.getSelectionParamsFor('test_selection'))

  def testGetSelectionParamsDictInterface(self):
    self.assertEquals('value',
                      self.portal_selections['test_selection']['key'])
    # the main use case is to have a dict interface in TALES expressions:
    from Products.PageTemplates.Expressions import getEngine
    evaluate_tales = getEngine().getContext(dict(context=self.portal)).evaluate
    self.assertEquals('value',
            evaluate_tales('context/portal_selections/test_selection/key'))
    self.assertEquals('default', evaluate_tales(
      'context/portal_selections/test_selection/not_found | string:default'))


  def testCallSelectionFor(self):
    self.assertEquals(None,
                      self.portal_selections.callSelectionFor('not_found_selection'))
    # XXX more tests needed

  def testCheckedUids(self):
    self.assertEquals([],
                      self.portal_selections.getSelectionCheckedUidsFor('test_selection'))
    self.portal_selections.setSelectionCheckedUidsFor('test_selection',
                                                      ['foo'])
    self.assertEquals(['foo'],
                      self.portal_selections.getSelectionCheckedUidsFor('test_selection'))
    self.portal_selections.updateSelectionCheckedUidList('test_selection',
                                                         ['foo'], ['bar'])
    self.assertEquals(['bar'],
                      self.portal_selections.getSelectionCheckedUidsFor('test_selection'))
    self.portal_selections.checkAll('test_selection',
                                    ['foo', 'baz'])
    self.assertEquals(sorted(['foo', 'bar', 'baz']),
                      sorted(self.portal_selections.getSelectionCheckedUidsFor('test_selection')))
    self.portal_selections.uncheckAll('test_selection',
                                    ['foo', 'bar'])
    self.assertEquals(['baz'],
                      self.portal_selections.getSelectionCheckedUidsFor('test_selection'))

  def testGetSelectionListUrlFor(self):
    self.assertEquals('',
                      self.portal_selections.getSelectionListUrlFor('test_selection'))

  def testInvertMode(self):
    self.portal_selections.setSelectionInvertModeFor('test_selection', 1)
    self.assertEquals(1,
                      self.portal_selections.getSelectionInvertModeFor('test_selection'))
    self.assertEquals([],
                      self.portal_selections.getSelectionInvertModeUidListFor('test_selection'))

  def testSetSelectionToAll(self):
    self.portal_selections.checkAll('test_selection',
                                    ['foo', 'bar'])
    self.portal_selections.setSelectionToAll('test_selection')
    self.assertEquals(0,
                      self.portal_selections.getSelectionInvertModeFor('test_selection'))
    self.assertEquals({},
                      self.portal_selections.getSelectionParamsFor('test_selection'))
    self.assertEquals([],
                      self.portal_selections.getSelectionCheckedUidsFor('test_selection'))

  def testSortOrder(self):
    self.portal_selections.setSelectionSortOrder('test_selection',
                                                 [('title', 'ascending')])
    self.assertEquals([('title', 'ascending')],
                      self.portal_selections.getSelectionSortOrder('test_selection'))
    self.portal_selections.setSelectionQuickSortOrder('test_selection',
                                                      'title')
    self.assertEquals([('title', 'descending')],
                      self.portal_selections.getSelectionSortOrder('test_selection'))
    self.portal_selections.setSelectionQuickSortOrder('test_selection',
                                                      'date')
    self.assertEquals([('date', 'ascending')],
                      self.portal_selections.getSelectionSortOrder('test_selection'))

  def testColumns(self):
    self.assertEquals([],
                      self.portal_selections.getSelectionColumns('test_selection'))
    self.assertEquals([('default_key', 'default_val')],
                      self.portal_selections.getSelectionColumns('test_selection', [('default_key', 'default_val')]))
    self.portal_selections.setSelectionColumns('test_selection',
                                                 [('key', 'val')])
    self.assertEquals([('key', 'val')],
                      self.portal_selections.getSelectionColumns('test_selection'))
    self.assertEquals([('key', 'val')],
                      self.portal_selections.getSelectionColumns('test_selection', [('default_key', 'default_val')]))

  def testStats(self):
    self.assertEquals([' ', ' ', ' ', ' ', ' ', ' '],
                      self.portal_selections.getSelectionStats('test_selection'))
    self.portal_selections.setSelectionStats('test_selection',
                                                 [])
    self.assertEquals([],
                      self.portal_selections.getSelectionStats('test_selection'))

  def testView(self):
    raise NotImplementedError('test should be added')

  def testPage(self):
    raise NotImplementedError('test should be added')

  def testDomainSelection(self):
    self.assertEquals('',
                      self.portal_selections.buildSQLJoinExpressionFromDomainSelection({}))
    self.assertEquals('',
                      self.portal_selections.buildSQLExpressionFromDomainSelection({}))
    from Products.ERP5Form.Selection import DomainSelection
    self.assertEquals('',
                      self.portal_selections.buildSQLJoinExpressionFromDomainSelection(DomainSelection({}).__of__(self.portal_selections)))
    category_tool = self.getCategoryTool()
    base = category_tool.newContent(portal_type = 'Base Category',
                                   id='test_base_cat')
    base_uid = base.getUid()
    self.assertEquals('category AS test_base_cat_category',
                      self.portal_selections.buildSQLJoinExpressionFromDomainSelection({'test_base_cat': ('portal_categories', 'test_base_cat')}))
    self.assertEquals('( catalog.uid = test_base_cat_category.uid AND (test_base_cat_category.category_uid = %d AND test_base_cat_category.base_category_uid = %d) )' % (base_uid, base_uid),
                      self.portal_selections.buildSQLExpressionFromDomainSelection({'test_base_cat': ('portal_categories', 'test_base_cat')}))
    test = base.newContent(portal_type = 'Category', id = 'test_cat')
    test_uid = test.getUid()
    self.assertEquals('category AS test_base_cat_category',
                      self.portal_selections.buildSQLJoinExpressionFromDomainSelection({'test_base_cat': ('portal_categories', 'test_base_cat/test_cat')}))
    self.assertEquals('( catalog.uid = test_base_cat_category.uid AND (test_base_cat_category.category_uid = %d AND test_base_cat_category.base_category_uid = %d) )' % (test_uid, base_uid),
                      self.portal_selections.buildSQLExpressionFromDomainSelection({'test_base_cat': ('portal_categories', 'test_base_cat/test_cat')}))
    self.assertEquals('( catalog.uid = test_base_cat_category.uid AND (test_base_cat_category.category_uid = %d AND test_base_cat_category.base_category_uid = %d AND test_base_cat_category.category_strict_membership = 1) )' % (test_uid, base_uid),
                      self.portal_selections.buildSQLExpressionFromDomainSelection({'test_base_cat': ('portal_categories', 'test_base_cat/test_cat')}, strict_membership = 1))

  def testDict(self):
    self.assertEquals({},
                      self.portal_selections.getSelectionDomainDictFor('test_selection'))
    self.assertEquals({},
                      self.portal_selections.getSelectionReportDictFor('test_selection'))

  def testIndex(self):
    self.assertEquals(None,
                      self.portal_selections.getSelectionIndexFor('test_selection'))

  def testDeleteSelection(self):
    selection = self.portal_selections.getSelectionFor('test_selection')
    self.assert_(isinstance(selection, Selection))
    self.portal_selections.manage_deleteSelection('test_selection')
    selection = self.portal_selections.getSelectionFor('test_selection')
    self.assertEqual(selection, None)

  def testDeleteSelectionForUser(self):
    # XXX: There is side effect, that manager, running user, is the same use
    #      and there is no way (for now) to get selections per user...
    selection = self.portal_selections.getSelectionFor('test_selection')
    self.assert_(isinstance(selection, Selection))
    self.portal_selections.manage_deleteSelectionForUser('test_selection',
        'manager')
    selection = self.portal_selections.getSelectionFor('test_selection')
    self.assertEqual(selection, None)

  def testDeleteGlobalSelection(self):
    selection = self.portal_selections.getSelectionFor('test_selection')
    self.assert_(isinstance(selection, Selection))
    self.portal_selections.manage_deleteGlobalSelection('test_selection')
    selection = self.portal_selections.getSelectionFor('test_selection')
    self.assertEqual(selection, None)

class TestSelectionPersistence(unittest.TestCase):
  """SelectionTool tests that needs a "real" FileStorage to make sure selection
  are really persistent and supports conflict resolution.
  """
  def setUp(self):
    # patch selection tool class so that we don't need a portal_membership to
    # find the current user name
    SelectionTool._getUserId_saved = SelectionTool._getUserId
    SelectionTool._getUserId = lambda self: 'user'

    self.db = ZODButil.makeDB()
    self.cnx = self.db.open()
    self.portal_selections = \
      self.cnx.root().portal_selections = SelectionTool()
    self.portal_selections.setSelectionFor('test_selection', Selection())
    transaction.commit()
    
  def tearDown(self):
    # revert the patch from setUp
    SelectionTool._getUserId = SelectionTool._getUserId_saved
    self.cnx.close()
    ZODButil.cleanDB()
  
  def _runWithAnotherConnection(self, thread_func):
    """runs `thread_func` with another ZODB connection

    thread_func must be a callable accepting the connection object as only
    argument.
    """
    t = Thread(target=thread_func, args=(self.db.open(),))
    t.start()
    t.join(60)
    self.assertFalse(t.isAlive())

  def testSelectionParamConflictResolution(self):
    # same user edits the same selection with two different parameters
    self.portal_selections.setSelectionParamsFor(
                       'test_selection', dict(a="b"))
    def thread_func(cnx):
      try:
        portal_selections = cnx.root().portal_selections
        portal_selections.setSelectionParamsFor(
                              'test_selection', dict(a="c"))
        transaction.commit()
      finally:
        cnx.close()
    self._runWithAnotherConnection(thread_func)

    # This would raise a ConflictError without conflict resolution code
    transaction.commit()
    params = self.portal_selections.getSelectionParamsFor('test_selection')
    self.assertTrue(params.get('a'))

  def testSelectionNameConflictResolution(self):
    # same user edits two different selections
    self.portal_selections.setSelectionParamsFor(
                       'test_selection2', dict(a="b"))
    def thread_func(cnx):
      try:
        portal_selections = cnx.root().portal_selections
        portal_selections.setSelectionParamsFor(
                       'test_selection1', dict(a="b"))
        transaction.commit()
      finally:
        cnx.close()
    self._runWithAnotherConnection(thread_func)

    # This would raise a ConflictError without conflict resolution code
    transaction.commit()
    params = self.portal_selections.getSelectionParamsFor('test_selection1')
    self.assertEquals(params.get('a'), 'b')
    params = self.portal_selections.getSelectionParamsFor('test_selection2')
    self.assertEquals(params.get('a'), 'b')

  def testDifferentUsernameConflictResolution(self):
    # different users edits selections
    SelectionTool._getUserId = lambda self: 'user-%s' % get_ident()
    # Note that in current implementation, the first time we initialized a
    # selection for a user the mapping user -> selections is modified, which
    # will generate a conflict if we have two new users at the same time.
    # This test just checks that once we have initialized a user it doesn't
    # generate conflicts when another users also modifies it owns selection.
    # So we make sure that selection container is initialized for this user
    self.portal_selections.setSelectionParamsFor(
                       'test_selection', dict(initialized="1"))
    transaction.commit()

    self.portal_selections.setSelectionParamsFor(
                       'test_selection', dict(a="b"))
    def thread_func(cnx):
      try:
        portal_selections = cnx.root().portal_selections
        portal_selections.setSelectionParamsFor(
                       'test_selection', dict(a="b"))
        transaction.commit()
      finally:
        cnx.close()
    self._runWithAnotherConnection(thread_func)

    transaction.commit()
    # this check is quite low level.
    # we know that setUp stored one selection, and each of our 2 threads stored
    # one selection.
    self.assertEquals(3, len(self.portal_selections.selection_data.keys()))

  def testPersistentSelections(self):
    # test that selection parameters are persistent
    self.portal_selections.setSelectionParamsFor(
                 'test_selection', dict(key="saved_value"))
    transaction.commit()
    self.cnx.close()

    self.cnx = self.db.open()
    portal_selections = self.cnx.root().portal_selections
    self.assertEquals('saved_value',
        portal_selections.getSelectionParamsFor('test_selection').get('key'))

class TestSelectionToolMemcachedStorage(TestSelectionTool):

  def getTitle(self):
    return "SelectionTool with Memcached Storage"

  def afterSetUp(self):
    # create a Memcached Plugin
    memcached_tool = self.getPortal().portal_memcached
    if getattr(memcached_tool, 'default_memcached_plugin', None) is None:
      memcached_tool.newContent(id='default_memcached_plugin',
                                portal_type='Memcached Plugin',
                                int_index=0,
                                url_string='127.0.0.1:11211')
    self.portal.portal_selections.setStorage('portal_memcached/default_memcached_plugin')
    TestSelectionTool.afterSetUp(self)

  def testGetSelectionContainer(self):
    self.assertEquals([],
                      self.portal_selections.getSelectionNameList())
    self.assertEquals([],
                      self.portal_selections.getSelectionNames())
    self.assert_(self.portal_selections._getMemcachedContainer() is not None)
    self.assert_(getattr(self.portal_selections, '_v_selection_data', None)
                 is not None)

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestSelectionTool))
  suite.addTest(unittest.makeSuite(TestSelectionToolMemcachedStorage))
  suite.addTest(unittest.makeSuite(TestSelectionPersistence))
  return suite
