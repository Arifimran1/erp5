# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2007 Nexedi SA and Contributors. All Rights Reserved.
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################

import unittest
import os
import email.Header

import transaction

from Products.CMFCore.WorkflowCore import WorkflowException
from Products.ERP5Type.tests.utils import DummyMailHost, FileUpload
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase,\
                                                       _getConversionServerDict
from Products.ERP5OOo.tests.testIngestion import FILE_NAME_REGULAR_EXPRESSION
from Products.ERP5OOo.tests.testIngestion import REFERENCE_REGULAR_EXPRESSION
from Products.ERP5Type.tests.backportUnittest import expectedFailure

def makeFilePath(name):
  return os.path.join(os.path.dirname(__file__), 'test_data', 'crm_emails', name)

def makeFileUpload(name):
  path = makeFilePath(name)
  return FileUpload(path, name)

clear_module_name_list = """
campaign_module
event_module
meeting_module
organisation_module
person_module
sale_opportunity_module
""".strip().splitlines()

class BaseTestCRM(ERP5TypeTestCase):

  def afterSetUp(self):
    super(BaseTestCRM, self).afterSetUp()
    # add a dummy mailhost not to send real messages
    self.oldMailHost = getattr(self.portal, 'MailHost', None)
    if self.oldMailHost is not None:
      self.portal.manage_delObjects(['MailHost'])
      self.portal._setObject('MailHost', DummyMailHost('MailHost'))

  def beforeTearDown(self):
    transaction.abort()
    # restore the original MailHost
    if self.oldMailHost is not None:
      self.portal.manage_delObjects(['MailHost'])
      self.portal._setObject('MailHost', DummyMailHost('MailHost'))
    # clear modules if necessary
    for module_name in clear_module_name_list:
      module = getattr(self.portal, module_name)
      module.manage_delObjects(list(module.objectIds()))

    self.stepTic()
    super(BaseTestCRM, self).beforeTearDown()

class TestCRM(BaseTestCRM):
  def getTitle(self):
    return "CRM"

  def getBusinessTemplateList(self):
    return ('erp5_base',
            'erp5_crm',)

  def test_Event_CreateRelatedEvent(self):
    # test workflow to create a related event from responded event
    event_module = self.portal.event_module
    portal_workflow = self.portal.portal_workflow
    ticket = self.portal.campaign_module.newContent(portal_type='Campaign',)
    for ptype in [x for x in self.portal.getPortalEventTypeList() if x !=
        'Acknowledgement']:
      event = event_module.newContent(portal_type=ptype,
                                      follow_up_value=ticket)

      event.receive()
      event.respond()

      self.assertEqual(len(event.getCausalityRelatedValueList()), 0)

      transaction.commit()
      self.tic()

      portal_workflow.doActionFor(event, 'create_related_event_action',
                                  related_event_portal_type=ptype,
                                  related_event_title='New Title',
                                  related_event_description='New Desc')

      transaction.commit()
      self.tic()

      self.assertEqual(len(event.getCausalityRelatedValueList()), 1)

      related_event = event.getCausalityRelatedValue()

      self.assertEqual(related_event.getPortalType(), ptype)
      self.assertEqual(related_event.getTitle(), 'New Title')
      self.assertEqual(related_event.getDescription(), 'New Desc')
      self.assertEqual(related_event.getFollowUpValue(), ticket)
 
  def test_Event_CreateRelatedEventUnauthorized(self):
    # test that we don't get Unauthorized error when invoking the "Create
    # Related Event" without add permission on the module,
    # but will get WorkflowException error.
    event = self.portal.event_module.newContent(portal_type='Letter')
    self.portal.event_module.manage_permission('Add portal content', [], 0)
    self.assertRaises(WorkflowException,
                      event.Event_createRelatedEvent,
                      portal_type='Letter',
                      title='New Title',
                      description='New Desc')
    
  def test_Ticket_CreateRelatedEvent(self):
    # test action to create a related event from a ticket
    event_module_url = self.portal.event_module.absolute_url()
    ticket = self.portal.meeting_module.newContent(portal_type='Meeting')
    for ptype in [x for x in self.portal.getPortalEventTypeList() if x !=
        'Acknowledgement']:
      # incoming
      redirect = ticket.Ticket_newEvent(direction='incoming',
                                        portal_type=ptype,
                                        title='New Title',
                                        description='New Desc')
      self.assert_(redirect.startswith(event_module_url), redirect)
      new_id = redirect[len(event_module_url)+1:].split('/', 1)[0]
      new_event = self.portal.event_module._getOb(new_id)
      self.assertEquals(ticket, new_event.getFollowUpValue())
      self.assertEquals('new', new_event.getSimulationState())

      # outgoing
      redirect = ticket.Ticket_newEvent(direction='outgoing',
                                        portal_type=ptype,
                                        title='New Title',
                                        description='New Desc')
      self.assert_(redirect.startswith(event_module_url), redirect)
      new_id = redirect[len(event_module_url)+1:].split('/', 1)[0]
      new_event = self.portal.event_module._getOb(new_id)
      self.assertEquals(ticket, new_event.getFollowUpValue())
      self.assertEquals('planned', new_event.getSimulationState())

  def test_Ticket_CreateRelatedEventUnauthorized(self):
    # test that we don't get Unauthorized error when invoking the "Create
    # New Event" without add permission on the module
    ticket = self.portal.meeting_module.newContent(portal_type='Meeting')
    self.portal.event_module.manage_permission('Add portal content', [], 0)
    ticket.Ticket_newEvent(portal_type='Letter',
                           title='New Title',
                           description='New Desc',
                           direction='incoming')
   
  def test_PersonModule_CreateRelatedEventSelectionParams(self):
    # create related event from selected persons.
    person_module = self.portal.person_module
    pers1 = person_module.newContent(portal_type='Person', title='Pers1')
    pers2 = person_module.newContent(portal_type='Person', title='Pers2')
    pers3 = person_module.newContent(portal_type='Person', title='Pers3')
    self.portal.person_module.view()
    self.portal.portal_selections.setSelectionCheckedUidsFor(
                          'person_module_selection', [])
    self.portal.portal_selections.setSelectionParamsFor(
                          'person_module_selection', dict(title='Pers1'))
    transaction.commit()
    self.tic()
    person_module.PersonModule_newEvent(portal_type='Mail Message',
                                        title='The Event Title',
                                        description='The Event Descr.',
                                        direction='outgoing',
                                        selection_name='person_module_selection',
                                        follow_up='',
                                        text_content='Event Content',
                                        form_id='PersonModule_viewPersonList')

    transaction.commit()
    self.tic()

    related_event = pers1.getDestinationRelatedValue(
                          portal_type='Mail Message')
    self.assertNotEquals(None, related_event)
    self.assertEquals('The Event Title', related_event.getTitle())
    self.assertEquals('The Event Descr.', related_event.getDescription())
    self.assertEquals('Event Content', related_event.getTextContent())

    for person in (pers2, pers3):
      self.assertEquals(None, person.getDestinationRelatedValue(
                                       portal_type='Mail Message'))

  def test_PersonModule_CreateRelatedEventCheckedUid(self):
    # create related event from selected persons.
    person_module = self.portal.person_module
    pers1 = person_module.newContent(portal_type='Person', title='Pers1')
    pers2 = person_module.newContent(portal_type='Person', title='Pers2')
    pers3 = person_module.newContent(portal_type='Person', title='Pers3')
    self.portal.person_module.view()
    self.portal.portal_selections.setSelectionCheckedUidsFor(
          'person_module_selection',
          [pers1.getUid(), pers2.getUid()])
    transaction.commit()
    self.tic()
    person_module.PersonModule_newEvent(portal_type='Mail Message',
                                        title='The Event Title',
                                        description='The Event Descr.',
                                        direction='outgoing',
                                        selection_name='person_module_selection',
                                        follow_up='',
                                        text_content='Event Content',
                                        form_id='PersonModule_viewPersonList')

    transaction.commit()
    self.tic()

    for person in (pers1, pers2):
      related_event = person.getDestinationRelatedValue(
                            portal_type='Mail Message')
      self.assertNotEquals(None, related_event)
      self.assertEquals('The Event Title', related_event.getTitle())
      self.assertEquals('The Event Descr.', related_event.getDescription())
      self.assertEquals('Event Content', related_event.getTextContent())

    self.assertEquals(None, pers3.getDestinationRelatedValue(
                                portal_type='Mail Message'))

  def test_SaleOpportunitySold(self):
    # test the workflow of sale opportunities, when the sale opportunity is
    # finaly sold
    so = self.portal.sale_opportunity_module.newContent(
                              portal_type='Sale Opportunity')
    self.assertEquals('draft', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'submit_action')
    self.assertEquals('submitted', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'validate_action')
    self.assertEquals('contacted', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'enquire_action')
    self.assertEquals('enquired', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'offer_action')
    self.assertEquals('offered', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'sell_action')
    self.assertEquals('sold', so.getSimulationState())

  def test_SaleOpportunityRejected(self):
    # test the workflow of sale opportunities, when the sale opportunity is
    # finaly rejected.
    # Uses different transitions than test_SaleOpportunitySold
    so = self.portal.sale_opportunity_module.newContent(
                              portal_type='Sale Opportunity')
    self.assertEquals('draft', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'validate_action')
    self.assertEquals('contacted', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'enquire_action')
    self.assertEquals('enquired', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'offer_action')
    self.assertEquals('offered', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'reject_action')
    self.assertEquals('rejected', so.getSimulationState())

  def test_SaleOpportunityExpired(self):
    # test the workflow of sale opportunities, when the sale opportunity
    # expires
    so = self.portal.sale_opportunity_module.newContent(
                              portal_type='Sale Opportunity')
    self.assertEquals('draft', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'validate_action')
    self.assertEquals('contacted', so.getSimulationState())
    self.portal.portal_workflow.doActionFor(so, 'expire_action')
    self.assertEquals('expired', so.getSimulationState())

  def test_Event_AcknowledgeAndCreateEvent(self):
    """
    Make sure that when acknowledge event, we can create a new event.

    XXX This is probably meaningless in near future. event_workflow
    will be reviewed in order to have steps closer to usual packing 
    list workflow. For now we have a conflict name between the 
    acknowledge method of event_workflow and Acknowledgement features
    that comes with AcknowledgementTool. So for now disable site
    message in this test.
    """
    portal_workflow = self.portal.portal_workflow

    event_type_list = [x for x in self.portal.getPortalEventTypeList() \
                       if x not in  ['Site Message', 'Acknowledgement']]

    # if create_event option is false, it does not create a new event.
    for portal_type in event_type_list:
      ticket = self.portal.meeting_module.newContent(portal_type='Meeting',
                                                     title='Meeting1')
      ticket_url = ticket.getRelativeUrl()
      event = self.portal.event_module.newContent(portal_type=portal_type,
                                                  follow_up=ticket_url)
      transaction.commit()
      self.tic()
      self.assertEqual(len(event.getCausalityRelatedValueList()), 0)
      event.receive()
      portal_workflow.doActionFor(event, 'acknowledge_action', create_event=0)
      transaction.commit()
      self.tic()
      self.assertEqual(len(event.getCausalityRelatedValueList()), 0)
      
    # if create_event option is true, it create a new event.
    for portal_type in event_type_list:
      ticket = self.portal.meeting_module.newContent(portal_type='Meeting',
                                                     title='Meeting1')
      ticket_url = ticket.getRelativeUrl()
      event = self.portal.event_module.newContent(portal_type=portal_type,
                                                  follow_up=ticket_url)
      transaction.commit()
      self.tic()
      self.assertEqual(len(event.getCausalityRelatedValueList()), 0)
      event.receive()
      portal_workflow.doActionFor(event, 'acknowledge_action', create_event=1)
      transaction.commit()
      self.tic()
      self.assertEqual(len(event.getCausalityRelatedValueList()), 1)
      new_event = event.getCausalityRelatedValue()
      self.assertEqual(new_event.getFollowUp(), ticket_url)

    # if quote_original_message option is true, the new event content will be
    # the current event message quoted.
    for portal_type in event_type_list:
      ticket = self.portal.meeting_module.newContent(portal_type='Meeting',
                                                     title='Meeting1')
      ticket_url = ticket.getRelativeUrl()
      event = self.portal.event_module.newContent(portal_type=portal_type,
                                                  follow_up=ticket_url,
                                                  title='Event Title',
                                                  text_content='Event Content',
                                                  content_type='text/plain')
      transaction.commit()
      self.tic()
      self.assertEqual(len(event.getCausalityRelatedValueList()), 0)
      event.receive()
      portal_workflow.doActionFor(event, 'acknowledge_action',
                                  create_event=1,
                                  quote_original_message=1)
      transaction.commit()
      self.tic()
      self.assertEqual(len(event.getCausalityRelatedValueList()), 1)
      new_event = event.getCausalityRelatedValue()
      self.assertEqual(new_event.getFollowUp(), ticket_url)
      self.assertEqual(new_event.getContentType(), 'text/plain')
      self.assertEqual(new_event.getTextContent(), '> Event Content')
      self.assertEqual(new_event.getTitle(), 'Re: Event Title')


class TestCRMMailIngestion(BaseTestCRM):
  """Test Mail Ingestion for standalone CRM.
  """
  def getTitle(self):
    return "CRM Mail Ingestion"

  def getBusinessTemplateList(self):
    # Mail Ingestion must work with CRM alone.
    return ('erp5_base',
            'erp5_ingestion',
            'erp5_ingestion_mysql_innodb_catalog',
            'erp5_crm',
            )

  def afterSetUp(self):
    super(TestCRMMailIngestion, self).afterSetUp()
    portal = self.portal

    # create customer organisation and person
    portal.organisation_module.newContent(
            id='customer',
            portal_type='Organisation',
            title='Customer')
    customer_organisation = portal.organisation_module.customer
    portal.person_module.newContent(
            id='sender',
            title='Sender',
            subordination_value=customer_organisation,
            default_email_text='sender@customer.com')
    # also create the recipients
    portal.person_module.newContent(
            id='me',
            title='Me',
            default_email_text='me@erp5.org')
    portal.person_module.newContent(
            id='he',
            title='He',
            default_email_text='he@erp5.org')

    # make sure customers are available to catalog
    transaction.commit()
    self.tic()

  def _readTestData(self, filename):
    """read test data from data directory."""
    return file(os.path.join(os.path.dirname(__file__),
                             'test_data', 'crm_emails', filename)).read()

  def _ingestMail(self, filename=None, data=None):
    """ingest an email from the mail in data dir named `filename`"""
    if data is None:
      data=self._readTestData(filename)
    return self.portal.portal_contributions.newContent(
                    container_path='event_module',
                    file_name='postfix_mail.eml',
                    data=data)

  def test_findTypeByName_MailMessage(self):
    # without this, ingestion will not work
    self.assertEquals(
      'Mail Message',
      self.portal.portal_contribution_registry.findPortalTypeName(
      file_name='postfix_mail.eml', mime_type='message/rfc822', data='Test'
      ))

  def test_Base_getEntityListFromFromHeader(self):
    expected_values = (
      ('me@erp5.org', ['person_module/me']),
      ('me@erp5.org, he@erp5.org', ['person_module/me', 'person_module/he']),
      ('Sender <sender@customer.com>', ['person_module/sender']),
      # tricks to confuse the e-mail parser:
      # a comma in the name
      ('"Sender," <sender@customer.com>, he@erp5.org', ['person_module/sender',
                                                        'person_module/he']),
      # multiple e-mails in the "Name" part that shouldn't be parsed
      ('"me@erp5.org,sender@customer.com," <he@erp5.org>', ['person_module/he']),
      # capitalised version
      ('"me@erp5.org,sEnder@CUSTOMER.cOm," <he@ERP5.OrG>', ['person_module/he']),
      # a < sign
      ('"He<" <he@erp5.org>', ['person_module/he']),
    )
    portal = self.portal
    Base_getEntityListFromFromHeader = portal.Base_getEntityListFromFromHeader
    pc = self.portal.portal_catalog
    for header, expected_paths in expected_values:
      paths = [entity.getRelativeUrl()
               for entity in portal.Base_getEntityListFromFromHeader(header)] 
      self.assertEquals(paths, expected_paths,
                        '%r should return %r, but returned %r' %
                        (header, expected_paths, paths))

  def test_document_creation(self):
    # CRM email ingestion creates a Mail Message in event_module
    event = self._ingestMail('simple')
    self.assertEquals(len(self.portal.event_module), 1)
    self.assertEquals(event, self.portal.event_module.contentValues()[0])
    self.assertEquals('Mail Message', event.getPortalType())
    self.assertEquals('text/plain', event.getContentType())
    self.assertEquals('message/rfc822', event._baseGetContentType())
    # check if parsing of metadata from content is working
    content_dict = {'source_list': ['person_module/sender'],
                    'destination_list': ['person_module/me',
                                         'person_module/he']}
    self.assertEquals(event.getPropertyDictFromContent(), content_dict)

  def test_title(self):
    # title is found automatically, based on the Subject: header in the mail
    event = self._ingestMail('simple')
    self.assertEquals('Simple Mail Test', event.getTitle())
    self.assertEquals('Simple Mail Test', event.getTitleOrId())

  def test_asText(self):
    # asText requires portal_transforms
    event = self._ingestMail('simple')
    self.assertEquals('Hello,\nContent of the mail.\n', str(event.asText()))
 
  def test_sender(self):
    # source is found automatically, based on the From: header in the mail
    event = self._ingestMail('simple')
    # metadata discovery is done in an activity
    transaction.commit()
    self.tic()
    self.assertEquals('person_module/sender', event.getSource())

  def test_recipient(self):
    # destination is found automatically, based on the To: header in the mail
    event = self._ingestMail('simple')
    transaction.commit()
    self.tic()
    destination_list = event.getDestinationList()
    destination_list.sort()
    self.assertEquals(['person_module/he', 'person_module/me'],
                      destination_list)

  def test_clone(self):
    # cloning an event must keep title and text-content
    event = self._ingestMail('simple')
    transaction.commit()
    self.tic()
    self.assertEquals('Simple Mail Test', event.getTitle())
    self.assertEquals('Simple Mail Test', event.getTitleOrId())
    self.assertEquals('Hello,\nContent of the mail.\n', str(event.asText()))
    self.assertEquals('Hello,\nContent of the mail.\n', str(event.getTextContent()))
    self.assertEquals('Mail Message', event.getPortalType())
    self.assertEquals('text/plain', event.getContentType())
    self.assertEquals('message/rfc822', event._baseGetContentType())
    # check if parsing of metadata from content is working
    content_dict = {'source_list': ['person_module/sender'],
                    'destination_list': ['person_module/me',
                                         'person_module/he']}
    self.assertEquals(event.getPropertyDictFromContent(), content_dict)
    new_event = event.Base_createCloneDocument(batch_mode=1)
    transaction.commit()
    self.tic()
    self.assertEquals('Simple Mail Test', new_event.getTitle())
    self.assertEquals('Simple Mail Test', new_event.getTitleOrId())
    self.assertEquals('Hello,\nContent of the mail.\n', str(new_event.asText()))
    self.assertEquals('Hello,\nContent of the mail.\n', str(new_event.getTextContent()))
    self.assertEquals('Mail Message', new_event.getPortalType())
    self.assertEquals('text/plain', new_event.getContentType())
    self.assertEquals('message/rfc822', new_event._baseGetContentType())
    # check if parsing of metadata from content is working
    content_dict = {'source_list': ['person_module/sender'],
                    'destination_list': ['person_module/me',
                                         'person_module/he']}
    self.assertEquals(new_event.getPropertyDictFromContent(), content_dict)


  def test_follow_up(self):
    # follow up is found automatically, based on the content of the mail, and
    # what you defined in preference regexpr.
    # But, we don't want it to associate with the first campaign simply
    # because we searched against nothing
    self.portal.campaign_module.newContent(portal_type='Campaign')
    transaction.commit()
    self.tic()
    event = self._ingestMail('simple')
    transaction.commit()
    self.tic()
    self.assertEquals(None, event.getFollowUp())

  def test_portal_type_determination(self):
    """
    Make sure that ingested email will be correctly converted to
    appropriate portal type by email metadata.
    """
    message = email.message_from_string(self._readTestData('simple'))
    message.replace_header('subject', 'Visit:Company A')
    data = message.as_string()
    document = self._ingestMail(data=data)
    self.assertEqual(document.portal_type, 'Visit')
    self.assertEqual(document.getTitle(), 'Company A')

    message = email.message_from_string(self._readTestData('simple'))
    message.replace_header('subject', 'Fax:Company B')
    data = message.as_string()
    document = self._ingestMail(data=data)
    self.assertEqual(document.portal_type, 'Fax Message')
    self.assertEqual(document.getTitle(), 'Company B')

    message = email.message_from_string(self._readTestData('simple'))
    message.replace_header('subject', 'TEST:Company B')
    data = message.as_string()
    document = self._ingestMail(data=data)
    self.assertEqual(document.portal_type, 'Mail Message')
    self.assertEqual(document.getTitle(), 'TEST:Company B')

    message = email.message_from_string(self._readTestData('simple'))
    message.replace_header('subject', 'visit:Company A')
    data = message.as_string()
    document = self._ingestMail(data=data)
    self.assertEqual(document.portal_type, 'Visit')
    self.assertEqual(document.getTitle(), 'Company A')

    message = email.message_from_string(self._readTestData('simple'))
    message.replace_header('subject', 'phone:Company B')
    data = message.as_string()
    document = self._ingestMail(data=data)
    self.assertEqual(document.portal_type, 'Phone Call')
    self.assertEqual(document.getTitle(), 'Company B')

    message = email.message_from_string(self._readTestData('simple'))
    message.replace_header('subject', 'LETTER:Company C')
    data = message.as_string()
    document = self._ingestMail(data=data)
    self.assertEqual(document.portal_type, 'Letter')
    self.assertEqual(document.getTitle(), 'Company C')

    message = email.message_from_string(self._readTestData('simple'))
    body = message.get_payload()
    message.set_payload('Visit:%s' % body)
    data = message.as_string()
    document = self._ingestMail(data=data)
    self.assertEqual(document.portal_type, 'Visit')
    self.assertEqual(document.getTextContent(), body)

    message = email.message_from_string(self._readTestData('simple'))
    body = message.get_payload()
    message.set_payload('PHONE CALL:%s' % body)
    data = message.as_string()
    document = self._ingestMail(data=data)
    self.assertEqual(document.portal_type, 'Phone Call')
    self.assertEqual(document.getTextContent(), body)

  def test_forwarder_mail(self):
    """
    Make sure that if ingested email is forwarded one, the sender of
    original mail should be the sender of event and the sender of
    forwarded mail should be the recipient of event.
    """
    document = self._ingestMail(filename='forwarded')

    transaction.commit()
    self.tic()

    self.assertEqual(document.getContentInformation().get('From'), 'Me <me@erp5.org>')
    self.assertEqual(document.getContentInformation().get('To'), 'crm@erp5.org')
    self.assertEqual(document.getSourceValue().getTitle(), 'Sender')
    self.assertEqual(document.getDestinationValue().getTitle(), 'Me')

  def test_forwarder_mail_with_attachment(self):
    """
    Make sure that if ingested email is forwarded one, the sender of
    original mail should be the sender of event and the sender of
    forwarded mail should be the recipient of event.
    """
    document = self._ingestMail(filename='forwarded_attached')

    transaction.commit()
    self.tic()

    self.assertEqual(document.getContentInformation().get('From'), 'Me <me@erp5.org>')
    self.assertEqual(document.getContentInformation().get('To'), 'crm@erp5.org')
    self.assertEqual(document.getSourceValue().getTitle(), 'Sender')
    self.assertEqual(document.getDestinationValue().getTitle(), 'Me')

  def test_encoding(self):
    document = self._ingestMail(filename='encoded')

    transaction.commit()
    self.tic()

    self.assertEqual(document.getContentInformation().get('To'),
                     'Me <me@erp5.org>')
    self.assertEqual(document.getSourceValue().getTitle(), 'Sender')
    self.assertEqual(document.getDestinationValue().getTitle(), 'Me')
    self.assertEqual(document.getContentInformation().get('Subject'),
                     'Test éncödèd email')
    self.assertEqual(document.getTitle(), 'Test éncödèd email')
    self.assertEqual(document.getTextContent(), 'cöntént\n')


  def test_HTML_multipart_attachments(self):
    """Test that html attachments are cleaned up.
    and check the behaviour of getTextContent
    if multipart/alternative return html
    if multipart/mixed return text
    """
    document = self._ingestMail(filename='sample_multipart_mixed_and_alternative')
    transaction.commit()
    self.tic()
    stripped_html = document.asStrippedHTML()
    self.assertTrue('<form' not in stripped_html)
    self.assertTrue('<form' not in document.getAttachmentData(4))
    self.assertEquals('This is my content.\n*ERP5* is a Free _Software_\n',
                      document.getAttachmentData(2))
    self.assertEquals('text/html', document.getContentType())
    self.assertEquals('\n<html>\n<head>\n\n<meta http-equiv="content-type"'\
                      ' content="text/html; charset=utf-8" />\n'\
                      '</head>\n<body text="#000000"'\
                      ' bgcolor="#ffffff">\nThis is my content.<br />\n'\
                      '<b>ERP5</b> is a Free <u>Software</u><br />'\
                      '\n\n</body>\n</html>\n', document.getAttachmentData(3))
    self.assertEquals(document.getAttachmentData(3), document.getTextContent())

    # now check a message with multipart/mixed
    mixed_document = self._ingestMail(filename='sample_html_attachment')
    transaction.commit()
    self.tic()
    self.assertEquals(mixed_document.getAttachmentData(1),
                      mixed_document.getTextContent())
    self.assertEquals('Hi, this is the Message.\nERP5 is a free software.\n\n',
                      mixed_document.getTextContent())
    self.assertEquals('text/plain', mixed_document.getContentType())


## TODO:
##
##  def test_attachements(self):
##    event = self._ingestMail('with_attachements')
##

class TestCRMMailSend(BaseTestCRM):
  """Test Mail Sending for CRM
  """
  def getTitle(self):
    return "CRM Mail Sending"

  def getBusinessTemplateList(self):
    # In this test, We will attach some document portal types in event.
    # So we add DMS and Web.
    return ('erp5_base',
            'erp5_ingestion',
            'erp5_ingestion_mysql_innodb_catalog',
            'erp5_crm',
            'erp5_web',
            'erp5_dms',
            )

  def afterSetUp(self):
    super(TestCRMMailSend, self).afterSetUp()
    portal = self.portal

    # create customer organisation and person
    portal.organisation_module.newContent(
            id='customer',
            portal_type='Organisation',
            title='Customer')
    customer_organisation = portal.organisation_module.customer
    portal.person_module.newContent(
            id='recipient',
            # The ',' below is to force quoting of the name in e-mail
            # addresses on Zope 2.12
            title='Recipient,',
            subordination_value=customer_organisation,
            default_email_text='recipient@example.com')
    # also create the sender
    portal.person_module.newContent(
            id='me',
            # The ',' below is to force quoting of the name in e-mail
            # addresses on Zope 2.12
            title='Me,',
            default_email_text='me@erp5.org')

    # set preference
    default_pref = self.portal.portal_preferences.default_site_preference
    conversion_dict = _getConversionServerDict()
    default_pref.setPreferredOoodocServerAddress(conversion_dict['hostname'])
    default_pref.setPreferredOoodocServerPortNumber(conversion_dict['port'])
    default_pref.setPreferredDocumentFileNameRegularExpression(FILE_NAME_REGULAR_EXPRESSION)
    default_pref.setPreferredDocumentReferenceRegularExpression(REFERENCE_REGULAR_EXPRESSION)
    if default_pref.getPreferenceState() == 'disabled':
      default_pref.enable()

    # make sure customers are available to catalog
    transaction.commit()
    self.tic()

  def test_MailFromMailMessageEvent(self):
    # passing start_action transition on event workflow will send an email to the
    # person as destination
    text_content = 'Mail Content'
    event = self.portal.event_module.newContent(portal_type='Mail Message')
    event.setSource('person_module/me')
    event.setDestination('person_module/recipient')
    event.setTitle('A Mail')
    event.setTextContent(text_content)
    self.portal.portal_workflow.doActionFor(event, 'start_action',
                                            send_mail=1)
    transaction.commit()
    self.tic()
    last_message = self.portal.MailHost._last_message
    self.assertNotEquals((), last_message)
    mfrom, mto, messageText = last_message
    self.assertEquals('"Me," <me@erp5.org>', mfrom)
    self.assertEquals(['"Recipient," <recipient@example.com>'], mto)
    self.assertEquals(event.getTextContent(), text_content)
    message = email.message_from_string(messageText)

    self.assertEquals('A Mail',
                      email.Header.decode_header(message['Subject'])[0][0])
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
    self.assertEqual(text_content, part.get_payload(decode=True))

    #
    # Test multiple recipients.
    #
    event = self.portal.event_module.newContent(portal_type='Mail Message')
    event.setSource('person_module/me')
    # multiple recipients.
    event.setDestinationList(['person_module/recipient', 'person_module/me'])
    event.setTitle('A Mail')
    event.setTextContent(text_content)
    self.portal.portal_workflow.doActionFor(event, 'start_action',
                                            send_mail=1)
    transaction.commit()
    self.tic()
    last_message_1, last_message_2 = self.portal.MailHost._message_list[-2:]
    self.assertNotEquals((), last_message_1)
    self.assertNotEquals((), last_message_2)
    # check last message 1 and last message 2 (the order is random)
    # both should have 'From: Me'
    self.assertEquals(['"Me," <me@erp5.org>', '"Me," <me@erp5.org>'],
                      [x[0] for x in (last_message_1, last_message_2)])
    # one should have 'To: Me' and the other should have 'To: Recipient'
    self.assertEquals([['"Me," <me@erp5.org>'], ['"Recipient," <recipient@example.com>']],
                      sorted([x[1] for x in (last_message_1, last_message_2)]))

  def test_MailFromMailMessageEventNoSendMail(self):
    # passing start_action transition on event workflow will send an email to the
    # person as destination, unless you don't check "send_mail" box in the
    # workflow dialog
    event = self.portal.event_module.newContent(portal_type='Mail Message')
    event.setSource('person_module/me')
    event.setDestination('person_module/recipient')
    event.setTitle('A Mail')
    event.setTextContent('Mail Content')
    self.portal.portal_workflow.doActionFor(event, 'start_action',
                                            send_mail=1)
    transaction.commit()
    self.tic()
    # no mail sent
    last_message = self.portal.MailHost._last_message

  def test_MailFromOtherEvents(self):
    # passing start_action transition on event workflow will not send an email
    # when the portal type is not Mail Message
    for ptype in [t for t in self.portal.getPortalEventTypeList()
        if t not in ('Mail Message', 'Document Ingestion Message',
          'Acknowledgement')]:
      event = self.portal.event_module.newContent(portal_type=ptype)
      event.setSource('person_module/me')
      event.setDestination('person_module/recipient')
      event.setTextContent('Hello !')
      self.portal.portal_workflow.doActionFor(event, 'start_action',
                                              send_mail=1)

      transaction.commit()
      self.tic()
      # this means no message have been set
      self.assertEquals((), self.portal.MailHost._last_message)

  def test_MailMarkPosted(self):
    # mark_started_action transition on event workflow will not send an email
    # even if the portal type is a Mail Message
    for ptype in [x for x in self.portal.getPortalEventTypeList() if x !=
        'Acknowledgement']:
      event = self.portal.event_module.newContent(portal_type=ptype)
      event.setSource('person_module/me')
      event.setDestination('person_module/recipient')
      event.setTextContent('Hello !')
      self.portal.portal_workflow.doActionFor(event, 'receive_action')
      self.portal.portal_workflow.doActionFor(event, 'mark_started_action')

      transaction.commit()
      self.tic()
      # this means no message have been set
      self.assertEquals((), self.portal.MailHost._last_message)


  def test_MailMessageHTML(self):
    # test sending a mail message edited as HTML (the default with FCKEditor),
    # then the mail should have HTML.
    text_content = 'Hello<br/>World'
    event = self.portal.event_module.newContent(portal_type='Mail Message')
    event.setSource('person_module/me')
    event.setDestination('person_module/recipient')
    event.setContentType('text/html')
    event.setTextContent(text_content)
    self.portal.portal_workflow.doActionFor(event, 'start_action',
                                            send_mail=1)
    transaction.commit()
    self.tic()
    self.assertEquals(event.getTextContent(), text_content)
    last_message = self.portal.MailHost._last_message
    self.assertNotEquals((), last_message)
    mfrom, mto, messageText = last_message
    self.assertEquals('"Me," <me@erp5.org>', mfrom)
    self.assertEquals(['"Recipient," <recipient@example.com>'], mto)

    message = email.message_from_string(messageText)
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/html':
        part = i
    self.assertNotEqual(part, None)
    self.assertEqual('<html><body>%s</body></html>' % text_content, part.get_payload(decode=True))

  @expectedFailure
  def test_MailMessageHTMLbis(self):
    # test sending a mail message edited as HTML (the default with FCKEditor),
    # then the mail should have HTML
    text_content = 'Hello<br/>World'
    event = self.portal.event_module.newContent(portal_type='Mail Message')
    event.setSource('person_module/me')
    event.setDestination('person_module/recipient')
    event.setContentType('text/html')
    event.setTextContent(text_content)
    self.portal.portal_workflow.doActionFor(event, 'start_action',
                                            send_mail=1)
    transaction.commit()
    self.tic()
    # This test fails because of known issue for outgoing emails.
    # there is conflict between properties from data
    # and properties from document.
    self.assertEquals(event.getContentType(), 'text/html')

  def test_MailMessageEncoding(self):
    # test sending a mail message with non ascii characters
    event = self.portal.event_module.newContent(portal_type='Mail Message')
    event.setSource('person_module/me')
    event.setDestination('person_module/recipient')
    event.setTitle('Héhé')
    event.setTextContent('Hàhà')
    self.portal.portal_workflow.doActionFor(event, 'start_action',
                                            send_mail=1)
    transaction.commit()
    self.tic()
    last_message = self.portal.MailHost._last_message
    self.assertNotEquals((), last_message)
    mfrom, mto, messageText = last_message
    self.assertEquals('"Me," <me@erp5.org>', mfrom)
    self.assertEquals(['"Recipient," <recipient@example.com>'], mto)
    
    message = email.message_from_string(messageText)

    self.assertEquals('Héhé',
                      email.Header.decode_header(message['Subject'])[0][0])
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
    self.assertEqual('Hàhà', part.get_payload(decode=True))

  def test_MailAttachmentPdf(self):
    """
    Make sure that pdf document is correctly attached in email
    """
    # Add a document which will be attached.

    def add_document(filename, id, container, portal_type):
      f = makeFileUpload(filename)
      document = container.newContent(id=id, portal_type=portal_type)
      document.edit(file=f, reference=filename)
      return document

    # pdf
    document_pdf = add_document('sample_attachment.pdf', '1',
                                self.portal.document_module, 'PDF')

    transaction.commit()
    self.tic()

    # Add a ticket
    ticket = self.portal.campaign_module.newContent(id='1',
                                                    portal_type='Campaign',
                                                    title='Advertisement')
    # Create a event
    ticket.Ticket_newEvent(portal_type='Mail Message',
                           title='Our new product',
                           description='Buy this now!',
                           direction='outgoing')

    # Set sender and attach a document to the event.
    event = self.portal.event_module.objectValues()[0]
    event.edit(source='person_module/me',
               destination='person_module/recipient',
               aggregate=document_pdf.getRelativeUrl(),
               text_content='This is an advertisement mail.')

    mail_text = event.send(download=True)

    # Check mail text.
    message = email.message_from_string(mail_text)
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
    self.assertEqual(part.get_payload(decode=True), event.getTextContent())

    # Check attachment
    # pdf
    self.assert_('sample_attachment.pdf' in 
                 [i.get_filename() for i in message.get_payload()])
    part = None
    for i in message.get_payload():
      if i.get_filename()=='sample_attachment.pdf':
        part = i
    self.assertEqual(part.get_payload(decode=True), str(document_pdf.getData()))

  def test_MailAttachmentText(self):
    """
    Make sure that text document is correctly attached in email
    """
    # Add a document which will be attached.

    def add_document(filename, id, container, portal_type):
      f = makeFileUpload(filename)
      document = container.newContent(id=id, portal_type=portal_type)
      document.edit(file=f, reference=filename)
      return document

    # odt
    document_odt = add_document('sample_attachment.odt', '2',
                                self.portal.document_module, 'Text')
    
    transaction.commit()
    self.tic()

    # Add a ticket
    ticket = self.portal.campaign_module.newContent(id='1',
                                                    portal_type='Campaign',
                                                    title='Advertisement')
    # Create a event
    ticket.Ticket_newEvent(portal_type='Mail Message',
                           title='Our new product',
                           description='Buy this now!',
                           direction='outgoing')

    # Set sender and attach a document to the event.
    event = self.portal.event_module.objectValues()[0]
    event.edit(source='person_module/me',
               destination='person_module/recipient',
               aggregate=document_odt.getRelativeUrl(),
               text_content='This is an advertisement mail.')

    mail_text = event.send(download=True)

    # Check mail text.
    message = email.message_from_string(mail_text)
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
    self.assertEqual(part.get_payload(decode=True), event.getTextContent())

    # Check attachment
    # odt
    self.assert_('sample_attachment.odt' in 
                 [i.get_filename() for i in message.get_payload()])
    part = None
    for i in message.get_payload():
      if i.get_filename()=='sample_attachment.odt':
        part = i
    self.assert_(len(part.get_payload(decode=True))>0)

  def test_MailAttachmentFile(self):
    """
    Make sure that file document is correctly attached in email
    """
    # Add a document which will be attached.

    def add_document(filename, id, container, portal_type):
      f = makeFileUpload(filename)
      document = container.newContent(id=id, portal_type=portal_type)
      document.edit(file=f, reference=filename)
      return document

    # zip
    document_zip = add_document('sample_attachment.zip', '3',
                                self.portal.document_module, 'File')

    transaction.commit()
    self.tic()

    # Add a ticket
    ticket = self.portal.campaign_module.newContent(id='1',
                                                    portal_type='Campaign',
                                                    title='Advertisement')
    # Create a event
    ticket.Ticket_newEvent(portal_type='Mail Message',
                           title='Our new product',
                           description='Buy this now!',
                           direction='outgoing')

    # Set sender and attach a document to the event.
    event = self.portal.event_module.objectValues()[0]
    event.edit(source='person_module/me',
               destination='person_module/recipient',
               aggregate=document_zip.getRelativeUrl(),
               text_content='This is an advertisement mail.')

    mail_text = event.send(download=True)

    # Check mail text.
    message = email.message_from_string(mail_text)
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
    self.assertEqual(part.get_payload(decode=True), event.getTextContent())

    # Check attachment
    # zip
    self.assert_('sample_attachment.zip' in 
                 [i.get_filename() for i in message.get_payload()])
    part = None
    for i in message.get_payload():
      if i.get_filename()=='sample_attachment.zip':
        part = i
    self.assert_(len(part.get_payload(decode=True))>0)

  def test_MailAttachmentImage(self):
    """
    Make sure that image document is correctly attached in email
    """
    # Add a document which will be attached.

    def add_document(filename, id, container, portal_type):
      f = makeFileUpload(filename)
      document = container.newContent(id=id, portal_type=portal_type)
      document.edit(file=f, reference=filename)
      return document

    # gif
    document_gif = add_document('sample_attachment.gif', '4',
                                self.portal.image_module, 'Image')

    transaction.commit()
    self.tic()

    # Add a ticket
    ticket = self.portal.campaign_module.newContent(id='1',
                                                    portal_type='Campaign',
                                                    title='Advertisement')
    # Create a event
    ticket.Ticket_newEvent(portal_type='Mail Message',
                           title='Our new product',
                           description='Buy this now!',
                           direction='outgoing')

    # Set sender and attach a document to the event.
    event = self.portal.event_module.objectValues()[0]
    event.edit(source='person_module/me',
               destination='person_module/recipient',
               aggregate=document_gif.getRelativeUrl(),
               text_content='This is an advertisement mail.')

    mail_text = event.send(download=True)

    # Check mail text.
    message = email.message_from_string(mail_text)
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
    self.assertEqual(part.get_payload(decode=True), event.getTextContent())

    # Check attachment
    # gif
    self.assert_('sample_attachment.gif' in 
                 [i.get_filename() for i in message.get_payload()])
    part = None
    for i in message.get_payload():
      if i.get_filename()=='sample_attachment.gif':
        part = i
    self.assertEqual(part.get_payload(decode=True), str(document_gif.getData()))

  def test_MailAttachmentWebPage(self):
    """
    Make sure that webpage document is correctly attached in email
    """
    # Add a document which will be attached.

    document_html = self.portal.web_page_module.newContent(id='5',
                                                           portal_type='Web Page')
    document_html.edit(text_content='<html><body>Hello world!</body></html>',
                       reference='sample_attachment.html')

    transaction.commit()
    self.tic()

    # Add a ticket
    ticket = self.portal.campaign_module.newContent(id='1',
                                                    portal_type='Campaign',
                                                    title='Advertisement')
    # Create a event
    ticket.Ticket_newEvent(portal_type='Mail Message',
                           title='Our new product',
                           description='Buy this now!',
                           direction='outgoing')

    # Set sender and attach a document to the event.
    event = self.portal.event_module.objectValues()[0]
    event.edit(source='person_module/me',
               destination='person_module/recipient',
               aggregate=document_html.getRelativeUrl(),
               text_content='This is an advertisement mail.')

    mail_text = event.send(download=True)

    # Check mail text.
    message = email.message_from_string(mail_text)
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
    self.assertEqual(part.get_payload(decode=True), event.getTextContent())

    # Check attachment
    # html
    self.assert_('sample_attachment.html' in 
                 [i.get_filename() for i in message.get_payload()])
    part = None
    for i in message.get_payload():
      if i.get_filename()=='sample_attachment.html':
        part = i
    self.assertEqual(part.get_payload(decode=True),
                     str(document_html.getTextContent()))
    self.assertEqual(part.get_content_type(), 'text/html')

  def test_MailRespond(self):
    """
    Test we can answer an incoming event and quote it
    """
    # Add a ticket
    ticket = self.portal.campaign_module.newContent(id='1',
                                                    portal_type='Campaign',
                                                    title='Advertisement')
    # Create a event
    ticket.Ticket_newEvent(portal_type='Mail Message',
                           title='Our new product',
                           description='Buy this now!',
                           direction='incoming')

    # Set sender and attach a document to the event.
    event = self.portal.event_module.objectValues()[0]
    event.edit(source='person_module/me',
               destination='person_module/recipient',
               text_content='This is an advertisement mail.')
    first_event_id = event.getId()
    self.getWorkflowTool().doActionFor(event, 'respond_action', 
                                       respond_event_portal_type = "Mail Message",
                                       respond_event_title = "Answer",
                                       respond_event_text_content="> This is an advertisement mail."
                                       )

    self.assertEqual(event.getSimulationState(), "responded")

    # answer event must have been created
    self.assertEqual(len(self.portal.event_module), 2)
    for ev in self.portal.event_module.objectValues():
      if ev.getId() != first_event_id:
        answer_event = ev

    # check properties of answer event
    self.assertEqual(answer_event.getSimulationState(), "started")
    self.assertEqual(answer_event.getCausality(), event.getRelativeUrl())
    self.assertEqual(answer_event.getDestination(), 'person_module/me')
    self.assertEqual(answer_event.getSource(), 'person_module/recipient')
    self.assertEqual(answer_event.getTextContent(), '> This is an advertisement mail.')
    self.assertEqual(answer_event.getFollowUpValue(), ticket)
    self.assert_(answer_event.getData() is not None)

  def test_MailAttachmentFileWithoutDMS(self):
    """
    Make sure that file document is correctly attached in email
    """
    # Add a document on a person which will be attached.

    def add_document(filename, id, container, portal_type):
      f = makeFileUpload(filename)
      document = container.newContent(id=id, portal_type=portal_type)
      document.edit(file=f, reference=filename)
      return document

    # txt
    document_txt = add_document('sample_attachment.txt', '2',
                                self.portal.person_module['me'], 'File')

    transaction.commit()
    self.tic()

    # Add a ticket
    ticket = self.portal.campaign_module.newContent(id='1',
                                                    portal_type='Campaign',
                                                    title='Advertisement')
    # Create a event
    ticket.Ticket_newEvent(portal_type='Mail Message',
                           title='Our new product',
                           description='Buy this now!',
                           direction='outgoing')

    # Set sender and attach a document to the event.
    event = self.portal.event_module.objectValues()[0]
    event.edit(source='person_module/me',
               destination='person_module/recipient',
               aggregate=document_txt.getRelativeUrl(),
               text_content='This is an advertisement mail.')

    mail_text = event.send(download=True)

    # Check mail text.
    message = email.message_from_string(mail_text)
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
        break
    self.assertEqual(part.get_payload(decode=True), event.getTextContent())

    # Check attachment
    # txt
    self.assert_('sample_attachment.txt' in 
                 [i.get_filename() for i in message.get_payload()])
    part = None
    for i in message.get_payload():
      if i.get_filename()=='sample_attachment.txt':
        part = i
    self.assert_(len(part.get_payload(decode=True))>0)



  def test_MailAttachmentImageWithoutDMS(self):
    """
    Make sure that image document is correctly attached in email without dms
    """
    # Add a document on a person which will be attached.

    def add_document(filename, id, container, portal_type):
      f = makeFileUpload(filename)
      document = container.newContent(id=id, portal_type=portal_type)
      document.edit(file=f, reference=filename)
      return document

    # gif
    document_gif = add_document('sample_attachment.gif', '1',
                                self.portal.person_module['me'], 'Image')

    transaction.commit()
    self.tic()

    # Add a ticket
    ticket = self.portal.campaign_module.newContent(id='1',
                                                    portal_type='Campaign',
                                                    title='Advertisement')
    # Create a event
    ticket.Ticket_newEvent(portal_type='Mail Message',
                           title='Our new product',
                           description='Buy this now!',
                           direction='outgoing')

    # Set sender and attach a document to the event.
    event = self.portal.event_module.objectValues()[0]
    event.edit(source='person_module/me',
               destination='person_module/recipient',
               aggregate=document_gif.getRelativeUrl(),
               text_content='This is an advertisement mail.')

    mail_text = event.send(download=True)

    # Check mail text.
    message = email.message_from_string(mail_text)
    part = None
    for i in message.get_payload():
      if i.get_content_type()=='text/plain':
        part = i
    self.assertEqual(part.get_payload(decode=True), event.getTextContent())

    # Check attachment
    # gif
    self.assert_('sample_attachment.gif' in 
                 [i.get_filename() for i in message.get_payload()])
    part = None
    for i in message.get_payload():
      if i.get_filename()=='sample_attachment.gif':
        part = i
    self.assertEqual(part.get_payload(decode=True), str(document_gif.getData()))

  def test_cloneEvent(self):
    """
      All events uses after script and interaciton
      workflow add a test for clone
    """
    portal_type = "Mail Message"
    title = "Title of the event"
    content = "This is the content of the event"
    event = self.portal.event_module.newContent(portal_type=portal_type,
                                                title=title,
                                                text_content=content,)
    event.setData("This is the context of the event...")

    self.stepTic()
    new_event = event.Base_createCloneDocument(batch_mode=1)
    self.failIf(new_event.hasFile())
    self.assertEquals(new_event.getData(), "")
    self.assertEquals(new_event.getTitle(), title)
    self.assertEquals(new_event.getTextContent(), content)


def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestCRM))
  suite.addTest(unittest.makeSuite(TestCRMMailIngestion))
  suite.addTest(unittest.makeSuite(TestCRMMailSend))
  return suite
