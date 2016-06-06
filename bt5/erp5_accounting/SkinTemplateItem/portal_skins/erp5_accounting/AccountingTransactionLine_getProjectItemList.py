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
            <value> <string>"""Returns all validated projects.\n
\n
This script is indented to be used on custom listfields for accounting lines, and on reports.\n
If this script returns an empty list, it means that reports by project are disabled.\n
"""\n
from Products.ERP5Type.Message import translateString\n
portal = context.getPortalObject()\n
\n
# case 1: script is used for reports, we display all validated projects.\n
if context.getPortalType() == \'Accounting Transaction Module\':\n
  project_list = []\n
  for project in portal.portal_catalog(\n
                           portal_type=\'Project\',\n
                           select_list=[\'relative_url\', \'title\', \'reference\'],\n
                           validation_state=(\'validated\',),\n
                           sort_on=((\'title\', \'ASC\'),)):\n
    if project.reference:\n
      project_list.append((\'%s - %s\' % (project.reference, project.title), project.relative_url,))\n
    else:\n
      project_list.append((project.title, project.relative_url,))\n
\n
  if not project_list:\n
    return [] # returning an empty list, not to add project column on reports\n
  return [(\'\', \'\'), (translateString(\'No Project\'), \'None\')] + project_list\n
  \n
# case 2: script is used on custom listfields.\n
#  for now the script has to be customized in such case.\n
# [(x.getTitle(), x.getRelativeUrl()) for x in context.project_module.searchFolder()]\n
return [(\'\', \'\')]\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>source=True</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>AccountingTransactionLine_getProjectItemList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
