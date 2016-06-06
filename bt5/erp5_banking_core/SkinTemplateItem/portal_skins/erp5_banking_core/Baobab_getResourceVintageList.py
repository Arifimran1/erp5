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
            <value> <string>from Products.ERP5Type.Cache import CachingMethod\n
\n
def getResourceVintageList(banknote=0, coin=0):\n
    variation_list = {}\n
    if banknote and not coin:\n
     portal_type_list = ["Banknote",]\n
    elif coin and not banknote:\n
     portal_type_list = ["Coin",]\n
    else:\n
      portal_type_list = ["Banknote", "Coin"]\n
\n
    for resource in context.currency_cash_module.objectValues():\n
      #context.log("Baobab_getResourcevintageList", "resource.getPriceCurrency() = %s, resource.getPortalType() = %s, portal_type_list = %s" %(resource.getPriceCurrency(),resource.getPortalType(), portal_type_list))\n
      if resource.getPriceCurrency() ==  "currency_module/%s" %(context.Baobab_getPortalReferenceCurrencyID(),) and resource.getPortalType() in portal_type_list:\n
        for variation in resource.getVariationList():\n
          variation_list[variation] = 1\n
    #context.log("variation_list", variation_list)\n
    return variation_list.keys()\n
\n
\n
getResourceVintageList = CachingMethod(getResourceVintageList, \n
                                       id=\'Baobab_getResourceVintageList\', \n
                                       cache_factory="erp5_ui_long")\n
\n
return getResourceVintageList(banknote, coin)\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>banknote=0, coin=0</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Baobab_getResourceVintageList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
