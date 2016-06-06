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
            <key> <string>_Access_contents_information_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Change_bindings_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Change_cache_settings_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Change_permissions_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Copy_or_Move_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Delete_objects_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Manage_WebDAV_Locks_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Manage_properties_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Take_ownership_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_Undo_changes_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_View_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_View_management_screens_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_WebDAV_Lock_items_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_WebDAV_Unlock_items_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
        </item>
        <item>
            <key> <string>_WebDAV_access_Permission</string> </key>
            <value>
              <list>
                <string>Manager</string>
              </list>
            </value>
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

"""List all skins that are present in more than one skin folder, ordered by\n
priority.\n
"""\n
\n
# make sure context is the skins tool\n
stool = context.portal_skins\n
\n
print \'<html><body>\'\n
skins_by_name = {}\n
\n
for skin_key, skin_path_list in stool.getSkinPaths():\n
  if skin_key == stool.getDefaultSkin():\n
    skin_path_list = skin_path_list.split(\',\')\n
    for skin_path in skin_path_list:\n
      # skip CMF paths\n
      if skin_path in (\'control\', \'zpt_control\',\n
                       \'generic\', \'zpt_generic\',\n
                       \'content\', \'zpt_content\'):\n
        continue\n
      skin_folder = stool.portal_skins[skin_path]\n
      for skin in skin_folder.objectValues():\n
        skins_by_name.setdefault(skin.getId(), []).append(skin_path)\n
\n
for skin_name, location_list in skins_by_name.items():\n
  if len(location_list) > 1:\n
    print skin_name, \'<br/>\'\n
    for location in location_list:\n
      print "&nbsp;" * 3, \'<a href="%s/%s/%s/manage_main">%s</a><br/>\' % (stool.absolute_url(), location, skin_name, location)\n
\n
print \'</body></html>\'\n
return printed\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>SkinsTool_listDuplicateSkins</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
