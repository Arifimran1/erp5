##############################################################################
#
# Copyright (c) 2002-2003 Nexedi SARL and Contributors. All Rights Reserved.
#                    Sebastien Robin <seb@nexedi.com>
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

from Acquisition import aq_base, aq_inner

from cStringIO import StringIO
from email.MIMEBase import MIMEBase
from email import Encoders
import pickle

from zLOG import LOG

def Base_asXML(object, ident=0):
  """
      Generate an xml text corresponding to the content of this object
  """
  self = object
  xml = ''
  if ident==0:
    xml += '<erp5>'
  LOG('asXML',0,'Working on: %s' % str(self.getPhysicalPath()))
  ident_string = '' # This is used in order to have the ident incremented
                    # for every sub-object
  for i in range(0,ident):
    ident_string += ' '
  xml += ident_string + '<object id=\"%s\" portal_type=\"%s\">\n' % \
                        (self.getId(),self.portal_type)

  # We have to find every property
  for prop_id in self.propertyIds():
    # In most case, we should not synchronize acquired properties
    prop = ''
    #if not prop.has_key('acquisition_base_category') \
    #   and prop['id'] != 'categories_list' and prop['id'] != 'uid':
    if prop_id not in ('uid','workflow_history'):
      prop_type = self.getPropertyType(prop_id)
      xml_prop_type = 'type="' + prop_type + '"'
      #try:
      value = self.getProperty(prop_id)
      #except AttributeError:
      #  value=None

      xml += ident_string + '  <%s %s>' %(prop_id,xml_prop_type)
      if value is None:
        pass
#       elif prop_type in ('image','file','document'):
#         LOG('asXML',0,'value: %s' % str(value))
#         # This property is binary and should be converted with mime
#         msg = MIMEBase('application','octet-stream')
#         msg.set_payload(value.getvalue())
#         Encoders.encode_base64(msg)
#         ascii_data = msg.get_payload()
#         ascii_data = ascii_data.replace('\n','@@@\n')
#         xml+=ascii_data
      elif prop_type in ('object',):
        # We may have very long lines, so we should split
        value = aq_base(value)
        value = pickle.dumps(value)
        msg = MIMEBase('application','octet-stream')
        msg.set_payload(value)
        Encoders.encode_base64(msg)
        ascii_data = msg.get_payload()
        ascii_data = ascii_data.replace('\n','@@@\n')
        xml+=ascii_data
      elif self.getPropertyType(prop_id) in ['lines','tokens']:
        i = 1
        for line in value:
          xml += '%s' % line
          if i<len(value):
            xml+='@@@' # XXX very bad hack, must find something better
          i += 1
      elif self.getPropertyType(prop_id) in ('text','string'):
        xml += str(value).replace('\n','@@@')
      else:
        xml+= str(value)
      xml += '</%s>\n' % prop_id

  # We have to describe the workflow history
  if hasattr(self,'workflow_history'):
    workflow_list = self.workflow_history
    workflow_list_keys = workflow_list.keys()
    workflow_list_keys.sort() # Make sure it is sorted

    for workflow_id in workflow_list_keys:
      #xml += ident_string + '    <workflow_history id=\"%s\">\n' % workflow_id
      for workflow_action in workflow_list[workflow_id]: # It is already sorted
        xml += ident_string + '      <workflow_action id=\"%s\">\n'  % workflow_id
        worfklow_variable_list = workflow_action.keys()
        worfklow_variable_list.sort()
        for workflow_variable in worfklow_variable_list: # Make sure it is sorted
          variable_type = "string" # Somewhat bad, should find a better way
          if workflow_variable.find('time')>= 0:
            variable_type = "date"
          xml += ident_string + '        <%s type=\"%s\">%s' % (workflow_variable,
                              variable_type,workflow_action[workflow_variable])
          xml += '</%s>\n' % workflow_variable
        xml += ident_string + '      </workflow_action>\n'
      #xml += ident_string + '    </workflow_history>\n'
    #xml += ident_string + '  </workflow_history>\n'

  # We should not describe security settings
  for user_role in self.get_local_roles():
    xml += ident_string + '  <local_role>%s' % user_role[0]
    for role in user_role[1]:
      xml += '@@@'
      xml += '%s' % role
    xml += '</local_role>\n'

  # We have finished to generate the xml
  xml += ident_string + '</object>\n'
  if ident==0:
    xml += '</erp5>'
  # Now convert the string as unicode
  if type(xml) is type(u"a"):
    xml_unicode = xml
  else:
    xml_unicode = unicode(xml,encoding='iso-8859-1')
  return xml_unicode.encode('utf-8')

def Folder_asXML(object, ident=0):
  """
      Generate an xml text corresponding to the content of this object
  """
  self = object
  xml = ''
  xml += Base_asXML(self, ident=ident)
  xml = xml[:xml.rfind('</object>')]
  # Make sure the list of sub objects is ordered
  object_value_list = list(self.objectValues())
  object_value_list.sort(lambda x, y: cmp(x.getId(), y.getId()))
  # Append to the xml the xml of subobjects
  for o in object_value_list:
    aq_ob = aq_base(o)
    if hasattr(aq_ob, 'asXML'):
      o_xml = o.asXML(ident=ident+2)
      if type(o_xml) is type('a'):
        xml += o_xml
  xml += '</object>\n'
  if ident==0:
    xml += '</erp5>'
  return xml
