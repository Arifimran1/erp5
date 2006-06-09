##############################################################################
#
# Copyright (c) 2004 Nexedi SARL and Contributors. All Rights Reserved.
#                    Sebastien Robin <seb@nexedi.com>
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

import time
from AccessControl import ClassSecurityInfo
from AccessControl.SecurityManagement import newSecurityManager
from Globals import InitializeClass, DTMLFile, PersistentMapping
from Products.ERP5Type.Document.Folder import Folder
from Products.ERP5Type.Tool.BaseTool import BaseTool
from Products.ERP5Type import Permissions
from Products.ERP5 import _dtmldir
from Products.CMFCore import CMFCorePermissions
from DateTime import DateTime

from zLOG import LOG, INFO

try:
  from Products.TimerService import getTimerService
except ImportError:
  def getTimerService(self):
    pass

class AlarmTool(BaseTool):
  """
    This tool manages alarms.

    It is used as a central managment point for all alarms.

    Inside this tool we have a way to retrieve all reports comings
    from Alarms,...
  """
  id = 'portal_alarms'
  meta_type = 'ERP5 Alarm Tool'
  portal_type = 'Alarm Tool'
  allowed_types = ('Supply Alarm Line',)

  # Declarative Security
  security = ClassSecurityInfo()

  security.declareProtected( Permissions.ManagePortal, 'manage_overview' )
  manage_overview = DTMLFile( 'explainAlarmTool', _dtmldir )

  security.declareProtected( Permissions.ManagePortal , 'manageAlarmList' )
  manageAlarmList = DTMLFile( 'manageAlarmList', _dtmldir )

  security.declareProtected( Permissions.ManagePortal , 'manageAlarmAdvanced' )
  manageAlarmAdvanced = DTMLFile( 'manageAlarmAdvanced', _dtmldir )


  manage_options = ( ( { 'label'   : 'Overview'
                       , 'action'   : 'manage_overview'
                       }
                     , { 'label'   : 'All Alarms'
                       , 'action'   : 'manageAlarmList'
                       }
                     , { 'label'   : 'Advanced'
                       , 'action'   : 'manageAlarmAdvanced'
                       }
                     ,
                     )
                     + Folder.manage_options
                   )

  interval = 60 # Default interval for alarms is 60 seconds
  last_tic = time.time()

  # API to manage alarms
  # Aim of this API:
  #-- see all alarms stored everywhere
  #-- defines global alarms
  #-- activate an alarm
  #-- see reports
  #-- see active alarms
  #-- retrieve all alarms

  security.declareProtected(Permissions.ModifyPortalContent, 'getAlarmList')
  def getAlarmList(self, to_active = 0):
    """
      We retrieve thanks to the catalog the full list of alarms
    """
    user = self.portal_catalog.getOwner()
    newSecurityManager(self.REQUEST, user)
    if to_active:
      now = str(DateTime())
      date_expression = '<= %s' % now
      catalog_search = self.portal_catalog(portal_type = \
        self.getPortalAlarmTypeList(), alarm_date = date_expression)
    else:
      catalog_search = self.portal_catalog(portal_type = \
        self.getPortalAlarmTypeList())
    alarm_list = map(lambda x:x.getObject(),catalog_search)
    if to_active:
      now = DateTime()
      date_expression = '<= %s' % str(now)
      catalog_search = self.portal_catalog(
        portal_type = self.getPortalAlarmTypeList(), alarm_date=date_expression
      )
      # check again the alarm date in case the alarm was not yet reindexed
      alarm_list = [x.getObject() for x in catalog_search \
          if x.getObject().getAlarmDate()<=now]
    else:
      catalog_search = self.portal_catalog(
        portal_type = self.getPortalAlarmTypeList()
      )
      alarm_list = map(lambda x:x.getObject(),catalog_search)
    return alarm_list

  security.declareProtected(Permissions.ModifyPortalContent, 'tic')
  def tic(self):
    """
      We will look at all alarms and see if they should be activated,
      if so then we will activate them.
    """
    current_date = DateTime()
    for alarm in self.getAlarmList(to_active=1):
      if alarm:
        user = alarm.getOwner()
        newSecurityManager(self.REQUEST, user)
        if alarm.isActive() or not alarm.isEnabled():
          # do nothing if already active, or not enabled
          continue
        alarm.activate().activeSense()

  security.declareProtected(Permissions.ManageProperties, 'isSubscribed')
  def isSubscribed(self):
      """
      return True, if we are subscribed to TimerService.
      Otherwise return False.
      """
      service = getTimerService(self)
      if not service:
          LOG('AlarmTool', INFO, 'TimerService not available')
          return False

      path = '/'.join(self.getPhysicalPath())
      if path in service.lisSubscriptions():
          return True
      return False

  security.declareProtected(Permissions.ManageProperties, 'subscribe')
  def subscribe(self):
    """
      Subscribe to the global Timer Service.
    """
    service = getTimerService(self)
    if not service:
      LOG('AlarmTool', INFO, 'TimerService not available')
      return
    service.subscribe(self)
    return "Subscribed to Timer Service"

  security.declareProtected(Permissions.ManageProperties, 'unsubscribe')
  def unsubscribe(self):
    """
      Unsubscribe from the global Timer Service.
    """
    service = getTimerService(self)
    if not service:
      LOG('AlarmTool', INFO, 'TimerService not available')
      return
    service.unsubscribe(self)
    return "Usubscribed from Timer Service"

  def manage_beforeDelete(self, item, container):
    self.unsubscribe()
    BaseTool.inheritedAttribute('manage_beforeDelete')(self, item, container)

  def manage_afterAdd(self, item, container):
    self.subscribe()
    BaseTool.inheritedAttribute('manage_afterAdd')(self, item, container)

  def process_timer(self, interval, tick, prev="", next=""):
    """
      Call tic() every x seconds. x is defined in self.interval
      This method is called by TimerService in the interval given
      in zope.conf. The Default is every 5 seconds.
    """
    if tick.timeTime() - self.last_tic >= self.interval:
      self.tic()
      self.last_tic = tick.timeTime()

