<?xml version="1.0"?>
<ZopeData>
  <record id="1" aka="AAAAAAAAAAE=">
    <pickle>
      <global name="File" module="OFS.Image"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>_Cacheable__manager_id</string> </key>
            <value> <string>http_cache</string> </value>
        </item>
        <item>
            <key> <string>_EtagSupport__etag</string> </key>
            <value> <string>ts83646620.89</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>theme-chaos.js</string> </value>
        </item>
        <item>
            <key> <string>content_type</string> </key>
            <value> <string>application/javascript</string> </value>
        </item>
        <item>
            <key> <string>data</string> </key>
            <value> <string>/* ***** BEGIN LICENSE BLOCK *****\n
 * Distributed under the BSD license:\n
 * \n
 * Copyright 2011 Irakli Gozalishvili. All rights reserved.\n
 * Permission is hereby granted, free of charge, to any person obtaining a copy\n
 * of this software and associated documentation files (the "Software"), to\n
 * deal in the Software without restriction, including without limitation the\n
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or\n
 * sell copies of the Software, and to permit persons to whom the Software is\n
 * furnished to do so, subject to the following conditions:\n
 *\n
 * The above copyright notice and this permission notice shall be included in\n
 * all copies or substantial portions of the Software.\n
 *\n
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\n
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS\n
 * IN THE SOFTWARE.\n
 * ***** END LICENSE BLOCK ***** */\n
\n
define(\'ace/theme/chaos\', [\'require\', \'exports\', \'module\' , \'ace/lib/dom\'], function(require, exports, module) {\n
\n
exports.isDark = true;\n
exports.cssClass = "ace-chaos";\n
exports.cssText = ".ace-chaos .ace_gutter {\\\n
background: #141414;\\\n
color: #595959;\\\n
border-right: 1px solid #282828;\\\n
}\\\n
.ace-chaos .ace_gutter-cell.ace_warning {\\\n
background-image: none;\\\n
background: #FC0;\\\n
border-left: none;\\\n
padding-left: 0;\\\n
color: #000;\\\n
}\\\n
.ace-chaos .ace_gutter-cell.ace_error {\\\n
background-position: -6px center;\\\n
background-image: none;\\\n
background: #F10;\\\n
border-left: none;\\\n
padding-left: 0;\\\n
color: #000;\\\n
}\\\n
.ace-chaos .ace_print-margin {\\\n
border-left: 1px solid #555;\\\n
right: 0;\\\n
background: #1D1D1D;\\\n
}\\\n
.ace-chaos {\\\n
background-color: #161616;\\\n
color: #E6E1DC;\\\n
}\\\n
.ace-chaos .ace_cursor {\\\n
border-left: 2px solid #FFFFFF;\\\n
}\\\n
.ace-chaos .ace_cursor.ace_overwrite {\\\n
border-left: 0px;\\\n
border-bottom: 1px solid #FFFFFF;\\\n
}\\\n
.ace-chaos .ace_marker-layer .ace_selection {\\\n
background: #494836;\\\n
}\\\n
.ace-chaos .ace_marker-layer .ace_step {\\\n
background: rgb(198, 219, 174);\\\n
}\\\n
.ace-chaos .ace_marker-layer .ace_bracket {\\\n
margin: -1px 0 0 -1px;\\\n
border: 1px solid #FCE94F;\\\n
}\\\n
.ace-chaos .ace_marker-layer .ace_active-line {\\\n
background: #333;\\\n
}\\\n
.ace-chaos .ace_gutter-active-line {\\\n
background-color: #222;\\\n
}\\\n
.ace-chaos .ace_invisible {\\\n
color: #404040;\\\n
}\\\n
.ace-chaos .ace_keyword {\\\n
color:#00698F;\\\n
}\\\n
.ace-chaos .ace_keyword.ace_operator {\\\n
color:#FF308F;\\\n
}\\\n
.ace-chaos .ace_constant {\\\n
color:#1EDAFB;\\\n
}\\\n
.ace-chaos .ace_constant.ace_language {\\\n
color:#FDC251;\\\n
}\\\n
.ace-chaos .ace_constant.ace_library {\\\n
color:#8DFF0A;\\\n
}\\\n
.ace-chaos .ace_constant.ace_numeric {\\\n
color:#58C554;\\\n
}\\\n
.ace-chaos .ace_invalid {\\\n
color:#FFFFFF;\\\n
background-color:#990000;\\\n
}\\\n
.ace-chaos .ace_invalid.ace_deprecated {\\\n
color:#FFFFFF;\\\n
background-color:#990000;\\\n
}\\\n
.ace-chaos .ace_support {\\\n
color: #999;\\\n
}\\\n
.ace-chaos .ace_support.ace_function {\\\n
color:#00AEEF;\\\n
}\\\n
.ace-chaos .ace_function {\\\n
color:#00AEEF;\\\n
}\\\n
.ace-chaos .ace_string {\\\n
color:#58C554;\\\n
}\\\n
.ace-chaos .ace_comment {\\\n
color:#555;\\\n
font-style:italic;\\\n
padding-bottom: 0px;\\\n
}\\\n
.ace-chaos .ace_variable {\\\n
color:#997744;\\\n
}\\\n
.ace-chaos .ace_meta.ace_tag {\\\n
color:#BE53E6;\\\n
}\\\n
.ace-chaos .ace_entity.ace_other.ace_attribute-name {\\\n
color:#FFFF89;\\\n
}\\\n
.ace-chaos .ace_markup.ace_underline {\\\n
text-decoration: underline;\\\n
}\\\n
.ace-chaos .ace_fold-widget {\\\n
text-align: center;\\\n
}\\\n
.ace-chaos .ace_fold-widget:hover {\\\n
color: #777;\\\n
}\\\n
.ace-chaos .ace_fold-widget.ace_start,\\\n
.ace-chaos .ace_fold-widget.ace_end,\\\n
.ace-chaos .ace_fold-widget.ace_closed{\\\n
background: none;\\\n
border: none;\\\n
box-shadow: none;\\\n
}\\\n
.ace-chaos .ace_fold-widget.ace_start:after {\\\n
content: \'▾\'\\\n
}\\\n
.ace-chaos .ace_fold-widget.ace_end:after {\\\n
content: \'▴\'\\\n
}\\\n
.ace-chaos .ace_fold-widget.ace_closed:after {\\\n
content: \'‣\'\\\n
}\\\n
.ace-chaos .ace_indent-guide {\\\n
border-right:1px dotted #333;\\\n
margin-right:-1px;\\\n
}\\\n
.ace-chaos .ace_fold { \\\n
background: #222; \\\n
border-radius: 3px; \\\n
color: #7AF; \\\n
border: none; \\\n
}\\\n
.ace-chaos .ace_fold:hover {\\\n
background: #CCC; \\\n
color: #000;\\\n
}\\\n
";\n
\n
var dom = require("../lib/dom");\n
dom.importCssString(exports.cssText, exports.cssClass);\n
\n
});</string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>4455</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
