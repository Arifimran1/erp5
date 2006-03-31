##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
# Copyright (c) 2003 Nexedi SARL and Contributors. All Rights Reserved.
#          Sebastien Robin <seb@nexedi.com>
#          Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

from Products.Formulator.Field import Field
from Products.Formulator.Widget import Widget
from AccessControl import ClassSecurityInfo
from zLOG import LOG

def Field_generate_field_key(self, validation=0, key=None):
    """Generate the key Silva uses to render the field in the form.
    """
    # Patched by JPS for ERP5 in order to
    # dynamically change the name
    if key is not None:
      return 'field_%s' % key
    if self.field_record is None:
        return 'field_%s' % self.id
    elif validation:
        return self.id
    elif isinstance(self.widget, MultiItemsWidget):
        return "%s.%s:record:list" % (self.field_record, self.id)
    else:
        return '%s.%s:record' % (self.field_record, self.id)

def Field_render(self, value=None, REQUEST=None, key=None):
    """Render the field widget.
    value -- the value the field should have (for instance
              from validation).
    REQUEST -- REQUEST can contain raw (unvalidated) field
              information. If value is None, REQUEST is searched
              for this value.
    if value and REQUEST are both None, the 'default' property of
    the field will be used for the value.
    """
    return self._render_helper(self.generate_field_key(key=key), value, REQUEST)

def Field_render_sub_field(self, id, value=None, REQUEST=None, key=None):
    """Render a sub field, as part of complete rendering of widget in
    a form. Works like render() but for sub field.
        Added key parameter for ERP5 in order to be compatible with listbox/matrixbox
    """
    return self.sub_form.get_field(id)._render_helper(
        self.generate_subfield_key(id, key=key), value, REQUEST)

def Field_generate_subfield_key(self, id, validation=0, key=None):
    """Generate the key Silva uses to render a sub field.
        Added key parameter for ERP5
        Added key parameter for ERP5 in order to be compatible with listbox/matrixbox
    """
    if key is None: key = self.id
    if self.field_record is None or validation:
        return 'subfield_%s_%s'%(key, id)
    return '%s.subfield_%s_%s:record' % (self.field_record, key, id)

def Field_validate_sub_field(self, id, REQUEST, key=None):
    """Validates a subfield (as part of field validation).
    """
    return self.sub_form.get_field(id)._validate_helper(
        self.generate_subfield_key(id, validation=1, key=key), REQUEST)

def Field_render_helper(self, key, value, REQUEST):
    value = self._get_default(key, value, REQUEST)
    if self.get_value('hidden'):
        return self.widget.render_hidden(self, key, value, REQUEST)
    elif (not self.get_value('editable',REQUEST=REQUEST)):
        return self.widget.render_view(self, value)
    else:
        return self.widget.render(self, key, value, REQUEST)

Field.generate_field_key = Field_generate_field_key
Field.render = Field_render
Field.render_sub_field = Field_render_sub_field
Field.generate_subfield_key = Field_generate_subfield_key
Field.validate_sub_field = Field_validate_sub_field
Field._render_helper = Field_render_helper

from Products.Formulator.Validator import SelectionValidator
from Products.Formulator.Validator import StringBaseValidator

def SelectionValidator_validate(self, field, key, REQUEST):
    value = StringBaseValidator.validate(self, field, key, REQUEST)

    if value == "" and not field.get_value('required'):
        return value

    # get the text and the value from the list of items
    # Patch by JPS for Listbox cell
    for item in field.get_value('items', cell=getattr(REQUEST,'cell',None)):
        try:
            item_text, item_value = item
        except ValueError:
            item_text = item
            item_value = item

        # check if the value is equal to the string/unicode version of
        # item_value; if that's the case, we can return the *original*
        # value in the list (not the submitted value). This way, integers
        # will remain integers.
        # XXX it is impossible with the UI currently to fill in unicode
        # items, but it's possible to do it with the TALES tab
        if field.get_value('unicode') and type(item_value) == type(u''):
            str_value = item_value.encode(field.get_form_encoding())
        else:
            str_value = str(item_value)

        if str_value == value:
            return item_value

    # if we didn't find the value, return error
    self.raise_error('unknown_selection', field)

SelectionValidator.validate = SelectionValidator_validate

# The required field should have a default value to 0
from Products.Formulator.DummyField import fields

StringBaseValidator_required = fields.CheckBoxField('required',
                                title='Required',
                                description=(
    "Checked if the field is required; the user has to fill in some "
    "data."),
                                default=0)
StringBaseValidator.required = StringBaseValidator_required

from Products.Formulator.Validator import SelectionValidator

def SelectionValidator_validate(self, field, key, REQUEST):
    value = StringBaseValidator.validate(self, field, key, REQUEST)

    if value == "" and not field.get_value('required'):
        return value

    # get the text and the value from the list of items
    for item in list(field.get_value('items', cell=getattr(REQUEST,'cell',None))) + [field.get_value('default', cell=getattr(REQUEST,'cell',None))]:
        try:
            item_text, item_value = item
        except ValueError:
            item_text = item
            item_value = item

        # check if the value is equal to the string/unicode version of
        # item_value; if that's the case, we can return the *original*
        # value in the list (not the submitted value). This way, integers
        # will remain integers.
        # XXX it is impossible with the UI currently to fill in unicode
        # items, but it's possible to do it with the TALES tab
        if field.get_value('unicode') and type(item_value) == type(u''):
            str_value = item_value.encode(field.get_form_encoding())
        else:
            str_value = str(item_value)

        if str_value == value:
            return item_value

    # if we didn't find the value, return error
    self.raise_error('unknown_selection', field)

SelectionValidator.validate = SelectionValidator_validate

from Products.Formulator.Validator import MultiSelectionValidator

def MultiSelectionValidator_validate(self, field, key, REQUEST):
    values = REQUEST.get(key, [])
    # NOTE: a hack to deal with single item selections
    if type(values) is not type([]):
        # put whatever we got in a list
        values = [values]
    # if we selected nothing and entry is required, give error, otherwise
    # give entry list
    if len(values) == 0:
        if field.get_value('required'):
            self.raise_error('required_not_found', field)
        else:
            return values
    # convert everything to unicode if necessary
    if field.get_value('unicode'):
        values = [unicode(value, field.get_form_encoding())
                  for value in values]

    # create a dictionary of possible values
    value_dict = {}
    for item in field.get_value('items', cell=getattr(REQUEST,'cell',None)): # Patch by JPS for Listbox
        try:
            item_text, item_value = item
        except ValueError:
            item_text = item
            item_value = item
        value_dict[item_value] = 0
    default_value = field.get_value('default', cell=getattr(REQUEST,'cell',None))
    if type(default_value) in (type([]), type(())):
      for v in default_value:
        value_dict[v] = 0
    else:
      value_dict[default_value] = 0


    # check whether all values are in dictionary
    result = []
    for value in values:
        # FIXME: hack to accept int values as well
        try:
            int_value = int(value)
        except ValueError:
            int_value = None
        if int_value is not None and value_dict.has_key(int_value):
            result.append(int_value)
            continue
        if value_dict.has_key(value):
            result.append(value)
            continue
        self.raise_error('unknown_selection', field)
    # everything checks out
    return result

MultiSelectionValidator.validate = MultiSelectionValidator_validate

from Products.Formulator.Validator import BooleanValidator

def BooleanValidator_validate(self, field, key, REQUEST):
    result = not not REQUEST.get(key, 0)
    if result==True:
       return 1
    else:
       return 0

BooleanValidator.validate = BooleanValidator_validate

# Patch the render_view of a TextAreaWidget so that
# it is rendered as a nice box, it is using the tag
# readonly understood by most browsers for a text area

from Products.Formulator.Widget import TextAreaWidget
from Products.Formulator.Widget import render_element
from DocumentTemplate.DT_Util import html_quote

def TextAreaWidget_render_view(self, field, value):
    width = field.get_value('width')
    height = field.get_value('height')

    return render_element("textarea",
                          name='',
                          css_class=field.get_value('css_class'),
                          cols=width,
                          rows=height,
                          contents=html_quote(value),
                          extra='readonly')

TextAreaWidget.render_view = TextAreaWidget_render_view

# Patch the render_view of LinkField so that it is clickable in read-only mode.
from Products.Formulator.Widget import TextWidget
from Products.Formulator.StandardFields import LinkField
from Globals import get_request
from urlparse import urljoin

class PatchedLinkWidget(TextWidget) :
  def render_view(self, field, value) :
    """Render link.
    """
    REQUEST = get_request()
    link_type = field.get_value('link_type')

    if link_type == 'internal':
      value = urljoin(REQUEST['BASE0'], value)
    elif link_type == 'relative':
      value = urljoin(REQUEST['URL1'], value)

    return '<a href="%s">%s</a>' % (value, field.get_value('title', cell=REQUEST.get('cell')))

PatchedLinkWidgetInstance = PatchedLinkWidget()
LinkField.widget = PatchedLinkWidgetInstance

class IntegerWidget(TextWidget) :
  def render(self, field, key, value, REQUEST) :
    """Render link.
    """
    if type(value) is type(1.0):
      value = int(value)
    display_maxwidth = field.get_value('display_maxwidth') or 0
    if display_maxwidth > 0:
        return render_element("input",
                              type="text",
                              name=key,
                              css_class=field.get_value('css_class'),
                              value=value,
                              size=field.get_value('display_width'),
                              maxlength=display_maxwidth,
                              extra=field.get_value('extra'))
    else:
        return render_element("input",
                              type="text",
                              name=key,
                              css_class=field.get_value('css_class'),
                              value=value,
                              size=field.get_value('display_width'),
                              extra=field.get_value('extra'))


from Products.Formulator.StandardFields import IntegerField
from Products.Formulator.Validator import IntegerValidator
IntegerFieldWidgetInstance = IntegerWidget()
IntegerField.widget = IntegerFieldWidgetInstance

import string

def IntegerValidator_validate(self, field, key, REQUEST):
    value = StringBaseValidator.validate(self, field, key, REQUEST)
    # we need to add this check again
    if value == "" and not field.get_value('required'):
        return value

    try:
        if value.find(' ')>0:
          value = value.replace(' ','')
        value = int(value)
    except ValueError:
        self.raise_error('not_integer', field)

    start = field.get_value('start')
    end = field.get_value('end')
    if start != "" and value < start:
        self.raise_error('integer_out_of_range', field)
    if end != "" and value >= end:
        self.raise_error('integer_out_of_range', field)
    return value

IntegerValidator.validate = IntegerValidator_validate

def StringBaseValidator_validate(self, field, key, REQUEST):
  # We had to add this patch for hidden fields of type "list"
  value = REQUEST.get(key, "")
  if type(value) is type('a'):
    value = string.strip(value)
  if field.get_value('required') and value == "":
      self.raise_error('required_not_found', field)
  #if field.get_value('uppercase'):
  #    value = value.upper()

  return value

StringBaseValidator.validate = StringBaseValidator_validate

def render_hidden(self, field, key, value, REQUEST):
    """Renders this widget as a hidden field.
    """
    #LOG('render_hidden',0,str(value))
    try:
        extra = field.get_value('extra')
    except KeyError:
    # In case extra is not defined as in DateTimeWidget
        extra = ''
    result = ''
    # We must adapt the rendering to the type of the value
    # in order to get the correct type back
    if type(value) is type([]) or type(value) is type(()):
      for v in value:
        result += render_element("input",
                          type="hidden",
                          name="%s:list" % key,
                          value=v,
                          extra=extra)
    else:
      result = render_element("input",
                          type="hidden",
                          name=key,
                          value=value,
                          extra=extra)
    return result

Widget.render_hidden = render_hidden

from Products.Formulator.Validator import LinesValidator

def LinesValidator_validate(self, field, key, REQUEST):
    value = StringBaseValidator.validate(self, field, key, REQUEST)
    # Added as a patch for hidden values
    if type(value) is type([]) or type(value) is type(()):
      value = string.join(value, "\n")
    # we need to add this check again
    if value == "" and not field.get_value('required'):
        return []
    if field.get_value('unicode'):
        value = unicode(value, field.get_form_encoding())
    # check whether the entire input is too long
    max_length = field.get_value('max_length') or 0
    if max_length and len(value) > max_length:
        self.raise_error('too_long', field)
    # split input into separate lines
    lines = string.split(value, "\n")

    # check whether we have too many lines
    max_lines = field.get_value('max_lines') or 0
    if max_lines and len(lines) > max_lines:
        self.raise_error('too_many_lines', field)

    # strip extraneous data from lines and check whether each line is
    # short enough
    max_linelength = field.get_value('max_linelength') or 0
    result = []
    whitespace_preserve = field.get_value('whitespace_preserve')
    for line in lines:
        if not whitespace_preserve:
            line = string.strip(line)
        if max_linelength and len(line) > max_linelength:
            self.raise_error('line_too_long', field)
        result.append(line)

    return result

LinesValidator.validate = LinesValidator_validate

from Products.Formulator.Validator import FloatValidator
def FloatValidator_validate(self, field, key, REQUEST):
    value = StringBaseValidator.validate(self, field, key, REQUEST)
    if value == "" and not field.get_value('required'):
        return value
    value = value.replace(' ','')
    input_style = field.get_value('input_style')
    if value.find(',') >= 0:
        value = value.replace(',','.')
    if value.find('%')>=0:
        value = value.replace('%','')
    try:
        value = float(value)
        if input_style.find('%')>=0:
            value = value/100
    except ValueError:
        self.raise_error('not_float', field)
    return value

FloatValidator.validate = FloatValidator_validate

from Products.Formulator.Widget import SingleItemsWidget

def SingleItemsWidget_render_items(self, field, key, value, REQUEST):
  # get items
  items = field.get_value('items', REQUEST=REQUEST, cell=getattr(REQUEST,'cell',None))

  # check if we want to select first item
  if not value and field.get_value('first_item') and len(items) > 0:
      try:
          text, value = items[0]
      except ValueError:
          value = items[0]

  css_class = field.get_value('css_class')
  extra_item = field.get_value('extra_item')

  # if we run into multiple items with same value, we select the
  # first one only (for now, may be able to fix this better later)
  selected_found = 0
  rendered_items = []
  for item in items:
      try:
          item_text, item_value = item
      except ValueError:
          item_text = item
          item_value = item


      if item_value == value and not selected_found:
          rendered_item = self.render_selected_item(item_text,
                                                    item_value,
                                                    key,
                                                    css_class,
                                                    extra_item)
          selected_found = 1
      else:
          rendered_item = self.render_item(item_text,
                                            item_value,
                                            key,
                                            css_class,
                                            extra_item)

      rendered_items.append(rendered_item)

  # XXX We want to make sure that we always have the current value in items. -yo
  if not selected_found and value:
      rendered_item = self.render_selected_item('??? (%s)' % value,
                                                value,
                                                key,
                                                css_class,
                                                extra_item)
      rendered_items.append(rendered_item)

  return rendered_items

SingleItemsWidget.render_items = SingleItemsWidget_render_items

from Products.Formulator.Widget import MultiItemsWidget

def MultiItemsWidget_render_items(self, field, key, value, REQUEST):
  # list is needed, not a tuple
  if type(value) is type(()):
      value = list(value)
  # need to deal with single item selects
  if type(value) is not type([]):
      value = [value]

  # XXX -yo
  selected_found = {}

  items = field.get_value('items',REQUEST=REQUEST, cell=getattr(REQUEST,'cell',None)) # The only thing changes, added request
  css_class = field.get_value('css_class')
  extra_item = field.get_value('extra_item')
  rendered_items = []
  for item in items:
      try:
          item_text, item_value = item
      except ValueError:
          item_text = item
          item_value = item

      if item_value in value:
          rendered_item = self.render_selected_item(item_text,
                                                    item_value,
                                                    key,
                                                    css_class,
                                                    extra_item)
          # XXX -yo
          index = value.index(item_value)
          selected_found[index] = 1
      else:
          rendered_item = self.render_item(item_text,
                                           item_value,
                                           key,
                                           css_class,
                                           extra_item)

      rendered_items.append(rendered_item)

  # XXX We want to make sure that we always have the current value in items. -yo
  for index in range(len(value)):
    v = value[index]
    if index not in selected_found and v:
      rendered_item = self.render_selected_item('??? (%s)' % v,
                                                v,
                                                key,
                                                css_class,
                                                extra_item)
      rendered_items.append(rendered_item)

  return rendered_items

MultiItemsWidget.render_items = MultiItemsWidget_render_items

from Products.Formulator.Widget import MultiListWidget

def MultiListWidget_render(self, field, key, value, REQUEST):
  rendered_items = self.render_items(field, key, value, REQUEST)
  return render_element(
          'select',
          name=key,
          multiple=None,
          css_class=field.get_value('css_class', REQUEST=REQUEST),
          size=field.get_value('size', REQUEST=REQUEST),
          contents=string.join(rendered_items, "\n"),
          extra=field.get_value('extra', REQUEST=REQUEST))

MultiListWidget.render = MultiListWidget_render

from Products.Formulator.Widget import ListWidget

def ListWidget_render(self, field, key, value, REQUEST):
  rendered_items = self.render_items(field, key, value, REQUEST)
  return render_element(
          'select',
          name=key,
          css_class=field.get_value('css_class', REQUEST=REQUEST),
          size=field.get_value('size', REQUEST=REQUEST),
          contents=string.join(rendered_items, "\n"),
          extra=field.get_value('extra', REQUEST=REQUEST))

ListWidget.render = ListWidget_render

# JPS - Subfield handling with listbox requires extension
from Products.Formulator.StandardFields import DateTimeField

def DateTimeField_get_default(self, key, value, REQUEST):
    if value is not None:
        return value
    # if there is something in the request then return None
    # sub fields should pick up defaults themselves
    if REQUEST is not None and hasattr(REQUEST, 'form') and \
        REQUEST.form.has_key('subfield_%s_%s' % (key, 'year')):
        return None
    else:
        return self.get_value('default')

DateTimeField._get_default = DateTimeField_get_default

from Products.Formulator.Widget import DateTimeWidget

class PatchedDateTimeWidget(DateTimeWidget):
    """
      Added support for key in every call to render_sub_field
    """

    def render(self, field, key, value, REQUEST):
        use_ampm = field.get_value('ampm_time_style')
        # FIXME: backwards compatibility hack:
        if not hasattr(field, 'sub_form'):
            from StandardFields import create_datetime_text_sub_form
            field.sub_form = create_datetime_text_sub_form()

        if value is None and field.get_value('default_now'):
            value = DateTime()
        year   = None
        month  = None
        day    = None
        hour   = None
        minute = None
        ampm   = None
        if type(value) is type(DateTime()):
            year = "%04d" % value.year()
            month = "%02d" % value.month()
            day = "%02d" % value.day()
            if use_ampm:
                hour = "%02d" % value.h_12()
            else:
                hour = "%02d" % value.hour()
            minute = "%02d" % value.minute()
            ampm = value.ampm()
        input_order = field.get_value('input_order')
        if input_order == 'ymd':
            order = [('year', year),
                     ('month', month),
                     ('day', day)]
        elif input_order == 'dmy':
            order = [('day', day),
                     ('month', month),
                     ('year', year)]
        elif input_order == 'mdy':
            order = [('month', month),
                     ('day', day),
                     ('year', year)]
        result = []
        for sub_field_name, sub_field_value in order:
            result.append(field.render_sub_field(sub_field_name,
                                                 sub_field_value, REQUEST, key=key))
        date_result = string.join(result, field.get_value('date_separator'))
        if not field.get_value('date_only'):
            time_result = (field.render_sub_field('hour', hour, REQUEST, key=key) +
                           field.get_value('time_separator') +
                           field.render_sub_field('minute', minute, REQUEST, key=key))

            if use_ampm:
                time_result += '&nbsp;' + field.render_sub_field('ampm',
                                                            ampm, REQUEST, key=key)

            return date_result + '&nbsp;&nbsp;&nbsp;' + time_result
        else:
            return date_result

    def render_view(self, field, value):
        if value is None:
            return ''

        use_ampm = field.get_value('ampm_time_style')

        year = "%04d" % value.year()
        month = "%02d" % value.month()
        day = "%02d" % value.day()
        if use_ampm:
            hour = "%02d" % value.h_12()
        else:
            hour = "%02d" % value.hour()
        minute = "%02d" % value.minute()
        ampm = value.ampm()

        order = field.get_value('input_order')
        if order == 'ymd':
            output = [year, month, day]
        elif order == 'dmy':
            output = [day, month, year]
        elif order == 'mdy':
            output = [month, day, year]
        else:
            output = [year, month, day]
        date_result = string.join(output, field.get_value('date_separator'))

        if not field.get_value('date_only'):
            time_result = hour + field.get_value('time_separator') + minute
            if use_ampm:
                time_result += '&nbsp;' + ampm
            return date_result + '&nbsp;&nbsp;&nbsp;' + time_result
        else:
            return date_result

DateTimeField.widget = PatchedDateTimeWidget()

from Products.Formulator.Validator import DateTimeValidator, ValidationError, DateTime
from DateTime.DateTime import DateError, TimeError

class PatchedDateTimeValidator(DateTimeValidator):
    """
      Added support for key in every call to validate_sub_field
    """

    def validate(self, field, key, REQUEST):
        try:
            year = field.validate_sub_field('year', REQUEST, key=key)
            month = field.validate_sub_field('month', REQUEST, key=key)
            day = field.validate_sub_field('day', REQUEST, key=key)

            if field.get_value('date_only'):
                hour = 0
                minute = 0
            elif field.get_value('allow_empty_time'):
                hour = field.validate_sub_field('hour', REQUEST, key=key)
                minute = field.validate_sub_field('minute', REQUEST, key=key)
                if hour == '' and minute == '':
                    hour = 0
                    minute = 0
                elif hour == '' or minute == '':
                    raise ValidationError('not_datetime', field)
            else:
                hour = field.validate_sub_field('hour', REQUEST, key=key)
                minute = field.validate_sub_field('minute', REQUEST, key=key)
        except ValidationError:
            self.raise_error('not_datetime', field)

        # handling of completely empty sub fields
        if ((year == '' and month == '' and day == '') and
            (field.get_value('date_only') or (hour == '' and minute == '')
            or (hour == 0 and minute == 0))):
            if field.get_value('required'):
                self.raise_error('required_not_found', field)
            else:
                # field is not required, return None for no entry
                return None
        # handling of partially empty sub fields; invalid datetime
        if ((year == '' or month == '' or day == '') or
            (not field.get_value('date_only') and
             (hour == '' or minute == ''))):
            self.raise_error('not_datetime', field)


        if field.get_value('ampm_time_style'):
            ampm = field.validate_sub_field('ampm', REQUEST, key=key)
            if field.get_value('allow_empty_time'):
                if ampm == '':
                    ampm = 'am'
            hour = int(hour)
            # handling not am or pm
            # handling hour > 12
            if ((ampm != 'am') and (ampm != 'pm')) or (hour > 12):
                self.raise_error('not_datetime', field)
            if (ampm == 'pm') and (hour == 0):
                self.raise_error('not_datetime', field)
            elif ampm == 'pm' and hour < 12:
                hour += 12

        try:
            result = DateTime(int(year), int(month), int(day), hour, minute)
        # ugh, a host of string based exceptions (not since Zope 2.7)
        except ('DateTimeError', 'Invalid Date Components', 'TimeError',
                DateError, TimeError) :
            self.raise_error('not_datetime', field)

        # check if things are within range
        start_datetime = field.get_value('start_datetime')
        if (start_datetime is not None and
            result < start_datetime):
            self.raise_error('datetime_out_of_range', field)
        end_datetime = field.get_value('end_datetime')
        if (end_datetime is not None and
            result >= end_datetime):
            self.raise_error('datetime_out_of_range', field)

        return result

DateTimeField.validator = PatchedDateTimeValidator()

from Products.Formulator.Widget import TextWidgetInstance

class FloatWidget(TextWidget):

    property_names = TextWidget.property_names +\
                     ['input_style','precision']

    input_style = fields.ListField('input_style',
                                   title="Input style",
                                   description=(
        "The type of float we should enter. "),
                                   default="-1234.5",
                                   items=[("-1234.5",  "-1234.5"),
                                          ("-1 234.5", "-1 234.5"),
                                          ("-12.3%", "-12.3%"),],
                                   required=1,
                                   size=1)

    precision = fields.IntegerField('precision',
                                        title='Precision',
                                        description=(
        "Number of digits after the decimal point"),
                                        default=None,
                                        required=0)

    def format_value(self, field, value):
        """Formats the value as requested"""
        if value not in (None,''):
          input_style = field.get_value('input_style')
          percent = 0
          if input_style.find('%')>=0:
            percent=1
            value = value * 100
          try :
            value = str(float(value))
          except ValueError:
            return value
          value_list = value.split('.')
          integer = value_list[0]
          if input_style.find(' ')>=0:
            integer = value_list[0]
            i = len(integer)%3
            value = integer[:i]
            while i != len(integer):
              value += ' ' + integer[i:i+3]
              i += 3
          else:
            value = value_list[0]
          precision = field.get_value('precision')
          if precision != 0:
            value += '.'
          if precision not in (None,''):
            for i in range(0,precision):
              if i < len(value_list[1]):
                value += value_list[1][i]
              else:
                value += '0'
          else:
            value += value_list[1]
          if percent:
            value += '%'
        return value.strip()

    def render(self, field, key, value, REQUEST):
        """Render Float input field
        """
        value = self.format_value(field, value)
        display_maxwidth = field.get_value('display_maxwidth') or 0
        extra_keys = {}
        if display_maxwidth > 0:
          extra_keys['maxlength'] = display_maxwidth
        return render_element( "input",
                                type="text",
                                name=key,
                                css_class=field.get_value('css_class'),
                                value=value,
                                size=field.get_value('display_width'),
                                extra=field.get_value('extra'),
                                **extra_keys)


    def render_view(self, field, value):
        """
          Render Float display field.
          This patch add:
            * replacement of spaces by unbreakable spaces if the content is float-like
            * support of extra CSS class when render as pure text
        """
        value = self.format_value(field, value)

        float_value = None
        try:
          float_value = float(value.replace(' ', ''))
        except:
          pass
        if float_value != None:
          value = value.replace(' ', '&nbsp;')

        extra = field.get_value('extra')
        if extra not in (None, ''):
          value = "<div %s>%s</div>" % (extra, value)

        return TextWidgetInstance.render_view(field, value)


FloatWidgetInstance = FloatWidget()
from Products.Formulator.StandardFields import FloatField
FloatField.widget = FloatWidgetInstance

###################################################################
# New formulator API
# 
# render method on Field must change, and have a new parameter:
#   render_format
# which is used to call others methods ('html' call render_html)
###################################################################
# XXX Patching all Fields is not easy, as ERP5 defines his own fields.
# def Widget_render(self, field, key, value, REQUEST, render_format='html')
#   # Test if method defined on class
#   method_id = 'render_%' % render_format
#   if hasattr(aq_self(self), method_id):
#     # Try to return built-in renderer
#     return getattr(self, method_id )(self, field, key, value, REQUEST)
#   raise KeyError, "Rendering not defined"

# Monkey Patch
# 
# Lookup all registered widgets and create render_html
# XXX This method is not a good way of patching, 
# because it breaks inheritance
# XXX It's difficult to get all possible widgets, as ERP5 defines 
# also his owns.
# for f in Formulator.widgets():
#   if not hasattr(f, '__erp5_patched'):
#     f.render_html = f.render
def Widget_render_html(self, *args, **kw):
  return self.render(*args, **kw)
Widget.render_html = Widget_render_html

def Field_render_html(self, *args, **kw):
  """
  render_html is used to as definition of render method in Formulator.
  """
  return self.render(*args, **kw)
Field.render_html = Field_render_html

def Field_render_htmlgrid(self, value=None, REQUEST=None, key=None):
  """
  render_htmlgrid returns a list of tuple (title, html render)
  """
  # What about CSS ? What about description ? What about error ?
  return ((self.get_value('title'), 
          self.render_html(value=value, REQUEST=REQUEST, key=key)),)
Field.render_htmlgrid = Field_render_htmlgrid

# Generic possible renderers                                                                                                                          
#   def render_ext(self, field, key, value, REQUEST):
#     return getattr(self, '%s_render' % self.__class__.__name__)
# 
#   def render_pt(self, field, key, value, REQUEST):
#     """
#     Call a page template which contains 1 macro per field
#     """
#     return self.field_master(self.__class__.__name__)
# 
#   def render_grid(self, field, key, value, REQUEST):
#     return ((self.get_value('title'), self.get_value('value'),)
#    # What about CSS ? What about description ? What about error ?
#    # What about rendering a listbox ?
#    # Grid is only valid if stucture of grid has some meaning and is
#    # implemeted by listbox (ex. spreadsheet = grid)
# 
#   def render_pdf(self, field, key, value, REQUEST):
#     return 'whatever for reportlab'
