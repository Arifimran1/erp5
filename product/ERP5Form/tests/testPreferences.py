##############################################################################
#
# Copyright (c) 2005 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jerome Perrin <jerome@nexedi.com>
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

from AccessControl.SecurityManagement import newSecurityManager
from zLOG import LOG
from DateTime import DateTime
from Testing import ZopeTestCase
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from Products.ERP5Form.Document.Preference import Priority


class TestPreferences(ERP5TypeTestCase):
  quiet = 0
  run_all_tests = 1
  
  def getTitle(self):
    return "Portal Preference"

  def getPreferenceTool(self) :
    return self.getPortal().portal_preferences
    
  def afterSetUp(self):
    uf = self.getPortal().acl_users
    uf._doAddUser('manager', '', ['Manager', 'Owner', 'Assignor'], [])
    user = uf.getUserById('manager').__of__(uf)
    newSecurityManager(None, user)
    if getattr(self.getPreferenceTool(), 'person1', None) is None :
      self.createPreferences()
  
  def createPreferences(self) :
    """ create some preferences objects  """
    portal_preferences = self.getPreferenceTool()
    ## create initial preferences
    person1 = portal_preferences.newContent(
        id='person1', portal_type='Preference')
    person2 = portal_preferences.newContent(
        id='person2', portal_type='Preference')
    group = portal_preferences.newContent(
        id='group', portal_type='Preference')
    group.setPriority(Priority.GROUP)
    site = portal_preferences.newContent(
        id='site', portal_type='Preference')
    site.setPriority(Priority.SITE)
    self.tic()
    # check preference levels are Ok
    self.assertEquals(person1.getPriority(), Priority.USER)
    self.assertEquals(person2.getPriority(), Priority.USER)
    self.assertEquals(group.getPriority(),   Priority.GROUP)
    self.assertEquals(site.getPriority(),    Priority.SITE)
    # check initial states
    self.assertEquals(person1.getPreferenceState(), 'disabled')
    self.assertEquals(person2.getPreferenceState(), 'disabled')
    self.assertEquals(group.getPreferenceState(),   'disabled')
    self.assertEquals(site.getPreferenceState(),    'disabled')
    
  def test_EnablePreferences(self, quiet=quiet, run=run_all_tests) :
    """ tests preference workflow """
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test enabling preferences')
    
    portal_workflow = self.getWorkflowTool()
    person1 = self.getPreferenceTool()['person1']
    person2 = self.getPreferenceTool()['person2']
    group = self.getPreferenceTool()['group']
    site = self.getPreferenceTool()['site']
    
    person1.portal_workflow.doActionFor(
       person1, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(person1.getPreferenceState(), 'enabled')
    
    portal_workflow.doActionFor(
       site, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(person1.getPreferenceState(), 'enabled')
    self.assertEquals(site.getPreferenceState(),    'enabled')

    portal_workflow.doActionFor(
       group, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(person1.getPreferenceState(), 'enabled')
    self.assertEquals(group.getPreferenceState(),   'enabled')
    self.assertEquals(site.getPreferenceState(),    'enabled')
    
    self.getPreferenceTool().recursiveImmediateReindexObject()
    
    portal_workflow.doActionFor(
       person2, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(person2.getPreferenceState(), 'enabled')
    # enabling a preference disable all other of the same level
    self.assertEquals(person1.getPreferenceState(), 'disabled')
    self.assertEquals(group.getPreferenceState(),   'enabled')
    self.assertEquals(site.getPreferenceState(),    'enabled')

  def test_GetPreference(self, quiet=quiet, run=run_all_tests):
    """ checks that getPreference returns the good preferred value"""
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test getPreference')
   
    portal_workflow = self.getWorkflowTool()
    pref_tool = self.getPreferenceTool()
    person1 = self.getPreferenceTool()['person1']
    group = self.getPreferenceTool()['group']
    site = self.getPreferenceTool()['site']
    
    portal_workflow.doActionFor(
       person1, 'enable_action', wf_id='preference_workflow')
    portal_workflow.doActionFor(
       group, 'enable_action', wf_id='preference_workflow')
    portal_workflow.doActionFor(
       site, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(person1.getPreferenceState(), 'enabled')
    self.assertEquals(group.getPreferenceState(),   'enabled')
    self.assertEquals(site.getPreferenceState(),    'enabled')
    person1.setPreferredAccountingTransactionSimulationState([])
    self.assertEquals(person1.getPreferredAccountingTransactionSimulationState(), None)
    group.setPreferredAccountingTransactionSimulationState([])
    self.assertEquals(group.getPreferredAccountingTransactionSimulationState(), None)
    site.setPreferredAccountingTransactionSimulationState([])
    self.assertEquals(site.getPreferredAccountingTransactionSimulationState(), None)

    from Products.ERP5Type.Cache import clearCache    
    clearCache()
    self.assertEquals(len(pref_tool.getPreference(
      'preferred_accounting_transaction_simulation_state')), 0)
    
    site.setPreferredAccountingTransactionSimulationStateList(
            ['stopped', 'delivered'])
    clearCache()
    self.assertEquals(list(pref_tool.getPreference(
      'preferred_accounting_transaction_simulation_state')),
      list(site.getPreferredAccountingTransactionSimulationStateList()))
    
    group.setPreferredAccountingTransactionSimulationStateList(['draft'])
    clearCache()
    self.assertEquals(list(pref_tool.getPreference(
      'preferred_accounting_transaction_simulation_state')),
      list(group.getPreferredAccountingTransactionSimulationStateList()))
    
    person1.setPreferredAccountingTransactionSimulationStateList(
              ['cancelled'])
    clearCache()
    self.assertEquals(list(pref_tool.getPreference(
      'preferred_accounting_transaction_simulation_state')),
      list(person1.getPreferredAccountingTransactionSimulationStateList()))
    # disable person -> group is selected
    self.getWorkflowTool().doActionFor(person1,
            'disable_action', wf_id='preference_workflow')
    clearCache()
    self.assertEquals(list(pref_tool.getPreference(
      'preferred_accounting_transaction_simulation_state')),
      list(group.getPreferredAccountingTransactionSimulationStateList()))

  def test_GetAttr(self, quiet=quiet, run=run_all_tests) :
    """ checks that preference methods can be called directly
      on portal_preferences """
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test methods on portal_preference')
      
    portal_workflow = self.getWorkflowTool()
    pref_tool = self.getPreferenceTool()
    person1 = self.getPreferenceTool()['person1']
    group = self.getPreferenceTool()['group']
    site = self.getPreferenceTool()['site']
    self.assertEquals(person1.getPreferenceState(), 'disabled')
    portal_workflow.doActionFor(
       group, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(group.getPreferenceState(),    'enabled')
    portal_workflow.doActionFor(
       site, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(site.getPreferenceState(),     'enabled')
    group.setPreferredAccountingTransactionSimulationStateList(['cancelled'])
    
    self.assertNotEquals( None,
      pref_tool.getPreferredAccountingTransactionSimulationStateList())
    self.assertNotEquals( [],
      list(pref_tool.getPreferredAccountingTransactionSimulationStateList()))
    self.assertEquals(
      list(pref_tool.getPreferredAccountingTransactionSimulationStateList()),
      list(pref_tool.getPreference(
            'preferred_accounting_transaction_simulation_state')))
    # standards attributes must not be looked up on Preferences
    self.assertNotEquals(pref_tool.getTitleOrId(), group.getTitleOrId())
    self.assertNotEquals(pref_tool.objectValues(), group.objectValues())
    self.assertNotEquals(pref_tool.aq_parent, group.aq_parent)
    try :
      pref_tool.getPreferredNotExistingPreference()
      self.assertNotEquals(1, 2)
    except AttributeError :
      pass
  
  def test_SetPreference(self, quiet=quiet, run=run_all_tests) :
    """ check setting a preference modifies 
     the first enabled user preference """
    if not run: return
    if not quiet:
      ZopeTestCase._print('\n Test setting preferences')
    
    portal_workflow = self.getWorkflowTool()
    pref_tool = self.getPreferenceTool()
    person1 = self.getPreferenceTool()['person1']
    
    portal_workflow.doActionFor(
       person1, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(person1.getPreferenceState(),    'enabled')
    person1.setPreferredAccountingTransactionAtDate(DateTime(2005, 01, 01))
    pref_tool.setPreference(
      'preferred_accounting_transaction_at_date', DateTime(2004, 12, 31))
    self.tic()
    self.assertEquals(
      pref_tool.getPreferredAccountingTransactionAtDate(),
      DateTime(2004, 12, 31))
    self.assertEquals(
      person1.getPreferredAccountingTransactionAtDate(),
      DateTime(2004, 12, 31))

  def test_UserIndependance(self, quiet=quiet, run=run_all_tests) :
    """ check that the preferences are related to the user. """
    if not run: return
    if not quiet:
      ZopeTestCase._print(
          '\n Test different users preferences are independants')
    
    portal_workflow = self.getWorkflowTool()
    portal_preferences = self.getPreferenceTool()
    # create 2 users: user_a and user_b
    uf = self.getPortal().acl_users
    uf._doAddUser('user_a', '', ['Manager', 'Assignor'], [])
    user_a = uf.getUserById('user_a').__of__(uf)
    uf._doAddUser('user_b', '', ['Manager', 'Assignor'], [])
    user_b = uf.getUserById('user_b').__of__(uf)
    
    # log as user_a 
    newSecurityManager(None, user_a)
    
    # create 2 prefs as user_a
    user_a_1 = portal_preferences.newContent(
        id='user_a_1', portal_type='Preference')
    user_a_2 = portal_preferences.newContent(
        id='user_a_2', portal_type='Preference')

    # enable a pref
    portal_workflow.doActionFor(
       user_a_1, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(user_a_1.getPreferenceState(), 'enabled')
    self.assertEquals(user_a_2.getPreferenceState(), 'disabled')
    
    # log as user_b
    newSecurityManager(None, user_b)
    
    # create a pref for user_b
    user_b_1 = portal_preferences.newContent(
        id='user_b_1', portal_type='Preference')
    user_b_1.setPreferredAccountingTransactionAtDate(DateTime(2002, 02, 02))
    
    # enable this preference
    portal_workflow.doActionFor(
       user_b_1, 'enable_action', wf_id='preference_workflow')
    self.assertEquals(user_b_1.getPreferenceState(), 'enabled')
    
    # check user_a's preference is still enabled
    self.assertEquals(user_a_1.getPreferenceState(), 'enabled')
    self.assertEquals(user_a_2.getPreferenceState(), 'disabled')

if __name__ == '__main__':
  framework()
else:
  import unittest
  def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPreferences))
    return suite
