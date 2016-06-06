<?xml version="1.0"?>
<ZopeData>
  <record id="1" aka="AAAAAAAAAAE=">
    <pickle>
      <global name="DTMLMethod" module="OFS.DTMLMethod"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>_Cacheable__manager_id</string> </key>
            <value> <string>http_cache</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>erp5.js</string> </value>
        </item>
        <item>
            <key> <string>_vars</string> </key>
            <value>
              <dictionary/>
            </value>
        </item>
        <item>
            <key> <string>globals</string> </key>
            <value>
              <dictionary/>
            </value>
        </item>
        <item>
            <key> <string>raw</string> </key>
            <value> <string encoding="cdata"><![CDATA[

/*\n
Copyright (c) 20xx-2006 Nexedi SARL and Contributors. All Rights Reserved.\n
\n
This program is Free Software; you can redistribute it and/or\n
modify it under the terms of the GNU General Public License\n
as published by the Free Software Foundation; either version 2\n
of the License, or (at your option) any later version.\n
\n
This program is distributed in the hope that it will be useful,\n
but WITHOUT ANY WARRANTY; without even the implied warranty of\n
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n
GNU General Public License for more details.\n
\n
You should have received a copy of the GNU General Public License\n
along with this program; if not, write to the Free Software\n
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.\n
*/\n
function submitAction(form,act) {\n
  form.action = act;\n
  form.submit();\n
}\n
\n
function isListMode() {\n
  if (document.getElementById("listmodeflag"))\n
    {\n
      alert("ca list");\n
      return(1);\n
    }\n
  else\n
    {\n
      alert("ca lsit pas");\n
      return(0);\n
    }\n
}\n
\n
function affOptions () {\n
var sc = document.getElementById("options_list");\n
if (!sc)\n
  {\n
    return(0);\n
  }\n
if (sc.style.display == "none")\n
  {\n
    sc.style.display = "block";\n
  }\n
else\n
  {\n
    sc.style.display = "none";\n
  }\n
}\n
\n
\n
function affShortcuts () {\n
var sc = document.getElementById("shortcuts");\n
if (!sc)\n
  {\n
    return(0);\n
  }\n
if (sc.style.display == "none")\n
  {\n
    sc.style.display = "block";\n
  }\n
else\n
  {\n
    sc.style.display = "none";\n
  }\n
}\n
\n
function simple_aff(dynamic_check_field) {\n
\n
 if(dynamic_check_field) \n
 {\n
  form_id=dynamic_check_field.split("listbox_")\n
  max_lenght_field_id=form_id[0]+"listbox_listMax"\n
  max_item_field_id=form_id[0]+"listbox_itemMax";\n
  span_field_id=form_id[0]+"listbox_check";\n
  var max_lenght = document.getElementById(max_lenght_field_id).value;\n
  var max_item = document.getElementById(max_item_field_id).value;\n
  var span_field = document.getElementById(span_field_id);\n
\n
  if (span_field.className=="div_short_mode") {\n
     var span_className="div_short_mode"\n
  }\n
  else {\n
     var span_className="div_normal_mode"\n
  }\n
\n
  for (b = 0; b < max_item; b++)\n
  {\n
   for (a = 0; a < max_lenght; a++)\n
    { var foo =form_id[0]+ \'listbox_\' + b + \'data\' + a;\n
      var target = document.getElementById(foo);\n
      if (span_className=="div_short_mode")\n
       {\n
        target.style.display = "inline";\n
        span_field.className="div_normal_mode"\n
       }\n
      else\n
       {\n
        target.style.display = "none";\n
        span_field.className="div_short_mode"\n
       }\n
    }\n
  }\n
 }\n
}\n
\n
function applyHiddenType() {\n
\n
 if(document.getElementById("listbox_listMax"))\n
 { var max_item = document.getElementById("listbox_itemMax").value;\n
   var max_lenght = document.getElementById("listbox_listMax").value;\n
   hideListItems(\'\',max_item, max_lenght)\n
 }\n
\n
/* XXX Hard code, get the number of box with show/hide mode */\n
 for (i = 0; i < 5; i++) {\n
  form_id = "x"+i+"_"\n
  var max_lenght_field_id=form_id+"listbox_listMax"\n
  var max_item_field_id=form_id+"listbox_itemMax"\n
  if(document.getElementById(max_lenght_field_id) && document.getElementById(max_item_field_id) )\n
   { \n
    var max_item = document.getElementById(max_item_field_id).value;\n
    var max_lenght = document.getElementById(max_lenght_field_id).value;\n
    hideListItems(form_id,max_item, max_lenght)\n
   }\n
  }\n
  affShortcuts ();\n
  showSearchSelectedColumn();\n
}\n
\n
function hideListItems(form_id, max_item, max_length)\n
{\n
 check=form_id+"listbox_check";\n
 for (b = 0; b < max_item; b++)\n
 {\n
  for (a = 0; a < max_length; a++)\n
   { var foo =form_id+ \'listbox_\' + b + \'data\' + a;\n
     var target = document.getElementById(foo);\n
     if(target) \n
       target.style.display = "none";\n
   }\n
  }\n
}\n
\n
function showSearchSelectedColumn()\n
{\n
  var select_search_field      = document.getElementById("select_search_field");\n
//   var search_value_list_count  = select_search_field.length;\n
  var search_value_list_count  = document.getElementById("search_value_list_count").value;\n
  var selected_field           = select_search_field.options[select_search_field.selectedIndex];\n
  var selected_field_value     = select_search_field.options[select_search_field.selectedIndex].value;\n
  var selected_field_id        = document.getElementById(\'input\'+selected_field.index).id;\n
\n
 if(selected_field) {\n
  for (a = 0; a < search_value_list_count; a++)\n
   { var foo =\'input\' + a;\n
     var target_name = document.getElementById(foo);\n
     if(target_name) {\n
       var target_id   = target_name.id;\n
       target_name.style.display=(target_id==selected_field_id)?\'inline\':\'none\';\n
       if(target_id==selected_field_id)\n
         select_search_field.selectedIndex=a;\n
     }\n
   }\n
  }\n
  else {\n
    for (a = 0; a < search_value_list_count; a++)\n
    { var foo =\'input\' + a;\n
      var target_name = document.getElementById(foo);\n
      var target_id   = target_name.id;\n
\n
      if(target_name) {\n
        if(a==0)\n
         target_name.style.display=\'inline\';\n
        else\n
         target_name.style.display=\'None\';\n
      }\n
    }\n
  }\n
\n
   /* selected_search_column.style.visibility=(select.options[select.selectedIndex].value == )?\'visible\':\'hidden\'; */\n
}\n
\n
function getTop(MyObject)\n
    {\n
    if (MyObject.offsetParent)\n
        return (MyObject.offsetTop + getTop(MyObject.offsetParent));\n
    else\n
        return (MyObject.offsetTop);\n
    }\n
\n
function loadDivSize () {\n
var left  = document.getElementById("div_prev");\n
var right = document.getElementById("div_next");\n
var sc    = document.getElementById("div_sc");\n
var good_top = getTop(left);\n
right.style.top = good_top;\n
sc.style.top = good_top;\n
}\n
\n
function fixLeftRightHeight(){\n
  var lh = 0;\n
  var lfieldset;\n
  var rh = 0;\n
  var rfieldset;\n
  var liste=document.getElementsByTagName(\'fieldset\');\n
  for(i=0; i<liste.length; i=i+1){\n
    list_parts = liste[i].id.split(\'_\');\n
    for(j=1; j<list_parts.length; j=j+1){\n
      if(list_parts[j] == "left"){\n
        lfieldset = liste[i];\n
      \tlh = lfieldset.offsetHeight;\n
        break;\n
      }else{\n
      \tif(list_parts[j] == "right"){\n
\t  rfieldset = liste[i];\n
\t  rh = rfieldset.offsetHeight;\n
          break;\n
\t}\n
      }\n
    }\n
    if(lh && rh){\n
      break;\n
    }\n
  }\n
  if(lh && rh){\n
    lfieldset.style.height=(lh>rh)? lh+"px" : rh+"px";\n
    rfieldset.style.height=(lh>rh)? lh+"px" : rh+"px";\n
    lfieldset.style.borderTop = \'1px solid #3D7474\';\n
    lfieldset.style.borderLeft = \'1px solid #3D7474\';\n
    lfieldset.style.borderBottom = \'1px solid #3D7474\';\n
    rfieldset.style.borderTop = \'1px solid #3D7474\';\n
    rfieldset.style.borderRight = \'1px solid #3D7474\';\n
    rfieldset.style.borderBottom = \'1px solid #3D7474\';\n
  }\n
}\n


]]></string> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
