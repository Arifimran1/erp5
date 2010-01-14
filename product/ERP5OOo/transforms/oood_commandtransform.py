# -*- coding: utf-8 -*-
from Products.PortalTransforms.libtransforms.commandtransform import commandtransform
from Products.PortalTransforms.interfaces import idatastream
from Products.ERP5Type.Document import newTempOOoDocument
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base
from zope.interface import implements
from OFS.Image import Image as OFSImage
from zLOG import LOG

try:
  from Products.ERP5OOo.OOoUtils import OOoBuilder
  import re
  from lxml import etree
  from lxml.etree import ParseError, Element
  import_succeed = 1
except ImportError:
  import_succeed = 0
from urllib import unquote
from urlparse import urlparse
try:
  # Python >= 2.6
  from urlparse import parse_qsl
except ImportError:
  from cgi import parse_qsl

CLEAN_RELATIVE_PATH = re.compile('^../')

class TransformError(Exception):
  pass

class OOoDocumentDataStream:
  """Handle OOoDocument in Portal Transforms"""
  implements(idatastream)

  def setData(self, value):
    """set the main"""
    self.value = value

  def getData(self):
    return self.value

  def setSubObjects(self, objects):
    pass

  def getSubObjects(self):
    return {}

  def getMetadata(self):
    """return a dict-like object with any optional metadata from
    the transform
    You can modify the returned dictionnary to add/change metadata
    """
    return {}

  def isCacheable(self):
    """
     True by Default
    """
    return getattr(self, '_is_cacheable', True)

  def setCachable(self, value):
    self._is_cacheable = value

class OOOdCommandTransform(commandtransform):
  """Transformer using oood"""

  def __init__(self, context, name, data, mimetype):
    commandtransform.__init__(self, name)
    if name:
      self.__name__ = name
    self.mimetype = mimetype
    self.context = context
    if import_succeed and self.mimetype == 'text/html':
      data = self.includeExternalCssList(data)
    self.data = data

  def name(self):
    return self.__name__

  def includeImageList(self, data):
    """Include Images in ODF archive

    - data: zipped archive content
    """
    builder = OOoBuilder(data)
    content = builder.extract('content.xml')
    xml_doc = etree.XML(content)
    image_tag_list = xml_doc.xpath('//*[name() = "draw:image"]')
    SVG_NAMESPACE = 'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0'
    XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
    ratio_px_cm = 2.54 / 100.
    # Flag to enable modification of OOoBuilder
    odt_content_modified = False
    for image_tag in image_tag_list:
      frame = image_tag.getparent()
      #Try to get image file from ZODB
      href_attribute_list = image_tag.xpath('.//@*[name() = "xlink:href"]')
      url = href_attribute_list[0]
      parse_result = urlparse(unquote(url))
      # urlparse return a 6-tuple: scheme, netloc, path, params, query, fragment
      path = parse_result[2]
      if path:
        # OOo corrupt relative Links inside HTML content during odt conversion
        # <img src="REF.TO.IMAGE" ... /> become <draw:image xlink:href="../REF.TO.IMAGE" ... />
        # So remove "../" added by OOo
        path = CLEAN_RELATIVE_PATH.sub('', path)
        # retrieve http parameters and use them to convert image
        query_parameter_string = parse_result[4]
        image_parameter_dict = dict(parse_qsl(query_parameter_string))
        try:
          image = self.context.restrictedTraverse(path)
        except (AttributeError, KeyError):
          #Image not found, this image is probably not hosted by ZODB. Do nothing
          image = None
        if image is not None:
          odt_content_modified = True
          content_type = image.getContentType()
          mimetype_list = getToolByName(self.context,
                                        'mimetypes_registry').lookup(content_type)
          #Need to improve default format handling
          format = 'png'
          if mimetype_list:
            format = mimetype_list[0].minor()
          if getattr(image, 'meta_type', None) == 'ERP5 Image':
            #ERP5 API
            if 'format' in image_parameter_dict:
              format = image_parameter_dict.pop('format')

            # convert image according parameters
            mime, image_data = image.convert(format, **image_parameter_dict)
            image = OFSImage(image.getId(), image.getTitle(), image_data)

          # image should be OFSImage
          data = image.data
          width = image.width
          height = image.height
          if height:
            frame.attrib.update({'{%s}height' % SVG_NAMESPACE: '%.3fcm' % (height * ratio_px_cm)})
          if width:
            frame.attrib.update({'{%s}width' % SVG_NAMESPACE: '%.3fcm' % (width * ratio_px_cm)})
          new_path = builder.addImage(data, format=format)
          image_tag.attrib.update({'{%s}href' % XLINK_NAMESPACE: new_path})
    if odt_content_modified:
      builder.replace('content.xml', etree.tostring(xml_doc, encoding='utf-8',
                                                    xml_declaration=True,
                                                    pretty_print=False))
    return builder.render()

  def includeExternalCssList(self, data):
    """Replace external Css link by style Element,
    to avoid ooo querying portal without crendentials through http.

    - data: html content
    """
    try:
      xml_doc = etree.XML(data)
    except ParseError:
      #If not valid xhtml do nothing
      return data
    xpath = '//*[local-name() = "link"][@type = "text/css"]'
    css_link_tag_list = xml_doc.xpath(xpath)
    for css_link_tag in css_link_tag_list:
      #Try to get css from ZODB
      href_attribute_list = css_link_tag.xpath('.//@href')
      url = href_attribute_list[0]
      parse_result = urlparse(unquote(url))
      # urlparse return a 6-tuple: scheme, netloc, path, params, query, fragment
      path = parse_result[2]
      if path:
        try:
          css_object = self.context.restrictedTraverse(path)
        except (AttributeError, KeyError):
          #Image not found, this image is probably not hosted by ZODB. Do nothing
          css_object = None
        if css_object is not None:
          if callable(aq_base(css_object)):
            #In case of DTMLDocument
            css_as_text = css_object(client=self.context.getPortalObject())
          else:
            #Other cases like files
            css_as_text = str(css_object)
          parent_node = css_link_tag.getparent()
          style_node = Element('style')
          style_node.text = css_as_text
          parent_node.append(style_node)
          style_node.attrib.update({'type': 'text/css'})
          parent_node.remove(css_link_tag)
    return etree.tostring(xml_doc, encoding='utf-8',
                          xml_declaration=False, pretty_print=False, )

  def convert(self):
    tmp_ooo = newTempOOoDocument(self.context, self.context.generateNewId())
    tmp_ooo.edit( base_data=self.data,
                  fname=self.name(),
                  source_reference=self.name(),
                  base_content_type=self.mimetype,)
    tmp_ooo.oo_data = self.data
    self.ooo = tmp_ooo

  def convertTo(self, format):
    if self.ooo.isTargetFormatAllowed(format):
      mime, data = self.ooo.convert(format)
      if import_succeed and self.mimetype == 'text/html':
        data = self.includeImageList(data)
      return data
    else:
      raise TransformError
