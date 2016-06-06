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

topmost_url_document = context.Base_getURLTopmostDocumentValue()\n
if not topmost_url_document.isURLAncestorOf(cancel_url):\n
  return context.ERP5Site_redirect(topmost_url_document.absolute_url(),\n
    keep_items={\'portal_status_message\': \'Redirection to an external site prevented.\'},\n
    **kw)\n
\n
if \'?selection_name=\' in cancel_url or \'&selection_name=\' in cancel_url:\n
  # if selection_name is already present in the cancel URL, we do not\n
  # use erp5_xhtml_style script that would add it again.\n
  return context.REQUEST.RESPONSE.redirect(cancel_url)\n
return context.ERP5Site_redirect(cancel_url, **kw)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>cancel_url, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Base_cancel</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
