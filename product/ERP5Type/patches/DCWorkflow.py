##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
# Copyright (c) 2002,2005 Nexedi SARL and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

# Optimized rendering of global actions (cache)

from Globals import DTMLFile
from Products.ERP5Type import _dtmldir
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition, StateChangeInfo, ObjectMoved, createExprContext, aq_parent, aq_inner
from Products.DCWorkflow import DCWorkflow
from Products.DCWorkflow.Transitions import TRIGGER_WORKFLOW_METHOD, TransitionDefinition
from AccessControl import getSecurityManager, ClassSecurityInfo, ModuleSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import  _getAuthenticatedUser
from DocumentTemplate.DT_Util import TemplateDict
from DateTime import DateTime
from Products.ERP5Type.Cache import CachingMethod
from Products.ERP5Type.Cache import DEFAULT_CACHE_FACTORY
from Products.ERP5Type.Utils import convertToMixedCase
from string import join
from zLOG import LOG



# Patch WorkflowUIMixin to add description on workflows
from Products.DCWorkflow.WorkflowUIMixin import WorkflowUIMixin as WorkflowUIMixin_class
from Products.DCWorkflow.Guard import Guard

# patched to add a description on worklist for ERP5 Web, and to add the cache
# control for worklists
def WorkflowUIMixin_setProperties( self, title, description='',
            cache_factory_id='', manager_bypass=0, props=None, REQUEST=None):
  """Sets basic properties.
  """
  self.title = str(title)
  self.description = str(description)
  self.manager_bypass = manager_bypass and 1 or 0
  self.cache_factory_id = cache_factory_id
  g = Guard()
  if g.changeFromProperties(props or REQUEST):
      self.creation_guard = g
  else:
      self.creation_guard = None
  if REQUEST is not None:
      return self.manage_properties(
          REQUEST, manage_tabs_message='Properties changed.')

WorkflowUIMixin_class.setProperties = WorkflowUIMixin_setProperties
WorkflowUIMixin_class.manage_properties = DTMLFile('workflow_properties', _dtmldir)


DCWorkflowDefinition_listGlobalActions_original = DCWorkflowDefinition.listGlobalActions

def DCWorkflowDefinition_listGlobalActions(self, info):
    '''
    Allows this workflow to
    include actions to be displayed in the actions box.
    Called on every request.
    Returns the actions to be displayed to the user.
    '''
    if not self.worklists:
      return None  # Optimization

    portal = self._getPortalRoot()
    def _listGlobalActions(user=None, id=None, portal_path=None):
      sm = getSecurityManager()
      res = []
      fmt_data = None
      # We want to display some actions depending on the current date
      # So, we can now put this kind of expression : <= "%(now)s"
      # May be this patch should be moved to listFilteredActions in the future
      info.now = DateTime()
      for id, qdef in self.worklists.items():
          if qdef.actbox_name:
              guard = qdef.guard
              dict = {}
              # Patch for ERP5 by JP Smets in order
              # to implement worklists and search of local roles
              searchres_len = 0
              var_match_keys = qdef.getVarMatchKeys()
              if var_match_keys:
                  # Check the catalog for items in the worklist.
                  catalog = getToolByName(self, 'portal_catalog')
                  for k in var_match_keys:
                      v = qdef.getVarMatch(k)
                      v_fmt = map(lambda x, info=info: x%info, v)
                      dict[k] = v_fmt
                  # Patch for ERP5 by JP Smets in order
                  # to implement worklists and search of local roles
                  if not (guard is None or guard.check(sm, self, portal)):
                      dict['local_roles'] = guard.roles
                  # Patch to use ZSQLCatalog and get high speed
                  searchres_len = int(apply(catalog.countResults, (), dict)[0][0])
                  if searchres_len == 0:
                      continue
              if fmt_data is None:
                  fmt_data = TemplateDict()
                  fmt_data._push(info)
              fmt_data._push({'count': searchres_len})
              # Patch for ERP5 by JP Smets in order
              # to implement worklists and search of local roles
              if dict.has_key('local_roles'):
                fmt_data._push({'local_roles': join(guard.roles,';')})
              else:
                fmt_data._push({'local_roles': ''})
              res.append((id, {'name': qdef.actbox_name % fmt_data,
                              'url': qdef.actbox_url % fmt_data,
                              'worklist_id': id,
                              'workflow_title': self.title,
                              'workflow_id': self.id,
                              'permissions': (),  # Predetermined.
                              'category': qdef.actbox_category}))
              fmt_data._pop()
      res.sort()
      return map((lambda (id, val): val), res)

    cache_tool = getToolByName(self, 'portal_caches', None)
    if cache_tool is not None:
      # If we have a cache factory controlling this workflow's worklist cache
      cache_factory = getattr(self, 'cache_factory_id', DEFAULT_CACHE_FACTORY)
      _listGlobalActions = CachingMethod(_listGlobalActions,
                                         id='%s_listGlobalActions' % self.id,
                                         cache_factory=cache_factory)
      user = str(_getAuthenticatedUser(self))
      return _listGlobalActions(user=user, portal_path=portal.getPhysicalPath())
    else:
      return DCWorkflowDefinition_listGlobalActions_original(self, info)

DCWorkflowDefinition.listGlobalActions = DCWorkflowDefinition_listGlobalActions

class ValidationFailed(Exception):
    """Transition can not be executed because data is not in consistent state"""
    def __init__(self, message_instance=None):
        """
        Redefine init in order to register the message class instance
        """
        Exception.__init__(self, message_instance)
        self.msg = message_instance

DCWorkflow.ValidationFailed = ValidationFailed

ModuleSecurityInfo('Products.DCWorkflow.DCWorkflow').declarePublic('ValidationFailed')



# Patch excecuteTransition from DCWorkflowDefinition, to put ValidationFailed
# error messages in workflow history.
def DCWorkflowDefinition_executeTransition(self, ob, tdef=None, kwargs=None):
    '''
    Private method.
    Puts object in a new state.
    '''
    sci = None
    econtext = None
    moved_exc = None
    validation_exc = None

    # Figure out the old and new states.
    old_sdef = self._getWorkflowStateOf(ob)
    old_state = old_sdef.getId()
    if tdef is None:
        new_state = self.initial_state
        former_status = {}
    else:
        new_state = tdef.new_state_id
        if not new_state:
            # Stay in same state.
            new_state = old_state
        former_status = self._getStatusOf(ob)
    new_sdef = self.states.get(new_state, None)
    if new_sdef is None:
        raise WorkflowException, (
            'Destination state undefined: ' + new_state)

    # Execute the "before" script.
    before_script_success = 1
    if tdef is not None and tdef.script_name:
        script = self.scripts[tdef.script_name]
        # Pass lots of info to the script in a single parameter.
        sci = StateChangeInfo(
            ob, self, former_status, tdef, old_sdef, new_sdef, kwargs)
        try:
            #LOG('_executeTransition', 0, "script = %s, sci = %s" % (repr(script), repr(sci)))
            script(sci)  # May throw an exception.
        except ValidationFailed, validation_exc:
            before_script_success = 0
            before_script_error_message = validation_exc.msg
        except ObjectMoved, moved_exc:
            ob = moved_exc.getNewObject()
            # Re-raise after transition

    # Update variables.
    state_values = new_sdef.var_values
    if state_values is None: state_values = {}
    tdef_exprs = None
    if tdef is not None: tdef_exprs = tdef.var_exprs
    if tdef_exprs is None: tdef_exprs = {}
    status = {}
    for id, vdef in self.variables.items():
        if not vdef.for_status:
            continue
        expr = None
        if state_values.has_key(id):
            value = state_values[id]
        elif tdef_exprs.has_key(id):
            expr = tdef_exprs[id]
        elif not vdef.update_always and former_status.has_key(id):
            # Preserve former value
            value = former_status[id]
        else:
            if vdef.default_expr is not None:
                expr = vdef.default_expr
            else:
                value = vdef.default_value
        if expr is not None:
            # Evaluate an expression.
            if econtext is None:
                # Lazily create the expression context.
                if sci is None:
                    sci = StateChangeInfo(
                        ob, self, former_status, tdef,
                        old_sdef, new_sdef, kwargs)
                econtext = createExprContext(sci)
            value = expr(econtext)
        status[id] = value

    # Do not proceed in case of failure of before script
    if not before_script_success:
        status[self.state_var] = old_state # Remain in state
        tool = aq_parent(aq_inner(self))
        tool.setStatusOf(self.id, ob, status)
        sci = StateChangeInfo(
            ob, self, status, tdef, old_sdef, new_sdef, kwargs)
        # put the error message in the workflow history
        sci.setWorkflowVariable(ob, workflow_id=self.id,
                                error_message = before_script_error_message)
        if validation_exc :
            # reraise validation failed exception
            raise validation_exc
        return new_sdef

    # Update state.
    status[self.state_var] = new_state
    tool = aq_parent(aq_inner(self))
    tool.setStatusOf(self.id, ob, status)

    # Update role to permission assignments.
    self.updateRoleMappingsFor(ob)

    # Execute the "after" script.
    if tdef is not None and tdef.after_script_name:
        # Script can be either script or workflow method
        #LOG('_executeTransition', 0, 'new_sdef.transitions = %s' % (repr(new_sdef.transitions)))
        if tdef.after_script_name in filter(lambda k: self.transitions[k].trigger_type == TRIGGER_WORKFLOW_METHOD,
                                                                                  new_sdef.transitions):
          script = getattr(ob, convertToMixedCase(tdef.after_script_name))
          script()
        else:
          script = self.scripts[tdef.after_script_name]
          # Pass lots of info to the script in a single parameter.
          sci = StateChangeInfo(
              ob, self, status, tdef, old_sdef, new_sdef, kwargs)
          script(sci)  # May throw an exception.

    # Return the new state object.
    if moved_exc is not None:
        # Propagate the notification that the object has moved.
        raise moved_exc
    else:
        return new_sdef


DCWorkflowDefinition._executeTransition = DCWorkflowDefinition_executeTransition
from Products.DCWorkflow.utils import modifyRolesForPermission

# Patch updateRoleMappingsFor so that if 2 workflows define security, then we
# should do an AND operation between each permission
def updateRoleMappingsFor(self, ob):
    '''
    Changes the object permissions according to the current
    state.
    '''
    changed = 0
    sdef = self._getWorkflowStateOf(ob)

    tool = aq_parent(aq_inner(self))
    other_workflow_list = \
       [x for x in tool.getWorkflowsFor(ob) if x.id != self.id and isinstance(x,DCWorkflowDefinition)]
    other_data_list = []
    for other_workflow in other_workflow_list:
      other_sdef = other_workflow._getWorkflowStateOf(ob)
      if other_sdef is not None and other_sdef.permission_roles is not None:
        other_data_list.append((other_workflow,other_sdef))
    # Be carefull, permissions_roles should not change
    # from list to tuple or vice-versa. (in modifyRolesForPermission,
    # list means acquire roles, tuple means do not acquire)
    if sdef is not None and self.permissions:
        for p in self.permissions:
            roles = []
            refused_roles = []
            role_type = 'list'
            if sdef.permission_roles is not None:
                roles = sdef.permission_roles.get(p, roles)
                if type(roles) is type(()):
                  role_type = 'tuple'
                roles = list(roles)
            # We will check that each role is activated
            # in each DCWorkflow
            for other_workflow,other_sdef in other_data_list:
              if p in other_workflow.permissions:
                other_roles = other_sdef.permission_roles.get(p, [])
                if type(other_roles) is type(()) :
                  role_type = 'tuple'
                for role in roles:
                  if role not in other_roles :
                    refused_roles.append(role)
            for role in refused_roles :
              if role in roles :
                roles.remove(role)
            if role_type=='tuple':
              roles = tuple(roles)
            if modifyRolesForPermission(ob, p, roles):
                changed = 1
    return changed

DCWorkflowDefinition.updateRoleMappingsFor = updateRoleMappingsFor

# This patch allows to update all objects using one workflow, for example
# after the permissions per state for this workflow were modified
def updateRoleMappings(self, REQUEST=None):
  """
  Changes permissions of all objects related to this workflow
  """
  wf_tool = aq_parent(aq_inner(self))
  chain_by_type = wf_tool._chains_by_type
  type_info_list = wf_tool._listTypeInfo()
  wf_id = self.id
  portal_type_list = []
  # get the list of portal types to update
  if wf_id in wf_tool._default_chain:
    include_default = 1
  else:
    include_default = 0
  for type_info in type_info_list:
    tid = type_info.getId()
    if chain_by_type.has_key(tid):
      if wf_id in chain_by_type[tid]:
        portal_type_list.append(tid)
    elif include_default == 1:
      portal_type_list.append(tid)

  count = 0
  #update the objects using these portal types
  if len(portal_type_list) > 0:
    portal_catalog = self.portal_catalog
    for brain in portal_catalog(portal_type=portal_type_list):
      obj = brain.getObject()
      self.updateRoleMappingsFor(obj)
      count += 1

  if REQUEST is not None:
    return self.manage_properties(REQUEST,
        manage_tabs_message='%d object(s) updated.' % count)
  else:
    return count

DCWorkflowDefinition.updateRoleMappings = updateRoleMappings

# This patch allows to use workflowmethod as an after_script
# However, the right way of doing would be to have a combined state of TRIGGER_USER_ACTION and TRIGGER_WORKFLOW_METHOD
# as well as workflow inheritance. This way, different user actions and dialogs can be specified easliy
# For now, we split UI transitions and logics transitions so that UI can be different and logics the same

class ERP5TransitionDefinition (TransitionDefinition):
  """
    This class is only for backward compatibility.
  """
  pass

def getAvailableScriptIds(self):
  return self.getWorkflow().scripts.keys() + \
   [k for k in self.getWorkflow().transitions.keys() if \
   self.getWorkflow().transitions[k].trigger_type == TRIGGER_WORKFLOW_METHOD]

TransitionDefinition.getAvailableScriptIds = getAvailableScriptIds

# Add a workflow factory for ERP5 style workflow, because some variables
# are needed for History tab.
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.ERP5Type import Permissions

def setupERP5Workflow(wf):
  """Sets up an DC Workflow with defaults variables needed by ERP5.
  """
  wf.setProperties(title='ERP5 default workflow')
  for s in ('draft',):
    wf.states.addState(s)
  for v in ('action', 'actor', 'comment', 'history', 'time',
            'error_message', 'portal_type'):
    wf.variables.addVariable(v)
  for perm in (Permissions.AccessContentsInformation,
               Permissions.View,
               Permissions.AddPortalContent,
               Permissions.ModifyPortalContent,
               Permissions.DeleteObjects):
    wf.addManagedPermission(perm)

  wf.states.setInitialState('draft')
  # set by default the state variable to simulation_state.
  # anyway, a default workflow needs to be configured.
  wf.variables.setStateVar('simulation_state')

  vdef = wf.variables['action']
  vdef.setProperties(description='The last transition',
                     default_expr='transition/getId|nothing',
                     for_status=1, update_always=1)

  vdef = wf.variables['actor']
  vdef.setProperties(description='The name of the user who performed '
                     'the last transition',
                     default_expr='user/getUserName',
                      for_status=1, update_always=1)

  vdef = wf.variables['comment']
  vdef.setProperties(description='Comments about the last transition',
               default_expr="python:state_change.kwargs.get('comment', '')",
               for_status=1, update_always=1)

  vdef = wf.variables['history']
  vdef.setProperties(description='Provides access to workflow history',
                     default_expr="state_change/getHistory")

  vdef = wf.variables['time']
  vdef.setProperties(description='Time of the last transition',
                     default_expr="state_change/getDateTime",
                     for_status=1, update_always=1)

  vdef = wf.variables['error_message']
  vdef.setProperties(description='Error message if validation failed',
                     for_status=1, update_always=1)
  
  vdef = wf.variables['portal_type']
  vdef.setProperties(description='portal type (use as filter for worklists)',
                     for_catalog=1)

def createERP5Workflow(id):
  """Creates an ERP5 Workflow """
  ob = DCWorkflowDefinition(id)
  setupERP5Workflow(ob)
  return ob

addWorkflowFactory(createERP5Workflow,
                   id='erp5_workflow',
                   title='ERP5-style empty workflow')


