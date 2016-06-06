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
            <value> <string># put all counter in closing state for the given site\n
from Products.DCWorkflow.DCWorkflow import ValidationFailed\n
from Products.ERP5Type.Message import Message\n
\n
transaction = state_change[\'object\']\n
\n
site = transaction.getSiteValue()\n
while True:\n
  if not hasattr(site, \'getVaultTypeList\'):\n
    msg = Message(domain = \'ui\', message = \'The site value is misconfigured; report this to system administrators.\')\n
    raise ValidationFailed, (msg,)\n
  if \'site\' in site.getVaultTypeList():\n
    break\n
  site = site.getParentValue()\n
\n
# First make sure there is not any pending operation\n
transaction.Baobab_checkRemainingOperation(site=site)\n
\n
# Then make sure there is nothing any more on counters\n
transaction.Baobab_checkStockBeforeClosingDate(site=site)\n
\n
current_date = transaction.getStartDate()\n
counter_list = [x.getObject() for x in context.portal_catalog(portal_type="Counter", simulation_state = [\'open\', \'closing\'], site_uid = site.getUid())]\n
\n
for counter in counter_list:\n
  # close the counter, this will cancel not finished operations automatically\n
  if counter.getSimulationState() == \'open\':\n
    # first go on state closing\n
    counter.dispose()\n
  # the close it\n
  counter.close()\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>state_change, *args, **kw</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>closeAllCounter</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
