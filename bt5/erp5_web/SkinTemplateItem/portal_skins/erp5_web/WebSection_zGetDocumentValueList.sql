<?xml version="1.0"?>
<ZopeData>
  <record id="1" aka="AAAAAAAAAAE=">
    <pickle>
      <global name="SQL" module="Products.ZSQLMethods.SQL"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>_Use_Database_Methods_Permission</string> </key>
            <value>
              <list>
                <string>Anonymous</string>
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
            <value> <string>language\r\n
all_languages\r\n
kw</string> </value>
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
            <value>
              <none/>
            </value>
        </item>
        <item>
            <key> <string>connection_id</string> </key>
            <value> <string>erp5_sql_connection</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>WebSection_zGetDocumentValueList</string> </value>
        </item>
        <item>
            <key> <string>max_cache_</string> </key>
            <value> <int>100</int> </value>
        </item>
        <item>
            <key> <string>max_rows_</string> </key>
            <value> <int>0</int> </value>
        </item>
        <item>
            <key> <string>src</string> </key>
            <value> <string encoding="cdata"><![CDATA[

<dtml-let query="buildSQLQuery(query=portal_catalog.getSecurityQuery(**kw), **kw)"\n
          selection_domain="kw.get(\'selection_domain\', None)"\n
          selection_report="kw.get(\'selection_report\', None)">\n
\n
  <dtml-comment>\n
    Currently, there is no other choice to implement this method as an SQL catalog until SQLCatalog\n
    can support more features which are needed here. Once SQLCatalog supports those feature,\n
    this method should be refactored to use catalog only.\n
\n
     The subquery is named catalog to prevent use another LEFT JOIN.\n
  </dtml-comment>\n
\n
  SELECT\n
    catalog.*\n
  FROM\n
    (\n
      SELECT DISTINCT\n
        catalog.uid,\n
        catalog.path,\n
        catalog.int_index,\n
        catalog.modification_date,\n
        catalog.reference,\n
        catalog.creation_date,\n
        catalog.title,\n
        CONCAT(CASE my_versioning.language\n
                   WHEN <dtml-sqlvar language type="string"> THEN \'4\'\n
                   WHEN \'\' THEN \'3\'\n
                   WHEN \'en\' THEN \'2\'\n
                   ELSE \'1\' END,\n
               my_versioning.version) AS priority\n
        <dtml-if "query[\'select_expression\']">,<dtml-var "query[\'select_expression\']"></dtml-if>\n
      FROM\n
        <dtml-in prefix="table" expr="query[\'from_table_list\']">\n
          <dtml-var table_item> AS <dtml-var table_key>,\n
        </dtml-in>\n
        <dtml-if selection_domain>\n
          <dtml-var "portal_selections.buildSQLJoinExpressionFromDomainSelection(selection_domain)">,\n
        </dtml-if>\n
        <dtml-if selection_report>\n
          <dtml-var "portal_selections.buildSQLJoinExpressionFromDomainSelection(selection_report)">,\n
        </dtml-if>\n
        versioning AS my_versioning\n
      WHERE\n
        my_versioning.uid = catalog.uid\n
        <dtml-if "query[\'where_expression\']">\n
          AND <dtml-var "query[\'where_expression\']">\n
        </dtml-if>\n
        <dtml-if selection_domain>\n
          AND <dtml-var "portal_selections.buildSQLExpressionFromDomainSelection(selection_domain)">\n
        </dtml-if>\n
        <dtml-if selection_report>\n
          AND <dtml-var "portal_selections.buildSQLExpressionFromDomainSelection(selection_report)">\n
        </dtml-if>\n
        <dtml-if all_languages>\n
        <dtml-else>\n
          AND my_versioning.language IN (<dtml-sqlvar language type="string">, \'\')\n
        </dtml-if>\n
\n
      ORDER BY\n
        priority DESC\n
\n
    ) AS catalog\n
\n
  <dtml-if "query[\'group_by_expression\']">\n
    GROUP BY <dtml-var "query[\'group_by_expression\']">\n
  </dtml-if>\n
\n
  ORDER BY <dtml-var "query[\'order_by_expression\'] or \'priority DESC\'">\n
\n
  <dtml-if "query[\'limit_expression\']">\n
    LIMIT <dtml-var "query[\'limit_expression\']">\n
  <dtml-else>\n
    LIMIT 1000\n
  </dtml-if>\n
\n
</dtml-let>\n


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
