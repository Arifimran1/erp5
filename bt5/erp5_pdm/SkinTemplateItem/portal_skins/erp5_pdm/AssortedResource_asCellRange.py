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

#  from Products.ERP5Type.Utils import cartesianProduct\n
# XXX unable to import cartesianProduct, so, I copied the code (Romain)\n
def cartesianProduct(list_of_list):\n
  if len(list_of_list) == 0:\n
    return [[]]\n
  result = []\n
  head = list_of_list[0]\n
  tail = list_of_list[1:]\n
  product = cartesianProduct(tail)\n
  for v in head:\n
    for p in product:\n
      result += [[v] + p]\n
  return result\n
\n
\n
line = []\n
column = []\n
tab = []\n
\n
transformation = context.getParentValue()\n
\n
\n
\n
\n
\n
#    security.declareProtected(Permissions.AccessContentsInformation, \'getQLineItemList\')\n
#    def getQLineItemList(self, display_id=\'getTitle\', base=1, current_category=None):\n
#      """\n
#      """\n
#      line_category = self._getSortedBaseCategoryList(self.getQVariationBaseCategoryList())[0]\n
#      #LOG(\'getQLineItemList\', 0, "%s" % str(line_category))\n
#      if line_category is None:\n
#        result = [(None,\'\')]\n
#      else:\n
#        result = self.getVariationRangeCategoryItemList(base_category_list = [line_category],\n
#                                                        display_id=display_id,\n
#                                                        base=base,\n
#                                                        current_category=current_category)\n
#      #LOG(\'getQLineItemList\', 10, "%s" % str(result))\n
#      return result\n
\n
#    security.declareProtected(Permissions.AccessContentsInformation, \'getQColumnItemList\')\n
#    def getQColumnItemList(self, display_id=\'getTitle\', base=1, current_category=None):\n
#      """\n
#      """\n
#      column_category = self._getSortedBaseCategoryList(self.getQVariationBaseCategoryList())[1]\n
#      #LOG(\'getQColumnItemList\', 0, "%s" % str(column_category))\n
#      if column_category is None:\n
#        result = [(None,\'\')]\n
#      else:\n
#        result = self.getVariationRangeCategoryItemList(base_category_list = [column_category],\n
#                                                        display_id=display_id,\n
#                                                        base=base,\n
#                                                        current_category=current_category)\n
#      #LOG(\'getQColumnItemList\', 0, "%s" % str(result))\n
#      return result\n
\n
#    security.declareProtected(Permissions.AccessContentsInformation, \'getQTabItemList\')\n
#    def getQTabItemList(self, display_id=\'getTitle\', base=1, current_category=None):\n
#      """\n
#        Returns a list of items which can be used as index for\n
#        each tab of a matrix or to define a cell range.\n
#      """\n
#      tab_category_list = self._getSortedBaseCategoryList(self.getQVariationBaseCategoryList())[2:]\n
#      tab_category_item_list_list = []\n
#      for tab_category in tab_category_list:\n
#        tab_category_item_list = self.getVariationRangeCategoryItemList(base_category_list = [tab_category],\n
#                                                                        display_id=display_id,\n
#                                                                        base=base,\n
#                                                                        current_category=current_category)\n
#        tab_category_item_list_list.append(tab_category_item_list)\n
#      transformation = self.getParentValue()\n
#      transformation_category_item_list = transformation.getVariationCategoryItemList(\n
#                                                          display_id=display_id,\n
#                                                          base=base,\n
#                                                          current_category=current_category)\n
#      tab_category_item_list_list.append(transformation_category_item_list)\n
#      if len(tab_category_item_list_list) > 0:\n
#        product_list = cartesianProduct(tab_category_item_list_list)\n
#        result = []\n
#        for item_list in product_list:\n
#          value_list = []\n
#          label_list = []\n
#          for item in item_list:\n
#            value_list.append(item[0])\n
#            label_list.append(item[1])\n
#          result.append((value_list, label_list))\n
#      else:\n
#        result = [(None,\'\')]\n
#      return result\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
\n
# base_cell_id possible value: \'quantity\', \'variation\'\n
base_cell_id = \'quantity\'\n
get_variation_base_category_method_dict = {\n
  \'quantity\': \'getQVariationBaseCategoryList\',\n
  \'variation\': \'getVVariationBaseCategoryList\'\n
}\n
\n
\n
#  from Products.ERP5Type.Utils import cartesianProduct\n
# XXX unable to import cartesianProduct, so, I copied the code (Romain)\n
def cartesianProduct(list_of_list):\n
  if len(list_of_list) == 0:\n
    return [[]]\n
  result = []\n
  head = list_of_list[0]\n
  tail = list_of_list[1:]\n
  product = cartesianProduct(tail)\n
  for v in head:\n
    for p in product:\n
      result += [[v] + p]\n
  return result\n
\n
\n
line = []\n
column = []\n
tab = []\n
\n
transformation = context.getParentValue()\n
\n
# Those value are define on property sheet of portal type\n
line_base_category = transformation.getVariationBaseCategoryLine()\n
column_base_category = transformation.getVariationBaseCategoryColumn()\n
\n
# Calculate line and column\n
for axe, axe_base_category in [(line, line_base_category),(column, column_base_category)]:\n
  clist = []\n
  #if axe_base_category in context.getVVariationBaseCategoryList():\n
  if axe_base_category in getattr(context, get_variation_base_category_method_dict[base_cell_id])():\n
\n
    if matrixbox == 1:\n
      # XXX matrixbox is right_display (not as listfield) => invert display and value in item\n
      axe += map(lambda x: (x[1],x[0]), transformation.getVariationCategoryItemList(base_category_list = (axe_base_category,) ) )\n
    else:\n
      axe += transformation.getVariationCategoryList(base_category_list = (axe_base_category,) )\n
\n
# Calculate tab\n
# We can only display 3 dimension, so, we use a cartesian product to decrease matrix dimension\n
base_category_list = transformation.getVariationBaseCategoryList()\n
base_category = []\n
\n
for c in base_category_list:\n
  if not c in (line_base_category, column_base_category):\n
    #if c in context.getVVariationBaseCategoryList():\n
    if c in getattr(context, get_variation_base_category_method_dict[base_cell_id])():\n
      if matrixbox == 1:\n
        # XXX matrixbox is right_display (not as listfield) => invert display and value in item\n
        base_category += [ map(lambda x: (x[1],x[0]), transformation.getVariationCategoryItemList(base_category_list = (c,) )) ]\n
      else:\n
        base_category += [ transformation.getVariationCategoryList(base_category_list = (c,) ) ]\n
\n
if len(base_category) > 0:\n
  # Then make a cartesian product\n
  # to calculate all possible combinations\n
  clist = cartesianProduct(base_category)\n
  \n
  # XXX is it possible to remove repr ?\n
  for c in clist:\n
    if matrixbox == 1:\n
      # XXX matrixbox is right display\n
      tab.append(  ( repr(map(lambda x: x[0], c)) , repr(map(lambda x: x[1], c)) ) )\n
    else:\n
      tab.append( repr(c) )\n
\n
# Try fill line first, then column, and after tab\n
for i in range(2):\n
  if line == []:\n
    tmp = line \n
    line = column\n
    column = tmp\n
    tmp = None\n
\n
  if column == []:\n
    tmp = column\n
    column = tab\n
    tab = tmp\n
    tmp = None\n
\n
cell_range = [line, column, tab]\n
return cell_range\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>matrixbox=0, base_id=None</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>AssortedResource_asCellRange</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
