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

from DateTime import DateTime\n
from Products.ZSQLCatalog.SQLCatalog import SimpleQuery\n
\n
# params\n
section_title = \'My Organisation\'\n
business_process = \'business_process_module/erp5_default_business_process\'\n
portal = context.getPortalObject()\n
accounting_module = portal.accounting_module\n
year = 2005\n
\n
total_receivable_quantity = 0\n
\n
# if the previous test didn\'t change input data, no need to recreate content\n
current_script_data_id = \'%s_month_count_%s\' % (\n
                                 month_count, script.getId())\n
if accounting_module.getProperty(\'current_content_script\',\n
                                \'\') == current_script_data_id:\n
  return "Accounting Transactions Created."\n
\n
# first, cleanup accounting module\n
# XXX should be done in an external script / tool, because we have to\n
# workaround some security checks\n
if 1:\n
  accounting_module.manage_delObjects(list(accounting_module.objectIds()))\n
\n
# XXX copy & paste \n
def getAccountByTitle(title):\n
  account_list = [x.getObject().getRelativeUrl() for x in\n
    portal.portal_catalog(portal_type=\'Account\',\n
                          title=SimpleQuery(title=title, comparison_operator=\'=\'))]\n
  assert len(account_list) == 1, \\\n
        \'%d account with title "%s"\' % (len(account_list), title)\n
  return account_list[0]\n
\n
def getOrganisationByTitle(title):\n
  document_list = [x.getObject().getRelativeUrl() for x in\n
    portal.portal_catalog(portal_type=\'Organisation\',\n
                          title=SimpleQuery(title=title, comparison_operator=\'=\'))]\n
  assert len(document_list) == 1, \\\n
        \'%d organisation with title "%s"\' % (len(document_list), title)\n
  return document_list[0]\n
section = getOrganisationByTitle(section_title)\n
\n
def getCurrencyByReference(reference):\n
  document_list = [x.getObject().getRelativeUrl() for x in\n
    portal.portal_catalog(portal_type=\'Currency\',\n
                          reference=reference)]\n
  assert len(document_list) == 1, \\\n
      \'%d currency with reference "%s"\' % (len(document_list), reference)\n
  return document_list[0]\n
euro_resource = getCurrencyByReference(\'EUR\')\n
\n
def getBankAccountByTitle(title):\n
  document_list = [x.getObject().getRelativeUrl() for x in\n
    portal.portal_catalog(portal_type=\'Bank Account\',\n
                          title=SimpleQuery(title=title, comparison_operator=\'=\'))]\n
  assert len(document_list) == 1, \\\n
      \'%d Bank Account with title "%s"\' % (len(document_list), title)\n
  return document_list[0]\n
\n
for month in range(1, month_count + 1):\n
  for day in range(1, 29):\n
    vat_rate = .1\n
    for client_title, amount  in ((\'Client 1\', 1000 * day),\n
                                  (\'Client 2\', 2000 * day) ):\n
      tr = accounting_module.newContent(\n
            portal_type=\'Sale Invoice Transaction\',\n
            title=\'%s Sale Invoice\' % client_title,\n
            source_section=section,\n
            destination_section=getOrganisationByTitle(client_title),\n
            created_by_builder=1,\n
            start_date=DateTime(year, month, day),\n
            stop_date=DateTime(year, month, day),\n
            resource=euro_resource,\n
            specialise=business_process,\n
        )\n
      receivable_qty = -(amount * (1 + vat_rate))\n
      total_receivable_quantity += receivable_qty\n
      tr.newContent(portal_type=\'Sale Invoice Transaction Line\',\n
                    source=getAccountByTitle(\'Receivable\'),\n
                    destination=getAccountByTitle(\'Payable\'),\n
                    quantity=receivable_qty,\n
      )\n
      tr.newContent(portal_type=\'Sale Invoice Transaction Line\',\n
                    source=getAccountByTitle(\'Collected VAT 10%\'),\n
                    destination=getAccountByTitle(\'Refundable VAT 10%\'),\n
                    quantity=amount * vat_rate,\n
      )\n
      tr.newContent(portal_type=\'Sale Invoice Transaction Line\',\n
                    source=getAccountByTitle(\'Goods Sales\'),\n
                    destination=getAccountByTitle(\'Goods Purchase\'),\n
                    quantity=amount,\n
      )\n
      tr.stop()\n
\n
      # payment\n
      ptr = accounting_module.newContent(\n
            portal_type=\'Payment Transaction\',\n
            title=\'Payment from %s Sale Invoice\' % client_title,\n
            source_section=section,\n
            source_payment=getBankAccountByTitle(\'My default bank account\'),\n
            destination_section=getOrganisationByTitle(client_title),\n
            created_by_builder=1,\n
            start_date=DateTime(year, month, day, 01, 01) + 10,\n
            stop_date=DateTime(year, month, day, 01, 01) + 10,\n
            causality_value=tr,\n
            resource=euro_resource,\n
        )\n
\n
      ptr.newContent(portal_type=\'Accounting Transaction Line\',\n
                    source=getAccountByTitle(\'Receivable\'),\n
                    quantity=(amount * (1 + vat_rate)),\n
      )\n
      ptr.newContent(portal_type=\'Accounting Transaction Line\',\n
                    source=getAccountByTitle(\'Bank\'),\n
                    quantity= - (amount * (1 + vat_rate)),\n
      )\n
      ptr.stop()\n
\n
      if not keep_grouping_reference:\n
        for line in ptr.getMovementList(\n
                          portal_type=ptr.getPortalAccountingMovementTypeList()):\n
          if line.getGroupingReference():\n
             line.activate(after_path_and_method_id=(\n
                  (ptr.getPath(), line.getPath()),\n
                    (\'recursiveImmediateReindexObject\',\n
                      \'immediateReindexObject\')),\n
             ).AccountingTransactionLine_resetGroupingReference()\n
\n
\n
accounting_module.setProperty(\'current_content_script\',\n
                              current_script_data_id)\n
\n
# test depends on this\n
return "Accounting Transactions Created."\n
# vim: syntax=python\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>month_count=1, no_creation_need=0, keep_grouping_reference=0</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>AccountingZuite_createAccountingTransactionListSalesAndPayments</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
