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
            <value> <string>ts83858910.13</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>fo.js</string> </value>
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
 * Faroese language file.\r\n
 */\r\n
\r\n
var FCKLang =\r\n
{\r\n
// Language direction : "ltr" (left to right) or "rtl" (right to left).\r\n
Dir\t\t\t\t\t: "ltr",\r\n
\r\n
ToolbarCollapse\t\t: "Fjal amboðsbjálkan",\r\n
ToolbarExpand\t\t: "Vís amboðsbjálkan",\r\n
\r\n
// Toolbar Items and Context Menu\r\n
Save\t\t\t\t: "Goym",\r\n
NewPage\t\t\t\t: "Nýggj síða",\r\n
Preview\t\t\t\t: "Frumsýning",\r\n
Cut\t\t\t\t\t: "Kvett",\r\n
Copy\t\t\t\t: "Avrita",\r\n
Paste\t\t\t\t: "Innrita",\r\n
PasteText\t\t\t: "Innrita reinan tekst",\r\n
PasteWord\t\t\t: "Innrita frá Word",\r\n
Print\t\t\t\t: "Prenta",\r\n
SelectAll\t\t\t: "Markera alt",\r\n
RemoveFormat\t\t: "Strika sniðgeving",\r\n
InsertLinkLbl\t\t: "Tilknýti",\r\n
InsertLink\t\t\t: "Ger/broyt tilknýti",\r\n
RemoveLink\t\t\t: "Strika tilknýti",\r\n
VisitLink\t\t\t: "Opna tilknýti",\r\n
Anchor\t\t\t\t: "Ger/broyt marknastein",\r\n
AnchorDelete\t\t: "Strika marknastein",\r\n
InsertImageLbl\t\t: "Myndir",\r\n
InsertImage\t\t\t: "Set inn/broyt mynd",\r\n
InsertFlashLbl\t\t: "Flash",\r\n
InsertFlash\t\t\t: "Set inn/broyt Flash",\r\n
InsertTableLbl\t\t: "Tabell",\r\n
InsertTable\t\t\t: "Set inn/broyt tabell",\r\n
InsertLineLbl\t\t: "Linja",\r\n
InsertLine\t\t\t: "Ger vatnrætta linju",\r\n
InsertSpecialCharLbl: "Sertekn",\r\n
InsertSpecialChar\t: "Set inn sertekn",\r\n
InsertSmileyLbl\t\t: "Smiley",\r\n
InsertSmiley\t\t: "Set inn Smiley",\r\n
About\t\t\t\t: "Um FCKeditor",\r\n
Bold\t\t\t\t: "Feit skrift",\r\n
Italic\t\t\t\t: "Skráskrift",\r\n
Underline\t\t\t: "Undirstrikað",\r\n
StrikeThrough\t\t: "Yvirstrikað",\r\n
Subscript\t\t\t: "Lækkað skrift",\r\n
Superscript\t\t\t: "Hækkað skrift",\r\n
LeftJustify\t\t\t: "Vinstrasett",\r\n
CenterJustify\t\t: "Miðsett",\r\n
RightJustify\t\t: "Høgrasett",\r\n
BlockJustify\t\t: "Javnir tekstkantar",\r\n
DecreaseIndent\t\t: "Minka reglubrotarinntriv",\r\n
IncreaseIndent\t\t: "Økja reglubrotarinntriv",\r\n
Blockquote\t\t\t: "Blockquote",\r\n
CreateDiv\t\t\t: "Ger DIV øki",\r\n
EditDiv\t\t\t\t: "Broyt DIV øki",\r\n
DeleteDiv\t\t\t: "Strika DIV øki",\r\n
Undo\t\t\t\t: "Angra",\r\n
Redo\t\t\t\t: "Vend aftur",\r\n
NumberedListLbl\t\t: "Talmerktur listi",\r\n
NumberedList\t\t: "Ger/strika talmerktan lista",\r\n
BulletedListLbl\t\t: "Punktmerktur listi",\r\n
BulletedList\t\t: "Ger/strika punktmerktan lista",\r\n
ShowTableBorders\t: "Vís tabellbordar",\r\n
ShowDetails\t\t\t: "Vís í smálutum",\r\n
Style\t\t\t\t: "Typografi",\r\n
FontFormat\t\t\t: "Skriftsnið",\r\n
Font\t\t\t\t: "Skrift",\r\n
FontSize\t\t\t: "Skriftstødd",\r\n
TextColor\t\t\t: "Tekstlitur",\r\n
BGColor\t\t\t\t: "Bakgrundslitur",\r\n
Source\t\t\t\t: "Kelda",\r\n
Find\t\t\t\t: "Leita",\r\n
Replace\t\t\t\t: "Yvirskriva",\r\n
SpellCheck\t\t\t: "Kanna stavseting",\r\n
UniversalKeyboard\t: "Knappaborð",\r\n
PageBreakLbl\t\t: "Síðuskift",\r\n
PageBreak\t\t\t: "Ger síðuskift",\r\n
\r\n
Form\t\t\t: "Formur",\r\n
Checkbox\t\t: "Flugubein",\r\n
RadioButton\t\t: "Radioknøttur",\r\n
TextField\t\t: "Tekstteigur",\r\n
Textarea\t\t: "Tekstumráði",\r\n
HiddenField\t\t: "Fjaldur teigur",\r\n
Button\t\t\t: "Knøttur",\r\n
SelectionField\t: "Valskrá",\r\n
ImageButton\t\t: "Myndaknøttur",\r\n
\r\n
FitWindow\t\t: "Set tekstviðgera til fulla stødd",\r\n
ShowBlocks\t\t: "Vís blokkar",\r\n
\r\n
// Context Menu\r\n
EditLink\t\t\t: "Broyt tilknýti",\r\n
CellCM\t\t\t\t: "Meski",\r\n
RowCM\t\t\t\t: "Rað",\r\n
ColumnCM\t\t\t: "Kolonna",\r\n
InsertRowAfter\t\t: "Set rað inn aftaná",\r\n
InsertRowBefore\t\t: "Set rað inn áðrenn",\r\n
DeleteRows\t\t\t: "Strika røðir",\r\n
InsertColumnAfter\t: "Set kolonnu inn aftaná",\r\n
InsertColumnBefore\t: "Set kolonnu inn áðrenn",\r\n
DeleteColumns\t\t: "Strika kolonnur",\r\n
InsertCellAfter\t\t: "Set meska inn aftaná",\r\n
InsertCellBefore\t: "Set meska inn áðrenn",\r\n
DeleteCells\t\t\t: "Strika meskar",\r\n
MergeCells\t\t\t: "Flætta meskar",\r\n
MergeRight\t\t\t: "Flætta meskar til høgru",\r\n
MergeDown\t\t\t: "Flætta saman",\r\n
HorizontalSplitCell\t: "Kloyv meska vatnrætt",\r\n
VerticalSplitCell\t: "Kloyv meska loddrætt",\r\n
TableDelete\t\t\t: "Strika tabell",\r\n
CellProperties\t\t: "Meskueginleikar",\r\n
TableProperties\t\t: "Tabelleginleikar",\r\n
ImageProperties\t\t: "Myndaeginleikar",\r\n
FlashProperties\t\t: "Flash eginleikar",\r\n
\r\n
AnchorProp\t\t\t: "Eginleikar fyri marknastein",\r\n
ButtonProp\t\t\t: "Eginleikar fyri knøtt",\r\n
CheckboxProp\t\t: "Eginleikar fyri flugubein",\r\n
HiddenFieldProp\t\t: "Eginleikar fyri fjaldan teig",\r\n
RadioButtonProp\t\t: "Eginleikar fyri radioknøtt",\r\n
ImageButtonProp\t\t: "Eginleikar fyri myndaknøtt",\r\n
TextFieldProp\t\t: "Eginleikar fyri tekstteig",\r\n
SelectionFieldProp\t: "Eginleikar fyri valskrá",\r\n
TextareaProp\t\t: "Eginleikar fyri tekstumráði",\r\n
FormProp\t\t\t: "Eginleikar fyri Form",\r\n
\r\n
FontFormats\t\t\t: "Vanligt;Sniðgivið;Adressa;Yvirskrift 1;Yvirskrift 2;Yvirskrift 3;Yvirskrift 4;Yvirskrift 5;Yvirskrift 6",\r\n
\r\n
// Alerts and Messages\r\n
ProcessingXHTML\t\t: "XHTML verður viðgjørt. Bíða við...",\r\n
Done\t\t\t\t: "Liðugt",\r\n
PasteWordConfirm\t: "Teksturin, royndur verður at seta inn, tykist at stava frá Word. Vilt tú reinsa tekstin, áðrenn hann verður settur inn?",\r\n
NotCompatiblePaste\t: "Hetta er bert tøkt í Internet Explorer 5.5 og nýggjari. Vilt tú seta tekstin inn kortini - óreinsaðan?",\r\n
UnknownToolbarItem\t: "Ókendur lutur í amboðsbjálkanum \\"%1\\"",\r\n
UnknownCommand\t\t: "Ókend kommando \\"%1\\"",\r\n
NotImplemented\t\t: "Hetta er ikki tøkt í hesi útgávuni",\r\n
UnknownToolbarSet\t: "Amboðsbjálkin \\"%1\\" finst ikki",\r\n
NoActiveX\t\t\t: "Trygdaruppsetingin í alnótskaganum kann sum er avmarka onkrar hentleikar í tekstviðgeranum. Tú mást loyva møguleikanum \\"Run/Kør ActiveX controls and plug-ins\\". Tú kanst uppliva feilir og ávaringar um tvørrandi hentleikar.",\r\n
BrowseServerBlocked : "Ambætarakagin kundi ikki opnast. Tryggja tær, at allar pop-up forðingar eru óvirknar.",\r\n
DialogBlocked\t\t: "Tað eyðnaðist ikki at opna samskiftisrútin. Tryggja tær, at allar pop-up forðingar eru óvirknar.",\r\n
VisitLinkBlocked\t: "Tað eyðnaðist ikki at opna nýggjan rút. Tryggja tær, at allar pop-up forðingar eru óvirknar.",\r\n
\r\n
// Dialogs\r\n
DlgBtnOK\t\t\t: "Góðkent",\r\n
DlgBtnCancel\t\t: "Avlýst",\r\n
DlgBtnClose\t\t\t: "Lat aftur",\r\n
DlgBtnBrowseServer\t: "Ambætarakagi",\r\n
DlgAdvancedTag\t\t: "Fjølbroytt",\r\n
DlgOpOther\t\t\t: "<Annað>",\r\n
DlgInfoTab\t\t\t: "Upplýsingar",\r\n
DlgAlertUrl\t\t\t: "Vinarliga veit ein URL",\r\n
\r\n
// General Dialogs Labels\r\n
DlgGenNotSet\t\t: "<ikki sett>",\r\n
DlgGenId\t\t\t: "Id",\r\n
DlgGenLangDir\t\t: "Tekstkós",\r\n
DlgGenLangDirLtr\t: "Frá vinstru til høgru (LTR)",\r\n
DlgGenLangDirRtl\t: "Frá høgru til vinstru (RTL)",\r\n
DlgGenLangCode\t\t: "Málkoda",\r\n
DlgGenAccessKey\t\t: "Snarvegisknappur",\r\n
DlgGenName\t\t\t: "Navn",\r\n
DlgGenTabIndex\t\t: "Inntriv indeks",\r\n
DlgGenLongDescr\t\t: "Víðkað URL frágreiðing",\r\n
DlgGenClass\t\t\t: "Typografi klassar",\r\n
DlgGenTitle\t\t\t: "Vegleiðandi heiti",\r\n
DlgGenContType\t\t: "Vegleiðandi innihaldsslag",\r\n
DlgGenLinkCharset\t: "Atknýtt teknsett",\r\n
DlgGenStyle\t\t\t: "Typografi",\r\n
\r\n
// Image Dialog\r\n
DlgImgTitle\t\t\t: "Myndaeginleikar",\r\n
DlgImgInfoTab\t\t: "Myndaupplýsingar",\r\n
DlgImgBtnUpload\t\t: "Send til ambætaran",\r\n
DlgImgURL\t\t\t: "URL",\r\n
DlgImgUpload\t\t: "Send",\r\n
DlgImgAlt\t\t\t: "Alternativur tekstur",\r\n
DlgImgWidth\t\t\t: "Breidd",\r\n
DlgImgHeight\t\t: "Hædd",\r\n
DlgImgLockRatio\t\t: "Læs lutfallið",\r\n
DlgBtnResetSize\t\t: "Upprunastødd",\r\n
DlgImgBorder\t\t: "Bordi",\r\n
DlgImgHSpace\t\t: "Høgri breddi",\r\n
DlgImgVSpace\t\t: "Vinstri breddi",\r\n
DlgImgAlign\t\t\t: "Justering",\r\n
DlgImgAlignLeft\t\t: "Vinstra",\r\n
DlgImgAlignAbsBottom: "Abs botnur",\r\n
DlgImgAlignAbsMiddle: "Abs miðja",\r\n
DlgImgAlignBaseline\t: "Basislinja",\r\n
DlgImgAlignBottom\t: "Botnur",\r\n
DlgImgAlignMiddle\t: "Miðja",\r\n
DlgImgAlignRight\t: "Høgra",\r\n
DlgImgAlignTextTop\t: "Tekst toppur",\r\n
DlgImgAlignTop\t\t: "Ovast",\r\n
DlgImgPreview\t\t: "Frumsýning",\r\n
DlgImgAlertUrl\t\t: "Rita slóðina til myndina",\r\n
DlgImgLinkTab\t\t: "Tilknýti",\r\n
\r\n
// Flash Dialog\r\n
DlgFlashTitle\t\t: "Flash eginleikar",\r\n
DlgFlashChkPlay\t\t: "Avspælingin byrjar sjálv",\r\n
DlgFlashChkLoop\t\t: "Endurspæl",\r\n
DlgFlashChkMenu\t\t: "Ger Flash skrá virkna",\r\n
DlgFlashScale\t\t: "Skalering",\r\n
DlgFlashScaleAll\t: "Vís alt",\r\n
DlgFlashScaleNoBorder\t: "Eingin bordi",\r\n
DlgFlashScaleFit\t: "Neyv skalering",\r\n
\r\n
// Link Dialog\r\n
DlgLnkWindowTitle\t: "Tilknýti",\r\n
DlgLnkInfoTab\t\t: "Tilknýtis upplýsingar",\r\n
DlgLnkTargetTab\t\t: "Mál",\r\n
\r\n
DlgLnkType\t\t\t: "Tilknýtisslag",\r\n
DlgLnkTypeURL\t\t: "URL",\r\n
DlgLnkTypeAnchor\t: "Tilknýti til marknastein í tekstinum",\r\n
DlgLnkTypeEMail\t\t: "Teldupostur",\r\n
DlgLnkProto\t\t\t: "Protokoll",\r\n
DlgLnkProtoOther\t: "<Annað>",\r\n
DlgLnkURL\t\t\t: "URL",\r\n
DlgLnkAnchorSel\t\t: "Vel ein marknastein",\r\n
DlgLnkAnchorByName\t: "Eftir navni á marknasteini",\r\n
DlgLnkAnchorById\t: "Eftir element Id",\r\n
DlgLnkNoAnchors\t\t: "(Eingir marknasteinar eru í hesum dokumentið)",\r\n
DlgLnkEMail\t\t\t: "Teldupost-adressa",\r\n
DlgLnkEMailSubject\t: "Evni",\r\n
DlgLnkEMailBody\t\t: "Breyðtekstur",\r\n
DlgLnkUpload\t\t: "Send til ambætaran",\r\n
DlgLnkBtnUpload\t\t: "Send til ambætaran",\r\n
\r\n
DlgLnkTarget\t\t: "Mál",\r\n
DlgLnkTargetFrame\t: "<ramma>",\r\n
DlgLnkTargetPopup\t: "<popup vindeyga>",\r\n
DlgLnkTargetBlank\t: "Nýtt vindeyga (_blank)",\r\n
DlgLnkTargetParent\t: "Upphavliga vindeygað (_parent)",\r\n
DlgLnkTargetSelf\t: "Sama vindeygað (_self)",\r\n
DlgLnkTargetTop\t\t: "Alt vindeygað (_top)",\r\n
DlgLnkTargetFrameName\t: "Vís navn vindeygans",\r\n
DlgLnkPopWinName\t: "Popup vindeygans navn",\r\n
DlgLnkPopWinFeat\t: "Popup vindeygans víðkaðu eginleikar",\r\n
DlgLnkPopResize\t\t: "Kann broyta stødd",\r\n
DlgLnkPopLocation\t: "Adressulinja",\r\n
DlgLnkPopMenu\t\t: "Skrábjálki",\r\n
DlgLnkPopScroll\t\t: "Rullibjálki",\r\n
DlgLnkPopStatus\t\t: "Støðufrágreiðingarbjálki",\r\n
DlgLnkPopToolbar\t: "Amboðsbjálki",\r\n
DlgLnkPopFullScrn\t: "Fullur skermur (IE)",\r\n
DlgLnkPopDependent\t: "Bundið (Netscape)",\r\n
DlgLnkPopWidth\t\t: "Breidd",\r\n
DlgLnkPopHeight\t\t: "Hædd",\r\n
DlgLnkPopLeft\t\t: "Frástøða frá vinstru",\r\n
DlgLnkPopTop\t\t: "Frástøða frá íerva",\r\n
\r\n
DlnLnkMsgNoUrl\t\t: "Vinarliga skriva tilknýti (URL)",\r\n
DlnLnkMsgNoEMail\t: "Vinarliga skriva teldupost-adressu",\r\n
DlnLnkMsgNoAnchor\t: "Vinarliga vel marknastein",\r\n
DlnLnkMsgInvPopName\t: "Popup navnið má byrja við bókstavi og má ikki hava millumrúm",\r\n
\r\n
// Color Dialog\r\n
DlgColorTitle\t\t: "Vel lit",\r\n
DlgColorBtnClear\t: "Strika alt",\r\n
DlgColorHighlight\t: "Framhevja",\r\n
DlgColorSelected\t: "Valt",\r\n
\r\n
// Smiley Dialog\r\n
DlgSmileyTitle\t\t: "Vel Smiley",\r\n
\r\n
// Special Character Dialog\r\n
DlgSpecialCharTitle\t: "Vel sertekn",\r\n
\r\n
// Table Dialog\r\n
DlgTableTitle\t\t: "Eginleikar fyri tabell",\r\n
DlgTableRows\t\t: "Røðir",\r\n
DlgTableColumns\t\t: "Kolonnur",\r\n
DlgTableBorder\t\t: "Bordabreidd",\r\n
DlgTableAlign\t\t: "Justering",\r\n
DlgTableAlignNotSet\t: "<Einki valt>",\r\n
DlgTableAlignLeft\t: "Vinstrasett",\r\n
DlgTableAlignCenter\t: "Miðsett",\r\n
DlgTableAlignRight\t: "Høgrasett",\r\n
DlgTableWidth\t\t: "Breidd",\r\n
DlgTableWidthPx\t\t: "pixels",\r\n
DlgTableWidthPc\t\t: "prosent",\r\n
DlgTableHeight\t\t: "Hædd",\r\n
DlgTableCellSpace\t: "Fjarstøða millum meskar",\r\n
DlgTableCellPad\t\t: "Meskubreddi",\r\n
DlgTableCaption\t\t: "Tabellfrágreiðing",\r\n
DlgTableSummary\t\t: "Samandráttur",\r\n
DlgTableHeaders\t\t: "Headers",\t//MISSING\r\n
DlgTableHeadersNone\t\t: "None",\t//MISSING\r\n
DlgTableHeadersColumn\t: "First column",\t//MISSING\r\n
DlgTableHeadersRow\t\t: "First Row",\t//MISSING\r\n
DlgTableHeadersBoth\t\t: "Both",\t//MISSING\r\n
\r\n
// Table Cell Dialog\r\n
DlgCellTitle\t\t: "Mesku eginleikar",\r\n
DlgCellWidth\t\t: "Breidd",\r\n
DlgCellWidthPx\t\t: "pixels",\r\n
DlgCellWidthPc\t\t: "prosent",\r\n
DlgCellHeight\t\t: "Hædd",\r\n
DlgCellWordWrap\t\t: "Orðkloyving",\r\n
DlgCellWordWrapNotSet\t: "<Einki valt>",\r\n
DlgCellWordWrapYes\t: "Ja",\r\n
DlgCellWordWrapNo\t: "Nei",\r\n
DlgCellHorAlign\t\t: "Vatnrøtt justering",\r\n
DlgCellHorAlignNotSet\t: "<Einki valt>",\r\n
DlgCellHorAlignLeft\t: "Vinstrasett",\r\n
DlgCellHorAlignCenter\t: "Miðsett",\r\n
DlgCellHorAlignRight: "Høgrasett",\r\n
DlgCellVerAlign\t\t: "Lodrøtt justering",\r\n
DlgCellVerAlignNotSet\t: "<Ikki sett>",\r\n
DlgCellVerAlignTop\t: "Ovast",\r\n
DlgCellVerAlignMiddle\t: "Miðjan",\r\n
DlgCellVerAlignBottom\t: "Niðast",\r\n
DlgCellVerAlignBaseline\t: "Basislinja",\r\n
DlgCellType\t\t: "Cell Type",\t//MISSING\r\n
DlgCellTypeData\t\t: "Data",\t//MISSING\r\n
DlgCellTypeHeader\t: "Header",\t//MISSING\r\n
DlgCellRowSpan\t\t: "Røðir, meskin fevnir um",\r\n
DlgCellCollSpan\t\t: "Kolonnur, meskin fevnir um",\r\n
DlgCellBackColor\t: "Bakgrundslitur",\r\n
DlgCellBorderColor\t: "Litur á borda",\r\n
DlgCellBtnSelect\t: "Vel...",\r\n
\r\n
// Find and Replace Dialog\r\n
DlgFindAndReplaceTitle\t: "Finn og broyt",\r\n
\r\n
// Find Dialog\r\n
DlgFindTitle\t\t: "Finn",\r\n
DlgFindFindBtn\t\t: "Finn",\r\n
DlgFindNotFoundMsg\t: "Leititeksturin varð ikki funnin",\r\n
\r\n
// Replace Dialog\r\n
DlgReplaceTitle\t\t\t: "Yvirskriva",\r\n
DlgReplaceFindLbl\t\t: "Finn:",\r\n
DlgReplaceReplaceLbl\t: "Yvirskriva við:",\r\n
DlgReplaceCaseChk\t\t: "Munur á stórum og smáðum bókstavum",\r\n
DlgReplaceReplaceBtn\t: "Yvirskriva",\r\n
DlgReplaceReplAllBtn\t: "Yvirskriva alt",\r\n
DlgReplaceWordChk\t\t: "Bert heil orð",\r\n
\r\n
// Paste Operations / Dialog\r\n
PasteErrorCut\t: "Trygdaruppseting alnótskagans forðar tekstviðgeranum í at kvetta tekstin. Vinarliga nýt knappaborðið til at kvetta tekstin (CTRL+X).",\r\n
PasteErrorCopy\t: "Trygdaruppseting alnótskagans forðar tekstviðgeranum í at avrita tekstin. Vinarliga nýt knappaborðið til at avrita tekstin (CTRL+C).",\r\n
\r\n
PasteAsText\t\t: "Innrita som reinan tekst",\r\n
PasteFromWord\t: "Innrita fra Word",\r\n
\r\n
DlgPasteMsg2\t: "Vinarliga koyr tekstin í hendan rútin við knappaborðinum (<strong>CTRL+V</strong>) og klikk á <strong>Góðtak</strong>.",\r\n
DlgPasteSec\t\t: "Trygdaruppseting alnótskagans forðar tekstviðgeranum í beinleiðis atgongd til avritingarminnið. Tygum mugu royna aftur í hesum rútinum.",\r\n
DlgPasteIgnoreFont\t\t: "Forfjóna Font definitiónirnar",\r\n
DlgPasteRemoveStyles\t: "Strika typografi definitiónir",\r\n
\r\n
// Color Picker\r\n
ColorAutomatic\t: "Automatiskt",\r\n
ColorMoreColors\t: "Fleiri litir...",\r\n
\r\n
// Document Properties\r\n
DocProps\t\t: "Eginleikar fyri dokument",\r\n
\r\n
// Anchor Dialog\r\n
DlgAnchorTitle\t\t: "Eginleikar fyri marknastein",\r\n
DlgAnchorName\t\t: "Heiti marknasteinsins",\r\n
DlgAnchorErrorName\t: "Vinarliga rita marknasteinsins heiti",\r\n
\r\n
// Speller Pages Dialog\r\n
DlgSpellNotInDic\t\t: "Finst ikki í orðabókini",\r\n
DlgSpellChangeTo\t\t: "Broyt til",\r\n
DlgSpellBtnIgnore\t\t: "Forfjóna",\r\n
DlgSpellBtnIgnoreAll\t: "Forfjóna alt",\r\n
DlgSpellBtnReplace\t\t: "Yvirskriva",\r\n
DlgSpellBtnReplaceAll\t: "Yvirskriva alt",\r\n
DlgSpellBtnUndo\t\t\t: "Angra",\r\n
DlgSpellNoSuggestions\t: "- Einki uppskot -",\r\n
DlgSpellProgress\t\t: "Rættstavarin arbeiðir...",\r\n
DlgSpellNoMispell\t\t: "Rættstavarain liðugur: Eingin feilur funnin",\r\n
DlgSpellNoChanges\t\t: "Rættstavarain liðugur: Einki orð varð broytt",\r\n
DlgSpellOneChange\t\t: "Rættstavarain liðugur: Eitt orð er broytt",\r\n
DlgSpellManyChanges\t\t: "Rættstavarain liðugur: %1 orð broytt",\r\n
\r\n
IeSpellDownload\t\t\t: "Rættstavarin er ikki tøkur í tekstviðgeranum. Vilt tú heinta hann nú?",\r\n
\r\n
// Button Dialog\r\n
DlgButtonText\t\t: "Tekstur",\r\n
DlgButtonType\t\t: "Slag",\r\n
DlgButtonTypeBtn\t: "Knøttur",\r\n
DlgButtonTypeSbm\t: "Send",\r\n
DlgButtonTypeRst\t: "Nullstilla",\r\n
\r\n
// Checkbox and Radio Button Dialogs\r\n
DlgCheckboxName\t\t: "Navn",\r\n
DlgCheckboxValue\t: "Virði",\r\n
DlgCheckboxSelected\t: "Valt",\r\n
\r\n
// Form Dialog\r\n
DlgFormName\t\t: "Navn",\r\n
DlgFormAction\t: "Hending",\r\n
DlgFormMethod\t: "Háttur",\r\n
\r\n
// Select Field Dialog\r\n
DlgSelectName\t\t: "Navn",\r\n
DlgSelectValue\t\t: "Virði",\r\n
DlgSelectSize\t\t: "Stødd",\r\n
DlgSelectLines\t\t: "Linjur",\r\n
DlgSelectChkMulti\t: "Loyv fleiri valmøguleikum samstundis",\r\n
DlgSelectOpAvail\t: "Tøkir møguleikar",\r\n
DlgSelectOpText\t\t: "Tekstur",\r\n
DlgSelectOpValue\t: "Virði",\r\n
DlgSelectBtnAdd\t\t: "Legg afturat",\r\n
DlgSelectBtnModify\t: "Broyt",\r\n
DlgSelectBtnUp\t\t: "Upp",\r\n
DlgSelectBtnDown\t: "Niður",\r\n
DlgSelectBtnSetValue : "Set sum valt virði",\r\n
DlgSelectBtnDelete\t: "Strika",\r\n
\r\n
// Textarea Dialog\r\n
DlgTextareaName\t: "Navn",\r\n
DlgTextareaCols\t: "kolonnur",\r\n
DlgTextareaRows\t: "røðir",\r\n
\r\n
// Text Field Dialog\r\n
DlgTextName\t\t\t: "Navn",\r\n
DlgTextValue\t\t: "Virði",\r\n
DlgTextCharWidth\t: "Breidd (sjónlig tekn)",\r\n
DlgTextMaxChars\t\t: "Mest loyvdu tekn",\r\n
DlgTextType\t\t\t: "Slag",\r\n
DlgTextTypeText\t\t: "Tekstur",\r\n
DlgTextTypePass\t\t: "Loyniorð",\r\n
\r\n
// Hidden Field Dialog\r\n
DlgHiddenName\t: "Navn",\r\n
DlgHiddenValue\t: "Virði",\r\n
\r\n
// Bulleted List Dialog\r\n
BulletedListProp\t: "Eginleikar fyri punktmerktan lista",\r\n
NumberedListProp\t: "Eginleikar fyri talmerktan lista",\r\n
DlgLstStart\t\t\t: "Byrjan",\r\n
DlgLstType\t\t\t: "Slag",\r\n
DlgLstTypeCircle\t: "Sirkul",\r\n
DlgLstTypeDisc\t\t: "Fyltur sirkul",\r\n
DlgLstTypeSquare\t: "Fjórhyrningur",\r\n
DlgLstTypeNumbers\t: "Talmerkt (1, 2, 3)",\r\n
DlgLstTypeLCase\t\t: "Smáir bókstavir (a, b, c)",\r\n
DlgLstTypeUCase\t\t: "Stórir bókstavir (A, B, C)",\r\n
DlgLstTypeSRoman\t: "Smá rómaratøl (i, ii, iii)",\r\n
DlgLstTypeLRoman\t: "Stór rómaratøl (I, II, III)",\r\n
\r\n
// Document Properties Dialog\r\n
DlgDocGeneralTab\t: "Generelt",\r\n
DlgDocBackTab\t\t: "Bakgrund",\r\n
DlgDocColorsTab\t\t: "Litir og breddar",\r\n
DlgDocMetaTab\t\t: "META-upplýsingar",\r\n
\r\n
DlgDocPageTitle\t\t: "Síðuheiti",\r\n
DlgDocLangDir\t\t: "Tekstkós",\r\n
DlgDocLangDirLTR\t: "Frá vinstru móti høgru (LTR)",\r\n
DlgDocLangDirRTL\t: "Frá høgru móti vinstru (RTL)",\r\n
DlgDocLangCode\t\t: "Málkoda",\r\n
DlgDocCharSet\t\t: "Teknsett koda",\r\n
DlgDocCharSetCE\t\t: "Miðeuropa",\r\n
DlgDocCharSetCT\t\t: "Kinesiskt traditionelt (Big5)",\r\n
DlgDocCharSetCR\t\t: "Cyrilliskt",\r\n
DlgDocCharSetGR\t\t: "Grikst",\r\n
DlgDocCharSetJP\t\t: "Japanskt",\r\n
DlgDocCharSetKR\t\t: "Koreanskt",\r\n
DlgDocCharSetTR\t\t: "Turkiskt",\r\n
DlgDocCharSetUN\t\t: "UNICODE (UTF-8)",\r\n
DlgDocCharSetWE\t\t: "Vestureuropa",\r\n
DlgDocCharSetOther\t: "Onnur teknsett koda",\r\n
\r\n
DlgDocDocType\t\t: "Dokumentslag yvirskrift",\r\n
DlgDocDocTypeOther\t: "Annað dokumentslag yvirskrift",\r\n
DlgDocIncXHTML\t\t: "Viðfest XHTML deklaratiónir",\r\n
DlgDocBgColor\t\t: "Bakgrundslitur",\r\n
DlgDocBgImage\t\t: "Leið til bakgrundsmynd (URL)",\r\n
DlgDocBgNoScroll\t: "Læst bakgrund (rullar ikki)",\r\n
DlgDocCText\t\t\t: "Tekstur",\r\n
DlgDocCLink\t\t\t: "Tilknýti",\r\n
DlgDocCVisited\t\t: "Vitjaði tilknýti",\r\n
DlgDocCActive\t\t: "Virkin tilknýti",\r\n
DlgDocMargins\t\t: "Síðubreddar",\r\n
DlgDocMaTop\t\t\t: "Ovast",\r\n
DlgDocMaLeft\t\t: "Vinstra",\r\n
DlgDocMaRight\t\t: "Høgra",\r\n
DlgDocMaBottom\t\t: "Niðast",\r\n
DlgDocMeIndex\t\t: "Dokument index lyklaorð (sundurbýtt við komma)",\r\n
DlgDocMeDescr\t\t: "Dokumentlýsing",\r\n
DlgDocMeAuthor\t\t: "Høvundur",\r\n
DlgDocMeCopy\t\t: "Upphavsrættindi",\r\n
DlgDocPreview\t\t: "Frumsýning",\r\n
\r\n
// Templates Dialog\r\n
Templates\t\t\t: "Skabelónir",\r\n
DlgTemplatesTitle\t: "Innihaldsskabelónir",\r\n
DlgTemplatesSelMsg\t: "Vinarliga vel ta skabelón, ið skal opnast í tekstviðgeranum<br>(Hetta yvirskrivar núverandi innihald):",\r\n
DlgTemplatesLoading\t: "Heinti yvirlit yvir skabelónir. Vinarliga bíða við...",\r\n
DlgTemplatesNoTpl\t: "(Ongar skabelónir tøkar)",\r\n
DlgTemplatesReplace\t: "Yvirskriva núverandi innihald",\r\n
\r\n
// About Dialog\r\n
DlgAboutAboutTab\t: "Um",\r\n
DlgAboutBrowserInfoTab\t: "Upplýsingar um alnótskagan",\r\n
DlgAboutLicenseTab\t: "License",\r\n
DlgAboutVersion\t\t: "version",\r\n
DlgAboutInfo\t\t: "Fyri fleiri upplýsingar, far til",\r\n
\r\n
// Div Dialog\r\n
DlgDivGeneralTab\t: "Generelt",\r\n
DlgDivAdvancedTab\t: "Fjølbroytt",\r\n
DlgDivStyle\t\t: "Typografi",\r\n
DlgDivInlineStyle\t: "Inline typografi",\r\n
\r\n
ScaytTitle\t\t\t: "SCAYT",\t//MISSING\r\n
ScaytTitleOptions\t: "Options",\t//MISSING\r\n
ScaytTitleLangs\t\t: "Languages",\t//MISSING\r\n
ScaytTitleAbout\t\t: "About"\t//MISSING\r\n
};\r\n


]]></string> </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>19293</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
