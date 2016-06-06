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
            <value> <string>from Products.PythonScripts.standard import Object\n
request = container.REQUEST\n
\n
initial_debit_balance = request[\'TrialBalance.total_initial_debit_balance\']\n
initial_credit_balance = request[\'TrialBalance.total_initial_credit_balance\']\n
debit = request[\'TrialBalance.debit\']\n
credit = request[\'TrialBalance.credit\']\n
final_balance_if_debit = request[\'TrialBalance.final_balance_if_debit\']\n
final_balance_if_credit = request[\'TrialBalance.final_balance_if_credit\']\n
\n
return [ Object( initial_debit_balance=initial_debit_balance,\n
                 initial_credit_balance=initial_credit_balance,\n
                 initial_balance=initial_debit_balance-initial_credit_balance,\n
                 debit=debit,\n
                 credit=credit,\n
                 final_balance=(initial_debit_balance + debit) - (initial_credit_balance + credit),\n
                 final_debit_balance=initial_debit_balance + debit,\n
                 final_credit_balance=initial_credit_balance + credit,\n
                 final_balance_if_debit=final_balance_if_debit,\n
                 final_balance_if_credit=final_balance_if_credit ) ]\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>**kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>AccountModule_statAccountListForTrialBalance</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
