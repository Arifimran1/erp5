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

inventory_kw = {}\n
if multiplier in (None, \'\'):\n
  multiplier = 1.0\n
inventory_kw["at_date"] = at_date\n
inventory_kw["from_date"] = from_date\n
inventory_kw["quantity"] = "<0"\n
if ledger:\n
  inventory_kw["parent_ledger_relative_url"] = "ledger/%s" % ledger\n
if multiplier is None:\n
  multiplier = 1\n
\n
portal = context.getPortalObject()\n
simulation_state_set = set(simulation_state_list)\n
# We will use inventory API in order to find all quantities\n
before_confirmed_task_state_set = set(portal.getPortalPlannedOrderStateList() + \\\n
         portal.getPortalDraftOrderStateList())\n
task_state_set = simulation_state_set.intersection(before_confirmed_task_state_set)\n
result_list = []\n
if len(task_state_set):\n
  result_list.extend(portal.portal_simulation.getInventoryList(\n
                simulation_state = [x for x in task_state_set],\n
                portal_type=[\'Task Line\'],\n
                **inventory_kw))\n
task_report_state_set = simulation_state_set.difference(before_confirmed_task_state_set)\n
if len(task_report_state_set):\n
  result_list.extend(portal.portal_simulation.getInventoryList(\n
                simulation_state = [x for x in task_report_state_set],\n
                portal_type=\'Task Report Line\',\n
                **inventory_kw))\n
\n
summary_dict = {}\n
total_project_dict = {}\n
item_url_set = set()\n
for x in result_list:\n
  aggregate_url = x.sub_variation_text\n
  item_url = None\n
  if aggregate_url:\n
    if aggregate_url.startswith("aggregate"):\n
      item_url = aggregate_url.split("aggregate/")[1]\n
  if item_url is None:\n
    item_url = "None"\n
  item_url_set.add(item_url)\n
  person_uid = x.node_uid\n
  person_dict = summary_dict.setdefault(person_uid, {})\n
  person_dict[item_url] = x.quantity * multiplier + person_dict.get(item_url, 0)\n
  person_dict["total"] = x.quantity * multiplier + person_dict.get("total", 0)\n
  total_project_dict[item_url] = x.quantity * multiplier + total_project_dict.get(item_url, 0)\n
  total_project_dict["total"] = x.quantity * multiplier + total_project_dict.get("total", 0)\n
\n
# now we group all results per person and we prepare one line in the listbox\n
# per person.\n
person_title_dict = {}\n
listbox_line_list = []\n
def getColumnUrl(brain=None, column_id=None, **kw):\n
  return getattr(brain, "%s_column_url" % column_id)\n
\n
absolute_url = portal.absolute_url()\n
\n
if len(summary_dict):\n
  for person in portal.portal_catalog(portal_type=("Person", "Organisation"), uid=summary_dict.keys(), select_list=["title"]):\n
    person_title_dict[person.uid] = person.title\n
  for person_uid in summary_dict.keys():\n
    person_kw = summary_dict[person_uid]\n
    person_kw["source_title"] = person_title_dict[person_uid]\n
    person = portal.person_module.newContent(temp_object=1, **person_kw)\n
    for item_url in summary_dict[person_uid].keys():\n
      task_report_module_url = "%s/task_report_module/view?reset:int=1&default_source_uid=%s&title=%%" % (absolute_url, person_uid)\n
      if item_url == "None":\n
        task_report_module_url += "&child_aggregate_relative_url=%%3dNULL&left_join_list=child_aggregate_relative_url&ledger_relative_url=ledger/%s" % \\\n
                     (ledger, )\n
      else:\n
        task_report_module_url += "&child_aggregate_relative_url=%s&ledger_relative_url=ledger/%s" % \\\n
                     (item_url, ledger)\n
      person.edit(**{"%s_column_url" % item_url: task_report_module_url})\n
    person.setProperty("getColumnUrl", getColumnUrl)\n
    listbox_line_list.append(person)\n
\n
listbox_line_list.sort(key=lambda x: x.getProperty("source_title"))\n
# now add an extra line for total\n
person = portal.person_module.newContent(temp_object=1, source_title="Total", **total_project_dict)\n
listbox_line_list.append(person)\n
\n
item_title_dict = {}\n
if item_url_set:\n
  for item in portal.portal_catalog(portal_type="Research Item", relative_url=list(item_url_set), select_list=["title","relative_url"]):\n
    item_title_dict[item.relative_url] = item.title\n
  item_title_dict["None"] = "undefined"\n
\n
# define which property to display in columns\n
column_list = [("source_title", "Worker"),\n
                ("None", "Undefined"), ]\n
for item_url, item_title in sorted(item_title_dict.items(), key=lambda url_title: url_title[1]):\n
  if item_url != \'None\':\n
    column_list.append((item_url, item_title))\n
column_list.append(("total", "Total"))\n
\n
# define which script to display url in columns\n
column_url_script_list = []\n
for item_url in item_title_dict.keys():\n
  column_url_script_list.append((item_url, "getColumnUrl"))\n
\n
context = context.asContext(column_list=column_list,\n
                            at_date=at_date,\n
                            from_date=from_date,\n
                            simulation_state_list=simulation_state_list,\n
                            column_url_script_list=column_url_script_list,\n
                            ledger=ledger,\n
                            multiplier=multiplier,\n
                            listbox_line_list=listbox_line_list)\n
                            \n
if batch_mode:\n
  return context\n
return context.ResearchItemModule_viewResearchSummaryReportData()\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>at_date=None, from_date=None, simulation_state_list=None, ledger=None, multiplier=None, batch_mode=False, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>ResearchItemModule_callResearchSummaryReport</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
