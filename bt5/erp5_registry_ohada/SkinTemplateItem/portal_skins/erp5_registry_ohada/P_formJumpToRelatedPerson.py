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
            <value> <string># Jump to a person of the current P form\n
request=context.REQUEST\n
p_form = context.getObject()\n
\n
if p_form is not None:\n
  portal = context.getPortalObject()\n
  rccm = p_form.getCorporateRegistrationCode()\n
  pers_result = portal.organisation.searchFolder(corporate_registration_code=rccm)\n
  person_uid_list = [pers.getObject().getUid() for pers in pers_result]\n
\n
  if len(person_uid_list) != 0 :\n
    kw = {\'uid\': person_uid_list}\n
    context.portal_selections.setSelectionParamsFor(\'Base_jumpToRelatedObjectList\', kw)\n
    request.set(\'object_uid\', context.getUid())\n
    request.set(\'uids\', person_uid_list)\n
    return context.Base_jumpToRelatedObjectList(uids=person_uid_list, REQUEST=request)\n
\n
redirect_url = \'%s/view?%s\' % (context.getPath(),\n
            \'portal_status_message=No+Person+Related+Current+Form\')\n
\n
return context.REQUEST[ \'RESPONSE\' ].redirect(redirect_url)\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>P_formJumpToRelatedPerson</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
