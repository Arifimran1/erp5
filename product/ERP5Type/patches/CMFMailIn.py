##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
# Copyright (c) 2006 Nexedi SARL and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

import mimetypes
import email
from email.Header import decode_header
from email.Utils import parseaddr

import traceback
import StringIO

from Products.CMFMailIn.MailIn_Tool import MailInTool

# Add new method on MailInTool
def MailInTool_postUTF8MailMessage(self, file=None):
  """
  Recode the email in UTF-8 in order to import it 
  in ERP5.
  """
  if not file:
      raise IOError, 'No Mail Message Supplied'
  # Prepare result
  theMail = {
    'attachment_list': [],
    'body': '',
    # Place all the email header in the headers dictionary in theMail
    'headers': {}
  }
  # Get Message
  msg = email.message_from_string(file)
  # Bake up original file
  theMail['__original__'] = file
  # Recode headers to UTF-8 if needed
  for key, value in msg.items():
    decoded_value_list = decode_header(value)
    new_value_list = []
    for x in decoded_value_list:
      if x[1] != None:
        new_value_list.append(unicode(x[0], x[1]).encode('utf-8'))
      else:
        new_value_list.append(x[0])
    new_value = ''.join(new_value_list)
#           msg.replace_header(key, new_value)
    theMail['headers'][key.lower()] = new_value
  # Filter mail
  for header in ('to', 'from'):
    theMail['headers'][header] = parseaddr(theMail['headers'][header])[1]
  # Get attachment
  body_found = 0
  for part in msg.walk():
    content_type = part.get_content_type()
    file_name = part.get_filename()
    # multipart/* are just containers
    # XXX Check if data is None ?
    if content_type.startswith('multipart'):
      continue
    elif content_type == 'message/rfc822':
      continue
    elif content_type == "text/plain":
      charset = part.get_content_charset()
      payload = part.get_payload(decode=True)
      payload = unicode(payload, charset).encode('utf-8')
      if body_found:
        # Keep the content type
        theMail['attachment_list'].append((file_name, 
                                           content_type, payload))
      else:
        theMail['body'] = payload
        body_found = 1
    else:
      payload = part.get_payload(decode=True)
      # Keep the content type
      theMail['attachment_list'].append((file_name, content_type, 
                                         payload))
  try:
    portal_url = self.portal_url.getPortalPath()
    if portal_url[-1]!='/': portal_url=portal_url+'/'
  except:
    portal_url = ''
      
  if self.method:
    try:
      return self.restrictedTraverse(portal_url+self.method)\
                                                    (theMail=theMail)
    except:
      # Generate log message
      fp = StringIO.StringIO()
      traceback.print_exc(file=fp)
      log_message = fp.getvalue()
      LOG("GeneratorTool, next", 1000, 
          log_message)
      return "Message rejected."
  
  self.REQUEST.RESPONSE.notFoundError('MailIn method not specified')

MailInTool.postUTF8MailMessage = MailInTool_postUTF8MailMessage
