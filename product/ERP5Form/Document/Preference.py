##############################################################################
#
# Copyright (c) 2005 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jerome Perrin <jerome@nexedi.com>
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
from Products.ERP5Type.Document.Folder import Folder
from Products.ERP5Type.Cache import clearCache

class Priority:
  """ names for priorities """
  SITE  = 1
  GROUP = 2
  USER  = 3

class Preference( Folder ):
  """
    A system or user preference

    TODO:
      - migrate to ERP5Type the whole preference system
  """

  # CMF Type Definition
  meta_type       = 'ERP5 Preference'
  portal_type     = 'Preference'
  add_permission  = Permissions.AddPortalContent
  isPortalContent = 1
  isRADContent    = 1
  
  # Declarative properties
  property_sheets = \
                    ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.DublinCore
                    )
  
  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  def _clearCache(self):
    """Clear caches used by methods of this preference
    # TODO: clear different caches according to the preference priority
    """
    clearCache()

  def _edit(self, **kw):
    """edit and clear all caches"""
    self._clearCache()
    Folder._edit(self, **kw)

  def enable(self):
    """Workflow method"""
    self._clearCache()

  def disable(self):
    """Workflow method"""
    self._clearCache()
  
