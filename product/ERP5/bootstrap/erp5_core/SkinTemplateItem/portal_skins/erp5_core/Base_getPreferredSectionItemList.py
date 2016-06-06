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
            <value> <string>""" Return the preferred sections.\n
The sections are of portal type `portal_type` and in state `validation_state`\n
and are member of the preferred section category (from preferences).\n
\n
An optional "base_category" can be passed to make sure the currently used\n
section is returned even if it\'s not in the list.\n
"""\n
\n
from Products.ERP5Type.Cache import CachingMethod\n
from AccessControl import getSecurityManager\n
\n
def getPreferredSectionItemList(portal_type, validation_state):\n
  portal = context.getPortalObject()\n
  section_category = portal.portal_preferences.getPreferredSectionCategory() or\\\n
                       portal.portal_preferences.getPreferredAccountingTransactionSectionCategory()\n
\n
  if not section_category:\n
    return [(\'\', \'\')]\n
\n
  group_uid = portal.portal_categories.getCategoryUid(section_category)\n
  return [(\'\', \'\')] + [(x.getTitle(), x.getRelativeUrl()) for x in \n
                      portal.portal_catalog(portal_type=portal_type,\n
                                            validation_state=validation_state,\n
                                            default_group_uid=group_uid,\n
                                            sort_on=(\'title\',))]\n
\n
getPreferredSectionItemList = CachingMethod(getPreferredSectionItemList,\n
                                            \'%s.%s\' % (script.getId(),\n
                                              getSecurityManager().getUser()),\n
                                            cache_factory=\'erp5_ui_short\')\n
section_item_list = getPreferredSectionItemList(portal_type, validation_state)\n
\n
if base_category:\n
  section_item_list = section_item_list[::] # make a copy not to modify the cache value\n
  current_category = context.getProperty(base_category)\n
  if current_category and current_category not in zip(*section_item_list)[1]:\n
    section_item_list.append(\n
        (context.getProperty(\'%s_title\' % base_category),\n
         context.getProperty(base_category)))\n
\n
return section_item_list\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>portal_type=[\'Organisation\'], validation_state=(\'validated\', \'draft\'), base_category=None</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Base_getPreferredSectionItemList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
