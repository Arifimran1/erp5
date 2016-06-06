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
            <value> <string>task_list = [x.getObject() for x in \\\n
  context.portal_catalog(selection_report=selection_report, \n
                         portal_type=\'Task\',\n
                         simulation_state=context.getPortalDraftOrderStateList()+\n
                                          context.getPortalPlannedOrderStateList())]\n
task_list.extend([x.getObject() for x in \\\n
  context.portal_catalog(selection_report=selection_report, \n
                         portal_type=\'Task Report\',\n
                         simulation_state=context.getPortalReservedInventoryStateList()+\n
                                          context.getPortalCurrentInventoryStateList())])\n
task_line_list = []\n
for task in task_list:\n
  current_task_line_list = task.objectValues(portal_type=(\'Task Line\', \'Task Report Line\'))\n
  for task_line in current_task_line_list:\n
    update_kw = {}\n
    if task_line.getPortalType() == \'Task Report Line\':\n
      simulation_related_list = task_line.getDeliveryRelatedValueList()\n
      causality_list = []\n
      for simulation_movement in simulation_related_list:\n
        causality_list.extend(simulation_movement.getOrderValueList())\n
      causality_len = len(causality_list)\n
      if causality_len == 0:\n
        # No task, so this was not decided at the beginning\n
        pass\n
      elif causality_len == 1:\n
        # There is a task, we should be able to compare quantity\n
        # date, resources....\n
        causality = causality_list[0]\n
        update_kw[\'initial_quantity\'] = causality.getQuantity()\n
        update_kw[\'initial_start_date\'] = causality.getStartDate()\n
        update_kw[\'initial_stop_date\'] = causality.getStopDate()\n
        update_kw[\'real_quantity\'] = task_line.getQuantity()\n
        update_kw[\'real_start_date\'] = task_line.getStartDate()\n
        update_kw[\'real_stop_date\'] = task_line.getStopDate()\n
      else:\n
        raise ValueError, "This script more than one causality yet"\n
    elif task_line.getPortalType() == \'Task Line\':\n
      update_kw[\'initial_quantity\'] = task_line.getQuantity()\n
      update_kw[\'initial_start_date\'] = task_line.getStartDate()\n
      update_kw[\'initial_stop_date\'] = task_line.getStopDate()\n
    task_line_list.append(task_line.asContext(**update_kw))\n
\n
return task_line_list\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>selection=None, selection_report=None, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Project_getSummaryList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
