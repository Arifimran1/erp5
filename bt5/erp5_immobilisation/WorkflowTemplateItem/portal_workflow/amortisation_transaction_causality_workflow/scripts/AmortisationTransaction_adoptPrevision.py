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
            <value> <string>transaction = state_change[\'object\']\n
\n
# Set relative simulation movements profit_quantity to 0\n
movement_list = transaction.getMovementList()\n
all_simulation_movement_path_list = []\n
for movement in movement_list:\n
  simulation_movement_list = movement.getDeliveryRelatedValueList(portal_type=\'Simulation Movement\')\n
  for simulation_movement in simulation_movement_list:\n
    simulation_movement.edit(profit_quantity=0)\n
  all_simulation_movement_path_list.extend([x.getPath() for x in simulation_movement_list])\n
\n
# Update from simulation, then adapt causality value\n
builder = transaction.portal_deliveries.amortisation_transaction_builder\n
builder.updateFromSimulation(transaction.getRelativeUrl())\n
tag = \'%s_afterBuild\' % transaction.getRelativeUrl()\n
transaction.activate(tag=tag,\n
    after_path_and_method_id=(\n
    all_simulation_movement_path_list,\n
    (\'immediateReindexObject\', \'recursiveImmediateReindexObject\'))).AmortisationTransaction_afterBuild()\n
\n
# Automatic workflow\n
transaction.activate(after_tag=tag).updateCausalityState()\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>state_change</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>AmortisationTransaction_adoptPrevision</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
