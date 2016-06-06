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
            <value> <string>"""\n
  This script edits a Knowledge Box instance used for saving a Gadget preferences.\n
"""\n
from Products.Formulator.Errors import FormValidationError\n
from json import dumps\n
\n
kw = {}\n
request = context.REQUEST\n
form = request.form\n
fields = filter(lambda x: x.startswith(form_fields_main_prefix), form.keys())\n
box = context.restrictedTraverse(box_relative_url)\n
portal_selection = context.getPortalObject().portal_selections\n
\n
# do validation\n
form = getattr(box, form_id)\n
try:\n
  # Validate\n
  form.validate_all_to_request(request, key_prefix=form_fields_main_prefix)\n
except FormValidationError, validation_errors:\n
  # Pack errors into the request\n
  field_errors = form.ErrorFields(validation_errors)\n
  request.set(\'field_errors\', field_errors)\n
  # we need form rendered in gadget mode\n
  request.set(\'is_gadget_mode\', 1)\n
  # Make sure editors are pushed back as values into the REQUEST object\n
  for f in form.get_fields():\n
    field_id = f.id\n
    if request.has_key(field_id):\n
      value = request.get(field_id)\n
      if callable(value):\n
        value(request)\n
  # return validation failed code and rendered form\n
  result = {\'content\': form(request, key_prefix=form_fields_main_prefix),\n
            \'validation_status\':  0}\n
  return dumps(result)\n
\n
form = request.form\n
# get interesting for us fields and save\n
listbox_selection_field_prefix = \'%s_my_listbox_selection_\' %form_fields_main_prefix\n
for field in fields:\n
  #if it\'s a fied in a lisbox gadget it modifies directly the selection\n
  if field.startswith(listbox_selection_field_prefix):\n
    selection_name = context.Base_getListboxGadgetSelectionName(box_relative_url)\n
    selection = portal_selection.getSelectionFor(selection_name)\n
    if selection is not None:\n
      params =  selection.getParams()\n
      params[field.replace(listbox_selection_field_prefix, \'\')] = str(form[field])\n
      portal_selection.setSelectionParamsFor(selection_name, params)\n
  kw[field.replace(\'%s_my_\' %form_fields_main_prefix, \'\')] = form[field]\n
\n
# edit\n
box.edit(**kw)\n
\n
if not synchronous_mode:\n
  # return JSON in asynchronous mode\n
  result = {\'content\': \'\',\n
            \'validation_status\': 1}\n
  return dumps(result)\n
\n
# determine redirect URL as passed from gadget preference form\n
if gadget_redirect_url is None:\n
  # taking URL1 as the base of the original URL. \n
  # it works for both synchronous and  asynchronous gadgets\n
  gadget_redirect_url = request[\'URL1\']\n
request.RESPONSE.redirect(\'%s?portal_status_message=%s\'\n
                           %(gadget_redirect_url, \n
                             context.Base_translateString(\'Preference updated.\')))\n
</string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>form_id, form_fields_main_prefix, box_relative_url, gadget_redirect_url=None, synchronous_mode=True</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>KnowledgeBox_baseEdit</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
