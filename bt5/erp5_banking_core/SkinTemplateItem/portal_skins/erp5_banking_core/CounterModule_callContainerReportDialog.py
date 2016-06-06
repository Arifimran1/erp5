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
            <value> <string>from DateTime import DateTime\n
node = context.REQUEST.form[\'vault\']\n
default_resource = context.REQUEST.form[\'resource\']\n
context.log("kw %s" %(kw,))\n
context.log("req %s" %(context.REQUEST.form,))\n
container_portal_type_list = ["Monetary Reception",]\n
\n
base_price_dict = {}\n
\n
if listbox is None:\n
\n
#  node = context.getSource()\n
  reference_date = DateTime()\n
  container_list = []\n
  listbox = []\n
  #context.log("tracking list", context.portal_simulation.getCurrentTrackingList(at_date= reference_date, node = node))\n
  resource_translated_title_dict = {}\n
  total_price_dict = {}\n
  listbox_append = listbox.append\n
  for o in context.portal_simulation.getCurrentTrackingList(at_date= reference_date, node = node):\n
    cash_container = o.getObject()\n
\n
    if cash_container.getParentValue().getPortalType()  in container_portal_type_list:\n
      # get one line in order to know some properties of the cash container\n
      container_dict = {}\n
      container_lines = cash_container.objectValues(portal_type=\'Container Line\')\n
      if len(container_lines) == 0:\n
        context.log("MonetaryIssue_generateCashContainerInputDialog", "No container line find for cash container %s" %(cash_container.getRelativeUrl(),))\n
        continue\n
      container_line = container_lines[0]\n
      if default_resource is not None and container_line.getResourceId() != default_resource:\n
        context.log("skipping doc")\n
        continue\n
      container_dict[\'reference\'] = cash_container.getReference()\n
      container_dict[\'cash_number_range_start\'] = cash_container.getCashNumberRangeStart()\n
      container_dict[\'cash_number_range_stop\'] = cash_container.getCashNumberRangeStop()\n
\n
      resource = container_line.getResource()\n
      base_price = base_price_dict.get(resource, None)\n
      if base_price is None:\n
        base_price = container_line.getResourceValue().getBasePrice()\n
        base_price_dict[resource] = base_price\n
      container_dict[\'base_price\'] = base_price\n
      resource_translated_title = resource_translated_title_dict.get(resource, None)\n
      if resource_translated_title is None:\n
        resource_translated_title = container_line.getResourceTranslatedTitle()\n
        resource_translated_title_dict[resource] = resource_translated_title\n
      container_dict[\'resource_translated_title\'] = resource_translated_title\n
      quantity = container_line.getQuantity()\n
      container_dict[\'quantity\'] = quantity\n
      total_price = total_price_dict.get((quantity,resource), None)\n
      if total_price is None:\n
        total_price = container_line.getTotalPrice(fast=0)\n
        total_price_dict[(quantity,resource)] = total_price\n
      container_dict[\'total_price\'] = total_price\n
      container_dict[\'selection\'] = 0\n
      container_dict[\'date\'] = o.date\n
      container_dict[\'uid\'] = \'new_%s\' %(cash_container.getUid(),)   #cash_container.getReference().replace(\'/\', \'_\'),)\n
\n
      listbox_append(container_dict)\n
\n
  def sortListbox(a, b):\n
    result = cmp(a["date"], b["date"])\n
    if result == 0:\n
      result = cmp(a["base_price"], b["base_price"])\n
      if result == 0:\n
        result = cmp(a["reference"], b["reference"])\n
      \n
    return result\n
\n
  listbox.sort(sortListbox)\n
\n
  context.Base_updateDialogForm(listbox=listbox\n
                                )\n
\n
  return context.asContext(context=None\n
                           , portal_type=context.getPortalType()\n
                           ).CounterModule_viewContainerReportForm(**kw)\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>listbox=None, cash_detail_dict=None, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>CounterModule_callContainerReportDialog</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
