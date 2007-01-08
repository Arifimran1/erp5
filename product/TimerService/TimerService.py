# -*- coding: UTF-8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# Authors: Nik Kim <fafhrd@legco.biz>
__version__ = '$Revision: 1.3 $'[11:-2]

import sys, time, threading
from DateTime import DateTime
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager

from zLOG import LOG, INFO, ERROR

from AccessControl import ClassSecurityInfo, Permissions
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

current_version = 1

processing_lock = threading.Lock()

class TimerService(SimpleItem):
    """ timer service, all objects that wants timer
    event subscribe here """

    id='timer_service'
    title = 'TimerService'

    security = ClassSecurityInfo()
    security.declareObjectPublic()
    
    icon = 'misc_/TimerService/timer_icon.gif'

    max_size = 0

    manage_options = (
        ({'label': 'Subscribers', 'action':'manage_viewSubscriptions'},))

    security.declareProtected(
        Permissions.view_management_screens, 'manage_viewSubscriptions')
    manage_viewSubscriptions = PageTemplateFile(
        'zpt/view_subscriptions',
        globals(),
        __name__='manage_viewSubscriptions'
        )

    _version = 0

    def __init__(self, id='timer_service'):
        """ """
        self._subscribers = []
        self._version = 1
    
    security.declarePublic('process_timer')
    def process_timer(self, interval):
        """ """
        # Try to acquire a lock, to make sure we only run one processing at a
        # time, and abort if another processing is currently running
        acquired = processing_lock.acquire(0)
        if not acquired:
            return
        try:
          # Don't let TimerService crash when the ERP5Site is not yet existing.
          # This case append when we create a new Portal: At that step Timer
          # Service start to 'ping' the portal before the zope transaction in
          # which the portal is created is commited.
          subscriptions = []
          try:
            subscriptions = [self.unrestrictedTraverse(path)
                             for path in self._subscribers]
          except KeyError:
            pass

          tick = time.time()
          prev_tick = tick - interval
          next_tick = tick + interval

          for subscriber in subscriptions:
              try:
                  subscriber.process_timer(
                      interval, DateTime(tick),
                      DateTime(prev_tick), DateTime(next_tick))
              except:
                  LOG('TimerService', ERROR, 'Process timer error',
                      error = sys.exc_info())
                  raise
        finally:
            # When processing is done, release the lock
            processing_lock.release()

    def subscribe(self, ob):
        """ """
        path = '/'.join(ob.getPhysicalPath())

        subscribers = self._subscribers
        if path not in subscribers:
            subscribers.append(path)
            self._subscribers = subscribers

    security.declareProtected(
        Permissions.view_management_screens, 'unsubscribeByPath')
    def unsubscribeByPath(self, path):
        subscribers = self._subscribers
        if path in subscribers:
            subscribers.remove(path)
            self._subscribers = subscribers

    def unsubscribe(self, ob):
        """ """
        path = '/'.join(ob.getPhysicalPath())

        subscribers = self._subscribers
        if path in subscribers:
            subscribers.remove(path)
            self._subscribers = subscribers

    security.declareProtected(
        Permissions.view_management_screens, 'lisSubscriptions')
    def lisSubscriptions(self):
        """ """
        return self._subscribers
    
    security.declareProtected(
        Permissions.view_management_screens, 'manage_removeSubscriptions')
    def manage_removeSubscriptions(self, no, REQUEST=None):
        """ """
        subs = self.lisSubscriptions()

        remove_list = [subs[n] for n in [int(n) for n in no]]

        for sub in remove_list:
            self.unsubscribeByPath(sub)

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('manage_viewSubscriptions')


InitializeClass(TimerService)
