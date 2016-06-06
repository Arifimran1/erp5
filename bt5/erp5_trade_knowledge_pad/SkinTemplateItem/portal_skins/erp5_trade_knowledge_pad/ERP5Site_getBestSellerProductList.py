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
            <value> <string>portal = context.getPortalObject()\n
from DateTime import DateTime\n
request = container.REQUEST\n
\n
preferences = {}\n
if not box_relative_url:\n
  box_relative_url = request.get(\'box_relative_url\', None)\n
if box_relative_url:\n
  box = portal.restrictedTraverse(box_relative_url)\n
  preferences = box.KnowledgeBox_getDefaultPreferencesDict()\n
\n
mode = preferences.get(\'mode\', \'total_price\')\n
if mode not in (\'total_price\', \'total_quantity\'):\n
  context.log("Unknown mode %s" % mode)\n
  return []\n
from_date = preferences.get(\'from_date\', DateTime(2010, 1, 1))\n
at_date = preferences.get(\'from_date\', DateTime(2011, 12, 31))\n
section_category = preferences.get(\'section_category\', \'group/my_group\')\n
if portal.portal_categories.restrictedTraverse(section_category, None) is None:\n
  return []\n
\n
limit = preferences.get(\'limit\', 5)\n
method = preferences.get(\'method\', \'getFutureInventoryList\')\n
if method not in (\'getFutureInventoryList\', \'getAvailableInventoryList\', \'getCurrentInventoryList\'):\n
  context.log("Unknown method %s" % method)\n
  return []\n
\n
product_list = []\n
\n
for brain in getattr(portal.portal_simulation, method)(\n
                          resource_portal_type="Product",\n
                          section_category=section_category,\n
                          from_date=from_date,\n
                          at_date=at_date,\n
                          portal_type=portal.getPortalSaleTypeList(), group_by_resource=1\n
                        # sort_on=((mode, \'ASC\'), ), limit=limit, # XXX not working ???\n
 ):\n
  resource = portal.portal_catalog.getObject(brain.resource_uid)\n
  total_price = (brain.total_price or 0) * -1\n
  total_quantity = (brain.total_quantity or 0) * -1\n
  product_list.append(resource.asContext(total_price=total_price, total_quantity=total_quantity))\n
\n
product_list.sort(key=lambda x: -1 * getattr(x, mode))\n
\n
return product_list[:limit]\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>box_relative_url="", **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>ERP5Site_getBestSellerProductList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
