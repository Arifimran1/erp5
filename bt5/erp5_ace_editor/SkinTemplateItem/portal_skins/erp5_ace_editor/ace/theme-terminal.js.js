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
            <value> <string>ts83646620.63</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>theme-terminal.js</string> </value>
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
 * \n
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
define(\'ace/theme/terminal\', [\'require\', \'exports\', \'module\' , \'ace/lib/dom\'], function(require, exports, module) {\n
\n
exports.isDark = true;\n
exports.cssClass = "ace-terminal-theme";\n
exports.cssText = ".ace-terminal-theme .ace_gutter {\\\n
background: #1a0005;\\\n
color: steelblue\\\n
}\\\n
.ace-terminal-theme .ace_print-margin {\\\n
width: 1px;\\\n
background: #1a1a1a\\\n
}\\\n
.ace-terminal-theme {\\\n
background-color: black;\\\n
color: #DEDEDE\\\n
}\\\n
.ace-terminal-theme .ace_cursor {\\\n
color: #9F9F9F\\\n
}\\\n
.ace-terminal-theme .ace_marker-layer .ace_selection {\\\n
background: #424242\\\n
}\\\n
.ace-terminal-theme.ace_multiselect .ace_selection.ace_start {\\\n
box-shadow: 0 0 3px 0px black;\\\n
border-radius: 2px\\\n
}\\\n
.ace-terminal-theme .ace_marker-layer .ace_step {\\\n
background: rgb(0, 0, 0)\\\n
}\\\n
.ace-terminal-theme .ace_marker-layer .ace_bracket {\\\n
background: #090;\\\n
}\\\n
.ace-terminal-theme .ace_marker-layer .ace_bracket-start {\\\n
background: #090;\\\n
}\\\n
.ace-terminal-theme .ace_marker-layer .ace_bracket-unmatched {\\\n
margin: -1px 0 0 -1px;\\\n
border: 1px solid #900\\\n
}\\\n
.ace-terminal-theme .ace_marker-layer .ace_active-line {\\\n
background: #2A2A2A\\\n
}\\\n
.ace-terminal-theme .ace_gutter-active-line {\\\n
background-color: #2A112A\\\n
}\\\n
.ace-terminal-theme .ace_marker-layer .ace_selected-word {\\\n
border: 1px solid #424242\\\n
}\\\n
.ace-terminal-theme .ace_invisible {\\\n
color: #343434\\\n
}\\\n
.ace-terminal-theme .ace_keyword,\\\n
.ace-terminal-theme .ace_meta,\\\n
.ace-terminal-theme .ace_storage,\\\n
.ace-terminal-theme .ace_storage.ace_type,\\\n
.ace-terminal-theme .ace_support.ace_type {\\\n
color: tomato\\\n
}\\\n
.ace-terminal-theme .ace_keyword.ace_operator {\\\n
color: deeppink\\\n
}\\\n
.ace-terminal-theme .ace_constant.ace_character,\\\n
.ace-terminal-theme .ace_constant.ace_language,\\\n
.ace-terminal-theme .ace_constant.ace_numeric,\\\n
.ace-terminal-theme .ace_keyword.ace_other.ace_unit,\\\n
.ace-terminal-theme .ace_support.ace_constant,\\\n
.ace-terminal-theme .ace_variable.ace_parameter {\\\n
color: #E78C45\\\n
}\\\n
.ace-terminal-theme .ace_constant.ace_other {\\\n
color: gold\\\n
}\\\n
.ace-terminal-theme .ace_invalid {\\\n
color: yellow;\\\n
background-color: red\\\n
}\\\n
.ace-terminal-theme .ace_invalid.ace_deprecated {\\\n
color: #CED2CF;\\\n
background-color: #B798BF\\\n
}\\\n
.ace-terminal-theme .ace_fold {\\\n
background-color: #7AA6DA;\\\n
border-color: #DEDEDE\\\n
}\\\n
.ace-terminal-theme .ace_entity.ace_name.ace_function,\\\n
.ace-terminal-theme .ace_support.ace_function,\\\n
.ace-terminal-theme .ace_variable {\\\n
color: #7AA6DA\\\n
}\\\n
.ace-terminal-theme .ace_support.ace_class,\\\n
.ace-terminal-theme .ace_support.ace_type {\\\n
color: #E7C547\\\n
}\\\n
.ace-terminal-theme .ace_heading,\\\n
.ace-terminal-theme .ace_string {\\\n
color: #B9CA4A\\\n
}\\\n
.ace-terminal-theme .ace_entity.ace_name.ace_tag,\\\n
.ace-terminal-theme .ace_entity.ace_other.ace_attribute-name,\\\n
.ace-terminal-theme .ace_meta.ace_tag,\\\n
.ace-terminal-theme .ace_string.ace_regexp,\\\n
.ace-terminal-theme .ace_variable {\\\n
color: #D54E53\\\n
}\\\n
.ace-terminal-theme .ace_comment {\\\n
color: orangered\\\n
}\\\n
.ace-terminal-theme .ace_indent-guide {\\\n
background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAEklEQVQImWNgYGBgYLBWV/8PAAK4AYnhiq+xAAAAAElFTkSuQmCC) right repeat-y;\\\n
}\\\n
";\n
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
            <value> <int>4905</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
