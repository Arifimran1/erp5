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
            <value> <string>ts83858910.14</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>is.js</string> </value>
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
 * Icelandic language file.\r\n
 */\r\n
\r\n
var FCKLang =\r\n
{\r\n
// Language direction : "ltr" (left to right) or "rtl" (right to left).\r\n
Dir\t\t\t\t\t: "ltr",\r\n
\r\n
ToolbarCollapse\t\t: "Fela verkstiku",\r\n
ToolbarExpand\t\t: "Sýna verkstiku",\r\n
\r\n
// Toolbar Items and Context Menu\r\n
Save\t\t\t\t: "Vista",\r\n
NewPage\t\t\t\t: "Ný síða",\r\n
Preview\t\t\t\t: "Forskoða",\r\n
Cut\t\t\t\t\t: "Klippa",\r\n
Copy\t\t\t\t: "Afrita",\r\n
Paste\t\t\t\t: "Líma",\r\n
PasteText\t\t\t: "Líma ósniðinn texta",\r\n
PasteWord\t\t\t: "Líma úr Word",\r\n
Print\t\t\t\t: "Prenta",\r\n
SelectAll\t\t\t: "Velja allt",\r\n
RemoveFormat\t\t: "Fjarlægja snið",\r\n
InsertLinkLbl\t\t: "Stikla",\r\n
InsertLink\t\t\t: "Stofna/breyta stiklu",\r\n
RemoveLink\t\t\t: "Fjarlægja stiklu",\r\n
VisitLink\t\t\t: "Opna stiklusíðu",\r\n
Anchor\t\t\t\t: "Stofna/breyta kaflamerki",\r\n
AnchorDelete\t\t: "Eyða kaflamerki",\r\n
InsertImageLbl\t\t: "Setja inn mynd",\r\n
InsertImage\t\t\t: "Setja inn/breyta mynd",\r\n
InsertFlashLbl\t\t: "Flash",\r\n
InsertFlash\t\t\t: "Setja inn/breyta Flash",\r\n
InsertTableLbl\t\t: "Tafla",\r\n
InsertTable\t\t\t: "Setja inn/breyta töflu",\r\n
InsertLineLbl\t\t: "Lína",\r\n
InsertLine\t\t\t: "Lóðrétt lína",\r\n
InsertSpecialCharLbl: "Merki",\r\n
InsertSpecialChar\t: "Setja inn merki",\r\n
InsertSmileyLbl\t\t: "Svipur",\r\n
InsertSmiley\t\t: "Setja upp svip",\r\n
About\t\t\t\t: "Um FCKeditor",\r\n
Bold\t\t\t\t: "Feitletrað",\r\n
Italic\t\t\t\t: "Skáletrað",\r\n
Underline\t\t\t: "Undirstrikað",\r\n
StrikeThrough\t\t: "Yfirstrikað",\r\n
Subscript\t\t\t: "Niðurskrifað",\r\n
Superscript\t\t\t: "Uppskrifað",\r\n
LeftJustify\t\t\t: "Vinstrijöfnun",\r\n
CenterJustify\t\t: "Miðja texta",\r\n
RightJustify\t\t: "Hægrijöfnun",\r\n
BlockJustify\t\t: "Jafna báðum megin",\r\n
DecreaseIndent\t\t: "Auka inndrátt",\r\n
IncreaseIndent\t\t: "Minnka inndrátt",\r\n
Blockquote\t\t\t: "Inndráttur",\r\n
CreateDiv\t\t\t: "Búa til DIV-hýsil",\r\n
EditDiv\t\t\t\t: "Breyta DIV-hýsli",\r\n
DeleteDiv\t\t\t: "Eyða DIV-hýsli",\r\n
Undo\t\t\t\t: "Afturkalla",\r\n
Redo\t\t\t\t: "Hætta við afturköllun",\r\n
NumberedListLbl\t\t: "Númeraður listi",\r\n
NumberedList\t\t: "Setja inn/fella númeraðan lista",\r\n
BulletedListLbl\t\t: "Punktalisti",\r\n
BulletedList\t\t: "Setja inn/fella punktalista",\r\n
ShowTableBorders\t: "Sýna töflugrind",\r\n
ShowDetails\t\t\t: "Sýna smáatriði",\r\n
Style\t\t\t\t: "Stílflokkur",\r\n
FontFormat\t\t\t: "Stílsnið",\r\n
Font\t\t\t\t: "Leturgerð ",\r\n
FontSize\t\t\t: "Leturstærð ",\r\n
TextColor\t\t\t: "Litur texta",\r\n
BGColor\t\t\t\t: "Bakgrunnslitur",\r\n
Source\t\t\t\t: "Kóði",\r\n
Find\t\t\t\t: "Leita",\r\n
Replace\t\t\t\t: "Skipta út",\r\n
SpellCheck\t\t\t: "Villuleit",\r\n
UniversalKeyboard\t: "Hnattrænt lyklaborð",\r\n
PageBreakLbl\t\t: "Síðuskil",\r\n
PageBreak\t\t\t: "Setja inn síðuskil",\r\n
\r\n
Form\t\t\t: "Setja inn innsláttarform",\r\n
Checkbox\t\t: "Setja inn hökunarreit",\r\n
RadioButton\t\t: "Setja inn valhnapp",\r\n
TextField\t\t: "Setja inn textareit",\r\n
Textarea\t\t: "Setja inn textasvæði",\r\n
HiddenField\t\t: "Setja inn falið svæði",\r\n
Button\t\t\t: "Setja inn hnapp",\r\n
SelectionField\t: "Setja inn lista",\r\n
ImageButton\t\t: "Setja inn myndahnapp",\r\n
\r\n
FitWindow\t\t: "Skoða ritil í fullri stærð",\r\n
ShowBlocks\t\t: "Sýna blokkir",\r\n
\r\n
// Context Menu\r\n
EditLink\t\t\t: "Breyta stiklu",\r\n
CellCM\t\t\t\t: "Reitur",\r\n
RowCM\t\t\t\t: "Röð",\r\n
ColumnCM\t\t\t: "Dálkur",\r\n
InsertRowAfter\t\t: "Skjóta inn röð fyrir neðan",\r\n
InsertRowBefore\t\t: "Skjóta inn röð fyrir ofan",\r\n
DeleteRows\t\t\t: "Eyða röð",\r\n
InsertColumnAfter\t: "Skjóta inn dálki hægra megin",\r\n
InsertColumnBefore\t: "Skjóta inn dálki vinstra megin",\r\n
DeleteColumns\t\t: "Fella dálk",\r\n
InsertCellAfter\t\t: "Skjóta inn reiti fyrir framan",\r\n
InsertCellBefore\t: "Skjóta inn reiti fyrir aftan",\r\n
DeleteCells\t\t\t: "Fella reit",\r\n
MergeCells\t\t\t: "Sameina reiti",\r\n
MergeRight\t\t\t: "Sameina til hægri",\r\n
MergeDown\t\t\t: "Sameina niður á við",\r\n
HorizontalSplitCell\t: "Kljúfa reit lárétt",\r\n
VerticalSplitCell\t: "Kljúfa reit lóðrétt",\r\n
TableDelete\t\t\t: "Fella töflu",\r\n
CellProperties\t\t: "Eigindi reits",\r\n
TableProperties\t\t: "Eigindi töflu",\r\n
ImageProperties\t\t: "Eigindi myndar",\r\n
FlashProperties\t\t: "Eigindi Flash",\r\n
\r\n
AnchorProp\t\t\t: "Eigindi kaflamerkis",\r\n
ButtonProp\t\t\t: "Eigindi hnapps",\r\n
CheckboxProp\t\t: "Eigindi markreits",\r\n
HiddenFieldProp\t\t: "Eigindi falins svæðis",\r\n
RadioButtonProp\t\t: "Eigindi valhnapps",\r\n
ImageButtonProp\t\t: "Eigindi myndahnapps",\r\n
TextFieldProp\t\t: "Eigindi textareits",\r\n
SelectionFieldProp\t: "Eigindi lista",\r\n
TextareaProp\t\t: "Eigindi textasvæðis",\r\n
FormProp\t\t\t: "Eigindi innsláttarforms",\r\n
\r\n
FontFormats\t\t\t: "Venjulegt letur;Forsniðið;Vistfang;Fyrirsögn 1;Fyrirsögn 2;Fyrirsögn 3;Fyrirsögn 4;Fyrirsögn 5;Fyrirsögn 6;Venjulegt (DIV)",\r\n
\r\n
// Alerts and Messages\r\n
ProcessingXHTML\t\t: "Meðhöndla XHTML...",\r\n
Done\t\t\t\t: "Tilbúið",\r\n
PasteWordConfirm\t: "Textinn sem þú ætlar að líma virðist koma úr Word. Viltu hreinsa óþarfar Word-skipanir úr honum?",\r\n
NotCompatiblePaste\t: "Þessi aðgerð er bundin við Internet Explorer 5.5 og nýrri. Viltu líma textann án þess að hreinsa hann?",\r\n
UnknownToolbarItem\t: "Óþekktur hlutur í verkstiku \\"%1\\"!",\r\n
UnknownCommand\t\t: "Óþekkt skipanaheiti \\"%1\\"!",\r\n
NotImplemented\t\t: "Skipun ekki virkjuð!",\r\n
UnknownToolbarSet\t: "Verkstikan \\"%1\\" ekki til!",\r\n
NoActiveX\t\t\t: "Öryggisstillingarnar í vafranum þínum leyfa ekki alla möguleika ritilsins.<br>Láttu vafrann leyfa Active-X og viðbætur til að komast hjá villum og takmörkunum.",\r\n
BrowseServerBlocked : "Ritillinn getur ekki opnað nauðsynlega hjálparglugga!<br>Láttu hann leyfa þessari síðu að opna sprettiglugga.",\r\n
DialogBlocked\t\t: "Ekki var hægt að opna skipanaglugga!<br>Nauðsynlegt er að leyfa síðunni að opna sprettiglugga.",\r\n
VisitLinkBlocked\t: "Ekki var hægt að opna nýjan glugga. Gangtu úr skugga um að engir sprettigluggabanar séu virkir.",\r\n
\r\n
// Dialogs\r\n
DlgBtnOK\t\t\t: "Í lagi",\r\n
DlgBtnCancel\t\t: "Hætta við",\r\n
DlgBtnClose\t\t\t: "Loka",\r\n
DlgBtnBrowseServer\t: "Fletta í skjalasafni",\r\n
DlgAdvancedTag\t\t: "Tæknilegt",\r\n
DlgOpOther\t\t\t: "<Annað>",\r\n
DlgInfoTab\t\t\t: "Upplýsingar",\r\n
DlgAlertUrl\t\t\t: "Sláðu inn slóð",\r\n
\r\n
// General Dialogs Labels\r\n
DlgGenNotSet\t\t: "<ekkert valið>",\r\n
DlgGenId\t\t\t: "Auðkenni",\r\n
DlgGenLangDir\t\t: "Lesstefna",\r\n
DlgGenLangDirLtr\t: "Frá vinstri til hægri (LTR)",\r\n
DlgGenLangDirRtl\t: "Frá hægri til vinstri (RTL)",\r\n
DlgGenLangCode\t\t: "Tungumálakóði",\r\n
DlgGenAccessKey\t\t: "Skammvalshnappur",\r\n
DlgGenName\t\t\t: "Nafn",\r\n
DlgGenTabIndex\t\t: "Raðnúmer innsláttarreits",\r\n
DlgGenLongDescr\t\t: "Nánari lýsing",\r\n
DlgGenClass\t\t\t: "Stílsniðsflokkur",\r\n
DlgGenTitle\t\t\t: "Titill",\r\n
DlgGenContType\t\t: "Tegund innihalds",\r\n
DlgGenLinkCharset\t: "Táknróf",\r\n
DlgGenStyle\t\t\t: "Stíll",\r\n
\r\n
// Image Dialog\r\n
DlgImgTitle\t\t\t: "Eigindi myndar",\r\n
DlgImgInfoTab\t\t: "Almennt",\r\n
DlgImgBtnUpload\t\t: "Hlaða upp",\r\n
DlgImgURL\t\t\t: "Vefslóð",\r\n
DlgImgUpload\t\t: "Hlaða upp",\r\n
DlgImgAlt\t\t\t: "Baklægur texti",\r\n
DlgImgWidth\t\t\t: "Breidd",\r\n
DlgImgHeight\t\t: "Hæð",\r\n
DlgImgLockRatio\t\t: "Festa stærðarhlutfall",\r\n
DlgBtnResetSize\t\t: "Reikna stærð",\r\n
DlgImgBorder\t\t: "Rammi",\r\n
DlgImgHSpace\t\t: "Vinstri bil",\r\n
DlgImgVSpace\t\t: "Hægri bil",\r\n
DlgImgAlign\t\t\t: "Jöfnun",\r\n
DlgImgAlignLeft\t\t: "Vinstri",\r\n
DlgImgAlignAbsBottom: "Abs neðst",\r\n
DlgImgAlignAbsMiddle: "Abs miðjuð",\r\n
DlgImgAlignBaseline\t: "Grunnlína",\r\n
DlgImgAlignBottom\t: "Neðst",\r\n
DlgImgAlignMiddle\t: "Miðjuð",\r\n
DlgImgAlignRight\t: "Hægri",\r\n
DlgImgAlignTextTop\t: "Efri brún texta",\r\n
DlgImgAlignTop\t\t: "Efst",\r\n
DlgImgPreview\t\t: "Sýna dæmi",\r\n
DlgImgAlertUrl\t\t: "Sláðu inn slóðina að myndinni",\r\n
DlgImgLinkTab\t\t: "Stikla",\r\n
\r\n
// Flash Dialog\r\n
DlgFlashTitle\t\t: "Eigindi Flash",\r\n
DlgFlashChkPlay\t\t: "Sjálfvirk spilun",\r\n
DlgFlashChkLoop\t\t: "Endurtekning",\r\n
DlgFlashChkMenu\t\t: "Sýna Flash-valmynd",\r\n
DlgFlashScale\t\t: "Skali",\r\n
DlgFlashScaleAll\t: "Sýna allt",\r\n
DlgFlashScaleNoBorder\t: "Án ramma",\r\n
DlgFlashScaleFit\t: "Fella skala að stærð",\r\n
\r\n
// Link Dialog\r\n
DlgLnkWindowTitle\t: "Stikla",\r\n
DlgLnkInfoTab\t\t: "Almennt",\r\n
DlgLnkTargetTab\t\t: "Mark",\r\n
\r\n
DlgLnkType\t\t\t: "Stikluflokkur",\r\n
DlgLnkTypeURL\t\t: "Vefslóð",\r\n
DlgLnkTypeAnchor\t: "Bókamerki á þessari síðu",\r\n
DlgLnkTypeEMail\t\t: "Netfang",\r\n
DlgLnkProto\t\t\t: "Samskiptastaðall",\r\n
DlgLnkProtoOther\t: "<annað>",\r\n
DlgLnkURL\t\t\t: "Vefslóð",\r\n
DlgLnkAnchorSel\t\t: "Veldu akkeri",\r\n
DlgLnkAnchorByName\t: "Eftir akkerisnafni",\r\n
DlgLnkAnchorById\t: "Eftir auðkenni einingar",\r\n
DlgLnkNoAnchors\t\t: "<Engin bókamerki á skrá>",\r\n
DlgLnkEMail\t\t\t: "Netfang",\r\n
DlgLnkEMailSubject\t: "Efni",\r\n
DlgLnkEMailBody\t\t: "Meginmál",\r\n
DlgLnkUpload\t\t: "Senda upp",\r\n
DlgLnkBtnUpload\t\t: "Senda upp",\r\n
\r\n
DlgLnkTarget\t\t: "Mark",\r\n
DlgLnkTargetFrame\t: "<rammi>",\r\n
DlgLnkTargetPopup\t: "<sprettigluggi>",\r\n
DlgLnkTargetBlank\t: "Nýr gluggi (_blank)",\r\n
DlgLnkTargetParent\t: "Yfirsettur rammi (_parent)",\r\n
DlgLnkTargetSelf\t: "Sami gluggi (_self)",\r\n
DlgLnkTargetTop\t\t: "Allur glugginn (_top)",\r\n
DlgLnkTargetFrameName\t: "Nafn markglugga",\r\n
DlgLnkPopWinName\t: "Nafn sprettiglugga",\r\n
DlgLnkPopWinFeat\t: "Eigindi sprettiglugga",\r\n
DlgLnkPopResize\t\t: "Skölun",\r\n
DlgLnkPopLocation\t: "Fanglína",\r\n
DlgLnkPopMenu\t\t: "Vallína",\r\n
DlgLnkPopScroll\t\t: "Skrunstikur",\r\n
DlgLnkPopStatus\t\t: "Stöðustika",\r\n
DlgLnkPopToolbar\t: "Verkfærastika",\r\n
DlgLnkPopFullScrn\t: "Heilskjár (IE)",\r\n
DlgLnkPopDependent\t: "Háð venslum (Netscape)",\r\n
DlgLnkPopWidth\t\t: "Breidd",\r\n
DlgLnkPopHeight\t\t: "Hæð",\r\n
DlgLnkPopLeft\t\t: "Fjarlægð frá vinstri",\r\n
DlgLnkPopTop\t\t: "Fjarlægð frá efri brún",\r\n
\r\n
DlnLnkMsgNoUrl\t\t: "Sláðu inn veffang stiklunnar!",\r\n
DlnLnkMsgNoEMail\t: "Sláðu inn netfang!",\r\n
DlnLnkMsgNoAnchor\t: "Veldu fyrst eitthvert bókamerki!",\r\n
DlnLnkMsgInvPopName\t: "Sprettisíðan verður að byrja á bókstaf (a-z) og má ekki innihalda stafabil",\r\n
\r\n
// Color Dialog\r\n
DlgColorTitle\t\t: "Velja lit",\r\n
DlgColorBtnClear\t: "Núllstilla",\r\n
DlgColorHighlight\t: "Litmerkja",\r\n
DlgColorSelected\t: "Valið",\r\n
\r\n
// Smiley Dialog\r\n
DlgSmileyTitle\t\t: "Velja svip",\r\n
\r\n
// Special Character Dialog\r\n
DlgSpecialCharTitle\t: "Velja tákn",\r\n
\r\n
// Table Dialog\r\n
DlgTableTitle\t\t: "Eigindi töflu",\r\n
DlgTableRows\t\t: "Raðir",\r\n
DlgTableColumns\t\t: "Dálkar",\r\n
DlgTableBorder\t\t: "Breidd ramma",\r\n
DlgTableAlign\t\t: "Jöfnun",\r\n
DlgTableAlignNotSet\t: "<ekkert valið>",\r\n
DlgTableAlignLeft\t: "Vinstrijafnað",\r\n
DlgTableAlignCenter\t: "Miðjað",\r\n
DlgTableAlignRight\t: "Hægrijafnað",\r\n
DlgTableWidth\t\t: "Breidd",\r\n
DlgTableWidthPx\t\t: "myndeindir",\r\n
DlgTableWidthPc\t\t: "prósent",\r\n
DlgTableHeight\t\t: "Hæð",\r\n
DlgTableCellSpace\t: "Bil milli reita",\r\n
DlgTableCellPad\t\t: "Reitaspássía",\r\n
DlgTableCaption\t\t: "Titill",\r\n
DlgTableSummary\t\t: "Áfram",\r\n
DlgTableHeaders\t\t: "Fyrirsagnir",\r\n
DlgTableHeadersNone\t\t: "Engar",\r\n
DlgTableHeadersColumn\t: "Fyrsti dálkur",\r\n
DlgTableHeadersRow\t\t: "Fyrsta röð",\r\n
DlgTableHeadersBoth\t\t: "Hvort tveggja",\r\n
\r\n
// Table Cell Dialog\r\n
DlgCellTitle\t\t: "Eigindi reits",\r\n
DlgCellWidth\t\t: "Breidd",\r\n
DlgCellWidthPx\t\t: "myndeindir",\r\n
DlgCellWidthPc\t\t: "prósent",\r\n
DlgCellHeight\t\t: "Hæð",\r\n
DlgCellWordWrap\t\t: "Línuskipting",\r\n
DlgCellWordWrapNotSet\t: "<ekkert valið>",\r\n
DlgCellWordWrapYes\t: "Já",\r\n
DlgCellWordWrapNo\t: "Nei",\r\n
DlgCellHorAlign\t\t: "Lárétt jöfnun",\r\n
DlgCellHorAlignNotSet\t: "<ekkert valið>",\r\n
DlgCellHorAlignLeft\t: "Vinstrijafnað",\r\n
DlgCellHorAlignCenter\t: "Miðjað",\r\n
DlgCellHorAlignRight: "Hægrijafnað",\r\n
DlgCellVerAlign\t\t: "Lóðrétt jöfnun",\r\n
DlgCellVerAlignNotSet\t: "<ekkert valið>",\r\n
DlgCellVerAlignTop\t: "Efst",\r\n
DlgCellVerAlignMiddle\t: "Miðjað",\r\n
DlgCellVerAlignBottom\t: "Neðst",\r\n
DlgCellVerAlignBaseline\t: "Grunnlína",\r\n
DlgCellType\t\t: "Tegund reits",\r\n
DlgCellTypeData\t\t: "Gögn",\r\n
DlgCellTypeHeader\t: "Fyrirsögn",\r\n
DlgCellRowSpan\t\t: "Hæð í röðum talið",\r\n
DlgCellCollSpan\t\t: "Breidd í dálkum talið",\r\n
DlgCellBackColor\t: "Bakgrunnslitur",\r\n
DlgCellBorderColor\t: "Rammalitur",\r\n
DlgCellBtnSelect\t: "Veldu...",\r\n
\r\n
// Find and Replace Dialog\r\n
DlgFindAndReplaceTitle\t: "Finna og skipta",\r\n
\r\n
// Find Dialog\r\n
DlgFindTitle\t\t: "Finna",\r\n
DlgFindFindBtn\t\t: "Finna",\r\n
DlgFindNotFoundMsg\t: "Leitartexti fannst ekki!",\r\n
\r\n
// Replace Dialog\r\n
DlgReplaceTitle\t\t\t: "Skipta út",\r\n
DlgReplaceFindLbl\t\t: "Leita að:",\r\n
DlgReplaceReplaceLbl\t: "Skipta út fyrir:",\r\n
DlgReplaceCaseChk\t\t: "Gera greinarmun á¡ há¡- og lágstöfum",\r\n
DlgReplaceReplaceBtn\t: "Skipta út",\r\n
DlgReplaceReplAllBtn\t: "Skipta út allsstaðar",\r\n
DlgReplaceWordChk\t\t: "Aðeins heil orð",\r\n
\r\n
// Paste Operations / Dialog\r\n
PasteErrorCut\t: "Öryggisstillingar vafrans þíns leyfa ekki klippingu texta með músaraðgerð. Notaðu lyklaborðið í klippa (Ctrl+X).",\r\n
PasteErrorCopy\t: "Öryggisstillingar vafrans þíns leyfa ekki afritun texta með músaraðgerð. Notaðu lyklaborðið í afrita (Ctrl+C).",\r\n
\r\n
PasteAsText\t\t: "Líma sem ósniðinn texta",\r\n
PasteFromWord\t: "Líma úr Word",\r\n
\r\n
DlgPasteMsg2\t: "Límdu í svæðið hér að neðan og (<STRONG>Ctrl+V</STRONG>) og smelltu á <STRONG>OK</STRONG>.",\r\n
DlgPasteSec\t\t: "Vegna öryggisstillinga í vafranum þínum fær ritillinn ekki beinan aðgang að klippuborðinu. Þú verður að líma innihaldið aftur inn í þennan glugga.",\r\n
DlgPasteIgnoreFont\t\t: "Hunsa leturskilgreiningar",\r\n
DlgPasteRemoveStyles\t: "Hunsa letureigindi",\r\n
\r\n
// Color Picker\r\n
ColorAutomatic\t: "Sjálfval",\r\n
ColorMoreColors\t: "Fleiri liti...",\r\n
\r\n
// Document Properties\r\n
DocProps\t\t: "Eigindi skjals",\r\n
\r\n
// Anchor Dialog\r\n
DlgAnchorTitle\t\t: "Eigindi bókamerkis",\r\n
DlgAnchorName\t\t: "Nafn bókamerkis",\r\n
DlgAnchorErrorName\t: "Sláðu inn nafn bókamerkis!",\r\n
\r\n
// Speller Pages Dialog\r\n
DlgSpellNotInDic\t\t: "Ekki í orðabókinni",\r\n
DlgSpellChangeTo\t\t: "Tillaga",\r\n
DlgSpellBtnIgnore\t\t: "Hunsa",\r\n
DlgSpellBtnIgnoreAll\t: "Hunsa allt",\r\n
DlgSpellBtnReplace\t\t: "Skipta",\r\n
DlgSpellBtnReplaceAll\t: "Skipta öllu",\r\n
DlgSpellBtnUndo\t\t\t: "Til baka",\r\n
DlgSpellNoSuggestions\t: "- engar tillögur -",\r\n
DlgSpellProgress\t\t: "Villuleit í gangi...",\r\n
DlgSpellNoMispell\t\t: "Villuleit lokið: Engin villa fannst",\r\n
DlgSpellNoChanges\t\t: "Villuleit lokið: Engu orði breytt",\r\n
DlgSpellOneChange\t\t: "Villuleit lokið: Einu orði breytt",\r\n
DlgSpellManyChanges\t\t: "Villuleit lokið: %1 orðum breytt",\r\n
\r\n
IeSpellDownload\t\t\t: "Villuleit ekki sett upp.<br>Viltu setja hana upp?",\r\n
\r\n
// Button Dialog\r\n
DlgButtonText\t\t: "Texti",\r\n
DlgButtonType\t\t: "Gerð",\r\n
DlgButtonTypeBtn\t: "Hnappur",\r\n
DlgButtonTypeSbm\t: "Staðfesta",\r\n
DlgButtonTypeRst\t: "Hreinsa",\r\n
\r\n
// Checkbox and Radio Button Dialogs\r\n
DlgCheckboxName\t\t: "Nafn",\r\n
DlgCheckboxValue\t: "Gildi",\r\n
DlgCheckboxSelected\t: "Valið",\r\n
\r\n
// Form Dialog\r\n
DlgFormName\t\t: "Nafn",\r\n
DlgFormAction\t: "Aðgerð",\r\n
DlgFormMethod\t: "Aðferð",\r\n
\r\n
// Select Field Dialog\r\n
DlgSelectName\t\t: "Nafn",\r\n
DlgSelectValue\t\t: "Gildi",\r\n
DlgSelectSize\t\t: "Stærð",\r\n
DlgSelectLines\t\t: "línur",\r\n
DlgSelectChkMulti\t: "Leyfa fleiri kosti",\r\n
DlgSelectOpAvail\t: "Kostir",\r\n
DlgSelectOpText\t\t: "Texti",\r\n
DlgSelectOpValue\t: "Gildi",\r\n
DlgSelectBtnAdd\t\t: "Bæta við",\r\n
DlgSelectBtnModify\t: "Breyta",\r\n
DlgSelectBtnUp\t\t: "Upp",\r\n
DlgSelectBtnDown\t: "Niður",\r\n
DlgSelectBtnSetValue : "Merkja sem valið",\r\n
DlgSelectBtnDelete\t: "Eyða",\r\n
\r\n
// Textarea Dialog\r\n
DlgTextareaName\t: "Nafn",\r\n
DlgTextareaCols\t: "Dálkar",\r\n
DlgTextareaRows\t: "Línur",\r\n
\r\n
// Text Field Dialog\r\n
DlgTextName\t\t\t: "Nafn",\r\n
DlgTextValue\t\t: "Gildi",\r\n
DlgTextCharWidth\t: "Breidd (leturtákn)",\r\n
DlgTextMaxChars\t\t: "Hámarksfjöldi leturtákna",\r\n
DlgTextType\t\t\t: "Gerð",\r\n
DlgTextTypeText\t\t: "Texti",\r\n
DlgTextTypePass\t\t: "Lykilorð",\r\n
\r\n
// Hidden Field Dialog\r\n
DlgHiddenName\t: "Nafn",\r\n
DlgHiddenValue\t: "Gildi",\r\n
\r\n
// Bulleted List Dialog\r\n
BulletedListProp\t: "Eigindi depillista",\r\n
NumberedListProp\t: "Eigindi tölusetts lista",\r\n
DlgLstStart\t\t\t: "Byrja",\r\n
DlgLstType\t\t\t: "Gerð",\r\n
DlgLstTypeCircle\t: "Hringur",\r\n
DlgLstTypeDisc\t\t: "Fylltur hringur",\r\n
DlgLstTypeSquare\t: "Ferningur",\r\n
DlgLstTypeNumbers\t: "Tölusett (1, 2, 3)",\r\n
DlgLstTypeLCase\t\t: "Lágstafir (a, b, c)",\r\n
DlgLstTypeUCase\t\t: "Hástafir (A, B, C)",\r\n
DlgLstTypeSRoman\t: "Rómverkar lágstafatölur (i, ii, iii)",\r\n
DlgLstTypeLRoman\t: "Rómverkar hástafatölur (I, II, III)",\r\n
\r\n
// Document Properties Dialog\r\n
DlgDocGeneralTab\t: "Almennt",\r\n
DlgDocBackTab\t\t: "Bakgrunnur",\r\n
DlgDocColorsTab\t\t: "Litir og rammar",\r\n
DlgDocMetaTab\t\t: "Lýsigögn",\r\n
\r\n
DlgDocPageTitle\t\t: "Titill síðu",\r\n
DlgDocLangDir\t\t: "Tungumál",\r\n
DlgDocLangDirLTR\t: "Vinstri til hægri (LTR)",\r\n
DlgDocLangDirRTL\t: "Hægri til vinstri (RTL)",\r\n
DlgDocLangCode\t\t: "Tungumálakóði",\r\n
DlgDocCharSet\t\t: "Letursett",\r\n
DlgDocCharSetCE\t\t: "Mið-evrópskt",\r\n
DlgDocCharSetCT\t\t: "Kínverskt, hefðbundið (Big5)",\r\n
DlgDocCharSetCR\t\t: "Kýrilskt",\r\n
DlgDocCharSetGR\t\t: "Grískt",\r\n
DlgDocCharSetJP\t\t: "Japanskt",\r\n
DlgDocCharSetKR\t\t: "Kóreskt",\r\n
DlgDocCharSetTR\t\t: "Tyrkneskt",\r\n
DlgDocCharSetUN\t\t: "Unicode (UTF-8)",\r\n
DlgDocCharSetWE\t\t: "Vestur-evrópst",\r\n
DlgDocCharSetOther\t: "Annað letursett",\r\n
\r\n
DlgDocDocType\t\t: "Flokkur skjalategunda",\r\n
DlgDocDocTypeOther\t: "Annar flokkur skjalategunda",\r\n
DlgDocIncXHTML\t\t: "Fella inn XHTML lýsingu",\r\n
DlgDocBgColor\t\t: "Bakgrunnslitur",\r\n
DlgDocBgImage\t\t: "Slóð bakgrunnsmyndar",\r\n
DlgDocBgNoScroll\t: "Læstur bakgrunnur",\r\n
DlgDocCText\t\t\t: "Texti",\r\n
DlgDocCLink\t\t\t: "Stikla",\r\n
DlgDocCVisited\t\t: "Heimsótt stikla",\r\n
DlgDocCActive\t\t: "Virk stikla",\r\n
DlgDocMargins\t\t: "Hliðarspássía",\r\n
DlgDocMaTop\t\t\t: "Efst",\r\n
DlgDocMaLeft\t\t: "Vinstri",\r\n
DlgDocMaRight\t\t: "Hægri",\r\n
DlgDocMaBottom\t\t: "Neðst",\r\n
DlgDocMeIndex\t\t: "Lykilorð efnisorðaskrár (aðgreind með kommum)",\r\n
DlgDocMeDescr\t\t: "Lýsing skjals",\r\n
DlgDocMeAuthor\t\t: "Höfundur",\r\n
DlgDocMeCopy\t\t: "Höfundarréttur",\r\n
DlgDocPreview\t\t: "Sýna",\r\n
\r\n
// Templates Dialog\r\n
Templates\t\t\t: "Sniðmát",\r\n
DlgTemplatesTitle\t: "Innihaldssniðmát",\r\n
DlgTemplatesSelMsg\t: "Veldu sniðmát til að opna í ritlinum.<br>(Núverandi innihald víkur fyrir því!):",\r\n
DlgTemplatesLoading\t: "Sæki lista yfir sniðmát...",\r\n
DlgTemplatesNoTpl\t: "(Ekkert sniðmát er skilgreint!)",\r\n
DlgTemplatesReplace\t: "Skipta út raunverulegu innihaldi",\r\n
\r\n
// About Dialog\r\n
DlgAboutAboutTab\t: "Um",\r\n
DlgAboutBrowserInfoTab\t: "Almennt",\r\n
DlgAboutLicenseTab\t: "Leyfi",\r\n
DlgAboutVersion\t\t: "útgáfa",\r\n
DlgAboutInfo\t\t: "Nánari upplýsinar, sjá:",\r\n
\r\n
// Div Dialog\r\n
DlgDivGeneralTab\t: "Almennt",\r\n
DlgDivAdvancedTab\t: "Sérhæft",\r\n
DlgDivStyle\t\t: "Stíll",\r\n
DlgDivInlineStyle\t: "Línulægur stíll",\r\n
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
            <value> <int>18742</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
