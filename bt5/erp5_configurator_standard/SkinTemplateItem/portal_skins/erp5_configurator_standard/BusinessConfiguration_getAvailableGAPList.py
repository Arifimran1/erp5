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
            <value> <string>"""This script returns the list of available accounting plan information.\n
\n
To make a new accounting plan available to TioLive , add an entry in this list.\n
"""\n
\n
Base_translateString = context.Base_translateString\n
\n
return [\n
  dict(id=\'ifrs\',\n
       name=Base_translateString(\'IAS-IFRS Compliant\'),\n
       root=\'gap/ias/ifrs\',\n
       bt5=\'erp5_accounting_l10n_ifrs\',),\n
  dict(id=\'fr\',\n
       name=Base_translateString(\'PCG (France)\'),\n
       root=\'gap/fr/pcg\',\n
       bt5=\'erp5_accounting_l10n_fr\',),\n
  dict(id=\'de\',\n
       name=Base_translateString(\'SKR04 (Germany)\'),\n
       root=\'gap/de/skr04\',\n
       bt5=\'erp5_accounting_l10n_de_skr04\',),\n
  dict(id=\'sn\',\n
       name=Base_translateString(\'SYSCOA (West Africa)\'),\n
       root=\'gap/ohada/syscohada\',\n
       bt5=\'erp5_accounting_l10n_sn\',),\n
  dict(id=\'br\',\n
       name=Base_translateString(\'Plano Geral de Contas (Brazil)\'),\n
       root=\'gap/br/pcg\',\n
       bt5=\'erp5_accounting_l10n_br_extend\',),\n
  dict(id=\'lu\',\n
       name=Base_translateString(\'Standard Luxembourgers Plan(Luxembourg)\'),\n
       root=\'gap/lu/standard\',\n
       bt5=\'erp5_accounting_l10n_lu\',),\n
  dict(id=\'ru\',\n
       name=Base_translateString(\'Standard Russian Plan (2000 edition)\'),\n
       root=\'gap/ru/ru2000\',\n
       bt5=\'erp5_accounting_l10n_ru\',),\n
  dict(id=\'cn\',\n
       name=Base_translateString(\'Basic Chinese Plan\'),\n
       root=\'gap/cn/basic\',\n
       bt5=\'erp5_accounting_l10n_cn_basic\',),\n
]\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>BusinessConfiguration_getAvailableGAPList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
