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

from Globals import InitializeClass, PersistentMapping
from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface

from Products.ERP5.Document.DeliveryLine import DeliveryLine
from Products.ERP5.Variated import Variated

from zLOG import LOG

class InvoiceLine(DeliveryLine):
    """
      A DeliveryLine object allows to implement lines in
      Deliveries (packing list, order, invoice, etc.)

      It may include a price (for insurance, for customs, for invoices,
      for orders)
    """

    meta_type = 'ERP5 Invoice Line'
    portal_type = 'Invoice Line'
    add_permission = Permissions.AddPortalContent
    isPortalContent = 1
    isRADContent = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Declarative interfaces
    __implements__ = ( Interface.Variated, )

    # Declarative properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.Amount
                      , PropertySheet.Task
                      , PropertySheet.ItemAggregation
                      , PropertySheet.Arrow
                      , PropertySheet.Movement
                      , PropertySheet.Price
                      , PropertySheet.VariationRange
                      )
    
    # Cell Related
    security.declareProtected( Permissions.ModifyPortalContent,
                               'newCellContent' )
    def newCellContent(self, id,**kw):
      """
          This method can be overriden
      """
      self.invokeFactory(type_name="Invoice Cell",id=id)
      return self.get(id)

    security.declareProtected( Permissions.AccessContentsInformation,
                               'isAccountable' )
    def isAccountable(self):
      """
        Invoice movements are never accountable, because they have no
        impact on stock calculations.
      """
      # Never accountable
      return 0

#    security.declareProtected( Permissions.AccessContentsInformation,
#                              'isDivergent' )
#    def isDivergent(self):
#      """
#        Returns 1 if the target is not met according to the current information
#        After and edit, the isOutOfTarget will be checked. If it is 1,
#        a message is emitted
#
#        emit targetUnreachable !
#      """
#      # Never divergent
#      return 0

    security.declareProtected( Permissions.AccessContentsInformation,
                               'getGroupCriterion' )
    def getGroupCriterion(self):
      """
        Return the criterion for grouping. This should be overriden by each class.
      """
      return int(round(self.getPrice() * 100))
