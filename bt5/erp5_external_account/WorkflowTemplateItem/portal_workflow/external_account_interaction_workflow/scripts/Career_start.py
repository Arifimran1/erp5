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
            <value> <string>"""\n
  Create respective accounts for a company employee.\n
"""\n
portal = context.getPortalObject()\n
\n
career = state_change[\'object\']\n
person = career.getParentValue()\n
\n
default_email_text = person.Person_getDefaultExternalEmailText()\n
username, domain = default_email_text.split(\'@\', 2)\n
if domain in portal.portal_preferences.getPreferredManagedExternalDomainNameList():\n
  # find (or create an external Email Account instance)\n
  kw = {\'email.url_string\':default_email_text,\n
        \'default_source_uid\': person.getUid(),\n
        \'validation_state\': \'validated\',\n
        \'portal_type\': "Email Account"}\n
  email_account = portal.portal_catalog.getResultValue(**kw)\n
  if email_account is None:\n
    # might be invalidate temporary\n
    kw[\'validation_state\'] = \'invalidated\'\n
    email_account = portal.portal_catalog.getResultValue(**kw)\n
    if email_account is not None:\n
      email_account.validate()\n
    else:\n
      # no external account at all so create it\n
      email_account = portal.external_account_module.newContent(\n
                                                       portal_type = "Email Account",\n
                                                       url_string = default_email_text,\n
                                                       source_value = person)\n
      email_account.validate()\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>state_change</string> </value>
        </item>
        <item>
            <key> <string>_proxy_roles</string> </key>
            <value>
              <tuple>
                <string>Manager</string>
                <string>Owner</string>
              </tuple>
            </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Career_start</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
