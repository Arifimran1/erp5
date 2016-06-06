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
            <value> <string>ts83646621.8</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>mode-livescript.js</string> </value>
        </item>
        <item>
            <key> <string>content_type</string> </key>
            <value> <string>application/javascript</string> </value>
        </item>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

define(\'ace/mode/livescript\', [\'require\', \'exports\', \'module\' , \'ace/tokenizer\', \'ace/mode/matching_brace_outdent\', \'ace/range\', \'ace/mode/text\'], function(require, exports, module) {\n
  var identifier, LiveScriptMode, keywordend, stringfill;\n
  identifier = \'(?![\\\\d\\\\s])[$\\\\w\\\\xAA-\\\\uFFDC](?:(?!\\\\s)[$\\\\w\\\\xAA-\\\\uFFDC]|-[A-Za-z])*\';\n
  exports.Mode = LiveScriptMode = (function(superclass){\n
    var indenter, prototype = extend$((import$(LiveScriptMode, superclass).displayName = \'LiveScriptMode\', LiveScriptMode), superclass).prototype, constructor = LiveScriptMode;\n
    function LiveScriptMode(){\n
      var that;\n
      this.$tokenizer = new (require(\'../tokenizer\')).Tokenizer(LiveScriptMode.Rules);\n
      if (that = require(\'../mode/matching_brace_outdent\')) {\n
        this.$outdent = new that.MatchingBraceOutdent;\n
      }\n
    }\n
    indenter = RegExp(\'(?:[({[=:]|[-~]>|\\\\b(?:e(?:lse|xport)|d(?:o|efault)|t(?:ry|hen)|finally|import(?:\\\\s*all)?|const|var|let|new|catch(?:\\\\s*\' + identifier + \')?))\\\\s*$\');\n
    prototype.getNextLineIndent = function(state, line, tab){\n
      var indent, tokens;\n
      indent = this.$getIndent(line);\n
      tokens = this.$tokenizer.getLineTokens(line, state).tokens;\n
      if (!(tokens.length && tokens[tokens.length - 1].type === \'comment\')) {\n
        if (state === \'start\' && indenter.test(line)) {\n
          indent += tab;\n
        }\n
      }\n
      return indent;\n
    };\n
    prototype.toggleCommentLines = function(state, doc, startRow, endRow){\n
      var comment, range, i$, i, out, line;\n
      comment = /^(\\s*)#/;\n
      range = new (require(\'../range\')).Range(0, 0, 0, 0);\n
      for (i$ = startRow; i$ <= endRow; ++i$) {\n
        i = i$;\n
        if (out = comment.test(line = doc.getLine(i))) {\n
          line = line.replace(comment, \'$1\');\n
        } else {\n
          line = line.replace(/^\\s*/, \'$&#\');\n
        }\n
        range.end.row = range.start.row = i;\n
        range.end.column = line.length + 1;\n
        doc.replace(range, line);\n
      }\n
      return 1 - out * 2;\n
    };\n
    prototype.checkOutdent = function(state, line, input){\n
      var ref$;\n
      return (ref$ = this.$outdent) != null ? ref$.checkOutdent(line, input) : void 8;\n
    };\n
    prototype.autoOutdent = function(state, doc, row){\n
      var ref$;\n
      return (ref$ = this.$outdent) != null ? ref$.autoOutdent(doc, row) : void 8;\n
    };\n
    return LiveScriptMode;\n
  }(require(\'../mode/text\').Mode));\n
  keywordend = \'(?![$\\\\w]|-[A-Za-z]|\\\\s*:(?![:=]))\';\n
  stringfill = {\n
    token: \'string\',\n
    regex: \'.+\'\n
  };\n
  LiveScriptMode.Rules = {\n
    start: [\n
      {\n
        token: \'keyword\',\n
        regex: \'(?:t(?:h(?:is|row|en)|ry|ypeof!?)|c(?:on(?:tinue|st)|a(?:se|tch)|lass)|i(?:n(?:stanceof)?|mp(?:ort(?:\\\\s+all)?|lements)|[fs])|d(?:e(?:fault|lete|bugger)|o)|f(?:or(?:\\\\s+own)?|inally|unction)|s(?:uper|witch)|e(?:lse|x(?:tends|port)|val)|a(?:nd|rguments)|n(?:ew|ot)|un(?:less|til)|w(?:hile|ith)|o[fr]|return|break|let|var|loop)\' + keywordend\n
      }, {\n
        token: \'constant.language\',\n
        regex: \'(?:true|false|yes|no|on|off|null|void|undefined)\' + keywordend\n
      }, {\n
        token: \'invalid.illegal\',\n
        regex: \'(?:p(?:ackage|r(?:ivate|otected)|ublic)|i(?:mplements|nterface)|enum|static|yield)\' + keywordend\n
      }, {\n
        token: \'language.support.class\',\n
        regex: \'(?:R(?:e(?:gExp|ferenceError)|angeError)|S(?:tring|yntaxError)|E(?:rror|valError)|Array|Boolean|Date|Function|Number|Object|TypeError|URIError)\' + keywordend\n
      }, {\n
        token: \'language.support.function\',\n
        regex: \'(?:is(?:NaN|Finite)|parse(?:Int|Float)|Math|JSON|(?:en|de)codeURI(?:Component)?)\' + keywordend\n
      }, {\n
        token: \'variable.language\',\n
        regex: \'(?:t(?:hat|il|o)|f(?:rom|allthrough)|it|by|e)\' + keywordend\n
      }, {\n
        token: \'identifier\',\n
        regex: identifier + \'\\\\s*:(?![:=])\'\n
      }, {\n
        token: \'variable\',\n
        regex: identifier\n
      }, {\n
        token: \'keyword.operator\',\n
        regex: \'(?:\\\\.{3}|\\\\s+\\\\?)\'\n
      }, {\n
        token: \'keyword.variable\',\n
        regex: \'(?:@+|::|\\\\.\\\\.)\',\n
        next: \'key\'\n
      }, {\n
        token: \'keyword.operator\',\n
        regex: \'\\\\.\\\\s*\',\n
        next: \'key\'\n
      }, {\n
        token: \'string\',\n
        regex: \'\\\\\\\\\\\\S[^\\\\s,;)}\\\\]]*\'\n
      }, {\n
        token: \'string.doc\',\n
        regex: \'\\\'\\\'\\\'\',\n
        next: \'qdoc\'\n
      }, {\n
        token: \'string.doc\',\n
        regex: \'"""\',\n
        next: \'qqdoc\'\n
      }, {\n
        token: \'string\',\n
        regex: \'\\\'\',\n
        next: \'qstring\'\n
      }, {\n
        token: \'string\',\n
        regex: \'"\',\n
        next: \'qqstring\'\n
      }, {\n
        token: \'string\',\n
        regex: \'`\',\n
        next: \'js\'\n
      }, {\n
        token: \'string\',\n
        regex: \'<\\\\[\',\n
        next: \'words\'\n
      }, {\n
        token: \'string.regex\',\n
        regex: \'//\',\n
        next: \'heregex\'\n
      }, {\n
        token: \'comment.doc\',\n
        regex: \'/\\\\*\',\n
        next: \'comment\'\n
      }, {\n
        token: \'comment\',\n
        regex: \'#.*\'\n
      }, {\n
        token: \'string.regex\',\n
        regex: \'\\\\/(?:[^[\\\\/\\\\n\\\\\\\\]*(?:(?:\\\\\\\\.|\\\\[[^\\\\]\\\\n\\\\\\\\]*(?:\\\\\\\\.[^\\\\]\\\\n\\\\\\\\]*)*\\\\])[^[\\\\/\\\\n\\\\\\\\]*)*)\\\\/[gimy$]{0,4}\',\n
        next: \'key\'\n
      }, {\n
        token: \'constant.numeric\',\n
        regex: \'(?:0x[\\\\da-fA-F][\\\\da-fA-F_]*|(?:[2-9]|[12]\\\\d|3[0-6])r[\\\\da-zA-Z][\\\\da-zA-Z_]*|(?:\\\\d[\\\\d_]*(?:\\\\.\\\\d[\\\\d_]*)?|\\\\.\\\\d[\\\\d_]*)(?:e[+-]?\\\\d[\\\\d_]*)?[\\\\w$]*)\'\n
      }, {\n
        token: \'lparen\',\n
        regex: \'[({[]\'\n
      }, {\n
        token: \'rparen\',\n
        regex: \'[)}\\\\]]\',\n
        next: \'key\'\n
      }, {\n
        token: \'keyword.operator\',\n
        regex: \'\\\\S+\'\n
      }, {\n
        token: \'text\',\n
        regex: \'\\\\s+\'\n
      }\n
    ],\n
    heregex: [\n
      {\n
        token: \'string.regex\',\n
        regex: \'.*?//[gimy$?]{0,4}\',\n
        next: \'start\'\n
      }, {\n
        token: \'string.regex\',\n
        regex: \'\\\\s*#{\'\n
      }, {\n
        token: \'comment.regex\',\n
        regex: \'\\\\s+(?:#.*)?\'\n
      }, {\n
        token: \'string.regex\',\n
        regex: \'\\\\S+\'\n
      }\n
    ],\n
    key: [\n
      {\n
        token: \'keyword.operator\',\n
        regex: \'[.?@!]+\'\n
      }, {\n
        token: \'identifier\',\n
        regex: identifier,\n
        next: \'start\'\n
      }, {\n
        token: \'text\',\n
        regex: \'.\',\n
        next: \'start\'\n
      }\n
    ],\n
    comment: [\n
      {\n
        token: \'comment.doc\',\n
        regex: \'.*?\\\\*/\',\n
        next: \'start\'\n
      }, {\n
        token: \'comment.doc\',\n
        regex: \'.+\'\n
      }\n
    ],\n
    qdoc: [\n
      {\n
        token: \'string\',\n
        regex: ".*?\'\'\'",\n
        next: \'key\'\n
      }, stringfill\n
    ],\n
    qqdoc: [\n
      {\n
        token: \'string\',\n
        regex: \'.*?"""\',\n
        next: \'key\'\n
      }, stringfill\n
    ],\n
    qstring: [\n
      {\n
        token: \'string\',\n
        regex: \'[^\\\\\\\\\\\']*(?:\\\\\\\\.[^\\\\\\\\\\\']*)*\\\'\',\n
        next: \'key\'\n
      }, stringfill\n
    ],\n
    qqstring: [\n
      {\n
        token: \'string\',\n
        regex: \'[^\\\\\\\\"]*(?:\\\\\\\\.[^\\\\\\\\"]*)*"\',\n
        next: \'key\'\n
      }, stringfill\n
    ],\n
    js: [\n
      {\n
        token: \'string\',\n
        regex: \'[^\\\\\\\\`]*(?:\\\\\\\\.[^\\\\\\\\`]*)*`\',\n
        next: \'key\'\n
      }, stringfill\n
    ],\n
    words: [\n
      {\n
        token: \'string\',\n
        regex: \'.*?\\\\]>\',\n
        next: \'key\'\n
      }, stringfill\n
    ]\n
  };\n
function extend$(sub, sup){\n
  function fun(){} fun.prototype = (sub.superclass = sup).prototype;\n
  (sub.prototype = new fun).constructor = sub;\n
  if (typeof sup.extended == \'function\') sup.extended(sub);\n
  return sub;\n
}\n
function import$(obj, src){\n
  var own = {}.hasOwnProperty;\n
  for (var key in src) if (own.call(src, key)) obj[key] = src[key];\n
  return obj;\n
}\n
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


]]></string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>8624</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
