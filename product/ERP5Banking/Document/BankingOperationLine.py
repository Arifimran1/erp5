##############################################################################
#
# Copyright (c) 2005 Nexedi SARL and Contributors. All Rights Reserved.
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
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowMethod
from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5.Document.AccountingTransactionLine import AccountingTransactionLine
from Products.ERP5Banking.BaobabMixin import BaobabMixin

class BankingOperationLine(BaobabMixin, AccountingTransactionLine):
  # CMF Type Definition
  meta_type = 'ERP5Banking Banking Operation Line'
  portal_type = 'Banking Operation Line'
  isPortalContent = 1
  isRADContent = 1

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.View)

  # Default Properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.CategoryCore
                    , PropertySheet.DublinCore
                    )

  security.declareProtected(Permissions.View, 'getSourceTotalAssetPrice')
  def getSourceTotalAssetPrice(self):
    """Default to quantity."""
    return self._baseGetSourceTotalAssetPrice() or abs(self.getQuantity())

  security.declareProtected(Permissions.View, 'getDestinationTotalAssetPrice')
  def getDestinationTotalAssetPrice(self):
    """Default to quantity."""
    return self._baseGetDestinationTotalAssetPrice() or abs(self.getQuantity())

  security.declareProtected(Permissions.View, 'getSourceTotalAssetPriceCurrencyReference')
  def getSourceTotalAssetPriceCurrencyReference(self):
    """Return the reference of the price currency of the source payment."""
    payment = self.getBaobabSourcePaymentValue()
    if payment is not None:
      currency = payment.getPriceCurrencyValue()
      if currency is not None:
        return currency.getReference()
    return None

  security.declareProtected(Permissions.View, 'getDestinationTotalAssetPriceCurrencyReference')
  def getDestinationTotalAssetPriceCurrencyReference(self):
    """Return the reference of the price currency of the destination payment."""
    payment = self.getBaobabDestinationPaymentValue()
    if payment is not None:
      currency = payment.getPriceCurrencyValue()
      if currency is not None:
        return currency.getReference()
    return None


