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
            <value> <string>"""This script is used to know if quantity can be edited by user.\n
\n
* If this is not a movement (line containing lines or cell), user\n
cannot edit this line which is just a container, but no actual movement.\n
\n
* If this line has variation category list, then it means it\'s a line that\n
will contain cell, so it\'s already not possible to set quantity, user have\n
to create cells and set quantities on cells.\n
\n
* If items are used, quantity is set by the item quantity.\n
"""\n
\n
if not context.isMovement():\n
  return False\n
\n
if context.getVariationCategoryList() and not \'Cell\' in context.getPortalType():\n
  return False\n
\n
return not (context.getResource() and context.getResourceValue().getAggregatedPortalTypeList())\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Movement_isQuantityEditable</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
