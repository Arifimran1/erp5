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
            <value> <string>from DateTime import DateTime\n
form = context.REQUEST.form\n
\n
# find project by title\n
test_suite = form.get(\'test_suite\', None)\n
project = context.ERP5Site_getProjectFromTestSuite(test_suite)\n
\n
# create test result object\n
# test_report = context.newContent( # Dangerous\n
test_report = context.getPortalObject().test_result_module.newContent(\n
  id=form.get(\'test_report_id\'),\n
  portal_type=\'Test Result\',\n
  title=test_suite,\n
  string_index=form.get(\'result\'),\n
  source_project_value=project)\n
\n
# update security\n
test_report.updateLocalRolesOnSecurityGroups()\n
\n
test_report.start(date=DateTime(form.get(\'launch_date\')))\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
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
            <value> <string>TestResultModule_reportRunning</string> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string>Called at test startup</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
