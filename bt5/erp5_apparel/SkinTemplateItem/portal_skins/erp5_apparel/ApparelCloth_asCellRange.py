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

cell_range = []\n
\n
# Get base category list\n
selected_base_category_list = context.getVariationBaseCategoryList()\n
\n
# Generate cell range\n
for base_category in selected_base_category_list:\n
  if matrixbox==1:\n
    # XXX matrixbox is right_display (not as listfield) \n
    # => invert display and value in item\n
    cell_range.append(map(lambda x: (x[1], x[0]),\n
                          context.getVariationCategoryItemList(\n
                                 base_category_list=[base_category,],\n
                                 display_base_category=display_base_category,\n
                                 sort_id=\'id\')))\n
  else:\n
    cell_range.append(\n
              context.getVariationCategoryList(\n
                                     base_category_list=[base_category,],\n
                                     sort_id=\'id\'))\n
\n
# Remove empty range\n
cell_range = [x for x in cell_range if x!=[]]\n
return cell_range\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>base_id=\'path\', matrixbox=0, display_base_category=1, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>ApparelCloth_asCellRange</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
