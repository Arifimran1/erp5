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
            <value> <string>zh-cn.js</string> </value>
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
 * Chinese Simplified language file.\r\n
 */\r\n
\r\n
var FCKLang =\r\n
{\r\n
// Language direction : "ltr" (left to right) or "rtl" (right to left).\r\n
Dir\t\t\t\t\t: "ltr",\r\n
\r\n
ToolbarCollapse\t\t: "折叠工具栏",\r\n
ToolbarExpand\t\t: "展开工具栏",\r\n
\r\n
// Toolbar Items and Context Menu\r\n
Save\t\t\t\t: "保存",\r\n
NewPage\t\t\t\t: "新建",\r\n
Preview\t\t\t\t: "预览",\r\n
Cut\t\t\t\t\t: "剪切",\r\n
Copy\t\t\t\t: "复制",\r\n
Paste\t\t\t\t: "粘贴",\r\n
PasteText\t\t\t: "粘贴为无格式文本",\r\n
PasteWord\t\t\t: "从 MS Word 粘贴",\r\n
Print\t\t\t\t: "打印",\r\n
SelectAll\t\t\t: "全选",\r\n
RemoveFormat\t\t: "清除格式",\r\n
InsertLinkLbl\t\t: "超链接",\r\n
InsertLink\t\t\t: "插入/编辑超链接",\r\n
RemoveLink\t\t\t: "取消超链接",\r\n
VisitLink\t\t\t: "打开超链接",\r\n
Anchor\t\t\t\t: "插入/编辑锚点链接",\r\n
AnchorDelete\t\t: "清除锚点链接",\r\n
InsertImageLbl\t\t: "图象",\r\n
InsertImage\t\t\t: "插入/编辑图象",\r\n
InsertFlashLbl\t\t: "Flash",\r\n
InsertFlash\t\t\t: "插入/编辑 Flash",\r\n
InsertTableLbl\t\t: "表格",\r\n
InsertTable\t\t\t: "插入/编辑表格",\r\n
InsertLineLbl\t\t: "水平线",\r\n
InsertLine\t\t\t: "插入水平线",\r\n
InsertSpecialCharLbl: "特殊符号",\r\n
InsertSpecialChar\t: "插入特殊符号",\r\n
InsertSmileyLbl\t\t: "表情符",\r\n
InsertSmiley\t\t: "插入表情图标",\r\n
About\t\t\t\t: "关于 FCKeditor",\r\n
Bold\t\t\t\t: "加粗",\r\n
Italic\t\t\t\t: "倾斜",\r\n
Underline\t\t\t: "下划线",\r\n
StrikeThrough\t\t: "删除线",\r\n
Subscript\t\t\t: "下标",\r\n
Superscript\t\t\t: "上标",\r\n
LeftJustify\t\t\t: "左对齐",\r\n
CenterJustify\t\t: "居中对齐",\r\n
RightJustify\t\t: "右对齐",\r\n
BlockJustify\t\t: "两端对齐",\r\n
DecreaseIndent\t\t: "减少缩进量",\r\n
IncreaseIndent\t\t: "增加缩进量",\r\n
Blockquote\t\t\t: "块引用",\r\n
CreateDiv\t\t\t: "插入 Div 标签",\r\n
EditDiv\t\t\t\t: "编辑 Div 标签",\r\n
DeleteDiv\t\t\t: "删除 Div 标签",\r\n
Undo\t\t\t\t: "撤消",\r\n
Redo\t\t\t\t: "重做",\r\n
NumberedListLbl\t\t: "编号列表",\r\n
NumberedList\t\t: "插入/删除编号列表",\r\n
BulletedListLbl\t\t: "项目列表",\r\n
BulletedList\t\t: "插入/删除项目列表",\r\n
ShowTableBorders\t: "显示表格边框",\r\n
ShowDetails\t\t\t: "显示详细资料",\r\n
Style\t\t\t\t: "样式",\r\n
FontFormat\t\t\t: "格式",\r\n
Font\t\t\t\t: "字体",\r\n
FontSize\t\t\t: "大小",\r\n
TextColor\t\t\t: "文本颜色",\r\n
BGColor\t\t\t\t: "背景颜色",\r\n
Source\t\t\t\t: "源代码",\r\n
Find\t\t\t\t: "查找",\r\n
Replace\t\t\t\t: "替换",\r\n
SpellCheck\t\t\t: "拼写检查",\r\n
UniversalKeyboard\t: "软键盘",\r\n
PageBreakLbl\t\t: "分页符",\r\n
PageBreak\t\t\t: "插入分页符",\r\n
\r\n
Form\t\t\t: "表单",\r\n
Checkbox\t\t: "复选框",\r\n
RadioButton\t\t: "单选按钮",\r\n
TextField\t\t: "单行文本",\r\n
Textarea\t\t: "多行文本",\r\n
HiddenField\t\t: "隐藏域",\r\n
Button\t\t\t: "按钮",\r\n
SelectionField\t: "列表/菜单",\r\n
ImageButton\t\t: "图像域",\r\n
\r\n
FitWindow\t\t: "全屏编辑",\r\n
ShowBlocks\t\t: "显示区块",\r\n
\r\n
// Context Menu\r\n
EditLink\t\t\t: "编辑超链接",\r\n
CellCM\t\t\t\t: "单元格",\r\n
RowCM\t\t\t\t: "行",\r\n
ColumnCM\t\t\t: "列",\r\n
InsertRowAfter\t\t: "在下方插入行",\r\n
InsertRowBefore\t\t: "在上方插入行",\r\n
DeleteRows\t\t\t: "删除行",\r\n
InsertColumnAfter\t: "在右侧插入列",\r\n
InsertColumnBefore\t: "在左侧插入列",\r\n
DeleteColumns\t\t: "删除列",\r\n
InsertCellAfter\t\t: "在右侧插入单元格",\r\n
InsertCellBefore\t: "在左侧插入单元格",\r\n
DeleteCells\t\t\t: "删除单元格",\r\n
MergeCells\t\t\t: "合并单元格",\r\n
MergeRight\t\t\t: "向右合并单元格",\r\n
MergeDown\t\t\t: "向下合并单元格",\r\n
HorizontalSplitCell\t: "水平拆分单元格",\r\n
VerticalSplitCell\t: "垂直拆分单元格",\r\n
TableDelete\t\t\t: "删除表格",\r\n
CellProperties\t\t: "单元格属性",\r\n
TableProperties\t\t: "表格属性",\r\n
ImageProperties\t\t: "图象属性",\r\n
FlashProperties\t\t: "Flash 属性",\r\n
\r\n
AnchorProp\t\t\t: "锚点链接属性",\r\n
ButtonProp\t\t\t: "按钮属性",\r\n
CheckboxProp\t\t: "复选框属性",\r\n
HiddenFieldProp\t\t: "隐藏域属性",\r\n
RadioButtonProp\t\t: "单选按钮属性",\r\n
ImageButtonProp\t\t: "图像域属性",\r\n
TextFieldProp\t\t: "单行文本属性",\r\n
SelectionFieldProp\t: "菜单/列表属性",\r\n
TextareaProp\t\t: "多行文本属性",\r\n
FormProp\t\t\t: "表单属性",\r\n
\r\n
FontFormats\t\t\t: "普通;已编排格式;地址;标题 1;标题 2;标题 3;标题 4;标题 5;标题 6;段落(DIV)",\r\n
\r\n
// Alerts and Messages\r\n
ProcessingXHTML\t\t: "正在处理 XHTML，请稍等...",\r\n
Done\t\t\t\t: "完成",\r\n
PasteWordConfirm\t: "您要粘贴的内容好像是来自 MS Word，是否要清除 MS Word 格式后再粘贴？",\r\n
NotCompatiblePaste\t: "该命令需要 Internet Explorer 5.5 或更高版本的支持，是否按常规粘贴进行？",\r\n
UnknownToolbarItem\t: "未知工具栏项目 \\"%1\\"",\r\n
UnknownCommand\t\t: "未知命令名称 \\"%1\\"",\r\n
NotImplemented\t\t: "命令无法执行",\r\n
UnknownToolbarSet\t: "工具栏设置 \\"%1\\" 不存在",\r\n
NoActiveX\t\t\t: "浏览器安全设置限制了本编辑器的某些功能。您必须启用安全设置中的“运行 ActiveX 控件和插件”，否则将出现某些错误并缺少功能。",\r\n
BrowseServerBlocked : "无法打开资源浏览器，请确认是否启用了禁止弹出窗口。",\r\n
DialogBlocked\t\t: "无法打开对话框窗口，请确认是否启用了禁止弹出窗口或网页对话框（IE）。",\r\n
VisitLinkBlocked\t: "无法打开新窗口，请确认是否启用了禁止弹出窗口或网页对话框（IE）。",\r\n
\r\n
// Dialogs\r\n
DlgBtnOK\t\t\t: "确定",\r\n
DlgBtnCancel\t\t: "取消",\r\n
DlgBtnClose\t\t\t: "关闭",\r\n
DlgBtnBrowseServer\t: "浏览服务器",\r\n
DlgAdvancedTag\t\t: "高级",\r\n
DlgOpOther\t\t\t: "<其它>",\r\n
DlgInfoTab\t\t\t: "信息",\r\n
DlgAlertUrl\t\t\t: "请插入 URL",\r\n
\r\n
// General Dialogs Labels\r\n
DlgGenNotSet\t\t: "<没有设置>",\r\n
DlgGenId\t\t\t: "ID",\r\n
DlgGenLangDir\t\t: "语言方向",\r\n
DlgGenLangDirLtr\t: "从左到右 (LTR)",\r\n
DlgGenLangDirRtl\t: "从右到左 (RTL)",\r\n
DlgGenLangCode\t\t: "语言代码",\r\n
DlgGenAccessKey\t\t: "访问键",\r\n
DlgGenName\t\t\t: "名称",\r\n
DlgGenTabIndex\t\t: "Tab 键次序",\r\n
DlgGenLongDescr\t\t: "详细说明地址",\r\n
DlgGenClass\t\t\t: "样式类名称",\r\n
DlgGenTitle\t\t\t: "标题",\r\n
DlgGenContType\t\t: "内容类型",\r\n
DlgGenLinkCharset\t: "字符编码",\r\n
DlgGenStyle\t\t\t: "行内样式",\r\n
\r\n
// Image Dialog\r\n
DlgImgTitle\t\t\t: "图象属性",\r\n
DlgImgInfoTab\t\t: "图象",\r\n
DlgImgBtnUpload\t\t: "发送到服务器上",\r\n
DlgImgURL\t\t\t: "源文件",\r\n
DlgImgUpload\t\t: "上传",\r\n
DlgImgAlt\t\t\t: "替换文本",\r\n
DlgImgWidth\t\t\t: "宽度",\r\n
DlgImgHeight\t\t: "高度",\r\n
DlgImgLockRatio\t\t: "锁定比例",\r\n
DlgBtnResetSize\t\t: "恢复尺寸",\r\n
DlgImgBorder\t\t: "边框大小",\r\n
DlgImgHSpace\t\t: "水平间距",\r\n
DlgImgVSpace\t\t: "垂直间距",\r\n
DlgImgAlign\t\t\t: "对齐方式",\r\n
DlgImgAlignLeft\t\t: "左对齐",\r\n
DlgImgAlignAbsBottom: "绝对底边",\r\n
DlgImgAlignAbsMiddle: "绝对居中",\r\n
DlgImgAlignBaseline\t: "基线",\r\n
DlgImgAlignBottom\t: "底边",\r\n
DlgImgAlignMiddle\t: "居中",\r\n
DlgImgAlignRight\t: "右对齐",\r\n
DlgImgAlignTextTop\t: "文本上方",\r\n
DlgImgAlignTop\t\t: "顶端",\r\n
DlgImgPreview\t\t: "预览",\r\n
DlgImgAlertUrl\t\t: "请输入图象地址",\r\n
DlgImgLinkTab\t\t: "链接",\r\n
\r\n
// Flash Dialog\r\n
DlgFlashTitle\t\t: "Flash 属性",\r\n
DlgFlashChkPlay\t\t: "自动播放",\r\n
DlgFlashChkLoop\t\t: "循环",\r\n
DlgFlashChkMenu\t\t: "启用 Flash 菜单",\r\n
DlgFlashScale\t\t: "缩放",\r\n
DlgFlashScaleAll\t: "全部显示",\r\n
DlgFlashScaleNoBorder\t: "无边框",\r\n
DlgFlashScaleFit\t: "严格匹配",\r\n
\r\n
// Link Dialog\r\n
DlgLnkWindowTitle\t: "超链接",\r\n
DlgLnkInfoTab\t\t: "超链接信息",\r\n
DlgLnkTargetTab\t\t: "目标",\r\n
\r\n
DlgLnkType\t\t\t: "超链接类型",\r\n
DlgLnkTypeURL\t\t: "超链接",\r\n
DlgLnkTypeAnchor\t: "页内锚点链接",\r\n
DlgLnkTypeEMail\t\t: "电子邮件",\r\n
DlgLnkProto\t\t\t: "协议",\r\n
DlgLnkProtoOther\t: "<其它>",\r\n
DlgLnkURL\t\t\t: "地址",\r\n
DlgLnkAnchorSel\t\t: "选择一个锚点",\r\n
DlgLnkAnchorByName\t: "按锚点名称",\r\n
DlgLnkAnchorById\t: "按锚点 ID",\r\n
DlgLnkNoAnchors\t\t: "(此文档没有可用的锚点)",\r\n
DlgLnkEMail\t\t\t: "地址",\r\n
DlgLnkEMailSubject\t: "主题",\r\n
DlgLnkEMailBody\t\t: "内容",\r\n
DlgLnkUpload\t\t: "上传",\r\n
DlgLnkBtnUpload\t\t: "发送到服务器上",\r\n
\r\n
DlgLnkTarget\t\t: "目标",\r\n
DlgLnkTargetFrame\t: "<框架>",\r\n
DlgLnkTargetPopup\t: "<弹出窗口>",\r\n
DlgLnkTargetBlank\t: "新窗口 (_blank)",\r\n
DlgLnkTargetParent\t: "父窗口 (_parent)",\r\n
DlgLnkTargetSelf\t: "本窗口 (_self)",\r\n
DlgLnkTargetTop\t\t: "整页 (_top)",\r\n
DlgLnkTargetFrameName\t: "目标框架名称",\r\n
DlgLnkPopWinName\t: "弹出窗口名称",\r\n
DlgLnkPopWinFeat\t: "弹出窗口属性",\r\n
DlgLnkPopResize\t\t: "调整大小",\r\n
DlgLnkPopLocation\t: "地址栏",\r\n
DlgLnkPopMenu\t\t: "菜单栏",\r\n
DlgLnkPopScroll\t\t: "滚动条",\r\n
DlgLnkPopStatus\t\t: "状态栏",\r\n
DlgLnkPopToolbar\t: "工具栏",\r\n
DlgLnkPopFullScrn\t: "全屏 (IE)",\r\n
DlgLnkPopDependent\t: "依附 (NS)",\r\n
DlgLnkPopWidth\t\t: "宽",\r\n
DlgLnkPopHeight\t\t: "高",\r\n
DlgLnkPopLeft\t\t: "左",\r\n
DlgLnkPopTop\t\t: "右",\r\n
\r\n
DlnLnkMsgNoUrl\t\t: "请输入超链接地址",\r\n
DlnLnkMsgNoEMail\t: "请输入电子邮件地址",\r\n
DlnLnkMsgNoAnchor\t: "请选择一个锚点",\r\n
DlnLnkMsgInvPopName\t: "弹出窗口名称必须以字母开头，并且不能含有空格。",\r\n
\r\n
// Color Dialog\r\n
DlgColorTitle\t\t: "选择颜色",\r\n
DlgColorBtnClear\t: "清除",\r\n
DlgColorHighlight\t: "预览",\r\n
DlgColorSelected\t: "选择",\r\n
\r\n
// Smiley Dialog\r\n
DlgSmileyTitle\t\t: "插入表情图标",\r\n
\r\n
// Special Character Dialog\r\n
DlgSpecialCharTitle\t: "选择特殊符号",\r\n
\r\n
// Table Dialog\r\n
DlgTableTitle\t\t: "表格属性",\r\n
DlgTableRows\t\t: "行数",\r\n
DlgTableColumns\t\t: "列数",\r\n
DlgTableBorder\t\t: "边框",\r\n
DlgTableAlign\t\t: "对齐",\r\n
DlgTableAlignNotSet\t: "<没有设置>",\r\n
DlgTableAlignLeft\t: "左对齐",\r\n
DlgTableAlignCenter\t: "居中",\r\n
DlgTableAlignRight\t: "右对齐",\r\n
DlgTableWidth\t\t: "宽度",\r\n
DlgTableWidthPx\t\t: "像素",\r\n
DlgTableWidthPc\t\t: "百分比",\r\n
DlgTableHeight\t\t: "高度",\r\n
DlgTableCellSpace\t: "间距",\r\n
DlgTableCellPad\t\t: "边距",\r\n
DlgTableCaption\t\t: "标题",\r\n
DlgTableSummary\t\t: "摘要",\r\n
DlgTableHeaders\t\t: "标题单元格",\r\n
DlgTableHeadersNone\t\t: "无",\r\n
DlgTableHeadersColumn\t: "第一列",\r\n
DlgTableHeadersRow\t\t: "第一行",\r\n
DlgTableHeadersBoth\t\t: "第一列和第一行",\r\n
\r\n
// Table Cell Dialog\r\n
DlgCellTitle\t\t: "单元格属性",\r\n
DlgCellWidth\t\t: "宽度",\r\n
DlgCellWidthPx\t\t: "像素",\r\n
DlgCellWidthPc\t\t: "百分比",\r\n
DlgCellHeight\t\t: "高度",\r\n
DlgCellWordWrap\t\t: "自动换行",\r\n
DlgCellWordWrapNotSet\t: "<没有设置>",\r\n
DlgCellWordWrapYes\t: "是",\r\n
DlgCellWordWrapNo\t: "否",\r\n
DlgCellHorAlign\t\t: "水平对齐",\r\n
DlgCellHorAlignNotSet\t: "<没有设置>",\r\n
DlgCellHorAlignLeft\t: "左对齐",\r\n
DlgCellHorAlignCenter\t: "居中",\r\n
DlgCellHorAlignRight: "右对齐",\r\n
DlgCellVerAlign\t\t: "垂直对齐",\r\n
DlgCellVerAlignNotSet\t: "<没有设置>",\r\n
DlgCellVerAlignTop\t: "顶端",\r\n
DlgCellVerAlignMiddle\t: "居中",\r\n
DlgCellVerAlignBottom\t: "底部",\r\n
DlgCellVerAlignBaseline\t: "基线",\r\n
DlgCellType\t\t: "单元格类型",\r\n
DlgCellTypeData\t\t: "资料",\r\n
DlgCellTypeHeader\t: "标题",\r\n
DlgCellRowSpan\t\t: "纵跨行数",\r\n
DlgCellCollSpan\t\t: "横跨列数",\r\n
DlgCellBackColor\t: "背景颜色",\r\n
DlgCellBorderColor\t: "边框颜色",\r\n
DlgCellBtnSelect\t: "选择...",\r\n
\r\n
// Find and Replace Dialog\r\n
DlgFindAndReplaceTitle\t: "查找和替换",\r\n
\r\n
// Find Dialog\r\n
DlgFindTitle\t\t: "查找",\r\n
DlgFindFindBtn\t\t: "查找",\r\n
DlgFindNotFoundMsg\t: "指定文本没有找到。",\r\n
\r\n
// Replace Dialog\r\n
DlgReplaceTitle\t\t\t: "替换",\r\n
DlgReplaceFindLbl\t\t: "查找:",\r\n
DlgReplaceReplaceLbl\t: "替换:",\r\n
DlgReplaceCaseChk\t\t: "区分大小写",\r\n
DlgReplaceReplaceBtn\t: "替换",\r\n
DlgReplaceReplAllBtn\t: "全部替换",\r\n
DlgReplaceWordChk\t\t: "全字匹配",\r\n
\r\n
// Paste Operations / Dialog\r\n
PasteErrorCut\t: "您的浏览器安全设置不允许编辑器自动执行剪切操作，请使用键盘快捷键(Ctrl+X)来完成。",\r\n
PasteErrorCopy\t: "您的浏览器安全设置不允许编辑器自动执行复制操作，请使用键盘快捷键(Ctrl+C)来完成。",\r\n
\r\n
PasteAsText\t\t: "粘贴为无格式文本",\r\n
PasteFromWord\t: "从 MS Word 粘贴",\r\n
\r\n
DlgPasteMsg2\t: "请使用键盘快捷键(<STRONG>Ctrl+V</STRONG>)把内容粘贴到下面的方框里，再按 <STRONG>确定</STRONG>。",\r\n
DlgPasteSec\t\t: "因为你的浏览器的安全设置原因，本编辑器不能直接访问你的剪贴板内容，你需要在本窗口重新粘贴一次。",\r\n
DlgPasteIgnoreFont\t\t: "忽略 Font 标签",\r\n
DlgPasteRemoveStyles\t: "清理 CSS 样式",\r\n
\r\n
// Color Picker\r\n
ColorAutomatic\t: "自动",\r\n
ColorMoreColors\t: "其它颜色...",\r\n
\r\n
// Document Properties\r\n
DocProps\t\t: "页面属性",\r\n
\r\n
// Anchor Dialog\r\n
DlgAnchorTitle\t\t: "命名锚点",\r\n
DlgAnchorName\t\t: "锚点名称",\r\n
DlgAnchorErrorName\t: "请输入锚点名称",\r\n
\r\n
// Speller Pages Dialog\r\n
DlgSpellNotInDic\t\t: "没有在字典里",\r\n
DlgSpellChangeTo\t\t: "更改为",\r\n
DlgSpellBtnIgnore\t\t: "忽略",\r\n
DlgSpellBtnIgnoreAll\t: "全部忽略",\r\n
DlgSpellBtnReplace\t\t: "替换",\r\n
DlgSpellBtnReplaceAll\t: "全部替换",\r\n
DlgSpellBtnUndo\t\t\t: "撤消",\r\n
DlgSpellNoSuggestions\t: "- 没有建议 -",\r\n
DlgSpellProgress\t\t: "正在进行拼写检查...",\r\n
DlgSpellNoMispell\t\t: "拼写检查完成：没有发现拼写错误",\r\n
DlgSpellNoChanges\t\t: "拼写检查完成：没有更改任何单词",\r\n
DlgSpellOneChange\t\t: "拼写检查完成：更改了一个单词",\r\n
DlgSpellManyChanges\t\t: "拼写检查完成：更改了 %1 个单词",\r\n
\r\n
IeSpellDownload\t\t\t: "拼写检查插件还没安装，你是否想现在就下载？",\r\n
\r\n
// Button Dialog\r\n
DlgButtonText\t\t: "标签(值)",\r\n
DlgButtonType\t\t: "类型",\r\n
DlgButtonTypeBtn\t: "按钮",\r\n
DlgButtonTypeSbm\t: "提交",\r\n
DlgButtonTypeRst\t: "重设",\r\n
\r\n
// Checkbox and Radio Button Dialogs\r\n
DlgCheckboxName\t\t: "名称",\r\n
DlgCheckboxValue\t: "选定值",\r\n
DlgCheckboxSelected\t: "已勾选",\r\n
\r\n
// Form Dialog\r\n
DlgFormName\t\t: "名称",\r\n
DlgFormAction\t: "动作",\r\n
DlgFormMethod\t: "方法",\r\n
\r\n
// Select Field Dialog\r\n
DlgSelectName\t\t: "名称",\r\n
DlgSelectValue\t\t: "选定",\r\n
DlgSelectSize\t\t: "高度",\r\n
DlgSelectLines\t\t: "行",\r\n
DlgSelectChkMulti\t: "允许多选",\r\n
DlgSelectOpAvail\t: "列表值",\r\n
DlgSelectOpText\t\t: "标签",\r\n
DlgSelectOpValue\t: "值",\r\n
DlgSelectBtnAdd\t\t: "新增",\r\n
DlgSelectBtnModify\t: "修改",\r\n
DlgSelectBtnUp\t\t: "上移",\r\n
DlgSelectBtnDown\t: "下移",\r\n
DlgSelectBtnSetValue : "设为初始化时选定",\r\n
DlgSelectBtnDelete\t: "删除",\r\n
\r\n
// Textarea Dialog\r\n
DlgTextareaName\t: "名称",\r\n
DlgTextareaCols\t: "字符宽度",\r\n
DlgTextareaRows\t: "行数",\r\n
\r\n
// Text Field Dialog\r\n
DlgTextName\t\t\t: "名称",\r\n
DlgTextValue\t\t: "初始值",\r\n
DlgTextCharWidth\t: "字符宽度",\r\n
DlgTextMaxChars\t\t: "最多字符数",\r\n
DlgTextType\t\t\t: "类型",\r\n
DlgTextTypeText\t\t: "文本",\r\n
DlgTextTypePass\t\t: "密码",\r\n
\r\n
// Hidden Field Dialog\r\n
DlgHiddenName\t: "名称",\r\n
DlgHiddenValue\t: "初始值",\r\n
\r\n
// Bulleted List Dialog\r\n
BulletedListProp\t: "项目列表属性",\r\n
NumberedListProp\t: "编号列表属性",\r\n
DlgLstStart\t\t\t: "开始序号",\r\n
DlgLstType\t\t\t: "列表类型",\r\n
DlgLstTypeCircle\t: "圆圈",\r\n
DlgLstTypeDisc\t\t: "圆点",\r\n
DlgLstTypeSquare\t: "方块",\r\n
DlgLstTypeNumbers\t: "数字 (1, 2, 3)",\r\n
DlgLstTypeLCase\t\t: "小写字母 (a, b, c)",\r\n
DlgLstTypeUCase\t\t: "大写字母 (A, B, C)",\r\n
DlgLstTypeSRoman\t: "小写罗马数字 (i, ii, iii)",\r\n
DlgLstTypeLRoman\t: "大写罗马数字 (I, II, III)",\r\n
\r\n
// Document Properties Dialog\r\n
DlgDocGeneralTab\t: "常规",\r\n
DlgDocBackTab\t\t: "背景",\r\n
DlgDocColorsTab\t\t: "颜色和边距",\r\n
DlgDocMetaTab\t\t: "Meta 数据",\r\n
\r\n
DlgDocPageTitle\t\t: "页面标题",\r\n
DlgDocLangDir\t\t: "语言方向",\r\n
DlgDocLangDirLTR\t: "从左到右 (LTR)",\r\n
DlgDocLangDirRTL\t: "从右到左 (RTL)",\r\n
DlgDocLangCode\t\t: "语言代码",\r\n
DlgDocCharSet\t\t: "字符编码",\r\n
DlgDocCharSetCE\t\t: "中欧",\r\n
DlgDocCharSetCT\t\t: "繁体中文 (Big5)",\r\n
DlgDocCharSetCR\t\t: "西里尔文",\r\n
DlgDocCharSetGR\t\t: "希腊文",\r\n
DlgDocCharSetJP\t\t: "日文",\r\n
DlgDocCharSetKR\t\t: "韩文",\r\n
DlgDocCharSetTR\t\t: "土耳其文",\r\n
DlgDocCharSetUN\t\t: "Unicode (UTF-8)",\r\n
DlgDocCharSetWE\t\t: "西欧",\r\n
DlgDocCharSetOther\t: "其它字符编码",\r\n
\r\n
DlgDocDocType\t\t: "文档类型",\r\n
DlgDocDocTypeOther\t: "其它文档类型",\r\n
DlgDocIncXHTML\t\t: "包含 XHTML 声明",\r\n
DlgDocBgColor\t\t: "背景颜色",\r\n
DlgDocBgImage\t\t: "背景图像",\r\n
DlgDocBgNoScroll\t: "不滚动背景图像",\r\n
DlgDocCText\t\t\t: "文本",\r\n
DlgDocCLink\t\t\t: "超链接",\r\n
DlgDocCVisited\t\t: "已访问的超链接",\r\n
DlgDocCActive\t\t: "活动超链接",\r\n
DlgDocMargins\t\t: "页面边距",\r\n
DlgDocMaTop\t\t\t: "上",\r\n
DlgDocMaLeft\t\t: "左",\r\n
DlgDocMaRight\t\t: "右",\r\n
DlgDocMaBottom\t\t: "下",\r\n
DlgDocMeIndex\t\t: "页面索引关键字 (用半角逗号[,]分隔)",\r\n
DlgDocMeDescr\t\t: "页面说明",\r\n
DlgDocMeAuthor\t\t: "作者",\r\n
DlgDocMeCopy\t\t: "版权",\r\n
DlgDocPreview\t\t: "预览",\r\n
\r\n
// Templates Dialog\r\n
Templates\t\t\t: "模板",\r\n
DlgTemplatesTitle\t: "内容模板",\r\n
DlgTemplatesSelMsg\t: "请选择编辑器内容模板:",\r\n
DlgTemplatesLoading\t: "正在加载模板列表，请稍等...",\r\n
DlgTemplatesNoTpl\t: "(没有模板)",\r\n
DlgTemplatesReplace\t: "替换当前内容",\r\n
\r\n
// About Dialog\r\n
DlgAboutAboutTab\t: "关于",\r\n
DlgAboutBrowserInfoTab\t: "浏览器信息",\r\n
DlgAboutLicenseTab\t: "许可证",\r\n
DlgAboutVersion\t\t: "版本",\r\n
DlgAboutInfo\t\t: "要获得更多信息请访问 ",\r\n
\r\n
// Div Dialog\r\n
DlgDivGeneralTab\t: "常规",\r\n
DlgDivAdvancedTab\t: "高级",\r\n
DlgDivStyle\t\t: "样式",\r\n
DlgDivInlineStyle\t: "CSS 样式",\r\n
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
            <value> <int>17809</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
