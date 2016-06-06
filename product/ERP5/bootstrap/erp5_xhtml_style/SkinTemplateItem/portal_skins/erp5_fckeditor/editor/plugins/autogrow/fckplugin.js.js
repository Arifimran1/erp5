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
            <value> <string>ts83858910.16</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>fckplugin.js</string> </value>
        </item>
        <item>
            <key> <string>content_type</string> </key>
            <value> <string>application/javascript</string> </value>
        </item>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

﻿/*\r\n
 * FCKeditor - The text editor for Internet - http://www.fckeditor.net\r\n
 * Copyright (C) 2003-2010 Frederico Caldeira Knabben\r\n
 *\r\n
 * == BEGIN LICENSE ==\r\n
 *\r\n
 * Licensed under the terms of any of the following licenses at your\r\n
 * choice:\r\n
 *\r\n
 *  - GNU General Public License Version 2 or later (the "GPL")\r\n
 *    http://www.gnu.org/licenses/gpl.html\r\n
 *\r\n
 *  - GNU Lesser General Public License Version 2.1 or later (the "LGPL")\r\n
 *    http://www.gnu.org/licenses/lgpl.html\r\n
 *\r\n
 *  - Mozilla Public License Version 1.1 or later (the "MPL")\r\n
 *    http://www.mozilla.org/MPL/MPL-1.1.html\r\n
 *\r\n
 * == END LICENSE ==\r\n
 *\r\n
 * Plugin: automatically resizes the editor until a configurable maximun\r\n
 * height (FCKConfig.AutoGrowMax), based on its contents.\r\n
 */\r\n
\r\n
var FCKAutoGrow = {\r\n
\tMIN_HEIGHT : window.frameElement.offsetHeight,\r\n
\r\n
\tCheck : function()\r\n
\t{\r\n
\t\tvar delta = FCKAutoGrow.GetHeightDelta() ;\r\n
\t\tif ( delta != 0 )\r\n
\t\t{\r\n
\t\t\tvar newHeight = window.frameElement.offsetHeight + delta ;\r\n
\r\n
\t\t\tnewHeight = FCKAutoGrow.GetEffectiveHeight( newHeight ) ;\r\n
\r\n
\t\t\tif ( newHeight != window.frameElement.height )\r\n
\t\t\t{\r\n
\t\t\t\twindow.frameElement.style.height = newHeight + "px" ;\r\n
\r\n
\t\t\t\t// Gecko browsers use an onresize handler to update the innermost\r\n
\t\t\t\t// IFRAME\'s height. If the document is modified before the onresize\r\n
\t\t\t\t// is triggered, the plugin will miscalculate the new height. Thus,\r\n
\t\t\t\t// forcibly trigger onresize. #1336\r\n
\t\t\t\tif ( typeof window.onresize == \'function\' )\r\n
\t\t\t\t{\r\n
\t\t\t\t\twindow.onresize() ;\r\n
\t\t\t\t}\r\n
\t\t\t}\r\n
\t\t}\r\n
\t},\r\n
\r\n
\tCheckEditorStatus : function( sender, status )\r\n
\t{\r\n
\t\tif ( status == FCK_STATUS_COMPLETE )\r\n
\t\t\tFCKAutoGrow.Check() ;\r\n
\t},\r\n
\r\n
\tGetEffectiveHeight : function( height )\r\n
\t{\r\n
\t\tif ( height < FCKAutoGrow.MIN_HEIGHT )\r\n
\t\t\theight = FCKAutoGrow.MIN_HEIGHT;\r\n
\t\telse\r\n
\t\t{\r\n
\t\t\tvar max = FCKConfig.AutoGrowMax;\r\n
\t\t\tif ( max && max > 0 && height > max )\r\n
\t\t\t\theight = max;\r\n
\t\t}\r\n
\r\n
\t\treturn height;\r\n
\t},\r\n
\r\n
\tGetHeightDelta : function()\r\n
\t{\r\n
\t\tvar oInnerDoc = FCK.EditorDocument ;\r\n
\r\n
\t\tvar iFrameHeight ;\r\n
\t\tvar iInnerHeight ;\r\n
\r\n
\t\tif ( FCKBrowserInfo.IsIE )\r\n
\t\t{\r\n
\t\t\tiFrameHeight = FCK.EditorWindow.frameElement.offsetHeight ;\r\n
\t\t\tiInnerHeight = oInnerDoc.body.scrollHeight ;\r\n
\t\t}\r\n
\t\telse\r\n
\t\t{\r\n
\t\t\tiFrameHeight = FCK.EditorWindow.innerHeight ;\r\n
\t\t\tiInnerHeight = oInnerDoc.body.offsetHeight +\r\n
\t\t\t\t( parseInt( FCKDomTools.GetCurrentElementStyle( oInnerDoc.body, \'margin-top\' ), 10 ) || 0 ) +\r\n
\t\t\t\t( parseInt( FCKDomTools.GetCurrentElementStyle( oInnerDoc.body, \'margin-bottom\' ), 10 ) || 0 ) ;\r\n
\t\t}\r\n
\r\n
\t\treturn iInnerHeight - iFrameHeight ;\r\n
\t},\r\n
\r\n
\tSetListeners : function()\r\n
\t{\r\n
\t\tif ( FCK.EditMode != FCK_EDITMODE_WYSIWYG )\r\n
\t\t\treturn ;\r\n
\r\n
\t\tFCK.EditorWindow.attachEvent( \'onscroll\', FCKAutoGrow.Check ) ;\r\n
\t\tFCK.EditorDocument.attachEvent( \'onkeyup\', FCKAutoGrow.Check ) ;\r\n
\t}\r\n
};\r\n
\r\n
FCK.AttachToOnSelectionChange( FCKAutoGrow.Check ) ;\r\n
\r\n
if ( FCKBrowserInfo.IsIE )\r\n
\tFCK.Events.AttachEvent( \'OnAfterSetHTML\', FCKAutoGrow.SetListeners ) ;\r\n
\r\n
FCK.Events.AttachEvent( \'OnStatusChange\', FCKAutoGrow.CheckEditorStatus ) ;\r\n


]]></string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>3061</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
