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
            <value> <string>Base_translateString = context.Base_translateString\n
split_depth = 2\n
\n
def getSubFieldDict():\n
  def getSubFieldDictCache():\n
    # Define a dictionary where we store the subfields to display.\n
    sub_field_dict = {}\n
    # Try to assign each item to a sub field.\n
    for item in item_list:\n
      # Get value of the item\n
      item_value = item[int(not is_right_display)]\n
      \n
      # Hash key from item_value\n
      item_split = item_value.split(\'/\')\n
      item_key = \'/\'.join(item_split[:split_depth])\n
\n
      # Create a new subfield if necessary\n
      if not sub_field_dict.has_key(item_key):\n
        # Create property dict (key are field parameters)\n
        sub_field_property_dict = default_sub_field_property_dict.copy()\n
        sub_field_property_dict[\'key\'] = item_key\n
        sub_field_property_dict[\'title\'] = Base_translateString("GAP - ${gap_title}", mapping=dict(\n
                    gap_title=context.portal_categories.resolveCategory(\n
                          \'gap/%s\' % item_key).getTitle()))\n
        sub_field_property_dict[\'required\'] = 0\n
        sub_field_property_dict[\'field_type\'] = \'ListField\'\n
        sub_field_property_dict[\'size\'] = 1\n
        sub_field_property_dict[\'item_list\'] = [(\'\', \'\') ]\n
        sub_field_property_dict[\'value\'] = None\n
        sub_field_dict[item_key] = sub_field_property_dict\n
\n
      sub_field_dict[item_key][\'item_list\'].append(item)\n
      sub_field_property_dict[\'size\'] = 1\n
    return sub_field_dict\n
\n
  from Products.ERP5Type.Cache import CachingMethod\n
  getSubFieldDictCache = CachingMethod(getSubFieldDictCache,\n
                                  id=\'Account_getSubFieldDict\')\n
  # Those cached dictionnaries are later modified, we just reset the \'value\'\n
  # key to return clean dictionnaries.\n
  sub_field_dict = getSubFieldDictCache()\n
  for k in sub_field_dict.keys():\n
    sub_field_dict[k][\'value\'] = None\n
  return sub_field_dict\n
\n
sub_field_dict = getSubFieldDict()\n
# Update sub_field_dict with values\n
for item_value in value_list:\n
  if item_value:\n
    # Hash key from item_value\n
    item_split = item_value.split(\'/\')\n
    item_key = \'/\'.join(item_split[:split_depth])\n
    \n
    if not sub_field_dict.has_key(item_key):\n
      # This can only happens if an accounting plan have been uninstalled\n
      sub_field_property_dict = default_sub_field_property_dict.copy()\n
      sub_field_property_dict[\'key\'] = item_key\n
      sub_field_property_dict[\'title\'] = item_key\n
      sub_field_property_dict[\'required\'] = 0\n
      sub_field_property_dict[\'field_type\'] = \'ListField\'\n
      sub_field_property_dict[\'size\'] = 1\n
      sub_field_property_dict[\'item_list\'] = [(\'\', \'\')]\n
      sub_field_property_dict[\'value\'] = None\n
      sub_field_dict[item_key] = sub_field_property_dict\n
\n
    sub_field_dict[item_key][\'value\'] = item_value\n
\n
# Return the list of subfield configuration.\n
return sub_field_dict.values()\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>item_list, value_list, default_sub_field_property_dict={}, is_right_display=0</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Account_hashGapItemList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
