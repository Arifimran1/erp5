# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Nexedi SA and Contributors. All Rights Reserved.
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

import mimetypes

from AccessControl import ClassSecurityInfo
from Products.ERP5Type.Base import WorkflowMethod
from Products.ERP5Type import Permissions, PropertySheet
from Products.ERP5.Document.Document import Document, VALID_TEXT_FORMAT_LIST
from Products.ERP5.Document.Document import ConversionError
from Products.ERP5Type.Base import Base, removeIContentishInterface
from Products.CMFDefault.File import File as CMFFile
from OFS.Image import Pdata
import cStringIO

# Mixin Import
from Products.ERP5.mixin.cached_convertable import CachedConvertableMixin

mimetypes.init()

def _unpackData(data):
  """
  Unpack Pdata into string
  OBSOLETED. use str(data) instead, because Pdata.__str__ is defined.
  """
  return str(data)

class File(Document, CMFFile):
  """
      A File can contain raw data which can be uploaded and downloaded.
      It is the root class of Image, OOoDocument (ERP5OOo product),
      etc. The main purpose of the File class is to handle efficiently
      large files. It uses Pdata from OFS.File for this purpose.

      File inherits from XMLObject and can be synchronized
      accross multiple sites.

      Subcontent: File can only contain role information.

      TODO:
      * make sure ZODB BLOBS are supported to prevent
       feeding the ZODB cache with unnecessary large data
  """

  meta_type = 'ERP5 File'
  portal_type = 'File'
  add_permission = Permissions.AddPortalContent

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Default global values
  content_type = '' # Required for WebDAV support (default value)
  data = '' # A hack required to use OFS.Image.index_html without calling OFS.Image.__init__

  # Default Properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.CategoryCore
                    , PropertySheet.DublinCore
                    , PropertySheet.Version
                    , PropertySheet.Reference
                    , PropertySheet.Document
                    , PropertySheet.Data
                    , PropertySheet.ExternalDocument
                    , PropertySheet.Url
                    , PropertySheet.Periodicity
    )

  ### Special edit method
  security.declarePrivate( '_edit' )
  def _edit(self, **kw):
    """
      This is used to edit files
    """
    if kw.has_key('file'):
      file = kw.get('file')
      precondition = kw.get('precondition')
      filename = getattr(file, 'filename', None)
      # if file field is empty(no file is uploaded),
      # filename is empty string.
      if filename:
        self._setSourceReference(filename)
      if self._isNotEmpty(file):
        self._setFile(file, precondition=precondition)
      del kw['file']
    Base._edit(self, **kw)

  security.declareProtected( Permissions.ModifyPortalContent, 'edit' )
  edit = WorkflowMethod( _edit )

  def get_size(self):
    """
    has to be overwritten here, otherwise WebDAV fails
    """
    return self.getSize()

  getcontentlength = get_size

  def _setFile(self, data, precondition=None):
    CMFFile._edit(self, precondition=precondition, file=data)

  security.declareProtected(Permissions.ModifyPortalContent,'setFile')
  def setFile(self, data, precondition=None):
    self._setFile(data, precondition=precondition)
    self.reindexObject()

  security.declareProtected(Permissions.AccessContentsInformation, 'hasFile')
  def hasFile(self):
    """
    Checks whether a file was uploaded into the document.
    """
    return self.hasData()

  security.declareProtected(Permissions.AccessContentsInformation, 'hasBaseData')
  def hasBaseData(self):
    """
      By default, a File instance does not require conversion
      to a base format. Therefore, hasBaseData must be overriden.
    """
    return self.hasData()

  security.declareProtected(Permissions.ModifyPortalContent, 'guessMimeType')
  def guessMimeType(self, fname=''):
    """
      get mime type from file name
    """
    if fname == '': fname = self.getSourceReference()
    if fname:
      content_type,enc = mimetypes.guess_type(fname)
      if content_type is not None:
        self.setContentType(content_type)
    else:
      content_type = None
    return content_type

  security.declareProtected(Permissions.ModifyPortalContent, '_setData')
  def _setData(self, data):
    """
    """
    size = None
    # update_data use len(data) when size is None, which breaks this method.
    # define size = 0 will prevent len be use and keep the consistency of 
    # getData() and setData()
    if data is None:
      size = 0
    if not isinstance(data, Pdata) and data is not None:
      file = cStringIO.StringIO(data)
      data, size = self._read_data(file)
    if getattr(self, 'update_data', None) is not None:
      # We call this method to make sure size is set and caches reset
      self.update_data(data, size=size)
    else:
      self._baseSetData(data) # XXX - It would be better to always use this accessor
      self._setSize(size)
      self.ZCacheable_invalidate()
      self.ZCacheable_set(None)
      self.http__refreshEtag()

  security.declareProtected(Permissions.AccessContentsInformation, 'getData')
  def getData(self, default=None):
    """return Data as str."""
    data = self._baseGetData()
    if data is None:
      return None
    else:
      return str(data)

  security.declareProtected(Permissions.ModifyPortalContent,'PUT')
  def PUT(self, REQUEST, RESPONSE):
    CMFFile.PUT(self, REQUEST, RESPONSE)

  # DAV Support
  index_html = CMFFile.index_html 
  PUT = CMFFile.PUT
  security.declareProtected('FTP access', 'manage_FTPget', 'manage_FTPstat', 'manage_FTPlist')
  manage_FTPget = CMFFile.manage_FTPget
  manage_FTPlist = CMFFile.manage_FTPlist
  manage_FTPstat = CMFFile.manage_FTPstat

  security.declareProtected(Permissions.AccessContentsInformation, 'getMimeTypeAndContent')
  def getMimeTypeAndContent(self):
    """This method returns a tuple which contains mimetype and content."""
    from Products.ERP5.Document.EmailDocument import MimeTypeException
    # return a tuple (mime_type, data)
    mime_type = None
    content = None

    # WARNING - this could fail since getContentType
    # is not (yet) part of Document API
    if getattr(self, 'getContentType', None) is not None:
      mime_type = self.getContentType()
    elif getattr(self, 'getTextFormat', None) is not None:
      mime_type = self.getTextFormat()
    else:
      raise ValueError, "Cannot find mimetype of the document."

    if mime_type is not None:
      try:
        mime_type, content = self.convert(mime_type)
      except ConversionError:
        mime_type = self.getBaseContentType()
        content = self.getBaseData()
      except (NotImplementedError, MimeTypeException):
        pass

    if content is None:
      if getattr(self, 'getTextContent', None) is not None:
        content = self.getTextContent()
      elif getattr(self, 'getData', None) is not None:
        content = self.getData()
      elif getattr(self, 'getBaseData', None) is not None:
        content = self.getBaseData()

    if content and not isinstance(content, str):
      content = str(content)

    return (mime_type, content)

  security.declareProtected(Permissions.AccessContentsInformation, 'convert')
  def convert(self, format, **kw):
    """According content_type of data we can proceed some Conversions.
    The idea is to wrap data into TempDocument who support conversion
    then return conversion from this temporary document.

    mimetype                             Class of temp document

    text/????                            newTempTextDocument
    image/????                           newTempImage
    application/pdf                      newTempPDFDocument
    [ooo supported content_type list]    newTempOOoDocument
    unknown                              no conversion supported

    XXX Another idea of implementation from JPS: Changing dynamicaly the Class
    of persistent_object.
    for example any instance of File portal_type can follow TextDocument API
    if content_type is 'text/html' and support conversion features of
    TextDocument.
    """
    content_type = self.getContentType()

    # Build the list of acceptable content_type for OOoDocument
    # Hopefully this is cached
    from Products.ERP5Type.Document import newTempOOoDocument
    temp_odt = newTempOOoDocument(self, 'testOOoOdt')
    temp_odt.edit(base_content_type='application/vnd.oasis.opendocument.text',
                  base_data='not empty')
    temp_ods = newTempOOoDocument(self, 'testOOoOds')
    temp_ods.edit(
            base_content_type='application/vnd.oasis.opendocument.spreadsheet',
            base_data='not empty')
    temp_odg = newTempOOoDocument(self, 'testOOoOdg')
    temp_odg.edit(base_content_type='application/vnd.oasis.opendocument.draw',
                  base_data='not empty')
    temp_odb = newTempOOoDocument(self, 'testOOoOdb')
    temp_odb.edit(base_content_type='application/vnd.oasis.opendocument.base',
                  base_data='not empty')

    supported_ooo_content_type_list = [item[0] for item in\
                                           temp_odt.getTargetFormatItemList()]\
                    + [item[0] for item in temp_ods.getTargetFormatItemList()]\
                    + [item[0] for item in temp_odg.getTargetFormatItemList()]\
                    + [item[0] for item in temp_odb.getTargetFormatItemList()]
    if content_type.startswith('text'):
      # We can wrap it into TextDocument
      from Products.ERP5Type.Document import newTempTextDocument
      temp_document = newTempTextDocument(self, 'temp_%s' % self.getId(),
                                          text_content=self.getData(),
                                          content_type=content_type)
      return temp_document.convert(format=format, **kw)
    elif content_type.startswith('image'):
      # We can wrap it into Image
      from Products.ERP5Type.Document import newTempImage
      temp_document = newTempImage(self, 'temp_%s' % self.getId(),
                                   data=self.getData(),
                                   content_type=content_type)
      return temp_document.convert(format=format, **kw)
    elif content_type == 'application/pdf':
      # We can wrap it into PDFDocument
      from Products.ERP5Type.Document import newTempPDFDocument
      temp_document = newTempPDFDocument(self, 'temp_%s' % self.getId(),
                                         data=self.getData(),
                                         content_type=content_type)
      return temp_document.convert(format=format, **kw)
    elif content_type in supported_ooo_content_type_list:
      # We can wrap it into OOoDocument
      temp_document = newTempOOoDocument(self, 'temp_%s' % self.getId(),
                                         text_content=self.getData(),
                                         content_type=content_type)
      return temp_document.convert(format=format, **kw)
    else:
      # We didn't find suitable wrapper to convert this File
      if format in VALID_TEXT_FORMAT_LIST:
        # This is acceptable to return empty string
        # for a File we can not convert
        return 'text/plain', ''
      elif format is None:
        # No conversion is asked,
        # we can return safely the file content itself
        return content_type, self.getData()
      raise NotImplementedError

# CMFFile also brings the IContentishInterface on CMF 2.2, remove it.
removeIContentishInterface(File)

