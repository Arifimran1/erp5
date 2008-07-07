##############################################################################
#
# Copyright (c) 2005, 2006 Nexedi SARL and Contributors. All Rights Reserved.
#                    Yoshinori Okuji <yo@nexedi.com>
#                    Romain Courteaud <romain@nexedi.com>
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

from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5.Document.Predicate import Predicate
from Products.ERP5.Document.MetaNode import MetaNode

from Products.ERP5.Document.InventoryCell import InventoryCell

from zLOG import LOG

class BudgetCell(Predicate, MetaNode):
    """
    BudgetCell ...
    """

    # Default Properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.SimpleItem
                      , PropertySheet.Folder
                      , PropertySheet.Predicate
                      , PropertySheet.SortIndex
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      , PropertySheet.Task
                      , PropertySheet.Arrow
                      , PropertySheet.Amount
                      , PropertySheet.Budget
                      , PropertySheet.MappedValue
                      , PropertySheet.VariationRange
                      )

    # CMF Type Definition
    meta_type='ERP5 Budget Cell'
    portal_type='Budget Cell'    
    add_permission = Permissions.AddPortalContent
    isPortalContent = 1
    isRADContent = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    security.declareProtected(Permissions.View, 'getTitle')
    def getTitle(self):
      """
      Return a calculated title.
      """
      script = self._getTypeBasedMethod('asTitle')
      try:
        title = script()
      except UnboundLocalError:
        raise UnboundLocalError,\
              "Did not find title script for portal type: %r" %\
              self.getPortalType()
      return title
    
    security.declareProtected(Permissions.View, 'getCurrentInventory')  
    def getCurrentInventory(self, **kw):
      """
      Returns current inventory
      """
      kw['node'] = self.getRelativeUrl()
      resource = self.getResourceValue()
      if resource is not None:
        kw['resource'] = resource.getRelativeUrl()
      return self.portal_simulation.getCurrentInventory(**kw)

    security.declareProtected(Permissions.View, 'getCurrentBalance')
    def getCurrentBalance(self):
      """
      Returns current balance
      """
      return self.getQuantity(0.0) + self.getCurrentInventory()

    security.declareProtected(Permissions.View, 'getConsumedBudget')
    def getConsumedBudget(self, src__=0):
      """
      Return consumed budget.
      """
      script = self._getTypeBasedMethod('getConsumedBudget')
      try:
        result = script(src__=src__)
      except UnboundLocalError:
        raise UnboundLocalError,\
              "Did not find consumed budget script for portal type: %r" % \
              self.getPortalType()
      return result

    security.declareProtected(Permissions.View, 'getAvailableBudget')
    def getAvailableBudget(self):
      """
      Return available budget.
      """
      return self.getCurrentBalance() - self.getConsumedBudget()
