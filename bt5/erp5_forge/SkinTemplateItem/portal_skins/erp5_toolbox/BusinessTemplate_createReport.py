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

portal = context.getPortalObject()\n
skin_folder = getattr(portal.portal_skins, skin_folder)\n
\n
type_name = portal_type.replace(\' \', \'\')\n
report_name_part = \'\'.join([part.capitalize() for part in report_name.split()])\n
dialog_form_name = \'%s_view%sReportDialog\' % (type_name, report_name_part)\n
report_form_name = \'%s_view%sReport\' % (type_name, report_name_part)\n
report_section_form_name = \'%s_view%sReportSection\' % (type_name,\n
    report_name_part)\n
get_report_section_script_name = \'%s_get%sReportSectionList\' % (type_name,\n
    report_name_part)\n
get_line_list_script_name = \'%s_get%sLineList\' % (type_name, report_name_part)\n
action_id = "%s_report" % \'_\'.join([part.lower() for part in report_name.split()])\n
\n
# Create the dialog\n
skin_folder.manage_addProduct[\'ERP5Form\'].addERP5Form(dialog_form_name, report_name)\n
dialog = getattr(skin_folder, dialog_form_name)\n
dialog.manage_settings(\n
    dict(field_title=dialog.title,\n
         field_name=dialog.name,\n
         field_description=dialog.description,\n
         field_action=report_form_name,\n
         field_update_action=dialog.update_action,\n
         field_update_action_title=dialog.update_action_title,\n
         field_enctype=dialog.enctype,\n
         field_encoding=dialog.encoding,\n
         field_stored_encoding=dialog.stored_encoding,\n
         field_unicode_mode=dialog.unicode_mode,\n
         field_method=dialog.method,\n
         field_row_length=str(dialog.row_length),\n
         field_pt=\'form_dialog\',\n
         field_edit_order=[]))\n
\n
if use_from_date_at_date:\n
  dialog.manage_addField(\n
           id=\'your_from_date\',\n
           fieldname=\'ProxyField\',\n
           title=\'\')\n
  dialog.your_from_date.manage_edit_xmlrpc(\n
      dict(form_id=\'Base_viewDialogFieldLibrary\',\n
           field_id=\'your_from_date\'))\n
  dialog.manage_addField(\n
           id=\'your_at_date\',\n
           fieldname=\'ProxyField\',\n
           title=\'\')\n
  dialog.your_at_date.manage_edit_xmlrpc(\n
      dict(form_id=\'Base_viewDialogFieldLibrary\',\n
           field_id=\'your_at_date\'))\n
\n
dialog.manage_addField(\n
         id=\'your_portal_skin\',\n
         fieldname=\'ProxyField\',\n
         title=\'\')\n
dialog.your_portal_skin.manage_edit_xmlrpc(\n
    dict(form_id=\'Base_viewDialogFieldLibrary\',\n
         field_id=\'your_portal_skin\'))\n
dialog.manage_addField(\n
         id=\'your_format\',\n
         fieldname=\'ProxyField\',\n
         title=\'\')\n
dialog.your_format.manage_edit_xmlrpc(\n
    dict(form_id=\'Base_viewDialogFieldLibrary\',\n
         field_id=\'your_format\'))\n
dialog.manage_addField(\n
         id=\'your_deferred_style\',\n
         fieldname=\'ProxyField\',\n
         title=\'\')\n
dialog.your_deferred_style.manage_edit_xmlrpc(\n
    dict(form_id=\'Base_viewDialogFieldLibrary\',\n
         field_id=\'your_deferred_style\'))\n
\n
# Associate the dialog with type information\n
type_information = portal.portal_types.getTypeInfo(portal_type)\n
max_priority = 0\n
action_list = type_information.contentValues(portal_type=\'Action Information\')\n
if action_list:\n
  max_priority = max([ai.getFloatIndex() or 0 for ai in action_list])\n
  \n
type_information.addAction(\n
    action_id,\n
    report_name,\n
    "string:${object_url}/%s" % dialog_form_name,\n
    \'\',\n
    \'View\',\n
    \'object_report\',\n
    priority=max_priority+1,)\n
\n
type_information.addAction(\n
    action_id.replace(\'_report\', \'_export\'),\n
    report_name,\n
    "string:${object_url}/%s?your_portal_skin=ODS&your_format=" % dialog_form_name,\n
    "python: getattr(portal.portal_skins, \'erp5_ods_style\', None) is not None",\n
    \'View\',\n
    \'object_exchange\',\n
    priority=max_priority+1,)\n
\n
\n
# Associate the dialog with type information in business template meta data\n
if context.getPortalType() == \'Business Template\' and \\\n
     context.getInstallationState() != \'installed\':\n
  context.setTemplateActionPathList(context.getTemplateActionPathList() +\n
      (\'%s | %s\' % (portal_type, action_id),\n
       \'%s | %s\' % (portal_type, action_id.replace(\'_report\', \'_export\')), ))\n
\n
# Create the report\n
skin_folder.manage_addProduct[\'ERP5Form\'].addERP5Report(report_form_name, report_name)\n
report = getattr(skin_folder, report_form_name)\n
report.manage_settings(\n
  dict(field_title=report.title,\n
       field_name=report.name,\n
       field_description=report.description,\n
       field_action=report_form_name,\n
       field_update_action=report.update_action,\n
       field_update_action_title=report.update_action_title,\n
       field_enctype=report.enctype,\n
       field_encoding=report.encoding,\n
       field_stored_encoding=report.stored_encoding,\n
       field_unicode_mode=report.unicode_mode,\n
       field_method=report.method,\n
       field_row_length=str(report.row_length),\n
       field_pt=\'report_view\',\n
       field_report_method=get_report_section_script_name,\n
       field_edit_order=[]))\n
\n
skin_folder.manage_addProduct[\'ERP5Form\'].addERP5Form(\n
                    report_section_form_name, report_name)\n
report_section_form = getattr(skin_folder, report_section_form_name)\n
report_section_form.manage_settings(\n
  dict(field_title=report_section_form.title,\n
       field_name=report_section_form.name,\n
       field_description=report_section_form.description,\n
       field_action=\'\',\n
       field_update_action=report_section_form.update_action,\n
       field_update_action_title=report_section_form.update_action_title,\n
       field_enctype=report_section_form.enctype,\n
       field_encoding=report_section_form.encoding,\n
       field_stored_encoding=report_section_form.stored_encoding,\n
       field_unicode_mode=report_section_form.unicode_mode,\n
       field_method=report_section_form.method,\n
       field_row_length=str(report_section_form.row_length),\n
       field_pt=\'form_view\',\n
       field_report_method=get_report_section_script_name,\n
       field_edit_order=[]))\n
\n
report_section_form.manage_addField(\n
         id=\'listbox\',\n
         fieldname=\'ProxyField\',\n
         title=\'\')\n
report_section_form.listbox.manage_edit_xmlrpc(\n
    dict(form_id=\'Base_viewFieldLibrary\',\n
         field_id=\'my_view_mode_listbox\'))\n
report_section_form.move_field_group((\'listbox\',), \'left\', \'bottom\')\n
\n
report_section_form.listbox.manage_edit_surcharged_xmlrpc(\n
  dict(selection_name=(\'_\'.join((portal_type + report_name).split())).lower() + \'_selection\',\n
       title=report_name,\n
       # XXX this must be a Method, but as far as I know, we cannot set list\n
       # method in restricted environment\n
     # list_method=get_line_list_script_name\n
       ))\n
\n
if use_from_date_at_date:\n
  report.manage_addField(\n
           id=\'your_from_date\',\n
           fieldname=\'ProxyField\',\n
           title=\'\')\n
  report.your_from_date.manage_edit_xmlrpc(\n
      dict(form_id=\'Base_viewReportFieldLibrary\',\n
           field_id=\'your_from_date\'))\n
  report.manage_addField(\n
           id=\'your_at_date\',\n
           fieldname=\'ProxyField\',\n
           title=\'\')\n
  report.your_at_date.manage_edit_xmlrpc(\n
      dict(form_id=\'Base_viewReportFieldLibrary\',\n
           field_id=\'your_at_date\'))\n
\n
# Create the report section script\n
skin_folder.manage_addProduct[\'PythonScripts\'].manage_addPythonScript(\n
    get_report_section_script_name)\n
script = getattr(skin_folder, get_report_section_script_name)\n
\n
get_param_part = \'\'\n
if use_from_date_at_date:\n
  get_param_part = \'from_date = request.get("from_date")\\n\'\\\n
                   \'at_date = request.get("at_date")\'\n
\n
script.ZPythonScript_edit(\'\',\n
"""from Products.ERP5Form.Report import ReportSection\n
portal = context.getPortalObject()\n
request = container.REQUEST\n
%s\n
\n
return [ReportSection(form_id=\'%s\',\n
                      path=context.getPhysicalPath())]\n
""" % (get_param_part, report_section_form_name))\n
\n
\n
# Create the script to get list of lines\n
skin_folder.manage_addProduct[\'PythonScripts\'].manage_addPythonScript(\n
    get_line_list_script_name)\n
script = getattr(skin_folder, get_line_list_script_name)\n
params = \'**kw\'\n
if use_from_date_at_date:\n
  params = \'from_date=None, at_date=None, **kw\'\n
\n
script.ZPythonScript_edit(params,\n
"""from Products.PythonScripts.standard import Object\n
portal = context.getPortalObject()\n
\n
# TODO: get list of lines here\n
\n
return [Object(uid=\'new_\',\n
               title=\'Nothing\',\n
              )]\n
""")\n
\n
\n
return context.Base_redirect(form_id,\n
    keep_items=dict(portal_status_message=\n
      context.Base_translateString(\'Report created.\')))\n


]]></string> </value>
        </item>
        <item>
            <key> <string>_params</string> </key>
            <value> <string>form_id=\'view\', portal_type=None, report_name=None, skin_folder=None, use_from_date_at_date=None</string> </value>
        </item>
        <item>
            <key> <string>id</string> </key>
            <value> <string>BusinessTemplate_createReport</string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
