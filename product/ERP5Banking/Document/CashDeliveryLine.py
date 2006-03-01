##############################################################################
#
# Copyright (c) 2005 Nexedi SARL and Contributors. All Rights Reserved.
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

from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5.Document.DeliveryLine import DeliveryLine
from Products.ERP5Banking.BaobabMixin import BaobabMixin

in_portal_type_list = ('Cash Exchange Line In', 'Cash To Currency Sale Line In','Cash To Currency Purchase Line In', 'Cash Incident Line In')
out_portal_type_list = ('Cash Exchange Line Out', 'Cash To Currency Sale Line Out','Cash To Currency Purchase Line Out','Cash Incident Line Out')


class CashDeliveryLine(BaobabMixin, DeliveryLine):
  """
    A Cash DeliveryLine object allows to implement lines
      in Cash Deliveries (packing list, Check payment, Cash Movement, etc.).

    It may include a price (for insurance, for customs, for invoices,
      for orders).
  """

  meta_type = 'ERP5Banking Cash Delivery Line'
  portal_type = 'Cash Delivery Line'
  add_permission = Permissions.AddPortalContent
  isPortalContent = 1
  isRADContent = 1

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.View)

  # Declarative interfaces
  __implements__ = ( Interface.Variated, )

  # Declarative properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.CategoryCore
                    , PropertySheet.Amount
                    , PropertySheet.Task
                    , PropertySheet.Arrow
                    , PropertySheet.Movement
                    , PropertySheet.Price
                    , PropertySheet.VariationRange
                    , PropertySheet.ItemAggregation
                    , PropertySheet.CashDeliveryLine
                    )

  security.declareProtected(Permissions.View, 'getBaobabSource')
  def getBaobabSource(self):
    """
      Returns a calculated source
    """
    script = self._getTypeBasedMethod('getBaobabSource')
    if script is not None:
      return script(self)      
    if self.portal_type in out_portal_type_list:
      return self.portal_categories.resolveCategory(self.getSource()).unrestrictedTraverse('sortante').getRelativeUrl()
    elif self.portal_type in in_portal_type_list:
      return None
    return self.getSource()

  security.declareProtected(Permissions.View, 'getBaobabDestination')
  def getBaobabDestination(self):
    """
      Returns a calculated destination
    """
    script = self._getTypeBasedMethod('getBaobabDestination')
    if script is not None:
      return script(self)
    if self.portal_type in in_portal_type_list:
      return self.portal_categories.resolveCategory(self.getSource()).unrestrictedTraverse('entrante').getUid()
    elif self.portal_type in out_portal_type_list :
      return None
    return self.getDestination()

