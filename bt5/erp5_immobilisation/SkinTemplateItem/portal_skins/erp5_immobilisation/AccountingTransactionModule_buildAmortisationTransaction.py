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

builder_kw = {\'activate_kw\':{\'tag\':\'build_amortisation_transaction\'}}\n
applied_rule_list = []\n
if len(item_uid_list) > 0:\n
  item_value_list = [context.portal_catalog.getObject(uid) for uid in item_uid_list]\n
  #context.log(\'item_value_list in AccountingTransactionModule_buildAmortisationTransaction\',item_value_list)\n
  for item_value in item_value_list:\n
    applied_rule = item_value.getCausalityRelatedValueList(portal_type=\'Applied Rule\')\n
    if len(applied_rule) == 1:\n
      applied_rule_list.append(applied_rule[0])\n
  builder_kw[\'applied_rule_uid\'] = [x.getUid() for x in applied_rule_list]\n
if at_date not in (None, \'None\'):\n
  date_dict = {\'query\':[at_date],\n
               \'range\':\'ngt\'}\n
  builder_kw[\'movement.stop_date\'] = date_dict\n
if len(item_uid_list) > 0 and len(applied_rule_list) == 0:\n
  context.log(\'ERP5 Amortisation Build :\',\'No applied rule to select for build with item_uid_list %s\' % item_uid_list)\n
  return None\n
#context.log(\'ERP5 Amortisation Build builder_kw:\',builder_kw)\n
context.portal_deliveries.amortisation_transaction_builder.build(**builder_kw)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>at_date=None, item_uid_list=[]</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>AccountingTransactionModule_buildAmortisationTransaction</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
