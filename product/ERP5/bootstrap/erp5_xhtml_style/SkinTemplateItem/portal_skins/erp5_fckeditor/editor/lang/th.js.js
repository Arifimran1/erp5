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
            <value> <string>th.js</string> </value>
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
 * Thai language file.\r\n
 */\r\n
\r\n
var FCKLang =\r\n
{\r\n
// Language direction : "ltr" (left to right) or "rtl" (right to left).\r\n
Dir\t\t\t\t\t: "ltr",\r\n
\r\n
ToolbarCollapse\t\t: "ซ่อนแถบเครื่องมือ",\r\n
ToolbarExpand\t\t: "แสดงแถบเครื่องมือ",\r\n
\r\n
// Toolbar Items and Context Menu\r\n
Save\t\t\t\t: "บันทึก",\r\n
NewPage\t\t\t\t: "สร้างหน้าเอกสารใหม่",\r\n
Preview\t\t\t\t: "ดูหน้าเอกสารตัวอย่าง",\r\n
Cut\t\t\t\t\t: "ตัด",\r\n
Copy\t\t\t\t: "สำเนา",\r\n
Paste\t\t\t\t: "วาง",\r\n
PasteText\t\t\t: "วางสำเนาจากตัวอักษรธรรมดา",\r\n
PasteWord\t\t\t: "วางสำเนาจากตัวอักษรเวิร์ด",\r\n
Print\t\t\t\t: "สั่งพิมพ์",\r\n
SelectAll\t\t\t: "เลือกทั้งหมด",\r\n
RemoveFormat\t\t: "ล้างรูปแบบ",\r\n
InsertLinkLbl\t\t: "ลิงค์เชื่อมโยงเว็บ อีเมล์ รูปภาพ หรือไฟล์อื่นๆ",\r\n
InsertLink\t\t\t: "แทรก/แก้ไข ลิงค์",\r\n
RemoveLink\t\t\t: "ลบ ลิงค์",\r\n
VisitLink\t\t\t: "Open Link",\t//MISSING\r\n
Anchor\t\t\t\t: "แทรก/แก้ไข Anchor",\r\n
AnchorDelete\t\t: "Remove Anchor",\t//MISSING\r\n
InsertImageLbl\t\t: "รูปภาพ",\r\n
InsertImage\t\t\t: "แทรก/แก้ไข รูปภาพ",\r\n
InsertFlashLbl\t\t: "ไฟล์ Flash",\r\n
InsertFlash\t\t\t: "แทรก/แก้ไข ไฟล์ Flash",\r\n
InsertTableLbl\t\t: "ตาราง",\r\n
InsertTable\t\t\t: "แทรก/แก้ไข ตาราง",\r\n
InsertLineLbl\t\t: "เส้นคั่นบรรทัด",\r\n
InsertLine\t\t\t: "แทรกเส้นคั่นบรรทัด",\r\n
InsertSpecialCharLbl: "ตัวอักษรพิเศษ",\r\n
InsertSpecialChar\t: "แทรกตัวอักษรพิเศษ",\r\n
InsertSmileyLbl\t\t: "รูปสื่ออารมณ์",\r\n
InsertSmiley\t\t: "แทรกรูปสื่ออารมณ์",\r\n
About\t\t\t\t: "เกี่ยวกับโปรแกรม FCKeditor",\r\n
Bold\t\t\t\t: "ตัวหนา",\r\n
Italic\t\t\t\t: "ตัวเอียง",\r\n
Underline\t\t\t: "ตัวขีดเส้นใต้",\r\n
StrikeThrough\t\t: "ตัวขีดเส้นทับ",\r\n
Subscript\t\t\t: "ตัวห้อย",\r\n
Superscript\t\t\t: "ตัวยก",\r\n
LeftJustify\t\t\t: "จัดชิดซ้าย",\r\n
CenterJustify\t\t: "จัดกึ่งกลาง",\r\n
RightJustify\t\t: "จัดชิดขวา",\r\n
BlockJustify\t\t: "จัดพอดีหน้ากระดาษ",\r\n
DecreaseIndent\t\t: "ลดระยะย่อหน้า",\r\n
IncreaseIndent\t\t: "เพิ่มระยะย่อหน้า",\r\n
Blockquote\t\t\t: "Blockquote",\t//MISSING\r\n
CreateDiv\t\t\t: "Create Div Container",\t//MISSING\r\n
EditDiv\t\t\t\t: "Edit Div Container",\t//MISSING\r\n
DeleteDiv\t\t\t: "Remove Div Container",\t//MISSING\r\n
Undo\t\t\t\t: "ยกเลิกคำสั่ง",\r\n
Redo\t\t\t\t: "ทำซ้ำคำสั่ง",\r\n
NumberedListLbl\t\t: "ลำดับรายการแบบตัวเลข",\r\n
NumberedList\t\t: "แทรก/แก้ไข ลำดับรายการแบบตัวเลข",\r\n
BulletedListLbl\t\t: "ลำดับรายการแบบสัญลักษณ์",\r\n
BulletedList\t\t: "แทรก/แก้ไข ลำดับรายการแบบสัญลักษณ์",\r\n
ShowTableBorders\t: "แสดงขอบของตาราง",\r\n
ShowDetails\t\t\t: "แสดงรายละเอียด",\r\n
Style\t\t\t\t: "ลักษณะ",\r\n
FontFormat\t\t\t: "รูปแบบ",\r\n
Font\t\t\t\t: "แบบอักษร",\r\n
FontSize\t\t\t: "ขนาด",\r\n
TextColor\t\t\t: "สีตัวอักษร",\r\n
BGColor\t\t\t\t: "สีพื้นหลัง",\r\n
Source\t\t\t\t: "ดูรหัส HTML",\r\n
Find\t\t\t\t: "ค้นหา",\r\n
Replace\t\t\t\t: "ค้นหาและแทนที่",\r\n
SpellCheck\t\t\t: "ตรวจการสะกดคำ",\r\n
UniversalKeyboard\t: "คีย์บอร์ดหลากภาษา",\r\n
PageBreakLbl\t\t: "ใส่ตัวแบ่งหน้า Page Break",\r\n
PageBreak\t\t\t: "แทรกตัวแบ่งหน้า Page Break",\r\n
\r\n
Form\t\t\t: "แบบฟอร์ม",\r\n
Checkbox\t\t: "เช็คบ๊อก",\r\n
RadioButton\t\t: "เรดิโอบัตตอน",\r\n
TextField\t\t: "เท็กซ์ฟิลด์",\r\n
Textarea\t\t: "เท็กซ์แอเรีย",\r\n
HiddenField\t\t: "ฮิดเดนฟิลด์",\r\n
Button\t\t\t: "ปุ่ม",\r\n
SelectionField\t: "แถบตัวเลือก",\r\n
ImageButton\t\t: "ปุ่มแบบรูปภาพ",\r\n
\r\n
FitWindow\t\t: "ขยายขนาดตัวอีดิตเตอร์",\r\n
ShowBlocks\t\t: "Show Blocks",\t//MISSING\r\n
\r\n
// Context Menu\r\n
EditLink\t\t\t: "แก้ไข ลิงค์",\r\n
CellCM\t\t\t\t: "ช่องตาราง",\r\n
RowCM\t\t\t\t: "แถว",\r\n
ColumnCM\t\t\t: "คอลัมน์",\r\n
InsertRowAfter\t\t: "Insert Row After",\t//MISSING\r\n
InsertRowBefore\t\t: "Insert Row Before",\t//MISSING\r\n
DeleteRows\t\t\t: "ลบแถว",\r\n
InsertColumnAfter\t: "Insert Column After",\t//MISSING\r\n
InsertColumnBefore\t: "Insert Column Before",\t//MISSING\r\n
DeleteColumns\t\t: "ลบสดมน์",\r\n
InsertCellAfter\t\t: "Insert Cell After",\t//MISSING\r\n
InsertCellBefore\t: "Insert Cell Before",\t//MISSING\r\n
DeleteCells\t\t\t: "ลบช่อง",\r\n
MergeCells\t\t\t: "ผสานช่อง",\r\n
MergeRight\t\t\t: "Merge Right",\t//MISSING\r\n
MergeDown\t\t\t: "Merge Down",\t//MISSING\r\n
HorizontalSplitCell\t: "Split Cell Horizontally",\t//MISSING\r\n
VerticalSplitCell\t: "Split Cell Vertically",\t//MISSING\r\n
TableDelete\t\t\t: "ลบตาราง",\r\n
CellProperties\t\t: "คุณสมบัติของช่อง",\r\n
TableProperties\t\t: "คุณสมบัติของตาราง",\r\n
ImageProperties\t\t: "คุณสมบัติของรูปภาพ",\r\n
FlashProperties\t\t: "คุณสมบัติของไฟล์ Flash",\r\n
\r\n
AnchorProp\t\t\t: "รายละเอียด Anchor",\r\n
ButtonProp\t\t\t: "รายละเอียดของ ปุ่ม",\r\n
CheckboxProp\t\t: "คุณสมบัติของ เช็คบ๊อก",\r\n
HiddenFieldProp\t\t: "คุณสมบัติของ ฮิดเดนฟิลด์",\r\n
RadioButtonProp\t\t: "คุณสมบัติของ เรดิโอบัตตอน",\r\n
ImageButtonProp\t\t: "คุณสมบัติของ ปุ่มแบบรูปภาพ",\r\n
TextFieldProp\t\t: "คุณสมบัติของ เท็กซ์ฟิลด์",\r\n
SelectionFieldProp\t: "คุณสมบัติของ แถบตัวเลือก",\r\n
TextareaProp\t\t: "คุณสมบัติของ เท็กแอเรีย",\r\n
FormProp\t\t\t: "คุณสมบัติของ แบบฟอร์ม",\r\n
\r\n
FontFormats\t\t\t: "Normal;Formatted;Address;Heading 1;Heading 2;Heading 3;Heading 4;Heading 5;Heading 6;Paragraph (DIV)",\r\n
\r\n
// Alerts and Messages\r\n
ProcessingXHTML\t\t: "โปรแกรมกำลังทำงานด้วยเทคโนโลยี XHTML กรุณารอสักครู่...",\r\n
Done\t\t\t\t: "โปรแกรมทำงานเสร็จสมบูรณ์",\r\n
PasteWordConfirm\t: "ข้อมูลที่ท่านต้องการวางลงในแผ่นงาน ถูกจัดรูปแบบจากโปรแกรมเวิร์ด. ท่านต้องการล้างรูปแบบที่มาจากโปรแกรมเวิร์ดหรือไม่?",\r\n
NotCompatiblePaste\t: "คำสั่งนี้ทำงานในโปรแกรมท่องเว็บ Internet Explorer version รุ่น 5.5 หรือใหม่กว่าเท่านั้น. ท่านต้องการวางตัวอักษรโดยไม่ล้างรูปแบบที่มาจากโปรแกรมเวิร์ดหรือไม่?",\r\n
UnknownToolbarItem\t: "ไม่สามารถระบุปุ่มเครื่องมือได้ \\"%1\\"",\r\n
UnknownCommand\t\t: "ไม่สามารถระบุชื่อคำสั่งได้ \\"%1\\"",\r\n
NotImplemented\t\t: "ไม่สามารถใช้งานคำสั่งได้",\r\n
UnknownToolbarSet\t: "ไม่มีการติดตั้งชุดคำสั่งในแถบเครื่องมือ \\"%1\\" กรุณาติดต่อผู้ดูแลระบบ",\r\n
NoActiveX\t\t\t: "โปรแกรมท่องอินเตอร์เน็ตของท่านไม่อนุญาติให้อีดิตเตอร์ทำงาน \\"Run ActiveX controls and plug-ins\\". หากไม่อนุญาติให้ใช้งาน ActiveX controls ท่านจะไม่สามารถใช้งานได้อย่างเต็มประสิทธิภาพ.",\r\n
BrowseServerBlocked : "เปิดหน้าต่างป๊อบอัพเพื่อทำงานต่อไม่ได้ กรุณาปิดเครื่องมือป้องกันป๊อบอัพในโปรแกรมท่องอินเตอร์เน็ตของท่านด้วย",\r\n
DialogBlocked\t\t: "เปิดหน้าต่างป๊อบอัพเพื่อทำงานต่อไม่ได้ กรุณาปิดเครื่องมือป้องกันป๊อบอัพในโปรแกรมท่องอินเตอร์เน็ตของท่านด้วย",\r\n
VisitLinkBlocked\t: "It was not possible to open a new window. Make sure all popup blockers are disabled.",\t//MISSING\r\n
\r\n
// Dialogs\r\n
DlgBtnOK\t\t\t: "ตกลง",\r\n
DlgBtnCancel\t\t: "ยกเลิก",\r\n
DlgBtnClose\t\t\t: "ปิด",\r\n
DlgBtnBrowseServer\t: "เปิดหน้าต่างจัดการไฟล์อัพโหลด",\r\n
DlgAdvancedTag\t\t: "ขั้นสูง",\r\n
DlgOpOther\t\t\t: "<อื่นๆ>",\r\n
DlgInfoTab\t\t\t: "อินโฟ",\r\n
DlgAlertUrl\t\t\t: "กรุณาระบุ URL",\r\n
\r\n
// General Dialogs Labels\r\n
DlgGenNotSet\t\t: "<ไม่ระบุ>",\r\n
DlgGenId\t\t\t: "ไอดี",\r\n
DlgGenLangDir\t\t: "การเขียน-อ่านภาษา",\r\n
DlgGenLangDirLtr\t: "จากซ้ายไปขวา (LTR)",\r\n
DlgGenLangDirRtl\t: "จากขวามาซ้าย (RTL)",\r\n
DlgGenLangCode\t\t: "รหัสภาษา",\r\n
DlgGenAccessKey\t\t: "แอคเซส คีย์",\r\n
DlgGenName\t\t\t: "ชื่อ",\r\n
DlgGenTabIndex\t\t: "ลำดับของ แท็บ",\r\n
DlgGenLongDescr\t\t: "คำอธิบายประกอบ URL",\r\n
DlgGenClass\t\t\t: "คลาสของไฟล์กำหนดลักษณะการแสดงผล",\r\n
DlgGenTitle\t\t\t: "คำเกริ่นนำ",\r\n
DlgGenContType\t\t: "ชนิดของคำเกริ่นนำ",\r\n
DlgGenLinkCharset\t: "ลิงค์เชื่อมโยงไปยังชุดตัวอักษร",\r\n
DlgGenStyle\t\t\t: "ลักษณะการแสดงผล",\r\n
\r\n
// Image Dialog\r\n
DlgImgTitle\t\t\t: "คุณสมบัติของ รูปภาพ",\r\n
DlgImgInfoTab\t\t: "ข้อมูลของรูปภาพ",\r\n
DlgImgBtnUpload\t\t: "อัพโหลดไฟล์ไปเก็บไว้ที่เครื่องแม่ข่าย (เซิร์ฟเวอร์)",\r\n
DlgImgURL\t\t\t: "ที่อยู่อ้างอิง URL",\r\n
DlgImgUpload\t\t: "อัพโหลดไฟล์",\r\n
DlgImgAlt\t\t\t: "คำประกอบรูปภาพ",\r\n
DlgImgWidth\t\t\t: "ความกว้าง",\r\n
DlgImgHeight\t\t: "ความสูง",\r\n
DlgImgLockRatio\t\t: "กำหนดอัตราส่วน กว้าง-สูง แบบคงที่",\r\n
DlgBtnResetSize\t\t: "กำหนดรูปเท่าขนาดจริง",\r\n
DlgImgBorder\t\t: "ขนาดขอบรูป",\r\n
DlgImgHSpace\t\t: "ระยะแนวนอน",\r\n
DlgImgVSpace\t\t: "ระยะแนวตั้ง",\r\n
DlgImgAlign\t\t\t: "การจัดวาง",\r\n
DlgImgAlignLeft\t\t: "ชิดซ้าย",\r\n
DlgImgAlignAbsBottom: "ชิดด้านล่างสุด",\r\n
DlgImgAlignAbsMiddle: "กึ่งกลาง",\r\n
DlgImgAlignBaseline\t: "ชิดบรรทัด",\r\n
DlgImgAlignBottom\t: "ชิดด้านล่าง",\r\n
DlgImgAlignMiddle\t: "กึ่งกลางแนวตั้ง",\r\n
DlgImgAlignRight\t: "ชิดขวา",\r\n
DlgImgAlignTextTop\t: "ใต้ตัวอักษร",\r\n
DlgImgAlignTop\t\t: "บนสุด",\r\n
DlgImgPreview\t\t: "หน้าเอกสารตัวอย่าง",\r\n
DlgImgAlertUrl\t\t: "กรุณาระบุที่อยู่อ้างอิงออนไลน์ของไฟล์รูปภาพ (URL)",\r\n
DlgImgLinkTab\t\t: "ลิ้งค์",\r\n
\r\n
// Flash Dialog\r\n
DlgFlashTitle\t\t: "คุณสมบัติของไฟล์ Flash",\r\n
DlgFlashChkPlay\t\t: "เล่นอัตโนมัติ Auto Play",\r\n
DlgFlashChkLoop\t\t: "เล่นวนรอบ Loop",\r\n
DlgFlashChkMenu\t\t: "ให้ใช้งานเมนูของ Flash",\r\n
DlgFlashScale\t\t: "อัตราส่วน Scale",\r\n
DlgFlashScaleAll\t: "แสดงให้เห็นทั้งหมด Show all",\r\n
DlgFlashScaleNoBorder\t: "ไม่แสดงเส้นขอบ No Border",\r\n
DlgFlashScaleFit\t: "แสดงให้พอดีกับพื้นที่ Exact Fit",\r\n
\r\n
// Link Dialog\r\n
DlgLnkWindowTitle\t: "ลิงค์เชื่อมโยงเว็บ อีเมล์ รูปภาพ หรือไฟล์อื่นๆ",\r\n
DlgLnkInfoTab\t\t: "รายละเอียด",\r\n
DlgLnkTargetTab\t\t: "การเปิดหน้าจอ",\r\n
\r\n
DlgLnkType\t\t\t: "ประเภทของลิงค์",\r\n
DlgLnkTypeURL\t\t: "ที่อยู่อ้างอิงออนไลน์ (URL)",\r\n
DlgLnkTypeAnchor\t: "จุดเชื่อมโยง (Anchor)",\r\n
DlgLnkTypeEMail\t\t: "ส่งอีเมล์ (E-Mail)",\r\n
DlgLnkProto\t\t\t: "โปรโตคอล",\r\n
DlgLnkProtoOther\t: "<อื่นๆ>",\r\n
DlgLnkURL\t\t\t: "ที่อยู่อ้างอิงออนไลน์ (URL)",\r\n
DlgLnkAnchorSel\t\t: "ระบุข้อมูลของจุดเชื่อมโยง (Anchor)",\r\n
DlgLnkAnchorByName\t: "ชื่อ",\r\n
DlgLnkAnchorById\t: "ไอดี",\r\n
DlgLnkNoAnchors\t\t: "(ยังไม่มีจุดเชื่อมโยงภายในหน้าเอกสารนี้)",\r\n
DlgLnkEMail\t\t\t: "อีเมล์ (E-Mail)",\r\n
DlgLnkEMailSubject\t: "หัวเรื่อง",\r\n
DlgLnkEMailBody\t\t: "ข้อความ",\r\n
DlgLnkUpload\t\t: "อัพโหลดไฟล์",\r\n
DlgLnkBtnUpload\t\t: "บันทึกไฟล์ไว้บนเซิร์ฟเวอร์",\r\n
\r\n
DlgLnkTarget\t\t: "การเปิดหน้าลิงค์",\r\n
DlgLnkTargetFrame\t: "<เปิดในเฟรม>",\r\n
DlgLnkTargetPopup\t: "<เปิดหน้าจอเล็ก (Pop-up)>",\r\n
DlgLnkTargetBlank\t: "เปิดหน้าจอใหม่ (_blank)",\r\n
DlgLnkTargetParent\t: "เปิดในหน้าหลัก (_parent)",\r\n
DlgLnkTargetSelf\t: "เปิดในหน้าปัจจุบัน (_self)",\r\n
DlgLnkTargetTop\t\t: "เปิดในหน้าบนสุด (_top)",\r\n
DlgLnkTargetFrameName\t: "ชื่อทาร์เก็ตเฟรม",\r\n
DlgLnkPopWinName\t: "ระบุชื่อหน้าจอเล็ก (Pop-up)",\r\n
DlgLnkPopWinFeat\t: "คุณสมบัติของหน้าจอเล็ก (Pop-up)",\r\n
DlgLnkPopResize\t\t: "ปรับขนาดหน้าจอ",\r\n
DlgLnkPopLocation\t: "แสดงที่อยู่ของไฟล์",\r\n
DlgLnkPopMenu\t\t: "แสดงแถบเมนู",\r\n
DlgLnkPopScroll\t\t: "แสดงแถบเลื่อน",\r\n
DlgLnkPopStatus\t\t: "แสดงแถบสถานะ",\r\n
DlgLnkPopToolbar\t: "แสดงแถบเครื่องมือ",\r\n
DlgLnkPopFullScrn\t: "แสดงเต็มหน้าจอ (IE5.5++ เท่านั้น)",\r\n
DlgLnkPopDependent\t: "แสดงเต็มหน้าจอ (Netscape)",\r\n
DlgLnkPopWidth\t\t: "กว้าง",\r\n
DlgLnkPopHeight\t\t: "สูง",\r\n
DlgLnkPopLeft\t\t: "พิกัดซ้าย (Left Position)",\r\n
DlgLnkPopTop\t\t: "พิกัดบน (Top Position)",\r\n
\r\n
DlnLnkMsgNoUrl\t\t: "กรุณาระบุที่อยู่อ้างอิงออนไลน์ (URL)",\r\n
DlnLnkMsgNoEMail\t: "กรุณาระบุอีเมล์ (E-mail)",\r\n
DlnLnkMsgNoAnchor\t: "กรุณาระบุจุดเชื่อมโยง (Anchor)",\r\n
DlnLnkMsgInvPopName\t: "ชื่อของหน้าต่างป๊อบอัพ จะต้องขึ้นต้นด้วยตัวอักษรเท่านั้น และต้องไม่มีช่องว่างในชื่อ",\r\n
\r\n
// Color Dialog\r\n
DlgColorTitle\t\t: "เลือกสี",\r\n
DlgColorBtnClear\t: "ล้างค่ารหัสสี",\r\n
DlgColorHighlight\t: "ตัวอย่างสี",\r\n
DlgColorSelected\t: "สีที่เลือก",\r\n
\r\n
// Smiley Dialog\r\n
DlgSmileyTitle\t\t: "แทรกสัญลักษณ์สื่ออารมณ์",\r\n
\r\n
// Special Character Dialog\r\n
DlgSpecialCharTitle\t: "แทรกตัวอักษรพิเศษ",\r\n
\r\n
// Table Dialog\r\n
DlgTableTitle\t\t: "คุณสมบัติของ ตาราง",\r\n
DlgTableRows\t\t: "แถว",\r\n
DlgTableColumns\t\t: "สดมน์",\r\n
DlgTableBorder\t\t: "ขนาดเส้นขอบ",\r\n
DlgTableAlign\t\t: "การจัดตำแหน่ง",\r\n
DlgTableAlignNotSet\t: "<ไม่ระบุ>",\r\n
DlgTableAlignLeft\t: "ชิดซ้าย",\r\n
DlgTableAlignCenter\t: "กึ่งกลาง",\r\n
DlgTableAlignRight\t: "ชิดขวา",\r\n
DlgTableWidth\t\t: "กว้าง",\r\n
DlgTableWidthPx\t\t: "จุดสี",\r\n
DlgTableWidthPc\t\t: "เปอร์เซ็น",\r\n
DlgTableHeight\t\t: "สูง",\r\n
DlgTableCellSpace\t: "ระยะแนวนอนน",\r\n
DlgTableCellPad\t\t: "ระยะแนวตั้ง",\r\n
DlgTableCaption\t\t: "หัวเรื่องของตาราง",\r\n
DlgTableSummary\t\t: "สรุปความ",\r\n
DlgTableHeaders\t\t: "Headers",\t//MISSING\r\n
DlgTableHeadersNone\t\t: "None",\t//MISSING\r\n
DlgTableHeadersColumn\t: "First column",\t//MISSING\r\n
DlgTableHeadersRow\t\t: "First Row",\t//MISSING\r\n
DlgTableHeadersBoth\t\t: "Both",\t//MISSING\r\n
\r\n
// Table Cell Dialog\r\n
DlgCellTitle\t\t: "คุณสมบัติของ ช่อง",\r\n
DlgCellWidth\t\t: "กว้าง",\r\n
DlgCellWidthPx\t\t: "จุดสี",\r\n
DlgCellWidthPc\t\t: "เปอร์เซ็น",\r\n
DlgCellHeight\t\t: "สูง",\r\n
DlgCellWordWrap\t\t: "ตัดบรรทัดอัตโนมัติ",\r\n
DlgCellWordWrapNotSet\t: "<ไม่ระบุ>",\r\n
DlgCellWordWrapYes\t: "ใ่ช่",\r\n
DlgCellWordWrapNo\t: "ไม่",\r\n
DlgCellHorAlign\t\t: "การจัดวางแนวนอน",\r\n
DlgCellHorAlignNotSet\t: "<ไม่ระบุ>",\r\n
DlgCellHorAlignLeft\t: "ชิดซ้าย",\r\n
DlgCellHorAlignCenter\t: "กึ่งกลาง",\r\n
DlgCellHorAlignRight: "ชิดขวา",\r\n
DlgCellVerAlign\t\t: "การจัดวางแนวตั้ง",\r\n
DlgCellVerAlignNotSet\t: "<ไม่ระบุ>",\r\n
DlgCellVerAlignTop\t: "บนสุด",\r\n
DlgCellVerAlignMiddle\t: "กึ่งกลาง",\r\n
DlgCellVerAlignBottom\t: "ล่างสุด",\r\n
DlgCellVerAlignBaseline\t: "อิงบรรทัด",\r\n
DlgCellType\t\t: "Cell Type",\t//MISSING\r\n
DlgCellTypeData\t\t: "Data",\t//MISSING\r\n
DlgCellTypeHeader\t: "Header",\t//MISSING\r\n
DlgCellRowSpan\t\t: "จำนวนแถวที่คร่อมกัน",\r\n
DlgCellCollSpan\t\t: "จำนวนสดมน์ที่คร่อมกัน",\r\n
DlgCellBackColor\t: "สีพื้นหลัง",\r\n
DlgCellBorderColor\t: "สีเส้นขอบ",\r\n
DlgCellBtnSelect\t: "เลือก..",\r\n
\r\n
// Find and Replace Dialog\r\n
DlgFindAndReplaceTitle\t: "Find and Replace",\t//MISSING\r\n
\r\n
// Find Dialog\r\n
DlgFindTitle\t\t: "ค้นหา",\r\n
DlgFindFindBtn\t\t: "ค้นหา",\r\n
DlgFindNotFoundMsg\t: "ไม่พบคำที่ค้นหา.",\r\n
\r\n
// Replace Dialog\r\n
DlgReplaceTitle\t\t\t: "ค้นหาและแทนที่",\r\n
DlgReplaceFindLbl\t\t: "ค้นหาคำว่า:",\r\n
DlgReplaceReplaceLbl\t: "แทนที่ด้วย:",\r\n
DlgReplaceCaseChk\t\t: "ตัวโหญ่-เล็ก ต้องตรงกัน",\r\n
DlgReplaceReplaceBtn\t: "แทนที่",\r\n
DlgReplaceReplAllBtn\t: "แทนที่ทั้งหมดที่พบ",\r\n
DlgReplaceWordChk\t\t: "ต้องตรงกันทุกคำ",\r\n
\r\n
// Paste Operations / Dialog\r\n
PasteErrorCut\t: "ไม่สามารถตัดข้อความที่เลือกไว้ได้เนื่องจากการกำหนดค่าระดับความปลอดภัย. กรุณาใช้ปุ่มลัดเพื่อวางข้อความแทน (กดปุ่ม Ctrl และตัว X พร้อมกัน).",\r\n
PasteErrorCopy\t: "ไม่สามารถสำเนาข้อความที่เลือกไว้ได้เนื่องจากการกำหนดค่าระดับความปลอดภัย. กรุณาใช้ปุ่มลัดเพื่อวางข้อความแทน (กดปุ่ม Ctrl และตัว C พร้อมกัน).",\r\n
\r\n
PasteAsText\t\t: "วางแบบตัวอักษรธรรมดา",\r\n
PasteFromWord\t: "วางแบบตัวอักษรจากโปรแกรมเวิร์ด",\r\n
\r\n
DlgPasteMsg2\t: "กรุณาใช้คีย์บอร์ดเท่านั้น โดยกดปุ๋ม (<strong>Ctrl และ V</strong>)พร้อมๆกัน และกด <strong>OK</strong>.",\r\n
DlgPasteSec\t\t: "Because of your browser security settings, the editor is not able to access your clipboard data directly. You are required to paste it again in this window.",\t//MISSING\r\n
DlgPasteIgnoreFont\t\t: "ไม่สนใจ Font Face definitions",\r\n
DlgPasteRemoveStyles\t: "ลบ Styles definitions",\r\n
\r\n
// Color Picker\r\n
ColorAutomatic\t: "สีอัตโนมัติ",\r\n
ColorMoreColors\t: "เลือกสีอื่นๆ...",\r\n
\r\n
// Document Properties\r\n
DocProps\t\t: "คุณสมบัติของเอกสาร",\r\n
\r\n
// Anchor Dialog\r\n
DlgAnchorTitle\t\t: "คุณสมบัติของ Anchor",\r\n
DlgAnchorName\t\t: "ชื่อ Anchor",\r\n
DlgAnchorErrorName\t: "กรุณาระบุชื่อของ Anchor",\r\n
\r\n
// Speller Pages Dialog\r\n
DlgSpellNotInDic\t\t: "ไม่พบในดิกชันนารี",\r\n
DlgSpellChangeTo\t\t: "แก้ไขเป็น",\r\n
DlgSpellBtnIgnore\t\t: "ยกเว้น",\r\n
DlgSpellBtnIgnoreAll\t: "ยกเว้นทั้งหมด",\r\n
DlgSpellBtnReplace\t\t: "แทนที่",\r\n
DlgSpellBtnReplaceAll\t: "แทนที่ทั้งหมด",\r\n
DlgSpellBtnUndo\t\t\t: "ยกเลิก",\r\n
DlgSpellNoSuggestions\t: "- ไม่มีคำแนะนำใดๆ -",\r\n
DlgSpellProgress\t\t: "กำลังตรวจสอบคำสะกด...",\r\n
DlgSpellNoMispell\t\t: "ตรวจสอบคำสะกดเสร็จสิ้น: ไม่พบคำสะกดผิด",\r\n
DlgSpellNoChanges\t\t: "ตรวจสอบคำสะกดเสร็จสิ้น: ไม่มีการแก้คำใดๆ",\r\n
DlgSpellOneChange\t\t: "ตรวจสอบคำสะกดเสร็จสิ้น: แก้ไข1คำ",\r\n
DlgSpellManyChanges\t\t: "ตรวจสอบคำสะกดเสร็จสิ้น:: แก้ไข %1 คำ",\r\n
\r\n
IeSpellDownload\t\t\t: "ไม่ได้ติดตั้งระบบตรวจสอบคำสะกด. ต้องการติดตั้งไหมครับ?",\r\n
\r\n
// Button Dialog\r\n
DlgButtonText\t\t: "ข้อความ (ค่าตัวแปร)",\r\n
DlgButtonType\t\t: "ข้อความ",\r\n
DlgButtonTypeBtn\t: "Button",\r\n
DlgButtonTypeSbm\t: "Submit",\r\n
DlgButtonTypeRst\t: "Reset",\r\n
\r\n
// Checkbox and Radio Button Dialogs\r\n
DlgCheckboxName\t\t: "ชื่อ",\r\n
DlgCheckboxValue\t: "ค่าตัวแปร",\r\n
DlgCheckboxSelected\t: "เลือกเป็นค่าเริ่มต้น",\r\n
\r\n
// Form Dialog\r\n
DlgFormName\t\t: "ชื่อ",\r\n
DlgFormAction\t: "แอคชั่น",\r\n
DlgFormMethod\t: "เมธอด",\r\n
\r\n
// Select Field Dialog\r\n
DlgSelectName\t\t: "ชื่อ",\r\n
DlgSelectValue\t\t: "ค่าตัวแปร",\r\n
DlgSelectSize\t\t: "ขนาด",\r\n
DlgSelectLines\t\t: "บรรทัด",\r\n
DlgSelectChkMulti\t: "เลือกหลายค่าได้",\r\n
DlgSelectOpAvail\t: "รายการตัวเลือก",\r\n
DlgSelectOpText\t\t: "ข้อความ",\r\n
DlgSelectOpValue\t: "ค่าตัวแปร",\r\n
DlgSelectBtnAdd\t\t: "เพิ่ม",\r\n
DlgSelectBtnModify\t: "แก้ไข",\r\n
DlgSelectBtnUp\t\t: "บน",\r\n
DlgSelectBtnDown\t: "ล่าง",\r\n
DlgSelectBtnSetValue : "เลือกเป็นค่าเริ่มต้น",\r\n
DlgSelectBtnDelete\t: "ลบ",\r\n
\r\n
// Textarea Dialog\r\n
DlgTextareaName\t: "ชื่อ",\r\n
DlgTextareaCols\t: "สดมภ์",\r\n
DlgTextareaRows\t: "แถว",\r\n
\r\n
// Text Field Dialog\r\n
DlgTextName\t\t\t: "ชื่อ",\r\n
DlgTextValue\t\t: "ค่าตัวแปร",\r\n
DlgTextCharWidth\t: "ความกว้าง",\r\n
DlgTextMaxChars\t\t: "จำนวนตัวอักษรสูงสุด",\r\n
DlgTextType\t\t\t: "ชนิด",\r\n
DlgTextTypeText\t\t: "ข้อความ",\r\n
DlgTextTypePass\t\t: "รหัสผ่าน",\r\n
\r\n
// Hidden Field Dialog\r\n
DlgHiddenName\t: "ชื่อ",\r\n
DlgHiddenValue\t: "ค่าตัวแปร",\r\n
\r\n
// Bulleted List Dialog\r\n
BulletedListProp\t: "คุณสมบัติของ บูลเล็ตลิสต์",\r\n
NumberedListProp\t: "คุณสมบัติของ นัมเบอร์ลิสต์",\r\n
DlgLstStart\t\t\t: "Start",\t//MISSING\r\n
DlgLstType\t\t\t: "ชนิด",\r\n
DlgLstTypeCircle\t: "รูปวงกลม",\r\n
DlgLstTypeDisc\t\t: "Disc",\t//MISSING\r\n
DlgLstTypeSquare\t: "รูปสี่เหลี่ยม",\r\n
DlgLstTypeNumbers\t: "หมายเลข (1, 2, 3)",\r\n
DlgLstTypeLCase\t\t: "ตัวพิมพ์เล็ก (a, b, c)",\r\n
DlgLstTypeUCase\t\t: "ตัวพิมพ์ใหญ่ (A, B, C)",\r\n
DlgLstTypeSRoman\t: "เลขโรมันพิมพ์เล็ก (i, ii, iii)",\r\n
DlgLstTypeLRoman\t: "เลขโรมันพิมพ์ใหญ่ (I, II, III)",\r\n
\r\n
// Document Properties Dialog\r\n
DlgDocGeneralTab\t: "ลักษณะทั่วไปของเอกสาร",\r\n
DlgDocBackTab\t\t: "พื้นหลัง",\r\n
DlgDocColorsTab\t\t: "สีและระยะขอบ",\r\n
DlgDocMetaTab\t\t: "ข้อมูลสำหรับเสิร์ชเอนจิ้น",\r\n
\r\n
DlgDocPageTitle\t\t: "ชื่อไตเติ้ล",\r\n
DlgDocLangDir\t\t: "การอ่านภาษา",\r\n
DlgDocLangDirLTR\t: "จากซ้ายไปขวา (LTR)",\r\n
DlgDocLangDirRTL\t: "จากขวาไปซ้าย (RTL)",\r\n
DlgDocLangCode\t\t: "รหัสภาษา",\r\n
DlgDocCharSet\t\t: "ชุดตัวอักษร",\r\n
DlgDocCharSetCE\t\t: "Central European",\r\n
DlgDocCharSetCT\t\t: "Chinese Traditional (Big5)",\r\n
DlgDocCharSetCR\t\t: "Cyrillic",\r\n
DlgDocCharSetGR\t\t: "Greek",\r\n
DlgDocCharSetJP\t\t: "Japanese",\r\n
DlgDocCharSetKR\t\t: "Korean",\r\n
DlgDocCharSetTR\t\t: "Turkish",\r\n
DlgDocCharSetUN\t\t: "Unicode (UTF-8)",\r\n
DlgDocCharSetWE\t\t: "Western European",\r\n
DlgDocCharSetOther\t: "ชุดตัวอักษรอื่นๆ",\r\n
\r\n
DlgDocDocType\t\t: "ประเภทของเอกสาร",\r\n
DlgDocDocTypeOther\t: "ประเภทเอกสารอื่นๆ",\r\n
DlgDocIncXHTML\t\t: "รวมเอา  XHTML Declarations ไว้ด้วย",\r\n
DlgDocBgColor\t\t: "สีพื้นหลัง",\r\n
DlgDocBgImage\t\t: "ที่อยู่อ้างอิงออนไลน์ของรูปพื้นหลัง (Image URL)",\r\n
DlgDocBgNoScroll\t: "พื้นหลังแบบไม่มีแถบเลื่อน",\r\n
DlgDocCText\t\t\t: "ข้อความ",\r\n
DlgDocCLink\t\t\t: "ลิงค์",\r\n
DlgDocCVisited\t\t: "ลิงค์ที่เคยคลิ้กแล้ว Visited Link",\r\n
DlgDocCActive\t\t: "ลิงค์ที่กำลังคลิ้ก Active Link",\r\n
DlgDocMargins\t\t: "ระยะขอบของหน้าเอกสาร",\r\n
DlgDocMaTop\t\t\t: "ด้านบน",\r\n
DlgDocMaLeft\t\t: "ด้านซ้าย",\r\n
DlgDocMaRight\t\t: "ด้านขวา",\r\n
DlgDocMaBottom\t\t: "ด้านล่าง",\r\n
DlgDocMeIndex\t\t: "คำสำคัญอธิบายเอกสาร (คั่นคำด้วย คอมม่า)",\r\n
DlgDocMeDescr\t\t: "ประโยคอธิบายเกี่ยวกับเอกสาร",\r\n
DlgDocMeAuthor\t\t: "ผู้สร้างเอกสาร",\r\n
DlgDocMeCopy\t\t: "สงวนลิขสิทธิ์",\r\n
DlgDocPreview\t\t: "ตัวอย่างหน้าเอกสาร",\r\n
\r\n
// Templates Dialog\r\n
Templates\t\t\t: "เทมเพลต",\r\n
DlgTemplatesTitle\t: "เทมเพลตของส่วนเนื้อหาเว็บไซต์",\r\n
DlgTemplatesSelMsg\t: "กรุณาเลือก เทมเพลต เพื่อนำไปแก้ไขในอีดิตเตอร์<br />(เนื้อหาส่วนนี้จะหายไป):",\r\n
DlgTemplatesLoading\t: "กำลังโหลดรายการเทมเพลตทั้งหมด...",\r\n
DlgTemplatesNoTpl\t: "(ยังไม่มีการกำหนดเทมเพลต)",\r\n
DlgTemplatesReplace\t: "แทนที่เนื้อหาเว็บไซต์ที่เลือก",\r\n
\r\n
// About Dialog\r\n
DlgAboutAboutTab\t: "เกี่ยวกับโปรแกรม",\r\n
DlgAboutBrowserInfoTab\t: "โปรแกรมท่องเว็บที่ท่านใช้",\r\n
DlgAboutLicenseTab\t: "ลิขสิทธิ์",\r\n
DlgAboutVersion\t\t: "รุ่น",\r\n
DlgAboutInfo\t\t: "For further information go to",\t//MISSING\r\n
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
            <value> <int>31405</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
