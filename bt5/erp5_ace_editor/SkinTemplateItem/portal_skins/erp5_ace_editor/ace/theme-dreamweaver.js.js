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
            <value> <string>ts83646620.8</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>theme-dreamweaver.js</string> </value>
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
define(\'ace/theme/dreamweaver\', [\'require\', \'exports\', \'module\' , \'ace/lib/dom\'], function(require, exports, module) {\n
exports.isDark = false;\n
exports.cssClass = "ace-dreamweaver";\n
exports.cssText = ".ace-dreamweaver .ace_gutter {\\\n
background: #e8e8e8;\\\n
color: #333;\\\n
}\\\n
.ace-dreamweaver .ace_print-margin {\\\n
width: 1px;\\\n
background: #e8e8e8;\\\n
}\\\n
.ace-dreamweaver {\\\n
background-color: #FFFFFF;\\\n
}\\\n
.ace-dreamweaver .ace_fold {\\\n
background-color: #757AD8;\\\n
}\\\n
.ace-dreamweaver .ace_cursor {\\\n
color: black;\\\n
}\\\n
.ace-dreamweaver .ace_invisible {\\\n
color: rgb(191, 191, 191);\\\n
}\\\n
.ace-dreamweaver .ace_storage,\\\n
.ace-dreamweaver .ace_keyword {\\\n
color: blue;\\\n
}\\\n
.ace-dreamweaver .ace_constant.ace_buildin {\\\n
color: rgb(88, 72, 246);\\\n
}\\\n
.ace-dreamweaver .ace_constant.ace_language {\\\n
color: rgb(88, 92, 246);\\\n
}\\\n
.ace-dreamweaver .ace_constant.ace_library {\\\n
color: rgb(6, 150, 14);\\\n
}\\\n
.ace-dreamweaver .ace_invalid {\\\n
background-color: rgb(153, 0, 0);\\\n
color: white;\\\n
}\\\n
.ace-dreamweaver .ace_support.ace_function {\\\n
color: rgb(60, 76, 114);\\\n
}\\\n
.ace-dreamweaver .ace_support.ace_constant {\\\n
color: rgb(6, 150, 14);\\\n
}\\\n
.ace-dreamweaver .ace_support.ace_type,\\\n
.ace-dreamweaver .ace_support.ace_class {\\\n
color: #009;\\\n
}\\\n
.ace-dreamweaver .ace_support.ace_php_tag {\\\n
color: #f00;\\\n
}\\\n
.ace-dreamweaver .ace_keyword.ace_operator {\\\n
color: rgb(104, 118, 135);\\\n
}\\\n
.ace-dreamweaver .ace_string {\\\n
color: #00F;\\\n
}\\\n
.ace-dreamweaver .ace_comment {\\\n
color: rgb(76, 136, 107);\\\n
}\\\n
.ace-dreamweaver .ace_comment.ace_doc {\\\n
color: rgb(0, 102, 255);\\\n
}\\\n
.ace-dreamweaver .ace_comment.ace_doc.ace_tag {\\\n
color: rgb(128, 159, 191);\\\n
}\\\n
.ace-dreamweaver .ace_constant.ace_numeric {\\\n
color: rgb(0, 0, 205);\\\n
}\\\n
.ace-dreamweaver .ace_variable {\\\n
color: #06F\\\n
}\\\n
.ace-dreamweaver .ace_xml-pe {\\\n
color: rgb(104, 104, 91);\\\n
}\\\n
.ace-dreamweaver .ace_entity.ace_name.ace_function {\\\n
color: #00F;\\\n
}\\\n
.ace-dreamweaver .ace_heading {\\\n
color: rgb(12, 7, 255);\\\n
}\\\n
.ace-dreamweaver .ace_list {\\\n
color:rgb(185, 6, 144);\\\n
}\\\n
.ace-dreamweaver .ace_marker-layer .ace_selection {\\\n
background: rgb(181, 213, 255);\\\n
}\\\n
.ace-dreamweaver .ace_marker-layer .ace_step {\\\n
background: rgb(252, 255, 0);\\\n
}\\\n
.ace-dreamweaver .ace_marker-layer .ace_stack {\\\n
background: rgb(164, 229, 101);\\\n
}\\\n
.ace-dreamweaver .ace_marker-layer .ace_bracket {\\\n
margin: -1px 0 0 -1px;\\\n
border: 1px solid rgb(192, 192, 192);\\\n
}\\\n
.ace-dreamweaver .ace_marker-layer .ace_active-line {\\\n
background: rgba(0, 0, 0, 0.07);\\\n
}\\\n
.ace-dreamweaver .ace_marker-layer .ace_selected-word {\\\n
background: rgb(250, 250, 255);\\\n
border: 1px solid rgb(200, 200, 250);\\\n
}\\\n
.ace-dreamweaver .ace_meta.ace_tag {\\\n
color:#009;\\\n
}\\\n
.ace-dreamweaver .ace_meta.ace_tag.ace_anchor {\\\n
color:#060;\\\n
}\\\n
.ace-dreamweaver .ace_meta.ace_tag.ace_form {\\\n
color:#F90;\\\n
}\\\n
.ace-dreamweaver .ace_meta.ace_tag.ace_image {\\\n
color:#909;\\\n
}\\\n
.ace-dreamweaver .ace_meta.ace_tag.ace_script {\\\n
color:#900;\\\n
}\\\n
.ace-dreamweaver .ace_meta.ace_tag.ace_style {\\\n
color:#909;\\\n
}\\\n
.ace-dreamweaver .ace_meta.ace_tag.ace_table {\\\n
color:#099;\\\n
}\\\n
.ace-dreamweaver .ace_string.ace_regex {\\\n
color: rgb(255, 0, 0)\\\n
}\\\n
.ace-dreamweaver .ace_indent-guide {\\\n
background: url(\\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAE0lEQVQImWP4////f4bLly//BwAmVgd1/w11/gAAAABJRU5ErkJggg==\\") right repeat-y;\\\n
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
            <value> <int>5077</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
