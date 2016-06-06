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
            <value> <string>ts83646622.7</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>ext-modelist.js</string> </value>
        </item>
        <item>
            <key> <string>content_type</string> </key>
            <value> <string>application/javascript</string> </value>
        </item>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

define(\'ace/ext/modelist\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
\n
var modes = [];\n
function getModeForPath(path) {\n
    var mode = modesByName.text;\n
    var fileName = path.split(/[\\/\\\\]/).pop();\n
    for (var i = 0; i < modes.length; i++) {\n
        if (modes[i].supportsFile(fileName)) {\n
            mode = modes[i];\n
            break;\n
        }\n
    }\n
    return mode;\n
}\n
\n
var Mode = function(name, caption, extensions) {\n
    this.name = name;\n
    this.caption = caption;\n
    this.mode = "ace/mode/" + name;\n
    this.extensions = extensions;\n
    if (/\\^/.test(extensions)) {\n
        var re = extensions.replace(/\\|(\\^)?/g, function(a, b){\n
            return "$|" + (b ? "^" : "^.*\\\\.");\n
        }) + "$";\n
    } else {\n
        var re = "^.*\\\\.(" + extensions + ")$";\n
    }\n
\n
    this.extRe = new RegExp(re, "gi");\n
};\n
\n
Mode.prototype.supportsFile = function(filename) {\n
    return filename.match(this.extRe);\n
};\n
var supportedModes = {\n
    ABAP:        ["abap"],\n
    ActionScript:["as"],\n
    ADA:         ["ada|adb"],\n
    AsciiDoc:    ["asciidoc"],\n
    Assembly_x86:["asm"],\n
    AutoHotKey:  ["ahk"],\n
    BatchFile:   ["bat|cmd"],\n
    C9Search:    ["c9search_results"],\n
    C_Cpp:       ["cpp|c|cc|cxx|h|hh|hpp"],\n
    Clojure:     ["clj"],\n
    Cobol:       ["CBL|COB"],\n
    coffee:      ["coffee|cf|cson|^Cakefile"],\n
    ColdFusion:  ["cfm"],\n
    CSharp:      ["cs"],\n
    CSS:         ["css"],\n
    Curly:       ["curly"],\n
    D:           ["d|di"],\n
    Dart:        ["dart"],\n
    Diff:        ["diff|patch"],\n
    Dot:         ["dot"],\n
    Erlang:      ["erl|hrl"],\n
    EJS:         ["ejs"],\n
    Forth:       ["frt|fs|ldr"],\n
    FTL:         ["ftl"],\n
    Glsl:        ["glsl|frag|vert"],\n
    golang:      ["go"],\n
    Groovy:      ["groovy"],\n
    HAML:        ["haml"],\n
    Handlebars:  ["hbs|handlebars|tpl|mustache"],\n
    Haskell:     ["hs"],\n
    haXe:        ["hx"],\n
    HTML:        ["html|htm|xhtml"],\n
    HTML_Ruby:   ["erb|rhtml|html.erb"],\n
    INI:         ["ini|conf|cfg|prefs"],\n
    Jack:        ["jack"],\n
    Jade:        ["jade"],\n
    Java:        ["java"],\n
    JavaScript:  ["js|jsm"],\n
    JSON:        ["json"],\n
    JSONiq:      ["jq"],\n
    JSP:         ["jsp"],\n
    JSX:         ["jsx"],\n
    Julia:       ["jl"],\n
    LaTeX:       ["tex|latex|ltx|bib"],\n
    LESS:        ["less"],\n
    Liquid:      ["liquid"],\n
    Lisp:        ["lisp"],\n
    LiveScript:  ["ls"],\n
    LogiQL:      ["logic|lql"],\n
    LSL:         ["lsl"],\n
    Lua:         ["lua"],\n
    LuaPage:     ["lp"],\n
    Lucene:      ["lucene"],\n
    Makefile:    ["^Makefile|^GNUmakefile|^makefile|^OCamlMakefile|make"],\n
    MATLAB:      ["matlab"],\n
    Markdown:    ["md|markdown"],\n
    MySQL:       ["mysql"],\n
    MUSHCode:    ["mc|mush"],\n
    Nix:         ["nix"],\n
    ObjectiveC:  ["m|mm"],\n
    OCaml:       ["ml|mli"],\n
    Pascal:      ["pas|p"],\n
    Perl:        ["pl|pm"],\n
    pgSQL:       ["pgsql"],\n
    PHP:         ["php|phtml"],\n
    Powershell:  ["ps1"],\n
    Prolog:      ["plg|prolog"],\n
    Properties:  ["properties"],\n
    Protobuf:    ["proto"],\n
    Python:      ["py"],\n
    R:           ["r"],\n
    RDoc:        ["Rd"],\n
    RHTML:       ["Rhtml"],\n
    Ruby:        ["rb|ru|gemspec|rake|^Guardfile|^Rakefile|^Gemfile"],\n
    Rust:        ["rs"],\n
    SASS:        ["sass"],\n
    SCAD:        ["scad"],\n
    Scala:       ["scala"],\n
    Scheme:      ["scm|rkt"],\n
    SCSS:        ["scss"],\n
    SH:          ["sh|bash|^.bashrc"],\n
    SJS:         ["sjs"],\n
    Space:       ["space"],\n
    snippets:    ["snippets"],\n
    Soy_Template:["soy"],\n
    SQL:         ["sql"],\n
    Stylus:      ["styl|stylus"],\n
    SVG:         ["svg"],\n
    Tcl:         ["tcl"],\n
    Tex:         ["tex"],\n
    Text:        ["txt"],\n
    Textile:     ["textile"],\n
    Toml:        ["toml"],\n
    Twig:        ["twig"],\n
    Typescript:  ["ts|typescript|str"],\n
    VBScript:    ["vbs"],\n
    Velocity:    ["vm"],\n
    Verilog:     ["v|vh|sv|svh"],\n
    XML:         ["xml|rdf|rss|wsdl|xslt|atom|mathml|mml|xul|xbl"],\n
    XQuery:      ["xq"],\n
    YAML:        ["yaml|yml"]\n
};\n
\n
var nameOverrides = {\n
    ObjectiveC: "Objective-C",\n
    CSharp: "C#",\n
    golang: "Go",\n
    C_Cpp: "C/C++",\n
    coffee: "CoffeeScript",\n
    HTML_Ruby: "HTML (Ruby)",\n
    FTL: "FreeMarker"\n
};\n
var modesByName = {};\n
for (var name in supportedModes) {\n
    var data = supportedModes[name];\n
    var displayName = nameOverrides[name] || name;\n
    var filename = name.toLowerCase();\n
    var mode = new Mode(filename, displayName, data[0]);\n
    modesByName[filename] = mode;\n
    modes.push(mode);\n
}\n
\n
module.exports = {\n
    getModeForPath: getModeForPath,\n
    modes: modes,\n
    modesByName: modesByName\n
};\n
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
            <value> <int>4644</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
