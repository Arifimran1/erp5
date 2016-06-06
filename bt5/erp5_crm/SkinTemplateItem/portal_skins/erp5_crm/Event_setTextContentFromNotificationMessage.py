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
            <value> <string>portal = context.getPortalObject()\n
if not language:\n
  language = context.getLanguage()\n
  if not language:\n
    language = portal.portal_preferences.getPreferredCustomerRelationLanguage()\n
    \n
notification_message = portal.portal_notifications.getDocumentValue(\n
                                language=language,\n
                                reference=reference)\n
\n
if substitution_method_parameter_dict is None:\n
  substitution_method_parameter_dict = {}\n
# Notification method will receive the current event under "event_value" key.\n
# This way notification method can return properties from recipient or follow up of the event.\n
substitution_method_parameter_dict.setdefault(\'event_value\', context)\n
\n
\n
if notification_message is not None:\n
  context.setContentType(notification_message.getContentType())\n
  target_format = "txt"\n
  if context.getContentType() == \'text/html\':\n
    target_format = "html"\n
  mime, text_content = notification_message.convert(target_format,\n
      substitution_method_parameter_dict=substitution_method_parameter_dict)\n
  context.setTextContent(text_content)\n
  context.setAggregateList(notification_message.getProperty(\'aggregate_list\', []))\n
  \n
  if not context.hasTitle():\n
    context.setTitle(notification_message.asSubjectText(\n
      substitution_method_parameter_dict=substitution_method_parameter_dict))\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>reference, language=None, substitution_method_parameter_dict=None</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Event_setTextContentFromNotificationMessage</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
