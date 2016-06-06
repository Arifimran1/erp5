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
            <value> <string>ts83646620.37</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>ext-split.js</string> </value>
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
define(\'ace/ext/split\', [\'require\', \'exports\', \'module\' , \'ace/split\'], function(require, exports, module) {\n
module.exports = require("../split");\n
\n
});\n
\n
define(\'ace/split\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/lib/lang\', \'ace/lib/event_emitter\', \'ace/editor\', \'ace/virtual_renderer\', \'ace/edit_session\'], function(require, exports, module) {\n
\n
\n
var oop = require("./lib/oop");\n
var lang = require("./lib/lang");\n
var EventEmitter = require("./lib/event_emitter").EventEmitter;\n
\n
var Editor = require("./editor").Editor;\n
var Renderer = require("./virtual_renderer").VirtualRenderer;\n
var EditSession = require("./edit_session").EditSession;\n
\n
\n
var Split = function(container, theme, splits) {\n
    this.BELOW = 1;\n
    this.BESIDE = 0;\n
\n
    this.$container = container;\n
    this.$theme = theme;\n
    this.$splits = 0;\n
    this.$editorCSS = "";\n
    this.$editors = [];\n
    this.$orientation = this.BESIDE;\n
\n
    this.setSplits(splits || 1);\n
    this.$cEditor = this.$editors[0];\n
\n
\n
    this.on("focus", function(editor) {\n
        this.$cEditor = editor;\n
    }.bind(this));\n
};\n
\n
(function(){\n
\n
    oop.implement(this, EventEmitter);\n
\n
    this.$createEditor = function() {\n
        var el = document.createElement("div");\n
        el.className = this.$editorCSS;\n
        el.style.cssText = "position: absolute; top:0px; bottom:0px";\n
        this.$container.appendChild(el);\n
        var editor = new Editor(new Renderer(el, this.$theme));\n
\n
        editor.on("focus", function() {\n
            this._emit("focus", editor);\n
        }.bind(this));\n
\n
        this.$editors.push(editor);\n
        editor.setFontSize(this.$fontSize);\n
        return editor;\n
    };\n
\n
    this.setSplits = function(splits) {\n
        var editor;\n
        if (splits < 1) {\n
            throw "The number of splits have to be > 0!";\n
        }\n
\n
        if (splits == this.$splits) {\n
            return;\n
        } else if (splits > this.$splits) {\n
            while (this.$splits < this.$editors.length && this.$splits < splits) {\n
                editor = this.$editors[this.$splits];\n
                this.$container.appendChild(editor.container);\n
                editor.setFontSize(this.$fontSize);\n
                this.$splits ++;\n
            }\n
            while (this.$splits < splits) {\n
                this.$createEditor();\n
                this.$splits ++;\n
            }\n
        } else {\n
            while (this.$splits > splits) {\n
                editor = this.$editors[this.$splits - 1];\n
                this.$container.removeChild(editor.container);\n
                this.$splits --;\n
            }\n
        }\n
        this.resize();\n
    };\n
    this.getSplits = function() {\n
        return this.$splits;\n
    };\n
    this.getEditor = function(idx) {\n
        return this.$editors[idx];\n
    };\n
    this.getCurrentEditor = function() {\n
        return this.$cEditor;\n
    };\n
    this.focus = function() {\n
        this.$cEditor.focus();\n
    };\n
    this.blur = function() {\n
        this.$cEditor.blur();\n
    };\n
    this.setTheme = function(theme) {\n
        this.$editors.forEach(function(editor) {\n
            editor.setTheme(theme);\n
        });\n
    };\n
    this.setKeyboardHandler = function(keybinding) {\n
        this.$editors.forEach(function(editor) {\n
            editor.setKeyboardHandler(keybinding);\n
        });\n
    };\n
    this.forEach = function(callback, scope) {\n
        this.$editors.forEach(callback, scope);\n
    };\n
\n
\n
    this.$fontSize = "";\n
    this.setFontSize = function(size) {\n
        this.$fontSize = size;\n
        this.forEach(function(editor) {\n
           editor.setFontSize(size);\n
        });\n
    };\n
\n
    this.$cloneSession = function(session) {\n
        var s = new EditSession(session.getDocument(), session.getMode());\n
\n
        var undoManager = session.getUndoManager();\n
        if (undoManager) {\n
            var undoManagerProxy = new UndoManagerProxy(undoManager, s);\n
            s.setUndoManager(undoManagerProxy);\n
        }\n
        s.$informUndoManager = lang.delayedCall(function() { s.$deltas = []; });\n
        s.setTabSize(session.getTabSize());\n
        s.setUseSoftTabs(session.getUseSoftTabs());\n
        s.setOverwrite(session.getOverwrite());\n
        s.setBreakpoints(session.getBreakpoints());\n
        s.setUseWrapMode(session.getUseWrapMode());\n
        s.setUseWorker(session.getUseWorker());\n
        s.setWrapLimitRange(session.$wrapLimitRange.min,\n
                            session.$wrapLimitRange.max);\n
        s.$foldData = session.$cloneFoldData();\n
\n
        return s;\n
    };\n
    this.setSession = function(session, idx) {\n
        var editor;\n
        if (idx == null) {\n
            editor = this.$cEditor;\n
        } else {\n
            editor = this.$editors[idx];\n
        }\n
        var isUsed = this.$editors.some(function(editor) {\n
           return editor.session === session;\n
        });\n
\n
        if (isUsed) {\n
            session = this.$cloneSession(session);\n
        }\n
        editor.setSession(session);\n
        return session;\n
    };\n
    this.getOrientation = function() {\n
        return this.$orientation;\n
    };\n
    this.setOrientation = function(orientation) {\n
        if (this.$orientation == orientation) {\n
            return;\n
        }\n
        this.$orientation = orientation;\n
        this.resize();\n
    };\n
    this.resize = function() {\n
        var width = this.$container.clientWidth;\n
        var height = this.$container.clientHeight;\n
        var editor;\n
\n
        if (this.$orientation == this.BESIDE) {\n
            var editorWidth = width / this.$splits;\n
            for (var i = 0; i < this.$splits; i++) {\n
                editor = this.$editors[i];\n
                editor.container.style.width = editorWidth + "px";\n
                editor.container.style.top = "0px";\n
                editor.container.style.left = i * editorWidth + "px";\n
                editor.container.style.height = height + "px";\n
                editor.resize();\n
            }\n
        } else {\n
            var editorHeight = height / this.$splits;\n
            for (var i = 0; i < this.$splits; i++) {\n
                editor = this.$editors[i];\n
                editor.container.style.width = width + "px";\n
                editor.container.style.top = i * editorHeight + "px";\n
                editor.container.style.left = "0px";\n
                editor.container.style.height = editorHeight + "px";\n
                editor.resize();\n
            }\n
        }\n
    };\n
\n
}).call(Split.prototype);\n
\n
 \n
function UndoManagerProxy(undoManager, session) {\n
    this.$u = undoManager;\n
    this.$doc = session;\n
}\n
\n
(function() {\n
    this.execute = function(options) {\n
        this.$u.execute(options);\n
    };\n
\n
    this.undo = function() {\n
        var selectionRange = this.$u.undo(true);\n
        if (selectionRange) {\n
            this.$doc.selection.setSelectionRange(selectionRange);\n
        }\n
    };\n
\n
    this.redo = function() {\n
        var selectionRange = this.$u.redo(true);\n
        if (selectionRange) {\n
            this.$doc.selection.setSelectionRange(selectionRange);\n
        }\n
    };\n
\n
    this.reset = function() {\n
        this.$u.reset();\n
    };\n
\n
    this.hasUndo = function() {\n
        return this.$u.hasUndo();\n
    };\n
\n
    this.hasRedo = function() {\n
        return this.$u.hasRedo();\n
    };\n
}).call(UndoManagerProxy.prototype);\n
\n
exports.Split = Split;\n
});\n


]]></string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>8919</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
