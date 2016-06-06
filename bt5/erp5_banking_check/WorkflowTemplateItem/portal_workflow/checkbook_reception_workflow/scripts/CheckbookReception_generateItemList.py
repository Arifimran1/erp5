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

from Products.DCWorkflow.DCWorkflow import ValidationFailed\n
from Products.ERP5Type.Message import Message\n
\n
transaction = state_change[\'object\']\n
\n
# Check getBaobabSource and getBaobabDestination\n
transaction.Base_checkBaobabSourceAndDestination()\n
\n
# Check that all lines do not define existing checks or checkbooks\n
transaction.CheckbookReception_checkOrCreateItemList(check=1)\n
\n
# Start activities for each line\n
confirm_check = transaction.isImported()\n
transaction.CheckbookReception_checkOrCreateItemList(create=1,\n
                      confirm_check=confirm_check)\n
\n
\n
#from Products.DCWorkflow.DCWorkflow import ValidationFailed\n
#transaction = state_change[\'object\']\n
#\n
## Check getBaobabSource and getBaobabDestination\n
#transaction.Base_checkBaobabSourceAndDestination()\n
#\n
#portal = transaction.getPortalObject()\n
#portal_activities = portal.portal_activities\n
#line_list = transaction.objectValues()\n
#encountered_check_identifiers_dict = {}\n
#\n
#def getReference(reference):\n
#  """\n
#    Convert a reference into an int.\n
#  """\n
#  # First convert to float to avoid failing to convert if reference = \'1.0\'\n
#  return int(float(reference))\n
#\n
#def generateReference(reference, original_reference):\n
#  """\n
#    Convert an int into a reference of correct length\n
#  """\n
#  reference = str(reference)\n
#  return \'%s%s\' % (\'0\' * (len(original_reference) - len(reference)), reference)\n
#\n
#def validateTravelerCheckReferenceFormat(traveler_check_reference):\n
#  """\n
#    Check provided traveler_check_reference format\n
#  """\n
#  if len(traveler_check_reference) != 10:\n
#    raise ValueError, \'Traveler check reference must be 10-char long.\'\n
#  int(traveler_check_reference[4:])\n
#\n
#def getTravelerCheckReferenceNumber(traveler_check_reference):\n
#  """\n
#    Extract traveler check reference number\n
#  """\n
#  validateTravelerCheckReferenceFormat(traveler_check_reference)\n
#  return int(traveler_check_reference[4:])\n
#\n
#def getTravelerCheckReferencePrefix(traveler_check_reference):\n
#  """\n
#    Extract traveler check reference prefix\n
#  """\n
#  validateTravelerCheckReferenceFormat(traveler_check_reference)\n
#  return traveler_check_reference[:4]\n
#\n
#def generateTravelerCheckReference(number, original_traveler_check_reference):\n
#  """\n
#    Generate a traveler check reference from an existing reference (to\n
#    extract its prefix) and a new numerical value.\n
#  """\n
#  if not same_type(number, 0):\n
#    raise ValueError, \'Traveler check number must be only numeric.\'\n
#  if len(str(number)) > 6:\n
#    raise ValueError, \'Traveler check number representation length must not exceed 6 char.\'\n
#  prefix = getTravelerCheckReferencePrefix(original_traveler_check_reference)\n
#  return \'%s%06d\' % (prefix, number)\n
#\n
#def assertReferenceMatchListEmpty(match_list):\n
#  """\n
#    Check that the list is empty, otherwise gather all conflicting references and display them in the error message.\n
#    TODO: make the error message Localizer-friendly\n
#  """\n
#  if len(match_list) > 0:\n
#    matched_reference_list = []\n
#    for match in match_list:\n
#      matched_reference_list.append(match.getReference())\n
#    raise ValidationFailed, \'The following references are already allocated : %s\' % (matched_reference_list, )\n
#\n
#def checkReferenceListUniqueness(reference_list, model, destination_payment_uid):\n
#  """\n
#    Check each given reference not to already exist.\n
#  """\n
#  if destination_payment_uid is None:\n
#    match_list = portal.portal_catalog(portal_type=\'Check\', reference=reference_list, resource_relative_url=model)\n
#  else:\n
#    match_list = portal.portal_catalog(portal_type=\'Check\', reference=reference_list, destination_payment_uid=destination_payment_uid, resource_relative_url=model)\n
#  assertReferenceMatchListEmpty(match_list)\n
#  for reference in reference_list:\n
#    tag = \'check_%s_%s_%s\' % (model, destination_payment_uid, reference)\n
#    if encountered_check_identifiers_dict.has_key(tag) or portal_activities.countMessageWithTag(tag) != 0:\n
#      raise ValidationFailed, \'The following references are already allocated : %s\' % ([reference, ], )\n
#\n
#def checkReferenceUniqueness(reference, model, destination_payment_uid):\n
#  """\n
#    Check the given reference not to already exist.\n
#  """\n
#  checkReferenceListUniqueness([reference, ], model, destination_payment_uid)\n
#\n
#start_date = transaction.getStartDate()\n
#destination = transaction.getDestination()\n
#\n
#for line in line_list:\n
#  quantity = line.getQuantity()\n
#  resource = line.getResourceValue()\n
#  reference_range_min = line.getReferenceRangeMin()\n
#\n
#  # We will look where we should create as many items\n
#  # as necessary and construct by the same time\n
#  # the aggregate list that we will store on the line\n
#  resource_portal_type = resource.getPortalType()\n
#  if resource_portal_type == \'Checkbook Model\':\n
#    is_checkbook = True\n
#    module = portal.checkbook_module\n
#    model = resource.getComposition()\n
#    # XXX: portal_type value is hardcoded because I don\'t want to get the\n
#    # portaltype on each created object as it will always be the same.\n
#    # We need a method to get the default content portaltype on a Folder.\n
#    check_amount = line.getCheckAmount()\n
#    check_quantity = int(portal.restrictedTraverse(check_amount).getQuantity())\n
#    reference_to_int = getReference\n
#    int_to_reference = generateReference\n
#  else:\n
#    is_checkbook = False\n
#    module = portal.check_module\n
#    model = resource.getRelativeUrl()\n
#    # XXX: portal_type value is hardcoded, see XXX above.\n
#    if resource_portal_type == \'Check Model\' and resource.isFixedPrice():\n
#      reference_to_int = getTravelerCheckReferenceNumber\n
#      int_to_reference = generateTravelerCheckReference\n
#    else:\n
#      reference_to_int = getReference\n
#      int_to_reference = generateReference\n
#\n
#  if resource.getAccountNumberEnabled():\n
#    destination_payment_value = line.getDestinationPaymentValue()\n
#    destination_payment_value.serialize()\n
#    destination_payment_uid = destination_payment_value.getUid()\n
#    destination_trade = line.getDestinationTrade()\n
#  else:\n
#    destination_payment_value = None\n
#    destination_payment_uid = None\n
#\n
#  aggregate_list = []\n
#  for i in xrange(quantity):\n
#    item = module.newContent()\n
#    item.setDestination(destination)\n
#    if destination_payment_value is not None:\n
#      item.setDestinationPaymentValue(destination_payment_value)\n
#      item.setDestinationTrade(destination_trade)\n
#    if is_checkbook:\n
#      last_reference_value = reference_to_int(reference_range_min) + check_quantity - 1\n
#      reference_list = [int_to_reference(x, reference_range_min) for x in range(reference_to_int(reference_range_min), last_reference_value + 1)]\n
#      checkReferenceListUniqueness(reference_list, model, destination_payment_uid)\n
#      reference_range_max = int_to_reference(last_reference_value, reference_range_min)\n
#      item.setReferenceRangeMax(reference_range_max)\n
#      item.setReferenceRangeMin(reference_range_min)\n
#      item.setResourceValue(resource)\n
#      item.setStartDate(start_date)\n
#      item.setTitle(\'%s - %s\' % (reference_range_min, reference_range_max))\n
#      item.setCheckAmount(check_amount)\n
#      destination_section = item.getDestinationSection()\n
#      for j in reference_list:\n
#        tag = \'check_%s_%s_%s\' % (model, destination_payment_uid, j)\n
#        encountered_check_identifiers_dict[tag] = None\n
#        check = item.newContent(portal_type=\'Check\', title=j, activate_kw={\'tag\': tag})\n
#        check.setDestination(destination_section)\n
#        check.setStartDate(start_date)\n
#        check.setReference(j)\n
#        check.setResource(model)\n
#    else:\n
#      checkReferenceUniqueness(reference_range_min, model, destination_payment_uid)\n
#      item.setReference(reference_range_min)\n
#      item.setResource(model)\n
#      item.setTitle(reference_range_min)\n
#      if len(resource.objectValues()) > 0:\n
#        item_type = line.getCheckTypeValue()\n
#        item.setPrice(item_type.getPrice())\n
#        item.setPriceCurrency(line.getPriceCurrency())\n
#      last_reference_value = reference_to_int(reference_range_min)\n
#      tag = \'check_%s_%s_%s\' % (model, destination_payment_uid, reference_range_min)\n
#      encountered_check_identifiers_dict[tag] = None\n
#      # Trigger a dummy activity just to avoi dbeing able to create that check multiple times in the same checkbook reception\n
#      item.activate(tag=tag).getUid()\n
#    # update reference_range_min for the next pass\n
#    reference_range_min = int_to_reference(last_reference_value + 1, reference_range_min)\n
#    # I (seb) think this is a big mistake\n
#    #if item.getPortalType()==\'Check\':\n
#    #  portal.portal_workflow.doActionFor(item,\'confirm_action\',\n
#    #                                     wf_id=\'check_workflow\')\n
#    aggregate_list.append(item)\n
#\n
#  # Finally set the aggregate list on the line\n
#  line.setAggregateValueList(aggregate_list)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>state_change</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>CheckbookReception_generateItemList</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
