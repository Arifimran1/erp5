##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
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

import socket, asyncore, urllib
from Products.CMFCore import CMFCorePermissions
from Products.ERP5Type.Document.Folder import Folder
from Products.ERP5Type.Utils import getPath
from Products.ERP5Type.Error import Error
from Products.PythonScripts.Utility import allow_class
from App.ApplicationManager import ApplicationManager
from AccessControl import ClassSecurityInfo, Permissions
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import UniqueObject, _checkPermission, _getAuthenticatedUser, getToolByName
from Globals import InitializeClass, DTMLFile, get_request
from Acquisition import aq_base
from DateTime.DateTime import DateTime
from Products.CMFActivity.ActiveObject import DISTRIBUTABLE_STATE, INVOKE_ERROR_STATE, VALIDATE_ERROR_STATE
from ActivityBuffer import ActivityBuffer
from AccessControl.SecurityManagement import newSecurityManager
import threading
import sys
from ZODB.POSException import ConflictError
from OFS.Traversable import NotFound

from zLOG import LOG, INFO, WARNING

try:
  from Products.TimerService import getTimerService
except ImportError:
  def getTimerService(self):
    pass

# Using a RAM property (not a property of an instance) allows
# to prevent from storing a state in the ZODB (and allows to restart...)
active_threads = 0
max_active_threads = 1 # 2 will cause more bug to appear (he he)
is_initialized = 0
tic_lock = threading.Lock() # A RAM based lock

# Activity Registration
activity_dict = {}
activity_list = []

def registerActivity(activity):
  # Must be rewritten to register
  # class and create instance for each activity
  #LOG('Init Activity', 0, str(activity.__name__))
  activity_instance = activity()
  activity_list.append(activity_instance)
  activity_dict[activity.__name__] = activity_instance

class Message:

  def __init__(self, object, active_process, activity_kw, method_id, args, kw):
    if type(object) is type('a'):
      self.object_path = object.split('/')
    else:
      self.object_path = object.getPhysicalPath()
    if type(active_process) is type('a'):
      self.active_process = active_process.split('/')
    elif active_process is None:
      self.active_process = None
    else:
      self.active_process = active_process.getPhysicalPath()
      self.active_process_uid = active_process.getUid()
    self.activity_kw = activity_kw
    self.method_id = method_id
    self.args = args
    self.kw = kw
    self.is_executed = 0
    self.exc_type = None
    self.user_name = str(_getAuthenticatedUser(self))
    # Store REQUEST Info ?

  def getObject(self, activity_tool):
    return activity_tool.unrestrictedTraverse(self.object_path)
    
  def getObjectList(self, activity_tool):
    try:
      expand_method_id = self.activity_kw['expand_method_id']
      obj = self.getObject(activity_tool)
      # FIXME: how to pass parameters?
      object_list = getattr(obj, expand_method_id)()
    except KeyError:
      object_list = [self.getObject(activity_tool)]
      
    return object_list
      
  def hasExpandMethod(self):
    return self.activity_kw.has_key('expand_method_id')
    
  def changeUser(self, user_name, activity_tool):
    uf = activity_tool.getPortalObject().acl_users
    user = uf.getUserById(user_name)
    if user is not None:
      user = user.__of__(uf)
      newSecurityManager(None, user)
    return user

  def activateResult(self, activity_tool, result, object):
    if self.active_process is not None:
      active_process = activity_tool.unrestrictedTraverse(self.active_process)
      if isinstance(result,Error):
        result.edit(object_path=object)
        result.edit(method_id=self.method_id)
        active_process.activateResult(result) # XXX Allow other method_id in future
      else:
        active_process.activateResult(Error(object_path=object,method_id=self.method_id,result=result)) # XXX Allow other method_id in future
  
  def __call__(self, activity_tool):
    try:
#       LOG('WARNING ActivityTool', 0,
#            'Trying to call method %s on object %s' % (self.method_id, self.object_path))
      obj = self.getObject(activity_tool)
      # Change user if required (TO BE DONE)
      # We will change the user only in order to execute this method
      current_user = str(_getAuthenticatedUser(self))
      user = self.changeUser(self.user_name, activity_tool)
      try:
        result = getattr(obj, self.method_id)(*self.args, **self.kw)
      finally:
        # Use again the previous user
        if user is not None:
          self.changeUser(current_user, activity_tool)
      self.activateResult(activity_tool, result, obj)
      self.is_executed = 1
    except:
      self.is_executed = 0
      self.exc_type = sys.exc_info()[0]
      LOG('WARNING ActivityTool', 0,
          'Could not call method %s on object %s' % (self.method_id, self.object_path), error=sys.exc_info())

  def validate(self, activity, activity_tool):
    return activity.validate(activity_tool, self, **self.activity_kw)

  def notifyUser(self, activity_tool, message="Failed Processing Activity"):
    #LOG('notifyUser begin', 0, str(self.user_name))
    user_email = activity_tool.portal_membership.getMemberById(self.user_name).getProperty('email')
    if user_email in ('', None):
      user_email = activity_tool.email_from_address
    #LOG('notifyUser user_email', 0, str(user_email))
    mail_text = """From: %s
To: %s
Subject: %s

%s

Document: %s
Method: %s
    """ % (activity_tool.email_from_address, user_email,
           message, message, '/'.join(self.object_path), self.method_id)
    #LOG('notifyUser mail_text', 0, str(mail_text))
    activity_tool.MailHost.send( mail_text )
    #LOG('notifyUser send', 0, '')

  def reactivate(self, activity_tool):
    # Reactivate the original object.
    obj= self.getObject(activity_tool)
    # Change user if required (TO BE DONE)
    # We will change the user only in order to execute this method
    current_user = str(_getAuthenticatedUser(self))
    user = self.changeUser(self.user_name, activity_tool)
    try:
      active_obj = obj.activate(**self.activity_kw)
      getattr(active_obj, self.method_id)(*self.args, **self.kw)
    finally:
      # Use again the previous user
      if user is not None:
        self.changeUser(current_user, activity_tool)

class Method:

  def __init__(self, passive_self, activity, active_process, kw, method_id):
    self.__passive_self = passive_self
    self.__activity = activity
    self.__active_process = active_process
    self.__kw = kw
    self.__method_id = method_id

  def __call__(self, *args, **kw):
    m = Message(self.__passive_self, self.__active_process, self.__kw, self.__method_id, args, kw)
    activity_dict[self.__activity].queueMessage(self.__passive_self.portal_activities, m)

allow_class(Method)

class ActiveWrapper:

  def __init__(self, passive_self, activity, active_process, **kw):
    self.__dict__['__passive_self'] = passive_self
    self.__dict__['__activity'] = activity
    self.__dict__['__active_process'] = active_process
    self.__dict__['__kw'] = kw

  def __getattr__(self, id):
    return Method(self.__dict__['__passive_self'], self.__dict__['__activity'],
                  self.__dict__['__active_process'],
                  self.__dict__['__kw'], id)

class ActivityTool (Folder, UniqueObject):
    """
    ActivityTool is the central point for activity management.

    Improvement to consider to reduce locks:

      Idea 1: create an SQL tool which accumulate queries and executes them at the end of a transaction,
              thus allowing all SQL transaction to happen in a very short time
              (this would also be a great way of using MyISAM tables)

      Idea 2: do the same at the level of ActivityTool

      Idea 3: do the same at the level of each activity (ie. queueMessage
              accumulates and fires messages at the end of the transactino)
    """
    id = 'portal_activities'
    meta_type = 'CMF Activity Tool'
    portal_type = 'Activity Tool'
    allowed_types = ( 'CMF Active Process', )
    security = ClassSecurityInfo()

    _distributingNode = ''
    _nodes = ()

    manage_options = tuple(
                     [ { 'label' : 'Overview', 'action' : 'manage_overview' }
                     , { 'label' : 'Activities', 'action' : 'manageActivities' }
                     , { 'label' : 'LoadBalancing', 'action' : 'manageLoadBalancing'}
                     , { 'label' : 'Advanced', 'action' : 'manageActivitiesAdvanced' }
                     ,
                     ] + list(Folder.manage_options))

    security.declareProtected( CMFCorePermissions.ManagePortal , 'manageActivities' )
    manageActivities = DTMLFile( 'dtml/manageActivities', globals() )

    security.declareProtected( CMFCorePermissions.ManagePortal , 'manageActivitiesAdvanced' )
    manageActivitiesAdvanced = DTMLFile( 'dtml/manageActivitiesAdvanced', globals() )

    security.declareProtected( CMFCorePermissions.ManagePortal , 'manage_overview' )
    manage_overview = DTMLFile( 'dtml/explainActivityTool', globals() )
    
    security.declareProtected( CMFCorePermissions.ManagePortal , 'manageLoadBalancing' )
    manageLoadBalancing = DTMLFile( 'dtml/manageLoadBalancing', globals() )
    
    distributingNode = ''
    _nodes = ()

    def __init__(self):
        return Folder.__init__(self, ActivityTool.id)

    # Filter content (ZMI))
    def filtered_meta_types(self, user=None):
        # Filters the list of available meta types.
        all = ActivityTool.inheritedAttribute('filtered_meta_types')(self)
        meta_types = []
        for meta_type in self.all_meta_types():
            if meta_type['name'] in self.allowed_types:
                meta_types.append(meta_type)
        return meta_types

    def initialize(self):
      global is_initialized
      from Activity import RAMQueue, RAMDict, SQLQueue, SQLDict
      # Initialize each queue
      for activity in activity_list:
        activity.initialize(self)
      is_initialized = 1
      
    security.declareProtected(Permissions.manage_properties, 'isSubscribed')
    def isSubscribed(self):
        """"
        return True, if we are subscribed to TimerService.
        Otherwise return False.
        """
        service = getTimerService(self)
        if not service:
            LOG('ActivityTool', INFO, 'TimerService not available')
            return False
        
        path = '/'.join(self.getPhysicalPath())
        if path in service.lisSubscriptions():
            return True
        return False

    security.declareProtected(Permissions.manage_properties, 'subscribe')
    def subscribe(self):
        """ subscribe to the global Timer Service """
        service = getTimerService(self)
        url = '%s/manageLoadBalancing?manage_tabs_message=' %self.absolute_url()
        if not service:
            LOG('ActivityTool', INFO, 'TimerService not available')
            url += urllib.quote('TimerService not available')
        else:
            service.subscribe(self)
            url += urllib.quote("Subscribed to Timer Service")
        return self.REQUEST.RESPONSE.redirect(url)

    security.declareProtected(Permissions.manage_properties, 'unsubscribe')
    def unsubscribe(self):
        """ unsubscribe from the global Timer Service """
        service = getTimerService(self)
        url = '%s/manageLoadBalancing?manage_tabs_message=' %self.absolute_url()
        if not service:
            LOG('ActivityTool', INFO, 'TimerService not available')
            url += urllib.quote('TimerService not available')
        else:
            service.unsubscribe(self)
            url += urllib.quote("Unsubscribed from Timer Service")
        return self.REQUEST.RESPONSE.redirect(url)

    def manage_beforeDelete(self, item, container):
        self.unsubscribe()
        Folder.inheritedAttribute('manage_beforeDelete')(self, item, container)
    
    def manage_afterAdd(self, item, container):
        self.subscribe()
        Folder.inheritedAttribute('manage_afterAdd')(self, item, container)
       
    def getCurrentNode(self):
        """ Return current node in form ip:port """
        port = ''
        from asyncore import socket_map
        for k, v in socket_map.items():
            if hasattr(v, 'port'):
                # see Zope/lib/python/App/ApplicationManager.py: def getServers(self)
                type = str(getattr(v, '__class__', 'unknown'))
                if type == 'ZServer.HTTPServer.zhttp_server':
                    port = v.port
                    break
        ip = socket.gethostbyname(socket.gethostname())
        currentNode = '%s:%s' %(ip, port)
        return currentNode
        
    security.declarePublic('getDistributingNode')
    def getDistributingNode(self):
        """ Return the distributingNode """
        return self.distributingNode

    security.declarePublic('getNodeList')
    def getNodes(self):
        """ Return all nodes """
        return self._nodes

    security.declarePublic('manage_setDistributingNode')
    def manage_setDistributingNode(self, distributingNode, REQUEST=None):
        """ set the distributing node """
        self.distributingNode = distributingNode
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(
                REQUEST.URL1 +
                '/manageLoadBalancing?manage_tabs_message=' +
                urllib.quote("Distributing Node successfully changed."))
    
    security.declarePublic('manage_addNode')
    def manage_addNode(self, node, REQUEST=None):
        """ add a node """
        if node in self._nodes:
            if REQUEST is not None:
                REQUEST.RESPONSE.redirect(
                    REQUEST.URL1 +
                    '/manageLoadBalancing?manage_tabs_message=' +
                    urllib.quote("Node exists already."))
            return
            
        self._nodes = self._nodes + (node,)
        
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(
                REQUEST.URL1 +
                '/manageLoadBalancing?manage_tabs_message=' +
                urllib.quote("Node successfully added."))
                        
    security.declarePublic('manage_delNode')
    def manage_delNode(self, deleteNodes, REQUEST=None):
        """ delete nodes """
        nodeList = list(self._nodes)
        for node in deleteNodes:
            if node in self._nodes:
                nodeList.remove(node)
        self._nodes = tuple(nodeList)
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(
                REQUEST.URL1 +
                '/manageLoadBalancing?manage_tabs_message=' +
                urllib.quote("Node(s) successfully deleted."))
        
    def process_timer(self, tick, interval):
        """ 
        Call distribute() if we are the Distributing Node and call tic()
        with our node number.
        This method is called by TimerService in the interval given
        in zope.conf. The Default is every 5 seconds.
        """
        
        # get owner of portal_catalog, so normally we should be able to
        # have the permission to invoke all activities
        user = self.portal_catalog.getOwner()
        newSecurityManager(self.REQUEST, user)
        
        currentNode = self.getCurrentNode()
        
        # only distribute when we are the distributingNode or if it's empty
        if (self.distributingNode == self.getCurrentNode()):
            self.distribute(len(self._nodes))
            #LOG('CMFActivity:', INFO, 'self.distribute(node_count=%s)' %len(self._nodes))

        elif not self.distributingNode:
            self.distribute(1)
            #LOG('CMFActivity:', INFO, 'distributingNodes empty! Calling distribute(1)')
        
        # call tic for the current processing_node
        # the processing_node numbers are the indices of the elements in the node tuple +1
        # because processing_node starts form 1
        if currentNode in self._nodes:
            self.tic(list(self._nodes).index(currentNode)+1)
            #LOG('CMFActivity:', INFO, 'self.tic(processing_node=%s)' %str(list(self._nodes).index(currentNode)+1))
            
        elif len(self._nodes) == 0:
            self.tic(1)
            #LOG('CMFActivity:', INFO, 'Node List is empty! Calling tic(1)')


    security.declarePublic('distribute')
    def distribute(self, node_count=1):
      """
        Distribute load
      """
      # Initialize if needed
      if not is_initialized: self.initialize()

      # Call distribute on each queue
      for activity in activity_list:
        try:
          activity.distribute(self, node_count)
        except ConflictError:
          raise
        except:
          LOG('CMFActivity:', 100, 'Core call to distribute failed for activity %s' % activity, error=sys.exc_info())

    security.declarePublic('tic')
    def tic(self, processing_node=1, force=0):
      """
        Starts again an activity
        processing_node starts from 1 (there is not node 0)
      """
      global active_threads, is_initialized

      # return if the number of threads is too high
      tic_lock.acquire()
      too_many_threads = (active_threads >= max_active_threads)
      tic_lock.release()
      if too_many_threads :
        if not force:
          raise RuntimeError, 'Too many threads'

      if tic_lock is None:
        return

      # Initialize if needed
      if not is_initialized: self.initialize()

      # increase the number of active_threads
      tic_lock.acquire()
      active_threads += 1
      tic_lock.release()

      try:
        # Wakeup each queue
        for activity in activity_list:
          try:
            activity.wakeup(self, processing_node)
          except ConflictError:
            raise
          except:
            LOG('CMFActivity:', 100, 'Core call to wakeup failed for activity %s' % activity)
  
        # Process messages on each queue in round robin
        has_awake_activity = 1
        while has_awake_activity:
          has_awake_activity = 0
          for activity in activity_list:
            try:
              activity.tic(self, processing_node) # Transaction processing is the responsability of the activity
              has_awake_activity = has_awake_activity or activity.isAwake(self, processing_node)
              #LOG('ActivityTool tic', 0, 'has_awake_activity = %r, activity = %r, activity.isAwake(self, processing_node) = %r' % (has_awake_activity, activity, activity.isAwake(self, processing_node)))
            except ConflictError:
              raise
            except:
              LOG('CMFActivity:', 100, 'Core call to tic or isAwake failed for activity %s' % activity, error=sys.exc_info())
      finally:
        # decrease the number of active_threads
        tic_lock.acquire()
        active_threads -= 1
        tic_lock.release()

    def hasActivity(self, *args, **kw):
      # Check in each queue if the object has deferred tasks
      # if not argument is provided, then check on self
      if len(args) > 0:
        object = args[0]
      else:
        object = self
      for activity in activity_list:
        if activity.hasActivity(self, object, **kw):
          return 1
      return 0

    def activate(self, object, activity, active_process, **kw):
      global is_initialized
      if not is_initialized: self.initialize()
      if not hasattr(self, '_v_activity_buffer'): self._v_activity_buffer = ActivityBuffer()
      return ActiveWrapper(object, activity, active_process, **kw)

    def deferredQueueMessage(self, activity, message):
      self._v_activity_buffer.deferredQueueMessage(self, activity, message)

    def deferredDeleteMessage(self, activity, message):
      if not hasattr(self, '_v_activity_buffer'): self._v_activity_buffer = ActivityBuffer()
      self._v_activity_buffer.deferredDeleteMessage(self, activity, message)

    def getRegisteredMessageList(self, activity):
      activity_buffer = getattr(self, '_v_activity_buffer', None)
      #if getattr(self, '_v_activity_buffer', None):
      if activity_buffer is not None:
        activity_buffer._register() # This is required if flush flush is called outside activate
        return activity.getRegisteredMessageList(self._v_activity_buffer, self)
      else:
        return []

    def unregisterMessage(self, activity, message):
      self._v_activity_buffer._register() # Required if called by flush, outside activate
      return activity.unregisterMessage(self._v_activity_buffer, self, message)

    def flush(self, object, invoke=0, **kw):
      global is_initialized
      if not is_initialized: self.initialize()
      if not hasattr(self, '_v_activity_buffer'): self._v_activity_buffer = ActivityBuffer()
      if type(object) is type(()):
        object_path = object
      else:
        object_path = object.getPhysicalPath()
      for activity in activity_list:
#         LOG('CMFActivity: ', 0, 'flushing activity %s' % activity.__class__.__name__)
        activity.flush(self, object_path, invoke=invoke, **kw)

    def start(self, **kw):
      global is_initialized
      if not is_initialized: self.initialize()
      for activity in activity_list:
#         LOG('CMFActivity: ', 0, 'starting activity %s' % activity.__class__.__name__)
        activity.start(self, **kw)

    def stop(self, **kw):
      global is_initialized
      if not is_initialized: self.initialize()
      for activity in activity_list:
#         LOG('CMFActivity: ', 0, 'starting activity %s' % activity.__class__.__name__)
        activity.stop(self, **kw)

    def invoke(self, message):
      message(self)
      
    def invokeGroup(self, method_id, message_list):
      # Invoke a group method.
      object_list = []
      expanded_object_list = []
      new_message_list = []
      path_dict = {}
      # Filter the list of messages. If an object is not available, ignore such a message.
      # In addition, expand an object if necessary, and make sure that no duplication happens.
      for m in message_list:
        try:
          obj = m.getObject(self)
          i = len(new_message_list) # This is an index of this message in new_message_list.
          if m.hasExpandMethod():
            for subobj in m.getObjectList(self):
              path = subobj.getPath()
              if path not in path_dict:
                path_dict[path] = i
                expanded_object_list.append(subobj)
          else:
            path = obj.getPath()
            if path not in path_dict:
              path_dict[path] = i
              expanded_object_list.append(obj)
          object_list.append(obj)
          new_message_list.append(m)
        except:
          m.is_executed = 0
          m.exc_type = sys.exc_info()[0]
          LOG('WARNING ActivityTool', 0,
              'Could not call method %s on object %s' % (m.method_id, m.object_path), error=sys.exc_info())
              
      if len(expanded_object_list) > 0:
        try:
          method = self.unrestrictedTraverse(method_id)
          # FIXME: how to pass parameters?
          # FIXME: how to apply security here?
          # NOTE: expanded_object_list must be set to failed objects by the callee.
          #       If it fully succeeds, expanded_object_list must be empty when returning.
          result = method(expanded_object_list)
        except:
          # In this case, the group method completely failed.
          for m in new_message_list:
            m.is_executed = 0
            m.exc_type = sys.exc_info()[0]
          LOG('WARNING ActivityTool', 0,
              'Could not call method %s on objects %s' % (method_id, expanded_object_list), error=sys.exc_info())
        else:
          # Obtain all indices of failed messages. Note that this can be a partial failure.
          failed_message_dict = {}
          for obj in expanded_object_list:
            path = obj.getPath()
            i = path_dict[path]
            failed_message_dict[i] = None
            
          # Only for succeeded messages, an activity process is invoked (if any).
          for i in xrange(len(object_list)):
            object = object_list[i]
            m = new_message_list[i]
            if i in failed_message_dict:
              m.is_executed = 0
              LOG('WARNING ActivityTool', 0, 
                  'the method %s partially failed on object %s' % (m.method_id, m.object_path,))
            else:
              try:
                m.activateResult(self, result, object)
                m.is_executed = 1
              except:
                m.is_executed = 0
                m.exc_type = sys.exc_info()[0]
                LOG('WARNING ActivityTool', 0,
                    'Could not call method %s on object %s' % (m.method_id, m.object_path), error=sys.exc_info())
            
    def newMessage(self, activity, path, active_process, activity_kw, method_id, *args, **kw):
      # Some Security Cheking should be made here XXX
      global is_initialized
      if not is_initialized: self.initialize()
      if not hasattr(self, '_v_activity_buffer'): self._v_activity_buffer = ActivityBuffer()
      activity_dict[activity].queueMessage(self, Message(path, active_process, activity_kw, method_id, args, kw))

    security.declareProtected( CMFCorePermissions.ManagePortal, 'manageInvoke' )
    def manageInvoke(self, object_path, method_id, REQUEST=None):
      """
        Invokes all methods for object "object_path"
      """
      if type(object_path) is type(''):
        object_path = tuple(object_path.split('/'))
      self.flush(object_path,method_id=method_id,invoke=1)
      if REQUEST is not None:
        return REQUEST.RESPONSE.redirect('%s/%s' % (self.absolute_url(), 'manageActivities'))

    security.declareProtected( CMFCorePermissions.ManagePortal, 'manageCancel' )
    def manageCancel(self, object_path, method_id, REQUEST=None):
      """
        Cancel all methods for object "object_path"
      """
      if type(object_path) is type(''):
        object_path = tuple(object_path.split('/'))
      self.flush(object_path,method_id=method_id,invoke=0)
      if REQUEST is not None:
        return REQUEST.RESPONSE.redirect('%s/%s' % (self.absolute_url(), 'manageActivities'))

    security.declareProtected( CMFCorePermissions.ManagePortal, 'manageClearActivities' )
    def manageClearActivities(self, REQUEST=None):
      """
        Clear all activities and recreate tables.
      """
      folder = getToolByName(self, 'portal_skins').activity

      # Obtain all pending messages.
      message_list = []
      for activity in activity_list:
        if hasattr(activity, 'dumpMessageList'):
          try:
            message_list.extend(activity.dumpMessageList(self))
          except ConflictError:
            raise
          except:
            LOG('ActivityTool', WARNING, 'could not dump messages from %s' % (activity,), error=sys.exc_info())
            
      if hasattr(folder, 'SQLDict_createMessageTable'):
        try:
          folder.SQLDict_dropMessageTable()
        except ConflictError:
          raise
        except:
          LOG('CMFActivities', 
              WARNING, 
              'could not drop the message table',
              error=sys.exc_info())
        folder.SQLDict_createMessageTable()

      if hasattr(folder, 'SQLQueue_createMessageTable'):
        try:
          folder.SQLQueue_dropMessageTable()
        except ConflictError:
          raise
        except:
          LOG('CMFActivities', 
              WARNING, 
              'could not drop the message queue table',
              error=sys.exc_info())
        folder.SQLQueue_createMessageTable()

      # Reactivate the messages.
      for m in message_list:
        try:
          m.reactivate(self)
        except ConflictError:
          raise
        except:
          LOG('ActivityTool', WARNING,
              'could not reactivate the message %r, %r' % (m.object_path, m.method_id),
              error=sys.exc_info())

      if REQUEST is not None:
        return REQUEST.RESPONSE.redirect('%s/%s' % (self.absolute_url(), 'manageActivitiesAdvanced?manage_tabs_message=Activities%20Cleared')) 

    security.declarePublic('getMessageList')
    def getMessageList(self):
      """
        List messages waiting in queues
      """
      # Initialize if needed
      if not is_initialized: self.initialize()

      message_list = []
      for activity in activity_list:
        try:
          message_list += activity.getMessageList(self)
        except AttributeError:
          LOG('getMessageList, could not get message from Activity:',0,activity)
      return message_list

    security.declareProtected( CMFCorePermissions.ManagePortal , 'newActiveProcess' )
    def newActiveProcess(self, **kw):
      from ActiveProcess import addActiveProcess
      new_id = str(self.generateNewId())
      addActiveProcess(self, new_id)
      active_process = self._getOb(new_id)
      active_process.edit(**kw)
      return active_process

    def reindexObject(self):
      self.immediateReindexObject()

    # Active synchronisation methods
    def validateOrder(self, message, validator_id, validation_value):
      global is_initialized
      if not is_initialized: self.initialize()
      for activity in activity_list:
        method_id = "_validate_%s" % validator_id
        if hasattr(activity, method_id):
#           LOG('CMFActivity: ', 0, 'validateOrder calling method_id %s' % method_id)
          if getattr(activity,method_id)(self, message, validation_value):
            return 1
      return 0

    # Required for tests (time shift)
    def timeShift(self, delay):
      global is_initialized
      if not is_initialized: self.initialize()
      for activity in activity_list:
        activity.timeShift(self, delay)

InitializeClass(ActivityTool)
