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
            <value> <string>"""Reset everything for the test"""\n
\n
# Clean up the contents.\n
for name in (\'foo_module\', \'bar_module\', \'foo_bar_module\'):\n
  module = getattr(context, name)\n
  module.manage_delObjects(list(module.objectIds()))\n
  module.setLastId(1)\n
\n
# Reset the foo module listbox\n
form = context.FooModule_viewFooList\n
result = form.listbox.ListBox_setPropertyList()\n
\n
#form.listbox.manage_edit(dict(\n
#  lines = 3, all_columns = [], search_columns = [], sort_columns = [],\n
#  sort = [], stat_columns = [], url_columns = [],\n
#  list_method = \'\', count_method = \'\',\n
#  stat_method = \'\', search = \'\', select = \'\', list_action = \'list\'))\n
\n
# Reset the Foo_viewRelationField listbox (modified by listbox_zuite/testRedirect UI test)\n
form = context.Foo_viewRelationField\n
default_columns = \'\\n\'.join(( \'id | ID\'\n
                            , \'title | Title\'\n
                            , \'quantity | Quantity\'\n
                            ))\n
result = form.listbox.ListBox_setPropertyList( \n
    field_title            = \'Foo Lines\'\n
  , field_columns          = default_columns\n
  , field_sort             = \'id\'\n
  , field_editable_columns = default_columns\n
  , field_list_method      = \'objectValues\'\n
  , field_count_method     = \'\'\n
  , field_selection_name   = \'foo_line_selection\'\n
  , field_portal_types     = \'\'\n
  , field_search           = \'\'\n
  , field_select           = \'\'\n
  , field_list_action      = \'Folder_viewContentList\'\n
  , field_editable         = \'checked\'\n
  )\n
\n
# Reset the selection.\n
def resetSelection(selection_name):\n
  selection_tool = context.portal_selections\n
  if selection_tool.getSelectionFor(selection_name) is not None:\n
    selection_tool.setSelectionToAll(selection_name, reset_domain_tree=True, reset_report_tree=True)\n
    selection_tool.setSelectionSortOrder(selection_name, [])\n
    selection_tool.setSelectionColumns(selection_name, [])\n
    selection_tool.setSelectionStats(selection_name, [])\n
    selection_tool.setListboxDisplayMode(context.REQUEST, \'FlatListMode\', selection_name)\n
    selection_tool.setSelectionParamsFor(selection_name, {})\n
\n
resetSelection(\'foo_selection\')\n
resetSelection(\'foo_line_selection\')\n
resetSelection(\'bar_selection\')\n
\n
\n
pref = getattr(context.portal_preferences, "erp5_ui_test_preference", None)\n
if pref is None:\n
  pref = context.portal_preferences.newContent(id="erp5_ui_test_preference", portal_type="Preference")\n
pref.setPreferredListboxViewModeLineCount(None)\n
pref.setPreferredListboxListModeLineCount(10)\n
if pref.getPreferenceState() == \'disabled\':\n
  pref.enable()\n
else:\n
  context.portal_caches.clearAllCache()\n
\n
return \'Reset Successfully.\'\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>ListBoxZuite_reset</string> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string>Reset Everything</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
