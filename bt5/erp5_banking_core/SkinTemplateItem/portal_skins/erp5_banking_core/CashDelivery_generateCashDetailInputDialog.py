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

# listbox is not passed at the first time when this script is called.\n
# when the user clicks on the Update button, listbox is passed, and\n
# the contents must be preserved in the form.\n
#\n
# rendering_vault : the vault that we want to render, if specified we will use\n
#                   getInventory in order to automatically full the fast input\n
\n
from Products.ERP5Type.Cache import CachingMethod\n
portal = context.getPortalObject()\n
precision = 0\n
if listbox is None:\n
  # This is the first time.\n
  cash_status_list          = cash_detail_dict[\'cash_status_list\']\n
  emission_letter_list      = cash_detail_dict[\'emission_letter_list\']\n
  variation_list            = cash_detail_dict[\'variation_list\']\n
  operation_currency        = cash_detail_dict[\'operation_currency\']\n
  line_portal_type          = cash_detail_dict[\'line_portal_type\']\n
  column_base_category      = cash_detail_dict[\'column_base_category\']\n
  read_only                 = cash_detail_dict[\'read_only\']\n
  check_float               = int(cash_detail_dict.get(\'check_float\', 1))\n
  currency_cash_portal_type = cash_detail_dict[\'currency_cash_portal_type\']\n
\n
  if fast_input_title is None:\n
    # Module getTranslatedTitle does not return a translated string.\n
    # Borrow code from ERP5Site_getModuleItemList to achieve hand translation.\n
    # XXX: Pass title value as a list to work around an encoding bug in TextWidget:\n
    #  It renders given value as a list of str, and casting to str throws an error when\n
    #  encountering UTF-8 chars. This cast is not called when provided value is a tuple\n
    # or a list...\n
    fast_input_title = [\'%s - %s\' % \\\n
      (context.getPortalObject().Localizer.erp5_ui.gettext(context.getParentValue().getTitle()),\n
       context.getSourceReference())]\n
  if \'target_total_price\' not in kw:\n
    target_total_price = context.getSourceTotalAssetPrice()\n
  else:\n
    target_total_price = kw.pop(\'target_total_price\')\n
\n
  # If use_inventory is passed, use that value. Otherwise, assume False.\n
  # use_inventory = cash_detail_dict.get(\'use_inventory\', False)\n
  # assume this is always false as we don\'t need to distinguish this anymore\n
  use_inventory = False\n
\n
  if currency_cash_portal_type is None:\n
    currency_cash_portal_type = (\'Banknote\',\'Coin\')\n
\n
  # If not passed, get the category IDs from the database.\n
  if cash_status_list is None:\n
    cash_status_list = list(context.portal_categories.cash_status.objectIds())\n
  if emission_letter_list is None :\n
    emission_letter_list = list(context.portal_categories.emission_letter.objectIds())\n
  if variation_list is None :\n
    variation_list = list(context.portal_categories.variation.objectIds())\n
\n
  def generic_prioritized_sort(a, b, priority_list):\n
    if a == b:\n
      return 0\n
    a_in_list = a in priority_list\n
    b_in_list = b in priority_list\n
    if a_in_list and (not b_in_list):\n
      return -1\n
    elif (not a_in_list) and b_in_list:\n
      return 1\n
    elif (not b_in_list) or (a > b):\n
      return -1\n
    elif (not a_in_list) or (a < b):\n
      return 1\n
\n
  prioritized_banknote_emission_letter_list = context.Baobab_getUserEmissionLetterList()\n
  prioritized_coin_cash_status_list = prioritized_coin_emission_letter_list = [\'not_defined\']\n
\n
  def banknote_emission_letter_sort(a, b):\n
    return generic_prioritized_sort(a, b, prioritized_banknote_emission_letter_list)\n
\n
  def coin_emission_letter_sort(a, b):\n
    return  generic_prioritized_sort(a, b, prioritized_coin_emission_letter_list)\n
\n
  def coin_cash_status_sort(a, b):\n
    return  generic_prioritized_sort(a, b, prioritized_coin_cash_status_list)\n
\n
  # Make sure to use separate instances of the lists.\n
  banknote_cash_status_list = cash_status_list\n
  coin_cash_status_list = [x for x in cash_status_list]\n
  banknote_emission_letter_list = emission_letter_list\n
  coin_emission_letter_list = [x for x in emission_letter_list]\n
\n
  # Sort the lists for consistency.\n
  banknote_cash_status_list.sort()\n
  banknote_emission_letter_list.sort(banknote_emission_letter_sort)\n
  coin_cash_status_list.sort(coin_cash_status_sort)\n
  coin_emission_letter_list.sort(coin_emission_letter_sort)\n
  variation_list.sort()\n
\n
  # Get the currency cash objects for a given currency.\n
  currency = \'currency_module/%s\' % operation_currency\n
  # This is very bad to call catalog each time, it is the bottleneck,\n
  # So we will add a caching method here\n
  def getCurrencyCashRelativeUrlList(currency=None, currency_cash_portal_type=None):\n
    result = context.portal_catalog(portal_type = currency_cash_portal_type)\n
    currency_cash_list = [x.getObject() for x in result \n
                          if x.getObject().getPriceCurrency() == currency \n
                          and len(x.getObject().getVariationList())>0]\n
    return [x.getRelativeUrl() for x in currency_cash_list]\n
  getCurrencyCashRelativeUrlList = CachingMethod(getCurrencyCashRelativeUrlList, \n
                               id=(\'CashDelivery_generateCashDetailInputDialog\', \n
                                              \'getCurrencyCashRelativeUrlList\'), \n
                               cache_factory=\'erp5_ui_long\')\n
  currency_cash_url_list = getCurrencyCashRelativeUrlList(currency=currency,\n
                              currency_cash_portal_type=currency_cash_portal_type)\n
  currency_cash_list = [portal.restrictedTraverse(x) for x in currency_cash_url_list]\n
\n
  # This is the same thing, but by using catalog, so this is not nice at all\n
  #result = context.portal_catalog(portal_type = currency_cash_portal_type)\n
  #currency_cash_list = [x.getObject() for x in result if x.getObject().getPriceCurrency() == currency and len(x.getObject().getVariationList())>0]\n
\n
\n
  # If only one variation is specified, we want to display a part of cash currencies which\n
  # exists in this variation (creation year, such as 2003).\n
  if len(variation_list) == 1:\n
    new_currency_cash_list = []\n
    variation = variation_list[0]\n
    for currency_cash in currency_cash_list:\n
      if variation in currency_cash.getVariationList():\n
        new_currency_cash_list.append(currency_cash)\n
    currency_cash_list = new_currency_cash_list\n
\n
  currency_cash_list = context.Base_sortCurrencyCashList(currency_cash_list)\n
\n
  # Get the axis information based on the specified column base category.\n
  # axis_list_dict contains the lists of objects, while axis_dict contains\n
  # the base categories.\n
  if column_base_category == \'cash_status\':\n
    axis_list_dict = {\n
                        \'column\': cash_status_list,\n
                        \'line1\' : emission_letter_list,\n
                        \'line2\' : variation_list\n
                     }\n
    axis_dict      = {\n
                        \'column\': \'cash_status\',\n
                        \'line1\': \'emission_letter\',\n
                        \'line2\': \'variation\'\n
                     }\n
  elif column_base_category == \'emission_letter\':\n
    axis_list_dict = {\n
                        \'column\': emission_letter_list,\n
                        \'line1\' : cash_status_list,\n
                        \'line2\' : variation_list\n
                     }\n
    axis_dict      = {\n
                        \'column\': \'emission_letter\',\n
                        \'line1\': \'cash_status\',\n
                        \'line2\': \'variation\'\n
                     }\n
  else:\n
    # column_base_category == variation\n
    axis_list_dict = {\n
                        \'column\': variation_list,\n
                        \'line1\' : emission_letter_list,\n
                        \'line2\' : cash_status_list\n
                     }\n
    axis_dict      = {\n
                        \'column\': \'variation\',\n
                        \'line1\': \'emission_letter\',\n
                        \'line2\': \'cash_status\'\n
                     }\n
\n
  total_price = 0\n
  listbox = []\n
\n
  inventory_dict = {}\n
  if rendering_vault is not None and len(context.objectValues(portal_type=line_portal_type))==0:\n
    # build the list of ressources for this vault\n
    inventory_list = context.CounterModule_getVaultTransactionList(vault=rendering_vault, at_date=context.getStartDate())\n
    # build the dict of ressources for this vault, the dict\n
    # allow to parse the list only one time\n
    for inventory in inventory_list:\n
      resource_id = inventory.resource_id\n
      resource_list = inventory_dict.setdefault(resource_id, [])\n
      resource_list.append(inventory)\n
\n
  for currency_cash in currency_cash_list:\n
    if currency_cash.getPortalType() == \'Coin\':\n
      cash_status_list = coin_cash_status_list\n
      emission_letter_list = coin_emission_letter_list\n
    else:\n
      cash_status_list = banknote_cash_status_list\n
      emission_letter_list = banknote_emission_letter_list\n
    # Search if the current object contains a line with a given portal type.\n
    currency_cash_id = currency_cash.getId()\n
    cash_delivery_line = context.CashDelivery_searchLineByResource(currency_cash_id, line_portal_type)\n
    # This variable counts the number of lines added for this currency cash.\n
    line_number = 0\n
\n
    if cash_delivery_line is not None or len(inventory_dict.get(currency_cash_id, ()))>0:\n
      # If a line exists for this cash currency, add lines into the listbox according to\n
      # the currency information.\n
      #context.log("cash_delivery_line", "cash_delivery_line = %s, currency = %s, type = %s" %(cash_delivery_line, currency_cash, line_portal_type))\n
      currency_dict = None\n
      resource_price = currency_cash.getBasePrice()\n
\n
      # Collect cells according to the categories.\n
      cell_dict_dict = {}\n
      cell_list = []\n
      if cash_delivery_line is not None:\n
        cell_list = cash_delivery_line.getCellValueList()\n
      else:\n
        # the result is inside the currency_dict\n
        cell_list = inventory_dict[currency_cash_id]\n
      for cell in cell_list:\n
        category1 = cell.getProperty(axis_dict[\'line1\']).split(\'/\')[-1]\n
        category2 = cell.getProperty(axis_dict[\'line2\']).split(\'/\')[-1]\n
        column_category = cell.getProperty(axis_dict[\'column\']).split(\'/\')[-1]\n
        key = (category1, category2)\n
        #context.log(str((key, axis_dict[\'column\'], column_category, cell.getVariation())), cell)\n
        cell_dict_dict.setdefault(key, {})[column_category] = cell\n
\n
\n
\n
      # Sort the keys to obtain a consistent behavior.\n
      key_list = cell_dict_dict.keys()\n
      key_list.sort(lambda a, b: cmp(a[0], b[0]) or cmp(a[1], b[1]))\n
\n
      # Look at all the cells of the dictionary to add lines.\n
      for key in key_list:\n
        cell_dict = cell_dict_dict[key]\n
        total_quantity = 0\n
        currency_dict = None\n
        for counter, column in enumerate(axis_list_dict[\'column\']):\n
          cell = cell_dict.get(column, None)\n
          #context.log("Cashdelivery_...", "cell = %s, column = %s"%(cell, column))\n
          if cell is None:\n
            continue\n
\n
          # Get the quantity of the cell, and skip it if not significant.\n
          if use_inventory:\n
            quantity = cell.getInventory()\n
          else:\n
            quantity = cell.getProperty(\'quantity\')\n
          if not quantity:\n
            continue\n
\n
          if currency_dict is None:\n
            currency_dict = {\n
              \'resource_translated_title\': currency_cash.getTranslatedTitle(),\n
              \'resource_id\':               currency_cash.getId(),\n
              axis_dict[\'line1\']:          key[0],\n
              axis_dict[\'line2\']:          key[1],\n
            }\n
\n
          currency_dict[\'column%d\' % (counter + 1)] = quantity\n
          total_quantity += quantity\n
        #context.log("currency_dict", currency_dict)\n
        if currency_dict is not None:\n
          price = total_quantity * resource_price\n
          currency_dict[\'price\'] = price\n
          total_price += price\n
          line_number += 1\n
          # set default value for column\n
          for counter, column in enumerate(axis_list_dict[\'column\']):\n
            col_key = \'column%d\' % (counter + 1)\n
            if not currency_dict.has_key(col_key):\n
              currency_dict[col_key] = 0\n
          currency_dict[\'number_line_to_add\'] = 0\n
          listbox.append(currency_dict)\n
\n
    if line_number == 0:\n
      # Add an empty line only if no line is present for this cash currency.\n
      currency_dict = {\n
        \'resource_translated_title\': currency_cash.getTranslatedTitle(),\n
        \'resource_id\': currency_cash.getId(),\n
        \'emission_letter\': emission_letter_list[0],\n
        \'cash_status\': cash_status_list[0],\n
        \'variation\': variation_list[0],\n
        \'additional_line_number\': 0,\n
        \'price\': 0,\n
        \'number_line_to_add\': 0\n
      }\n
      # set default value for column\n
      for counter, column in enumerate(axis_list_dict[\'column\']):\n
        currency_dict[\'column%d\' % (counter + 1)] = 0\n
      listbox.append(currency_dict)\n
      \n
  if check_float == 0:\n
    precision = 4\n
  other_parameter_list = (operation_currency, line_portal_type, read_only, column_base_category, use_inventory, fast_input_title[0], target_total_price, check_float)\n
  context.Base_updateDialogForm(listbox=listbox\n
                                , calculated_price=total_price\n
                                , empty_line_number=0\n
                                , cash_status_list = cash_status_list\n
                                , emission_letter_list = emission_letter_list\n
                                , variation_list = variation_list\n
                                , other_parameter = other_parameter_list\n
                                , fast_input_title=fast_input_title\n
                                , target_total_price=target_total_price\n
                                , precision=precision\n
                                , )\n
\n
  return context.asContext(  context=None\n
                             , portal_type=context.getPortalType()\n
                             , calculated_price=total_price\n
                             , cash_status_list = cash_status_list\n
                             , emission_letter_list = emission_letter_list\n
                             , variation_list = variation_list\n
                             , other_parameter = other_parameter_list\n
                             , fast_input_title=fast_input_title\n
                             , target_total_price=target_total_price\n
                             , precision=precision\n
                             ).CashDetail_viewLineFastInputForm(**kw)\n
\n
\n
else :\n
\n
  # we want to update the listbox\n
  cash_status_list          = kw[\'cash_status_list\']\n
  emission_letter_list      = kw[\'emission_letter_list\']\n
  variation_list            = kw[\'variation_list\']\n
  other_parameter           = kw[\'other_parameter\']\n
  operation_currency        = other_parameter[0]\n
  line_portal_type          = other_parameter[1]\n
  read_only                 = other_parameter[2]\n
  column_base_category      = other_parameter[3]\n
  use_inventory             = other_parameter[4]\n
  fast_input_title          = other_parameter[5]\n
  target_total_price        = other_parameter[6]\n
  check_float               = int(other_parameter[7])\n
\n
  # we don\'t update anything in read only mode\n
  if read_only == "True":\n
    context.Base_updateDialogForm(listbox=listbox, empty_line_number=0)\n
    return context.asContext(context=None, portal_type=context.getPortalType() ,**kw ).CashDetail_viewLineFastInputForm(**kw)\n
\n
  # get the maximum number of line allowed for a variation\n
  if column_base_category == \'cash_status\':\n
    columne_base_list = cash_status_list\n
    max_lines =len(emission_letter_list) * len(variation_list)\n
  elif column_base_category == \'emission_letter\':\n
    column_base_list = emission_letter_list\n
    max_lines =len(cash_status_list) * len(variation_list)\n
  else:\n
    column_base_list = variation_list\n
    max_lines =len(cash_status_list) * len(emission_letter_list)\n
\n
  line_counter_dict = {}\n
  # compute number of exisiting lines for a resource\n
  for line in listbox:\n
    resource_key = line[\'resource_id\']\n
    if line_counter_dict.has_key(resource_key):\n
      line_counter_dict[resource_key] = line_counter_dict[resource_key] + 1\n
    else:\n
      line_counter_dict[resource_key] = 1\n
\n
  total_price = 0\n
  new_line_list = []\n
  next_listbox_key = max([int(x.get(\'listbox_key\', 0)) for x in listbox]) + 1\n
  # browse line to determine new lines to add\n
  for line in listbox:\n
    # must get the resource\n
    resource_id = line[\'resource_id\']\n
    # This is a huge performance problem to call many times the catalog\n
    # for each fast input !!!!\n
    #resource_list = context.portal_catalog(portal_type = (\'Banknote\',\'Coin\') ,id = resource_id)\n
    #resource_price = resource_list[0].getObject().getBasePrice()\n
    resource_value = context.currency_cash_module[resource_id]\n
    resource_price = resource_value.getObject().getBasePrice()\n
    line[\'resource_translated_title\'] = resource_value.getTranslatedTitle()\n
    # get the number of lines to add\n
    if line.has_key(\'number_line_to_add\'):\n
      lines_to_add = int(line[\'number_line_to_add\'])\n
    else:\n
      lines_to_add = 0\n
    line[\'number_line_to_add\'] = 0\n
    # remove the key\n
    #del line[\'listbox_key\']\n
    # create new line\n
    for num in xrange(lines_to_add):\n
      # make sure we don\'t have too many lines\n
      if line_counter_dict[resource_id] <= max_lines:\n
        line_counter_dict[resource_id] = line_counter_dict[resource_id] + 1\n
        new_line = line.copy()\n
        new_line[\'listbox_key\'] = next_listbox_key\n
        next_listbox_key += 1\n
        # set default quantity to 0\n
        for column_nb in xrange(1, len(column_base_list) + 1):\n
          new_line[\'column%s\' %(str(column_nb))] = 0\n
        new_line[\'price\'] = 0\n
        new_line_list.append(new_line)\n
    # compute the price for existing line\n
    quantity = 0\n
    for column_nb in xrange(1, len(column_base_list) + 1):\n
      if line[\'column%s\' %(str(column_nb))] != \'\' and line[\'column%s\' %(str(column_nb))] is not None:\n
        quantity += line[\'column%s\' %(str(column_nb))]\n
    line[\'price\'] = resource_price * quantity\n
    total_price += line[\'price\']\n
    # add current line\n
    new_line_list.append(line)\n
\n
  if check_float == 0:\n
   precision = 4\n
  listbox = new_line_list\n
  context.Base_updateDialogForm(  listbox=listbox\n
                                  , calculated_price=total_price\n
                                  , empty_line_number=0\n
                                  , fast_input_title=fast_input_title\n
                                  , precision=precision\n
                                  , target_total_price=target_total_price)\n
\n
  return context.asContext(  context=None\n
                             , portal_type=context.getPortalType()\n
                             , calculated_price=total_price\n
                             , fast_input_title=fast_input_title\n
                             , target_total_price=target_total_price\n
                             , precision=precision\n
                             ,**kw\n
                             ).CashDetail_viewLineFastInputForm(**kw)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>listbox=None,cash_detail_dict=None, rendering_vault=None, fast_input_title=None, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>CashDelivery_generateCashDetailInputDialog</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
