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

portal_templates = context.getPortalObject().portal_templates\n
delete_list = []\n
bt_list = portal_templates.objectValues()\n
for bt in bt_list:\n
  bt_id = bt.getId()\n
  installation_state = bt.getInstallationState()\n
  if installation_state in (\'deleted\', \'replaced\'):\n
    delete_list.append(bt_id)\n
  elif installation_state == \'not_installed\':\n
    title = bt.getTitle()\n
    modification_date = bt.getModificationDate()\n
    for x in bt_list:\n
      if (x.getTitle() == title and\n
          x.getInstallationState() in (\'installed\', \'not_installed\') and\n
          x.getModificationDate() > modification_date):\n
        delete_list.append(bt_id)\n
        break\n
\n
print \'Deleted id list:%r\' % delete_list\n
portal_templates.manage_delObjects(delete_list)\n
return printed\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>TemplateTool_deleteObsoleteTemplateList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
