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
            <value> <string>gl.js</string> </value>
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
 * Galician language file.\r\n
 */\r\n
\r\n
var FCKLang =\r\n
{\r\n
// Language direction : "ltr" (left to right) or "rtl" (right to left).\r\n
Dir\t\t\t\t\t: "ltr",\r\n
\r\n
ToolbarCollapse\t\t: "Ocultar Ferramentas",\r\n
ToolbarExpand\t\t: "Mostrar Ferramentas",\r\n
\r\n
// Toolbar Items and Context Menu\r\n
Save\t\t\t\t: "Gardar",\r\n
NewPage\t\t\t\t: "Nova Páxina",\r\n
Preview\t\t\t\t: "Vista Previa",\r\n
Cut\t\t\t\t\t: "Cortar",\r\n
Copy\t\t\t\t: "Copiar",\r\n
Paste\t\t\t\t: "Pegar",\r\n
PasteText\t\t\t: "Pegar como texto plano",\r\n
PasteWord\t\t\t: "Pegar dende Word",\r\n
Print\t\t\t\t: "Imprimir",\r\n
SelectAll\t\t\t: "Seleccionar todo",\r\n
RemoveFormat\t\t: "Eliminar Formato",\r\n
InsertLinkLbl\t\t: "Ligazón",\r\n
InsertLink\t\t\t: "Inserir/Editar Ligazón",\r\n
RemoveLink\t\t\t: "Eliminar Ligazón",\r\n
VisitLink\t\t\t: "Open Link",\t//MISSING\r\n
Anchor\t\t\t\t: "Inserir/Editar Referencia",\r\n
AnchorDelete\t\t: "Remove Anchor",\t//MISSING\r\n
InsertImageLbl\t\t: "Imaxe",\r\n
InsertImage\t\t\t: "Inserir/Editar Imaxe",\r\n
InsertFlashLbl\t\t: "Flash",\r\n
InsertFlash\t\t\t: "Inserir/Editar Flash",\r\n
InsertTableLbl\t\t: "Tabla",\r\n
InsertTable\t\t\t: "Inserir/Editar Tabla",\r\n
InsertLineLbl\t\t: "Liña",\r\n
InsertLine\t\t\t: "Inserir Liña Horizontal",\r\n
InsertSpecialCharLbl: "Carácter Special",\r\n
InsertSpecialChar\t: "Inserir Carácter Especial",\r\n
InsertSmileyLbl\t\t: "Smiley",\r\n
InsertSmiley\t\t: "Inserir Smiley",\r\n
About\t\t\t\t: "Acerca de FCKeditor",\r\n
Bold\t\t\t\t: "Negrita",\r\n
Italic\t\t\t\t: "Cursiva",\r\n
Underline\t\t\t: "Sub-raiado",\r\n
StrikeThrough\t\t: "Tachado",\r\n
Subscript\t\t\t: "Subíndice",\r\n
Superscript\t\t\t: "Superíndice",\r\n
LeftJustify\t\t\t: "Aliñar á Esquerda",\r\n
CenterJustify\t\t: "Centrado",\r\n
RightJustify\t\t: "Aliñar á Dereita",\r\n
BlockJustify\t\t: "Xustificado",\r\n
DecreaseIndent\t\t: "Disminuir Sangría",\r\n
IncreaseIndent\t\t: "Aumentar Sangría",\r\n
Blockquote\t\t\t: "Blockquote",\t//MISSING\r\n
CreateDiv\t\t\t: "Create Div Container",\t//MISSING\r\n
EditDiv\t\t\t\t: "Edit Div Container",\t//MISSING\r\n
DeleteDiv\t\t\t: "Remove Div Container",\t//MISSING\r\n
Undo\t\t\t\t: "Desfacer",\r\n
Redo\t\t\t\t: "Refacer",\r\n
NumberedListLbl\t\t: "Lista Numerada",\r\n
NumberedList\t\t: "Inserir/Eliminar Lista Numerada",\r\n
BulletedListLbl\t\t: "Marcas",\r\n
BulletedList\t\t: "Inserir/Eliminar Marcas",\r\n
ShowTableBorders\t: "Mostrar Bordes das Táboas",\r\n
ShowDetails\t\t\t: "Mostrar Marcas Parágrafo",\r\n
Style\t\t\t\t: "Estilo",\r\n
FontFormat\t\t\t: "Formato",\r\n
Font\t\t\t\t: "Tipo",\r\n
FontSize\t\t\t: "Tamaño",\r\n
TextColor\t\t\t: "Cor do Texto",\r\n
BGColor\t\t\t\t: "Cor do Fondo",\r\n
Source\t\t\t\t: "Código Fonte",\r\n
Find\t\t\t\t: "Procurar",\r\n
Replace\t\t\t\t: "Substituir",\r\n
SpellCheck\t\t\t: "Corrección Ortográfica",\r\n
UniversalKeyboard\t: "Teclado Universal",\r\n
PageBreakLbl\t\t: "Salto de Páxina",\r\n
PageBreak\t\t\t: "Inserir Salto de Páxina",\r\n
\r\n
Form\t\t\t: "Formulario",\r\n
Checkbox\t\t: "Cadro de Verificación",\r\n
RadioButton\t\t: "Botón de Radio",\r\n
TextField\t\t: "Campo de Texto",\r\n
Textarea\t\t: "Área de Texto",\r\n
HiddenField\t\t: "Campo Oculto",\r\n
Button\t\t\t: "Botón",\r\n
SelectionField\t: "Campo de Selección",\r\n
ImageButton\t\t: "Botón de Imaxe",\r\n
\r\n
FitWindow\t\t: "Maximizar o tamaño do editor",\r\n
ShowBlocks\t\t: "Show Blocks",\t//MISSING\r\n
\r\n
// Context Menu\r\n
EditLink\t\t\t: "Editar Ligazón",\r\n
CellCM\t\t\t\t: "Cela",\r\n
RowCM\t\t\t\t: "Fila",\r\n
ColumnCM\t\t\t: "Columna",\r\n
InsertRowAfter\t\t: "Insert Row After",\t//MISSING\r\n
InsertRowBefore\t\t: "Insert Row Before",\t//MISSING\r\n
DeleteRows\t\t\t: "Borrar Filas",\r\n
InsertColumnAfter\t: "Insert Column After",\t//MISSING\r\n
InsertColumnBefore\t: "Insert Column Before",\t//MISSING\r\n
DeleteColumns\t\t: "Borrar Columnas",\r\n
InsertCellAfter\t\t: "Insert Cell After",\t//MISSING\r\n
InsertCellBefore\t: "Insert Cell Before",\t//MISSING\r\n
DeleteCells\t\t\t: "Borrar Cela",\r\n
MergeCells\t\t\t: "Unir Celas",\r\n
MergeRight\t\t\t: "Merge Right",\t//MISSING\r\n
MergeDown\t\t\t: "Merge Down",\t//MISSING\r\n
HorizontalSplitCell\t: "Split Cell Horizontally",\t//MISSING\r\n
VerticalSplitCell\t: "Split Cell Vertically",\t//MISSING\r\n
TableDelete\t\t\t: "Borrar Táboa",\r\n
CellProperties\t\t: "Propriedades da Cela",\r\n
TableProperties\t\t: "Propriedades da Táboa",\r\n
ImageProperties\t\t: "Propriedades Imaxe",\r\n
FlashProperties\t\t: "Propriedades Flash",\r\n
\r\n
AnchorProp\t\t\t: "Propriedades da Referencia",\r\n
ButtonProp\t\t\t: "Propriedades do Botón",\r\n
CheckboxProp\t\t: "Propriedades do Cadro de Verificación",\r\n
HiddenFieldProp\t\t: "Propriedades do Campo Oculto",\r\n
RadioButtonProp\t\t: "Propriedades do Botón de Radio",\r\n
ImageButtonProp\t\t: "Propriedades do Botón de Imaxe",\r\n
TextFieldProp\t\t: "Propriedades do Campo de Texto",\r\n
SelectionFieldProp\t: "Propriedades do Campo de Selección",\r\n
TextareaProp\t\t: "Propriedades da Área de Texto",\r\n
FormProp\t\t\t: "Propriedades do Formulario",\r\n
\r\n
FontFormats\t\t\t: "Normal;Formateado;Enderezo;Enacabezado 1;Encabezado 2;Encabezado 3;Encabezado 4;Encabezado 5;Encabezado 6;Paragraph (DIV)",\r\n
\r\n
// Alerts and Messages\r\n
ProcessingXHTML\t\t: "Procesando XHTML. Por facor, agarde...",\r\n
Done\t\t\t\t: "Feiro",\r\n
PasteWordConfirm\t: "Parece que o texto que quere pegar está copiado do Word.¿Quere limpar o formato antes de pegalo?",\r\n
NotCompatiblePaste\t: "Este comando está disponible para Internet Explorer versión 5.5 ou superior. ¿Quere pegalo sen limpar o formato?",\r\n
UnknownToolbarItem\t: "Ítem de ferramentas descoñecido \\"%1\\"",\r\n
UnknownCommand\t\t: "Nome de comando descoñecido \\"%1\\"",\r\n
NotImplemented\t\t: "Comando non implementado",\r\n
UnknownToolbarSet\t: "O conxunto de ferramentas \\"%1\\" non existe",\r\n
NoActiveX\t\t\t: "As opcións de seguridade do seu navegador poderían limitar algunha das características de editor. Debe activar a opción \\"Executar controis ActiveX e plug-ins\\". Pode notar que faltan características e experimentar erros",\r\n
BrowseServerBlocked : "Non se poido abrir o navegador de recursos. Asegúrese de que están desactivados os bloqueadores de xanelas emerxentes",\r\n
DialogBlocked\t\t: "Non foi posible abrir a xanela de diálogo. Asegúrese de que están desactivados os bloqueadores de xanelas emerxentes",\r\n
VisitLinkBlocked\t: "It was not possible to open a new window. Make sure all popup blockers are disabled.",\t//MISSING\r\n
\r\n
// Dialogs\r\n
DlgBtnOK\t\t\t: "OK",\r\n
DlgBtnCancel\t\t: "Cancelar",\r\n
DlgBtnClose\t\t\t: "Pechar",\r\n
DlgBtnBrowseServer\t: "Navegar no Servidor",\r\n
DlgAdvancedTag\t\t: "Advanzado",\r\n
DlgOpOther\t\t\t: "<Outro>",\r\n
DlgInfoTab\t\t\t: "Info",\r\n
DlgAlertUrl\t\t\t: "Por favor, insira a URL",\r\n
\r\n
// General Dialogs Labels\r\n
DlgGenNotSet\t\t: "<non definido>",\r\n
DlgGenId\t\t\t: "Id",\r\n
DlgGenLangDir\t\t: "Orientación do Idioma",\r\n
DlgGenLangDirLtr\t: "Esquerda a Dereita (LTR)",\r\n
DlgGenLangDirRtl\t: "Dereita a Esquerda (RTL)",\r\n
DlgGenLangCode\t\t: "Código do Idioma",\r\n
DlgGenAccessKey\t\t: "Chave de Acceso",\r\n
DlgGenName\t\t\t: "Nome",\r\n
DlgGenTabIndex\t\t: "Índice de Tabulación",\r\n
DlgGenLongDescr\t\t: "Descrición Completa da URL",\r\n
DlgGenClass\t\t\t: "Clases da Folla de Estilos",\r\n
DlgGenTitle\t\t\t: "Título",\r\n
DlgGenContType\t\t: "Tipo de Contido",\r\n
DlgGenLinkCharset\t: "Fonte de Caracteres Vinculado",\r\n
DlgGenStyle\t\t\t: "Estilo",\r\n
\r\n
// Image Dialog\r\n
DlgImgTitle\t\t\t: "Propriedades da Imaxe",\r\n
DlgImgInfoTab\t\t: "Información da Imaxe",\r\n
DlgImgBtnUpload\t\t: "Enviar ó Servidor",\r\n
DlgImgURL\t\t\t: "URL",\r\n
DlgImgUpload\t\t: "Carregar",\r\n
DlgImgAlt\t\t\t: "Texto Alternativo",\r\n
DlgImgWidth\t\t\t: "Largura",\r\n
DlgImgHeight\t\t: "Altura",\r\n
DlgImgLockRatio\t\t: "Proporcional",\r\n
DlgBtnResetSize\t\t: "Tamaño Orixinal",\r\n
DlgImgBorder\t\t: "Límite",\r\n
DlgImgHSpace\t\t: "Esp. Horiz.",\r\n
DlgImgVSpace\t\t: "Esp. Vert.",\r\n
DlgImgAlign\t\t\t: "Aliñamento",\r\n
DlgImgAlignLeft\t\t: "Esquerda",\r\n
DlgImgAlignAbsBottom: "Abs Inferior",\r\n
DlgImgAlignAbsMiddle: "Abs Centro",\r\n
DlgImgAlignBaseline\t: "Liña Base",\r\n
DlgImgAlignBottom\t: "Pé",\r\n
DlgImgAlignMiddle\t: "Centro",\r\n
DlgImgAlignRight\t: "Dereita",\r\n
DlgImgAlignTextTop\t: "Tope do Texto",\r\n
DlgImgAlignTop\t\t: "Tope",\r\n
DlgImgPreview\t\t: "Vista Previa",\r\n
DlgImgAlertUrl\t\t: "Por favor, escriba a URL da imaxe",\r\n
DlgImgLinkTab\t\t: "Ligazón",\r\n
\r\n
// Flash Dialog\r\n
DlgFlashTitle\t\t: "Propriedades Flash",\r\n
DlgFlashChkPlay\t\t: "Auto Execución",\r\n
DlgFlashChkLoop\t\t: "Bucle",\r\n
DlgFlashChkMenu\t\t: "Activar Menú Flash",\r\n
DlgFlashScale\t\t: "Escalar",\r\n
DlgFlashScaleAll\t: "Amosar Todo",\r\n
DlgFlashScaleNoBorder\t: "Sen Borde",\r\n
DlgFlashScaleFit\t: "Encaixar axustando",\r\n
\r\n
// Link Dialog\r\n
DlgLnkWindowTitle\t: "Ligazón",\r\n
DlgLnkInfoTab\t\t: "Información da Ligazón",\r\n
DlgLnkTargetTab\t\t: "Referencia a esta páxina",\r\n
\r\n
DlgLnkType\t\t\t: "Tipo de Ligazón",\r\n
DlgLnkTypeURL\t\t: "URL",\r\n
DlgLnkTypeAnchor\t: "Referencia nesta páxina",\r\n
DlgLnkTypeEMail\t\t: "E-Mail",\r\n
DlgLnkProto\t\t\t: "Protocolo",\r\n
DlgLnkProtoOther\t: "<outro>",\r\n
DlgLnkURL\t\t\t: "URL",\r\n
DlgLnkAnchorSel\t\t: "Seleccionar unha Referencia",\r\n
DlgLnkAnchorByName\t: "Por Nome de Referencia",\r\n
DlgLnkAnchorById\t: "Por Element Id",\r\n
DlgLnkNoAnchors\t\t: "(Non hai referencias disponibles no documento)",\r\n
DlgLnkEMail\t\t\t: "Enderezo de E-Mail",\r\n
DlgLnkEMailSubject\t: "Asunto do Mensaxe",\r\n
DlgLnkEMailBody\t\t: "Corpo do Mensaxe",\r\n
DlgLnkUpload\t\t: "Carregar",\r\n
DlgLnkBtnUpload\t\t: "Enviar ó servidor",\r\n
\r\n
DlgLnkTarget\t\t: "Destino",\r\n
DlgLnkTargetFrame\t: "<frame>",\r\n
DlgLnkTargetPopup\t: "<Xanela Emerxente>",\r\n
DlgLnkTargetBlank\t: "Nova Xanela (_blank)",\r\n
DlgLnkTargetParent\t: "Xanela Pai (_parent)",\r\n
DlgLnkTargetSelf\t: "Mesma Xanela (_self)",\r\n
DlgLnkTargetTop\t\t: "Xanela Primaria (_top)",\r\n
DlgLnkTargetFrameName\t: "Nome do Marco Destino",\r\n
DlgLnkPopWinName\t: "Nome da Xanela Emerxente",\r\n
DlgLnkPopWinFeat\t: "Características da Xanela Emerxente",\r\n
DlgLnkPopResize\t\t: "Axustable",\r\n
DlgLnkPopLocation\t: "Barra de Localización",\r\n
DlgLnkPopMenu\t\t: "Barra de Menú",\r\n
DlgLnkPopScroll\t\t: "Barras de Desplazamento",\r\n
DlgLnkPopStatus\t\t: "Barra de Estado",\r\n
DlgLnkPopToolbar\t: "Barra de Ferramentas",\r\n
DlgLnkPopFullScrn\t: "A Toda Pantalla (IE)",\r\n
DlgLnkPopDependent\t: "Dependente (Netscape)",\r\n
DlgLnkPopWidth\t\t: "Largura",\r\n
DlgLnkPopHeight\t\t: "Altura",\r\n
DlgLnkPopLeft\t\t: "Posición Esquerda",\r\n
DlgLnkPopTop\t\t: "Posición dende Arriba",\r\n
\r\n
DlnLnkMsgNoUrl\t\t: "Por favor, escriba a ligazón URL",\r\n
DlnLnkMsgNoEMail\t: "Por favor, escriba o enderezo de e-mail",\r\n
DlnLnkMsgNoAnchor\t: "Por favor, seleccione un destino",\r\n
DlnLnkMsgInvPopName\t: "The popup name must begin with an alphabetic character and must not contain spaces",\t//MISSING\r\n
\r\n
// Color Dialog\r\n
DlgColorTitle\t\t: "Seleccionar Color",\r\n
DlgColorBtnClear\t: "Nengunha",\r\n
DlgColorHighlight\t: "Destacado",\r\n
DlgColorSelected\t: "Seleccionado",\r\n
\r\n
// Smiley Dialog\r\n
DlgSmileyTitle\t\t: "Inserte un Smiley",\r\n
\r\n
// Special Character Dialog\r\n
DlgSpecialCharTitle\t: "Seleccione Caracter Especial",\r\n
\r\n
// Table Dialog\r\n
DlgTableTitle\t\t: "Propiedades da Táboa",\r\n
DlgTableRows\t\t: "Filas",\r\n
DlgTableColumns\t\t: "Columnas",\r\n
DlgTableBorder\t\t: "Tamaño do Borde",\r\n
DlgTableAlign\t\t: "Aliñamento",\r\n
DlgTableAlignNotSet\t: "<Non Definido>",\r\n
DlgTableAlignLeft\t: "Esquerda",\r\n
DlgTableAlignCenter\t: "Centro",\r\n
DlgTableAlignRight\t: "Ereita",\r\n
DlgTableWidth\t\t: "Largura",\r\n
DlgTableWidthPx\t\t: "pixels",\r\n
DlgTableWidthPc\t\t: "percent",\r\n
DlgTableHeight\t\t: "Altura",\r\n
DlgTableCellSpace\t: "Marxe entre Celas",\r\n
DlgTableCellPad\t\t: "Marxe interior",\r\n
DlgTableCaption\t\t: "Título",\r\n
DlgTableSummary\t\t: "Sumario",\r\n
DlgTableHeaders\t\t: "Headers",\t//MISSING\r\n
DlgTableHeadersNone\t\t: "None",\t//MISSING\r\n
DlgTableHeadersColumn\t: "First column",\t//MISSING\r\n
DlgTableHeadersRow\t\t: "First Row",\t//MISSING\r\n
DlgTableHeadersBoth\t\t: "Both",\t//MISSING\r\n
\r\n
// Table Cell Dialog\r\n
DlgCellTitle\t\t: "Propriedades da Cela",\r\n
DlgCellWidth\t\t: "Largura",\r\n
DlgCellWidthPx\t\t: "pixels",\r\n
DlgCellWidthPc\t\t: "percent",\r\n
DlgCellHeight\t\t: "Altura",\r\n
DlgCellWordWrap\t\t: "Axustar Liñas",\r\n
DlgCellWordWrapNotSet\t: "<Non Definido>",\r\n
DlgCellWordWrapYes\t: "Si",\r\n
DlgCellWordWrapNo\t: "Non",\r\n
DlgCellHorAlign\t\t: "Aliñamento Horizontal",\r\n
DlgCellHorAlignNotSet\t: "<Non definido>",\r\n
DlgCellHorAlignLeft\t: "Esquerda",\r\n
DlgCellHorAlignCenter\t: "Centro",\r\n
DlgCellHorAlignRight: "Dereita",\r\n
DlgCellVerAlign\t\t: "Aliñamento Vertical",\r\n
DlgCellVerAlignNotSet\t: "<Non definido>",\r\n
DlgCellVerAlignTop\t: "Arriba",\r\n
DlgCellVerAlignMiddle\t: "Medio",\r\n
DlgCellVerAlignBottom\t: "Abaixo",\r\n
DlgCellVerAlignBaseline\t: "Liña de Base",\r\n
DlgCellType\t\t: "Cell Type",\t//MISSING\r\n
DlgCellTypeData\t\t: "Data",\t//MISSING\r\n
DlgCellTypeHeader\t: "Header",\t//MISSING\r\n
DlgCellRowSpan\t\t: "Ocupar Filas",\r\n
DlgCellCollSpan\t\t: "Ocupar Columnas",\r\n
DlgCellBackColor\t: "Color de Fondo",\r\n
DlgCellBorderColor\t: "Color de Borde",\r\n
DlgCellBtnSelect\t: "Seleccionar...",\r\n
\r\n
// Find and Replace Dialog\r\n
DlgFindAndReplaceTitle\t: "Find and Replace",\t//MISSING\r\n
\r\n
// Find Dialog\r\n
DlgFindTitle\t\t: "Procurar",\r\n
DlgFindFindBtn\t\t: "Procurar",\r\n
DlgFindNotFoundMsg\t: "Non te atopou o texto indicado.",\r\n
\r\n
// Replace Dialog\r\n
DlgReplaceTitle\t\t\t: "Substituir",\r\n
DlgReplaceFindLbl\t\t: "Texto a procurar:",\r\n
DlgReplaceReplaceLbl\t: "Substituir con:",\r\n
DlgReplaceCaseChk\t\t: "Coincidir Mai./min.",\r\n
DlgReplaceReplaceBtn\t: "Substituir",\r\n
DlgReplaceReplAllBtn\t: "Substitiur Todo",\r\n
DlgReplaceWordChk\t\t: "Coincidir con toda a palabra",\r\n
\r\n
// Paste Operations / Dialog\r\n
PasteErrorCut\t: "Os axustes de seguridade do seu navegador non permiten que o editor realice automáticamente as tarefas de corte. Por favor, use o teclado para iso (Ctrl+X).",\r\n
PasteErrorCopy\t: "Os axustes de seguridade do seu navegador non permiten que o editor realice automáticamente as tarefas de copia. Por favor, use o teclado para iso (Ctrl+C).",\r\n
\r\n
PasteAsText\t\t: "Pegar como texto plano",\r\n
PasteFromWord\t: "Pegar dende Word",\r\n
\r\n
DlgPasteMsg2\t: "Por favor, pegue dentro do seguinte cadro usando o teclado (<STRONG>Ctrl+V</STRONG>) e pulse <STRONG>OK</STRONG>.",\r\n
DlgPasteSec\t\t: "Because of your browser security settings, the editor is not able to access your clipboard data directly. You are required to paste it again in this window.",\t//MISSING\r\n
DlgPasteIgnoreFont\t\t: "Ignorar as definicións de Tipografía",\r\n
DlgPasteRemoveStyles\t: "Eliminar as definicións de Estilos",\r\n
\r\n
// Color Picker\r\n
ColorAutomatic\t: "Automático",\r\n
ColorMoreColors\t: "Máis Cores...",\r\n
\r\n
// Document Properties\r\n
DocProps\t\t: "Propriedades do Documento",\r\n
\r\n
// Anchor Dialog\r\n
DlgAnchorTitle\t\t: "Propriedades da Referencia",\r\n
DlgAnchorName\t\t: "Nome da Referencia",\r\n
DlgAnchorErrorName\t: "Por favor, escriba o nome da referencia",\r\n
\r\n
// Speller Pages Dialog\r\n
DlgSpellNotInDic\t\t: "Non está no diccionario",\r\n
DlgSpellChangeTo\t\t: "Cambiar a",\r\n
DlgSpellBtnIgnore\t\t: "Ignorar",\r\n
DlgSpellBtnIgnoreAll\t: "Ignorar Todas",\r\n
DlgSpellBtnReplace\t\t: "Substituir",\r\n
DlgSpellBtnReplaceAll\t: "Substituir Todas",\r\n
DlgSpellBtnUndo\t\t\t: "Desfacer",\r\n
DlgSpellNoSuggestions\t: "- Sen candidatos -",\r\n
DlgSpellProgress\t\t: "Corrección ortográfica en progreso...",\r\n
DlgSpellNoMispell\t\t: "Corrección ortográfica rematada: Non se atoparon erros",\r\n
DlgSpellNoChanges\t\t: "Corrección ortográfica rematada: Non se substituiu nengunha verba",\r\n
DlgSpellOneChange\t\t: "Corrección ortográfica rematada: Unha verba substituida",\r\n
DlgSpellManyChanges\t\t: "Corrección ortográfica rematada: %1 verbas substituidas",\r\n
\r\n
IeSpellDownload\t\t\t: "O corrector ortográfico non está instalado. ¿Quere descargalo agora?",\r\n
\r\n
// Button Dialog\r\n
DlgButtonText\t\t: "Texto (Valor)",\r\n
DlgButtonType\t\t: "Tipo",\r\n
DlgButtonTypeBtn\t: "Button",\t//MISSING\r\n
DlgButtonTypeSbm\t: "Submit",\t//MISSING\r\n
DlgButtonTypeRst\t: "Reset",\t//MISSING\r\n
\r\n
// Checkbox and Radio Button Dialogs\r\n
DlgCheckboxName\t\t: "Nome",\r\n
DlgCheckboxValue\t: "Valor",\r\n
DlgCheckboxSelected\t: "Seleccionado",\r\n
\r\n
// Form Dialog\r\n
DlgFormName\t\t: "Nome",\r\n
DlgFormAction\t: "Acción",\r\n
DlgFormMethod\t: "Método",\r\n
\r\n
// Select Field Dialog\r\n
DlgSelectName\t\t: "Nome",\r\n
DlgSelectValue\t\t: "Valor",\r\n
DlgSelectSize\t\t: "Tamaño",\r\n
DlgSelectLines\t\t: "liñas",\r\n
DlgSelectChkMulti\t: "Permitir múltiples seleccións",\r\n
DlgSelectOpAvail\t: "Opcións Disponibles",\r\n
DlgSelectOpText\t\t: "Texto",\r\n
DlgSelectOpValue\t: "Valor",\r\n
DlgSelectBtnAdd\t\t: "Engadir",\r\n
DlgSelectBtnModify\t: "Modificar",\r\n
DlgSelectBtnUp\t\t: "Subir",\r\n
DlgSelectBtnDown\t: "Baixar",\r\n
DlgSelectBtnSetValue : "Definir como valor por defecto",\r\n
DlgSelectBtnDelete\t: "Borrar",\r\n
\r\n
// Textarea Dialog\r\n
DlgTextareaName\t: "Nome",\r\n
DlgTextareaCols\t: "Columnas",\r\n
DlgTextareaRows\t: "Filas",\r\n
\r\n
// Text Field Dialog\r\n
DlgTextName\t\t\t: "Nome",\r\n
DlgTextValue\t\t: "Valor",\r\n
DlgTextCharWidth\t: "Tamaño do Caracter",\r\n
DlgTextMaxChars\t\t: "Máximo de Caracteres",\r\n
DlgTextType\t\t\t: "Tipo",\r\n
DlgTextTypeText\t\t: "Texto",\r\n
DlgTextTypePass\t\t: "Chave",\r\n
\r\n
// Hidden Field Dialog\r\n
DlgHiddenName\t: "Nome",\r\n
DlgHiddenValue\t: "Valor",\r\n
\r\n
// Bulleted List Dialog\r\n
BulletedListProp\t: "Propriedades das Marcas",\r\n
NumberedListProp\t: "Propriedades da Lista de Numeración",\r\n
DlgLstStart\t\t\t: "Start",\t//MISSING\r\n
DlgLstType\t\t\t: "Tipo",\r\n
DlgLstTypeCircle\t: "Círculo",\r\n
DlgLstTypeDisc\t\t: "Disco",\r\n
DlgLstTypeSquare\t: "Cuadrado",\r\n
DlgLstTypeNumbers\t: "Números (1, 2, 3)",\r\n
DlgLstTypeLCase\t\t: "Letras Minúsculas (a, b, c)",\r\n
DlgLstTypeUCase\t\t: "Letras Maiúsculas (A, B, C)",\r\n
DlgLstTypeSRoman\t: "Números Romanos en minúscula (i, ii, iii)",\r\n
DlgLstTypeLRoman\t: "Números Romanos en Maiúscula (I, II, III)",\r\n
\r\n
// Document Properties Dialog\r\n
DlgDocGeneralTab\t: "Xeral",\r\n
DlgDocBackTab\t\t: "Fondo",\r\n
DlgDocColorsTab\t\t: "Cores e Marxes",\r\n
DlgDocMetaTab\t\t: "Meta Data",\r\n
\r\n
DlgDocPageTitle\t\t: "Título da Páxina",\r\n
DlgDocLangDir\t\t: "Orientación do Idioma",\r\n
DlgDocLangDirLTR\t: "Esquerda a Dereita (LTR)",\r\n
DlgDocLangDirRTL\t: "Dereita a Esquerda (RTL)",\r\n
DlgDocLangCode\t\t: "Código de Idioma",\r\n
DlgDocCharSet\t\t: "Codificación do Xogo de Caracteres",\r\n
DlgDocCharSetCE\t\t: "Central European",\t//MISSING\r\n
DlgDocCharSetCT\t\t: "Chinese Traditional (Big5)",\t//MISSING\r\n
DlgDocCharSetCR\t\t: "Cyrillic",\t//MISSING\r\n
DlgDocCharSetGR\t\t: "Greek",\t//MISSING\r\n
DlgDocCharSetJP\t\t: "Japanese",\t//MISSING\r\n
DlgDocCharSetKR\t\t: "Korean",\t//MISSING\r\n
DlgDocCharSetTR\t\t: "Turkish",\t//MISSING\r\n
DlgDocCharSetUN\t\t: "Unicode (UTF-8)",\t//MISSING\r\n
DlgDocCharSetWE\t\t: "Western European",\t//MISSING\r\n
DlgDocCharSetOther\t: "Outra Codificación do Xogo de Caracteres",\r\n
\r\n
DlgDocDocType\t\t: "Encabezado do Tipo de Documento",\r\n
DlgDocDocTypeOther\t: "Outro Encabezado do Tipo de Documento",\r\n
DlgDocIncXHTML\t\t: "Incluir Declaracións XHTML",\r\n
DlgDocBgColor\t\t: "Cor de Fondo",\r\n
DlgDocBgImage\t\t: "URL da Imaxe de Fondo",\r\n
DlgDocBgNoScroll\t: "Fondo Fixo",\r\n
DlgDocCText\t\t\t: "Texto",\r\n
DlgDocCLink\t\t\t: "Ligazóns",\r\n
DlgDocCVisited\t\t: "Ligazón Visitada",\r\n
DlgDocCActive\t\t: "Ligazón Activa",\r\n
DlgDocMargins\t\t: "Marxes da Páxina",\r\n
DlgDocMaTop\t\t\t: "Arriba",\r\n
DlgDocMaLeft\t\t: "Esquerda",\r\n
DlgDocMaRight\t\t: "Dereita",\r\n
DlgDocMaBottom\t\t: "Abaixo",\r\n
DlgDocMeIndex\t\t: "Palabras Chave de Indexación do Documento (separadas por comas)",\r\n
DlgDocMeDescr\t\t: "Descripción do Documento",\r\n
DlgDocMeAuthor\t\t: "Autor",\r\n
DlgDocMeCopy\t\t: "Copyright",\r\n
DlgDocPreview\t\t: "Vista Previa",\r\n
\r\n
// Templates Dialog\r\n
Templates\t\t\t: "Plantillas",\r\n
DlgTemplatesTitle\t: "Plantillas de Contido",\r\n
DlgTemplatesSelMsg\t: "Por favor, seleccione a plantilla a abrir no editor<br>(o contido actual perderase):",\r\n
DlgTemplatesLoading\t: "Cargando listado de plantillas. Por favor, espere...",\r\n
DlgTemplatesNoTpl\t: "(Non hai plantillas definidas)",\r\n
DlgTemplatesReplace\t: "Replace actual contents",\t//MISSING\r\n
\r\n
// About Dialog\r\n
DlgAboutAboutTab\t: "Acerca de",\r\n
DlgAboutBrowserInfoTab\t: "Información do Navegador",\r\n
DlgAboutLicenseTab\t: "Licencia",\r\n
DlgAboutVersion\t\t: "versión",\r\n
DlgAboutInfo\t\t: "Para máis información visitar:",\r\n
\r\n
// Div Dialog\r\n
DlgDivGeneralTab\t: "General",\t//MISSING\r\n
DlgDivAdvancedTab\t: "Advanced",\t//MISSING\r\n
DlgDivStyle\t\t: "Style",\t//MISSING\r\n
DlgDivInlineStyle\t: "Inline Style",\t//MISSING\r\n
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
            <value> <int>20000</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
