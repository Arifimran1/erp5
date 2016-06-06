<?xml version="1.0"?>
<ZopeData>
  <record id="1" aka="AAAAAAAAAAE=">
    <pickle>
      <tuple>
        <tuple>
          <string>Products.ZSQLMethods.SQL</string>
          <string>SQL</string>
        </tuple>
        <none/>
      </tuple>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>__ac_local_roles__</string> </key>
            <value>
              <none/>
            </value>
        </item>
        <item>
            <key> <string>_arg</string> </key>
            <value>
              <object>
                <klass>
                  <global name="Args" module="Shared.DC.ZRDB.Aqueduct"/>
                </klass>
                <tuple/>
                <state>
                  <dictionary>
                    <item>
                        <key> <string>_data</string> </key>
                        <value>
                          <dictionary/>
                        </value>
                    </item>
                    <item>
                        <key> <string>_keys</string> </key>
                        <value>
                          <list/>
                        </value>
                    </item>
                  </dictionary>
                </state>
              </object>
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
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>cache_time_</string> </key>
            <value> <int>0</int> </value>
        </item>
        <item>
            <key> <string>class_file_</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>class_name_</string> </key>
            <value> <string></string> </value>
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
            <value> <string>z_create_compatibility</string> </value>
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
            <value> <string># Host:\n
# Database: test\n
# Table: \'compatibility\'\n
#\n
CREATE TABLE `compatibility` (\n
  `uid` BIGINT UNSIGNED NOT NULL,\n
  `Creator` varchar(255) default \'\',\n
  `Date` datetime default \'0000-00-00 00:00:00\',\n
  `PrincipiaSearchSource` text,\n
  `SearchableText` text,\n
  `CreationDate` datetime default \'0000-00-00 00:00:00\',\n
  `EffectiveDate` datetime default \'0000-00-00 00:00:00\',\n
  `ExpiresDate` datetime default \'0000-00-00 00:00:00\',\n
  `ModificationDate` datetime default \'0000-00-00 00:00:00\',\n
  `Type` varchar(255) default \'\',\n
  `bobobase_modification_time` datetime default \'0000-00-00 00:00:00\',\n
  `created` datetime default \'0000-00-00 00:00:00\',\n
  `effective` datetime default \'0000-00-00 00:00:00\',\n
  `expires` datetime default \'0000-00-00 00:00:00\',\n
  `getIcon` varchar(255) default \'\',\n
  `in_reply_to` varchar(255) default \'\',\n
  `modified` datetime default \'0000-00-00 00:00:00\',\n
  `review_state` varchar(255) default \'\',\n
  `summary` text,\n
  PRIMARY KEY  (`uid`),\n
  KEY `Type` (`Type`),\n
  KEY `review_state` (`review_state`)\n
) TYPE=ndb;\n
</string> </value>
        </item>
        <item>
            <key> <string>template</string> </key>
            <value>
              <object>
                <klass>
                  <global name="SQL" module="Shared.DC.ZRDB.DA"/>
                </klass>
                <none/>
                <state>
                  <dictionary>
                    <item>
                        <key> <string>__name__</string> </key>
                        <value> <string encoding="cdata"><![CDATA[

<string>

]]></string> </value>
                    </item>
                    <item>
                        <key> <string>_vars</string> </key>
                        <value>
                          <dictionary/>
                        </value>
                    </item>
                    <item>
                        <key> <string>globals</string> </key>
                        <value>
                          <dictionary/>
                        </value>
                    </item>
                    <item>
                        <key> <string>raw</string> </key>
                        <value> <string># Host:\n
# Database: test\n
# Table: \'compatibility\'\n
#\n
CREATE TABLE `compatibility` (\n
  `uid` BIGINT UNSIGNED NOT NULL,\n
  `Creator` varchar(255) default \'\',\n
  `Date` datetime default \'0000-00-00 00:00:00\',\n
  `PrincipiaSearchSource` text,\n
  `SearchableText` text,\n
  `CreationDate` datetime default \'0000-00-00 00:00:00\',\n
  `EffectiveDate` datetime default \'0000-00-00 00:00:00\',\n
  `ExpiresDate` datetime default \'0000-00-00 00:00:00\',\n
  `ModificationDate` datetime default \'0000-00-00 00:00:00\',\n
  `Type` varchar(255) default \'\',\n
  `bobobase_modification_time` datetime default \'0000-00-00 00:00:00\',\n
  `created` datetime default \'0000-00-00 00:00:00\',\n
  `effective` datetime default \'0000-00-00 00:00:00\',\n
  `expires` datetime default \'0000-00-00 00:00:00\',\n
  `getIcon` varchar(255) default \'\',\n
  `in_reply_to` varchar(255) default \'\',\n
  `modified` datetime default \'0000-00-00 00:00:00\',\n
  `review_state` varchar(255) default \'\',\n
  `summary` text,\n
  PRIMARY KEY  (`uid`),\n
  KEY `Type` (`Type`),\n
  KEY `review_state` (`review_state`)\n
) TYPE=ndb;\n
</string> </value>
                    </item>
                  </dictionary>
                </state>
              </object>
            </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
