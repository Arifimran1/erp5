<?xml version="1.0"?>
<ZopeData>
  <record id="1" aka="AAAAAAAAAAE=">
    <pickle>
      <global name="File" module="OFS.Image"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>_EtagSupport__etag</string> </key>
            <value> <string>ts40515059.47</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>ext-closepath.js</string> </value>
        </item>
        <item>
            <key> <string>content_type</string> </key>
            <value> <string>application/javascript</string> </value>
        </item>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

/*globals svgEditor, $*/\n
/*jslint vars: true, eqeq: true*/\n
/*\n
 * ext-closepath.js\n
 *\n
 * Licensed under the MIT License\n
 *\n
 * Copyright(c) 2010 Jeff Schiller\n
 *\n
 */\n
\n
// This extension adds a simple button to the contextual panel for paths\n
// The button toggles whether the path is open or closed\n
svgEditor.addExtension(\'ClosePath\', function() {\'use strict\';\n
\tvar selElems,\n
\t\tupdateButton = function(path) {\n
\t\t\tvar seglist = path.pathSegList,\n
\t\t\t\tclosed = seglist.getItem(seglist.numberOfItems - 1).pathSegType == 1,\n
\t\t\t\tshowbutton = closed ? \'#tool_openpath\' : \'#tool_closepath\',\n
\t\t\t\thidebutton = closed ? \'#tool_closepath\' : \'#tool_openpath\';\n
\t\t\t\t$(hidebutton).hide();\n
\t\t\t\t$(showbutton).show();\n
\t\t},\n
\t\tshowPanel = function(on) {\n
\t\t\t$(\'#closepath_panel\').toggle(on);\n
\t\t\tif (on) {\n
\t\t\t\tvar path = selElems[0];\n
\t\t\t\tif (path) {updateButton(path);}\n
\t\t\t}\n
\t\t},\n
\t\ttoggleClosed = function() {\n
\t\t\tvar path = selElems[0];\n
\t\t\tif (path) {\n
\t\t\t\tvar seglist = path.pathSegList,\n
\t\t\t\t\tlast = seglist.numberOfItems - 1;\n
\t\t\t\t// is closed\n
\t\t\t\tif (seglist.getItem(last).pathSegType == 1) {\n
\t\t\t\t\tseglist.removeItem(last);\n
\t\t\t\t} else {\n
\t\t\t\t\tseglist.appendItem(path.createSVGPathSegClosePath());\n
\t\t\t\t}\n
\t\t\t\tupdateButton(path);\n
\t\t\t}\n
\t\t};\n
\n
\treturn {\n
\t\tname: \'ClosePath\',\n
\t\tsvgicons: svgEditor.curConfig.extPath + \'closepath_icons.svg\',\n
\t\tbuttons: [{\n
\t\t\tid: \'tool_openpath\',\n
\t\t\ttype: \'context\',\n
\t\t\tpanel: \'closepath_panel\',\n
\t\t\ttitle: \'Open path\',\n
\t\t\tevents: {\n
\t\t\t\tclick: function() {\n
\t\t\t\t\ttoggleClosed();\n
\t\t\t\t}\n
\t\t\t}\n
\t\t},\n
\t\t{\n
\t\t\tid: \'tool_closepath\',\n
\t\t\ttype: \'context\',\n
\t\t\tpanel: \'closepath_panel\',\n
\t\t\ttitle: \'Close path\',\n
\t\t\tevents: {\n
\t\t\t\tclick: function() {\n
\t\t\t\t\ttoggleClosed();\n
\t\t\t\t}\n
\t\t\t}\n
\t\t}],\n
\t\tcallback: function() {\n
\t\t\t$(\'#closepath_panel\').hide();\n
\t\t},\n
\t\tselectedChanged: function(opts) {\n
\t\t\tselElems = opts.elems;\n
\t\t\tvar i = selElems.length;\n
\t\t\twhile (i--) {\n
\t\t\t\tvar elem = selElems[i];\n
\t\t\t\tif (elem && elem.tagName == \'path\') {\n
\t\t\t\t\tif (opts.selectedElement && !opts.multiselected) {\n
\t\t\t\t\t\tshowPanel(true);\n
\t\t\t\t\t} else {\n
\t\t\t\t\t\tshowPanel(false);\n
\t\t\t\t\t}\n
\t\t\t\t} else {\n
\t\t\t\t\tshowPanel(false);\n
\t\t\t\t}\n
\t\t\t}\n
\t\t}\n
\t};\n
});\n


]]></string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>2091</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
