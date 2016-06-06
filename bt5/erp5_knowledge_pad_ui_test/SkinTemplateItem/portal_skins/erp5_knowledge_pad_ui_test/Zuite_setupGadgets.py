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
            <value> <string># Publish all knowledge pad gadgets\n
for gadget in context.portal_gadgets.objectValues():\n
  if gadget.getValidationState() == \'invisible\':\n
    gadget.visible()\n
    gadget.public()\n
\n
# add to preference a template pad\n
active_preference = context.portal_preferences.getActivePreference()\n
knowledge_pad = active_preference.newContent(portal_type="Knowledge Pad",\n
                                             title="Template Pad")\n
knowledge_pad.visible()\n
knowledge_pad.public()\n
\n
\n
if remove_existing_pads:\n
  # delete existing pads\n
  user_knowledge_pad_list = context.ERP5Site_getKnowledgePadListForUser(mode = mode)\n
  context.knowledge_pad_module.manage_delObjects([x.getId() for x in user_knowledge_pad_list])\n
\n
print "Done"\n
return printed\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>remove_existing_pads=0, mode=\'erp5_front\'</string> </value>
        </item>
        <item>
            <key> <string>_proxy_roles</string> </key>
            <value>
              <tuple>
                <string>Manager</string>
                <string>Owner</string>
              </tuple>
            </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Zuite_setupGadgets</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
