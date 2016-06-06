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
  Sets the causality relation on a delivery from the order it comes from.\n
This script should be called in the after generation script of the DeliveryBuilder.\n
\n
IMPORTANT WARNING: this script will not work if your simulation movements are not\n
reindexed yet ()\n
It will also not work if strict security is set on simulation. It\'s recommended to use\n
(Delivery) Causality Movement Group as delivery level movement group in the corresponding\n
delivery builder.\n
"""\n
from Products.ERP5Type.Log import log\n
LOG = lambda msg:log(\n
          "Delivery_setCausalityFromSimulation on %s" % context.getPath(), msg)\n
LOG = lambda msg:\'DISABLED\'\n
\n
delivery = context\n
\n
# get the list of simulation movement which have built this delivery\n
simulation_movement_list = []\n
for movement in delivery.getMovementList() :\n
  LOG("movement %s " % movement.getPath())\n
  simulation_movement_list.extend(\n
        movement.getDeliveryRelatedValueList(\n
          portal_type = \'Simulation Movement\'))\n
\n
LOG("simulation_movement_list %s " % simulation_movement_list)\n
\n
causality_value_set = {}\n
for simulation_movement in simulation_movement_list :\n
  LOG("simulation_movement %s " % simulation_movement.getPath())\n
  if simulation_movement.getParentValue() != simulation_movement.getRootAppliedRule():\n
    explanation_value = simulation_movement.getParentValue().getParentValue().getExplanationValue()\n
  else :\n
    explanation_value = simulation_movement.getExplanationValue()\n
  if explanation_value is not None :\n
    causality_value_set[explanation_value] = 1\n
\n
LOG(\'setCausalityValueList %s\'%causality_value_set.keys())\n
delivery.setCausalityValueList(causality_value_set.keys() + delivery.getCausalityValueList())\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Delivery_setCausalityFromSimulation</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
