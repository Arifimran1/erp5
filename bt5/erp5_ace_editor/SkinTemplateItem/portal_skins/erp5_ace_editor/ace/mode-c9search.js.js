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
            <value> <string>ts83646622.43</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>mode-c9search.js</string> </value>
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
define(\'ace/mode/c9search\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text\', \'ace/tokenizer\', \'ace/mode/c9search_highlight_rules\', \'ace/mode/matching_brace_outdent\', \'ace/mode/folding/c9search\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextMode = require("./text").Mode;\n
var Tokenizer = require("../tokenizer").Tokenizer;\n
var C9SearchHighlightRules = require("./c9search_highlight_rules").C9SearchHighlightRules;\n
var MatchingBraceOutdent = require("./matching_brace_outdent").MatchingBraceOutdent;\n
var C9StyleFoldMode = require("./folding/c9search").FoldMode;\n
\n
var Mode = function() {\n
    this.HighlightRules = C9SearchHighlightRules;\n
    this.$outdent = new MatchingBraceOutdent();\n
    this.foldingRules = new C9StyleFoldMode();\n
};\n
oop.inherits(Mode, TextMode);\n
\n
(function() {\n
    \n
    this.getNextLineIndent = function(state, line, tab) {\n
        var indent = this.$getIndent(line);\n
        return indent;\n
    };\n
\n
    this.checkOutdent = function(state, line, input) {\n
        return this.$outdent.checkOutdent(line, input);\n
    };\n
\n
    this.autoOutdent = function(state, doc, row) {\n
        this.$outdent.autoOutdent(doc, row);\n
    };\n
\n
}).call(Mode.prototype);\n
\n
exports.Mode = Mode;\n
\n
});\n
\n
define(\'ace/mode/c9search_highlight_rules\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text_highlight_rules\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;\n
\n
var C9SearchHighlightRules = function() {\n
    this.$rules = {\n
        "start" : [\n
            {\n
                token : ["c9searchresults.constant.numeric", "c9searchresults.text", "c9searchresults.text"],\n
                regex : "(^\\\\s+[0-9]+)(:\\\\s*)(.+)"\n
            },\n
            {\n
                token : ["string", "text"], // single line\n
                regex : "(.+)(:$)"\n
            }\n
        ]\n
    };\n
};\n
\n
oop.inherits(C9SearchHighlightRules, TextHighlightRules);\n
\n
exports.C9SearchHighlightRules = C9SearchHighlightRules;\n
\n
});\n
\n
define(\'ace/mode/matching_brace_outdent\', [\'require\', \'exports\', \'module\' , \'ace/range\'], function(require, exports, module) {\n
\n
\n
var Range = require("../range").Range;\n
\n
var MatchingBraceOutdent = function() {};\n
\n
(function() {\n
\n
    this.checkOutdent = function(line, input) {\n
        if (! /^\\s+$/.test(line))\n
            return false;\n
\n
        return /^\\s*\\}/.test(input);\n
    };\n
\n
    this.autoOutdent = function(doc, row) {\n
        var line = doc.getLine(row);\n
        var match = line.match(/^(\\s*\\})/);\n
\n
        if (!match) return 0;\n
\n
        var column = match[1].length;\n
        var openBracePos = doc.findMatchingBracket({row: row, column: column});\n
\n
        if (!openBracePos || openBracePos.row == row) return 0;\n
\n
        var indent = this.$getIndent(doc.getLine(openBracePos.row));\n
        doc.replace(new Range(row, 0, row, column-1), indent);\n
    };\n
\n
    this.$getIndent = function(line) {\n
        return line.match(/^\\s*/)[0];\n
    };\n
\n
}).call(MatchingBraceOutdent.prototype);\n
\n
exports.MatchingBraceOutdent = MatchingBraceOutdent;\n
});\n
\n
\n
define(\'ace/mode/folding/c9search\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/range\', \'ace/mode/folding/fold_mode\'], function(require, exports, module) {\n
\n
\n
var oop = require("../../lib/oop");\n
var Range = require("../../range").Range;\n
var BaseFoldMode = require("./fold_mode").FoldMode;\n
\n
var FoldMode = exports.FoldMode = function() {};\n
oop.inherits(FoldMode, BaseFoldMode);\n
\n
(function() {\n
\n
    this.foldingStartMarker = /^(\\S.*\\:|Searching for.*)$/;\n
    this.foldingStopMarker = /^(\\s+|Found.*)$/;\n
    \n
    this.getFoldWidgetRange = function(session, foldStyle, row) {\n
        var lines = session.doc.getAllLines(row);\n
        var line = lines[row];\n
        var level1 = /^(Found.*|Searching for.*)$/;\n
        var level2 = /^(\\S.*\\:|\\s*)$/;\n
        var re = level1.test(line) ? level1 : level2;\n
\n
        if (this.foldingStartMarker.test(line)) {            \n
            for (var i = row + 1, l = session.getLength(); i < l; i++) {\n
                if (re.test(lines[i]))\n
                    break;\n
            }\n
\n
            return new Range(row, line.length, i, 0);\n
        }\n
\n
        if (this.foldingStopMarker.test(line)) {\n
            for (var i = row - 1; i >= 0; i--) {\n
                line = lines[i];\n
                if (re.test(line))\n
                    break;\n
            }\n
\n
            return new Range(i, line.length, row, 0);\n
        }\n
    };\n
    \n
}).call(FoldMode.prototype);\n
\n
});\n
\n


]]></string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>6195</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
