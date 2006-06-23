##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#          Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
#
# Based on: db.py in ZMySQLDA
#
##############################################################################

from Shared.DC.ZRDB.TM import TM
from zLOG import LOG, ERROR, INFO
import sys
from thread import allocate_lock, get_ident

try:
  from transaction import get as get_transaction
except ImportError:
  pass

class ActivityBuffer(TM):

  _p_oid=_p_changed=_registered=None

  def __init__(self, activity_tool=None):
    self._use_TM = self._transactions = 1
    if self._use_TM:
      self._tlock = allocate_lock()
      self._tthread = None
    self._lock = allocate_lock()

    # Directly store the activity tool as an attribute. At the beginning
    # the activity tool was stored as a part of the key in queued_activity and
    # in flushed_activity, but this is not nice because in that case we must
    # use hash on it, and when there is no uid on activity tool, it is
    # impossible to generate a new uid because acquisition is not available
    # in the dictionary.
    assert activity_tool is not None
    self._activity_tool = activity_tool

    # Referring to a persistent object is dangerous when finishing a transaction,
    # so store only the required information.
    self._activity_tool_path = activity_tool.getPhysicalPath()

  # Keeps a list of messages to add and remove
  # at end of transaction
  def _begin(self, *ignored):
    from ActivityTool import activity_list
    self._tlock.acquire()
    self._tthread = get_ident()
    self.requires_prepare = 1
    try:
      self.queued_activity = []
      self.flushed_activity = []
      for activity in activity_list:              # Reset registration for each transaction
        activity.registerActivityBuffer(self)
      # In Zope 2.8 (ZODB 3.4), use beforeCommitHook instead of
      # patching Trasaction.
      transaction = get_transaction()
      try:
        transaction.beforeCommitHook(self.tpc_prepare, transaction)
      except AttributeError:
        pass
    except:
      LOG('ActivityBuffer', ERROR, "exception during _begin",
          error=sys.exc_info())
      self._tlock.release()
      raise

  def _finish(self, *ignored):
    if not self._tlock.locked() or self._tthread != get_ident():
      LOG('ActivityBuffer', INFO, "ignoring _finish")
      return
    try:
      try:
        # Try to push / delete all messages
        for (activity, message) in self.flushed_activity:
          #LOG('ActivityBuffer finishDeleteMessage', ERROR, str(message.method_id))
          activity.finishDeleteMessage(self._activity_tool_path, message)
        for (activity, message) in self.queued_activity:
          #LOG('ActivityBuffer finishQueueMessage', ERROR, str(message.method_id))
          activity.finishQueueMessage(self._activity_tool_path, message)
      except:
        LOG('ActivityBuffer', ERROR, "exception during _finish",
            error=sys.exc_info())
        raise
    finally:
      self._tlock.release()

  def _abort(self, *ignored):
    if not self._tlock.locked() or self._tthread != get_ident():
      LOG('ActivityBuffer', 0, "ignoring _abort")
      return
    self._tlock.release()

  def tpc_prepare(self, transaction, sub=None):
    if sub is not None: # Do nothing if it is a subtransaction
      return
    if not self.requires_prepare: return
    self.requires_prepare = 0
    if not self._tlock.locked() or self._tthread != get_ident():
      LOG('ActivityBuffer', 0, "ignoring tpc_prepare")
      return
    try:
      # Try to push / delete all messages
      for (activity, message) in self.flushed_activity:
        #LOG('ActivityBuffer prepareDeleteMessage', ERROR, str(message.method_id))
        activity.prepareDeleteMessage(self._activity_tool, message)
      activity_dict = {}
      for (activity, message) in self.queued_activity:
        key = activity
        if key not in activity_dict:
          activity_dict[key] = []
        activity_dict[key].append(message)
      for key, message_list in activity_dict.items():
        activity = key
        if hasattr(activity, 'prepareQueueMessageList'):
          activity.prepareQueueMessageList(self._activity_tool, message_list)
        else:
          for message in message_list:
            activity.prepareQueueMessage(self._activity_tool, message)
    except:
      LOG('ActivityBuffer', ERROR, "exception during tpc_prepare",
          error=sys.exc_info())
      raise

  def deferredQueueMessage(self, activity_tool, activity, message):
    self._register()
    # Activity is called to prevent queuing some messages (useful for example
    # to prevent reindexing objects multiple times)
    if not activity.isMessageRegistered(self, activity_tool, message):
      self.queued_activity.append((activity, message))
      # We register queued messages so that we can
      # unregister them
      activity.registerMessage(self, activity_tool, message)

  def deferredDeleteMessage(self, activity_tool, activity, message):
    self._register()
    self.flushed_activity.append((activity, message))
