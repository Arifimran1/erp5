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
            <value> <string>def checkTopLevel():\n
  portal = context.getPortalObject()\n
  for o in portal.objectValues():\n
    error_list = o.checkFolderHandler(fixit=fixit)\n
    if len(error_list):\n
      portal.portal_activities.activate(active_process=active_process, priority=2) \\\n
      .Base_makeActiveResult(title=o.absolute_url_path(), error_list=error_list)\n
\n
if \'tag\' not in kwargs:\n
  kwargs[\'tag\'] = []\n
\n
kwargs.update(\n
    method_id=\'checkFolderHandler\',\n
    method_kw={\'fixit\': fixit},\n
)\n
\n
if context.getPortalType() == \'Alarm\':\n
  active_process = context.newActiveProcess().getPath()\n
  ERP5Site_checkDataWithScript = context.ERP5Site_checkDataWithScript\n
else:\n
  active_process = context.portal_activities.newActiveProcess().getPath()\n
  ERP5Site_checkDataWithScript = context.portal_activities.ERP5Site_checkDataWithScript\n
  print \'Results will be saved to %s\' % active_process\n
\n
checkTopLevel()\n
ERP5Site_checkDataWithScript(\n
  active_process=active_process,\n
  *args,\n
  **kwargs)\n
\n
return printed\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>fixit=0, *args, **kwargs</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>ERP5Site_checkFolderHandler</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
