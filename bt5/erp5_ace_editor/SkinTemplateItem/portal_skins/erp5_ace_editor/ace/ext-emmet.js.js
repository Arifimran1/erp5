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
            <value> <string>ts83646621.47</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>ext-emmet.js</string> </value>
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
define(\'ace/ext/emmet\', [\'require\', \'exports\', \'module\' , \'ace/keyboard/hash_handler\', \'ace/editor\', \'ace/snippets\', \'ace/range\', \'ace/config\'], function(require, exports, module) {\n
\n
var HashHandler = require("ace/keyboard/hash_handler").HashHandler;\n
var Editor = require("ace/editor").Editor;\n
var snippetManager = require("ace/snippets").snippetManager;\n
var Range = require("ace/range").Range;\n
var emmet;\n
\n
Editor.prototype.indexToPosition = function(index) {\n
    return this.session.doc.indexToPosition(index);\n
};\n
\n
Editor.prototype.positionToIndex = function(pos) {\n
    return this.session.doc.positionToIndex(pos);\n
};\n
function AceEmmetEditor() {}\n
\n
AceEmmetEditor.prototype = {\n
    setupContext: function(editor) {\n
        this.ace = editor;\n
        this.indentation = editor.session.getTabString();\n
        if (!emmet)\n
            emmet = window.emmet;\n
        emmet.require("resources").setVariable("indentation", this.indentation);\n
        this.$syntax = null;\n
        this.$syntax = this.getSyntax();\n
    },\n
    getSelectionRange: function() {\n
        var range = this.ace.getSelectionRange();\n
        return {\n
            start: this.ace.positionToIndex(range.start),\n
            end: this.ace.positionToIndex(range.end)\n
        };\n
    },\n
    createSelection: function(start, end) {\n
        this.ace.selection.setRange({\n
            start: this.ace.indexToPosition(start),\n
            end: this.ace.indexToPosition(end)\n
        });\n
    },\n
    getCurrentLineRange: function() {\n
        var row = this.ace.getCursorPosition().row;\n
        var lineLength = this.ace.session.getLine(row).length;\n
        var index = this.ace.positionToIndex({row: row, column: 0});\n
        return {\n
            start: index,\n
            end: index + lineLength\n
        };\n
    },\n
    getCaretPos: function(){\n
        var pos = this.ace.getCursorPosition();\n
        return this.ace.positionToIndex(pos);\n
    },\n
    setCaretPos: function(index){\n
        var pos = this.ace.indexToPosition(index);\n
        this.ace.clearSelection();\n
        this.ace.selection.moveCursorToPosition(pos);\n
    },\n
    getCurrentLine: function() {\n
        var row = this.ace.getCursorPosition().row;\n
        return this.ace.session.getLine(row);\n
    },\n
    replaceContent: function(value, start, end, noIndent) {\n
        if (end == null)\n
            end = start == null ? this.getContent().length : start;\n
        if (start == null)\n
            start = 0;        \n
        \n
        var editor = this.ace;\n
        var range = Range.fromPoints(editor.indexToPosition(start), editor.indexToPosition(end));\n
        editor.session.remove(range);\n
        \n
        range.end = range.start;\n
        \n
        value = this.$updateTabstops(value);\n
        snippetManager.insertSnippet(editor, value)\n
    },\n
    getContent: function(){\n
        return this.ace.getValue();\n
    },\n
    getSyntax: function() {\n
        if (this.$syntax)\n
            return this.$syntax;\n
        var syntax = this.ace.session.$modeId.split("/").pop();\n
        if (syntax == "html" || syntax == "php") {\n
            var cursor = this.ace.getCursorPosition();\n
            var state = this.ace.session.getState(cursor.row);\n
            if (typeof state != "string")\n
                state = state[0];\n
            if (state) {\n
                state = state.split("-");\n
                if (state.length > 1)\n
                    syntax = state[0];\n
                else if (syntax == "php")\n
                    syntax = "html";\n
            }\n
        }\n
        return syntax;\n
    },\n
    getProfileName: function() {\n
        switch(this.getSyntax()) {\n
          case "css": return "css";\n
          case "xml":\n
          case "xsl":\n
            return "xml";\n
          case "html":\n
            var profile = emmet.require("resources").getVariable("profile");\n
            if (!profile)\n
                profile = this.ace.session.getLines(0,2).join("").search(/<!DOCTYPE[^>]+XHTML/i) != -1 ? "xhtml": "html";\n
            return profile;\n
        }\n
        return "xhtml";\n
    },\n
    prompt: function(title) {\n
        return prompt(title);\n
    },\n
    getSelection: function() {\n
        return this.ace.session.getTextRange();\n
    },\n
    getFilePath: function() {\n
        return "";\n
    },\n
    $updateTabstops: function(value) {\n
        var base = 1000;\n
        var zeroBase = 0;\n
        var lastZero = null;\n
        var range = emmet.require(\'range\');\n
        var ts = emmet.require(\'tabStops\');\n
        var settings = emmet.require(\'resources\').getVocabulary("user");\n
        var tabstopOptions = {\n
            tabstop: function(data) {\n
                var group = parseInt(data.group, 10);\n
                var isZero = group === 0;\n
                if (isZero)\n
                    group = ++zeroBase;\n
                else\n
                    group += base;\n
\n
                var placeholder = data.placeholder;\n
                if (placeholder) {\n
                    placeholder = ts.processText(placeholder, tabstopOptions);\n
                }\n
\n
                var result = \'${\' + group + (placeholder ? \':\' + placeholder : \'\') + \'}\';\n
\n
                if (isZero) {\n
                    lastZero = range.create(data.start, result);\n
                }\n
\n
                return result\n
            },\n
            escape: function(ch) {\n
                if (ch == \'$\') return \'\\\\$\';\n
                if (ch == \'\\\\\') return \'\\\\\\\\\';\n
                return ch;\n
            }\n
        };\n
\n
        value = ts.processText(value, tabstopOptions);\n
\n
        if (settings.variables[\'insert_final_tabstop\'] && !/\\$\\{0\\}$/.test(value)) {\n
            value += \'${0}\';\n
        } else if (lastZero) {\n
            value = emmet.require(\'utils\').replaceSubstring(value, \'${0}\', lastZero);\n
        }\n
        \n
        return value;\n
    }\n
};\n
\n
\n
var keymap = {\n
    expand_abbreviation: {"mac": "ctrl+alt+e", "win": "alt+e"},\n
    match_pair_outward: {"mac": "ctrl+d", "win": "ctrl+,"},\n
    match_pair_inward: {"mac": "ctrl+j", "win": "ctrl+shift+0"},\n
    matching_pair: {"mac": "ctrl+alt+j", "win": "alt+j"},\n
    next_edit_point: "alt+right",\n
    prev_edit_point: "alt+left",\n
    toggle_comment: {"mac": "command+/", "win": "ctrl+/"},\n
    split_join_tag: {"mac": "shift+command+\'", "win": "shift+ctrl+`"},\n
    remove_tag: {"mac": "command+\'", "win": "shift+ctrl+;"},\n
    evaluate_math_expression: {"mac": "shift+command+y", "win": "shift+ctrl+y"},\n
    increment_number_by_1: "ctrl+up",\n
    decrement_number_by_1: "ctrl+down",\n
    increment_number_by_01: "alt+up",\n
    decrement_number_by_01: "alt+down",\n
    increment_number_by_10: {"mac": "alt+command+up", "win": "shift+alt+up"},\n
    decrement_number_by_10: {"mac": "alt+command+down", "win": "shift+alt+down"},\n
    select_next_item: {"mac": "shift+command+.", "win": "shift+ctrl+."},\n
    select_previous_item: {"mac": "shift+command+,", "win": "shift+ctrl+,"},\n
    reflect_css_value: {"mac": "shift+command+r", "win": "shift+ctrl+r"},\n
\n
    encode_decode_data_url: {"mac": "shift+ctrl+d", "win": "ctrl+\'"},\n
    expand_abbreviation_with_tab: "Tab",\n
    wrap_with_abbreviation: {"mac": "shift+ctrl+a", "win": "shift+ctrl+a"}\n
};\n
\n
var editorProxy = new AceEmmetEditor();\n
exports.commands = new HashHandler();\n
exports.runEmmetCommand = function(editor) {\n
    editorProxy.setupContext(editor);\n
    if (editorProxy.getSyntax() == "php")\n
        return false;\n
    var actions = emmet.require("actions");\n
\n
    if (this.action == "expand_abbreviation_with_tab") {\n
        if (!editor.selection.isEmpty())\n
            return false;\n
    }\n
    \n
    if (this.action == "wrap_with_abbreviation") {\n
        return setTimeout(function() {\n
            actions.run("wrap_with_abbreviation", editorProxy);\n
        }, 0);\n
    }\n
    \n
    try {\n
        var result = actions.run(this.action, editorProxy);\n
    } catch(e) {\n
        editor._signal("changeStatus", typeof e == "string" ? e : e.message);\n
        console.log(e);\n
    }\n
    return result;\n
};\n
\n
for (var command in keymap) {\n
    exports.commands.addCommand({\n
        name: "emmet:" + command,\n
        action: command,\n
        bindKey: keymap[command],\n
        exec: exports.runEmmetCommand,\n
        multiSelectAction: "forEach"\n
    });\n
}\n
\n
var onChangeMode = function(e, target) {\n
    var editor = target;\n
    if (!editor)\n
        return;\n
    var modeId = editor.session.$modeId;\n
    var enabled = modeId && /css|less|scss|sass|stylus|html|php/.test(modeId);\n
    if (e.enableEmmet === false)\n
        enabled = false;\n
    if (enabled)\n
        editor.keyBinding.addKeyboardHandler(exports.commands);\n
    else\n
        editor.keyBinding.removeKeyboardHandler(exports.commands);\n
};\n
\n
\n
exports.AceEmmetEditor = AceEmmetEditor;\n
require("ace/config").defineOptions(Editor.prototype, "editor", {\n
    enableEmmet: {\n
        set: function(val) {\n
            this[val ? "on" : "removeListener"]("changeMode", onChangeMode);\n
            onChangeMode({enableEmmet: !!val}, this);\n
        },\n
        value: true\n
    }\n
});\n
\n
\n
exports.setCore = function(e) {emmet = e;};\n
});\n
\n
define(\'ace/snippets\', [\'require\', \'exports\', \'module\' , \'ace/lib/lang\', \'ace/range\', \'ace/keyboard/hash_handler\', \'ace/tokenizer\', \'ace/lib/dom\'], function(require, exports, module) {\n
\n
var lang = require("./lib/lang")\n
var Range = require("./range").Range\n
var HashHandler = require("./keyboard/hash_handler").HashHandler;\n
var Tokenizer = require("./tokenizer").Tokenizer;\n
var comparePoints = Range.comparePoints;\n
\n
var SnippetManager = function() {\n
    this.snippetMap = {};\n
    this.snippetNameMap = {};\n
};\n
\n
(function() {\n
    this.getTokenizer = function() {\n
        function TabstopToken(str, _, stack) {\n
            str = str.substr(1);\n
            if (/^\\d+$/.test(str) && !stack.inFormatString)\n
                return [{tabstopId: parseInt(str, 10)}];\n
            return [{text: str}]\n
        }\n
        function escape(ch) {\n
            return "(?:[^\\\\\\\\" + ch + "]|\\\\\\\\.)";\n
        }\n
        SnippetManager.$tokenizer = new Tokenizer({\n
            start: [\n
                {regex: /:/, onMatch: function(val, state, stack) {\n
                    if (stack.length && stack[0].expectIf) {\n
                        stack[0].expectIf = false;\n
                        stack[0].elseBranch = stack[0];\n
                        return [stack[0]];\n
                    }\n
                    return ":";\n
                }},\n
                {regex: /\\\\./, onMatch: function(val, state, stack) {\n
                    var ch = val[1];\n
                    if (ch == "}" && stack.length) {\n
                        val = ch;\n
                    }else if ("`$\\\\".indexOf(ch) != -1) {\n
                        val = ch;\n
                    } else if (stack.inFormatString) {\n
                        if (ch == "n")\n
                            val = "\\n";\n
                        else if (ch == "t")\n
                            val = "\\n";\n
                        else if ("ulULE".indexOf(ch) != -1) {\n
                            val = {changeCase: ch, local: ch > "a"};\n
                        }\n
                    }\n
\n
                    return [val];\n
                }},\n
                {regex: /}/, onMatch: function(val, state, stack) {\n
                    return [stack.length ? stack.shift() : val];\n
                }},\n
                {regex: /\\$(?:\\d+|\\w+)/, onMatch: TabstopToken},\n
                {regex: /\\$\\{[\\dA-Z_a-z]+/, onMatch: function(str, state, stack) {\n
                    var t = TabstopToken(str.substr(1), state, stack);\n
                    stack.unshift(t[0]);\n
                    return t;\n
                }, next: "snippetVar"},\n
                {regex: /\\n/, token: "newline", merge: false}\n
            ],\n
            snippetVar: [\n
                {regex: "\\\\|" + escape("\\\\|") + "*\\\\|", onMatch: function(val, state, stack) {\n
                    stack[0].choices = val.slice(1, -1).split(",");\n
                }, next: "start"},\n
                {regex: "/(" + escape("/") + "+)/(?:(" + escape("/") + "*)/)(\\\\w*):?",\n
                 onMatch: function(val, state, stack) {\n
                    var ts = stack[0];\n
                    ts.fmtString = val;\n
\n
                    val = this.splitRegex.exec(val);\n
                    ts.guard = val[1];\n
                    ts.fmt = val[2];\n
                    ts.flag = val[3];\n
                    return "";\n
                }, next: "start"},\n
                {regex: "`" + escape("`") + "*`", onMatch: function(val, state, stack) {\n
                    stack[0].code = val.splice(1, -1);\n
                    return "";\n
                }, next: "start"},\n
                {regex: "\\\\?", onMatch: function(val, state, stack) {\n
                    if (stack[0])\n
                        stack[0].expectIf = true;\n
                }, next: "start"},\n
                {regex: "([^:}\\\\\\\\]|\\\\\\\\.)*:?", token: "", next: "start"}\n
            ],\n
            formatString: [\n
                {regex: "/(" + escape("/") + "+)/", token: "regex"},\n
                {regex: "", onMatch: function(val, state, stack) {\n
                    stack.inFormatString = true;\n
                }, next: "start"}\n
            ]\n
        });\n
        SnippetManager.prototype.getTokenizer = function() {\n
            return SnippetManager.$tokenizer;\n
        }\n
        return SnippetManager.$tokenizer;\n
    };\n
\n
    this.tokenizeTmSnippet = function(str, startState) {\n
        return this.getTokenizer().getLineTokens(str, startState).tokens.map(function(x) {\n
            return x.value || x;\n
        });\n
    };\n
\n
    this.$getDefaultValue = function(editor, name) {\n
        if (/^[A-Z]\\d+$/.test(name)) {\n
            var i = name.substr(1);\n
            return (this.variables[name[0] + "__"] || {})[i];\n
        }\n
        if (/^\\d+$/.test(name)) {\n
            return (this.variables.__ || {})[name];\n
        }\n
        name = name.replace(/^TM_/, "");\n
\n
        if (!editor)\n
            return;\n
        var s = editor.session;\n
        switch(name) {\n
            case "CURRENT_WORD":\n
                var r = s.getWordRange();\n
            case "SELECTION":\n
            case "SELECTED_TEXT":\n
                return s.getTextRange(r);\n
            case "CURRENT_LINE":\n
                return s.getLine(editor.getCursorPosition().row);\n
            case "PREV_LINE": // not possible in textmate\n
                return s.getLine(editor.getCursorPosition().row - 1);\n
            case "LINE_INDEX":\n
                return editor.getCursorPosition().column;\n
            case "LINE_NUMBER":\n
                return editor.getCursorPosition().row + 1;\n
            case "SOFT_TABS":\n
                return s.getUseSoftTabs() ? "YES" : "NO";\n
            case "TAB_SIZE":\n
                return s.getTabSize();\n
            case "FILENAME":\n
            case "FILEPATH":\n
                return "ace.ajax.org";\n
            case "FULLNAME":\n
                return "Ace";\n
        }\n
    };\n
    this.variables = {};\n
    this.getVariableValue = function(editor, varName) {\n
        if (this.variables.hasOwnProperty(varName))\n
            return this.variables[varName](editor, varName) || "";\n
        return this.$getDefaultValue(editor, varName) || "";\n
    };\n
    this.tmStrFormat = function(str, ch, editor) {\n
        var flag = ch.flag || "";\n
        var re = ch.guard;\n
        re = new RegExp(re, flag.replace(/[^gi]/, ""));\n
        var fmtTokens = this.tokenizeTmSnippet(ch.fmt, "formatString");\n
        var _self = this;\n
        var formatted = str.replace(re, function() {\n
            _self.variables.__ = arguments;\n
            var fmtParts = _self.resolveVariables(fmtTokens, editor);\n
            var gChangeCase = "E";\n
            for (var i  = 0; i < fmtParts.length; i++) {\n
                var ch = fmtParts[i];\n
                if (typeof ch == "object") {\n
                    fmtParts[i] = "";\n
                    if (ch.changeCase && ch.local) {\n
                        var next = fmtParts[i + 1];\n
                        if (next && typeof next == "string") {\n
                            if (ch.changeCase == "u")\n
                                fmtParts[i] = next[0].toUpperCase();\n
                            else\n
                                fmtParts[i] = next[0].toLowerCase();\n
                            fmtParts[i + 1] = next.substr(1);\n
                        }\n
                    } else if (ch.changeCase) {\n
                        gChangeCase = ch.changeCase;\n
                    }\n
                } else if (gChangeCase == "U") {\n
                    fmtParts[i] = ch.toUpperCase();\n
                } else if (gChangeCase == "L") {\n
                    fmtParts[i] = ch.toLowerCase();\n
                }\n
            }\n
            return fmtParts.join("");\n
        });\n
        this.variables.__ = null;\n
        return formatted;\n
    };\n
\n
    this.resolveVariables = function(snippet, editor) {\n
        var result = [];\n
        for (var i = 0; i < snippet.length; i++) {\n
            var ch = snippet[i];\n
            if (typeof ch == "string") {\n
                result.push(ch);\n
            } else if (typeof ch != "object") {\n
                continue;\n
            } else if (ch.skip) {\n
                gotoNext(ch);\n
            } else if (ch.processed < i) {\n
                continue;\n
            } else if (ch.text) {\n
                var value = this.getVariableValue(editor, ch.text);\n
                if (value && ch.fmtString)\n
                    value = this.tmStrFormat(value, ch);\n
                ch.processed = i;\n
                if (ch.expectIf == null) {\n
                    if (value) {\n
                        result.push(value);\n
                        gotoNext(ch);\n
                    }\n
                } else {\n
                    if (value) {\n
                        ch.skip = ch.elseBranch;\n
                    } else\n
                        gotoNext(ch);\n
                }\n
            } else if (ch.tabstopId != null) {\n
                result.push(ch);\n
            } else if (ch.changeCase != null) {\n
                result.push(ch);\n
            }\n
        }\n
        function gotoNext(ch) {\n
            var i1 = snippet.indexOf(ch, i + 1);\n
            if (i1 != -1)\n
                i = i1;\n
        }\n
        return result;\n
    };\n
\n
    this.insertSnippet = function(editor, snippetText) {\n
        var cursor = editor.getCursorPosition();\n
        var line = editor.session.getLine(cursor.row);\n
        var indentString = line.match(/^\\s*/)[0];\n
        var tabString = editor.session.getTabString();\n
\n
        var tokens = this.tokenizeTmSnippet(snippetText);\n
        tokens = this.resolveVariables(tokens, editor);\n
        tokens = tokens.map(function(x) {\n
            if (x == "\\n")\n
                return x + indentString;\n
            if (typeof x == "string")\n
                return x.replace(/\\t/g, tabString);\n
            return x;\n
        });\n
        var tabstops = [];\n
        tokens.forEach(function(p, i) {\n
            if (typeof p != "object")\n
                return;\n
            var id = p.tabstopId;\n
            var ts = tabstops[id];\n
            if (!ts) {\n
                ts = tabstops[id] = [];\n
                ts.index = id;\n
                ts.value = "";\n
            }\n
            if (ts.indexOf(p) !== -1)\n
                return;\n
            ts.push(p);\n
            var i1 = tokens.indexOf(p, i + 1);\n
            if (i1 === -1)\n
                return;\n
\n
            var value = tokens.slice(i + 1, i1);\n
            var isNested = value.some(function(t) {return typeof t === "object"});          \n
            if (isNested && !ts.value) {\n
                ts.value = value;\n
            } else if (value.length && (!ts.value || typeof ts.value !== "string")) {\n
                ts.value = value.join("");\n
            }\n
        });\n
        tabstops.forEach(function(ts) {ts.length = 0});\n
        var expanding = {};\n
        function copyValue(val) {\n
            var copy = []\n
            for (var i = 0; i < val.length; i++) {\n
                var p = val[i];\n
                if (typeof p == "object") {\n
                    if (expanding[p.tabstopId])\n
                        continue;\n
                    var j = val.lastIndexOf(p, i - 1);\n
                    p = copy[j] || {tabstopId: p.tabstopId};\n
                }\n
                copy[i] = p;\n
            }\n
            return copy;\n
        }\n
        for (var i = 0; i < tokens.length; i++) {\n
            var p = tokens[i];\n
            if (typeof p != "object")\n
                continue;\n
            var id = p.tabstopId;\n
            var i1 = tokens.indexOf(p, i + 1);\n
            if (expanding[id] == p) { \n
                expanding[id] = null;\n
                continue;\n
            }\n
            \n
            var ts = tabstops[id];\n
            var arg = typeof ts.value == "string" ? [ts.value] : copyValue(ts.value);\n
            arg.unshift(i + 1, Math.max(0, i1 - i));\n
            arg.push(p);\n
            expanding[id] = p;\n
            tokens.splice.apply(tokens, arg);\n
\n
            if (ts.indexOf(p) === -1)\n
                ts.push(p);\n
        };\n
        var row = 0, column = 0;\n
        var text = "";\n
        tokens.forEach(function(t) {\n
            if (typeof t === "string") {\n
                if (t[0] === "\\n"){\n
                    column = t.length - 1;\n
                    row ++;\n
                } else\n
                    column += t.length;\n
                text += t;\n
            } else {\n
                if (!t.start)\n
                    t.start = {row: row, column: column};\n
                else\n
                    t.end = {row: row, column: column};\n
            }\n
        });\n
        var range = editor.getSelectionRange();\n
        var end = editor.session.replace(range, text);\n
\n
        var tabstopManager = new TabstopManager(editor);\n
        tabstopManager.addTabstops(tabstops, range.start, end);\n
        tabstopManager.tabNext();\n
    };\n
\n
    this.$getScope = function(editor) {\n
        var scope = editor.session.$mode.$id || "";\n
        scope = scope.split("/").pop();\n
        if (scope === "html" || scope === "php") {\n
            if (scope === "php") \n
                scope = "html";\n
            var c = editor.getCursorPosition()\n
            var state = editor.session.getState(c.row);\n
            if (typeof state === "object") {\n
                state = state[0];\n
            }\n
            if (state.substring) {\n
                if (state.substring(0, 3) == "js-")\n
                    scope = "javascript";\n
                else if (state.substring(0, 4) == "css-")\n
                    scope = "css";\n
                else if (state.substring(0, 4) == "php-")\n
                    scope = "php";\n
            }\n
        }\n
        \n
        return scope;\n
    };\n
\n
    this.expandWithTab = function(editor) {\n
        var cursor = editor.getCursorPosition();\n
        var line = editor.session.getLine(cursor.row);\n
        var before = line.substring(0, cursor.column);\n
        var after = line.substr(cursor.column);\n
\n
        var scope = this.$getScope(editor);\n
        var snippetMap = this.snippetMap;\n
        var snippet;\n
        [scope, "_"].some(function(scope) {\n
            var snippets = snippetMap[scope];\n
            if (snippets)\n
                snippet = this.findMatchingSnippet(snippets, before, after);\n
            return !!snippet;\n
        }, this);\n
        if (!snippet)\n
            return false;\n
\n
        editor.session.doc.removeInLine(cursor.row,\n
            cursor.column - snippet.replaceBefore.length,\n
            cursor.column + snippet.replaceAfter.length\n
        );\n
\n
        this.variables.M__ = snippet.matchBefore;\n
        this.variables.T__ = snippet.matchAfter;\n
        this.insertSnippet(editor, snippet.content);\n
\n
        this.variables.M__ = this.variables.T__ = null;\n
        return true;\n
    };\n
\n
    this.findMatchingSnippet = function(snippetList, before, after) {\n
        for (var i = snippetList.length; i--;) {\n
            var s = snippetList[i];\n
            if (s.startRe && !s.startRe.test(before))\n
                continue;\n
            if (s.endRe && !s.endRe.test(after))\n
                continue;\n
            if (!s.startRe && !s.endRe)\n
                continue;\n
\n
            s.matchBefore = s.startRe ? s.startRe.exec(before) : [""];\n
            s.matchAfter = s.endRe ? s.endRe.exec(after) : [""];\n
            s.replaceBefore = s.triggerRe ? s.triggerRe.exec(before)[0] : "";\n
            s.replaceAfter = s.endTriggerRe ? s.endTriggerRe.exec(after)[0] : "";\n
            return s;\n
        }\n
    };\n
\n
    this.snippetMap = {};\n
    this.snippetNameMap = {};\n
    this.register = function(snippets, scope) {\n
        var snippetMap = this.snippetMap;\n
        var snippetNameMap = this.snippetNameMap;\n
        var self = this;\n
        function wrapRegexp(src) {\n
            if (src && !/^\\^?\\(.*\\)\\$?$|^\\\\b$/.test(src))\n
                src = "(?:" + src + ")"\n
\n
            return src || "";\n
        }\n
        function guardedRegexp(re, guard, opening) {\n
            re = wrapRegexp(re);\n
            guard = wrapRegexp(guard);\n
            if (opening) {\n
                re = guard + re;\n
                if (re && re[re.length - 1] != "$")\n
                    re = re + "$";\n
            } else {\n
                re = re + guard;\n
                if (re && re[0] != "^")\n
                    re = "^" + re;\n
            }\n
            return new RegExp(re);\n
        }\n
\n
        function addSnippet(s) {\n
            if (!s.scope)\n
                s.scope = scope || "_";\n
            scope = s.scope\n
            if (!snippetMap[scope]) {\n
                snippetMap[scope] = [];\n
                snippetNameMap[scope] = {};\n
            }\n
\n
            var map = snippetNameMap[scope];\n
            if (s.name) {\n
                var old = map[s.name];\n
                if (old)\n
                    self.unregister(old);\n
                map[s.name] = s;\n
            }\n
            snippetMap[scope].push(s);\n
\n
            if (s.tabTrigger && !s.trigger) {\n
                if (!s.guard && /^\\w/.test(s.tabTrigger))\n
                    s.guard = "\\\\b";\n
                s.trigger = lang.escapeRegExp(s.tabTrigger);\n
            }\n
\n
            s.startRe = guardedRegexp(s.trigger, s.guard, true);\n
            s.triggerRe = new RegExp(s.trigger, "", true);\n
\n
            s.endRe = guardedRegexp(s.endTrigger, s.endGuard, true);\n
            s.endTriggerRe = new RegExp(s.endTrigger, "", true);\n
        };\n
\n
        if (snippets.content)\n
            addSnippet(snippets);\n
        else if (Array.isArray(snippets))\n
            snippets.forEach(addSnippet);\n
    };\n
    this.unregister = function(snippets, scope) {\n
        var snippetMap = this.snippetMap;\n
        var snippetNameMap = this.snippetNameMap;\n
\n
        function removeSnippet(s) {\n
            var nameMap = snippetNameMap[s.scope||scope];\n
            if (nameMap && nameMap[s.name]) {\n
                delete nameMap[s.name];\n
                var map = snippetMap[s.scope||scope];\n
                var i = map && map.indexOf(s);\n
                if (i >= 0)\n
                    map.splice(i, 1);\n
            }\n
        }\n
        if (snippets.content)\n
            removeSnippet(snippets);\n
        else if (Array.isArray(snippets))\n
            snippets.forEach(removeSnippet);\n
    };\n
    this.parseSnippetFile = function(str) {\n
        str = str.replace(/\\r/g, "");\n
        var list = [], snippet = {};\n
        var re = /^#.*|^({[\\s\\S]*})\\s*$|^(\\S+) (.*)$|^((?:\\n*\\t.*)+)/gm;\n
        var m;\n
        while (m = re.exec(str)) {\n
            if (m[1]) {\n
                try {\n
                    snippet = JSON.parse(m[1])\n
                    list.push(snippet);\n
                } catch (e) {}\n
            } if (m[4]) {\n
                snippet.content = m[4].replace(/^\\t/gm, "");\n
                list.push(snippet);\n
                snippet = {};\n
            } else {\n
                var key = m[2], val = m[3];\n
                if (key == "regex") {\n
                    var guardRe = /\\/((?:[^\\/\\\\]|\\\\.)*)|$/g;\n
                    snippet.guard = guardRe.exec(val)[1];\n
                    snippet.trigger = guardRe.exec(val)[1];\n
                    snippet.endTrigger = guardRe.exec(val)[1];\n
                    snippet.endGuard = guardRe.exec(val)[1];\n
                } else if (key == "snippet") {\n
                    snippet.tabTrigger = val.match(/^\\S*/)[0];\n
                    if (!snippet.name)\n
                        snippet.name = val;\n
                } else {\n
                    snippet[key] = val;\n
                }\n
            }\n
        }\n
        return list;\n
    };\n
    this.getSnippetByName = function(name, editor) {\n
        var scope = editor && this.$getScope(editor);\n
        var snippetMap = this.snippetNameMap;\n
        var snippet;\n
        [scope, "_"].some(function(scope) {\n
            var snippets = snippetMap[scope];\n
            if (snippets)\n
                snippet = snippets[name];\n
            return !!snippet;\n
        }, this);\n
        return snippet;\n
    };\n
\n
}).call(SnippetManager.prototype);\n
\n
\n
var TabstopManager = function(editor) {\n
    if (editor.tabstopManager)\n
        return editor.tabstopManager;\n
    editor.tabstopManager = this;\n
    this.$onChange = this.onChange.bind(this);\n
    this.$onChangeSelection = lang.delayedCall(this.onChangeSelection.bind(this)).schedule;\n
    this.$onChangeSession = this.onChangeSession.bind(this);\n
    this.$onAfterExec = this.onAfterExec.bind(this);\n
    this.attach(editor);\n
};\n
(function() {\n
    this.attach = function(editor) {\n
        this.index = -1;\n
        this.ranges = [];\n
        this.tabstops = [];\n
        this.selectedTabstop = null;\n
\n
        this.editor = editor;\n
        this.editor.on("change", this.$onChange);\n
        this.editor.on("changeSelection", this.$onChangeSelection);\n
        this.editor.on("changeSession", this.$onChangeSession);\n
        this.editor.commands.on("afterExec", this.$onAfterExec);\n
        this.editor.keyBinding.addKeyboardHandler(this.keyboardHandler);\n
    };\n
    this.detach = function() {\n
        this.tabstops.forEach(this.removeTabstopMarkers, this);\n
        this.ranges = null;\n
        this.tabstops = null;\n
        this.selectedTabstop = null;\n
        this.editor.removeListener("change", this.$onChange);\n
        this.editor.removeListener("changeSelection", this.$onChangeSelection);\n
        this.editor.removeListener("changeSession", this.$onChangeSession);\n
        this.editor.commands.removeListener("afterExec", this.$onAfterExec);\n
        this.editor.keyBinding.removeKeyboardHandler(this.keyboardHandler);\n
        this.editor.tabstopManager = null;\n
        this.editor = null;\n
    };\n
\n
    this.onChange = function(e) {\n
        var changeRange = e.data.range;\n
        var isRemove = e.data.action[0] == "r";\n
        var start = changeRange.start;\n
        var end = changeRange.end;\n
        var startRow = start.row;\n
        var endRow = end.row;\n
        var lineDif = endRow - startRow;\n
        var colDiff = end.column - start.column;\n
\n
        if (isRemove) {\n
            lineDif = -lineDif;\n
            colDiff = -colDiff;\n
        }\n
        if (!this.$inChange && isRemove) {\n
            var ts = this.selectedTabstop;\n
            var changedOutside = !ts.some(function(r) {\n
                return comparePoints(r.start, start) <= 0 && comparePoints(r.end, end) >= 0;\n
            });\n
            if (changedOutside)\n
                return this.detach();\n
        }\n
        var ranges = this.ranges;\n
        for (var i = 0; i < ranges.length; i++) {\n
            var r = ranges[i];\n
            if (r.end.row < start.row)\n
                continue;\n
\n
            if (comparePoints(start, r.start) < 0 && comparePoints(end, r.end) > 0) {\n
                this.removeRange(r);\n
                i--;\n
                continue;\n
            }\n
\n
            if (r.start.row == startRow && r.start.column > start.column)\n
                r.start.column += colDiff;\n
            if (r.end.row == startRow && r.end.column >= start.column)\n
                r.end.column += colDiff;\n
            if (r.start.row >= startRow)\n
                r.start.row += lineDif;\n
            if (r.end.row >= startRow)\n
                r.end.row += lineDif;\n
\n
            if (comparePoints(r.start, r.end) > 0)\n
                this.removeRange(r);\n
        }\n
        if (!ranges.length)\n
            this.detach();\n
    };\n
    this.updateLinkedFields = function() {\n
        var ts = this.selectedTabstop;\n
        if (!ts.hasLinkedRanges)\n
            return;\n
        this.$inChange = true;\n
        var session = this.editor.session;\n
        var text = session.getTextRange(ts.firstNonLinked);\n
        for (var i = ts.length; i--;) {\n
            var range = ts[i];\n
            if (!range.linked)\n
                continue;\n
            var fmt = exports.snippetManager.tmStrFormat(text, range.original)\n
            session.replace(range, fmt);\n
        }\n
        this.$inChange = false;\n
    };\n
    this.onAfterExec = function(e) {\n
        if (e.command && !e.command.readOnly)\n
            this.updateLinkedFields();\n
    };\n
    this.onChangeSelection = function() {\n
        if (!this.editor)\n
            return\n
        var lead = this.editor.selection.lead;\n
        var anchor = this.editor.selection.anchor;\n
        var isEmpty = this.editor.selection.isEmpty();\n
        for (var i = this.ranges.length; i--;) {\n
            if (this.ranges[i].linked)\n
                continue;\n
            var containsLead = this.ranges[i].contains(lead.row, lead.column);\n
            var containsAnchor = isEmpty || this.ranges[i].contains(anchor.row, anchor.column);\n
            if (containsLead && containsAnchor)\n
                return;\n
        }\n
        this.detach();\n
    };\n
    this.onChangeSession = function() {\n
        this.detach();\n
    };\n
    this.tabNext = function(dir) {\n
        var max = this.tabstops.length - 1;\n
        var index = this.index + (dir || 1);\n
        index = Math.min(Math.max(index, 0), max);\n
        this.selectTabstop(index);\n
        if (index == max)\n
            this.detach();\n
    };\n
    this.selectTabstop = function(index) {\n
        var ts = this.tabstops[this.index];\n
        if (ts)\n
            this.addTabstopMarkers(ts);\n
        this.index = index;\n
        ts = this.tabstops[this.index];\n
        if (!ts || !ts.length)\n
            return;\n
        \n
        this.selectedTabstop = ts;\n
        if (!this.editor.inVirtualSelectionMode) {        \n
            var sel = this.editor.multiSelect;\n
            sel.toSingleRange(ts.firstNonLinked.clone());\n
            for (var i = ts.length; i--;) {\n
                if (ts.hasLinkedRanges && ts[i].linked)\n
                    continue;\n
                sel.addRange(ts[i].clone(), true);\n
            }\n
        } else {\n
            this.editor.selection.setRange(ts.firstNonLinked);\n
        }\n
        \n
        this.editor.keyBinding.addKeyboardHandler(this.keyboardHandler);\n
    };\n
    this.addTabstops = function(tabstops, start, end) {\n
        if (!tabstops[0]) {\n
            var p = Range.fromPoints(end, end);\n
            moveRelative(p.start, start);\n
            moveRelative(p.end, start);\n
            tabstops[0] = [p];\n
            tabstops[0].index = 0;\n
        }\n
\n
        var i = this.index;\n
        var arg = [i, 0];\n
        var ranges = this.ranges;\n
        var editor = this.editor;\n
        tabstops.forEach(function(ts) {\n
            for (var i = ts.length; i--;) {\n
                var p = ts[i];\n
                var range = Range.fromPoints(p.start, p.end || p.start);\n
                movePoint(range.start, start);\n
                movePoint(range.end, start);\n
                range.original = p;\n
                range.tabstop = ts;\n
                ranges.push(range);\n
                ts[i] = range;\n
                if (p.fmtString) {\n
                    range.linked = true;\n
                    ts.hasLinkedRanges = true;\n
                } else if (!ts.firstNonLinked)\n
                    ts.firstNonLinked = range;\n
            }\n
            if (!ts.firstNonLinked)\n
                ts.hasLinkedRanges = false;\n
            arg.push(ts);\n
            this.addTabstopMarkers(ts);\n
        }, this);\n
        arg.push(arg.splice(2, 1)[0]);\n
        this.tabstops.splice.apply(this.tabstops, arg);\n
    };\n
\n
    this.addTabstopMarkers = function(ts) {\n
        var session = this.editor.session;\n
        ts.forEach(function(range) {\n
            if  (!range.markerId)\n
                range.markerId = session.addMarker(range, "ace_snippet-marker", "text");\n
        });\n
    };\n
    this.removeTabstopMarkers = function(ts) {\n
        var session = this.editor.session;\n
        ts.forEach(function(range) {\n
            session.removeMarker(range.markerId);\n
            range.markerId = null;\n
        });\n
    };\n
    this.removeRange = function(range) {\n
        var i = range.tabstop.indexOf(range);\n
        range.tabstop.splice(i, 1);\n
        i = this.ranges.indexOf(range);\n
        this.ranges.splice(i, 1);\n
        this.editor.session.removeMarker(range.markerId);\n
    };\n
\n
    this.keyboardHandler = new HashHandler();\n
    this.keyboardHandler.bindKeys({\n
        "Tab": function(ed) {\n
            ed.tabstopManager.tabNext(1);\n
        },\n
        "Shift-Tab": function(ed) {\n
            ed.tabstopManager.tabNext(-1);\n
        },\n
        "Esc": function(ed) {\n
            ed.tabstopManager.detach();\n
        },\n
        "Return": function(ed) {\n
            return false;\n
        }\n
    });\n
}).call(TabstopManager.prototype);\n
\n
\n
var movePoint = function(point, diff) {\n
    if (point.row == 0)\n
        point.column += diff.column;\n
    point.row += diff.row;\n
};\n
\n
var moveRelative = function(point, start) {\n
    if (point.row == start.row)\n
        point.column -= start.column;\n
    point.row -= start.row;\n
};\n
\n
\n
require("./lib/dom").importCssString("\\\n
.ace_snippet-marker {\\\n
    -moz-box-sizing: border-box;\\\n
    box-sizing: border-box;\\\n
    background: rgba(194, 193, 208, 0.09);\\\n
    border: 1px dotted rgba(211, 208, 235, 0.62);\\\n
    position: absolute;\\\n
}");\n
\n
exports.snippetManager = new SnippetManager();\n
\n
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
            <value> <int>39213</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
