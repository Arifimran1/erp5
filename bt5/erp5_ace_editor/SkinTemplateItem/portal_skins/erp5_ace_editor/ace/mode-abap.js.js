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
            <value> <string>ts83646622.79</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>mode-abap.js</string> </value>
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
define(\'ace/mode/abap\', [\'require\', \'exports\', \'module\' , \'ace/tokenizer\', \'ace/mode/abap_highlight_rules\', \'ace/mode/folding/coffee\', \'ace/range\', \'ace/mode/text\', \'ace/lib/oop\'], function(require, exports, module) {\n
\n
\n
var Tokenizer = require("../tokenizer").Tokenizer;\n
var Rules = require("./abap_highlight_rules").AbapHighlightRules;\n
var FoldMode = require("./folding/coffee").FoldMode;\n
var Range = require("../range").Range;\n
var TextMode = require("./text").Mode;\n
var oop = require("../lib/oop");\n
\n
function Mode() {\n
    this.HighlightRules = Rules;\n
    this.foldingRules = new FoldMode();\n
}\n
\n
oop.inherits(Mode, TextMode);\n
\n
(function() {\n
    \n
    this.getNextLineIndent = function(state, line, tab) {\n
        var indent = this.$getIndent(line);\n
        return indent;\n
    };\n
    \n
    this.toggleCommentLines = function(state, doc, startRow, endRow){\n
        var range = new Range(0, 0, 0, 0);\n
        for (var i = startRow; i <= endRow; ++i) {\n
            var line = doc.getLine(i);\n
            if (hereComment.test(line))\n
                continue;\n
                \n
            if (commentLine.test(line))\n
                line = line.replace(commentLine, \'$1\');\n
            else\n
                line = line.replace(indentation, \'$&#\');\n
    \n
            range.end.row = range.start.row = i;\n
            range.end.column = line.length + 1;\n
            doc.replace(range, line);\n
        }\n
    };\n
    \n
}).call(Mode.prototype);\n
\n
exports.Mode = Mode;\n
\n
});\n
\n
define(\'ace/mode/abap_highlight_rules\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text_highlight_rules\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;\n
\n
var AbapHighlightRules = function() {\n
\n
    var keywordMapper = this.createKeywordMapper({\n
        "variable.language": "this",\n
        "keyword": \n
            "ADD ALIAS ALIASES ASSERT ASSIGN ASSIGNING AT BACK" +\n
            " CALL CASE CATCH CHECK CLASS CLEAR CLOSE CNT COLLECT COMMIT COMMUNICATION COMPUTE CONCATENATE CONDENSE CONSTANTS CONTINUE CONTROLS CONVERT CREATE CURRENCY" +\n
            " DATA DEFINE DEFINITION DEFERRED DELETE DESCRIBE DETAIL DIVIDE DO" +\n
            " ELSE ELSEIF ENDAT ENDCASE ENDCLASS ENDDO ENDEXEC ENDFORM ENDFUNCTION ENDIF ENDIFEND ENDINTERFACE ENDLOOP ENDMETHOD ENDMODULE ENDON ENDPROVIDE ENDSELECT ENDTRY ENDWHILE EVENT EVENTS EXEC EXIT EXPORT EXPORTING EXTRACT" +\n
            " FETCH FIELDS FORM FORMAT FREE FROM FUNCTION" +\n
            " GENERATE GET" +\n
            " HIDE" +\n
            " IF IMPORT IMPORTING INDEX INFOTYPES INITIALIZATION INTERFACE INTERFACES INPUT INSERT IMPLEMENTATION" +\n
            " LEAVE LIKE LINE LOAD LOCAL LOOP" +\n
            " MESSAGE METHOD METHODS MODIFY MODULE MOVE MULTIPLY" +\n
            " ON OVERLAY OPTIONAL OTHERS" +\n
            " PACK PARAMETERS PERFORM POSITION PROGRAM PROVIDE PUT" +\n
            " RAISE RANGES READ RECEIVE RECEIVING REDEFINITION REFERENCE REFRESH REJECT REPLACE REPORT RESERVE RESTORE RETURNING ROLLBACK" +\n
            " SCAN SCROLL SEARCH SELECT SET SHIFT SKIP SORT SORTED SPLIT STANDARD STATICS STEP STOP SUBMIT SUBTRACT SUM SUMMARY SUPPRESS" +\n
            " TABLES TIMES TRANSFER TRANSLATE TRY TYPE TYPES" +\n
            " UNASSIGN ULINE UNPACK UPDATE" +\n
            " WHEN WHILE WINDOW WRITE" +\n
            " OCCURS STRUCTURE OBJECT PROPERTY" +\n
            " CASTING APPEND RAISING VALUE COLOR" +\n
            " CHANGING EXCEPTION EXCEPTIONS DEFAULT CHECKBOX COMMENT" +\n
            " ID NUMBER FOR TITLE OUTPUT" +\n
            " WITH EXIT USING" +\n
            " INTO WHERE GROUP BY HAVING ORDER BY SINGLE" +\n
            " APPENDING CORRESPONDING FIELDS OF TABLE" +\n
            " LEFT RIGHT OUTER INNER JOIN AS CLIENT SPECIFIED BYPASSING BUFFER UP TO ROWS CONNECTING" +\n
            " EQ NE LT LE GT GE NOT AND OR XOR IN LIKE BETWEEN",\n
        "constant.language": \n
            "TRUE FALSE NULL SPACE",\n
        "support.type": \n
            "c n i p f d t x string xstring decfloat16 decfloat34",\n
        "keyword.operator":\n
            "abs sign ceil floor trunc frac acos asin atan cos sin tan" +\n
            " abapOperator cosh sinh tanh exp log log10 sqrt" +\n
            " strlen xstrlen charlen numofchar dbmaxlen lines" \n
    }, "text", true, " ");\n
\n
    var compoundKeywords = "WITH\\\\W+(?:HEADER\\\\W+LINE|FRAME|KEY)|NO\\\\W+STANDARD\\\\W+PAGE\\\\W+HEADING|"+\n
        "EXIT\\\\W+FROM\\\\W+STEP\\\\W+LOOP|BEGIN\\\\W+OF\\\\W+(?:BLOCK|LINE)|BEGIN\\\\W+OF|"+\n
        "END\\\\W+OF\\\\W+(?:BLOCK|LINE)|END\\\\W+OF|NO\\\\W+INTERVALS|"+\n
        "RESPECTING\\\\W+BLANKS|SEPARATED\\\\W+BY|USING\\\\W+(?:EDIT\\\\W+MASK)|"+\n
        "WHERE\\\\W+(?:LINE)|RADIOBUTTON\\\\W+GROUP|REF\\\\W+TO|"+\n
        "(?:PUBLIC|PRIVATE|PROTECTED)(?:\\\\W+SECTION)?|DELETING\\\\W+(?:TRAILING|LEADING)"+\n
        "(?:ALL\\\\W+OCCURRENCES)|(?:FIRST|LAST)\\\\W+OCCURRENCE|INHERITING\\\\W+FROM|"+\n
        "LINE-COUNT|ADD-CORRESPONDING|AUTHORITY-CHECK|BREAK-POINT|CLASS-DATA|CLASS-METHODS|"+\n
        "CLASS-METHOD|DIVIDE-CORRESPONDING|EDITOR-CALL|END-OF-DEFINITION|END-OF-PAGE|END-OF-SELECTION|"+\n
        "FIELD-GROUPS|FIELD-SYMBOLS|FUNCTION-POOL|MOVE-CORRESPONDING|MULTIPLY-CORRESPONDING|NEW-LINE|"+\n
        "NEW-PAGE|NEW-SECTION|PRINT-CONTROL|RP-PROVIDE-FROM-LAST|SELECT-OPTIONS|SELECTION-SCREEN|"+\n
        "START-OF-SELECTION|SUBTRACT-CORRESPONDING|SYNTAX-CHECK|SYNTAX-TRACE|TOP-OF-PAGE|TYPE-POOL|"+\n
        "TYPE-POOLS|LINE-SIZE|LINE-COUNT|MESSAGE-ID|DISPLAY-MODE|READ(?:-ONLY)?|"+\n
        "IS\\\\W+(?:NOT\\\\W+)?(?:ASSIGNED|BOUND|INITIAL|SUPPLIED)";\n
     \n
    this.$rules = {\n
        "start" : [\n
            {token : "string", regex : "`", next  : "string"},\n
            {token : "string", regex : "\'", next  : "qstring"},\n
            {token : "doc.comment", regex : /^\\*.+/},\n
            {token : "comment",  regex : /".+$/},\n
            {token : "invalid", regex: "\\\\.{2,}"},\n
            {token : "keyword.operator", regex: /\\W[\\-+\\%=<>*]\\W|\\*\\*|[~:,\\.&$]|->*?|=>/},\n
            {token : "paren.lparen", regex : "[\\\\[({]"},\n
            {token : "paren.rparen", regex : "[\\\\])}]"},\n
            {token : "constant.numeric", regex: "[+-]?\\\\d+\\\\b"},\n
            {token : "variable.parameter", regex : /sy|pa?\\d\\d\\d\\d\\|t\\d\\d\\d\\.|innnn/}, \n
            {token : "keyword", regex : compoundKeywords}, \n
            {token : "variable.parameter", regex : /\\w+-\\w+(?:-\\w+)*/}, \n
            {token : keywordMapper, regex : "\\\\b\\\\w+\\\\b"},\n
            {caseInsensitive: true}\n
        ],\n
        "qstring" : [\n
            {token : "constant.language.escape",   regex : "\'\'"},\n
            {token : "string", regex : "\'",     next  : "start"},\n
            {defaultToken : "string"}\n
        ],\n
        "string" : [\n
            {token : "constant.language.escape",   regex : "``"},\n
            {token : "string", regex : "`",     next  : "start"},\n
            {defaultToken : "string"}\n
        ]\n
    }\n
};\n
oop.inherits(AbapHighlightRules, TextHighlightRules);\n
\n
exports.AbapHighlightRules = AbapHighlightRules;\n
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
            <value> <int>11318</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
