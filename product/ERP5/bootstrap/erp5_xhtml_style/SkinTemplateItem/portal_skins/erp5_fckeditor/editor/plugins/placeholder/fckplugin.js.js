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
 * Plugin to insert "Placeholders" in the editor.\r\n
 */\r\n
\r\n
// Register the related command.\r\n
FCKCommands.RegisterCommand( \'Placeholder\', new FCKDialogCommand( \'Placeholder\', FCKLang.PlaceholderDlgTitle, FCKPlugins.Items[\'placeholder\'].Path + \'fck_placeholder.html\', 340, 160 ) ) ;\r\n
\r\n
// Create the "Plaholder" toolbar button.\r\n
var oPlaceholderItem = new FCKToolbarButton( \'Placeholder\', FCKLang.PlaceholderBtn ) ;\r\n
oPlaceholderItem.IconPath = FCKPlugins.Items[\'placeholder\'].Path + \'placeholder.gif\' ;\r\n
\r\n
FCKToolbarItems.RegisterItem( \'Placeholder\', oPlaceholderItem ) ;\r\n
\r\n
\r\n
// The object used for all Placeholder operations.\r\n
var FCKPlaceholders = new Object() ;\r\n
\r\n
// Add a new placeholder at the actual selection.\r\n
FCKPlaceholders.Add = function( name )\r\n
{\r\n
\tvar oSpan = FCK.InsertElement( \'span\' ) ;\r\n
\tthis.SetupSpan( oSpan, name ) ;\r\n
}\r\n
\r\n
FCKPlaceholders.SetupSpan = function( span, name )\r\n
{\r\n
\tspan.innerHTML = \'[[ \' + name + \' ]]\' ;\r\n
\r\n
\tspan.style.backgroundColor = \'#ffff00\' ;\r\n
\tspan.style.color = \'#000000\' ;\r\n
\r\n
\tif ( FCKBrowserInfo.IsGecko )\r\n
\t\tspan.style.cursor = \'default\' ;\r\n
\r\n
\tspan._fckplaceholder = name ;\r\n
\tspan.contentEditable = false ;\r\n
\r\n
\t// To avoid it to be resized.\r\n
\tspan.onresizestart = function()\r\n
\t{\r\n
\t\tFCK.EditorWindow.event.returnValue = false ;\r\n
\t\treturn false ;\r\n
\t}\r\n
}\r\n
\r\n
// On Gecko we must do this trick so the user select all the SPAN when clicking on it.\r\n
FCKPlaceholders._SetupClickListener = function()\r\n
{\r\n
\tFCKPlaceholders._ClickListener = function( e )\r\n
\t{\r\n
\t\tif ( e.target.tagName == \'SPAN\' && e.target._fckplaceholder )\r\n
\t\t\tFCKSelection.SelectNode( e.target ) ;\r\n
\t}\r\n
\r\n
\tFCK.EditorDocument.addEventListener( \'click\', FCKPlaceholders._ClickListener, true ) ;\r\n
}\r\n
\r\n
// Open the Placeholder dialog on double click.\r\n
FCKPlaceholders.OnDoubleClick = function( span )\r\n
{\r\n
\tif ( span.tagName == \'SPAN\' && span._fckplaceholder )\r\n
\t\tFCKCommands.GetCommand( \'Placeholder\' ).Execute() ;\r\n
}\r\n
\r\n
FCK.RegisterDoubleClickHandler( FCKPlaceholders.OnDoubleClick, \'SPAN\' ) ;\r\n
\r\n
// Check if a Placholder name is already in use.\r\n
FCKPlaceholders.Exist = function( name )\r\n
{\r\n
\tvar aSpans = FCK.EditorDocument.getElementsByTagName( \'SPAN\' ) ;\r\n
\r\n
\tfor ( var i = 0 ; i < aSpans.length ; i++ )\r\n
\t{\r\n
\t\tif ( aSpans[i]._fckplaceholder == name )\r\n
\t\t\treturn true ;\r\n
\t}\r\n
\r\n
\treturn false ;\r\n
}\r\n
\r\n
if ( FCKBrowserInfo.IsIE )\r\n
{\r\n
\tFCKPlaceholders.Redraw = function()\r\n
\t{\r\n
\t\tif ( FCK.EditMode != FCK_EDITMODE_WYSIWYG )\r\n
\t\t\treturn ;\r\n
\r\n
\t\tvar aPlaholders = FCK.EditorDocument.body.innerText.match( /\\[\\[[^\\[\\]]+\\]\\]/g ) ;\r\n
\t\tif ( !aPlaholders )\r\n
\t\t\treturn ;\r\n
\r\n
\t\tvar oRange = FCK.EditorDocument.body.createTextRange() ;\r\n
\r\n
\t\tfor ( var i = 0 ; i < aPlaholders.length ; i++ )\r\n
\t\t{\r\n
\t\t\tif ( oRange.findText( aPlaholders[i] ) )\r\n
\t\t\t{\r\n
\t\t\t\tvar sName = aPlaholders[i].match( /\\[\\[\\s*([^\\]]*?)\\s*\\]\\]/ )[1] ;\r\n
\t\t\t\toRange.pasteHTML( \'<span style="color: #000000; background-color: #ffff00" contenteditable="false" _fckplaceholder="\' + sName + \'">\' + aPlaholders[i] + \'</span>\' ) ;\r\n
\t\t\t}\r\n
\t\t}\r\n
\t}\r\n
}\r\n
else\r\n
{\r\n
\tFCKPlaceholders.Redraw = function()\r\n
\t{\r\n
\t\tif ( FCK.EditMode != FCK_EDITMODE_WYSIWYG )\r\n
\t\t\treturn ;\r\n
\r\n
\t\tvar oInteractor = FCK.EditorDocument.createTreeWalker( FCK.EditorDocument.body, NodeFilter.SHOW_TEXT, FCKPlaceholders._AcceptNode, true ) ;\r\n
\r\n
\t\tvar\taNodes = new Array() ;\r\n
\r\n
\t\twhile ( ( oNode = oInteractor.nextNode() ) )\r\n
\t\t{\r\n
\t\t\taNodes[ aNodes.length ] = oNode ;\r\n
\t\t}\r\n
\r\n
\t\tfor ( var n = 0 ; n < aNodes.length ; n++ )\r\n
\t\t{\r\n
\t\t\tvar aPieces = aNodes[n].nodeValue.split( /(\\[\\[[^\\[\\]]+\\]\\])/g ) ;\r\n
\r\n
\t\t\tfor ( var i = 0 ; i < aPieces.length ; i++ )\r\n
\t\t\t{\r\n
\t\t\t\tif ( aPieces[i].length > 0 )\r\n
\t\t\t\t{\r\n
\t\t\t\t\tif ( aPieces[i].indexOf( \'[[\' ) == 0 )\r\n
\t\t\t\t\t{\r\n
\t\t\t\t\t\tvar sName = aPieces[i].match( /\\[\\[\\s*([^\\]]*?)\\s*\\]\\]/ )[1] ;\r\n
\r\n
\t\t\t\t\t\tvar oSpan = FCK.EditorDocument.createElement( \'span\' ) ;\r\n
\t\t\t\t\t\tFCKPlaceholders.SetupSpan( oSpan, sName ) ;\r\n
\r\n
\t\t\t\t\t\taNodes[n].parentNode.insertBefore( oSpan, aNodes[n] ) ;\r\n
\t\t\t\t\t}\r\n
\t\t\t\t\telse\r\n
\t\t\t\t\t\taNodes[n].parentNode.insertBefore( FCK.EditorDocument.createTextNode( aPieces[i] ) , aNodes[n] ) ;\r\n
\t\t\t\t}\r\n
\t\t\t}\r\n
\r\n
\t\t\taNodes[n].parentNode.removeChild( aNodes[n] ) ;\r\n
\t\t}\r\n
\r\n
\t\tFCKPlaceholders._SetupClickListener() ;\r\n
\t}\r\n
\r\n
\tFCKPlaceholders._AcceptNode = function( node )\r\n
\t{\r\n
\t\tif ( /\\[\\[[^\\[\\]]+\\]\\]/.test( node.nodeValue ) )\r\n
\t\t\treturn NodeFilter.FILTER_ACCEPT ;\r\n
\t\telse\r\n
\t\t\treturn NodeFilter.FILTER_SKIP ;\r\n
\t}\r\n
}\r\n
\r\n
FCK.Events.AttachEvent( \'OnAfterSetHTML\', FCKPlaceholders.Redraw ) ;\r\n
\r\n
// We must process the SPAN tags to replace then with the real resulting value of the placeholder.\r\n
FCKXHtml.TagProcessors[\'span\'] = function( node, htmlNode )\r\n
{\r\n
\tif ( htmlNode._fckplaceholder )\r\n
\t\tnode = FCKXHtml.XML.createTextNode( \'[[\' + htmlNode._fckplaceholder + \']]\' ) ;\r\n
\telse\r\n
\t\tFCKXHtml._AppendChildNodes( node, htmlNode, false ) ;\r\n
\r\n
\treturn node ;\r\n
}\r\n


]]></string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>5416</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
