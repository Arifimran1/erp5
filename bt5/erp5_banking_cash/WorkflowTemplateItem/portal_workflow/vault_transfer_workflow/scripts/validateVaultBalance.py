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
date = transaction.getStartDate()\n
vault = transaction.getSource()\n
vaultDestination = transaction.getDestination()\n
\n
if vault is None or vaultDestination is None:\n
  msg = Message(domain="ui", message="You must define vaults.")\n
  raise ValidationFailed, (msg,)\n
\n
# use of the constraint : Test source and destination\n
vliste = transaction.checkConsistency()\n
transaction.log(\'vliste\', vliste)\n
if len(vliste) != 0:\n
  raise ValidationFailed, (vliste[0].getMessage(),)\n
\n
# check we are in an opened accounting day\n
transaction.Baobab_checkCounterDateOpen(site=vaultDestination, date=date)\n
\n
\n
if \'reserve\' in vault and \'salle_tri\' in vaultDestination:\n
  msg = Message(domain="ui", message="Cannot transfer ressource to ${destination} from ${source}.",\n
                mapping={\'source\':transaction.getSourceValue().getParentValue().getTitle(),\n
                         \'destination\':transaction.getDestinationValue().getParentValue().getTitle()})\n
\n
  raise ValidationFailed, (msg,)\n
resource = transaction.CashDelivery_checkCounterInventory(source=vault, portal_type=\'Vault Transfer Line\')\n
\n
# Get price and total_price.\n
amount = transaction.getSourceTotalAssetPrice()\n
total_price = transaction.getTotalPrice(portal_type=[\'Vault Transfer Line\',\'Vault Transfer Cell\'],fast=0)\n
\n
if resource == 2:\n
  msg = Message(domain="ui", message="No Resource.")\n
  raise ValidationFailed, (msg,)\n
elif amount != total_price:\n
  msg = Message(domain="ui", message="Amount differ from total price.")\n
  raise ValidationFailed, (msg,)\n
elif resource <> 0 :\n
  msg = Message(domain="ui", message="Insufficient Balance.")\n
  raise ValidationFailed, (msg,)\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>state_change</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>validateVaultBalance</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
