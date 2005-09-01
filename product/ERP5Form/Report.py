##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from Globals import InitializeClass, DTMLFile, get_request
from AccessControl import ClassSecurityInfo
from Products.PythonScripts.Utility import allow_class
from Products.Formulator.DummyField import fields
from Products.Formulator.Form import ZMIForm

from urllib import quote
from Products.ERP5Type import PropertySheet

from Form import ERP5Form
from Form import create_settings_form as Form_create_settings_form

def create_settings_form():
    form = Form_create_settings_form()
    report_method = fields.StringField(
                         'report_method',
                         title='Report Method',
                         description=('The method to get a list of items (object, form, parameters) '
                                      'to aggregate in a single Report'),
                         default='',
                         required=0)

    form.add_fields([report_method])
    return form

manage_addReport = DTMLFile("dtml/report_add", globals())

def addERP5Report(self, id, title="", REQUEST=None):
    """Add form to folder.
    id     -- the id of the new form to add
    title  -- the title of the form to add
    Result -- empty string
    """
    # add actual object
    id = self._setObject(id, ERP5Report(id, title))
    # respond to the add_and_edit button if necessary
    add_and_edit(self, id, REQUEST)
    return ''    
    
class ERP5Report(ERP5Form):
    """
        An ERP5Form which allows to aggregate a list of 
        forms each of which is rendered on an object with parameters.
        
        Application: create an accounting book from ERP5 objects 
        
        - Display the total of each account (report)
        
        - List all accounts
        
        - Display the transactions of each account (one form with listbox)
        
        - List all clients
        
        - Display the transactions of each client (one form with listbox)
        
        - List all vendors
        
        - Display the transactions of each vendor (one form with listbox)
        
          
    """
    meta_type = "ERP5 Report"
    icon = "www/Form.png"

    # Declarative Security
    security = ClassSecurityInfo()

    # Declarative properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.SimpleItem)

    # Constructors
    constructors =   (manage_addReport, addERP5Report)

    # This is a patched dtml formOrder
    security.declareProtected('View management screens', 'formOrder')
    formOrder = DTMLFile('dtml/formOrder', globals())

    # Default Attributes
    report_method = None
    
    # Special Settings
    settings_form = create_settings_form()

    def __init__(self, id, title, unicode_mode=0, encoding='UTF-8', stored_encoding='UTF-8'):
        """Initialize form.
        id    -- id of form
        title -- the title of the form
        """
        ZMIForm.inheritedAttribute('__init__')(self, "", "POST", "", id,
                                               encoding, stored_encoding,
                                               unicode_mode)
        self.id = id
        self.title = title
        self.row_length = 4

    # Proxy method to PageTemplate
    def __call__(self, *args, **kwargs):
        if not kwargs.has_key('args'):
          kwargs['args'] = args
        form = self
        object = getattr(form, 'aq_parent', None)
        if object:
          container = object.aq_inner.aq_parent
        else:
          container = None
        pt = getattr(self,self.pt)
        report_method = getattr(object,self.report_method)
        extra_context = self.pt_getContext()
        extra_context['options'] = kwargs
        extra_context['form'] = self
        extra_context['container'] = container ## PROBLEM NOT TAKEN INTO ACCOUNT
        extra_context['here'] = object
        extra_context['report_method'] = report_method
        return pt.pt_render(extra_context=extra_context)

    def _exec(self, bound_names, args, kw):
        pt = getattr(self,self.pt)
        return pt._exec(self, bound_names, args, kw)

def add_and_edit(self, id, REQUEST):
    """Helper method to point to the object's management screen if
    'Add and Edit' button is pressed.
    id -- id of the object we just added
    """
    if REQUEST is None:
        return
    try:
        u = self.DestinationURL()
    except:
        u = REQUEST['URL1']
    if REQUEST['submit'] == " Add and Edit ":
        u = "%s/%s" % (u, quote(id))
    REQUEST.RESPONSE.redirect(u+'/manage_main')

def manage_add_report(self, id, title="", unicode_mode=0, REQUEST=None):
    """Add form to folder.
    id     -- the id of the new form to add
    title  -- the title of the form to add
    Result -- empty string
    """
    # add actual object
    id = self._setObject(id, ZMIForm(id, title, unicode_mode))
    # respond to the add_and_edit button if necessary
    add_and_edit(self, id, REQUEST)
    return ''

class ReportSection:
  meta_type = "ReportSection"
  security = ClassSecurityInfo()
  
  param_dict = {}

  def __init__(self, path='', form_id='view',
                     title=None, translated_title=None, level=1,
                     selection_name=None, selection_params=None,
                     listbox_display_mode=None, selection_columns=None,
                     selection_sort_order=None,
                     selection_report_path=None, selection_report_list=None,
                     preferences = None ) :
    """
      Initialize the line and set the default values
      Selected columns must be defined in parameter of listbox.render...

      In ReportTree listbox display mode, you can override :
        selection_report_path, the root category for this report 
        selection_report_list, the list of unfolded categories (defaults to all)      
 
    """
    
    self.path = path
    self.form_id = form_id
    self.title = title
    self.translated_title = translated_title
    self.level = level
    self.saved_request = {}
    self.selection_name = selection_name
    self.selection_params = selection_params
    self.listbox_display_mode = listbox_display_mode
    self.selection_columns = selection_columns
    self.selection_sort_order = selection_sort_order
    self.saved_selections = {}
    self.selection_report_path = selection_report_path
    self.selection_report_list = selection_report_list
    if preferences == None :
      preferences = {}
    self.preferences = preferences
    self.saved_preferences = {}
    
  security.declarePublic('getTitle')
  def getTitle(self):
    return self.title

  security.declarePublic('getTranslatedTitle')
  def getTranslatedTitle(self):
    return self.translated_title

  security.declarePublic('getLevel')
  def getLevel(self):
    return self.level

  security.declarePublic('getPath')
  def getPath(self):
    return self.path

  security.declarePublic('getObject')
  def getObject(self, context):
    return context.restrictedTraverse(self.path)

  security.declarePublic('getFormId')
  def getFormId(self):
    return self.form_id
  
  _no_parameter_ = []
    
  security.declarePublic('pushReport')
  def pushReport(self, context):
    REQUEST = get_request()
    for k,v in self.param_dict.items():
      self.saved_request[k] = REQUEST.form.get(k, self._no_parameter_)
      REQUEST.form[k] = v
    
    portal_selections = context.portal_selections
    selection_list = [self.selection_name]
    if self.form_id and hasattr(context[self.form_id], 'listbox') :
      selection_list += [ context[self.form_id].listbox.get_value('selection_name') ]
    # save report's selection and orignal form's selection, as ListBox will overwrite it
    for selection_name in selection_list :
      if selection_name is not None :
        if not self.saved_selections.has_key(selection_name) :
          self.saved_selections[selection_name] = {}
        if self.selection_report_list is not None:
          selection = portal_selections.getSelectionFor(selection_name, REQUEST=REQUEST)
          self.saved_selections[selection_name]['report_list'] = \
               selection.getReportList()
          selection.edit(report_list=self.selection_report_list)
        if self.selection_report_path is not None:
          selection = portal_selections.getSelectionFor(selection_name, REQUEST=REQUEST)
          self.saved_selections[selection_name]['report_path'] = \
               selection.getReportPath()
          selection.edit(report_path=self.selection_report_path)
        if self.listbox_display_mode is not None:
          self.saved_selections[selection_name]['display_mode'] = \
               portal_selections.getListboxDisplayMode(selection_name, REQUEST=REQUEST)
          portal_selections.setListboxDisplayMode(REQUEST, self.listbox_display_mode,
                                                selection_name=selection_name)
        if self.selection_params is not None:
          self.saved_selections[selection_name]['params'] =  \
               portal_selections.getSelectionParams(selection_name, REQUEST=REQUEST)
          portal_selections.setSelectionParamsFor(selection_name,
                                                  self.selection_params, REQUEST=REQUEST)
        if self.selection_columns is not None:
          self.saved_selections[selection_name]['columns'] =  \
               portal_selections.getSelectionColumns(selection_name, REQUEST=REQUEST)
          portal_selections.setSelectionColumns(selection_name, self.selection_columns,
                                              REQUEST=REQUEST)
        if self.selection_sort_order is not None:
          self.saved_selections[selection_name]['sort_order'] =  \
               portal_selections.getSelectionSortOrder(selection_name, REQUEST=REQUEST)
          portal_selections.setSelectionSortOrder(selection_name, self.selection_sort_order,
                                              REQUEST=REQUEST)

    portal_pref = context.getPortalObject().portal_preferences
    for pref, value in self.preferences.items() :
      self.saved_preferences[pref] = portal_pref.getPreference(pref)
      portal_pref.setPreference(pref, value)
    
  security.declarePublic('popReport')
  def popReport(self, context):
    REQUEST = get_request()
    for k,v in self.param_dict.items():
      if self.saved_request[k] is self._no_parameter_:
        del REQUEST.form[k]
      else:
        REQUEST.form[k] = self.saved_request[k]
    
    portal_selections = context.portal_selections
    selection_list = []
    if self.form_id and hasattr(context[self.form_id], 'listbox') :
      selection_list += [ context[self.form_id].listbox.get_value('selection_name') ]
    selection_list += [self.selection_name]
    # restore report then form selection
    for selection_name in selection_list:
      if selection_name is not None:
        if self.selection_report_list is not None:
          selection = portal_selections.getSelectionFor(selection_name, REQUEST=REQUEST)
          selection.edit(report_list = self.saved_selections[selection_name]['report_list'])
        if self.selection_report_path is not None:
          selection = portal_selections.getSelectionFor(selection_name, REQUEST=REQUEST)
          selection.edit(report_path = self.saved_selections[selection_name]['report_path'])
        if self.listbox_display_mode is not None:
          portal_selections.setListboxDisplayMode(REQUEST,
                                                self.saved_selections[selection_name]['display_mode'],
                                                selection_name=selection_name)
        if self.listbox_display_mode is not None:
          portal_selections.setListboxDisplayMode(REQUEST,
                                                self.saved_selections[selection_name]['display_mode'],
                                                selection_name=selection_name)
        if self.selection_params is not None:
          # first make sure no parameters that have been pushed are erased 
          portal_selections.setSelectionParamsFor(selection_name, {}, REQUEST=REQUEST)
          # then restore the original params
          portal_selections.setSelectionParamsFor(selection_name,
                                                  self.saved_selections[selection_name]['params'],
                                                  REQUEST=REQUEST)
        if self.selection_columns is not None:
          portal_selections.setSelectionColumns(selection_name,
                                              self.saved_selections[selection_name]['columns'],
                                              REQUEST=REQUEST)
        if self.selection_sort_order is not None:
          portal_selections.setSelectionSortOrder(selection_name,
                                              self.saved_selections[selection_name]['sort_order'],
                                              REQUEST=REQUEST)

    for pref, value in self.saved_preferences.items() :
      context.getPortalObject().portal_preferences.setPreference(pref, value)

InitializeClass(ReportSection)
allow_class(ReportSection)

