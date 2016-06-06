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
            <value> <string>ts83646620.17</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>theme-tomorrow.js</string> </value>
        </item>
        <item>
            <key> <string>content_type</string> </key>
            <value> <string>application/javascript</string> </value>
        </item>
        <item>
            <key> <string>data</string> </key>
            <value> <string>/* ***** BEGIN LICENSE BLOCK *****\n
 * Distributed under the BSD license:\n
 *\n
 * Copyright (c) 2010, Ajax.org B.V.\n
 * All rights reserved.\n
 *\n
 * Redistribution and use in source and binary forms, with or without\n
 * modification, are permitted provided that the following conditions are met:\n
 *     * Redistributions of source code must retain the above copyright\n
 *       notice, this list of conditions and the following disclaimer.\n
 *     * Redistributions in binary form must reproduce the above copyright\n
 *       notice, this list of conditions and the following disclaimer in the\n
 *       documentation and/or other materials provided with the distribution.\n
 *     * Neither the name of Ajax.org B.V. nor the\n
 *       names of its contributors may be used to endorse or promote products\n
 *       derived from this software without specific prior written permission.\n
 * \n
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\n
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n
 * DISCLAIMED. IN NO EVENT SHALL AJAX.ORG B.V. BE LIABLE FOR ANY\n
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND\n
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n
 *\n
 * ***** END LICENSE BLOCK ***** */\n
\n
define(\'ace/theme/tomorrow\', [\'require\', \'exports\', \'module\' , \'ace/lib/dom\'], function(require, exports, module) {\n
\n
exports.isDark = false;\n
exports.cssClass = "ace-tomorrow";\n
exports.cssText = ".ace-tomorrow .ace_gutter {\\\n
background: #f6f6f6;\\\n
color: #4D4D4C\\\n
}\\\n
.ace-tomorrow .ace_print-margin {\\\n
width: 1px;\\\n
background: #f6f6f6\\\n
}\\\n
.ace-tomorrow {\\\n
background-color: #FFFFFF;\\\n
color: #4D4D4C\\\n
}\\\n
.ace-tomorrow .ace_cursor {\\\n
color: #AEAFAD\\\n
}\\\n
.ace-tomorrow .ace_marker-layer .ace_selection {\\\n
background: #D6D6D6\\\n
}\\\n
.ace-tomorrow.ace_multiselect .ace_selection.ace_start {\\\n
box-shadow: 0 0 3px 0px #FFFFFF;\\\n
border-radius: 2px\\\n
}\\\n
.ace-tomorrow .ace_marker-layer .ace_step {\\\n
background: rgb(255, 255, 0)\\\n
}\\\n
.ace-tomorrow .ace_marker-layer .ace_bracket {\\\n
margin: -1px 0 0 -1px;\\\n
border: 1px solid #D1D1D1\\\n
}\\\n
.ace-tomorrow .ace_marker-layer .ace_active-line {\\\n
background: #EFEFEF\\\n
}\\\n
.ace-tomorrow .ace_gutter-active-line {\\\n
background-color : #dcdcdc\\\n
}\\\n
.ace-tomorrow .ace_marker-layer .ace_selected-word {\\\n
border: 1px solid #D6D6D6\\\n
}\\\n
.ace-tomorrow .ace_invisible {\\\n
color: #D1D1D1\\\n
}\\\n
.ace-tomorrow .ace_keyword,\\\n
.ace-tomorrow .ace_meta,\\\n
.ace-tomorrow .ace_storage,\\\n
.ace-tomorrow .ace_storage.ace_type,\\\n
.ace-tomorrow .ace_support.ace_type {\\\n
color: #8959A8\\\n
}\\\n
.ace-tomorrow .ace_keyword.ace_operator {\\\n
color: #3E999F\\\n
}\\\n
.ace-tomorrow .ace_constant.ace_character,\\\n
.ace-tomorrow .ace_constant.ace_language,\\\n
.ace-tomorrow .ace_constant.ace_numeric,\\\n
.ace-tomorrow .ace_keyword.ace_other.ace_unit,\\\n
.ace-tomorrow .ace_support.ace_constant,\\\n
.ace-tomorrow .ace_variable.ace_parameter {\\\n
color: #F5871F\\\n
}\\\n
.ace-tomorrow .ace_constant.ace_other {\\\n
color: #666969\\\n
}\\\n
.ace-tomorrow .ace_invalid {\\\n
color: #FFFFFF;\\\n
background-color: #C82829\\\n
}\\\n
.ace-tomorrow .ace_invalid.ace_deprecated {\\\n
color: #FFFFFF;\\\n
background-color: #8959A8\\\n
}\\\n
.ace-tomorrow .ace_fold {\\\n
background-color: #4271AE;\\\n
border-color: #4D4D4C\\\n
}\\\n
.ace-tomorrow .ace_entity.ace_name.ace_function,\\\n
.ace-tomorrow .ace_support.ace_function,\\\n
.ace-tomorrow .ace_variable {\\\n
color: #4271AE\\\n
}\\\n
.ace-tomorrow .ace_support.ace_class,\\\n
.ace-tomorrow .ace_support.ace_type {\\\n
color: #C99E00\\\n
}\\\n
.ace-tomorrow .ace_heading,\\\n
.ace-tomorrow .ace_string {\\\n
color: #718C00\\\n
}\\\n
.ace-tomorrow .ace_entity.ace_name.ace_tag,\\\n
.ace-tomorrow .ace_entity.ace_other.ace_attribute-name,\\\n
.ace-tomorrow .ace_meta.ace_tag,\\\n
.ace-tomorrow .ace_string.ace_regexp,\\\n
.ace-tomorrow .ace_variable {\\\n
color: #C82829\\\n
}\\\n
.ace-tomorrow .ace_comment {\\\n
color: #8E908C\\\n
}\\\n
.ace-tomorrow .ace_indent-guide {\\\n
background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAE0lEQVQImWP4////f4bdu3f/BwAlfgctduB85QAAAABJRU5ErkJggg==) right repeat-y\\\n
}";\n
\n
var dom = require("../lib/dom");\n
dom.importCssString(exports.cssText, exports.cssClass);\n
});\n
</string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>4496</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
