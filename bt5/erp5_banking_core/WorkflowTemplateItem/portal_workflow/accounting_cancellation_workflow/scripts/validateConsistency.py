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
#context.checkUserPermission(state_change)\n
\n
site = transaction.getSite()\n
date = transaction.getStartDate()\n
# No need to check counter date, only accounting date\n
transaction.Base_checkConsistency()\n
transaction.Baobab_checkAccountingDateOpen(site=site, date=date)\n
\n
\n
# Check some properties of document\n
price = transaction.getSourceTotalAssetPrice()\n
if price is None or price <= 0:\n
  msg = Message(domain=\'ui\', message=\'Amount is not valid.\')\n
  raise ValidationFailed, (msg,)\n
if transaction.getSiteValue() is None:\n
  msg = Message(domain=\'ui\', message=\'Sorry, no site defined.\')\n
  raise ValidationFailed, (msg,)\n
if transaction.getResource() is None:\n
  msg = Message(domain=\'ui\', message=\'No resource defined.\')\n
  raise ValidationFailed, (msg,)\n
\n
# Check the source bank account.\n
source_bank_account = transaction.getSourcePaymentValue()\n
\n
# test we have account transfer line defined\n
nb_transfer_line = len(transaction.objectValues(portal_type=\'Accounting Cancellation Line\'))\n
if  nb_transfer_line == 0:\n
  msg = Message(domain=\'ui\', message=\'You must add line before validating the operation\')\n
  raise ValidationFailed, (msg,)\n
\n
# only one line can be defined with SICA/STAR, on order as it can be cancel or reject later\n
#if transaction.getExternalSoftware() in (\'sica\', \'star\') and nb_transfer_line != 1:\n
#  msg = Message(domain=\'ui\', message=\'You can defined only one lines when using SICA\')\n
#  raise ValidationFailed, (msg,)  \n
\n
# Check each line\n
total_line_price = 0\n
for line in transaction.objectValues(portal_type=\'Accounting Cancellation Line\'):\n
  total_line_price += abs(line.getQuantity())\n
  # First check there is something defined on line\n
  if line.getSourcePaymentReference(None) is None and \\\n
         line.getSourceSection() is None:\n
    msg = Message(domain=\'ui\', message="No account defined on line.")\n
    raise ValidationFailed, (msg,)\n
  # check we don\'t have both account and accounting code defined\n
  if line.getDestinationPayment(None) is not None \\\n
        and line.getDestinationSection() is not None:\n
    msg = Message(domain=\'ui\', message="You can\'t defined account and accounting code on line.")\n
    raise ValidationFailed, (msg,)\n
  # check that at least destination_payment or destination_section is defined\n
  if line.getDestinationPayment() is None and \\\n
      line.getDestinationSection() is None:\n
    msg = Message(domain=\'ui\', message="Destination account is not defined.")\n
    raise ValidationFailed, (msg,)\n
  # Index the banking operation line so it impacts account position\n
  if line.getSourcePaymentReference() not in (None, \'\'):\n
    context.BankingOperationLine_index(line, source=1)\n
\n
if total_line_price != transaction.getSourceTotalAssetPrice():\n
  msg = Message(domain=\'ui\', message="Total price doesn\'t match between line and document.")\n
  raise ValidationFailed, (msg,)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>state_change</string> </value>
        </item>
        <item>
            <key> <string>_proxy_roles</string> </key>
            <value>
              <tuple>
                <string>Manager</string>
              </tuple>
            </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>validateConsistency</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
