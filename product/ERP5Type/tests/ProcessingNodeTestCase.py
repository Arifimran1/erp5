# -*- coding: utf-8 -*-
import base64, errno, select, socket, time
from threading import Thread
import Lifetime
import transaction
from BTrees.OIBTree import OIBTree
from Testing import ZopeTestCase
from Products.CMFActivity.Activity.Queue import VALIDATION_ERROR_DELAY
from Products.ERP5Type.tests import backportUnittest
from Products.ERP5Type.tests.utils import createZServer


def patchActivityTool():
  """Redefine several methods of ActivityTool for unit tests
  """
  from Products.CMFActivity.ActivityTool import ActivityTool
  def patch(function):
    name = function.__name__
    orig_function = getattr(ActivityTool, name)
    setattr(ActivityTool, '_orig_' + name, orig_function)
    setattr(ActivityTool, name, function)
    function.__doc__ = orig_function.__doc__

  # When a ZServer can't be started, the node name ends with ':' (no port).
  @patch
  def _isValidNodeName(self, node_name):
    return True

  # Divert location to register processing and distributing nodes.
  # Load balancing is configured at the root instead of the activity tool,
  # so that additional can register even if there is no portal set up yet.
  # Properties at the root are:
  # - 'test_processing_nodes' to list processing nodes
  # - 'test_distributing_node' to select the distributing node
  @patch
  def getNodeDict(self):
    app = self.getPhysicalRoot()
    if getattr(app, 'test_processing_nodes', None) is None:
      app.test_processing_nodes = OIBTree()
    return app.test_processing_nodes

  @patch
  def getDistributingNode(self):
    return self.getPhysicalRoot().test_distributing_node

  @patch
  def manage_setDistributingNode(self, distributingNode, REQUEST=None):
    # A property to catch setattr on 'distributingNode' doesn't work
    # because self would lose all acquisition wrappers.
    previous_node = self.distributingNode
    try:
      self._orig_manage_setDistributingNode(distributingNode, REQUEST=REQUEST)
      self.getPhysicalRoot().test_distributing_node = self.distributingNode
    finally:
      self.distributingNode = previous_node

  # When there is more than 1 node, prevent the distributing node from
  # processing activities.
  @patch
  def tic(self, processing_node=1, force=0):
    processing_node_list = self.getProcessingNodeList()
    if len(processing_node_list) > 1 and \
       self.getCurrentNode() == self.getDistributingNode():
      # Sleep between each distribute.
      time.sleep(0.3)
      transaction.commit()
    else:
      self._orig_tic(processing_node, force)


class ProcessingNodeTestCase(backportUnittest.TestCase, ZopeTestCase.TestCase):
  """Minimal ERP5 TestCase class to process activities

  When a processing node starts, the portal may not exist yet, or its name is
  unknown, so an additional 'test_portal_name' property at the root is set by
  the node running the unit tests to tell other nodes on which portal activities
  should be processed.
  """

  @staticmethod
  def asyncore_loop():
    try:
      Lifetime.lifetime_loop()
    except KeyboardInterrupt:
      pass
    Lifetime.graceful_shutdown_loop()

  def startZServer(self, verbose=False):
    """Start HTTP ZServer in background"""
    utils = ZopeTestCase.utils
    if utils._Z2HOST is None:
      _print = lambda hs: verbose and ZopeTestCase._print(
        "Running %s server at %s:%s\n" % (
          hs.server_protocol, hs.server_name, hs.server_port))
      try:
        hs = createZServer()
      except RuntimeError, e:
        ZopeTestCase._print(str(e))
      else:
        utils._Z2HOST, utils._Z2PORT = hs.server_name, hs.server_port
        _print(hs)
        try:
          _print(createZServer(zserver_type='webdav'))
        except RuntimeError, e:
          ZopeTestCase._print(str(e))
        t = Thread(target=Lifetime.loop)
        t.setDaemon(1)
        t.start()
    return utils._Z2HOST, utils._Z2PORT

  def _registerNode(self, distributing, processing):
    """Register node to process and/or distribute activities"""
    try:
      activity_tool = self.portal.portal_activities
    except AttributeError:
      from Products.CMFActivity.ActivityTool import ActivityTool
      activity_tool = ActivityTool().__of__(self.app)
    currentNode = activity_tool.getCurrentNode()
    if distributing:
      activity_tool.manage_setDistributingNode(currentNode)
    if processing:
      activity_tool.manage_addToProcessingList((currentNode,))
    else:
      activity_tool.manage_removeFromProcessingList((currentNode,))

  def assertNoPendingMessage(self):
    """Get the last error message from error_log"""
    message_list = self.portal.portal_activities.getMessageList()
    if message_list:
      error_message = 'These messages are pending: %r' % [
          ('/'.join(m.object_path), m.method_id, m.processing_node, m.retry)
          for m in message_list]
      error_log = self.portal.error_log._getLog()
      if len(error_log):
        error_message += '\nLast error message:' \
                         '\n%(type)s\n%(value)s\n%(tb_text)s' \
                         % error_log[-1]
      self.fail(error_message)

  def tic(self, verbose=0):
    """Execute pending activities"""
    # Some tests like testDeferredStyle require that we use self.getPortal()
    # instead of self.portal in order to setup current skin.
    portal_activities = self.getPortal().portal_activities
    if 1:
      if verbose:
        ZopeTestCase._print('Executing pending activities ...')
        old_message_count = 0
        start = time.time()
      count = 1000
      getMessageList = portal_activities.getMessageList
      message_count = len(getMessageList(include_processing=1))
      while message_count:
        if verbose and old_message_count != message_count:
          ZopeTestCase._print(' %i' % message_count)
          old_message_count = message_count
        portal_activities.process_timer(None, None)
        if Lifetime._shutdown_phase:
          # XXX CMFActivity contains bare excepts
          raise KeyboardInterrupt
        message_count = len(getMessageList(include_processing=1))
        # This prevents an infinite loop.
        count -= 1
        if count == 0:
          error_message = 'tic is looping forever. '
          try:
            self.assertNoPendingMessage()
          except AssertionError, e:
            error_message += str(e)
          raise RuntimeError(error_message)
        # This give some time between messages
        if count % 10 == 0:
          portal_activities.timeShift(3 * VALIDATION_ERROR_DELAY)
      if verbose:
        ZopeTestCase._print(' done (%.3fs)\n' % (time.time() - start))

  def afterSetUp(self):
    """Initialize a node that will only process activities"""
    self.startZServer()
    self._registerNode(distributing=0, processing=1)
    transaction.commit()

  def processing_node(self):
    """Main loop for nodes that process activities"""
    try:
      while not Lifetime._shutdown_phase:
        time.sleep(.3)
        transaction.begin()
        try:
          portal = self.app[self.app.test_portal_name]
        except (AttributeError, KeyError):
          continue
        portal.portal_activities.process_timer(None, None)
    except KeyboardInterrupt:
      pass
