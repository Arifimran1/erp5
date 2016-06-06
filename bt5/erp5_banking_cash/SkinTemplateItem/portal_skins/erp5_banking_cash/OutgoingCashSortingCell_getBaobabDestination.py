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

if context.getSource() is None:\n
  return None\n
\n
site_letter = context.getSourceValue().getCodification()[0].lower()\n
site = context.Baobab_getVaultSite(context.getSource()).getRelativeUrl()\n
cash_status = context.getCashStatus()\n
# possible cash status : cancelled, to_sort, valid\n
emission_letter = context.getEmissionLetter()\n
\n
resource_portal_type = context.getResourceValue().getPortalType()\n
if resource_portal_type == \'Banknote\':\n
  if emission_letter == "not_defined":\n
    if cash_status == "to_sort":\n
      # banknote letter \'not defined\' / a trier -> caisse source\n
      source = context.getSource()\n
      if not \'ventilation\' in source:\n
        return \'%s/caveau/auxiliaire/encaisse_des_billets_et_monnaies\' %(site,)\n
      else:\n
        return \'%s/caveau/auxiliaire/%s\' %(site, \'/\'.join(source.split(\'/\')[-2:]))\n
    else:\n
      # This case is/must be protected by a constraint: a document containing a\n
      # line matching this condition must not get validated.\n
      # XXX: Maybe we should return None here instead of raising.\n
      raise Exception, \'Should not be here\'\n
  elif emission_letter == site_letter:\n
    if cash_status == "valid":\n
      # banknote \'valid\' from same country -> caisse de reserve / billets et monnaies\n
      return \'%s/caveau/reserve/encaisse_des_billets_et_monnaies\' %(site,)\n
    else:\n
      # banknote of any other status from same country -> caisse auxiliaire / billets et monnaies\n
      return \'%s/caveau/auxiliaire/encaisse_des_billets_et_monnaies\' %(site,)\n
  elif emission_letter == "mixed":\n
    # banknote letter \'mixed\' -> caisse auxiliaire / encaisse externe\n
    return \'%s/caveau/auxiliaire/encaisse_des_externes\' %(site,)\n
  else: # emission_letter != site_letter\n
    # external banknote  -> caisse auxiliaire / encaisse externe\n
    return \'%s/caveau/auxiliaire/encaisse_des_externes\' %(site,)\n
else:\n
  # Coin\n
  if cash_status == "valid":\n
    return \'%s/caveau/reserve/encaisse_des_billets_et_monnaies\' %(site,)\n
  else:\n
    return \'%s/caveau/auxiliaire/encaisse_des_billets_et_monnaies\' %(site,)\n
     \n
  \n
\n
# if emission_letter!=\'not_defined\' and not (emission_letter in site_letter):\n
#   return \'%s/caveau/auxiliaire/encaisse_des_externes\' %(site,)\n
# elif cash_status == "mixed":\n
#   return \'%s/caveau/auxiliaire/encaisse_des_externes\' %(site,)\n
# elif emission_letter==\'not_defined\':\n
#   # remaining banknote which are not sorted yet, or cancelled one\n
#   if not \'ventilation\' in context.getSource():\n
#     return \'%s/caveau/auxiliaire/encaisse_des_billets_et_monnaies\' %(site,)\n
#   else:\n
#     if context.getCashStatus() in ("to_sort",):\n
#       return context.getSource()\n
#       #return \'%s/caveau/auxiliaire/encaisse_des_externes\' %(site,)\n
#     else:\n
#       # take classification into account here\n
#       source_list = context.getSource().split(\'/\')\n
#       return \'%s/caveau/auxiliaire/%s\' %(site,\'/\'.join(source_list[-2:]))\n
# elif (context.getCashStatus() in (\'to_sort\', \'cancelled\')) and emission_letter in site_letter:\n
#   return \'%s/caveau/auxiliaire/encaisse_des_billets_et_monnaies\' %(site,)\n
# elif emission_letter in site_letter:\n
#   return \'%s/caveau/reserve/encaisse_des_billets_et_monnaies\' %(site,)\n
# else:\n
#   return \'%s/caveau/auxiliaire/encaisse_des_externes\' %(site,)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>*args, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>OutgoingCashSortingCell_getBaobabDestination</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
