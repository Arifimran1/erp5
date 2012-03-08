##############################################################################
#
# Copyright (c) 2006 Nexedi SARL and Contributors. All Rights Reserved.
#                    Ivan Tyagov <ivan@nexedi.com>
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

import zope.interface
from Acquisition import aq_base
from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions, PropertySheet, interfaces
from Products.ERP5Type.XMLObject import XMLObject
from DateTime import DateTime
from Products.ERP5Configurator.mixin.configurator_item import ConfiguratorItemMixin

class PersonConfiguratorItem(XMLObject, ConfiguratorItemMixin):
  """ Setup user. """

  meta_type = 'ERP5 Person Configurator Item'
  portal_type = 'Person Configurator Item'
  add_permission = Permissions.AddPortalContent
  isPortalContent = 1
  isRADContent = 1

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Declarative interfaces
  zope.interface.implements(interfaces.IConfiguratorItem)

  # Declarative properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.CategoryCore
                    , PropertySheet.DublinCore
                    , PropertySheet.Reference
                    , PropertySheet.Person 
                    , PropertySheet.Login)

  def _build(self, business_configuration):
    portal = self.getPortalObject()
    person = portal.person_module.newContent(portal_type="Person")
    group_id = getattr(aq_base(self), 'group_id', None)
    site_id = getattr(aq_base(self), 'site_id', None)

    if getattr(aq_base(self), 'organisation_id', None) is not None:
      person.setCareerSubordination('organisation_module/%s' %self.organisation_id)

    # save
    person_dict = {'default_email_text': self.getDefaultEmailText(),
                   'default_telephone_text': self.getDefaultTelephoneText(),
                   'first_name': self.getFirstName(),
                   'career_function': self.getFunction(),
                   'last_name': self.getLastName(),
                   'password': self.getPassword(),
                    } 
    person.edit(**person_dict)

    # explicitly use direct mutator to avoid uniqueness checks in Person.setReference 
    # which work in main ERP5 site context (uses catalog and cache)
    # this is a problem when customer's entered reference is the same as 
    # already exisitng one in main ERP5 site one
    person._setReference(self.getReference())

    assignment = person.newContent(portal_type="Assignment")
    assignment.setFunction(self.getFunction())
    assignment.setGroup(group_id)
    assignment.setSite(site_id)

    # Set dates are required to create valid assigments.
    now = DateTime()
    assignment.setStartDate(now)
    # XXX Is it required to set stop date?
    # Define valid for 10 years.
    assignment.setStopDate(now + (365*10))

    # Validate the Person if possible
    if self.portal_workflow.isTransitionPossible(person, 'validate'):
      person.validate(comment="Validated by Configurator")

    if self.portal_workflow.isTransitionPossible(assignment, 'open'):
      assignment.open(comment="Open by Configuration")
    
    ## add to customer template
    self.install(person, business_configuration)
