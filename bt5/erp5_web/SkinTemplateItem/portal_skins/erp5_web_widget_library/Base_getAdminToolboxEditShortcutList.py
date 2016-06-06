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

"""\n
  This script creates edit actions for the admin toolbox\n
  and adds some extra actions taken from the action_list\n
  defined in portal_types tool.\n
\n
  The script is able to rewrite some actions by looking at the\n
  editable_absolute_url property stored on Context objects\n
  which are created for virtual pages. (ie. pages which\n
  are obtained through _aq_dynamic from Web Section or Web Page)\n
"""\n
# Init some variables\n
translateString = context.Base_translateString\n
result = []\n
portal_type = context.getPortalType()\n
translated_portal_type = context.getTranslatedPortalType()\n
request = context.REQUEST\n
current_web_section = request.current_web_section\n
current_web_section_translated_portal_type = current_web_section.getTranslatedPortalType()\n
action_dict = request.get(\'actions\', {}) # XXX actions needs to be renamed to action_dict\n
exchange_action_list = action_dict.get(\'object_exchange\', [])\n
button_action_list = action_dict.get(\'object_button\', [])\n
portal_url = (context.getWebSiteValue() or context.getPortalObject()).absolute_url()\n
http_parameters = request.get(\'http_parameters\', \'\')\n
http_parameters = http_parameters.replace(\'editable_mode\', \'dummy_editable_mode\')\n
\n
# Try to get the original absolute_url if this is a permanent URL\n
absolute_url = context.absolute_url()\n
editable_absolute_url = getattr(context, \'editable_absolute_url\', absolute_url)\n
\n
# action title based on security\n
\n
editable_mode = int(request.form.get(\'editable_mode\', \n
                                     request.get(\'editable_mode\', 0)))\n
edit_permission = context.portal_membership.checkPermission(\'Modify portal content\', context)\n
\n
# Append a button to edit the content of the current document for Web Page\n
if not editable_mode and edit_permission and portal_type == \'Web Page\':\n
  result.append(dict(\n
    url = "%s/WebPage_viewEditor?editable_mode:int=1&%s" \n
            %(editable_absolute_url, http_parameters),\n
    icon = "%s/%s" % (portal_url, context.getIcon(relative_to_portal=True) or \'file_icon.gif\'),\n
    title = translateString("Edit ${portal_type} content",\n
                                 mapping=dict(portal_type=translated_portal_type)),\n
    label = ""))\n
\n
# Append a button to edit the current document\n
if not editable_mode:\n
  if edit_permission:\n
    edit_title = translateString("Edit ${portal_type} details",\n
                                 mapping=dict(portal_type=translated_portal_type))\n
  else:\n
    edit_title = translateString("Access ${portal_type} details",\n
                                 mapping=dict(portal_type=translated_portal_type))\n
  result.append(dict(\n
    url = "%s/view?editable_mode:int=1&%s" \n
            %(editable_absolute_url, http_parameters),\n
    icon = "%s/%s" % (portal_url, context.getIcon(relative_to_portal=True) or \'file_icon.gif\'),\n
    title = edit_title,\n
    label = ""))\n
else: \n
  result.append(dict(\n
    url = "%s/view?editable_mode:int=0&%s" % (absolute_url, http_parameters),\n
    icon = "%s/%s" % (portal_url, context.getIcon(relative_to_portal=True) or \'file_icon.gif\'),\n
    title = translateString("View ${portal_type}", \n
                            mapping=dict(portal_type=translated_portal_type)),\n
                            label = ""))\n
\n
# Append a button to edit the parent section\n
if portal_type not in (\'Web Section\', \'Web Site\'): \n
  result.append(dict(\n
    url = "%s/view?editable_mode=1" % current_web_section.absolute_url(),\n
    icon = "%s/%s" % (portal_url, current_web_section.getIcon(relative_to_portal=True)),\n
    title = translateString("Edit Parent ${portal_type}",\n
                             mapping=dict(portal_type=current_web_section_translated_portal_type)),\n
    label = ""))\n
\n
# Append all icon buttons\n
for action in button_action_list:\n
  if action[\'id\'] == \'webdav\':\n
    result.append(dict(\n
      url = action[\'url\'].replace(absolute_url, editable_absolute_url),\n
      icon = action[\'icon\'],\n
      title = translateString(action[\'title\']),\n
      label = ""))\n
\n
# Append an exchange button\n
if len(exchange_action_list):\n
  action = exchange_action_list[0]\n
  url = action[\'url\'].replace(absolute_url, editable_absolute_url)\n
  url = \'%s?dialog_category=object_exchange&cancel_url=%s/view\' % (url, absolute_url)\n
  result.append(dict(\n
    url = url,\n
    icon  = \'%s/import_export.png\' % portal_url,\n
    title = translateString(\'Import / Export\'),\n
    label = ""))\n
\n
return result\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Base_getAdminToolboxEditShortcutList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
