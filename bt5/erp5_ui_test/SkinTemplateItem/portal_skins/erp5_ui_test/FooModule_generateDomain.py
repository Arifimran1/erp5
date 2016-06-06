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
            <value> <string>"""Special domains for foo"""\n
domain_list = []\n
\n
if depth == 0:\n
  url = \'foo_category\'\n
else:\n
  url = parent.getProperty(\'membership_criterion_category\')\n
\n
#context.log(script.id, \'parent = %r, context = %r, url = %r, depth = %r\' % (parent, context, url, depth))\n
\n
category_list = context.portal_categories.getCategoryValue(url).contentValues()\n
for category in category_list:\n
  domain = parent.generateTempDomain(id = category.getId())\n
  domain.edit(title = category.getTitle(),\n
              membership_criterion_base_category = (\'foo_category\',), \n
              membership_criterion_category = (category.getRelativeUrl(),),\n
              domain_generator_method_id = script.id,\n
              uid = category.getUid())\n
\n
  domain_list.append(domain)\n
\n
#context.log(script.id, \'parent = %r, category_list = %r, domain_list = %r\' % (parent, category_list, domain_list))\n
\n
return domain_list\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>depth, parent, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>FooModule_generateDomain</string> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string>Generate a domain</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
