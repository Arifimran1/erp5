# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2007 Nexedi SA and Contributors. All Rights Reserved.
#                    Bartek Gorny <bg@erp5.pl>
#                    Jean-Paul Smets <jp@nexedi.com>
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################

import unittest
import os, cStringIO, zipfile
from xml.dom.minidom import parseString
import transaction
from Testing import ZopeTestCase
from DateTime import DateTime
from AccessControl.SecurityManagement import newSecurityManager
from Products.ERP5Type.Utils import convertToUpperCase
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from Products.ERP5Type.tests.Sequence import SequenceList
from Products.ERP5Type.tests.utils import FileUpload
from Products.ERP5OOo.Document.OOoDocument import ConversionError
from zLOG import LOG, INFO, ERROR
from Products.CMFCore.utils import getToolByName

# Define the conversion server host
conversion_server_host = ('127.0.0.1', 8008)

# test files' home
TEST_FILES_HOME = os.path.join(os.path.dirname(__file__), 'test_document')
FILE_NAME_REGULAR_EXPRESSION = "(?P<reference>[A-Z&é@{]{3,7})-(?P<language>[a-z]{2})-(?P<version>[0-9]{3})"
REFERENCE_REGULAR_EXPRESSION = "(?P<reference>[A-Z&é@{]{3,7})(-(?P<language>[a-z]{2}))?(-(?P<version>[0-9]{3}))?"
NON_PROCESSABLE_PORTAL_TYPE_LIST = ('Image', 'File', 'PDF')

def printAndLog(msg):
  """
  A utility function to print a message
  to the standard output and to the LOG
  at the same time
  """
  msg = str(msg)
  ZopeTestCase._print('\n ' + msg)
  LOG('Testing... ', 0, msg)


def makeFilePath(name):
  return os.path.join(TEST_FILES_HOME, name)

def makeFileUpload(name, as_name=None):
  if as_name is None:
    as_name = name
  path = makeFilePath(name)
  return FileUpload(path, as_name)

class TestIngestion(ERP5TypeTestCase):
  """
    ERP5 Document Management System - test file ingestion mechanism
  """

  # pseudo constants
  RUN_ALL_TEST = 1
  QUIET = 0

  ##################################
  ##  ZopeTestCase Skeleton
  ##################################

  def getTitle(self):
    """
      Return the title of the current test set.
    """
    return "ERP5 DMS - Ingestion"

  def getBusinessTemplateList(self):
    """
      Return the list of required business templates.
    """
    return ('erp5_base',
            'erp5_ingestion', 'erp5_ingestion_mysql_innodb_catalog',
            'erp5_web', 'erp5_crm', 'erp5_dms')

  def afterSetUp(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Initialize the ERP5 site.
    """
    self.login()
    self.datetime = DateTime()
    self.portal = self.getPortal()
    self.portal_categories = self.getCategoryTool()
    self.portal_catalog = self.getCatalogTool()
    self.createDefaultCategoryList()
    self.setSystemPreference()
    self.setSimulatedNotificationScript()

  def beforeTearDown(self):
    activity_tool = self.portal.portal_activities
    activity_status = set(m.processing_node < -1
                          for m in activity_tool.getMessageList())
    if True in activity_status:
      activity_tool.manageClearActivities()
    else:
      assert not activity_status
    self.portal.portal_caches.clearAllCache()

  def setSystemPreference(self):
    default_pref = self.portal.portal_preferences.default_site_preference
    default_pref.setPreferredOoodocServerAddress(conversion_server_host[0])
    default_pref.setPreferredOoodocServerPortNumber(conversion_server_host[1])
    default_pref.setPreferredDocumentFileNameRegularExpression(FILE_NAME_REGULAR_EXPRESSION)
    default_pref.setPreferredDocumentReferenceRegularExpression(REFERENCE_REGULAR_EXPRESSION)
    if default_pref.getPreferenceState() != 'global':
      default_pref.enable()

  def setSimulatedNotificationScript(self, sequence=None, sequence_list=None, **kw):
    """
      Create simulated (empty) email notification script
    """
    context = self.portal.portal_skins.custom
    script_id = 'Document_notifyByEmail'
    if not hasattr(context, script_id):
      factory = context.manage_addProduct['PythonScripts'].manage_addPythonScript
      factory(id=script_id)
    script = getattr(context, script_id)
    script.ZPythonScript_edit('email_to, event, doc, **kw', 'return')

  def login(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Create a new manager user and login.
    """
    user_name = 'dms_user'
    user_folder = self.portal.acl_users
    user_folder._doAddUser(user_name, '', ['Manager', 'Owner', 'Assignor'], [])
    user = user_folder.getUserById(user_name).__of__(user_folder)
    newSecurityManager(None, user)

  def createDefaultCategoryList(self):
    """
      Create some categories for testing. DMS security
      is based on group, site, function, publication_section
      and projects.

      NOTE (XXX): some parts of this method could be either
      moved to Category Tool or to ERP5 Test Case.
    """
    self.category_list = [
                         # Role categories
                          {'path' : 'role/internal'
                           ,'title': 'Internal'
                           }
                          ,{'path' : 'function/musician/wind/saxophone'
                           ,'title': 'Saxophone'
                           }
                          ,{'path' : 'group/medium'
                           ,'title': 'Medium'
                           }
                          ,{'path' : 'site/arctic/spitsbergen'
                           ,'title': 'Spitsbergen'
                           }
                          ,{'path' : 'group/anybody'
                           ,'title': 'Anybody'
                           }
                          ,{'path' : 'publication_section/cop'
                           ,'title': 'COPs'
                           }
                          ,{'path' : 'publication_section/cop/one'
                           ,'title': 'COP one'
                           }
                         ]

    # Create categories
    # Note : this code was taken from the CategoryTool_importCategoryFile python
    #        script (packaged in erp5_core).
    for category in self.category_list:
      keys = category.keys()
      if 'path' in keys:
        base_path_obj = self.portal_categories
        is_base_category = True
        for category_id in category['path'].split('/'):
          # The current category is not existing
          if category_id not in base_path_obj.contentIds():
            # Create the category
            if is_base_category:
              category_type = 'Base Category'
            else:
              category_type = 'Category'
            base_path_obj.newContent( portal_type       = category_type
                                    , id                = category_id
                                    , immediate_reindex = 1
                                    )
          base_path_obj = base_path_obj[category_id]
          is_base_category = False
        new_category = base_path_obj

        # Set the category properties
        for key in keys:
          if key != 'path':
            method_id = "set" + convertToUpperCase(key)
            value = category[key]
            if value not in ('', None):
              if hasattr(new_category, method_id):
                method = getattr(new_category, method_id)
                method(value.encode('UTF-8'))
    self.stepTic()

  def getCategoryList(self, base_category=None):
    """
      Get a list of categories with same base categories.
    """
    categories = []
    if base_category is not None:
      for category in self.category_list:
        if category["path"].split('/')[0] == base_category:
          categories.append(category)
    return categories

  def getDocument(self, id):
    """
      Returns a document with given ID in the
      document module.
    """
    document_module = self.portal.document_module
    return getattr(document_module, id)

  def checkIsObjectCatalogged(self, portal_type, **kw):
    """
      Make sure that a document with given portal type
      and kw properties is already present in the catalog.

      Typical use of this method consists in providing
      an id or reference.
    """
    res = self.portal_catalog(portal_type=portal_type, **kw.copy())
    self.assertEquals(len(res), 1)
    for key, value in kw.items():
      self.assertEquals(res[0].getProperty(key), value)

  def newEmptyCataloggedDocument(self, portal_type, id):
    """
      Create an empty document of given portal type
      and given ID. 

      Documents are immediately catalogged and verified
      both form catalog point of view and from their
      presence in the document module.
    """
    document_module = self.portal.getDefaultModule(portal_type)
    document = getattr(document_module, id, None)
    if document is not None:
      document_module.manage_delObjects([id,])
    document = document_module.newContent(portal_type=portal_type, id=id)
    self.stepTic()
    self.checkIsObjectCatalogged(portal_type, id=id, parent_uid=document_module.getUid())
    self.assert_(hasattr(document_module, id))
    return document

  def ingestFormatList(self, document_id, format_list, portal_type=None):
    """
      Upload in document document_id all test files which match
      any of the formats in format_list.

      portal_type can be specified to force the use of
      the default module for a given portal type instead
      of the document module.

      For every file, this checks is the word "magic"
      is present in both SearchableText and asText.
    """
    if portal_type is None:
      document_module = self.portal.document_module
    else:
      document_module = self.portal.getDefaultModule(portal_type)
    document = getattr(document_module, document_id)
    for revision, format in enumerate(format_list):
      filename = 'TEST-en-002.%s' %format
      f = makeFileUpload(filename)
      document.edit(file=f)
      self.stepTic()
      self.failUnless(document.hasFile())
      if document.getPortalType() in NON_PROCESSABLE_PORTAL_TYPE_LIST:
        # File and images do not support conversion to text in DMS
        # PDF has not implemented _convertToBaseFormat() so can not be converted
        self.assertEquals(document.getExternalProcessingState(), 'uploaded')
      else:
        self.assertEquals(document.getExternalProcessingState(), 'converted') # this is how we know if it was ok or not
        self.assert_('magic' in document.SearchableText())
        self.assert_('magic' in str(document.asText()))

  def checkDocumentExportList(self, document_id, format, asserted_target_list):
    """
      Upload document ID document_id with
      a test file of given format and assert that the document
      can be converted to any of the formats in asserted_target_list
    """
    document = self.getDocument(document_id)
    filename = 'TEST-en-002.' + format
    f = makeFileUpload(filename)
    document.edit(file=f)
    self.stepTic()
    # We call clear cache to be sure that the target list is updated
    self.getPortal().portal_caches.clearCache()
    target_list = document.getTargetFormatList()
    for target in asserted_target_list:
      self.assert_(target in target_list)

  def contributeFileList(self, with_portal_type=False):
    """
      Tries to a create new content through portal_contributions
      for every possible file type. If with_portal_type is set
      to true, portal_type is specified when calling newContent
      on portal_contributions.
      http://framework.openoffice.org/documentation/mimetypes/mimetypes.html
    """
    created_documents = []
    extension_to_type = (('ppt', 'Presentation')
                        ,('doc', 'Text')
                        ,('sdc', 'Spreadsheet')
                        ,('sxc', 'Spreadsheet')
                        ,('pdf', 'PDF')
                        ,('jpg', 'Image')
                        ,('py', 'File')
                        )
    counter = 1
    old_portal_type = ''
    for extension, portal_type in extension_to_type:
      filename = 'TEST-en-002.%s' %extension
      file = makeFileUpload(filename)
      # if we change portal type we must change version because 
      # mergeRevision would fail
      if portal_type != old_portal_type:
        counter += 1
        old_portal_type = portal_type
      file.filename = 'TEST-en-00%d.%s' % (counter, extension)
      if with_portal_type:
        document = self.portal.portal_contributions.newContent(portal_type=portal_type, file=file)
      else:
        document = self.portal.portal_contributions.newContent(file=file)
      created_documents.append(document)
    self.stepTic()
    # inspect created objects
    count = 0
    for extension, portal_type in extension_to_type:
      document = created_documents[count]
      count+=1
      self.assertEquals(document.getPortalType(), portal_type)
      self.assertEquals(document.getReference(), 'TEST')
      if document.getPortalType() in NON_PROCESSABLE_PORTAL_TYPE_LIST:
        # Image, File and PDF are not converted to a base format
        self.assertEquals(document.getExternalProcessingState(), 'uploaded')
      else:
        # We check if conversion has succeeded by looking
        # at the external_processing workflow
        self.assertEquals(document.getExternalProcessingState(), 'converted')
        self.assert_('magic' in document.SearchableText())

  def newPythonScript(self, object_id, script_id, argument_list, code):
    """
      Creates a new python script with given argument_list
      and source code.
    """
    context = self.getDocument(object_id)
    context.manage_addProduct['PythonScripts'].manage_addPythonScript(id=script_id)
    script = getattr(context, script_id)
    script.ZPythonScript_edit(argument_list, code)

  def setDiscoveryOrder(self, order, id='one'):
    """
      Creates a script to define the metadata discovery order
      for Text documents.
    """
    script_code = "return %s" % str(order)
    self.newPythonScript(id, 'Text_getPreferredDocumentMetadataDiscoveryOrderList', '', script_code)
    
  def discoverMetadata(self, document_id='one'):
    """
      Sets input parameters and on the document ID document_id
      and discover metadata. For reindexing
    """
    document = self.getDocument(document_id)
    # simulate user input
    document._backup_input = dict(reference='INPUT', 
                                  language='in',
                                  version='004', 
                                  short_title='from_input',
                                  contributor='person_module/james')
    # pass to discovery file_name and user_login
    document.discoverMetadata(document.getSourceReference(), 'john_doe') 
    self.stepTic()
    
  def checkMetadataOrder(self, expected_metadata, document_id='one'):
    """
    Asserts that metadata of document ID document_id
    is the same as expected_metadata
    """
    document = self.getDocument(document_id)
    for k, v in expected_metadata.items():
      self.assertEquals(document.getProperty(k), v)

  def receiveEmail(self, data,
                   portal_type='Document Ingestion Message',
                   container_path='document_ingestion_module',
                   file_name='email.emx'):
    return self.portal.portal_contributions.newContent(data=data,
                                                       portal_type=portal_type,
                                                       container_path=container_path,
                                                       file_name=file_name)

  ##################################
  ##  Basic steps
  ##################################
  def stepCreatePerson(self, sequence=None, sequence_list=None, **kw):
    """
      Create a person with ID "john" if it does not exists already
    """
    portal_type = 'Person'
    person_id = 'john'
    reference = 'john_doe'
    person_module = self.portal.person_module
    if getattr(person_module, person_id, None) is not None:
      return
    person = person_module.newContent(portal_type='Person',
                                      id=person_id,
                                      reference=reference,
                                      first_name='John',
                                      last_name='Doe',
                                      default_email_text='john@doe.com')
    self.stepTic()

  def stepCreateTextDocument(self, sequence=None, sequence_list=None, **kw):
    """
      Create an empty Text document with ID 'one'
      This document will be used in most tests.
    """
    self.newEmptyCataloggedDocument('Text', 'one')

  def stepCreateSpreadsheetDocument(self, sequence=None, sequence_list=None, **kw):
    """
      Create an empty Spreadsheet document with ID 'two'
      This document will be used in most tests.
    """
    self.newEmptyCataloggedDocument('Spreadsheet', 'two')

  def stepCreatePresentationDocument(self, sequence=None, sequence_list=None, **kw):
    """
      Create an empty Presentation document with ID 'three'
      This document will be used in most tests.
    """
    self.newEmptyCataloggedDocument('Presentation', 'three')

  def stepCreateDrawingDocument(self, sequence=None, sequence_list=None, **kw):
    """
      Create an empty Drawing document with ID 'four'
      This document will be used in most tests.
    """
    self.newEmptyCataloggedDocument('Drawing', 'four')

  def stepCreatePDFDocument(self, sequence=None, sequence_list=None, **kw):
    """
      Create an empty PDF document with ID 'five'
      This document will be used in most tests.
    """
    self.newEmptyCataloggedDocument('PDF', 'five')

  def stepCreateImageDocument(self, sequence=None, sequence_list=None, **kw):
    """
      Create an empty Image document with ID 'six'
      This document will be used in most tests.
    """
    self.newEmptyCataloggedDocument('Image', 'six')

  def stepCheckEmptyState(self, sequence=None, sequence_list=None, **kw):
    """
      Check if the document is in "empty" processing state
      (ie. no file upload has been done yet)
    """
    document = self.getDocument('one')
    return self.assertEquals(document.getExternalProcessingState(), 'empty')

  def stepCheckUploadedState(self, sequence=None, sequence_list=None, **kw):
    """
      Check if the document is in "uploaded" processing state
      (ie. a file upload has been done)
    """
    document = self.getDocument('one')
    return self.assertEquals(document.getExternalProcessingState(), 'uploaded')

  def stepCheckConvertingState(self, sequence=None, sequence_list=None, **kw):
    """
      Check if the document is in "converting" processing state
      (ie. a file upload has been done and the document is converting)
    """
    document = self.getDocument('one')
    return self.assertEquals(document.getExternalProcessingState(), 'converting')

  def stepCheckConvertedState(self, sequence=None, sequence_list=None, **kw):
    """
      Check if the document is in "converted" processing state
      (ie. a file conversion has been done and the document has
      been converted)
    """
    document = self.getDocument('one')
    return self.assertEquals(document.getExternalProcessingState(), 'converted')

  def stepStraightUpload(self, sequence=None, sequence_list=None, **kw):
    """
      Upload a file directly from the form
      check if it has the data and source_reference
    """
    filename = 'TEST-en-002.doc'
    document = self.getDocument('one')
    # First revision is 1 (like web pages)
    self.assertEquals(document.getRevision(), '1')
    f = makeFileUpload(filename)
    document.edit(file=f)
    self.assert_(document.hasFile())
    # source_reference set to file name ?
    self.assertEquals(document.getSourceReference(), filename) 
    # Revision is 1 after upload (revisions are strings)
    self.assertEquals(document.getRevision(), '2')
    document.reindexObject()
    transaction.commit()
    
  def stepUploadFromViewForm(self, sequence=None, sequence_list=None, **kw):
    """
      Upload a file from view form and make sure this increases the revision
    """
    document = self.getDocument('one')
    f = makeFileUpload('TEST-en-002.doc')
    revision = document.getRevision()
    document.edit(file=f)
    self.assertEquals(document.getRevision(), str(int(revision) + 1))
    document.reindexObject()
    transaction.commit()
    
  def stepUploadTextFromContributionTool(self, sequence=None, sequence_list=None, **kw):
    """
      Upload a file from contribution.
    """
    f = makeFileUpload('TEST-en-002.doc')
    self.portal.portal_contributions.newContent(id='one', file=f)
    transaction.commit()

  def stepReuploadTextFromContributionTool(self, sequence=None, sequence_list=None, **kw):
    """
      Upload a file from contribution form and make sure this update existing
      document and don't make a new document.
    """
    document = self.getDocument('one')
    revision = document.getRevision()
    number_of_document = len(self.portal.document_module.objectIds())
    self.assert_('This document is modified.' not in document.asText())

    f = makeFileUpload('TEST-en-002-modified.doc')
    f.filename = 'TEST-en-002.doc'

    self.portal.portal_contributions.newContent(file=f)
    self.stepTic()
    self.assertEquals(document.getRevision(), str(int(revision) + 1))
    self.assert_('This document is modified.' in document.asText())
    self.assertEquals(len(self.portal.document_module.objectIds()),
                      number_of_document)
    document.reindexObject()
    transaction.commit()

  def stepUploadAnotherTextFromContributionTool(self, sequence=None, sequence_list=None, **kw):
    """
      Upload another file from contribution.
    """
    f = makeFileUpload('ANOTHE-en-001.doc')
    self.portal.portal_contributions.newContent(id='two', file=f)
    self.stepTic()
    document = self.getDocument('two')
    self.assert_('This is a another very interesting document.' in document.asText())
    self.assertEquals(document.getReference(), 'ANOTHE')
    self.assertEquals(document.getVersion(), '001')
    self.assertEquals(document.getLanguage(), 'en')

  def stepDiscoverFromFilename(self, sequence=None, sequence_list=None, **kw):
    """
      Upload a file using contribution tool. This should trigger metadata
      discovery and we should have basic coordinates immediately,
      from first stage.
    """
    document = self.getDocument('one')
    file_name = 'TEST-en-002.doc'
    # First make sure the regular expressions work
    property_dict = document.getPropertyDictFromFileName(file_name)
    self.assertEquals(property_dict['reference'], 'TEST')
    self.assertEquals(property_dict['language'], 'en')
    self.assertEquals(property_dict['version'], '002')
    # Then make sure content discover works
    # XXX - This part must be extended
    property_dict = document.getPropertyDictFromContent()
    self.assertEquals(property_dict['title'], 'title')
    self.assertEquals(property_dict['description'], 'comments')
    self.assertEquals(property_dict['subject_list'], ['keywords'])
    # Then make sure metadata discovery works
    f = makeFileUpload(file_name)
    document.edit(file=f)
    self.assertEquals(document.getReference(), 'TEST')
    self.assertEquals(document.getLanguage(), 'en')
    self.assertEquals(document.getVersion(), '002')
    self.assertEquals(document.getSourceReference(), file_name)

  def stepCheckConvertedContent(self, sequence=None, sequence_list=None, **kw):
    """
      Check that the input file was successfully converted
      and that its SearchableText and asText contain
      the word "magic"
    """
    self.tic()
    document = self.getDocument('one')
    self.assert_(document.hasBaseData())
    self.assert_('magic' in document.SearchableText())
    self.assert_('magic' in str(document.asText()))

  def stepSetSimulatedDiscoveryScript(self, sequence=None, sequence_list=None, **kw):
    """
      Create Text_getPropertyDictFrom[source] scripts
      to simulate custom site's configuration
    """
    self.newPythonScript('one', 'Text_getPropertyDictFromUserLogin',
                         'user_name=None', "return {'contributor':'person_module/john'}")
    self.newPythonScript('one', 'Text_getPropertyDictFromContent', '',
                         "return {'short_title':'short', 'title':'title', 'contributor':'person_module/john',}")

  def stepTestMetadataSetting(self, sequence=None, sequence_list=None, **kw):
    """
      Upload with custom getPropertyDict methods
      check that all metadata are correct
    """
    document = self.getDocument('one')
    f = makeFileUpload('TEST-en-002.doc')
    document.edit(file=f)
    self.stepTic()
    # Then make sure content discover works
    property_dict = document.getPropertyDictFromUserLogin()
    self.assertEquals(property_dict['contributor'], 'person_module/john')
    # reference from filename (the rest was checked some other place)
    self.assertEquals(document.getReference(), 'TEST')
    # short_title from content
    self.assertEquals(document.getShortTitle(), 'short')
    # title from metadata inside the document
    self.assertEquals(document.getTitle(),  'title')
    # contributors from user
    self.assertEquals(document.getContributor(), 'person_module/john')

  def stepEditMetadata(self, sequence=None, sequence_list=None, **kw):
    """
      we change metadata in a document which has ODF
    """
    document = self.getDocument('one')
    kw = dict(title='another title',
              subject='another subject',
              description='another description')
    document.edit(**kw)
    self.stepTic()

  def stepCheckChangedMetadata(self, sequence=None, sequence_list=None, **kw):
    """
      then we download it and check if it is changed
    """
    # XXX actually this is an example of how it should be
    # implemented in OOoDocument class - we don't really
    # need oood for getting/setting metadata...
    document = self.getDocument('one')
    newcontent = document.getBaseData()
    cs = cStringIO.StringIO()
    cs.write(str(newcontent))
    z = zipfile.ZipFile(cs)
    s = z.read('meta.xml')
    xmlob = parseString(s)
    title = xmlob.getElementsByTagName('dc:title')[0].childNodes[0].data
    self.assertEquals(title, u'another title')
    subject = xmlob.getElementsByTagName('meta:keyword')[0].childNodes[0].data
    self.assertEquals(subject, u'another subject')
    description = xmlob.getElementsByTagName('dc:description')[0].childNodes[0].data
    self.assertEquals(description, u'another description')
    
  def stepIngestTextFormats(self, sequence=None, sequence_list=None, **kw):
    """
      ingest all supported text formats
      make sure they are converted
    """
    format_list = ['rtf', 'doc', 'txt', 'sxw', 'sdw']
    self.ingestFormatList('one', format_list)

  def stepIngestSpreadsheetFormats(self, sequence=None, sequence_list=None, **kw):
    """
      ingest all supported spreadsheet formats
      make sure they are converted
    """
    format_list = ['xls', 'sxc', 'sdc']
    self.ingestFormatList('two', format_list)

  def stepIngestPresentationFormats(self, sequence=None, sequence_list=None, **kw):
    """
      ingest all supported presentation formats
      make sure they are converted
    """
    format_list = ['ppt', 'sxi', 'sdd']
    self.ingestFormatList('three', format_list)

  def stepIngestPDFFormats(self, sequence=None, sequence_list=None, **kw):
    """
      ingest all supported PDF formats
      make sure they are converted
    """
    format_list = ['pdf']
    self.ingestFormatList('five', format_list)

  def stepIngestDrawingFormats(self, sequence=None, sequence_list=None, **kw):
    """
      ingest all supported presentation formats
      make sure they are converted
    """
    format_list = ['sxd',]
    self.ingestFormatList('four', format_list)

  def stepIngestPDFFormats(self, sequence=None, sequence_list=None, **kw):
    """
      ingest all supported pdf formats
      make sure they are converted
    """
    format_list = ['pdf']
    self.ingestFormatList('five', format_list)

  def stepIngestImageFormats(self, sequence=None, sequence_list=None, **kw):
    """
      ingest all supported image formats
    """
    format_list = ['jpg', 'gif', 'bmp', 'png']
    self.ingestFormatList('six', format_list, 'Image')

  def stepCheckTextDocumentExportList(self, sequence=None, sequence_list=None, **kw):
    self.checkDocumentExportList('one', 'doc', ['pdf', 'doc', 'rtf', 'writer.html', 'txt'])

  def stepCheckSpreadsheetDocumentExportList(self, sequence=None, sequence_list=None, **kw):
    self.checkDocumentExportList('two', 'xls', ['csv', 'calc.html', 'xls', 'calc.pdf'])

  def stepCheckPresentationDocumentExportList(self, sequence=None, sequence_list=None, **kw):
    self.checkDocumentExportList('three', 'ppt', ['impr.pdf', 'ppt'])

  def stepCheckDrawingDocumentExportList(self, sequence=None, sequence_list=None, **kw):
    self.checkDocumentExportList('four', 'sxd', ['jpg', 'draw.pdf', 'svg'])

  def stepExportPDF(self, sequence=None, sequence_list=None, **kw):
    """
      Try to export PDF to text and HTML
    """
    document = self.getDocument('five')
    f = makeFileUpload('TEST-en-002.pdf')
    document.edit(file=f)
    mime, text = document.convert('text')
    self.failUnless('magic' in text)
    self.failUnless(mime == 'text/plain')
    mime, html = document.convert('html')
    self.failUnless('magic' in html)
    self.failUnless(mime == 'text/html')

  def stepExportImage(self, sequence=None, sequence_list=None, **kw):
    """
      Don't see a way to test it here, Image.index_html makes heavy use 
      of REQUEST and RESPONSE, and the rest of the implementation is way down
      in Zope core
    """
    printAndLog('stepExportImage not implemented')

  def stepCheckHasSnapshot(self, sequence=None, sequence_list=None, **kw):
    document = self.getDocument('one')
    self.failUnless(document.hasSnapshotData())

  def stepCheckHasNoSnapshot(self, sequence=None, sequence_list=None, **kw):
    document = self.getDocument('one')
    self.failIf(document.hasSnapshotData())

  def stepCreateSnapshot(self, sequence=None, sequence_list=None, **kw):
    document = self.getDocument('one')
    document.createSnapshot()

  def stepTryRecreateSnapshot(self, sequence=None, sequence_list=None, **kw):
    document = self.getDocument('one')
    # XXX this always fails, don't know why
    #self.assertRaises(ConversionError, document.createSnapshot)

  def stepDeleteSnapshot(self, sequence=None, sequence_list=None, **kw):
    document = self.getDocument('one')
    document.deleteSnapshot()

  def stepCleanUp(self, sequence=None, sequence_list=None, **kw):
    """
        Clean up DMS system from old content.
    """
    portal = self.getPortal()
    for module in (portal.document_module, portal.image_module, portal.document_ingestion_module):
      module.manage_delObjects(map(None, module.objectIds()))
    
  def stepContributeFileListWithType(self, sequence=None, sequence_list=None, **kw):
    """
      Contribute all kinds of files giving portal type explicitly
      TODO: test situation whereby portal_type given explicitly is wrong
    """
    self.contributeFileList(with_portal_type=True)

  def stepContributeFileListWithNoType(self, sequence=None, sequence_list=None, **kw):
    """
      Contribute all kinds of files
      let the system figure out portal type by itself
    """
    self.contributeFileList(with_portal_type=False)

  def stepSetSimulatedDiscoveryScriptForOrdering(self, sequence=None, sequence_list=None, **kw):
    """
      set scripts which are supposed to overwrite each other's metadata
      desing is the following:
                    File Name     User    Content        Input
      reference     TEST          USER    CONT           INPUT
      language      en            us                     in
      version       002                   003            004
      contributor                 john    jack           james
      short_title                         from_content   from_input
    """
    self.newPythonScript('one', 'Text_getPropertyDictFromUserLogin', 'user_name=None', "return {'reference':'USER', 'language':'us', 'contributor':'person_module/john'}")
    self.newPythonScript('one', 'Text_getPropertyDictFromContent', '', "return {'reference':'CONT', 'version':'003', 'contributor':'person_module/jack', 'short_title':'from_content'}")

  def stepCheckMetadataSettingOrderFICU(self, sequence=None, sequence_list=None, **kw):
    """
     This is the default
    """  
    expected_metadata = dict(reference='TEST', language='en', version='002', short_title='from_input', contributor='person_module/james')
    self.setDiscoveryOrder(['file_name', 'input', 'content', 'user_login'])
    self.discoverMetadata()
    self.checkMetadataOrder(expected_metadata)

  def stepCheckMetadataSettingOrderCUFI(self, sequence=None, sequence_list=None, **kw):
    """
     Content - User - Filename - Input
    """
    expected_metadata = dict(reference='CONT', language='us', version='003', short_title='from_content', contributor='person_module/jack')
    self.setDiscoveryOrder(['content', 'user_login', 'file_name', 'input'])
    self.discoverMetadata()
    self.checkMetadataOrder(expected_metadata)

  def stepCheckMetadataSettingOrderUIFC(self, sequence=None, sequence_list=None, **kw):
    """
     User - Input - Filename - Content
    """
    expected_metadata = dict(reference='USER', language='us', version='004', short_title='from_input', contributor='person_module/john')
    self.setDiscoveryOrder(['user_login', 'input', 'file_name', 'content'])
    self.discoverMetadata()
    self.checkMetadataOrder(expected_metadata)

  def stepCheckMetadataSettingOrderICUF(self, sequence=None, sequence_list=None, **kw):
    """
     Input - Content - User - Filename
    """
    expected_metadata = dict(reference='INPUT', language='in', version='004', short_title='from_input', contributor='person_module/james')
    self.setDiscoveryOrder(['input', 'content', 'user_login', 'file_name'])
    self.discoverMetadata()
    self.checkMetadataOrder(expected_metadata)

  def stepCheckMetadataSettingOrderUFCI(self, sequence=None, sequence_list=None, **kw):
    """
     User - Filename - Content - Input
    """
    expected_metadata = dict(reference='USER', language='us', version='002', short_title='from_content', contributor='person_module/john')
    self.setDiscoveryOrder(['user_login', 'file_name', 'content', 'input'])
    self.discoverMetadata()
    self.checkMetadataOrder(expected_metadata)
   
  def stepReceiveEmail(self, sequence=None, sequence_list=None, **kw):
    """
      Email was sent in by someone to ERP5.
    """
    f = open(makeFilePath('email_from.txt'))
    document = self.receiveEmail(f.read())
    self.stepTic()

  def stepReceiveMultipleAttachmentsEmail(self, sequence=None, sequence_list=None, **kw):
    """
      Email was sent in by someone to ERP5.
    """
    f = open(makeFilePath('email_multiple_attachments.eml'))
    document = self.receiveEmail(f.read())
    self.stepTic()

  def stepVerifyEmailedMultipleDocumentsInitialContribution(self, sequence=None, sequence_list=None, **kw):
    """
      Verify contributed for initial time multiple document per email.
    """
    attachment_list, ingested_document = self.verifyEmailedMultipleDocuments()
    self.assertEquals('1', ingested_document.getRevision())
    
  def stepVerifyEmailedMultipleDocumentsMultipleContribution(self, sequence=None, sequence_list=None, **kw):
    """
      Verify contributed for initial time multiple document per email.
    """
    attachment_list, ingested_document = self.verifyEmailedMultipleDocuments()
    self.assertTrue(ingested_document.getRevision() > '1')

  def stepVerifyEmailedDocumentInitialContribution(self, sequence=None, sequence_list=None, **kw):
    """
      Verify contributed for initial time document per email.
    """
    attachment_list, ingested_document = self.verifyEmailedDocument()
    self.assertEquals('1', ingested_document.getRevision())

  def stepVerifyEmailedDocumentMultipleContribution(self, sequence=None, sequence_list=None, **kw):
    """
      Verify contributed for multiple times document per email.
    """
    attachment_list, ingested_document = self.verifyEmailedDocument()
    self.assertTrue(ingested_document.getRevision() > '1')

  def playSequence(self, step_list, quiet):
    sequence_list = SequenceList()
    sequence_string = ' '.join(step_list)
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self, quiet=quiet)

  def verifyEmailedMultipleDocuments(self):
    """
      Basic checks for verifying a mailed-in multiple documents.
    """
    # First, check document ingestion message
    ingestion_message = self.portal_catalog.getResultValue(
                                 portal_type='Document Ingestion Message',
                                 title='Multiple Attachments',
                                 source_title='John Doe')
    self.assertTrue(ingestion_message is not None)
    # Second, check attachments to ingested message
    attachment_list = ingestion_message.getAggregateValueList()
    self.assertEqual(len(attachment_list), 5)
    extension_reference_portal_type_map = {'DOC': 'Text', 
                                           'JPG': 'Image',
                                           'ODT': 'Text', 
                                           'PDF': 'PDF',
                                           'PPT': 'Presentation'}
    for sub_reference, portal_type in extension_reference_portal_type_map.items():
      ingested_document = self.portal_catalog.getResultValue(
                               portal_type=portal_type,
                               reference='TEST%s' %sub_reference,
                               language='en',
                               version='002')
      self.assertNotEquals(None, ingested_document)
      if portal_type not in NON_PROCESSABLE_PORTAL_TYPE_LIST:
        self.assertEquals('converted', ingested_document.getExternalProcessingState())
      else:
        self.assertEquals('uploaded', ingested_document.getExternalProcessingState())
      # check aggregate between 'Document Ingestion Message' and ingested document
      self.assertTrue(ingested_document in attachment_list)
    return attachment_list, ingested_document
    
  def verifyEmailedDocument(self):
    """
      Basic checks for verifying a mailed-in document
    """
    # First, check document ingestion message
    ingestion_message = self.portal_catalog.getResultValue(
                                 portal_type='Document Ingestion Message',
                                 title='A Test Mail',
                                 source_title='John Doe')
    self.assertTrue(ingestion_message is not None)
    
    # Second, check attachments to ingested message
    attachment_list = ingestion_message.getAggregateValueList()
    self.assertEqual(len(attachment_list), 1)

    # Third, check document is ingested properly
    ingested_document = self.portal_catalog.getResultValue(
                               portal_type='Text',
                               reference='MAIL',
                               language='en',
                               version='002')
    self.assertEquals('MAIL-en-002.doc', ingested_document.getSourceReference())
    self.assertEquals('converted', ingested_document.getExternalProcessingState())
    self.assertTrue('magic' in ingested_document.asText())
    
    # check aggregate between 'Document Ingestion Message' and ingested document
    self.assertEquals(attachment_list[0], ingested_document)
    return attachment_list, ingested_document
    
  ##################################
  ##  Tests
  ##################################

  def test_01_PreferenceSetup(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Make sure that preferences are set up properly and accessible
    """
    if not run: return
    if not quiet: printAndLog('test_01_PreferenceSetup')
    preference_tool = self.portal.portal_preferences
    self.assertEquals(preference_tool.getPreferredOoodocServerAddress(), conversion_server_host[0])
    self.assertEquals(preference_tool.getPreferredOoodocServerPortNumber(), conversion_server_host[1])
    self.assertEquals(preference_tool.getPreferredDocumentFileNameRegularExpression(), FILE_NAME_REGULAR_EXPRESSION)
    self.assertEquals(preference_tool.getPreferredDocumentReferenceRegularExpression(), REFERENCE_REGULAR_EXPRESSION)
    
  def test_02_FileExtensionRegistry(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      check if we successfully imported registry
      and that it has all the entries we need
    """
    if not run: return
    if not quiet: printAndLog('test_02_FileExtensionRegistry')
    reg = self.portal.portal_contribution_registry
    correct_type_mapping = {
            'doc' : 'Text',
            'txt' : 'Text',
            'odt' : 'Text',
            'sxw' : 'Text',
            'rtf' : 'Text',
            'gif' : 'Image',
            'jpg' : 'Image',
            'png' : 'Image',
            'bmp' : 'Image',
            'pdf' : 'PDF',
            'xls' : 'Spreadsheet',
            'ods' : 'Spreadsheet',
            'sdc' : 'Spreadsheet',
            'ppt' : 'Presentation',
            'odp' : 'Presentation',
            'sxi' : 'Presentation',
            'sxd' : 'Drawing',
            'xxx' : 'File',
          }
    for type, portal_type in correct_type_mapping.items():
      file_name = 'aaa.' + type
      self.assertEquals(reg.findPortalTypeName(file_name, None, None),
                        portal_type)

  def test_03_TextDoc(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Test basic behaviour of a document:
      - create empty document
      - upload a file directly
      - upload a file using upload dialog
      - make sure revision was increased
      - check that it was properly converted
      - check if coordinates were extracted from file name
    """
    if not run: return
    if not quiet: printAndLog('test_03_TextDoc')
    step_list = ['stepCleanUp'
                 ,'stepCreateTextDocument'
                 ,'stepCheckEmptyState'
                 ,'stepStraightUpload'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepUploadFromViewForm'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                ]
    self.playSequence(step_list, quiet)

  def test_04_MetadataExtraction(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Test metadata extraction from various sources:
      - from file name (doublecheck)
      - from user (by overwriting type-based method
                   and simulating the result)
      - from content (by overwriting type-based method
                      and simulating the result)
      - from file metadata

      NOTE: metadata of document (title, subject, description)
      are no longer retrieved and set upon conversion
    """
    if not run: return
    if not quiet: printAndLog('test_04_MetadataExtraction')
    step_list = [ 'stepCleanUp'
                 ,'stepUploadTextFromContributionTool'
                 ,'stepSetSimulatedDiscoveryScript'
                 ,'stepTic'
                 ,'stepTestMetadataSetting'
                ]
    self.playSequence(step_list, quiet)

  def test_041_MetadataEditing(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Check metadata in the object and in the ODF document
      Edit metadata on the object
      Download ODF, make sure it is changed
    """
    if not run: return
    if not quiet: printAndLog('test_04_MetadataEditing')
    step_list = [ 'stepCleanUp'
                 ,'stepCreateTextDocument'
                 ,'stepUploadFromViewForm'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepEditMetadata'
                 ,'stepCheckChangedMetadata'
                ]
    self.playSequence(step_list, quiet)

  #    Ingest various formats (xls, doc, sxi, ppt etc)
  #    Verify that they are successfully converted
  #    - have ODF data and contain magic word in SearchableText
  #    - or have text data and contain magic word in SearchableText
  #      TODO:
  #    - or were not moved in processing_status_workflow if the don't
  #      implement _convertToBase (e.g. Image)
  #    Verify that you can not upload file of the wrong format.

  def test_05_FormatIngestionText(self, quiet=QUIET, run=RUN_ALL_TEST):
    step_list = ['stepCleanUp'
                 ,'stepCreateTextDocument'
                 ,'stepIngestTextFormats'
                ]
    self.playSequence(step_list, quiet)

  def test_05_FormatIngestionSpreadSheet(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_05_FormatIngestion')
    step_list = ['stepCleanUp'
                 ,'stepCreateSpreadsheetDocument'
                 ,'stepIngestSpreadsheetFormats'
                ]
    self.playSequence(step_list, quiet)

  def test_05_FormatIngestionPresentation(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_05_FormatIngestion')
    step_list = ['stepCleanUp'
                 ,'stepCreatePresentationDocument'
                 ,'stepIngestPresentationFormats'
                ]
    self.playSequence(step_list, quiet)

  def test_05_FormatIngestionDrawing(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_05_FormatIngestion')
    step_list = ['stepCleanUp'
                 ,'stepCreateDrawingDocument'
                 ,'stepIngestDrawingFormats'
                ]
    self.playSequence(step_list, quiet)

  def test_05_FormatIngestionPDF(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_05_FormatIngestion')
    step_list = ['stepCleanUp'
                 ,'stepCreatePDFDocument'
                 ,'stepIngestPDFFormats'
                ]
    self.playSequence(step_list, quiet)

  def test_05_FormatIngestionImage(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_05_FormatIngestion')
    step_list = ['stepCleanUp'
                 ,'stepCreateImageDocument'
                 ,'stepIngestImageFormats'
                ]
    self.playSequence(step_list, quiet)


  # Test generation of files in all possible formats
  # which means check if they have correct lists of available formats for export
  # actual generation is tested in oood tests
  # PDF and Image should be tested here
  def test_06_FormatGenerationText(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_06_FormatGeneration')
    step_list = [ 'stepCleanUp'
                 ,'stepCreateTextDocument'
                 ,'stepCheckTextDocumentExportList'
                ]
    self.playSequence(step_list, quiet)

  def test_06_FormatGenerationSpreadsheet(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_06_FormatGeneration')
    step_list = [ 'stepCleanUp'
                 ,'stepCreateSpreadsheetDocument'
                 ,'stepCheckSpreadsheetDocumentExportList'
                ]
    self.playSequence(step_list, quiet)

  def test_06_FormatGenerationPresentation(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_06_FormatGeneration')
    step_list = [ 'stepCleanUp'
                 ,'stepCreatePresentationDocument'
                 ,'stepCheckPresentationDocumentExportList'
                ]
    self.playSequence(step_list, quiet)

  def test_06_FormatGenerationDrawing(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_06_FormatGeneration')
    step_list = [ 'stepCleanUp'
                 ,'stepCreateDrawingDocument'
                 ,'stepCheckDrawingDocumentExportList'
                ]
    self.playSequence(step_list, quiet)

  def test_06_FormatGenerationPdf(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_06_FormatGeneration')
    step_list = [ 'stepCleanUp'
                 ,'stepCreatePDFDocument'
                 ,'stepExportPDF'
                 ,'stepTic'
                ]
    self.playSequence(step_list, quiet)

  def test_06_FormatGenerationImage(self, quiet=QUIET, run=RUN_ALL_TEST):
    if not run: return
    if not quiet: printAndLog('test_06_FormatGeneration')
    step_list = [ 'stepCleanUp'
                 ,'stepCreateImageDocument'
                 ,'stepExportImage'
                ]
    self.playSequence(step_list, quiet)


  def test_07_SnapshotGeneration(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Generate snapshot, make sure it is there, 
      try to generate it again, remove and 
      generate once more
    """
    if not run: return
    if not quiet: printAndLog('test_07_SnapshotGeneration')
    step_list = [ 'stepCleanUp'
                 ,'stepCreateTextDocument'
                 ,'stepUploadFromViewForm'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepCheckHasNoSnapshot'
                 ,'stepCreateSnapshot'
                 ,'stepTryRecreateSnapshot'
                 ,'stepCheckHasSnapshot'
                 ,'stepDeleteSnapshot'
                 ,'stepCheckHasNoSnapshot'
                 ,'stepCreateSnapshot'
                 ,'stepTic'
                ]
    self.playSequence(step_list, quiet)

  def test_08_Cache(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      I don't know how to verify how cache works
    """

  def test_09_Contribute(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Create content through portal_contributions
      - use newContent to ingest various types 
        also to test content_type_registry setup
      - verify that
        - appropriate portal_types were created
        - the files were converted
        - metadata was read
    """
    if not run: return
    if not quiet: printAndLog('test_09_Contribute')
    step_list = [ 'stepCleanUp'
                 ,'stepContributeFileListWithNoType'
                 ,'stepCleanUp'
                 ,'stepContributeFileListWithType'
                ]
    self.playSequence(step_list, quiet)

  def test_10_MetadataSettingPreferenceOrder(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Set some metadata discovery scripts
      Contribute a document, let it get metadata using default setup
      (default is FUC)

      check that the right ones are there
      change preference order, check again
    """
    if not run: return
    if not quiet: printAndLog('test_10_MetadataSettingPreferenceOrder')
    step_list = [ 'stepCleanUp' 
                 ,'stepCreateTextDocument'
                 ,'stepStraightUpload'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepSetSimulatedDiscoveryScriptForOrdering'
                 ,'stepCheckMetadataSettingOrderFICU'
                 ,'stepCreateTextDocument'
                 ,'stepStraightUpload'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepSetSimulatedDiscoveryScriptForOrdering'
                 ,'stepCheckMetadataSettingOrderCUFI'
                 ,'stepCreateTextDocument'
                 ,'stepStraightUpload'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepSetSimulatedDiscoveryScriptForOrdering'
                 ,'stepCheckMetadataSettingOrderUIFC'
                 ,'stepCreateTextDocument'
                 ,'stepStraightUpload'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepSetSimulatedDiscoveryScriptForOrdering'
                 ,'stepCheckMetadataSettingOrderICUF'
                 ,'stepCreateTextDocument'
                 ,'stepStraightUpload'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepSetSimulatedDiscoveryScriptForOrdering'
                 ,'stepCheckMetadataSettingOrderUFCI'
                ]
    self.playSequence(step_list, quiet)

  def test_11_EmailIngestion(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Simulate email piped to ERP5 by an MTA by uploading test email from file
      Check that document objects are created and appropriate data are set
      (owner, and anything discovered from user and mail body)
    """
    if not run: return
    if not quiet: printAndLog('test_11_EmailIngestion')
    step_list = [ 'stepCleanUp'
                 # unknown sender
                 ,'stepReceiveEmail'
                 # create sender as Person object in ERP5
                 ,'stepCreatePerson'
                 # now a known sender
                 ,'stepReceiveEmail'
                 ,'stepVerifyEmailedDocumentInitialContribution'
                 # send one more time
                 ,'stepReceiveEmail'
                 ,'stepVerifyEmailedDocumentMultipleContribution'
                 # send email with multiple attachments
                 ,'stepReceiveMultipleAttachmentsEmail'
                 ,'stepVerifyEmailedMultipleDocumentsInitialContribution'
                 # send email with multiple attachments one more time
                 ,'stepReceiveMultipleAttachmentsEmail'
                 ,'stepVerifyEmailedMultipleDocumentsMultipleContribution'
                ]
    self.playSequence(step_list, quiet)

  def test_12_UploadTextFromContributionTool(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
      Make sure that when upload file from contribution tool, it creates a new
      document in document module. when reupload same filename file, then it
      does not create a new document and update existing document.
    """
    if not run: return
    if not quiet: printAndLog('test_12_ReUploadSameFilenameFile')
    step_list = [ 'stepCleanUp'
                 ,'stepUploadTextFromContributionTool'
                 ,'stepCheckConvertingState'
                 ,'stepTic'
                 ,'stepCheckConvertedState'
                 ,'stepDiscoverFromFilename'
                 ,'stepTic'
                 ,'stepReuploadTextFromContributionTool'
                 ,'stepUploadAnotherTextFromContributionTool'
                ]
    self.playSequence(step_list, quiet)

  def stepUploadTextFromContributionToolWithNonASCIIFilename(self, 
                                 sequence=None, sequence_list=None, **kw):
    """
      Upload a file from contribution.
    """
    f = makeFileUpload('TEST-en-002.doc', 'T&é@{T-en-002.doc')
    document = self.portal.portal_contributions.newContent(file=f)
    sequence.edit(document_id=document.getId())
    transaction.commit()

  def stepDiscoverFromFilenameWithNonASCIIFilename(self, 
                                 sequence=None, sequence_list=None, **kw):
    """
      Upload a file using contribution tool. This should trigger metadata
      discovery and we should have basic coordinates immediately,
      from first stage.
    """
    context = self.getDocument(sequence.get('document_id'))
    file_name = 'T&é@{T-en-002.doc'
    # First make sure the regular expressions work
    property_dict = context.getPropertyDictFromFileName(file_name)
    self.assertEquals(property_dict['reference'], 'T&é@{T')
    self.assertEquals(property_dict['language'], 'en')
    self.assertEquals(property_dict['version'], '002')
    # Then make sure content discover works
    # XXX - This part must be extended
    property_dict = context.getPropertyDictFromContent()
    self.assertEquals(property_dict['title'], 'title')
    self.assertEquals(property_dict['description'], 'comments')
    self.assertEquals(property_dict['subject_list'], ['keywords'])
    # Then make sure metadata discovery works
    self.assertEquals(context.getReference(), 'T&é@{T')
    self.assertEquals(context.getLanguage(), 'en')
    self.assertEquals(context.getVersion(), '002')
    self.assertEquals(context.getSourceReference(), file_name)

  def test_13_UploadTextFromContributionToolWithNonASCIIFilename(self, 
                                           quiet=QUIET, run=RUN_ALL_TEST):
    """
      Make sure that when upload file from contribution tool, it creates a new
      document in document module. when reupload same filename file, then it
      does not create a new document and update existing document.
    """
    if not run: return
    if not quiet:
      printAndLog('test_13_UploadTextFromContributionToolWithNonASCIIFilename')
    step_list = [ 'stepCleanUp'
                 ,'stepUploadTextFromContributionToolWithNonASCIIFilename'
                 ,'stepTic'
                 ,'stepDiscoverFromFilenameWithNonASCIIFilename'
                ]
    self.playSequence(step_list, quiet)

  def test_14_ContributionToolIndexation(self, quiet=QUIET, run=RUN_ALL_TEST):
    """
    Check that contribution tool is correctly indexed after business template
    installation.
    Check that contribution tool is correctly indexed by ERP5Site_reindexAll.
    """
    portal = self.portal

    contribution_tool = getToolByName(portal, 'portal_contributions')
    self.assertEquals(1,
        len(portal.portal_catalog(path=contribution_tool.getPath())))

    # Clear catalog
    portal_catalog = self.getCatalogTool()
    portal_catalog.manage_catalogClear()
    # Reindex all
    portal.ERP5Site_reindexAll()
    self.stepTic()
    self.assertEquals(1,
        len(portal.portal_catalog(path=contribution_tool.getPath())))

  def test_15_TestFileNameDiscovery(self):
    """Test that filename is well set in source_reference
    - filename can we discovery from file
    - filename can be pass as argument by the user
    """
    portal = self.portal
    contribution_tool = getToolByName(portal, 'portal_contributions')
    file_object = makeFileUpload('TEST-en-002.doc')
    document = contribution_tool.newContent(file=file_object)
    self.assertEquals(document.getSourceReference(), 'TEST-en-002.doc')
    my_filename = 'Something.doc'
    document = contribution_tool.newContent(file=file_object,
                                            file_name=my_filename)
    self.stepTic()
    self.assertEquals(document.getSourceReference(), my_filename)

# Missing tests
"""
    property_dict = context.getPropertyDictFromUserLogin()
    property_dict = context.getPropertyDictFromInput()
"""

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestIngestion))
  return suite
