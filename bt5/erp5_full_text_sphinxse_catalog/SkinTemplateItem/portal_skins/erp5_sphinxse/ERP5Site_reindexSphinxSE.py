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
            <value> <string>portal_catalog = context.portal_catalog\n
sql_catalog = portal_catalog.getSQLCatalog(sql_catalog_id)\n
\n
LIMIT = 100\n
\n
i = 0\n
while True:\n
  full_text_list = portal_catalog(limit=(i*LIMIT, LIMIT))\n
  if len(full_text_list) == 0:\n
    break\n
  sql_catalog.SQLCatalog_deferFullTextIndex(getPath=[x.path for x in full_text_list])\n
  i += 1\n
return \'SphinxSE index will be updated in background.\'\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>sql_catalog_id=None</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>ERP5Site_reindexSphinxSE</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
