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
            <value> <string>ts83646621.57</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>mode-pascal.js</string> </value>
        </item>
        <item>
            <key> <string>content_type</string> </key>
            <value> <string>application/javascript</string> </value>
        </item>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

/* ***** BEGIN LICENSE BLOCK *****\n
 * Distributed under the BSD license:\n
 *\n
 * Copyright (c) 2012, Ajax.org B.V.\n
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
 *\n
 * Contributor(s):\n
 * \n
 *\n
 *\n
 * ***** END LICENSE BLOCK ***** */\n
\n
define(\'ace/mode/pascal\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text\', \'ace/tokenizer\', \'ace/mode/pascal_highlight_rules\', \'ace/mode/folding/coffee\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextMode = require("./text").Mode;\n
var Tokenizer = require("../tokenizer").Tokenizer;\n
var PascalHighlightRules = require("./pascal_highlight_rules").PascalHighlightRules;\n
var FoldMode = require("./folding/coffee").FoldMode;\n
\n
var Mode = function() {\n
    this.HighlightRules = PascalHighlightRules;\n
    this.foldingRules = new FoldMode();\n
};\n
oop.inherits(Mode, TextMode);\n
\n
(function() {\n
       \n
    this.lineCommentStart = ["--", "//"];\n
    this.blockComment = [\n
        {start: "(*", end: "*)"},\n
        {start: "{", end: "}"}\n
    ];\n
    \n
}).call(Mode.prototype);\n
\n
exports.Mode = Mode;\n
});\n
\n
define(\'ace/mode/pascal_highlight_rules\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text_highlight_rules\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;\n
\n
var PascalHighlightRules = function() {\n
\n
    this.$rules = { start: \n
       [ { caseInsensitive: true,\n
           token: \'keyword.control.pascal\',\n
           regex: \'\\\\b(?:(absolute|abstract|all|and|and_then|array|as|asm|attribute|begin|bindable|case|class|const|constructor|destructor|div|do|do|else|end|except|export|exports|external|far|file|finalization|finally|for|forward|goto|if|implementation|import|in|inherited|initialization|interface|interrupt|is|label|library|mod|module|name|near|nil|not|object|of|only|operator|or|or_else|otherwise|packed|pow|private|program|property|protected|public|published|qualified|record|repeat|resident|restricted|segment|set|shl|shr|then|to|try|type|unit|until|uses|value|var|view|virtual|while|with|xor))\\\\b\' },\n
         { caseInsensitive: true,           \n
           token: \n
            [ \'variable.pascal\', "text",\n
              \'storage.type.prototype.pascal\',\n
              \'entity.name.function.prototype.pascal\' ],\n
           regex: \'\\\\b(function|procedure)(\\\\s+)(\\\\w+)(\\\\.\\\\w+)?(?=(?:\\\\(.*?\\\\))?;\\\\s*(?:attribute|forward|external))\' },\n
         { caseInsensitive: true,\n
           token: \n
            [ \'variable.pascal\', "text",\n
              \'storage.type.function.pascal\',\n
              \'entity.name.function.pascal\' ],\n
           regex: \'\\\\b(function|procedure)(\\\\s+)(\\\\w+)(\\\\.\\\\w+)?\' },\n
         { token: \'constant.numeric.pascal\',\n
           regex: \'\\\\b((0(x|X)[0-9a-fA-F]*)|(([0-9]+\\\\.?[0-9]*)|(\\\\.[0-9]+))((e|E)(\\\\+|-)?[0-9]+)?)(L|l|UL|ul|u|U|F|f|ll|LL|ull|ULL)?\\\\b\' },\n
         { token: \'punctuation.definition.comment.pascal\',\n
           regex: \'--.*$\',\n
           push_: \n
            [ { token: \'comment.line.double-dash.pascal.one\',\n
                regex: \'$\',\n
                next: \'pop\' },\n
              { defaultToken: \'comment.line.double-dash.pascal.one\' } ] },\n
         { token: \'punctuation.definition.comment.pascal\',\n
           regex: \'//.*$\',\n
           push_: \n
            [ { token: \'comment.line.double-slash.pascal.two\',\n
                regex: \'$\',\n
                next: \'pop\' },\n
              { defaultToken: \'comment.line.double-slash.pascal.two\' } ] },\n
         { token: \'punctuation.definition.comment.pascal\',\n
           regex: \'\\\\(\\\\*\',\n
           push: \n
            [ { token: \'punctuation.definition.comment.pascal\',\n
                regex: \'\\\\*\\\\)\',\n
                next: \'pop\' },\n
              { defaultToken: \'comment.block.pascal.one\' } ] },\n
         { token: \'punctuation.definition.comment.pascal\',\n
           regex: \'\\\\{\',\n
           push: \n
            [ { token: \'punctuation.definition.comment.pascal\',\n
                regex: \'\\\\}\',\n
                next: \'pop\' },\n
              { defaultToken: \'comment.block.pascal.two\' } ] },\n
         { token: \'punctuation.definition.string.begin.pascal\',\n
           regex: \'"\',\n
           push: \n
            [ { token: \'constant.character.escape.pascal\', regex: \'\\\\\\\\.\' },\n
              { token: \'punctuation.definition.string.end.pascal\',\n
                regex: \'"\',\n
                next: \'pop\' },\n
              { defaultToken: \'string.quoted.double.pascal\' } ],\n
            },\n
         { token: \'punctuation.definition.string.begin.pascal\',\n
           regex: \'\\\'\',\n
           push: \n
            [ { token: \'constant.character.escape.apostrophe.pascal\',\n
                regex: \'\\\'\\\'\' },\n
              { token: \'punctuation.definition.string.end.pascal\',\n
                regex: \'\\\'\',\n
                next: \'pop\' },\n
              { defaultToken: \'string.quoted.single.pascal\' } ] },\n
          { token: \'keyword.operator\',\n
           regex: \'[+\\\\-;,/*%]|:=|=\' } ] }\n
    \n
    this.normalizeRules();\n
};\n
\n
oop.inherits(PascalHighlightRules, TextHighlightRules);\n
\n
exports.PascalHighlightRules = PascalHighlightRules;\n
});\n
\n
define(\'ace/mode/folding/coffee\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/folding/fold_mode\', \'ace/range\'], function(require, exports, module) {\n
\n
\n
var oop = require("../../lib/oop");\n
var BaseFoldMode = require("./fold_mode").FoldMode;\n
var Range = require("../../range").Range;\n
\n
var FoldMode = exports.FoldMode = function() {};\n
oop.inherits(FoldMode, BaseFoldMode);\n
\n
(function() {\n
\n
    this.getFoldWidgetRange = function(session, foldStyle, row) {\n
        var range = this.indentationBlock(session, row);\n
        if (range)\n
            return range;\n
\n
        var re = /\\S/;\n
        var line = session.getLine(row);\n
        var startLevel = line.search(re);\n
        if (startLevel == -1 || line[startLevel] != "#")\n
            return;\n
\n
        var startColumn = line.length;\n
        var maxRow = session.getLength();\n
        var startRow = row;\n
        var endRow = row;\n
\n
        while (++row < maxRow) {\n
            line = session.getLine(row);\n
            var level = line.search(re);\n
\n
            if (level == -1)\n
                continue;\n
\n
            if (line[level] != "#")\n
                break;\n
\n
            endRow = row;\n
        }\n
\n
        if (endRow > startRow) {\n
            var endColumn = session.getLine(endRow).length;\n
            return new Range(startRow, startColumn, endRow, endColumn);\n
        }\n
    };\n
    this.getFoldWidget = function(session, foldStyle, row) {\n
        var line = session.getLine(row);\n
        var indent = line.search(/\\S/);\n
        var next = session.getLine(row + 1);\n
        var prev = session.getLine(row - 1);\n
        var prevIndent = prev.search(/\\S/);\n
        var nextIndent = next.search(/\\S/);\n
\n
        if (indent == -1) {\n
            session.foldWidgets[row - 1] = prevIndent!= -1 && prevIndent < nextIndent ? "start" : "";\n
            return "";\n
        }\n
        if (prevIndent == -1) {\n
            if (indent == nextIndent && line[indent] == "#" && next[indent] == "#") {\n
                session.foldWidgets[row - 1] = "";\n
                session.foldWidgets[row + 1] = "";\n
                return "start";\n
            }\n
        } else if (prevIndent == indent && line[indent] == "#" && prev[indent] == "#") {\n
            if (session.getLine(row - 2).search(/\\S/) == -1) {\n
                session.foldWidgets[row - 1] = "start";\n
                session.foldWidgets[row + 1] = "";\n
                return "";\n
            }\n
        }\n
\n
        if (prevIndent!= -1 && prevIndent < indent)\n
            session.foldWidgets[row - 1] = "start";\n
        else\n
            session.foldWidgets[row - 1] = "";\n
\n
        if (indent < nextIndent)\n
            return "start";\n
        else\n
            return "";\n
    };\n
\n
}).call(FoldMode.prototype);\n
\n
});\n


]]></string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>9273</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
