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
            <value> <string>ts83646620.31</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>mode-jack.js</string> </value>
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
define(\'ace/mode/jack\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text\', \'ace/tokenizer\', \'ace/mode/jack_highlight_rules\', \'ace/mode/matching_brace_outdent\', \'ace/mode/behaviour/cstyle\', \'ace/mode/folding/cstyle\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextMode = require("./text").Mode;\n
var Tokenizer = require("../tokenizer").Tokenizer;\n
var HighlightRules = require("./jack_highlight_rules").JackHighlightRules;\n
var MatchingBraceOutdent = require("./matching_brace_outdent").MatchingBraceOutdent;\n
var CstyleBehaviour = require("./behaviour/cstyle").CstyleBehaviour;\n
var CStyleFoldMode = require("./folding/cstyle").FoldMode;\n
\n
var Mode = function() {\n
    this.HighlightRules = HighlightRules;\n
    this.$outdent = new MatchingBraceOutdent();\n
    this.$behaviour = new CstyleBehaviour();\n
    this.foldingRules = new CStyleFoldMode();\n
};\n
oop.inherits(Mode, TextMode);\n
\n
(function() {\n
\n
    this.lineCommentStart = "--";\n
\n
    this.getNextLineIndent = function(state, line, tab) {\n
        var indent = this.$getIndent(line);\n
\n
        if (state == "start") {\n
            var match = line.match(/^.*[\\{\\(\\[]\\s*$/);\n
            if (match) {\n
                indent += tab;\n
            }\n
        }\n
\n
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
\n
}).call(Mode.prototype);\n
\n
exports.Mode = Mode;\n
});\n
\n
define(\'ace/mode/jack_highlight_rules\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text_highlight_rules\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;\n
\n
var JackHighlightRules = function() {\n
    this.$rules = {\n
        "start" : [\n
            {\n
                token : "string",\n
                regex : \'"\',\n
                next  : "string2"\n
            }, {\n
                token : "string",\n
                regex : "\'",\n
                next  : "string1"\n
            }, {\n
                token : "constant.numeric", // hex\n
                regex: "-?0[xX][0-9a-fA-F]+\\\\b"\n
            }, {\n
                token : "constant.numeric", // float\n
                regex : "(?:0|[-+]?[1-9][0-9]*)\\\\b"\n
            }, {\n
                token : "constant.binary",\n
                regex : "<[0-9A-Fa-f][0-9A-Fa-f](\\\\s+[0-9A-Fa-f][0-9A-Fa-f])*>"\n
            }, {\n
                token : "constant.language.boolean",\n
                regex : "(?:true|false)\\\\b"\n
            }, {\n
                token : "constant.language.null",\n
                regex : "null\\\\b"\n
            }, {\n
                token : "storage.type",\n
                regex: "(?:Integer|Boolean|Null|String|Buffer|Tuple|List|Object|Function|Coroutine|Form)\\\\b"\n
            }, {\n
                token : "keyword",\n
                regex : "(?:return|abort|vars|for|delete|in|is|escape|exec|split|and|if|elif|else|while)\\\\b"\n
            }, {\n
                token : "language.builtin",\n
                regex : "(?:lines|source|parse|read-stream|interval|substr|parseint|write|print|range|rand|inspect|bind|i-values|i-pairs|i-map|i-filter|i-chunk|i-all\\\\?|i-any\\\\?|i-collect|i-zip|i-merge|i-each)\\\\b"\n
            }, {\n
                token : "comment",\n
                regex : "--.*$"\n
            }, {\n
                token : "paren.lparen",\n
                regex : "[[({]"\n
            }, {\n
                token : "paren.rparen",\n
                regex : "[\\\\])}]"\n
            }, {\n
                token : "storage.form",\n
                regex : "@[a-z]+"\n
            }, {\n
                token : "constant.other.symbol",\n
                regex : \':+[a-zA-Z_]([-]?[a-zA-Z0-9_])*[?!]?\'\n
            }, {\n
                token : "variable",\n
                regex : \'[a-zA-Z_]([-]?[a-zA-Z0-9_])*[?!]?\'\n
            }, {\n
                token : "keyword.operator",\n
                regex : "\\\\|\\\\||\\\\^\\\\^|&&|!=|==|<=|<|>=|>|\\\\+|-|\\\\*|\\\\/|\\\\^|\\\\%|\\\\#|\\\\!"\n
            }, {\n
                token : "text",\n
                regex : "\\\\s+"\n
            }\n
        ],\n
        "string1" : [\n
            {\n
                token : "constant.language.escape",\n
                regex : /\\\\(?:x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|[\'"\\\\\\/bfnrt])/\n
            }, {\n
                token : "string",\n
                regex : "[^\'\\\\\\\\]+"\n
            }, {\n
                token : "string",\n
                regex : "\'",\n
                next  : "start"\n
            }, {\n
                token : "string",\n
                regex : "",\n
                next  : "start"\n
            }\n
        ],\n
        "string2" : [\n
            {\n
                token : "constant.language.escape",\n
                regex : /\\\\(?:x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|[\'"\\\\\\/bfnrt])/\n
            }, {\n
                token : "string",\n
                regex : \'[^"\\\\\\\\]+\'\n
            }, {\n
                token : "string",\n
                regex : \'"\',\n
                next  : "start"\n
            }, {\n
                token : "string",\n
                regex : "",\n
                next  : "start"\n
            }\n
        ]\n
    };\n
    \n
};\n
\n
oop.inherits(JackHighlightRules, TextHighlightRules);\n
\n
exports.JackHighlightRules = JackHighlightRules;\n
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
define(\'ace/mode/behaviour/cstyle\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/behaviour\', \'ace/token_iterator\', \'ace/lib/lang\'], function(require, exports, module) {\n
\n
\n
var oop = require("../../lib/oop");\n
var Behaviour = require("../behaviour").Behaviour;\n
var TokenIterator = require("../../token_iterator").TokenIterator;\n
var lang = require("../../lib/lang");\n
\n
var SAFE_INSERT_IN_TOKENS =\n
    ["text", "paren.rparen", "punctuation.operator"];\n
var SAFE_INSERT_BEFORE_TOKENS =\n
    ["text", "paren.rparen", "punctuation.operator", "comment"];\n
\n
\n
var autoInsertedBrackets = 0;\n
var autoInsertedRow = -1;\n
var autoInsertedLineEnd = "";\n
var maybeInsertedBrackets = 0;\n
var maybeInsertedRow = -1;\n
var maybeInsertedLineStart = "";\n
var maybeInsertedLineEnd = "";\n
\n
var CstyleBehaviour = function () {\n
    \n
    CstyleBehaviour.isSaneInsertion = function(editor, session) {\n
        var cursor = editor.getCursorPosition();\n
        var iterator = new TokenIterator(session, cursor.row, cursor.column);\n
        if (!this.$matchTokenType(iterator.getCurrentToken() || "text", SAFE_INSERT_IN_TOKENS)) {\n
            var iterator2 = new TokenIterator(session, cursor.row, cursor.column + 1);\n
            if (!this.$matchTokenType(iterator2.getCurrentToken() || "text", SAFE_INSERT_IN_TOKENS))\n
                return false;\n
        }\n
        iterator.stepForward();\n
        return iterator.getCurrentTokenRow() !== cursor.row ||\n
            this.$matchTokenType(iterator.getCurrentToken() || "text", SAFE_INSERT_BEFORE_TOKENS);\n
    };\n
    \n
    CstyleBehaviour.$matchTokenType = function(token, types) {\n
        return types.indexOf(token.type || token) > -1;\n
    };\n
    \n
    CstyleBehaviour.recordAutoInsert = function(editor, session, bracket) {\n
        var cursor = editor.getCursorPosition();\n
        var line = session.doc.getLine(cursor.row);\n
        if (!this.isAutoInsertedClosing(cursor, line, autoInsertedLineEnd[0]))\n
            autoInsertedBrackets = 0;\n
        autoInsertedRow = cursor.row;\n
        autoInsertedLineEnd = bracket + line.substr(cursor.column);\n
        autoInsertedBrackets++;\n
    };\n
    \n
    CstyleBehaviour.recordMaybeInsert = function(editor, session, bracket) {\n
        var cursor = editor.getCursorPosition();\n
        var line = session.doc.getLine(cursor.row);\n
        if (!this.isMaybeInsertedClosing(cursor, line))\n
            maybeInsertedBrackets = 0;\n
        maybeInsertedRow = cursor.row;\n
        maybeInsertedLineStart = line.substr(0, cursor.column) + bracket;\n
        maybeInsertedLineEnd = line.substr(cursor.column);\n
        maybeInsertedBrackets++;\n
    };\n
    \n
    CstyleBehaviour.isAutoInsertedClosing = function(cursor, line, bracket) {\n
        return autoInsertedBrackets > 0 &&\n
            cursor.row === autoInsertedRow &&\n
            bracket === autoInsertedLineEnd[0] &&\n
            line.substr(cursor.column) === autoInsertedLineEnd;\n
    };\n
    \n
    CstyleBehaviour.isMaybeInsertedClosing = function(cursor, line) {\n
        return maybeInsertedBrackets > 0 &&\n
            cursor.row === maybeInsertedRow &&\n
            line.substr(cursor.column) === maybeInsertedLineEnd &&\n
            line.substr(0, cursor.column) == maybeInsertedLineStart;\n
    };\n
    \n
    CstyleBehaviour.popAutoInsertedClosing = function() {\n
        autoInsertedLineEnd = autoInsertedLineEnd.substr(1);\n
        autoInsertedBrackets--;\n
    };\n
    \n
    CstyleBehaviour.clearMaybeInsertedClosing = function() {\n
        maybeInsertedBrackets = 0;\n
        maybeInsertedRow = -1;\n
    };\n
\n
    this.add("braces", "insertion", function (state, action, editor, session, text) {\n
        var cursor = editor.getCursorPosition();\n
        var line = session.doc.getLine(cursor.row);\n
        if (text == \'{\') {\n
            var selection = editor.getSelectionRange();\n
            var selected = session.doc.getTextRange(selection);\n
            if (selected !== "" && selected !== "{" && editor.getWrapBehavioursEnabled()) {\n
                return {\n
                    text: \'{\' + selected + \'}\',\n
                    selection: false\n
                };\n
            } else if (CstyleBehaviour.isSaneInsertion(editor, session)) {\n
                if (/[\\]\\}\\)]/.test(line[cursor.column])) {\n
                    CstyleBehaviour.recordAutoInsert(editor, session, "}");\n
                    return {\n
                        text: \'{}\',\n
                        selection: [1, 1]\n
                    };\n
                } else {\n
                    CstyleBehaviour.recordMaybeInsert(editor, session, "{");\n
                    return {\n
                        text: \'{\',\n
                        selection: [1, 1]\n
                    };\n
                }\n
            }\n
        } else if (text == \'}\') {\n
            var rightChar = line.substring(cursor.column, cursor.column + 1);\n
            if (rightChar == \'}\') {\n
                var matching = session.$findOpeningBracket(\'}\', {column: cursor.column + 1, row: cursor.row});\n
                if (matching !== null && CstyleBehaviour.isAutoInsertedClosing(cursor, line, text)) {\n
                    CstyleBehaviour.popAutoInsertedClosing();\n
                    return {\n
                        text: \'\',\n
                        selection: [1, 1]\n
                    };\n
                }\n
            }\n
        } else if (text == "\\n" || text == "\\r\\n") {\n
            var closing = "";\n
            if (CstyleBehaviour.isMaybeInsertedClosing(cursor, line)) {\n
                closing = lang.stringRepeat("}", maybeInsertedBrackets);\n
                CstyleBehaviour.clearMaybeInsertedClosing();\n
            }\n
            var rightChar = line.substring(cursor.column, cursor.column + 1);\n
            if (rightChar == \'}\' || closing !== "") {\n
                var openBracePos = session.findMatchingBracket({row: cursor.row, column: cursor.column}, \'}\');\n
                if (!openBracePos)\n
                     return null;\n
\n
                var indent = this.getNextLineIndent(state, line.substring(0, cursor.column), session.getTabString());\n
                var next_indent = this.$getIndent(line);\n
\n
                return {\n
                    text: \'\\n\' + indent + \'\\n\' + next_indent + closing,\n
                    selection: [1, indent.length, 1, indent.length]\n
                };\n
            }\n
        }\n
    });\n
\n
    this.add("braces", "deletion", function (state, action, editor, session, range) {\n
        var selected = session.doc.getTextRange(range);\n
        if (!range.isMultiLine() && selected == \'{\') {\n
            var line = session.doc.getLine(range.start.row);\n
            var rightChar = line.substring(range.end.column, range.end.column + 1);\n
            if (rightChar == \'}\') {\n
                range.end.column++;\n
                return range;\n
            } else {\n
                maybeInsertedBrackets--;\n
            }\n
        }\n
    });\n
\n
    this.add("parens", "insertion", function (state, action, editor, session, text) {\n
        if (text == \'(\') {\n
            var selection = editor.getSelectionRange();\n
            var selected = session.doc.getTextRange(selection);\n
            if (selected !== "" && editor.getWrapBehavioursEnabled()) {\n
                return {\n
                    text: \'(\' + selected + \')\',\n
                    selection: false\n
                };\n
            } else if (CstyleBehaviour.isSaneInsertion(editor, session)) {\n
                CstyleBehaviour.recordAutoInsert(editor, session, ")");\n
                return {\n
                    text: \'()\',\n
                    selection: [1, 1]\n
                };\n
            }\n
        } else if (text == \')\') {\n
            var cursor = editor.getCursorPosition();\n
            var line = session.doc.getLine(cursor.row);\n
            var rightChar = line.substring(cursor.column, cursor.column + 1);\n
            if (rightChar == \')\') {\n
                var matching = session.$findOpeningBracket(\')\', {column: cursor.column + 1, row: cursor.row});\n
                if (matching !== null && CstyleBehaviour.isAutoInsertedClosing(cursor, line, text)) {\n
                    CstyleBehaviour.popAutoInsertedClosing();\n
                    return {\n
                        text: \'\',\n
                        selection: [1, 1]\n
                    };\n
                }\n
            }\n
        }\n
    });\n
\n
    this.add("parens", "deletion", function (state, action, editor, session, range) {\n
        var selected = session.doc.getTextRange(range);\n
        if (!range.isMultiLine() && selected == \'(\') {\n
            var line = session.doc.getLine(range.start.row);\n
            var rightChar = line.substring(range.start.column + 1, range.start.column + 2);\n
            if (rightChar == \')\') {\n
                range.end.column++;\n
                return range;\n
            }\n
        }\n
    });\n
\n
    this.add("brackets", "insertion", function (state, action, editor, session, text) {\n
        if (text == \'[\') {\n
            var selection = editor.getSelectionRange();\n
            var selected = session.doc.getTextRange(selection);\n
            if (selected !== "" && editor.getWrapBehavioursEnabled()) {\n
                return {\n
                    text: \'[\' + selected + \']\',\n
                    selection: false\n
                };\n
            } else if (CstyleBehaviour.isSaneInsertion(editor, session)) {\n
                CstyleBehaviour.recordAutoInsert(editor, session, "]");\n
                return {\n
                    text: \'[]\',\n
                    selection: [1, 1]\n
                };\n
            }\n
        } else if (text == \']\') {\n
            var cursor = editor.getCursorPosition();\n
            var line = session.doc.getLine(cursor.row);\n
            var rightChar = line.substring(cursor.column, cursor.column + 1);\n
            if (rightChar == \']\') {\n
                var matching = session.$findOpeningBracket(\']\', {column: cursor.column + 1, row: cursor.row});\n
                if (matching !== null && CstyleBehaviour.isAutoInsertedClosing(cursor, line, text)) {\n
                    CstyleBehaviour.popAutoInsertedClosing();\n
                    return {\n
                        text: \'\',\n
                        selection: [1, 1]\n
                    };\n
                }\n
            }\n
        }\n
    });\n
\n
    this.add("brackets", "deletion", function (state, action, editor, session, range) {\n
        var selected = session.doc.getTextRange(range);\n
        if (!range.isMultiLine() && selected == \'[\') {\n
            var line = session.doc.getLine(range.start.row);\n
            var rightChar = line.substring(range.start.column + 1, range.start.column + 2);\n
            if (rightChar == \']\') {\n
                range.end.column++;\n
                return range;\n
            }\n
        }\n
    });\n
\n
    this.add("string_dquotes", "insertion", function (state, action, editor, session, text) {\n
        if (text == \'"\' || text == "\'") {\n
            var quote = text;\n
            var selection = editor.getSelectionRange();\n
            var selected = session.doc.getTextRange(selection);\n
            if (selected !== "" && selected !== "\'" && selected != \'"\' && editor.getWrapBehavioursEnabled()) {\n
                return {\n
                    text: quote + selected + quote,\n
                    selection: false\n
                };\n
            } else {\n
                var cursor = editor.getCursorPosition();\n
                var line = session.doc.getLine(cursor.row);\n
                var leftChar = line.substring(cursor.column-1, cursor.column);\n
                if (leftChar == \'\\\\\') {\n
                    return null;\n
                }\n
                var tokens = session.getTokens(selection.start.row);\n
                var col = 0, token;\n
                var quotepos = -1; // Track whether we\'re inside an open quote.\n
\n
                for (var x = 0; x < tokens.length; x++) {\n
                    token = tokens[x];\n
                    if (token.type == "string") {\n
                      quotepos = -1;\n
                    } else if (quotepos < 0) {\n
                      quotepos = token.value.indexOf(quote);\n
                    }\n
                    if ((token.value.length + col) > selection.start.column) {\n
                        break;\n
                    }\n
                    col += tokens[x].value.length;\n
                }\n
                if (!token || (quotepos < 0 && token.type !== "comment" && (token.type !== "string" || ((selection.start.column !== token.value.length+col-1) && token.value.lastIndexOf(quote) === token.value.length-1)))) {\n
                    if (!CstyleBehaviour.isSaneInsertion(editor, session))\n
                        return;\n
                    return {\n
                        text: quote + quote,\n
                        selection: [1,1]\n
                    };\n
                } else if (token && token.type === "string") {\n
                    var rightChar = line.substring(cursor.column, cursor.column + 1);\n
                    if (rightChar == quote) {\n
                        return {\n
                            text: \'\',\n
                            selection: [1, 1]\n
                        };\n
                    }\n
                }\n
            }\n
        }\n
    });\n
\n
    this.add("string_dquotes", "deletion", function (state, action, editor, session, range) {\n
        var selected = session.doc.getTextRange(range);\n
        if (!range.isMultiLine() && (selected == \'"\' || selected == "\'")) {\n
            var line = session.doc.getLine(range.start.row);\n
            var rightChar = line.substring(range.start.column + 1, range.start.column + 2);\n
            if (rightChar == selected) {\n
                range.end.column++;\n
                return range;\n
            }\n
        }\n
    });\n
\n
};\n
\n
oop.inherits(CstyleBehaviour, Behaviour);\n
\n
exports.CstyleBehaviour = CstyleBehaviour;\n
});\n
\n
define(\'ace/mode/folding/cstyle\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/range\', \'ace/mode/folding/fold_mode\'], function(require, exports, module) {\n
\n
\n
var oop = require("../../lib/oop");\n
var Range = require("../../range").Range;\n
var BaseFoldMode = require("./fold_mode").FoldMode;\n
\n
var FoldMode = exports.FoldMode = function(commentRegex) {\n
    if (commentRegex) {\n
        this.foldingStartMarker = new RegExp(\n
            this.foldingStartMarker.source.replace(/\\|[^|]*?$/, "|" + commentRegex.start)\n
        );\n
        this.foldingStopMarker = new RegExp(\n
            this.foldingStopMarker.source.replace(/\\|[^|]*?$/, "|" + commentRegex.end)\n
        );\n
    }\n
};\n
oop.inherits(FoldMode, BaseFoldMode);\n
\n
(function() {\n
\n
    this.foldingStartMarker = /(\\{|\\[)[^\\}\\]]*$|^\\s*(\\/\\*)/;\n
    this.foldingStopMarker = /^[^\\[\\{]*(\\}|\\])|^[\\s\\*]*(\\*\\/)/;\n
\n
    this.getFoldWidgetRange = function(session, foldStyle, row) {\n
        var line = session.getLine(row);\n
        var match = line.match(this.foldingStartMarker);\n
        if (match) {\n
            var i = match.index;\n
\n
            if (match[1])\n
                return this.openingBracketBlock(session, match[1], row, i);\n
\n
            return session.getCommentFoldRange(row, i + match[0].length, 1);\n
        }\n
\n
        if (foldStyle !== "markbeginend")\n
            return;\n
\n
        var match = line.match(this.foldingStopMarker);\n
        if (match) {\n
            var i = match.index + match[0].length;\n
\n
            if (match[1])\n
                return this.closingBracketBlock(session, match[1], row, i);\n
\n
            return session.getCommentFoldRange(row, i, -1);\n
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
            <value> <int>23337</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
