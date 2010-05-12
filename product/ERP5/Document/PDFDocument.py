# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2002-2006 Nexedi SARL and Contributors. All Rights Reserved.
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

import tempfile, os

from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName, _setCacheHeaders,\
    _ViewEmulator

from Products.ERP5Type import Permissions, PropertySheet
from Products.ERP5.Document.Image import Image
from Products.ERP5.Document.Document import ConversionError
from Products.ERP5.mixin.cached_convertable import CachedConvertableMixin

class PDFDocument(Image, CachedConvertableMixin):
  """
  PDFDocument is a subclass of Image which is able to
  extract text content from a PDF file either as text
  or as HTML.
  """
  # CMF Type Definition
  meta_type = 'ERP5 PDF Document'
  portal_type = 'PDF'

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

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

  searchable_property_list = ('asText', 'title', 'description', 'id', 'reference',
                              'version', 'short_title',
                              'subject', 'source_reference', 'source_project_title',)

  # Conversion API
  security.declareProtected(Permissions.AccessContentsInformation, 'convert')
  def convert(self, format, **kw):
    """
    Implementation of conversion for PDF files
    """
    if format == 'html':
      try:
        return self.getConversion(format=format)
      except KeyError:
        mime = 'text/html'
        data = self._convertToHTML()
        self.setConversion(data, mime=mime, format=format)
        return (mime, data)
    elif format in ('txt', 'text'):
      try:
        return self.getConversion(format='txt')
      except KeyError:
        mime = 'text/plain'
        data = self._convertToText()
        self.setConversion(data, mime=mime, format='txt')
        return (mime, data)
    else:
      return Image.convert(self, format, **kw)

  security.declareProtected(Permissions.ModifyPortalContent, 'populateContent')
  def populateContent(self):
    """
      Convert each page to an Image and populate the
      PDF directory with converted images. May be useful
      to provide online PDF reader
    """
    raise NotImplementedError

  security.declarePrivate('_convertToText')
  def _convertToText(self):
    """
      Convert the PDF text content to text with pdftotext
    """
    if not self.data:
      return ''
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(str(self.data))
    tmp.seek(0)
    cmd = 'pdftotext -layout -enc UTF-8 -nopgbrk %s -' % tmp.name
    r = os.popen(cmd)
    h = r.read()
    tmp.close()
    r.close()
    
    if h != '':
      return h
    else:
      # Try to use OCR
      # As high dpi images are required, it may take some times to convert the
      # pdf. 
      # It may be required to use activities to fill the cache and at the end, 
      # to calculate the final result
      text = ''
      content_information = self.getContentInformation()
      page_count = int(content_information.get('Pages', 0))
      try:
        # if the dimension is too big, rasterized image can be too
        # big. so we limit the maximum of rasterized image to 4096
        # pixles.
        # XXX since the dimention can be different on each page, it is
        # better to call 'pdfinfo -f page_num -l page_num' to get the
        # size of each page.
        max_size = 4096
        size = content_information.get('Page size',
                                       '%s x %s pts' % (max_size, max_size))
        width = int(size.split(' ')[0])
        height = int(size.split(' ')[2])
        resolution = 72.0 * max_size / max(width, height)
      except (ValueError, ZeroDivisionError):
        resolution = None
      for page_number in range(page_count):
        src_mimetype, png_data = self.convert(
            'png', quality=100, resolution=resolution,
            frame=page_number, display='identical')
        if not src_mimetype.endswith('png'):
          continue
        content = '%s' % png_data
        mime_type = getToolByName(self, 'mimetypes_registry').\
                                    lookupExtension('name.%s' % 'txt')
        if content is not None:
          portal_transforms = getToolByName(self, 'portal_transforms')
          result = portal_transforms.convertToData(mime_type, content,
                                                   context=self,
                                                   filename=self.getTitleOrId(),
                                                   mimetype=src_mimetype)
          if result is None:
            raise ConversionError('PDFDocument conversion error. '
                                  'portal_transforms failed to convert to %s: %r' % (mime_type, self))
          text += result
      return text

  security.declareProtected('View', 'getSizeFromImageDisplay')
  def getSizeFromImageDisplay(self, image_display):
    """
    Return the size for this image display, or None if this image display name
    is not known. If the preference is not set, (0, 0) is returned.
    """
    # identical parameter can be considered as a hack, in order not to
    # resize the image to prevent text distorsion when using OCR.
    # A cleaner API is required.
    if image_display == 'identical':
      return (self.getWidth(), self.getHeight())
    else:
      return Image.getSizeFromImageDisplay(self, image_display)

  security.declarePrivate('_convertToHTML')
  def _convertToHTML(self):
    """
    Convert the PDF text content to HTML with pdftohtml

    NOTE: XXX check that command exists and was executed
    successfully
    """
    if not self.data:
      return ''
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(str(self.data))
    tmp.seek(0)
    cmd = 'pdftohtml -enc UTF-8 -stdout -noframes -i %s' % tmp.name
    r = os.popen(cmd)
    h = r.read()
    tmp.close()
    r.close()
    h = h.replace('<BODY bgcolor="#A0A0A0"', '<BODY ') # Quick hack to remove bg color - XXX
    h = h.replace('href="%s.html' % tmp.name.split(os.sep)[-1], 'href="asEntireHTML') # Make links relative
    return h

  security.declareProtected(Permissions.AccessContentsInformation, 'getContentInformation')
  def getContentInformation(self):
    """
    Returns the information about the PDF document with
    pdfinfo.

    NOTE: XXX check that command exists and was executed
    successfully
    """
    try:
      return self._content_information.copy()
    except AttributeError:
      pass
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(str(self.data))
    tmp.seek(0)
    try:
      # First, we use pdfinfo to get standard metadata
      cmd = 'pdfinfo -meta -box %s' % tmp.name
      r = os.popen(cmd)
      h = r.read()
      r.close()
      result = {}
      for line in h.splitlines():
        item_list = line.split(':')
        key = item_list[0].strip()
        value = ':'.join(item_list[1:]).strip()
        result[key] = value

      # Then we use pdftk to get extra metadata
      cmd = 'pdftk %s dump_data output' % tmp.name
      r = os.popen(cmd)
      h = r.read()
      r.close()
      line_list = (line for line in h.splitlines())
      while True:
        try:
          line = line_list.next()
        except StopIteration:
          break
        if line.startswith('InfoKey'):
          key = line[len('InfoKey: '):]
          line = line_list.next()
          assert line.startswith('InfoValue: '),\
              "Wrong format returned by pdftk dump_data"
          value = line[len('InfoValue: '):]
          result.setdefault(key, value)
    finally:
      tmp.close()

    self._content_information = result
    return result.copy()

  def _setFile(self, data, precondition=None):
    try:
      del self._content_information
    except (AttributeError, KeyError):
      pass
    Image._setFile(self, data, precondition)
