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
            <value> <string>"""\n
  TODO:\n
  Make consistent with ERP5Site_newContent\n
  User cache\n
  XXX maybe it could/should use ERP5TypeInformation.isConstructionAllowed ???\n
"""\n
\n
portal_object = context.getPortalObject()\n
try:\n
  module = portal_object.getDefaultModule(portal_type)\n
except ValueError:\n
  return False\n
if module is None:\n
  return False\n
\n
if user is None: # can be passed directly to save resources if we are doing this many times\n
  from AccessControl import getSecurityManager\n
  user = getSecurityManager().getUser()\n
\n
return user.has_permission(\'Add portal content\', module)\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>portal_type, user=None</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>ERP5Site_isNewContentAllowed</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
