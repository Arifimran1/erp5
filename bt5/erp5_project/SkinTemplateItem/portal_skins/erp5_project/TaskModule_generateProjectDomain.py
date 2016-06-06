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

restrictedTraverse = context.getPortalObject().restrictedTraverse\n
domain_list = []\n
\n
def Task_getRelatedSourceProject(depth, parent_relative_url=None):\n
  if depth == 0:\n
    task_uid_list  = context.portal_selections.getSelectionUidList(context=context, selection_name=\'task_module_selection\')\n
    project_result = context.portal_catalog(portal_type=["Project", "Project Line"],\n
                                            source_project_related_uid=task_uid_list,\n
                                            select_expression=\'portal_type, relative_url, id, title\',\n
                                            sort_on = ((\'title\',\'ascending\'),))\n
  else:\n
    project_result = context.portal_catalog(portal_type=["Project Line", "Project Milestones"],\n
                                            select_expression=\'portal_type, relative_url, id, title\',\n
                                            parent_relative_url=parent_relative_url,\n
                                            sort_on = ((\'title\',\'ascending\'),))\n
  # use a dict to store catalog result\n
  project_dict = {}\n
  category_dict = {}\n
  project_list = []\n
  append = project_list.append\n
  for x in project_result:\n
    key = x.uid\n
    if key not in project_dict:\n
      project_dict[key] = None\n
      category_dict = {\'relative_url\':x.relative_url, \n
                       \'portal_type\':x.portal_type,\n
                       \'id\':x.id,\n
                       \'title\':x.title,\n
                       \'uid\':x.uid}\n
      append(category_dict)\n
    \n
  return project_list\n
\n
def Task_getRelatedSourceProjectCategory(depth):\n
  parent_relative_url = None\n
  if depth > 0:\n
    parent_relative_url = parent.getMembershipCriterionCategoryList()\n
  project_list = Task_getRelatedSourceProject(depth=depth,\n
                                              parent_relative_url=parent_relative_url)\n
\n
  category_dict = {}\n
  category_list = []\n
  append = category_list.append\n
\n
  for project in project_list:\n
    if project[\'portal_type\'] == \'Project\' or depth > 0:\n
      category = project\n
    else:\n
      # XXX here we need to get the project line object to get the explanation value\n
      project_line_value = restrictedTraverse(project[\'relative_url\'])\n
      explanation_value = project_line_value.getExplanationValue()\n
      category = {\'relative_url\':explanation_value.getRelativeUrl(), \n
                  \'portal_type\':explanation_value.getPortalType(),\n
                  \'id\':explanation_value.getId(),\n
                  \'title\':explanation_value.getTitle(),\n
                  \'uid\':explanation_value.getUid()}\n
    key = category[\'uid\']\n
    if key not in category_dict:\n
      category_dict[key] = None\n
      append(category)\n
\n
  return category_list\n
\n
category_list = Task_getRelatedSourceProjectCategory(depth)\n
\n
for category in category_list:\n
  domain = parent.generateTempDomain(id = \'sub\' + category[\'id\'] )\n
  domain.edit(title = category[\'title\'],\n
              membership_criterion_base_category = (\'source_project\', ), \n
              membership_criterion_category = (category[\'relative_url\'],),\n
              domain_generator_method_id = script.id,\n
              uid = category[\'uid\'])\n
                \n
  domain_list.append(domain)\n
return domain_list\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>depth, parent, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>TaskModule_generateProjectDomain</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
