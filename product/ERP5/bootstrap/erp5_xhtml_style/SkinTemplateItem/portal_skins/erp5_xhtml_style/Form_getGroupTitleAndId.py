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
  This script splits a form group id in two part:\n
    * a group id,\n
    * a group title.\n
\n
  The group should be named based on the following pattern: "group id (Group Title)" \n
\n
  This script is a hack to let us merge two informations (id and title) into one (id) to get\n
    over Formulator limitations. This script should disappear with Formulator\'s refactoring.\n
\n
  Features: \n
    * Multiple parenthesis allowed;\n
    * Group id can continue after the title definition.\n
\n
  Example:\n
    A string like\n
      "left webcontent (The Fantastic Group (and (funky) lisp-like parenthesis)) extra",\n
    will return the following tuple:\n
      ( \'left webcontent extra\'\n
      , \'The Fantastic Group (and (funky) lisp-like parenthesis)\'\n
      , \'left webcontent (The Fantastic Group (and (funky) lisp-like parenthesis)) extra\'\n
      )\n
"""\n
form=context\n
\n
def getFormGroupTitleAndId():\n
  res = []\n
  append = res.append\n
  for original_group_id in form.get_groups(include_empty=0):\n
    group_id = original_group_id\n
    try:\n
      group_id_head, group_id_rest = group_id.split(\'(\', 1)\n
      group_title, group_id_tail = group_id_rest.rsplit(\')\', 1)\n
      group_id = group_id_head + group_id_tail\n
      if not group_title:\n
        group_title = None\n
    except ValueError:\n
      # When group_id does not have parentheses.\n
      group_title = None\n
    group_id = \' \'.join((w for w in group_id.split(\' \') if w))\n
    append({\'gid\': group_id, \'gtitle\': group_title, \'goid\': original_group_id})\n
  return res\n
\n
return getFormGroupTitleAndId()\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Form_getGroupTitleAndId</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
