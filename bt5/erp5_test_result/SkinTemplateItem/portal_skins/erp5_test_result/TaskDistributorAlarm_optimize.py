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

from Products.ZSQLCatalog.SQLCatalog import Query\n
from DateTime import DateTime\n
now = DateTime()\n
#Clean-up invalidated Test Nodes and\n
# invalidate inactive ones \n
list_node = context.portal_catalog(\n
       portal_type="Test Node",\n
       )\n
old_date = now-1.0/24*11\n
for test_node in list_node:\n
  test_node = test_node.getObject()\n
  ping_date = test_node.getPingDate()\n
  validation_state = test_node.getValidationState()\n
  if validation_state == \'validated\':\n
    if ping_date is not None:\n
      if ping_date <= old_date:\n
        test_node.invalidate()\n
  elif validation_state == \'invalidated\':\n
    if test_node.getSpecialise():\n
      test_node.getSpecialiseValue().cleanupInvalidatedTestNode(test_node)\n
\n
portal = context.getPortalObject()\n
\n
distributor_list = portal.portal_task_distribution.objectValues()\n
for distributor in distributor_list: \n
  distributor.activate().optimizeConfiguration()\n
return list_node\n


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
                <string>Manager</string>
              </tuple>
            </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>TaskDistributorAlarm_optimize</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
