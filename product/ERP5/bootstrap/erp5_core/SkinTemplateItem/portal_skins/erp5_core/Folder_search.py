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

request = container.REQUEST\n
\n
from Products.ZSQLCatalog.SQLCatalog import Query, NegatedQuery, ComplexQuery\n
\n
def sorted(seq):\n
  seq = [x for x in seq]\n
  seq.sort()\n
  return seq\n
\n
# Convert mapping from request.form into something the catalog can understand\n
# This script uses ad-hoc values that are understood by\n
# Folder_viewSearchDialog: x_value_ and x_usage_ are used to remember what was\n
# the entered value, and what was the usage.\n
\n
# Note that we don\'t use queries, because we want to let the catalog filter out\n
# ignored parameters by itself.\n
\n
usage_map = dict(min=\'>=\',\n
                 max=\'<\',\n
                 ngt=\'<=\',\n
                 nlt=\'>\',)\n
\n
new_mapping = dict(ignore_hide_rows=1)\n
query_list = []\n
left_join_list = []\n
for key in sorted(request.form.keys()):\n
  # we use sorted to make sure x_search_key appears before x\n
  value = request.form[key]\n
  # to remove unnecessary None value\n
  if value is None:\n
    request.form.pop(key)\n
    continue\n
  \n
  # workaround the bogus case where a value is passed ?value=None\n
  if value == \'None\':\n
    value = None\n
\n
  # remove Formulator markers\n
  if key.startswith(\'default_field_\') or key.startswith(\'field_\'):\n
    request.form.pop(key)\n
    continue\n
\n
  if key.endswith(\'_search_key\') and value:\n
    real_key = key[:-11]\n
    new_mapping[real_key] = dict(query=new_mapping[real_key], key=value)\n
\n
  elif key.endswith(\'_usage_\') and value:\n
    request.form.pop(key)\n
    real_key = key[:-7]\n
    new_mapping[\'%s_value_\' % real_key] = new_mapping[real_key]\n
    new_mapping[\'%s_usage_\' % real_key] = value\n
    # TODO: this is a quick and dirty implementation of what should be done by\n
    # Query.asSearchTextExpression. Instead of keeping \'%s_value_\' and \'%s_usage_\',\n
    # we\'ll simply keep the query.\n
    new_mapping[real_key] = \'%s %s\' % (usage_map[value], new_mapping[real_key])\n
\n
  else:\n
    if request.form.get(\'%s_is_excluded_\' % key):\n
      # Build a negated query\n
      nq_kw = {\'strict_%s\' % key : value}\n
      q_kw = {key : None}\n
      left_join_list.append(key) \n
      left_join_list.append(\'strict_%s\' % key)\n
      query_list.append(ComplexQuery(NegatedQuery(Query(**nq_kw)), Query(**q_kw), operator="OR"))\n
      new_mapping[key] = ""\n
      new_mapping["dialog_%s" %(key,)] = value\n
      new_mapping["dialog_excluded_%s" %(key,)] = True\n
    else:\n
      if request.form.get(\'%s_is_strict_\' % key):\n
        new_mapping[\'strict_%s\' % key] = value\n
        new_mapping[\'dialog_strict_%s\' % key] = value\n
      else:\n
        new_mapping[key] = value\n
        new_mapping[\'dialog_%s\' % key] = value\n
\n
      \n
new_mapping["query"] = ComplexQuery(query_list)\n
new_mapping[\'left_join_list\'] = left_join_list\n
\n
# set selection parameters\n
container.portal_selections.setSelectionParamsFor(selection_name, new_mapping)\n
\n
request.form.update(new_mapping)\n
return getattr(context, form_id)(request)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>form_id=\'\', selection_name=\'\', **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Folder_search</string> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
