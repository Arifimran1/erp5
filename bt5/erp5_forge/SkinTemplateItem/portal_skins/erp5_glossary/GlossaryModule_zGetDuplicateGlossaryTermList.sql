<?xml version="1.0"?>
<ZopeData>
  <record id="1" aka="AAAAAAAAAAE=">
    <pickle>
      <global name="SQL" module="Products.ZSQLMethods.SQL"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>_col</string> </key>
            <value>
              <list>
                <dictionary>
                  <item>
                      <key> <string>name</string> </key>
                      <value> <string>path</string> </value>
                  </item>
                  <item>
                      <key> <string>null</string> </key>
                      <value> <int>0</int> </value>
                  </item>
                  <item>
                      <key> <string>type</string> </key>
                      <value> <string>t</string> </value>
                  </item>
                  <item>
                      <key> <string>width</string> </key>
                      <value> <int>27</int> </value>
                  </item>
                </dictionary>
                <dictionary>
                  <item>
                      <key> <string>name</string> </key>
                      <value> <string>uid</string> </value>
                  </item>
                  <item>
                      <key> <string>null</string> </key>
                      <value> <int>0</int> </value>
                  </item>
                  <item>
                      <key> <string>type</string> </key>
                      <value> <string>l</string> </value>
                  </item>
                  <item>
                      <key> <string>width</string> </key>
                      <value> <int>10</int> </value>
                  </item>
                </dictionary>
                <dictionary>
                  <item>
                      <key> <string>name</string> </key>
                      <value> <string>num_of_duplicates</string> </value>
                  </item>
                  <item>
                      <key> <string>null</string> </key>
                      <value> <int>0</int> </value>
                  </item>
                  <item>
                      <key> <string>type</string> </key>
                      <value> <string>l</string> </value>
                  </item>
                  <item>
                      <key> <string>width</string> </key>
                      <value> <int>1</int> </value>
                  </item>
                </dictionary>
              </list>
            </value>
        </item>
        <item>
            <key> <string>allow_simple_one_argument_traversal</string> </key>
            <value>
              <none/>
            </value>
        </item>
        <item>
            <key> <string>arguments_src</string> </key>
            <value> <string>selection_params=""</string> </value>
        </item>
        <item>
            <key> <string>cache_time_</string> </key>
            <value> <int>0</int> </value>
        </item>
        <item>
            <key> <string>class_file_</string> </key>
            <value> <string>ZSQLCatalog.zsqlbrain</string> </value>
        </item>
        <item>
            <key> <string>class_name_</string> </key>
            <value> <string>ZSQLBrain</string> </value>
        </item>
        <item>
            <key> <string>connection_hook</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>connection_id</string> </key>
            <value> <string>erp5_sql_connection</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>GlossaryModule_zGetDuplicateGlossaryTermList</string> </value>
        </item>
        <item>
            <key> <string>max_cache_</string> </key>
            <value> <int>100</int> </value>
        </item>
        <item>
            <key> <string>max_rows_</string> </key>
            <value> <int>1000</int> </value>
        </item>
        <item>
            <key> <string>src</string> </key>
            <value> <string encoding="cdata"><![CDATA[

<dtml-let query="portal_catalog.buildSQLQuery(query=portal_catalog.getSecurityQuery(**selection_params), **selection_params)">\n
\n
select distinct\n
  catalog.path, catalog.uid, count(*)-1 as num_of_duplicates\n
from\n
  <dtml-in prefix="table" expr="query[\'from_table_list\']">\n
    <dtml-if "table_key not in (\'catalog\',)">\n
      <dtml-var table_item> AS <dtml-var table_key>,\n
    </dtml-if>\n
  </dtml-in>\n
  catalog\n
where\n
  catalog.portal_type=\'Glossary Term\'\n
  and catalog.validation_state in (\'draft\', \'validated\')\n
  and related_language_title_category.category_strict_membership = 1\n
  and related_business_field_title_category.category_strict_membership = 1\n
  <dtml-if "query[\'where_expression\']">\n
    AND <dtml-var "query[\'where_expression\']">\n
  </dtml-if>\n
group by\n
  catalog.reference, related_language_title_category.category_uid, related_business_field_title_category.category_uid\n
having\n
  count(*) > 1\n
<dtml-if "query[\'order_by_expression\']">\n
  order by <dtml-var "query[\'order_by_expression\']">\n
</dtml-if>\n
</dtml-let>

]]></string> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
