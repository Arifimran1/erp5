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

source_project_uid_list = [x.uid for x in context.portal_catalog(\n
     relative_url=\'%s/%%\' % context.getRelativeUrl())] + [context.getUid()]\n
\n
from Products.ZSQLCatalog.SQLCatalog import Query\n
\n
sql_kw = {}\n
if kw.has_key(\'from_date\') and kw[\'from_date\'] is not None:\n
  query_kw = {\'delivery.start_date\' : kw[\'from_date\'],\n
              \'range\' : \'min\'}\n
  sql_kw[\'delivery.start_date\'] = Query(**query_kw)\n
if kw.has_key(\'at_date\') and kw[\'at_date\'] is not None:\n
  query_kw = {\'delivery.stop_date\' : kw[\'at_date\'],\n
              \'range\' : \'ngt\'}\n
  sql_kw[\'delivery.stop_date\'] = Query(**query_kw)\n
if kw.has_key(\'simulation_state\') and len(kw[\'simulation_state\']) > 0 :\n
  sql_kw[\'simulation_state\'] = kw[\'simulation_state\']\n
\n
task_list = [x.getObject() for x in \\\n
  context.portal_catalog(selection_report=selection_report, \n
          portal_type=\'Task\',\n
          source_project_uid = source_project_uid_list,\n
          **sql_kw)]\n
task_line_list = []\n
for task in task_list:\n
  task_line_list.extend(task.contentValues(portal_type=\'Task Line\'))\n
\n
def sortTaskLine(a, b):\n
  result = cmp(a.getStartDate(), b.getStartDate())\n
  if result == 0:\n
    result = cmp(a.getTitle(), b.getTitle())\n
  return result\n
\n
task_line_list.sort(sortTaskLine)\n
\n
return task_line_list\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>selection=None, selection_report=None, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Project_getSourceProjectRelatedTaskList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
