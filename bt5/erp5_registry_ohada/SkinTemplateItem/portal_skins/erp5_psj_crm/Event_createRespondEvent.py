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
            <value> <string># this script allows to create a new follow up ticket for a given event\n
event_object = context\n
event_module = context.getPortalObject().getDefaultModule(\n
                                          respond_event_portal_type)\n
# Create the outgoing\n
respond_event = event_module.newContent(\n
                       portal_type=respond_event_portal_type,\n
                       title=respond_event_title,\n
                       description=respond_event_description,\n
                       start_date=DateTime(),\n
                       source=context.getDefaultDestination(),\n
                       destination=context.getDefaultSource(),\n
                       causality=context.getRelativeUrl(),                      \n
)\n
\n
if respond_event_quotation:\n
  respond_event.edit(text_content=context.getReplyBody())\n
# Change the state to outgoing\n
respond_event.plan()\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>respond_event_portal_type, respond_event_title, respond_event_quotation, respond_event_description=\'\'</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Event_createRespondEvent</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
