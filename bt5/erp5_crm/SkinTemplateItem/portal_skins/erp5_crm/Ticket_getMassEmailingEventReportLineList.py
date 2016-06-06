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

portal = context.getPortalObject()\n
\n
count = portal.portal_catalog.countResults\n
\n
total_events = count(follow_up_uid=context.getUid(), \n
  portal_type="Mail Message", \n
  simulation_state=("received", "delivered", "started"))[0][0]\n
total_opened = count(follow_up_uid=context.getUid(), \n
  portal_type="Mail Message", \n
  simulation_state=("received", "delivered"))[0][0]\n
total_read = count(follow_up_uid=context.getUid(), \n
  portal_type="Mail Message", simulation_state="delivered")[0][0]\n
\n
if total_events > 0:\n
  line = context.newContent(temp_object=1, total_event_sent=total_events, \n
    total_event_received=total_opened, \n
    total_event_received_percent=float(total_opened)/float(total_events)*100, \n
    total_event_delivered=total_read,\n
    total_event_delivered_percent=float(total_read)/float(total_events)*100)\n
  return line,\n
else:\n
  return []\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>*args, **kw</string> </value>
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
            <value> <string>Ticket_getMassEmailingEventReportLineList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
