from Products.ERP5Type.XMLObject import XMLObject
from DateTime import DateTime
from zLOG import LOG
from zLOG import ERROR
from zLOG import INFO
from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions

class TestSuite(XMLObject):

  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)
  
  security.declareProtected(Permissions.ModifyPortalContent, 'setPingDate')
  def setPingDate(self):
    """
    Set a new date to now when the node was last alive
    """
    portal = self.getPortalObject()
    portal.portal_task_distribution.getMemcachedDict().set(
       "%s_ping_date" % (self.getRelativeUrl()), DateTime())
    if self.getValidationState() == "invalidated":
      self.validate()

  security.declareProtected(Permissions.AccessContentsInformation, 'getPingDate')
  def getPingDate(self):
    """
    Set a new date to now when the node was last alive
    """
    portal = self.getPortalObject()
    return portal.portal_task_distribution.getMemcachedDict().get(
       "%s_ping_date" % (self.getRelativeUrl()))

       
