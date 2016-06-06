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
 This script is part of ERP5 Web\n
\n
 ERP5 Web is a business template of ERP5 which provides a way\n
 to create web sites which can display selected\n
 ERP5 contents through multiple custom web layouts.\n
\n
 This script returns a list of document values (ie. objects or brains)\n
 which are considered as part of this section. It can be\n
 a list of web pages (usual case), a list of products\n
 (online catalog), a list of tenders (e-government), etc.\n
\n
 The default implementation provided here consists in\n
 listing documents which meet the predicate defined\n
 by the section (ex. which are part of a given publication_section)\n
 and which are in "published" state and of a "Web Page" portal_type.\n
\n
 It should be noted that document selection should be implemented\n
 as much as possible using the Domain API.\n
\n
 This script can be changed to meet other requirements. For example\n
 one may want to display a list of products in a section. In this case,\n
 this script must return a list of documents of type "Product"\n
 with a "validated" state and in the appropriate product family.\n
\n
 This script is intended to be overriden by creating a new script\n
 within the Web Section or Web Site instance. It can be also\n
 customised per portal type within portal_skins. Customisation\n
 thourgh local scripts is recommended to host multiple sites\n
 on the same ERP5Site instance.\n
\n
 The API uses **kw so that it is possible to extend the behaviour of\n
 the default script with advanced features (ex. group by reference,\n
 by version, only select a specific publication state, etc.).\n
\n
 Here are some suggestions which can either be implemented using\n
 SQL (group_by, order_by) or using additional python scripting\n
 if this is compatible with data size.\n
\n
 SUGGESTIONS:\n
\n
 - Prevent showing duplicate references\n
 \n
 - Add documents associated to this section through \'aggregate\'.\n
\n
 - Display only the latest version and the appropriate language.\n
"""\n
portal_catalog = container.portal_catalog\n
\n
# First find the Web Section or Web Site we belong to\n
current_section = context.getWebSectionValue()\n
\n
# Build the list of parameters\n
if not kw.has_key(\'validation_state\'):\n
  kw[\'validation_state\'] = [\'draft\', \'submitted\', \'shared\',\n
                            \'released\', \'published\', \'restricted\']\n
if not kw.has_key(\'sort_on\'):\n
  kw[\'sort_on\'] = [(\'int_index\', \'descending\')]\n
if not kw.has_key(\'group_by\'):\n
  kw[\'group_by\'] = (\'reference\',)\n
\n
# Remove sort on validation and groupd_by\n
kw.pop(\'validation_state\')\n
kw.pop(\'group_by\')\n
\n
# Return the list of matching documents for the given states\n
return current_section.searchResults(**kw)\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>**kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>WebSection_getDocumentValueList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
