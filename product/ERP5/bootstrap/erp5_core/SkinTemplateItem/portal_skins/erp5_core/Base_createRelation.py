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

# Updates attributes of an Zope document\n
# which is in a class inheriting from ERP5 Base\n
\n
request=context.REQUEST\n
\n
o = context.portal_catalog.getObject(object_uid)\n
\n
form = getattr(context,dialog_id)\n
form.validate_all_to_request(request)\n
my_field = form.get_fields()[0]\n
k = my_field.id\n
values = getattr(request,k,None)\n
module = context.restrictedTraverse(default_module)\n
\n
ref_list = []\n
\n
for v in values:\n
  if catalog_index == \'id\':\n
    # We should not edit the id field\n
    # because the object which is created is not attached to a\n
    # module yet\n
    id = v\n
  else:\n
    id=str(module.generateNewId())\n
  module.invokeFactory(type_name=portal_type,id=id)\n
  new_ob = module.get(id)\n
  kw = {}\n
  if catalog_index != \'id\':\n
    kw[catalog_index] = v\n
    new_ob.edit(**kw)\n
  ref_list.append(new_ob)\n
  new_ob.flushActivity(invoke=1)\n
\n
o.setValue(base_category, ref_list, portal_type=[portal_type])\n
\n
return request[ \'RESPONSE\' ].redirect( return_url )\n
\n
\n
try:\n
  # Validate the form\n
  form = getattr(context,form_id)\n
  form.validate_all_to_request(request)\n
  my_field = None\n
  # Find out which field defines the relation\n
  for f in form.get_fields():\n
    if f.has_value( \'base_category\'):\n
      if f.get_value(\'base_category\') == base_category:\n
        k = f.id\n
        v = getattr(request,k,None)\n
        if v != context.getProperty(k[3:]):\n
          my_field = f\n
  if my_field:\n
    kw ={}\n
    kw[my_field.get_value(\'catalog_index\')] = request.get( my_field.id, None)\n
    context.portal_selections.setSelectionParamsFor(\'Base_viewRelatedObjectList\', kw.copy())\n
    kw[\'base_category\'] = base_category\n
    kw[\'portal_type\'] = my_field.get_value(\'portal_type\')\n
    request.set(\'base_category\', base_category)\n
    request.set(\'portal_type\', my_field.get_value(\'portal_type\'))\n
    request.set(\'form_id\', \'Base_viewRelatedObjectList\')\n
    request.set(my_field.get_value(\'catalog_index\'), request.get( my_field.id, None))\n
    relation_list = context.portal_catalog(**kw)\n
    if len(relation_list) > 0:\n
      return context.Base_viewRelatedObjectList( REQUEST=request )\n
    else:\n
      request.set(\'catalog_index\', my_field.get_value(\'catalog_index\'))\n
      request.set(\'relation_values\', request.get( my_field.id, None))\n
      return context.Base_viewCreateRelationDialog( REQUEST=request )\n
      pass\n
      # context.newRelation(base_category, my_field.get_value(\'portal_type\'))\n
except FormValidationError, validation_errors:\n
  # Pack errors into the request\n
  field_errors = form.ErrorFields(validation_errors)\n
  request.set(\'field_errors\', field_errors)\n
  return form(request)\n
else:\n
  message = \'Relation+Unchanged.\'\n
\n
if not selection_index:\n
  redirect_url = \'%s/%s?%s\' % ( o.absolute_url()\n
                            , form_id\n
                            , \'portal_status_message=%s\' % message\n
                            )\n
else:\n
  redirect_url = \'%s/%s?selection_index=%s&selection_name=%s&%s\' % ( o.absolute_url()\n
                            , form_id\n
                            , selection_index\n
                            , selection_name\n
                            , \'portal_status_message=%s\' % message\n
                            )\n
\n
request[ \'RESPONSE\' ].redirect( redirect_url )\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>form_id, dialog_id, selection_index, selection_name, object_uid, base_category, catalog_index, portal_type, default_module, return_url</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>Base_createRelation</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
