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

# params\n
section_title = \'My Organisation\'\n
business_process = \'business_process_module/erp5_default_business_process\'\n
portal = context.getPortalObject()\n
accounting_module = portal.accounting_module\n
from DateTime import DateTime\n
from Products.ZSQLCatalog.SQLCatalog import SimpleQuery\n
year = 2005\n
\n
# if the previous test didn\'t change input data, no need to recreate content\n
current_script_data_id = \'%s_month_count_%s\' % (\n
                                 month_count, script.getId())\n
if accounting_module.getProperty(\'current_content_script\',\n
                                \'\') == current_script_data_id:\n
  return "Accounting Transactions Created."\n
\n
\n
# first, cleanup accounting module\n
# XXX should be done in an external script / tool, because we have to\n
# workaround some security checks\n
if 1:\n
  for module_id in [\'accounting_module\',\n
                    \'sale_packing_list_module\',\n
                    \'portal_simulation\', ]:\n
    module = portal[module_id]\n
    module.manage_delObjects(list(module.objectIds()))\n
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
def getPersonByTitle(title):\n
  document_list = [x.getObject().getRelativeUrl() for x in\n
    portal.portal_catalog(portal_type=\'Person\',\n
                          title=SimpleQuery(title=title, comparison_operator=\'=\'))]\n
  assert len(document_list) == 1, \\\n
        \'%d person with title "%s"\' % (len(document_list), title)\n
  return document_list[0]\n
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
  day = 1\n
  vat_rate = .1\n
  for client_title, amount  in ((\'John Smith\', 1000),):\n
    tr = accounting_module.newContent(\n
          portal_type=\'Sale Invoice Transaction\',\n
          title=\'%s Sale Invoice\' % client_title,\n
          source_section=section,\n
          destination_section=getPersonByTitle(client_title),\n
          created_by_builder=1,\n
          start_date=DateTime(year, month, day),\n
          stop_date=DateTime(year, month, day),\n
          specialise=business_process,\n
          resource=euro_resource,\n
      )\n
    tr.newContent(portal_type=\'Sale Invoice Transaction Line\',\n
                  source=getAccountByTitle(\'Receivable\'),\n
                  destination=getAccountByTitle(\'Payable\'),\n
                  quantity=-(amount * (1 + vat_rate)))\n
    tr.newContent(portal_type=\'Sale Invoice Transaction Line\',\n
                  source=getAccountByTitle(\'Collected VAT 10%\'),\n
                  destination=getAccountByTitle(\'Refundable VAT 10%\'),\n
                  quantity=amount * vat_rate)\n
    tr.newContent(portal_type=\'Sale Invoice Transaction Line\',\n
                  source=getAccountByTitle(\'Goods Sales\'),\n
                  destination=getAccountByTitle(\'Goods Purchase\'),\n
                  quantity=amount)\n
    tr.stop()\n
    tr.setSourceReference(\'source_reference\')\n
    tr.setDestinationReference(\'destination_reference\')\n
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
            <value> <string>month_count=1</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>AccountingZuite_createAccountingTransactionListWithPersons</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
