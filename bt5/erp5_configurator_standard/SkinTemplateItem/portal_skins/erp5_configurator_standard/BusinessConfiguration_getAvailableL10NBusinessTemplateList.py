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
            <value> <string>"""This script returns the list of available translation business templates.\n
\n
"""\n
\n
Base_translateString = context.Base_translateString\n
\n
return [\n
  dict(id=\'fr\',\n
       name=Base_translateString(\'French\'),\n
       bt5=\'erp5_l10n_fr\',),\n
  dict(id=\'de\',\n
       name=Base_translateString(\'German\'),\n
       bt5=\'erp5_l10n_de\',),\n
  dict(id=\'pl\',\n
       name=Base_translateString(\'Polish\'),\n
       bt5=\'erp5_l10n_pl_PL\',),\n
  dict(id=\'pt-BR\',\n
       name=Base_translateString(\'Portuguese / Brazil\'),\n
       bt5=\'erp5_l10n_pt-BR\',),\n
  dict(id=\'ko\',\n
       name=Base_translateString(\'Korean\'),\n
       bt5=\'erp5_l10n_ko\',),\n
  dict(id=\'ru\',\n
       name=Base_translateString(\'Russian\'),\n
       bt5=\'erp5_l10n_ru\',),\n
  dict(id=\'zh\',\n
       name=Base_translateString(\'Chinese\'),\n
       bt5=\'erp5_l10n_zh\',),\n
]\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>BusinessConfiguration_getAvailableL10NBusinessTemplateList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
