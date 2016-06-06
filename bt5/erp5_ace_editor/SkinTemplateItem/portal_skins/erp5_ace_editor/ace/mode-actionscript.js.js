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
            <value> <string>ts83646622.51</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>mode-actionscript.js</string> </value>
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
 *\n
 * Contributor(s):\n
 *\n
 *\n
 *\n
 * ***** END LICENSE BLOCK ***** */\n
\n
define(\'ace/mode/actionscript\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text\', \'ace/tokenizer\', \'ace/mode/actionscript_highlight_rules\', \'ace/mode/folding/cstyle\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextMode = require("./text").Mode;\n
var Tokenizer = require("../tokenizer").Tokenizer;\n
var ActionScriptHighlightRules = require("./actionscript_highlight_rules").ActionScriptHighlightRules;\n
var FoldMode = require("./folding/cstyle").FoldMode;\n
\n
var Mode = function() {\n
    this.HighlightRules = ActionScriptHighlightRules;\n
    this.foldingRules = new FoldMode();\n
};\n
oop.inherits(Mode, TextMode);\n
\n
(function() {\n
    this.lineCommentStart = "//";\n
    this.blockComment = {start: "/*", end: "*/"};\n
}).call(Mode.prototype);\n
\n
exports.Mode = Mode;\n
});\n
\n
define(\'ace/mode/actionscript_highlight_rules\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/mode/text_highlight_rules\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;\n
\n
var ActionScriptHighlightRules = function() {\n
\n
    this.$rules = { start: \n
       [ { token: \'support.class.actionscript.2\',\n
           regex: \'\\\\b(?:R(?:ecordset|DBMSResolver|adioButton(?:Group)?)|X(?:ML(?:Socket|Node|Connector)?|UpdateResolverDataHolder)|M(?:M(?:Save|Execute)|icrophoneMicrophone|o(?:use|vieClip(?:Loader)?)|e(?:nu(?:Bar)?|dia(?:Controller|Display|Playback))|ath)|B(?:yName|inding|utton)|S(?:haredObject|ystem|crollPane|t(?:yleSheet|age|ream)|ound|e(?:ndEvent|rviceObject)|OAPCall|lide)|N(?:umericStepper|et(?:stream|S(?:tream|ervices)|Connection|Debug(?:Config)?))|C(?:heckBox|o(?:ntextMenu(?:Item)?|okie|lor|m(?:ponentMixins|boBox))|ustomActions|lient|amera)|T(?:ypedValue|ext(?:Snapshot|Input|F(?:ield|ormat)|Area)|ree|AB)|Object|D(?:ownload|elta(?:Item|Packet)?|at(?:e(?:Chooser|Field)?|a(?:G(?:lue|rid)|Set|Type)))|U(?:RL|TC|IScrollBar)|P(?:opUpManager|endingCall|r(?:intJob|o(?:duct|gressBar)))|E(?:ndPoint|rror)|Video|Key|F(?:RadioButton|GridColumn|MessageBox|BarChart|S(?:croll(?:Bar|Pane)|tyleFormat|plitView)|orm|C(?:heckbox|omboBox|alendar)|unction|T(?:icker|ooltip(?:Lite)?|ree(?:Node)?)|IconButton|D(?:ataGrid|raggablePane)|P(?:ieChart|ushButton|ro(?:gressBar|mptBox))|L(?:i(?:stBox|neChart)|oadingBox)|AdvancedMessageBox)|W(?:indow|SDLURL|ebService(?:Connector)?)|L(?:ist|o(?:calConnection|ad(?:er|Vars)|g)|a(?:unch|bel))|A(?:sBroadcaster|cc(?:ordion|essibility)|S(?:Set(?:Native|PropFlags)|N(?:ew|ative)|C(?:onstructor|lamp(?:2)?)|InstanceOf)|pplication|lert|rray))\\\\b\' },\n
         { token: \'support.function.actionscript.2\',\n
           regex: \'\\\\b(?:s(?:h(?:ift|ow(?:GridLines|Menu|Border|Settings|Headers|ColumnHeaders|Today|Preferences)?|ad(?:ow|ePane))|c(?:hema|ale(?:X|Mode|Y|Content)|r(?:oll(?:Track|Drag)?|een(?:Resolution|Color|DPI)))|t(?:yleSheet|op(?:Drag|A(?:nimation|llSounds|gent))?|epSize|a(?:tus|rt(?:Drag|A(?:nimation|gent))?))|i(?:n|ze|lence(?:TimeOut|Level))|o(?:ngname|urce|rt(?:Items(?:By)?|On(?:HeaderRelease)?|able(?:Columns)?)?)|u(?:ppressInvalidCalls|bstr(?:ing)?)|p(?:li(?:ce|t)|aceCol(?:umnsEqually|lumnsEqually))|e(?:nd(?:DefaultPushButtonEvent|AndLoad)?|curity|t(?:R(?:GB|o(?:otNode|w(?:Height|Count))|esizable(?:Columns)?|a(?:nge|te))|G(?:ain|roupName)|X(?:AxisTitle)?|M(?:i(?:n(?:imum|utes)|lliseconds)|o(?:nth(?:Names)?|tionLevel|de)|ultilineMode|e(?:ssage|nu(?:ItemEnabled(?:At)?|EnabledAt)|dia)|a(?:sk|ximum))|B(?:u(?:tton(?:s|Width)|fferTime)|a(?:seTabIndex|ndwidthLimit|ckground))|S(?:howAsDisabled|croll(?:ing|Speed|Content|Target|P(?:osition|roperties)|barState|Location)|t(?:yle(?:Property)?|opOnFocus|at(?:us|e))|i(?:ze|lenceLevel)|ort(?:able(?:Columns)?|Function)|p(?:litterBarPosition|acing)|e(?:conds|lect(?:Multiple|ion(?:Required|Type)?|Style|Color|ed(?:Node(?:s)?|Cell|I(?:nd(?:ices|ex)|tem(?:s)?))?|able))|kin|m(?:oothness|allScroll))|H(?:ighlight(?:s|Color)|Scroll|o(?:urs|rizontal)|eader(?:Symbol|Height|Text|Property|Format|Width|Location)?|as(?:Shader|CloseBox))|Y(?:ear|AxisTitle)?|N(?:ode(?:Properties|ExpansionHandler)|ewTextFormat)|C(?:h(?:ildNodes|a(?:ngeHandler|rt(?:Title|EventHandler)))|o(?:ntent(?:Size)?|okie|lumns)|ell(?:Symbol|Data)|l(?:i(?:ckHandler|pboard)|oseHandler)|redentials)|T(?:ype(?:dVaule)?|i(?:tle(?:barHeight)?|p(?:Target|Offset)?|me(?:out(?:Handler)?)?)|oggle|extFormat|ransform)|I(?:s(?:Branch|Open)|n(?:terval|putProperty)|con(?:SymbolName)?|te(?:rator|m(?:ByKey|Symbol)))|Orientation|D(?:i(?:splay(?:Range|Graphics|Mode|Clip|Text|edMonth)|rection)|uration|e(?:pth(?:Below|To|Above)|fault(?:GatewayURL|Mappings|NodeIconSymbolName)|l(?:iveryMode|ay)|bug(?:ID)?)|a(?:yOfWeekNames|t(?:e(?:Filter)?|a(?:Mapping(?:s)?|Item(?:Text|Property|Format)|Provider|All(?:Height|Property|Format|Width))?))|ra(?:wConnectors|gContent))|U(?:se(?:Shadow|HandCursor|EchoSuppression|rInput|Fade)|TC(?:M(?:i(?:nutes|lliseconds)|onth)|Seconds|Hours|Date|FullYear))|P(?:osition|ercentComplete|an(?:e(?:M(?:inimumSize|aximumSize)|Size|Title))?|ro(?:pert(?:y(?:Data)?|iesAt)|gress))|E(?:nabled|dit(?:Handler|able)|xpand(?:NodeTrigger|erSymbolName))|V(?:Scroll|olume|alue(?:Source)?)|KeyFrameInterval|Quality|F(?:i(?:eld|rst(?:DayOfWeek|VisibleNode))|ocus|ullYear|ps|ade(?:InLength|OutLength)|rame(?:Color|Width))|Width|L(?:ine(?:Color|Weight)|o(?:opback|adTarget)|a(?:rgeScroll|bel(?:Source|Placement)?))|A(?:s(?:Boolean|String|Number)|n(?:yTypedValue|imation)|ctiv(?:e(?:State(?:Handler)?|Handler)|ateHandler)|utoH(?:ideScrollBar|eight)))?|paratorBefore|ek|lect(?:ion(?:Disabled|Unfocused)?|ed(?:Node(?:s)?|Child|I(?:nd(?:ices|ex)|tem(?:s)?)|Dat(?:e|a))?|able(?:Ranges)?)|rver(?:String)?)|kip|qrt|wapDepths|lice|aveToSharedObj|moothing)|h(?:scroll(?:Policy)?|tml(?:Text)?|i(?:t(?:Test(?:TextNearPos)?|Area)|de(?:BuiltInItems|Child)?|ghlight(?:2D|3D)?)|orizontal|e(?:ight|ader(?:Re(?:nderer|lease)|Height|Text))|P(?:osition|ageScrollSize)|a(?:s(?:childNodes|MP3|S(?:creen(?:Broadcast|Playback)|treaming(?:Video|Audio)|ort)|Next|OwnProperty|Pr(?:inting|evious)|EmbeddedVideo|VideoEncoder|A(?:ccesibility|udio(?:Encoder)?))|ndlerName)|LineScrollSize)|ye(?:sLabel|ar)|n(?:o(?:t|de(?:Name|Close|Type|Open|Value)|Label)|u(?:llValue|mChild(?:S(?:creens|lides)|ren|Forms))|e(?:w(?:Item|line|Value|LocationDialog)|xt(?:S(?:cene|ibling|lide)|TabIndex|Value|Frame)?)?|ame(?:s)?)|c(?:h(?:ildNodes|eck|a(?:nge(?:sPending)?|r(?:CodeAt|At))|r)|o(?:s|n(?:st(?:ant|ructor)|nect|c(?:urrency|at)|t(?:ent(?:Type|Path)?|ains|rol(?:Placement|lerPolicy))|denseWhite|version)|py|l(?:or|umn(?:Stretch|Name(?:s)?|Count))|m(?:p(?:onent|lete)|ment))|u(?:stomItems|ePoint(?:s)?|r(?:veTo|Value|rent(?:Slide|ChildSlide|Item|F(?:ocused(?:S(?:creen|lide)|Form)|ps))))|e(?:il|ll(?:Renderer|Press|Edit|Focus(?:In|Out)))|l(?:i(?:ck|ents)|o(?:se(?:Button|Pane)?|ne(?:Node)?)|ear(?:S(?:haredObjects|treams)|Timeout|Interval)?)|a(?:ncelLabel|tch|p(?:tion|abilities)|l(?:cFields|l(?:e(?:e|r))?))|reate(?:GatewayConnection|Menu|Se(?:rver|gment)|C(?:hild(?:AtDepth)?|l(?:ient|ass(?:ChildAtDepth|Object(?:AtDepth)?))|all)|Text(?:Node|Field)|Item|Object(?:AtDepth)?|PopUp|E(?:lement|mptyMovieClip)))|t(?:h(?:is|row)|ype(?:of|Name)?|i(?:tle(?:StyleDeclaration)?|me(?:out)?)|o(?:talTime|String|olTipText|p|UpperCase|ggle(?:HighQuality)?|Lo(?:caleString|werCase))|e(?:st|llTarget|xt(?:RightMargin|Bold|S(?:ize|elected)|Height|Color|I(?:ndent|talic)|Disabled|Underline|F(?:ield|ont)|Width|LeftMargin|Align)?)|a(?:n|rget(?:Path)?|b(?:Stops|Children|Index|Enabled|leName))|r(?:y|igger|ac(?:e|k(?:AsMenu)?)))|i(?:s(?:Running|Branch|NaN|Con(?:soleOpen|nected)|Toggled|Installed|Open|D(?:own|ebugger)|P(?:urchased|ro(?:totypeOf|pertyEnumerable))|Empty|F(?:inite|ullyPopulated)|Local|Active)|n(?:s(?:tall|ertBefore)|cludeDeltaPacketInfo|t|it(?:ialize|Component|Pod|A(?:pplication|gent))?|de(?:nt|terminate|x(?:InParent(?:Slide|Form)?|Of)?)|put|validate|finity|LocalInternetCache)?|con(?:F(?:ield|unction))?|t(?:e(?:ratorScrolled|m(?:s|RollO(?:ut|ver)|ClassName))|alic)|d3|p|fFrameLoaded|gnore(?:Case|White))|o(?:s|n(?:R(?:ollO(?:ut|ver)|e(?:s(?:ize|ult)|l(?:ease(?:Outside)?|aseOutside)))|XML|Mouse(?:Move|Down|Up|Wheel)|S(?:ync|croller|tatus|oundComplete|e(?:tFocus|lect(?:edItem)?))|N(?:oticeEvent|etworkChange)|C(?:hanged|onnect|l(?:ipEvent|ose))|ID3|D(?:isconnect|eactivate|ata|ragO(?:ut|ver))|Un(?:install|load)|P(?:aymentResult|ress)|EnterFrame|K(?:illFocus|ey(?:Down|Up))|Fault|Lo(?:ad|g)|A(?:ctiv(?:ity|ate)|ppSt(?:op|art)))?|pe(?:n|ration)|verLayChildren|kLabel|ldValue|r(?:d)?)|d(?:i(?:s(?:connect|play(?:Normal|ed(?:Month|Year)|Full)|able(?:Shader|d(?:Ranges|Days)|CloseBox|Events))|rection)|o(?:cTypeDecl|tall|Decoding|main|LazyDecoding)|u(?:plicateMovieClip|ration)|e(?:stroy(?:ChildAt|Object)|code|fault(?:PushButton(?:Enabled)?|KeydownHandler)?|l(?:ta(?:Packet(?:Changed)?)?|ete(?:PopUp|All)?)|blocking)|a(?:shBoardSave|yNames|ta(?:Provider)?|rkshadow)|r(?:opdown(?:Width)?|a(?:w|gO(?:ut|ver))))|u(?:se(?:Sort|HandCursor|Codepage|EchoSuppression)|n(?:shift|install|derline|escape|format|watch|lo(?:ck|ad(?:Movie(?:Num)?)?))|pdate(?:Results|Mode|I(?:nputProperties|tem(?:ByIndex)?)|P(?:acket|roperties)|View|AfterEvent)|rl)|join|p(?:ixelAspectRatio|o(?:sition|p|w)|u(?:sh|rge|blish)|ercen(?:tComplete|Loaded)|lay(?:head(?:Change|Time)|ing|Hidden|erType)?|a(?:ssword|use|r(?:se(?:XML|CSS|Int|Float)|ent(?:Node|Is(?:S(?:creen|lide)|Form))|ams))|r(?:int(?:Num|AsBitmap(?:Num)?)?|o(?:to(?:type)?|pert(?:y|ies)|gress)|e(?:ss|v(?:ious(?:S(?:ibling|lide)|Value)?|Scene|Frame)|ferred(?:Height|Width))))|e(?:scape|n(?:code(?:r)?|ter(?:Frame)?|dFill|able(?:Shader|d|CloseBox|Events))|dit(?:able|Field|LocationDialog)|v(?:ent|al(?:uate)?)|q|x(?:tended|p|ec(?:ute)?|actSettings)|m(?:phasized(?:StyleDeclaration)?|bedFonts))|v(?:i(?:sible|ewPod)|ScrollPolicy|o(?:id|lume)|ersion|P(?:osition|ageScrollSize)|a(?:l(?:idat(?:ionError|e(?:Property|ActivationKey)?)|ue(?:Of)?)|riable)|LineScrollSize)|k(?:ind|ey(?:Down|Up|Press|FrameInterval))|q(?:sort|uality)|f(?:scommand|i(?:n(?:d(?:Text|First|Last)?|ally)|eldInfo|lter(?:ed|Func)?|rst(?:Slide|Child|DayOfWeek|VisibleNode)?)|o(?:nt|cus(?:In|edCell|Out|Enabled)|r(?:egroundDisabled|mat(?:ter)?))|unctionName|ps|l(?:oor|ush)|ace|romCharCode)|w(?:i(?:th|dth)|ordWrap|atch|riteAccess)|l(?:t|i(?:st(?:Owner)?|ne(?:Style|To))|o(?:c(?:k|a(?:t(?:ion|eByld)|l(?:ToGlobal|FileReadDisable)))|opback|ad(?:Movie(?:Num)?|S(?:crollContent|ound)|ed|Variables(?:Num)?|Application)?|g(?:Changes)?)|e(?:ngth|ft(?:Margin)?|ading)?|a(?:st(?:Slide|Child|Index(?:Of)?)?|nguage|b(?:el(?:Placement|F(?:ield|unction))?|leField)))|a(?:s(?:scociate(?:Controller|Display)|in|pectRatio|function)|nd|c(?:ceptConnection|tiv(?:ityLevel|ePlayControl)|os)|t(?:t(?:ach(?:Movie|Sound|Video|Audio)|ributes)|an(?:2)?)|dd(?:header|RequestHeader|Menu(?:Item(?:At)?|At)?|Sort|Header|No(?:tice|de(?:At)?)|C(?:olumn(?:At)?|uePoint)|T(?:oLocalInternetCache|reeNode(?:At)?)|I(?:con|tem(?:s(?:At)?|At)?)|DeltaItem|P(?:od|age|roperty)|EventListener|View|FieldInfo|Listener|Animation)?|uto(?:Size|Play|KeyNav|Load)|pp(?:endChild|ly(?:Changes|Updates)?)|vHardwareDisable|fterLoaded|l(?:ternateRowColors|ign|l(?:ow(?:InsecureDomain|Domain)|Transitions(?:InDone|OutDone))|bum)|r(?:tist|row|g(?:uments|List))|gent|bs)|r(?:ight(?:Margin)?|o(?:ot(?:S(?:creen|lide)|Form)|und|w(?:Height|Count)|llO(?:ut|ver))|e(?:s(?:yncDepth|t(?:orePane|artAnimation|rict)|iz(?:e|able(?:Columns)?)|olveDelta|ult(?:s)?|ponse)|c(?:o(?:ncile(?:Results|Updates)|rd)|eive(?:Video|Audio))|draw|jectConnection|place(?:Sel|ItemAt|AllItems)?|ve(?:al(?:Child)?|rse)|quest(?:SizeChange|Payment)?|f(?:errer|resh(?:ScrollContent|Destinations|Pane|FromSources)?)|lease(?:Outside)?|ad(?:Only|Access)|gister(?:SkinElement|C(?:olor(?:Style|Name)|lass)|InheritingStyle|Proxy)|move(?:Range|M(?:ovieClip|enu(?:Item(?:At)?|At))|Background|Sort|No(?:tice|de(?:sAt|At)?)|C(?:olum(?:nAt|At)|uePoints)|T(?:extField|reeNode(?:At)?)|Item(?:At)?|Pod|EventListener|FromLocalInternetCache|Listener|All(?:C(?:olumns|uePoints)|Items)?))|a(?:ndom|te|dioDot))|g(?:t|oto(?:Slide|NextSlide|PreviousSlide|FirstSlide|LastSlide|And(?:Stop|Play))|e(?:nre|t(?:R(?:GB|o(?:otNode|wCount)|e(?:sizable|mote))|X(?:AxisTitle)?|M(?:i(?:n(?:imum(?:Size)?|utes)|lliseconds)|onth(?:Names)?|ultilineMode|e(?:ssage|nu(?:ItemAt|EnabledAt|At))|aximum(?:Size)?)|B(?:ytes(?:Total|Loaded)|ounds|utton(?:s|Width)|eginIndex|a(?:ndwidthLimit|ckground))|S(?:howAsDisabled|croll(?:ing|Speed|Content|Position|barState|Location)|t(?:yle(?:Names)?|opOnFocus|ate)|ize|o(?:urce|rtState)|p(?:litterBarPosition|acing)|e(?:conds|lect(?:Multiple|ion(?:Required|Type)|Style|ed(?:Node(?:s)?|Cell|Text|I(?:nd(?:ices|ex)|tem(?:s)?))?)|rvice)|moothness|WFVersion)|H(?:ighlight(?:s|Color)|ours|e(?:ight|ader(?:Height|Text|Property|Format|Width|Location)?)|as(?:Shader|CloseBox))|Y(?:ear|AxisTitle)?|N(?:o(?:tices|de(?:DisplayedAt|At))|um(?:Children|berAvailable)|e(?:wTextFormat|xtHighestDepth))|C(?:h(?:ild(?:S(?:creen|lide)|Nodes|Form|At)|artTitle)|o(?:n(?:tent|figInfo)|okie|de|unt|lumn(?:Names|Count|Index|At))|uePoint|ellIndex|loseHandler|a(?:ll|retIndex))|T(?:ypedValue|i(?:tle(?:barHeight)?|p(?:Target|Offset)?|me(?:stamp|zoneOffset|out(?:State|Handler)|r)?)|oggle|ext(?:Extent|Format)?|r(?:ee(?:NodeAt|Length)|ans(?:form|actionId)))|I(?:s(?:Branch|Open)|n(?:stanceAtDepth|d(?:icesByKey|exByKey))|con(?:SymbolName)?|te(?:rator|m(?:sByKey|By(?:Name|Key)|id|ID|At))|d)|O(?:utput(?:Parameter(?:s|ByName)?|Value(?:s)?)|peration|ri(?:entation|ginalCellData))|D(?:i(?:s(?:play(?:Range|Mode|Clip|Index|edMonth)|kUsage)|rection)|uration|e(?:pth|faultNodeIconSymbolName|l(?:taPacket|ay)|bug(?:Config|ID)?)|a(?:y(?:OfWeekNames)?|t(?:e|a(?:Mapping(?:s)?|Item(?:Text|Property|Format)|Label|All(?:Height|Property|Format|Width))?))|rawConnectors)|U(?:se(?:Shadow|HandCursor|rInput|Fade)|RL|TC(?:M(?:i(?:nutes|lliseconds)|onth)|Seconds|Hours|Da(?:y|te)|FullYear))|P(?:o(?:sition|ds)|ercentComplete|a(?:n(?:e(?:M(?:inimums|aximums)|Height|Title|Width))?|rentNode)|r(?:operty(?:Name|Data)?|efer(?:ences|red(?:Height|Width))))|E(?:n(?:dIndex|abled)|ditingData|x(?:panderSymbolName|andNodeTrigger))|V(?:iewed(?:Pods|Applications)|olume|ersion|alue(?:Source)?)|F(?:i(?:eld|rst(?:DayOfWeek|VisibleNode))|o(?:ntList|cus)|ullYear|ade(?:InLength|OutLength)|rame(?:Color|Width))|Width|L(?:ine(?:Color|Weight)|o(?:cal|adTarget)|ength|a(?:stTabIndex|bel(?:Source)?))|A(?:s(?:cii|Boolean|String|Number)|n(?:yTypedValue|imation)|ctiv(?:eState(?:Handler)?|ateHandler)|utoH(?:ideScrollBar|eight)|llItems|gent))?)?|lobal(?:StyleFormat|ToLocal)?|ain|roupName)|x(?:updatePackety|mlDecl)?|m(?:y(?:MethodName|Call)|in(?:imum)?|o(?:nthNames|tion(?:TimeOut|Level)|de(?:lChanged)?|use(?:Move|O(?:ut|ver)|Down(?:Somewhere|Outside)?|Up(?:Somewhere)?|WheelEnabled)|ve(?:To)?)|u(?:ted|lti(?:pleS(?:imultaneousAllowed|elections)|line))|e(?:ssage|nu(?:Show|Hide)?|th(?:od)?|diaType)|a(?:nufacturer|tch|x(?:scroll|hscroll|imum|HPosition|Chars|VPosition)?)|b(?:substring|chr|ord|length))|b(?:ytes(?:Total|Loaded)|indFormat(?:Strings|Function)|o(?:ttom(?:Scroll)?|ld|rder(?:Color)?)|u(?:tton(?:Height|Width)|iltInItems|ffer(?:Time|Length)|llet)|e(?:foreApplyUpdates|gin(?:GradientFill|Fill))|lockIndent|a(?:ndwidth|ckground(?:Style|Color|Disabled)?)|roadcastMessage)|onHTTPStatus)\\\\b\' },\n
         { token: \'support.constant.actionscript.2\',\n
           regex: \'\\\\b(?:__proto__|__resolve|_accProps|_alpha|_changed|_currentframe|_droptarget|_flash|_focusrect|_framesloaded|_global|_height|_highquality|_level|_listeners|_lockroot|_name|_parent|_quality|_root|_rotation|_soundbuftime|_target|_totalframes|_url|_visible|_width|_x|_xmouse|_xscale|_y|_ymouse|_yscale)\\\\b\' },\n
         { token: \'keyword.control.actionscript.2\',\n
           regex: \'\\\\b(?:dynamic|extends|import|implements|interface|public|private|new|static|super|var|for|in|break|continue|while|do|return|if|else|case|switch)\\\\b\' },\n
         { token: \'storage.type.actionscript.2\',\n
           regex: \'\\\\b(?:Boolean|Number|String|Void)\\\\b\' },\n
         { token: \'constant.language.actionscript.2\',\n
           regex: \'\\\\b(?:null|undefined|true|false)\\\\b\' },\n
         { token: \'constant.numeric.actionscript.2\',\n
           regex: \'\\\\b(?:0(?:x|X)[0-9a-fA-F]*|(?:[0-9]+\\\\.?[0-9]*|\\\\.[0-9]+)(?:(?:e|E)(?:\\\\+|-)?[0-9]+)?)(?:L|l|UL|ul|u|U|F|f)?\\\\b\' },\n
         { token: \'punctuation.definition.string.begin.actionscript.2\',\n
           regex: \'"\',\n
           push: \n
            [ { token: \'punctuation.definition.string.end.actionscript.2\',\n
                regex: \'"\',\n
                next: \'pop\' },\n
              { token: \'constant.character.escape.actionscript.2\',\n
                regex: \'\\\\\\\\.\' },\n
              { defaultToken: \'string.quoted.double.actionscript.2\' } ] },\n
         { token: \'punctuation.definition.string.begin.actionscript.2\',\n
           regex: \'\\\'\',\n
           push: \n
            [ { token: \'punctuation.definition.string.end.actionscript.2\',\n
                regex: \'\\\'\',\n
                next: \'pop\' },\n
              { token: \'constant.character.escape.actionscript.2\',\n
                regex: \'\\\\\\\\.\' },\n
              { defaultToken: \'string.quoted.single.actionscript.2\' } ] },\n
         { token: \'support.constant.actionscript.2\',\n
           regex: \'\\\\b(?:BACKSPACE|CAPSLOCK|CONTROL|DELETEKEY|DOWN|END|ENTER|HOME|INSERT|LEFT|LN10|LN2|LOG10E|LOG2E|MAX_VALUE|MIN_VALUE|NEGATIVE_INFINITY|NaN|PGDN|PGUP|PI|POSITIVE_INFINITY|RIGHT|SPACE|SQRT1_2|SQRT2|UP)\\\\b\' },\n
         { token: \'punctuation.definition.comment.actionscript.2\',\n
           regex: \'/\\\\*\',\n
           push: \n
            [ { token: \'punctuation.definition.comment.actionscript.2\',\n
                regex: \'\\\\*/\',\n
                next: \'pop\' },\n
              { defaultToken: \'comment.block.actionscript.2\' } ] },\n
         { token: \'punctuation.definition.comment.actionscript.2\',\n
           regex: \'//.*$\',\n
           push_: \n
            [ { token: \'comment.line.double-slash.actionscript.2\',\n
                regex: \'$\',\n
                next: \'pop\' },\n
              { defaultToken: \'comment.line.double-slash.actionscript.2\' } ] },\n
         { token: \'keyword.operator.actionscript.2\',\n
           regex: \'\\\\binstanceof\\\\b\' },\n
         { token: \'keyword.operator.symbolic.actionscript.2\',\n
           regex: \'[-!%&*+=/?:]\' },\n
         { token: \n
            [ \'meta.preprocessor.actionscript.2\',\n
              \'punctuation.definition.preprocessor.actionscript.2\',\n
              \'meta.preprocessor.actionscript.2\' ],\n
           regex: \'^([ \\\\t]*)(#)([a-zA-Z]+)\' },\n
         { token: \n
            [ \'storage.type.function.actionscript.2\',\n
              \'meta.function.actionscript.2\',\n
              \'entity.name.function.actionscript.2\',\n
              \'meta.function.actionscript.2\',\n
              \'punctuation.definition.parameters.begin.actionscript.2\' ],\n
           regex: \'\\\\b(function)(\\\\s+)([a-zA-Z_]\\\\w*)(\\\\s*)(\\\\()\',\n
           push: \n
            [ { token: \'punctuation.definition.parameters.end.actionscript.2\',\n
                regex: \'\\\\)\',\n
                next: \'pop\' },\n
              { token: \'variable.parameter.function.actionscript.2\',\n
                regex: \'[^,)$]+\' },\n
              { defaultToken: \'meta.function.actionscript.2\' } ] },\n
         { token: \n
            [ \'storage.type.class.actionscript.2\',\n
              \'meta.class.actionscript.2\',\n
              \'entity.name.type.class.actionscript.2\',\n
              \'meta.class.actionscript.2\',\n
              \'storage.modifier.extends.actionscript.2\',\n
              \'meta.class.actionscript.2\',\n
              \'entity.other.inherited-class.actionscript.2\' ],\n
           regex: \'\\\\b(class)(\\\\s+)([a-zA-Z_](?:\\\\w|\\\\.)*)(?:(\\\\s+)(extends)(\\\\s+)([a-zA-Z_](?:\\\\w|\\\\.)*))?\' } ] }\n
    \n
    this.normalizeRules();\n
};\n
\n
ActionScriptHighlightRules.metaData = { fileTypes: [ \'as\' ],\n
      keyEquivalent: \'^~A\',\n
      name: \'ActionScript\',\n
      scopeName: \'source.actionscript.2\' }\n
\n
\n
oop.inherits(ActionScriptHighlightRules, TextHighlightRules);\n
\n
exports.ActionScriptHighlightRules = ActionScriptHighlightRules;\n
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
            <value> <int>23359</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
