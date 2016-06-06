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
This script returns a list of dictionaries which represent\n
the security groups which a person is member of. It extracts\n
the categories from the current content. It is useful in the\n
following cases:\n
\n
- calculate a security group based on a given\n
  category of the current object (ex. group). This\n
  is used for example in ERP5 DMS to calculate\n
  document security.\n
\n
- assign local roles to a document based on\n
  the person which the object related to through\n
  a given base category (ex. destination). This\n
  is used for example in ERP5 Project to calculate\n
  Task / Task Report security.\n
\n
The parameters are\n
\n
  base_category_list -- list of category values we need to retrieve\n
  user_name          -- string obtained from getSecurityManager().getUser().getId()\n
  object             -- object which we want to assign roles to\n
  portal_type        -- portal type of object\n
\n
NOTE: for now, this script requires proxy manager\n
"""\n
from Products.CMFCore.WorkflowCore import WorkflowException\n
\n
portal_workflow = context.getPortalObject().portal_workflow\n
\n
last_site, last_group, last_function, last_user = (None, None, None, None)\n
\n
wf_list = [x for x, y in context.getWorkflowStateItemList()]\n
for wf_id in wf_list: \n
  try:\n
    history_list = context.portal_workflow.getInfoFor(ob=context, \n
                                              name=\'history\', wf_id=wf_id)\n
  except WorkflowException:\n
    continue\n
\n
  # reverse the list to get the first assign user\n
  history_list = list(history_list)\n
  history_list.reverse()\n
\n
  for history_line in history_list:\n
    if history_line.has_key(\'assigned_group\') and history_line[\'assigned_group\']:\n
      last_group = history_line[\'assigned_group\']\n
      last_function = history_line[\'assigned_function\']\n
      last_site = history_line[\'assigned_site\']\n
    if history_line.has_key(\'assigned_user\') and history_line[\'assigned_user\']:\n
      last_user = history_line[\'assigned_user\']\n
\n
if last_group:\n
  return [{\'function\': last_function,\n
           \'group\': last_group,\n
           \'site\': last_site}\n
         ]\n
\n
if last_user:\n
  user = context.ERP5Site_getPersonObjectFromUserName(last_user)\n
  if user:\n
    url = user.getRelativeUrl()\n
    return [{\'group\': url},]\n
\n
return []\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>base_category_list=[], user_name=None, object=None, portal_type=None</string> </value>
        </item>
        <item>
            <key> <string>_proxy_roles</string> </key>
            <value>
              <tuple>
                <string>Assignor</string>
                <string>Manager</string>
              </tuple>
            </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>ERP5Site_getSecurityFromWorkflowAssignment</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
