<?xml version="1.0"?>
<ZopeData>
  <record id="1" aka="AAAAAAAAAAE=">
    <pickle>
      <global name="PythonScript" module="Products.PythonScripts.PythonScript"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>Script_magic</string> </key>
            <value> <int>3</int> </value>
        </item>
        <item>
            <key> <string>_bind_names</string> </key>
            <value>
              <object>
                <klass>
                  <global name="NameAssignments" module="Shared.DC.Scripts.Bindings"/>
                </klass>
                <tuple/>
                <state>
                  <dictionary>
                    <item>
                        <key> <string>_asgns</string> </key>
                        <value>
                          <dictionary>
                            <item>
                                <key> <string>name_container</string> </key>
                                <value> <string>container</string> </value>
                            </item>
                            <item>
                                <key> <string>name_context</string> </key>
                                <value> <string>context</string> </value>
                            </item>
                            <item>
                                <key> <string>name_m_self</string> </key>
                                <value> <string>script</string> </value>
                            </item>
                            <item>
                                <key> <string>name_subpath</string> </key>
                                <value> <string>traverse_subpath</string> </value>
                            </item>
                          </dictionary>
                        </value>
                    </item>
                  </dictionary>
                </state>
              </object>
            </value>
        </item>
        <item>
            <key> <string>_body</string> </key>
            <value> <string encoding="cdata"><![CDATA[

"""\n
This script tries to send a message containing the credentials to the\n
organisation. It uses portal_notifications and the getObject API of ERP5Catalog.\n
"""\n
from Products.DCWorkflow.DCWorkflow import ValidationFailed\n
\n
\n
translateString = context.Base_translateString\n
portal_catalog = context.portal_catalog\n
vat_code = context.getVatCode()\n
\n
# get the new organisation :\n
result = portal_catalog(portal_type=\'Organisation\',\n
    vat_code=vat_code)\n
\n
if len(result) > 1:\n
  msg = "Error : There is more than one company with the NINEA code ${code}"\n
  msg = translateString(msg, mapping=dict(code=vat_code))\n
  raise ValidationFailed, msg \n
\n
if len(result) == 0:\n
  msg = "No organisation with the NINEA code ${code}"\n
  msg = translateString(msg, mapping=dict(code=vat_code))\n
  raise ValidationFailed, msg \n
\n
organisation = result[0]\n
\n
# Build the message and translate it\n
subject = translateString("Your credential for ${site_address}", mapping=dict(site_address=\'www.erp5.org\'))\n
msg = """Thanks for registrering to ERP5. Now you can connect in on ${site_address} with this credentials : \n
\n
Login : ${login}\n
Password : ${password}\n
\n
This credentials are usefull to track your application and more. Please visit ${site_address} for more information.\n
"""\n
msg = translateString(msg,\n
             mapping=dict(site_address=\'www.erp5.org\',\n
                          login=organisation.getReference(),\n
                          password=organisation.getPassword())\n
            )\n
\n
# We can now notify the owner through the notification tool\n
context.portal_notifications.sendMessage(recipient=organisation.getReference(), \n
    subject=subject, message=msg, portal_type_list=(\'Person\', \'Organisation\'),\n
    store_as_event=True)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>_proxy_roles</string> </key>
            <value>
              <tuple>
                <string>Assignor</string>
                <string>Manager</string>
              </tuple>
            </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Organisation_sendCrendentialsByEMail</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
