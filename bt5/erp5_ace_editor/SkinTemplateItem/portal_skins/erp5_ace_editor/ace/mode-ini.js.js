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
            <value> <string>ts83646622.02</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>mode-ini.js</string> </value>
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
 *\n
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
define(\'ace/mode/ini\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text\', \'ace/tokenizer\', \'ace/mode/ini_highlight_rules\', \'ace/mode/folding/ini\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextMode = require("./text").Mode;\n
var Tokenizer = require("../tokenizer").Tokenizer;\n
var IniHighlightRules = require("./ini_highlight_rules").IniHighlightRules;\n
var FoldMode = require("./folding/ini").FoldMode;\n
\n
var Mode = function() {\n
    this.HighlightRules = IniHighlightRules;\n
    this.foldingRules = new FoldMode();\n
};\n
oop.inherits(Mode, TextMode);\n
\n
(function() {\n
    this.lineCommentStart = ";";\n
    this.blockComment = {start: "/*", end: "*/"};\n
}).call(Mode.prototype);\n
\n
exports.Mode = Mode;\n
});\n
\n
define(\'ace/mode/ini_highlight_rules\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text_highlight_rules\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;\n
\n
var escapeRe = "\\\\\\\\(?:[\\\\\\\\0abtrn;#=:]|x[a-fA-F\\\\d]{4})";\n
\n
var IniHighlightRules = function() {\n
    this.$rules = {\n
        start: [{\n
            token: \'punctuation.definition.comment.ini\',\n
            regex: \'#.*\',\n
            push_: [{\n
                token: \'comment.line.number-sign.ini\',\n
                regex: \'$|^\',\n
                next: \'pop\'\n
            }, {\n
                defaultToken: \'comment.line.number-sign.ini\'\n
            }]\n
        }, {\n
            token: \'punctuation.definition.comment.ini\',\n
            regex: \';.*\',\n
            push_: [{\n
                token: \'comment.line.semicolon.ini\',\n
                regex: \'$|^\',\n
                next: \'pop\'\n
            }, {\n
                defaultToken: \'comment.line.semicolon.ini\'\n
            }]\n
        }, {\n
            token: [\'keyword.other.definition.ini\', \'text\', \'punctuation.separator.key-value.ini\'],\n
            regex: \'\\\\b([a-zA-Z0-9_.-]+)\\\\b(\\\\s*)(=)\'\n
        }, {\n
            token: [\'punctuation.definition.entity.ini\', \'constant.section.group-title.ini\', \'punctuation.definition.entity.ini\'],\n
            regex: \'^(\\\\[)(.*?)(\\\\])\'\n
        }, {\n
            token: \'punctuation.definition.string.begin.ini\',\n
            regex: "\'",\n
            push: [{\n
                token: \'punctuation.definition.string.end.ini\',\n
                regex: "\'",\n
                next: \'pop\'\n
            }, {\n
                token: "constant.language.escape",\n
                regex: escapeRe\n
            }, {\n
                defaultToken: \'string.quoted.single.ini\'\n
            }]\n
        }, {\n
            token: \'punctuation.definition.string.begin.ini\',\n
            regex: \'"\',\n
            push: [{\n
                token: "constant.language.escape",\n
                regex: escapeRe\n
            }, {\n
                token: \'punctuation.definition.string.end.ini\',\n
                regex: \'"\',\n
                next: \'pop\'\n
            }, {\n
                defaultToken: \'string.quoted.double.ini\'\n
            }]\n
        }]\n
    };\n
\n
    this.normalizeRules();\n
};\n
\n
IniHighlightRules.metaData = {\n
    fileTypes: [\'ini\', \'conf\'],\n
    keyEquivalent: \'^~I\',\n
    name: \'Ini\',\n
    scopeName: \'source.ini\'\n
};\n
\n
\n
oop.inherits(IniHighlightRules, TextHighlightRules);\n
\n
exports.IniHighlightRules = IniHighlightRules;\n
});\n
\n
define(\'ace/mode/folding/ini\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/range\', \'ace/mode/folding/fold_mode\'], function(require, exports, module) {\n
\n
\n
var oop = require("../../lib/oop");\n
var Range = require("../../range").Range;\n
var BaseFoldMode = require("./fold_mode").FoldMode;\n
\n
var FoldMode = exports.FoldMode = function() {\n
};\n
oop.inherits(FoldMode, BaseFoldMode);\n
\n
(function() {\n
\n
    this.foldingStartMarker = /^\\s*\\[([^\\])]*)]\\s*(?:$|[;#])/;\n
\n
    this.getFoldWidgetRange = function(session, foldStyle, row) {\n
        var re = this.foldingStartMarker;\n
        var line = session.getLine(row);\n
        \n
        var m = line.match(re);\n
        \n
        if (!m) return;\n
        \n
        var startName = m[1] + ".";\n
        \n
        var startColumn = line.length;\n
        var maxRow = session.getLength();\n
        var startRow = row;\n
        var endRow = row;\n
\n
        while (++row < maxRow) {\n
            line = session.getLine(row);\n
            if (/^\\s*$/.test(line))\n
                continue;\n
            m = line.match(re);\n
            if (m && m[1].lastIndexOf(startName, 0) !== 0)\n
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
            <value> <int>6342</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
