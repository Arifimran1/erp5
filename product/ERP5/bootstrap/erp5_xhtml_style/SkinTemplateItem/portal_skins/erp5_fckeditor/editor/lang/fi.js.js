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
            <value> <string>fi.js</string> </value>
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
 * Finnish language file.\r\n
 */\r\n
\r\n
var FCKLang =\r\n
{\r\n
// Language direction : "ltr" (left to right) or "rtl" (right to left).\r\n
Dir\t\t\t\t\t: "ltr",\r\n
\r\n
ToolbarCollapse\t\t: "Piilota työkalurivi",\r\n
ToolbarExpand\t\t: "Näytä työkalurivi",\r\n
\r\n
// Toolbar Items and Context Menu\r\n
Save\t\t\t\t: "Tallenna",\r\n
NewPage\t\t\t\t: "Tyhjennä",\r\n
Preview\t\t\t\t: "Esikatsele",\r\n
Cut\t\t\t\t\t: "Leikkaa",\r\n
Copy\t\t\t\t: "Kopioi",\r\n
Paste\t\t\t\t: "Liitä",\r\n
PasteText\t\t\t: "Liitä tekstinä",\r\n
PasteWord\t\t\t: "Liitä Wordista",\r\n
Print\t\t\t\t: "Tulosta",\r\n
SelectAll\t\t\t: "Valitse kaikki",\r\n
RemoveFormat\t\t: "Poista muotoilu",\r\n
InsertLinkLbl\t\t: "Linkki",\r\n
InsertLink\t\t\t: "Lisää linkki/muokkaa linkkiä",\r\n
RemoveLink\t\t\t: "Poista linkki",\r\n
VisitLink\t\t\t: "Avaa linkki",\r\n
Anchor\t\t\t\t: "Lisää ankkuri/muokkaa ankkuria",\r\n
AnchorDelete\t\t: "Poista ankkuri",\r\n
InsertImageLbl\t\t: "Kuva",\r\n
InsertImage\t\t\t: "Lisää kuva/muokkaa kuvaa",\r\n
InsertFlashLbl\t\t: "Flash",\r\n
InsertFlash\t\t\t: "Lisää/muokkaa Flashia",\r\n
InsertTableLbl\t\t: "Taulu",\r\n
InsertTable\t\t\t: "Lisää taulu/muokkaa taulua",\r\n
InsertLineLbl\t\t: "Murtoviiva",\r\n
InsertLine\t\t\t: "Lisää murtoviiva",\r\n
InsertSpecialCharLbl: "Erikoismerkki",\r\n
InsertSpecialChar\t: "Lisää erikoismerkki",\r\n
InsertSmileyLbl\t\t: "Hymiö",\r\n
InsertSmiley\t\t: "Lisää hymiö",\r\n
About\t\t\t\t: "FCKeditorista",\r\n
Bold\t\t\t\t: "Lihavoitu",\r\n
Italic\t\t\t\t: "Kursivoitu",\r\n
Underline\t\t\t: "Alleviivattu",\r\n
StrikeThrough\t\t: "Yliviivattu",\r\n
Subscript\t\t\t: "Alaindeksi",\r\n
Superscript\t\t\t: "Yläindeksi",\r\n
LeftJustify\t\t\t: "Tasaa vasemmat reunat",\r\n
CenterJustify\t\t: "Keskitä",\r\n
RightJustify\t\t: "Tasaa oikeat reunat",\r\n
BlockJustify\t\t: "Tasaa molemmat reunat",\r\n
DecreaseIndent\t\t: "Pienennä sisennystä",\r\n
IncreaseIndent\t\t: "Suurenna sisennystä",\r\n
Blockquote\t\t\t: "Lainaus",\r\n
CreateDiv\t\t\t: "Lisää Div",\r\n
EditDiv\t\t\t\t: "Muokkaa Div:ä",\r\n
DeleteDiv\t\t\t: "Poista Div",\r\n
Undo\t\t\t\t: "Kumoa",\r\n
Redo\t\t\t\t: "Toista",\r\n
NumberedListLbl\t\t: "Numerointi",\r\n
NumberedList\t\t: "Lisää/poista numerointi",\r\n
BulletedListLbl\t\t: "Luottelomerkit",\r\n
BulletedList\t\t: "Lisää/poista luottelomerkit",\r\n
ShowTableBorders\t: "Näytä taulun rajat",\r\n
ShowDetails\t\t\t: "Näytä muotoilu",\r\n
Style\t\t\t\t: "Tyyli",\r\n
FontFormat\t\t\t: "Muotoilu",\r\n
Font\t\t\t\t: "Fontti",\r\n
FontSize\t\t\t: "Koko",\r\n
TextColor\t\t\t: "Tekstiväri",\r\n
BGColor\t\t\t\t: "Taustaväri",\r\n
Source\t\t\t\t: "Koodi",\r\n
Find\t\t\t\t: "Etsi",\r\n
Replace\t\t\t\t: "Korvaa",\r\n
SpellCheck\t\t\t: "Tarkista oikeinkirjoitus",\r\n
UniversalKeyboard\t: "Universaali näppäimistö",\r\n
PageBreakLbl\t\t: "Sivun vaihto",\r\n
PageBreak\t\t\t: "Lisää sivun vaihto",\r\n
\r\n
Form\t\t\t: "Lomake",\r\n
Checkbox\t\t: "Valintaruutu",\r\n
RadioButton\t\t: "Radiopainike",\r\n
TextField\t\t: "Tekstikenttä",\r\n
Textarea\t\t: "Tekstilaatikko",\r\n
HiddenField\t\t: "Piilokenttä",\r\n
Button\t\t\t: "Painike",\r\n
SelectionField\t: "Valintakenttä",\r\n
ImageButton\t\t: "Kuvapainike",\r\n
\r\n
FitWindow\t\t: "Suurenna editori koko ikkunaan",\r\n
ShowBlocks\t\t: "Näytä elementit",\r\n
\r\n
// Context Menu\r\n
EditLink\t\t\t: "Muokkaa linkkiä",\r\n
CellCM\t\t\t\t: "Solu",\r\n
RowCM\t\t\t\t: "Rivi",\r\n
ColumnCM\t\t\t: "Sarake",\r\n
InsertRowAfter\t\t: "Lisää rivi alapuolelle",\r\n
InsertRowBefore\t\t: "Lisää rivi yläpuolelle",\r\n
DeleteRows\t\t\t: "Poista rivit",\r\n
InsertColumnAfter\t: "Lisää sarake oikealle",\r\n
InsertColumnBefore\t: "Lisää sarake vasemmalle",\r\n
DeleteColumns\t\t: "Poista sarakkeet",\r\n
InsertCellAfter\t\t: "Lisää solu perään",\r\n
InsertCellBefore\t: "Lisää solu eteen",\r\n
DeleteCells\t\t\t: "Poista solut",\r\n
MergeCells\t\t\t: "Yhdistä solut",\r\n
MergeRight\t\t\t: "Yhdistä oikealla olevan kanssa",\r\n
MergeDown\t\t\t: "Yhdistä alla olevan kanssa",\r\n
HorizontalSplitCell\t: "Jaa solu vaakasuunnassa",\r\n
VerticalSplitCell\t: "Jaa solu pystysuunnassa",\r\n
TableDelete\t\t\t: "Poista taulu",\r\n
CellProperties\t\t: "Solun ominaisuudet",\r\n
TableProperties\t\t: "Taulun ominaisuudet",\r\n
ImageProperties\t\t: "Kuvan ominaisuudet",\r\n
FlashProperties\t\t: "Flash ominaisuudet",\r\n
\r\n
AnchorProp\t\t\t: "Ankkurin ominaisuudet",\r\n
ButtonProp\t\t\t: "Painikkeen ominaisuudet",\r\n
CheckboxProp\t\t: "Valintaruudun ominaisuudet",\r\n
HiddenFieldProp\t\t: "Piilokentän ominaisuudet",\r\n
RadioButtonProp\t\t: "Radiopainikkeen ominaisuudet",\r\n
ImageButtonProp\t\t: "Kuvapainikkeen ominaisuudet",\r\n
TextFieldProp\t\t: "Tekstikentän ominaisuudet",\r\n
SelectionFieldProp\t: "Valintakentän ominaisuudet",\r\n
TextareaProp\t\t: "Tekstilaatikon ominaisuudet",\r\n
FormProp\t\t\t: "Lomakkeen ominaisuudet",\r\n
\r\n
FontFormats\t\t\t: "Normaali;Muotoiltu;Osoite;Otsikko 1;Otsikko 2;Otsikko 3;Otsikko 4;Otsikko 5;Otsikko 6",\r\n
\r\n
// Alerts and Messages\r\n
ProcessingXHTML\t\t: "Prosessoidaan XHTML:ää. Odota hetki...",\r\n
Done\t\t\t\t: "Valmis",\r\n
PasteWordConfirm\t: "Teksti, jonka haluat liittää, näyttää olevan kopioitu Wordista. Haluatko puhdistaa sen ennen liittämistä?",\r\n
NotCompatiblePaste\t: "Tämä komento toimii vain Internet Explorer 5.5:ssa tai uudemmassa. Haluatko liittää ilman puhdistusta?",\r\n
UnknownToolbarItem\t: "Tuntemanton työkalu \\"%1\\"",\r\n
UnknownCommand\t\t: "Tuntematon komento \\"%1\\"",\r\n
NotImplemented\t\t: "Komentoa ei ole liitetty sovellukseen",\r\n
UnknownToolbarSet\t: "Työkalukokonaisuus \\"%1\\" ei ole olemassa",\r\n
NoActiveX\t\t\t: "Selaimesi turvallisuusasetukset voivat rajoittaa joitain editorin ominaisuuksia. Sinun pitää ottaa käyttöön asetuksista \\"Suorita ActiveX komponentit ja -plugin-laajennukset\\". Saatat kohdata virheitä ja huomata puuttuvia ominaisuuksia.",\r\n
BrowseServerBlocked : "Resurssiselainta ei voitu avata. Varmista, että ponnahdusikkunoiden estäjät eivät ole päällä.",\r\n
DialogBlocked\t\t: "Apuikkunaa ei voitu avaata. Varmista, että ponnahdusikkunoiden estäjät eivät ole päällä.",\r\n
VisitLinkBlocked\t: "IUutta ikkunaa ei voitu avata. Varmista, että ponnahdusikkunoiden estäjät eivät ole päällä.",\r\n
\r\n
// Dialogs\r\n
DlgBtnOK\t\t\t: "OK",\r\n
DlgBtnCancel\t\t: "Peruuta",\r\n
DlgBtnClose\t\t\t: "Sulje",\r\n
DlgBtnBrowseServer\t: "Selaa palvelinta",\r\n
DlgAdvancedTag\t\t: "Lisäominaisuudet",\r\n
DlgOpOther\t\t\t: "Muut",\r\n
DlgInfoTab\t\t\t: "Info",\r\n
DlgAlertUrl\t\t\t: "Lisää URL",\r\n
\r\n
// General Dialogs Labels\r\n
DlgGenNotSet\t\t: "<ei asetettu>",\r\n
DlgGenId\t\t\t: "Tunniste",\r\n
DlgGenLangDir\t\t: "Kielen suunta",\r\n
DlgGenLangDirLtr\t: "Vasemmalta oikealle (LTR)",\r\n
DlgGenLangDirRtl\t: "Oikealta vasemmalle (RTL)",\r\n
DlgGenLangCode\t\t: "Kielikoodi",\r\n
DlgGenAccessKey\t\t: "Pikanäppäin",\r\n
DlgGenName\t\t\t: "Nimi",\r\n
DlgGenTabIndex\t\t: "Tabulaattori indeksi",\r\n
DlgGenLongDescr\t\t: "Pitkän kuvauksen URL",\r\n
DlgGenClass\t\t\t: "Tyyliluokat",\r\n
DlgGenTitle\t\t\t: "Avustava otsikko",\r\n
DlgGenContType\t\t: "Avustava sisällön tyyppi",\r\n
DlgGenLinkCharset\t: "Linkitetty kirjaimisto",\r\n
DlgGenStyle\t\t\t: "Tyyli",\r\n
\r\n
// Image Dialog\r\n
DlgImgTitle\t\t\t: "Kuvan ominaisuudet",\r\n
DlgImgInfoTab\t\t: "Kuvan tiedot",\r\n
DlgImgBtnUpload\t\t: "Lähetä palvelimelle",\r\n
DlgImgURL\t\t\t: "Osoite",\r\n
DlgImgUpload\t\t: "Lisää kuva",\r\n
DlgImgAlt\t\t\t: "Vaihtoehtoinen teksti",\r\n
DlgImgWidth\t\t\t: "Leveys",\r\n
DlgImgHeight\t\t: "Korkeus",\r\n
DlgImgLockRatio\t\t: "Lukitse suhteet",\r\n
DlgBtnResetSize\t\t: "Alkuperäinen koko",\r\n
DlgImgBorder\t\t: "Raja",\r\n
DlgImgHSpace\t\t: "Vaakatila",\r\n
DlgImgVSpace\t\t: "Pystytila",\r\n
DlgImgAlign\t\t\t: "Kohdistus",\r\n
DlgImgAlignLeft\t\t: "Vasemmalle",\r\n
DlgImgAlignAbsBottom: "Aivan alas",\r\n
DlgImgAlignAbsMiddle: "Aivan keskelle",\r\n
DlgImgAlignBaseline\t: "Alas (teksti)",\r\n
DlgImgAlignBottom\t: "Alas",\r\n
DlgImgAlignMiddle\t: "Keskelle",\r\n
DlgImgAlignRight\t: "Oikealle",\r\n
DlgImgAlignTextTop\t: "Ylös (teksti)",\r\n
DlgImgAlignTop\t\t: "Ylös",\r\n
DlgImgPreview\t\t: "Esikatselu",\r\n
DlgImgAlertUrl\t\t: "Kirjoita kuvan osoite (URL)",\r\n
DlgImgLinkTab\t\t: "Linkki",\r\n
\r\n
// Flash Dialog\r\n
DlgFlashTitle\t\t: "Flash ominaisuudet",\r\n
DlgFlashChkPlay\t\t: "Automaattinen käynnistys",\r\n
DlgFlashChkLoop\t\t: "Toisto",\r\n
DlgFlashChkMenu\t\t: "Näytä Flash-valikko",\r\n
DlgFlashScale\t\t: "Levitä",\r\n
DlgFlashScaleAll\t: "Näytä kaikki",\r\n
DlgFlashScaleNoBorder\t: "Ei rajaa",\r\n
DlgFlashScaleFit\t: "Tarkka koko",\r\n
\r\n
// Link Dialog\r\n
DlgLnkWindowTitle\t: "Linkki",\r\n
DlgLnkInfoTab\t\t: "Linkin tiedot",\r\n
DlgLnkTargetTab\t\t: "Kohde",\r\n
\r\n
DlgLnkType\t\t\t: "Linkkityyppi",\r\n
DlgLnkTypeURL\t\t: "Osoite",\r\n
DlgLnkTypeAnchor\t: "Ankkuri tässä sivussa",\r\n
DlgLnkTypeEMail\t\t: "Sähköposti",\r\n
DlgLnkProto\t\t\t: "Protokolla",\r\n
DlgLnkProtoOther\t: "<muu>",\r\n
DlgLnkURL\t\t\t: "Osoite",\r\n
DlgLnkAnchorSel\t\t: "Valitse ankkuri",\r\n
DlgLnkAnchorByName\t: "Ankkurin nimen mukaan",\r\n
DlgLnkAnchorById\t: "Ankkurin ID:n mukaan",\r\n
DlgLnkNoAnchors\t\t: "(Ei ankkureita tässä dokumentissa)",\r\n
DlgLnkEMail\t\t\t: "Sähköpostiosoite",\r\n
DlgLnkEMailSubject\t: "Aihe",\r\n
DlgLnkEMailBody\t\t: "Viesti",\r\n
DlgLnkUpload\t\t: "Lisää tiedosto",\r\n
DlgLnkBtnUpload\t\t: "Lähetä palvelimelle",\r\n
\r\n
DlgLnkTarget\t\t: "Kohde",\r\n
DlgLnkTargetFrame\t: "<kehys>",\r\n
DlgLnkTargetPopup\t: "<popup ikkuna>",\r\n
DlgLnkTargetBlank\t: "Uusi ikkuna (_blank)",\r\n
DlgLnkTargetParent\t: "Emoikkuna (_parent)",\r\n
DlgLnkTargetSelf\t: "Sama ikkuna (_self)",\r\n
DlgLnkTargetTop\t\t: "Päällimmäisin ikkuna (_top)",\r\n
DlgLnkTargetFrameName\t: "Kohdekehyksen nimi",\r\n
DlgLnkPopWinName\t: "Popup ikkunan nimi",\r\n
DlgLnkPopWinFeat\t: "Popup ikkunan ominaisuudet",\r\n
DlgLnkPopResize\t\t: "Venytettävä",\r\n
DlgLnkPopLocation\t: "Osoiterivi",\r\n
DlgLnkPopMenu\t\t: "Valikkorivi",\r\n
DlgLnkPopScroll\t\t: "Vierityspalkit",\r\n
DlgLnkPopStatus\t\t: "Tilarivi",\r\n
DlgLnkPopToolbar\t: "Vakiopainikkeet",\r\n
DlgLnkPopFullScrn\t: "Täysi ikkuna (IE)",\r\n
DlgLnkPopDependent\t: "Riippuva (Netscape)",\r\n
DlgLnkPopWidth\t\t: "Leveys",\r\n
DlgLnkPopHeight\t\t: "Korkeus",\r\n
DlgLnkPopLeft\t\t: "Vasemmalta (px)",\r\n
DlgLnkPopTop\t\t: "Ylhäältä (px)",\r\n
\r\n
DlnLnkMsgNoUrl\t\t: "Linkille on kirjoitettava URL",\r\n
DlnLnkMsgNoEMail\t: "Kirjoita sähköpostiosoite",\r\n
DlnLnkMsgNoAnchor\t: "Valitse ankkuri",\r\n
DlnLnkMsgInvPopName\t: "Popup-ikkunan nimi pitää alkaa aakkosella ja ei saa sisältää välejä",\r\n
\r\n
// Color Dialog\r\n
DlgColorTitle\t\t: "Valitse väri",\r\n
DlgColorBtnClear\t: "Tyhjennä",\r\n
DlgColorHighlight\t: "Kohdalla",\r\n
DlgColorSelected\t: "Valittu",\r\n
\r\n
// Smiley Dialog\r\n
DlgSmileyTitle\t\t: "Lisää hymiö",\r\n
\r\n
// Special Character Dialog\r\n
DlgSpecialCharTitle\t: "Valitse erikoismerkki",\r\n
\r\n
// Table Dialog\r\n
DlgTableTitle\t\t: "Taulun ominaisuudet",\r\n
DlgTableRows\t\t: "Rivit",\r\n
DlgTableColumns\t\t: "Sarakkeet",\r\n
DlgTableBorder\t\t: "Rajan paksuus",\r\n
DlgTableAlign\t\t: "Kohdistus",\r\n
DlgTableAlignNotSet\t: "<ei asetettu>",\r\n
DlgTableAlignLeft\t: "Vasemmalle",\r\n
DlgTableAlignCenter\t: "Keskelle",\r\n
DlgTableAlignRight\t: "Oikealle",\r\n
DlgTableWidth\t\t: "Leveys",\r\n
DlgTableWidthPx\t\t: "pikseliä",\r\n
DlgTableWidthPc\t\t: "prosenttia",\r\n
DlgTableHeight\t\t: "Korkeus",\r\n
DlgTableCellSpace\t: "Solujen väli",\r\n
DlgTableCellPad\t\t: "Solujen sisennys",\r\n
DlgTableCaption\t\t: "Otsikko",\r\n
DlgTableSummary\t\t: "Yhteenveto",\r\n
DlgTableHeaders\t\t: "Ylätunnisteet",\r\n
DlgTableHeadersNone\t\t: "Ei ylätunnisteita",\r\n
DlgTableHeadersColumn\t: "Ensimmäinen sarake",\r\n
DlgTableHeadersRow\t\t: "Ensimmäinen rivi",\r\n
DlgTableHeadersBoth\t\t: "Molemmat",\r\n
\r\n
// Table Cell Dialog\r\n
DlgCellTitle\t\t: "Solun ominaisuudet",\r\n
DlgCellWidth\t\t: "Leveys",\r\n
DlgCellWidthPx\t\t: "pikseliä",\r\n
DlgCellWidthPc\t\t: "prosenttia",\r\n
DlgCellHeight\t\t: "Korkeus",\r\n
DlgCellWordWrap\t\t: "Tekstikierrätys",\r\n
DlgCellWordWrapNotSet\t: "<Ei asetettu>",\r\n
DlgCellWordWrapYes\t: "Kyllä",\r\n
DlgCellWordWrapNo\t: "Ei",\r\n
DlgCellHorAlign\t\t: "Vaakakohdistus",\r\n
DlgCellHorAlignNotSet\t: "<Ei asetettu>",\r\n
DlgCellHorAlignLeft\t: "Vasemmalle",\r\n
DlgCellHorAlignCenter\t: "Keskelle",\r\n
DlgCellHorAlignRight: "Oikealle",\r\n
DlgCellVerAlign\t\t: "Pystykohdistus",\r\n
DlgCellVerAlignNotSet\t: "<Ei asetettu>",\r\n
DlgCellVerAlignTop\t: "Ylös",\r\n
DlgCellVerAlignMiddle\t: "Keskelle",\r\n
DlgCellVerAlignBottom\t: "Alas",\r\n
DlgCellVerAlignBaseline\t: "Tekstin alas",\r\n
DlgCellType\t\t: "Solun tyyppi",\r\n
DlgCellTypeData\t\t: "Sisältö",\r\n
DlgCellTypeHeader\t: "Ylätunniste",\r\n
DlgCellRowSpan\t\t: "Rivin jatkuvuus",\r\n
DlgCellCollSpan\t\t: "Sarakkeen jatkuvuus",\r\n
DlgCellBackColor\t: "Taustaväri",\r\n
DlgCellBorderColor\t: "Rajan väri",\r\n
DlgCellBtnSelect\t: "Valitse...",\r\n
\r\n
// Find and Replace Dialog\r\n
DlgFindAndReplaceTitle\t: "Etsi ja korvaa",\r\n
\r\n
// Find Dialog\r\n
DlgFindTitle\t\t: "Etsi",\r\n
DlgFindFindBtn\t\t: "Etsi",\r\n
DlgFindNotFoundMsg\t: "Etsittyä tekstiä ei löytynyt.",\r\n
\r\n
// Replace Dialog\r\n
DlgReplaceTitle\t\t\t: "Korvaa",\r\n
DlgReplaceFindLbl\t\t: "Etsi mitä:",\r\n
DlgReplaceReplaceLbl\t: "Korvaa tällä:",\r\n
DlgReplaceCaseChk\t\t: "Sama kirjainkoko",\r\n
DlgReplaceReplaceBtn\t: "Korvaa",\r\n
DlgReplaceReplAllBtn\t: "Korvaa kaikki",\r\n
DlgReplaceWordChk\t\t: "Koko sana",\r\n
\r\n
// Paste Operations / Dialog\r\n
PasteErrorCut\t: "Selaimesi turva-asetukset eivät salli editorin toteuttaa leikkaamista. Käytä näppäimistöä leikkaamiseen (Ctrl+X).",\r\n
PasteErrorCopy\t: "Selaimesi turva-asetukset eivät salli editorin toteuttaa kopioimista. Käytä näppäimistöä kopioimiseen (Ctrl+C).",\r\n
\r\n
PasteAsText\t\t: "Liitä tekstinä",\r\n
PasteFromWord\t: "Liitä Wordista",\r\n
\r\n
DlgPasteMsg2\t: "Liitä painamalla (<STRONG>Ctrl+V</STRONG>) ja painamalla <STRONG>OK</STRONG>.",\r\n
DlgPasteSec\t\t: "Selaimesi turva-asetukset eivät salli editorin käyttää leikepöytää suoraan. Sinun pitää suorittaa liittäminen tässä ikkunassa.",\r\n
DlgPasteIgnoreFont\t\t: "Jätä huomioimatta fonttimääritykset",\r\n
DlgPasteRemoveStyles\t: "Poista tyylimääritykset",\r\n
\r\n
// Color Picker\r\n
ColorAutomatic\t: "Automaattinen",\r\n
ColorMoreColors\t: "Lisää värejä...",\r\n
\r\n
// Document Properties\r\n
DocProps\t\t: "Dokumentin ominaisuudet",\r\n
\r\n
// Anchor Dialog\r\n
DlgAnchorTitle\t\t: "Ankkurin ominaisuudet",\r\n
DlgAnchorName\t\t: "Nimi",\r\n
DlgAnchorErrorName\t: "Ankkurille on kirjoitettava nimi",\r\n
\r\n
// Speller Pages Dialog\r\n
DlgSpellNotInDic\t\t: "Ei sanakirjassa",\r\n
DlgSpellChangeTo\t\t: "Vaihda",\r\n
DlgSpellBtnIgnore\t\t: "Jätä huomioimatta",\r\n
DlgSpellBtnIgnoreAll\t: "Jätä kaikki huomioimatta",\r\n
DlgSpellBtnReplace\t\t: "Korvaa",\r\n
DlgSpellBtnReplaceAll\t: "Korvaa kaikki",\r\n
DlgSpellBtnUndo\t\t\t: "Kumoa",\r\n
DlgSpellNoSuggestions\t: "Ei ehdotuksia",\r\n
DlgSpellProgress\t\t: "Tarkistus käynnissä...",\r\n
DlgSpellNoMispell\t\t: "Tarkistus valmis: Ei virheitä",\r\n
DlgSpellNoChanges\t\t: "Tarkistus valmis: Yhtään sanaa ei muutettu",\r\n
DlgSpellOneChange\t\t: "Tarkistus valmis: Yksi sana muutettiin",\r\n
DlgSpellManyChanges\t\t: "Tarkistus valmis: %1 sanaa muutettiin",\r\n
\r\n
IeSpellDownload\t\t\t: "Oikeinkirjoituksen tarkistusta ei ole asennettu. Haluatko ladata sen nyt?",\r\n
\r\n
// Button Dialog\r\n
DlgButtonText\t\t: "Teksti (arvo)",\r\n
DlgButtonType\t\t: "Tyyppi",\r\n
DlgButtonTypeBtn\t: "Painike",\r\n
DlgButtonTypeSbm\t: "Lähetä",\r\n
DlgButtonTypeRst\t: "Tyhjennä",\r\n
\r\n
// Checkbox and Radio Button Dialogs\r\n
DlgCheckboxName\t\t: "Nimi",\r\n
DlgCheckboxValue\t: "Arvo",\r\n
DlgCheckboxSelected\t: "Valittu",\r\n
\r\n
// Form Dialog\r\n
DlgFormName\t\t: "Nimi",\r\n
DlgFormAction\t: "Toiminto",\r\n
DlgFormMethod\t: "Tapa",\r\n
\r\n
// Select Field Dialog\r\n
DlgSelectName\t\t: "Nimi",\r\n
DlgSelectValue\t\t: "Arvo",\r\n
DlgSelectSize\t\t: "Koko",\r\n
DlgSelectLines\t\t: "Rivit",\r\n
DlgSelectChkMulti\t: "Salli usea valinta",\r\n
DlgSelectOpAvail\t: "Ominaisuudet",\r\n
DlgSelectOpText\t\t: "Teksti",\r\n
DlgSelectOpValue\t: "Arvo",\r\n
DlgSelectBtnAdd\t\t: "Lisää",\r\n
DlgSelectBtnModify\t: "Muuta",\r\n
DlgSelectBtnUp\t\t: "Ylös",\r\n
DlgSelectBtnDown\t: "Alas",\r\n
DlgSelectBtnSetValue : "Aseta valituksi",\r\n
DlgSelectBtnDelete\t: "Poista",\r\n
\r\n
// Textarea Dialog\r\n
DlgTextareaName\t: "Nimi",\r\n
DlgTextareaCols\t: "Sarakkeita",\r\n
DlgTextareaRows\t: "Rivejä",\r\n
\r\n
// Text Field Dialog\r\n
DlgTextName\t\t\t: "Nimi",\r\n
DlgTextValue\t\t: "Arvo",\r\n
DlgTextCharWidth\t: "Leveys",\r\n
DlgTextMaxChars\t\t: "Maksimi merkkimäärä",\r\n
DlgTextType\t\t\t: "Tyyppi",\r\n
DlgTextTypeText\t\t: "Teksti",\r\n
DlgTextTypePass\t\t: "Salasana",\r\n
\r\n
// Hidden Field Dialog\r\n
DlgHiddenName\t: "Nimi",\r\n
DlgHiddenValue\t: "Arvo",\r\n
\r\n
// Bulleted List Dialog\r\n
BulletedListProp\t: "Luettelon ominaisuudet",\r\n
NumberedListProp\t: "Numeroinnin ominaisuudet",\r\n
DlgLstStart\t\t\t: "Alku",\r\n
DlgLstType\t\t\t: "Tyyppi",\r\n
DlgLstTypeCircle\t: "Kehä",\r\n
DlgLstTypeDisc\t\t: "Ympyrä",\r\n
DlgLstTypeSquare\t: "Neliö",\r\n
DlgLstTypeNumbers\t: "Numerot (1, 2, 3)",\r\n
DlgLstTypeLCase\t\t: "Pienet kirjaimet (a, b, c)",\r\n
DlgLstTypeUCase\t\t: "Isot kirjaimet (A, B, C)",\r\n
DlgLstTypeSRoman\t: "Pienet roomalaiset numerot (i, ii, iii)",\r\n
DlgLstTypeLRoman\t: "Isot roomalaiset numerot (Ii, II, III)",\r\n
\r\n
// Document Properties Dialog\r\n
DlgDocGeneralTab\t: "Yleiset",\r\n
DlgDocBackTab\t\t: "Tausta",\r\n
DlgDocColorsTab\t\t: "Värit ja marginaalit",\r\n
DlgDocMetaTab\t\t: "Meta-tieto",\r\n
\r\n
DlgDocPageTitle\t\t: "Sivun nimi",\r\n
DlgDocLangDir\t\t: "Kielen suunta",\r\n
DlgDocLangDirLTR\t: "Vasemmalta oikealle (LTR)",\r\n
DlgDocLangDirRTL\t: "Oikealta vasemmalle (RTL)",\r\n
DlgDocLangCode\t\t: "Kielikoodi",\r\n
DlgDocCharSet\t\t: "Merkistökoodaus",\r\n
DlgDocCharSetCE\t\t: "Keskieurooppalainen",\r\n
DlgDocCharSetCT\t\t: "Kiina, perinteinen (Big5)",\r\n
DlgDocCharSetCR\t\t: "Kyrillinen",\r\n
DlgDocCharSetGR\t\t: "Kreikka",\r\n
DlgDocCharSetJP\t\t: "Japani",\r\n
DlgDocCharSetKR\t\t: "Korealainen",\r\n
DlgDocCharSetTR\t\t: "Turkkilainen",\r\n
DlgDocCharSetUN\t\t: "Unicode (UTF-8)",\r\n
DlgDocCharSetWE\t\t: "Länsieurooppalainen",\r\n
DlgDocCharSetOther\t: "Muu merkistökoodaus",\r\n
\r\n
DlgDocDocType\t\t: "Dokumentin tyyppi",\r\n
DlgDocDocTypeOther\t: "Muu dokumentin tyyppi",\r\n
DlgDocIncXHTML\t\t: "Lisää XHTML julistukset",\r\n
DlgDocBgColor\t\t: "Taustaväri",\r\n
DlgDocBgImage\t\t: "Taustakuva",\r\n
DlgDocBgNoScroll\t: "Paikallaanpysyvä tausta",\r\n
DlgDocCText\t\t\t: "Teksti",\r\n
DlgDocCLink\t\t\t: "Linkki",\r\n
DlgDocCVisited\t\t: "Vierailtu linkki",\r\n
DlgDocCActive\t\t: "Aktiivinen linkki",\r\n
DlgDocMargins\t\t: "Sivun marginaalit",\r\n
DlgDocMaTop\t\t\t: "Ylä",\r\n
DlgDocMaLeft\t\t: "Vasen",\r\n
DlgDocMaRight\t\t: "Oikea",\r\n
DlgDocMaBottom\t\t: "Ala",\r\n
DlgDocMeIndex\t\t: "Hakusanat (pilkulla erotettuna)",\r\n
DlgDocMeDescr\t\t: "Kuvaus",\r\n
DlgDocMeAuthor\t\t: "Tekijä",\r\n
DlgDocMeCopy\t\t: "Tekijänoikeudet",\r\n
DlgDocPreview\t\t: "Esikatselu",\r\n
\r\n
// Templates Dialog\r\n
Templates\t\t\t: "Pohjat",\r\n
DlgTemplatesTitle\t: "Sisältöpohjat",\r\n
DlgTemplatesSelMsg\t: "Valitse pohja editoriin<br>(aiempi sisältö menetetään):",\r\n
DlgTemplatesLoading\t: "Ladataan listaa pohjista. Hetkinen...",\r\n
DlgTemplatesNoTpl\t: "(Ei määriteltyjä pohjia)",\r\n
DlgTemplatesReplace\t: "Korvaa editorin koko sisältö",\r\n
\r\n
// About Dialog\r\n
DlgAboutAboutTab\t: "Editorista",\r\n
DlgAboutBrowserInfoTab\t: "Selaimen tiedot",\r\n
DlgAboutLicenseTab\t: "Lisenssi",\r\n
DlgAboutVersion\t\t: "versio",\r\n
DlgAboutInfo\t\t: "Lisää tietoa osoitteesta",\r\n
\r\n
// Div Dialog\r\n
DlgDivGeneralTab\t: "Edistynyt",\r\n
DlgDivAdvancedTab\t: "Advanced",\t//MISSING\r\n
DlgDivStyle\t\t: "Tyyli",\r\n
DlgDivInlineStyle\t: "Rivin sisäinen tyyli",\r\n
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
            <value> <int>18745</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
