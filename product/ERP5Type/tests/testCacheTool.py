##############################################################################
#
# Copyright (c) 2005 Nexedi SARL and Contributors. All Rights Reserved.
#                     Ivan Tyagov <ivan@nexedi.com>
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
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
from Products.ERP5Type.CachePlugins.DummyCache import DummyCache
from Products.ERP5Type.Cache import CachingMethod
from AccessControl.SecurityManagement import newSecurityManager
from zLOG import LOG
import time

try:
  from transaction import get as get_transaction
except ImportError:
  pass

class TestingCache(DummyCache):
  """A dummy cache that mark cache miss, so that you can later count access
  using getCacheMisses() """
  def __init__(self, params):
    DummyCache.__init__(self, params)
  
  def __call__(self, callable_object, cache_id, scope, cache_duration=None,
                *args, **kwd):
    self.markCacheMiss(1)
    return callable_object(*args, **kwd)

class TestCacheTool(ERP5TypeTestCase):

  run_all_test = 1
 
  def getTitle(self):
    return "Cache Tool"
  
  def afterSetUp(self):
    self.login()
    
  def login(self, quiet=0, run=run_all_test):
    uf = self.getPortal().acl_users
    uf._doAddUser('seb', '', ['Manager'], [])
    uf._doAddUser('ERP5TypeTestCase', '', ['Manager'], [])
    user = uf.getUserById('seb').__of__(uf)
    newSecurityManager(None, user)

  def test_01_CheckCacheTool(self, quiet=0, run=run_all_test):
    if not run:
      return
    if not quiet:
      message = '\nCheck CacheTool '
      ZopeTestCase._print(message)
      LOG('Testing... ',0,message)
      
      portal = self.getPortal()
      self.assertNotEqual(None,getattr(portal,'portal_caches',None))
      get_transaction().commit()


  def test_02_CheckPortalTypes(self, quiet=0, run=run_all_test):
    if not run:
      return
    if not quiet:
      message = '\nCheck Portal Types'
      ZopeTestCase._print(message)
      LOG('Testing... ',0,message)
      
      portal = self.getPortal()
      portal_types = portal.portal_types
      typeinfo_names = ("Cache Factory",
                      "Ram Cache",
                      "Distributed Ram Cache",
                      "SQL Cache",
                      )
      for typeinfo_name in typeinfo_names:
        portal_type = getattr(portal_types,typeinfo_name,None)
        self.assertNotEqual(None,portal_type)
      get_transaction().commit()
      
  def test_03_CreateCacheFactories(self, quiet=0, run=run_all_test):
    if not run:
      return
    if not quiet:
      message = '\nCreate Cache Tool Factories'
      ZopeTestCase._print(message)
      LOG('Testing... ',0,message)
      portal = self.getPortal()
      portal_caches = portal.portal_caches
        
      # Cache plugins are organised into 'Cache factories' so we create
      # factories first ram_cache_factory (to test Ram Cache Plugin) 
      ram_cache_factory = portal_caches.newContent(portal_type="Cache Factory",
                                                  id = 'ram_cache_factory',
                                                  container=portal_caches)
      ram_cache_plugin = ram_cache_factory.newContent(portal_type="Ram Cache",
                                                    container=ram_cache_factory)
      ram_cache_plugin.setIntIndex(0)

      
      ## distributed_ram_cache_factory (to test Distributed Ram Cache Plugin) 
      dram_cache_factory = portal_caches.newContent(portal_type="Cache Factory",
                                          id = 'distributed_ram_cache_factory',
                                          container=portal_caches)
      dram_cache_plugin = dram_cache_factory.newContent(
              portal_type="Distributed Ram Cache", container=dram_cache_factory)
      dram_cache_plugin.setIntIndex(0)
      
      ## sql_cache_factory (to test SQL Cache Plugin) 
      sql_cache_factory = portal_caches.newContent(portal_type="Cache Factory",
                                                   id = 'sql_cache_factory',
                                                   container=portal_caches)
      sql_cache_plugin = sql_cache_factory.newContent(
                      portal_type="SQL Cache", container=sql_cache_factory)
      sql_cache_plugin.setIntIndex(0)
      
      ## erp5_user_factory (to test a combination of all cache plugins)
      erp5_user_factory = portal_caches.newContent(portal_type="Cache Factory",
                                                   id = "erp5_user_factory",
                                                   container=portal_caches)
      
      ram_cache_plugin = erp5_user_factory.newContent(
              portal_type="Ram Cache", container=erp5_user_factory)
      ram_cache_plugin.setIntIndex(0)
      dram_cache_plugin = erp5_user_factory.newContent(
              portal_type="Distributed Ram Cache", container=erp5_user_factory)
      dram_cache_plugin.setIntIndex(1)
      sql_cache_plugin = erp5_user_factory.newContent(
              portal_type="SQL Cache", container=erp5_user_factory)
      sql_cache_plugin.setIntIndex(2)
      
      ##
      get_transaction().commit()

      ## update Ram Cache structure
      portal_caches.updateCache()
      from Products.ERP5Type.Cache import CachingMethod
      
      ## do we have the same structure we created above?
      self.assert_('ram_cache_factory' in CachingMethod.factories)
      self.assert_('distributed_ram_cache_factory' in CachingMethod.factories)
      self.assert_('sql_cache_factory' in CachingMethod.factories)
      self.assert_('erp5_user_factory' in CachingMethod.factories)
      
  def test_04_CreateCachedMethod(self, quiet=0, run=run_all_test):
    if not run:
      return
    if not quiet:
      message = '\nCreate Cache Method (Python Script)'
      ZopeTestCase._print(message)
      LOG('Testing... ',0,message)
      portal = self.getPortal()
      
      ## add test cached method
      py_script_id = "testCachedMethod"
      py_script_params = "value=10000, portal_path=('','erp5')"
      py_script_body = """
def veryExpensiveMethod(value):
 ## do something expensive for some time
 ## no 'time.sleep()' available in Zope
 ## so concatenate strings
 s = ""
 for i in range(0, value):
   s = str(value*value*value) + s
 return value

result = veryExpensiveMethod(value)
return result
"""
      portal.manage_addProduct['PythonScripts'].manage_addPythonScript(
                                                  id=py_script_id)
      py_script_obj = getattr(portal, py_script_id)
      py_script_obj.ZPythonScript_edit(py_script_params, py_script_body)
      get_transaction().commit()

  def test_05_CacheFactoryOnePlugin(self, quiet=0, run=run_all_test):
    """ Test cache factory containing only one cache plugin. """
    if not run:
      return
    if not quiet:
      message = '\nTest each type of cache plugin individually.'
      ZopeTestCase._print(message)
      LOG('Testing... ',0,message)
      portal = self.getPortal()
      from Products.ERP5Type.Cache import CachingMethod
      py_script_id = "testCachedMethod"
      py_script_obj = getattr(portal, py_script_id)
      for cf_name in ('ram_cache_factory',
                      'distributed_ram_cache_factory',
                      'sql_cache_factory'):
        my_cache = CachingMethod(py_script_obj,
                                 'py_script_obj',
                                 cache_factory=cf_name)
        self._cacheFactoryInstanceTest(my_cache, cf_name)
        
  def test_06_CacheFactoryMultiPlugins(self, quiet=0, run=run_all_test):
    """ Test a cache factory containing multiple cache plugins. """
    if not run:
      return
    if not quiet:
      message = '\nTest combination of available cache plugins under a cache'\
                ' factory'
      ZopeTestCase._print(message)
      LOG('Testing... ',0,message)
      portal = self.getPortal()
      from Products.ERP5Type.Cache import CachingMethod
      py_script_id = "testCachedMethod"
      py_script_obj = getattr(portal, py_script_id)
      cf_name = 'erp5_user_factory'
      my_cache = CachingMethod(py_script_obj,
                               'py_script_obj',
                               cache_factory=cf_name)
      self._cacheFactoryInstanceTest(my_cache, cf_name)
  
  def _cacheFactoryInstanceTest(self, my_cache, cf_name):
      portal = self.getPortal()
      print 
      print "="*40
      print "TESTING:", cf_name
      portal.portal_caches.clearCacheFactory(cf_name)
      ## 1st call
      start = time.time()
      original =  my_cache(20000, portal_path=('', portal.getId()))
      end = time.time()
      calculation_time = end-start
      print "\n\tCalculation time (1st call)", calculation_time
      
      ## 2nd call - should be cached now
      start = time.time()
      cached =  my_cache(20000, portal_path=('', portal.getId()))
      end = time.time()
      calculation_time = end-start
      print "\n\tCalculation time (2nd call)", calculation_time

      # check if cache works by getting calculation_time for last cache
      # operation even remote cache must have access time less than a second.
      # if it's greater than method wasn't previously cached and was calculated
      # instead
      self.assert_(1.0 > calculation_time)
      
      ## check if equal.
      self.assertEquals(original, cached)
        
      ## OK so far let's clear cache
      portal.portal_caches.clearCacheFactory(cf_name)
        
      ## 1st call
      start = time.time()
      original =  my_cache(20000, portal_path=('', portal.getId()))
      end = time.time()
      calculation_time = end-start
      print "\n\tCalculation time (after cache clear)", calculation_time
      
      ## Cache  cleared shouldn't be previously cached
      self.assert_(1.0 < calculation_time)

if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestCacheTool))
        return suite

