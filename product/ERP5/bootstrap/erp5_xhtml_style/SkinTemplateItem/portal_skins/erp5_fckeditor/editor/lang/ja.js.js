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
            <value> <string>ja.js</string> </value>
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
 * Japanese language file.\r\n
 */\r\n
\r\n
var FCKLang =\r\n
{\r\n
// Language direction : "ltr" (left to right) or "rtl" (right to left).\r\n
Dir\t\t\t\t\t: "ltr",\r\n
\r\n
ToolbarCollapse\t\t: "ツールバーを隠す",\r\n
ToolbarExpand\t\t: "ツールバーを表示",\r\n
\r\n
// Toolbar Items and Context Menu\r\n
Save\t\t\t\t: "保存",\r\n
NewPage\t\t\t\t: "新しいページ",\r\n
Preview\t\t\t\t: "プレビュー",\r\n
Cut\t\t\t\t\t: "切り取り",\r\n
Copy\t\t\t\t: "コピー",\r\n
Paste\t\t\t\t: "貼り付け",\r\n
PasteText\t\t\t: "プレーンテキスト貼り付け",\r\n
PasteWord\t\t\t: "ワード文章から貼り付け",\r\n
Print\t\t\t\t: "印刷",\r\n
SelectAll\t\t\t: "すべて選択",\r\n
RemoveFormat\t\t: "フォーマット削除",\r\n
InsertLinkLbl\t\t: "リンク",\r\n
InsertLink\t\t\t: "リンク挿入/編集",\r\n
RemoveLink\t\t\t: "リンク削除",\r\n
VisitLink\t\t\t: "リンクを開く",\r\n
Anchor\t\t\t\t: "アンカー挿入/編集",\r\n
AnchorDelete\t\t: "アンカー削除",\r\n
InsertImageLbl\t\t: "イメージ",\r\n
InsertImage\t\t\t: "イメージ挿入/編集",\r\n
InsertFlashLbl\t\t: "Flash",\r\n
InsertFlash\t\t\t: "Flash挿入/編集",\r\n
InsertTableLbl\t\t: "テーブル",\r\n
InsertTable\t\t\t: "テーブル挿入/編集",\r\n
InsertLineLbl\t\t: "ライン",\r\n
InsertLine\t\t\t: "横罫線",\r\n
InsertSpecialCharLbl: "特殊文字",\r\n
InsertSpecialChar\t: "特殊文字挿入",\r\n
InsertSmileyLbl\t\t: "絵文字",\r\n
InsertSmiley\t\t: "絵文字挿入",\r\n
About\t\t\t\t: "FCKeditorヘルプ",\r\n
Bold\t\t\t\t: "太字",\r\n
Italic\t\t\t\t: "斜体",\r\n
Underline\t\t\t: "下線",\r\n
StrikeThrough\t\t: "打ち消し線",\r\n
Subscript\t\t\t: "添え字",\r\n
Superscript\t\t\t: "上付き文字",\r\n
LeftJustify\t\t\t: "左揃え",\r\n
CenterJustify\t\t: "中央揃え",\r\n
RightJustify\t\t: "右揃え",\r\n
BlockJustify\t\t: "両端揃え",\r\n
DecreaseIndent\t\t: "インデント解除",\r\n
IncreaseIndent\t\t: "インデント",\r\n
Blockquote\t\t\t: "ブロック引用",\r\n
CreateDiv\t\t\t: "Div 作成",\r\n
EditDiv\t\t\t\t: "Div 編集",\r\n
DeleteDiv\t\t\t: "Div 削除",\r\n
Undo\t\t\t\t: "元に戻す",\r\n
Redo\t\t\t\t: "やり直し",\r\n
NumberedListLbl\t\t: "段落番号",\r\n
NumberedList\t\t: "段落番号の追加/削除",\r\n
BulletedListLbl\t\t: "箇条書き",\r\n
BulletedList\t\t: "箇条書きの追加/削除",\r\n
ShowTableBorders\t: "テーブルボーダー表示",\r\n
ShowDetails\t\t\t: "詳細表示",\r\n
Style\t\t\t\t: "スタイル",\r\n
FontFormat\t\t\t: "フォーマット",\r\n
Font\t\t\t\t: "フォント",\r\n
FontSize\t\t\t: "サイズ",\r\n
TextColor\t\t\t: "テキスト色",\r\n
BGColor\t\t\t\t: "背景色",\r\n
Source\t\t\t\t: "ソース",\r\n
Find\t\t\t\t: "検索",\r\n
Replace\t\t\t\t: "置き換え",\r\n
SpellCheck\t\t\t: "スペルチェック",\r\n
UniversalKeyboard\t: "ユニバーサル・キーボード",\r\n
PageBreakLbl\t\t: "改ページ",\r\n
PageBreak\t\t\t: "改ページ挿入",\r\n
\r\n
Form\t\t\t: "フォーム",\r\n
Checkbox\t\t: "チェックボックス",\r\n
RadioButton\t\t: "ラジオボタン",\r\n
TextField\t\t: "１行テキスト",\r\n
Textarea\t\t: "テキストエリア",\r\n
HiddenField\t\t: "不可視フィールド",\r\n
Button\t\t\t: "ボタン",\r\n
SelectionField\t: "選択フィールド",\r\n
ImageButton\t\t: "画像ボタン",\r\n
\r\n
FitWindow\t\t: "エディタサイズを最大にします",\r\n
ShowBlocks\t\t: "ブロック表示",\r\n
\r\n
// Context Menu\r\n
EditLink\t\t\t: "リンク編集",\r\n
CellCM\t\t\t\t: "セル",\r\n
RowCM\t\t\t\t: "行",\r\n
ColumnCM\t\t\t: "カラム",\r\n
InsertRowAfter\t\t: "列の後に挿入",\r\n
InsertRowBefore\t\t: "列の前に挿入",\r\n
DeleteRows\t\t\t: "行削除",\r\n
InsertColumnAfter\t: "カラムの後に挿入",\r\n
InsertColumnBefore\t: "カラムの前に挿入",\r\n
DeleteColumns\t\t: "列削除",\r\n
InsertCellAfter\t\t: "セルの後に挿入",\r\n
InsertCellBefore\t: "セルの前に挿入",\r\n
DeleteCells\t\t\t: "セル削除",\r\n
MergeCells\t\t\t: "セル結合",\r\n
MergeRight\t\t\t: "右に結合",\r\n
MergeDown\t\t\t: "下に結合",\r\n
HorizontalSplitCell\t: "セルを水平方向分割",\r\n
VerticalSplitCell\t: "セルを垂直方向に分割",\r\n
TableDelete\t\t\t: "テーブル削除",\r\n
CellProperties\t\t: "セル プロパティ",\r\n
TableProperties\t\t: "テーブル プロパティ",\r\n
ImageProperties\t\t: "イメージ プロパティ",\r\n
FlashProperties\t\t: "Flash プロパティ",\r\n
\r\n
AnchorProp\t\t\t: "アンカー プロパティ",\r\n
ButtonProp\t\t\t: "ボタン プロパティ",\r\n
CheckboxProp\t\t: "チェックボックス プロパティ",\r\n
HiddenFieldProp\t\t: "不可視フィールド プロパティ",\r\n
RadioButtonProp\t\t: "ラジオボタン プロパティ",\r\n
ImageButtonProp\t\t: "画像ボタン プロパティ",\r\n
TextFieldProp\t\t: "１行テキスト プロパティ",\r\n
SelectionFieldProp\t: "選択フィールド プロパティ",\r\n
TextareaProp\t\t: "テキストエリア プロパティ",\r\n
FormProp\t\t\t: "フォーム プロパティ",\r\n
\r\n
FontFormats\t\t\t: "標準;書式付き;アドレス;見出し 1;見出し 2;見出し 3;見出し 4;見出し 5;見出し 6;標準 (DIV)",\r\n
\r\n
// Alerts and Messages\r\n
ProcessingXHTML\t\t: "XHTML処理中. しばらくお待ちください...",\r\n
Done\t\t\t\t: "完了",\r\n
PasteWordConfirm\t: "貼り付けを行うテキストは、ワード文章からコピーされようとしています。貼り付ける前にクリーニングを行いますか？",\r\n
NotCompatiblePaste\t: "このコマンドはインターネット・エクスプローラーバージョン5.5以上で利用可能です。クリーニングしないで貼り付けを行いますか？",\r\n
UnknownToolbarItem\t: "未知のツールバー項目 \\"%1\\"",\r\n
UnknownCommand\t\t: "未知のコマンド名 \\"%1\\"",\r\n
NotImplemented\t\t: "コマンドはインプリメントされませんでした。",\r\n
UnknownToolbarSet\t: "ツールバー設定 \\"%1\\" 存在しません。",\r\n
NoActiveX\t\t\t: "エラー、警告メッセージなどが発生した場合、ブラウザーのセキュリティ設定によりエディタのいくつかの機能が制限されている可能性があります。セキュリティ設定のオプションで\\"ActiveXコントロールとプラグインの実行\\"を有効にするにしてください。",\r\n
BrowseServerBlocked : "サーバーブラウザーを開くことができませんでした。ポップアップ・ブロック機能が無効になっているか確認してください。",\r\n
DialogBlocked\t\t: "ダイアログウィンドウを開くことができませんでした。ポップアップ・ブロック機能が無効になっているか確認してください。",\r\n
VisitLinkBlocked\t: "新しいウィンドウを開くことができませんでした。ポップアップ・ブロック機能が無効になっているか確認してください。",\r\n
\r\n
// Dialogs\r\n
DlgBtnOK\t\t\t: "OK",\r\n
DlgBtnCancel\t\t: "キャンセル",\r\n
DlgBtnClose\t\t\t: "閉じる",\r\n
DlgBtnBrowseServer\t: "サーバーブラウザー",\r\n
DlgAdvancedTag\t\t: "高度な設定",\r\n
DlgOpOther\t\t\t: "<その他>",\r\n
DlgInfoTab\t\t\t: "情報",\r\n
DlgAlertUrl\t\t\t: "URLを挿入してください",\r\n
\r\n
// General Dialogs Labels\r\n
DlgGenNotSet\t\t: "<なし>",\r\n
DlgGenId\t\t\t: "Id",\r\n
DlgGenLangDir\t\t: "文字表記の方向",\r\n
DlgGenLangDirLtr\t: "左から右 (LTR)",\r\n
DlgGenLangDirRtl\t: "右から左 (RTL)",\r\n
DlgGenLangCode\t\t: "言語コード",\r\n
DlgGenAccessKey\t\t: "アクセスキー",\r\n
DlgGenName\t\t\t: "Name属性",\r\n
DlgGenTabIndex\t\t: "タブインデックス",\r\n
DlgGenLongDescr\t\t: "longdesc属性(長文説明)",\r\n
DlgGenClass\t\t\t: "スタイルシートクラス",\r\n
DlgGenTitle\t\t\t: "Title属性",\r\n
DlgGenContType\t\t: "Content Type属性",\r\n
DlgGenLinkCharset\t: "リンクcharset属性",\r\n
DlgGenStyle\t\t\t: "スタイルシート",\r\n
\r\n
// Image Dialog\r\n
DlgImgTitle\t\t\t: "イメージ プロパティ",\r\n
DlgImgInfoTab\t\t: "イメージ 情報",\r\n
DlgImgBtnUpload\t\t: "サーバーに送信",\r\n
DlgImgURL\t\t\t: "URL",\r\n
DlgImgUpload\t\t: "アップロード",\r\n
DlgImgAlt\t\t\t: "代替テキスト",\r\n
DlgImgWidth\t\t\t: "幅",\r\n
DlgImgHeight\t\t: "高さ",\r\n
DlgImgLockRatio\t\t: "ロック比率",\r\n
DlgBtnResetSize\t\t: "サイズリセット",\r\n
DlgImgBorder\t\t: "ボーダー",\r\n
DlgImgHSpace\t\t: "横間隔",\r\n
DlgImgVSpace\t\t: "縦間隔",\r\n
DlgImgAlign\t\t\t: "行揃え",\r\n
DlgImgAlignLeft\t\t: "左",\r\n
DlgImgAlignAbsBottom: "下部(絶対的)",\r\n
DlgImgAlignAbsMiddle: "中央(絶対的)",\r\n
DlgImgAlignBaseline\t: "ベースライン",\r\n
DlgImgAlignBottom\t: "下",\r\n
DlgImgAlignMiddle\t: "中央",\r\n
DlgImgAlignRight\t: "右",\r\n
DlgImgAlignTextTop\t: "テキスト上部",\r\n
DlgImgAlignTop\t\t: "上",\r\n
DlgImgPreview\t\t: "プレビュー",\r\n
DlgImgAlertUrl\t\t: "イメージのURLを入力してください。",\r\n
DlgImgLinkTab\t\t: "リンク",\r\n
\r\n
// Flash Dialog\r\n
DlgFlashTitle\t\t: "Flash プロパティ",\r\n
DlgFlashChkPlay\t\t: "再生",\r\n
DlgFlashChkLoop\t\t: "ループ再生",\r\n
DlgFlashChkMenu\t\t: "Flashメニュー可能",\r\n
DlgFlashScale\t\t: "拡大縮小設定",\r\n
DlgFlashScaleAll\t: "すべて表示",\r\n
DlgFlashScaleNoBorder\t: "外が見えない様に拡大",\r\n
DlgFlashScaleFit\t: "上下左右にフィット",\r\n
\r\n
// Link Dialog\r\n
DlgLnkWindowTitle\t: "ハイパーリンク",\r\n
DlgLnkInfoTab\t\t: "ハイパーリンク 情報",\r\n
DlgLnkTargetTab\t\t: "ターゲット",\r\n
\r\n
DlgLnkType\t\t\t: "リンクタイプ",\r\n
DlgLnkTypeURL\t\t: "URL",\r\n
DlgLnkTypeAnchor\t: "このページのアンカー",\r\n
DlgLnkTypeEMail\t\t: "E-Mail",\r\n
DlgLnkProto\t\t\t: "プロトコル",\r\n
DlgLnkProtoOther\t: "<その他>",\r\n
DlgLnkURL\t\t\t: "URL",\r\n
DlgLnkAnchorSel\t\t: "アンカーを選択",\r\n
DlgLnkAnchorByName\t: "アンカー名",\r\n
DlgLnkAnchorById\t: "エレメントID",\r\n
DlgLnkNoAnchors\t\t: "(ドキュメントにおいて利用可能なアンカーはありません。)",\r\n
DlgLnkEMail\t\t\t: "E-Mail アドレス",\r\n
DlgLnkEMailSubject\t: "件名",\r\n
DlgLnkEMailBody\t\t: "本文",\r\n
DlgLnkUpload\t\t: "アップロード",\r\n
DlgLnkBtnUpload\t\t: "サーバーに送信",\r\n
\r\n
DlgLnkTarget\t\t: "ターゲット",\r\n
DlgLnkTargetFrame\t: "<フレーム>",\r\n
DlgLnkTargetPopup\t: "<ポップアップウィンドウ>",\r\n
DlgLnkTargetBlank\t: "新しいウィンドウ (_blank)",\r\n
DlgLnkTargetParent\t: "親ウィンドウ (_parent)",\r\n
DlgLnkTargetSelf\t: "同じウィンドウ (_self)",\r\n
DlgLnkTargetTop\t\t: "最上位ウィンドウ (_top)",\r\n
DlgLnkTargetFrameName\t: "目的のフレーム名",\r\n
DlgLnkPopWinName\t: "ポップアップウィンドウ名",\r\n
DlgLnkPopWinFeat\t: "ポップアップウィンドウ特徴",\r\n
DlgLnkPopResize\t\t: "リサイズ可能",\r\n
DlgLnkPopLocation\t: "ロケーションバー",\r\n
DlgLnkPopMenu\t\t: "メニューバー",\r\n
DlgLnkPopScroll\t\t: "スクロールバー",\r\n
DlgLnkPopStatus\t\t: "ステータスバー",\r\n
DlgLnkPopToolbar\t: "ツールバー",\r\n
DlgLnkPopFullScrn\t: "全画面モード(IE)",\r\n
DlgLnkPopDependent\t: "開いたウィンドウに連動して閉じる (Netscape)",\r\n
DlgLnkPopWidth\t\t: "幅",\r\n
DlgLnkPopHeight\t\t: "高さ",\r\n
DlgLnkPopLeft\t\t: "左端からの座標で指定",\r\n
DlgLnkPopTop\t\t: "上端からの座標で指定",\r\n
\r\n
DlnLnkMsgNoUrl\t\t: "リンクURLを入力してください。",\r\n
DlnLnkMsgNoEMail\t: "メールアドレスを入力してください。",\r\n
DlnLnkMsgNoAnchor\t: "アンカーを選択してください。",\r\n
DlnLnkMsgInvPopName\t: "ポップ・アップ名は英字で始まる文字で指定してくだい。ポップ・アップ名にスペースは含めません",\r\n
\r\n
// Color Dialog\r\n
DlgColorTitle\t\t: "色選択",\r\n
DlgColorBtnClear\t: "クリア",\r\n
DlgColorHighlight\t: "ハイライト",\r\n
DlgColorSelected\t: "選択色",\r\n
\r\n
// Smiley Dialog\r\n
DlgSmileyTitle\t\t: "顔文字挿入",\r\n
\r\n
// Special Character Dialog\r\n
DlgSpecialCharTitle\t: "特殊文字選択",\r\n
\r\n
// Table Dialog\r\n
DlgTableTitle\t\t: "テーブル プロパティ",\r\n
DlgTableRows\t\t: "行",\r\n
DlgTableColumns\t\t: "列",\r\n
DlgTableBorder\t\t: "ボーダーサイズ",\r\n
DlgTableAlign\t\t: "キャプションの整列",\r\n
DlgTableAlignNotSet\t: "<なし>",\r\n
DlgTableAlignLeft\t: "左",\r\n
DlgTableAlignCenter\t: "中央",\r\n
DlgTableAlignRight\t: "右",\r\n
DlgTableWidth\t\t: "テーブル幅",\r\n
DlgTableWidthPx\t\t: "ピクセル",\r\n
DlgTableWidthPc\t\t: "パーセント",\r\n
DlgTableHeight\t\t: "テーブル高さ",\r\n
DlgTableCellSpace\t: "セル内余白",\r\n
DlgTableCellPad\t\t: "セル内間隔",\r\n
DlgTableCaption\t\t: "ｷｬﾌﾟｼｮﾝ",\r\n
DlgTableSummary\t\t: "テーブル目的/構造",\r\n
DlgTableHeaders\t\t: "Headers",\t//MISSING\r\n
DlgTableHeadersNone\t\t: "None",\t//MISSING\r\n
DlgTableHeadersColumn\t: "First column",\t//MISSING\r\n
DlgTableHeadersRow\t\t: "First Row",\t//MISSING\r\n
DlgTableHeadersBoth\t\t: "Both",\t//MISSING\r\n
\r\n
// Table Cell Dialog\r\n
DlgCellTitle\t\t: "セル プロパティ",\r\n
DlgCellWidth\t\t: "幅",\r\n
DlgCellWidthPx\t\t: "ピクセル",\r\n
DlgCellWidthPc\t\t: "パーセント",\r\n
DlgCellHeight\t\t: "高さ",\r\n
DlgCellWordWrap\t\t: "折り返し",\r\n
DlgCellWordWrapNotSet\t: "<なし>",\r\n
DlgCellWordWrapYes\t: "Yes",\r\n
DlgCellWordWrapNo\t: "No",\r\n
DlgCellHorAlign\t\t: "セル横の整列",\r\n
DlgCellHorAlignNotSet\t: "<なし>",\r\n
DlgCellHorAlignLeft\t: "左",\r\n
DlgCellHorAlignCenter\t: "中央",\r\n
DlgCellHorAlignRight: "右",\r\n
DlgCellVerAlign\t\t: "セル縦の整列",\r\n
DlgCellVerAlignNotSet\t: "<なし>",\r\n
DlgCellVerAlignTop\t: "上",\r\n
DlgCellVerAlignMiddle\t: "中央",\r\n
DlgCellVerAlignBottom\t: "下",\r\n
DlgCellVerAlignBaseline\t: "ベースライン",\r\n
DlgCellType\t\t: "Cell Type",\t//MISSING\r\n
DlgCellTypeData\t\t: "Data",\t//MISSING\r\n
DlgCellTypeHeader\t: "Header",\t//MISSING\r\n
DlgCellRowSpan\t\t: "縦幅(行数)",\r\n
DlgCellCollSpan\t\t: "横幅(列数)",\r\n
DlgCellBackColor\t: "背景色",\r\n
DlgCellBorderColor\t: "ボーダーカラー",\r\n
DlgCellBtnSelect\t: "選択...",\r\n
\r\n
// Find and Replace Dialog\r\n
DlgFindAndReplaceTitle\t: "検索して置換",\r\n
\r\n
// Find Dialog\r\n
DlgFindTitle\t\t: "検索",\r\n
DlgFindFindBtn\t\t: "検索",\r\n
DlgFindNotFoundMsg\t: "指定された文字列は見つかりませんでした。",\r\n
\r\n
// Replace Dialog\r\n
DlgReplaceTitle\t\t\t: "置き換え",\r\n
DlgReplaceFindLbl\t\t: "検索する文字列:",\r\n
DlgReplaceReplaceLbl\t: "置換えする文字列:",\r\n
DlgReplaceCaseChk\t\t: "部分一致",\r\n
DlgReplaceReplaceBtn\t: "置換え",\r\n
DlgReplaceReplAllBtn\t: "すべて置換え",\r\n
DlgReplaceWordChk\t\t: "単語単位で一致",\r\n
\r\n
// Paste Operations / Dialog\r\n
PasteErrorCut\t: "ブラウザーのセキュリティ設定によりエディタの切り取り操作が自動で実行することができません。実行するには手動でキーボードの(Ctrl+X)を使用してください。",\r\n
PasteErrorCopy\t: "ブラウザーのセキュリティ設定によりエディタのコピー操作が自動で実行することができません。実行するには手動でキーボードの(Ctrl+C)を使用してください。",\r\n
\r\n
PasteAsText\t\t: "プレーンテキスト貼り付け",\r\n
PasteFromWord\t: "ワード文章から貼り付け",\r\n
\r\n
DlgPasteMsg2\t: "キーボード(<STRONG>Ctrl+V</STRONG>)を使用して、次の入力エリア内で貼って、<STRONG>OK</STRONG>を押してください。",\r\n
DlgPasteSec\t\t: "ブラウザのセキュリティ設定により、エディタはクリップボード・データに直接アクセスすることができません。このウィンドウは貼り付け操作を行う度に表示されます。",\r\n
DlgPasteIgnoreFont\t\t: "FontタグのFace属性を無視します。",\r\n
DlgPasteRemoveStyles\t: "スタイル定義を削除します。",\r\n
\r\n
// Color Picker\r\n
ColorAutomatic\t: "自動",\r\n
ColorMoreColors\t: "その他の色...",\r\n
\r\n
// Document Properties\r\n
DocProps\t\t: "文書 プロパティ",\r\n
\r\n
// Anchor Dialog\r\n
DlgAnchorTitle\t\t: "アンカー プロパティ",\r\n
DlgAnchorName\t\t: "アンカー名",\r\n
DlgAnchorErrorName\t: "アンカー名を必ず入力してください。",\r\n
\r\n
// Speller Pages Dialog\r\n
DlgSpellNotInDic\t\t: "辞書にありません",\r\n
DlgSpellChangeTo\t\t: "変更",\r\n
DlgSpellBtnIgnore\t\t: "無視",\r\n
DlgSpellBtnIgnoreAll\t: "すべて無視",\r\n
DlgSpellBtnReplace\t\t: "置換",\r\n
DlgSpellBtnReplaceAll\t: "すべて置換",\r\n
DlgSpellBtnUndo\t\t\t: "やり直し",\r\n
DlgSpellNoSuggestions\t: "- 該当なし -",\r\n
DlgSpellProgress\t\t: "スペルチェック処理中...",\r\n
DlgSpellNoMispell\t\t: "スペルチェック完了: スペルの誤りはありませんでした",\r\n
DlgSpellNoChanges\t\t: "スペルチェック完了: 語句は変更されませんでした",\r\n
DlgSpellOneChange\t\t: "スペルチェック完了: １語句変更されました",\r\n
DlgSpellManyChanges\t\t: "スペルチェック完了: %1 語句変更されました",\r\n
\r\n
IeSpellDownload\t\t\t: "スペルチェッカーがインストールされていません。今すぐダウンロードしますか?",\r\n
\r\n
// Button Dialog\r\n
DlgButtonText\t\t: "テキスト (値)",\r\n
DlgButtonType\t\t: "タイプ",\r\n
DlgButtonTypeBtn\t: "ボタン",\r\n
DlgButtonTypeSbm\t: "送信",\r\n
DlgButtonTypeRst\t: "リセット",\r\n
\r\n
// Checkbox and Radio Button Dialogs\r\n
DlgCheckboxName\t\t: "名前",\r\n
DlgCheckboxValue\t: "値",\r\n
DlgCheckboxSelected\t: "選択済み",\r\n
\r\n
// Form Dialog\r\n
DlgFormName\t\t: "フォーム名",\r\n
DlgFormAction\t: "アクション",\r\n
DlgFormMethod\t: "メソッド",\r\n
\r\n
// Select Field Dialog\r\n
DlgSelectName\t\t: "名前",\r\n
DlgSelectValue\t\t: "値",\r\n
DlgSelectSize\t\t: "サイズ",\r\n
DlgSelectLines\t\t: "行",\r\n
DlgSelectChkMulti\t: "複数項目選択を許可",\r\n
DlgSelectOpAvail\t: "利用可能なオプション",\r\n
DlgSelectOpText\t\t: "選択項目名",\r\n
DlgSelectOpValue\t: "選択項目値",\r\n
DlgSelectBtnAdd\t\t: "追加",\r\n
DlgSelectBtnModify\t: "編集",\r\n
DlgSelectBtnUp\t\t: "上へ",\r\n
DlgSelectBtnDown\t: "下へ",\r\n
DlgSelectBtnSetValue : "選択した値を設定",\r\n
DlgSelectBtnDelete\t: "削除",\r\n
\r\n
// Textarea Dialog\r\n
DlgTextareaName\t: "名前",\r\n
DlgTextareaCols\t: "列",\r\n
DlgTextareaRows\t: "行",\r\n
\r\n
// Text Field Dialog\r\n
DlgTextName\t\t\t: "名前",\r\n
DlgTextValue\t\t: "値",\r\n
DlgTextCharWidth\t: "サイズ",\r\n
DlgTextMaxChars\t\t: "最大長",\r\n
DlgTextType\t\t\t: "タイプ",\r\n
DlgTextTypeText\t\t: "テキスト",\r\n
DlgTextTypePass\t\t: "パスワード入力",\r\n
\r\n
// Hidden Field Dialog\r\n
DlgHiddenName\t: "名前",\r\n
DlgHiddenValue\t: "値",\r\n
\r\n
// Bulleted List Dialog\r\n
BulletedListProp\t: "箇条書き プロパティ",\r\n
NumberedListProp\t: "段落番号 プロパティ",\r\n
DlgLstStart\t\t\t: "開始文字",\r\n
DlgLstType\t\t\t: "タイプ",\r\n
DlgLstTypeCircle\t: "白丸",\r\n
DlgLstTypeDisc\t\t: "黒丸",\r\n
DlgLstTypeSquare\t: "四角",\r\n
DlgLstTypeNumbers\t: "アラビア数字 (1, 2, 3)",\r\n
DlgLstTypeLCase\t\t: "英字小文字 (a, b, c)",\r\n
DlgLstTypeUCase\t\t: "英字大文字 (A, B, C)",\r\n
DlgLstTypeSRoman\t: "ローマ数字小文字 (i, ii, iii)",\r\n
DlgLstTypeLRoman\t: "ローマ数字大文字 (I, II, III)",\r\n
\r\n
// Document Properties Dialog\r\n
DlgDocGeneralTab\t: "全般",\r\n
DlgDocBackTab\t\t: "背景",\r\n
DlgDocColorsTab\t\t: "色とマージン",\r\n
DlgDocMetaTab\t\t: "メタデータ",\r\n
\r\n
DlgDocPageTitle\t\t: "ページタイトル",\r\n
DlgDocLangDir\t\t: "言語文字表記の方向",\r\n
DlgDocLangDirLTR\t: "左から右に表記(LTR)",\r\n
DlgDocLangDirRTL\t: "右から左に表記(RTL)",\r\n
DlgDocLangCode\t\t: "言語コード",\r\n
DlgDocCharSet\t\t: "文字セット符号化",\r\n
DlgDocCharSetCE\t\t: "Central European",\r\n
DlgDocCharSetCT\t\t: "Chinese Traditional (Big5)",\r\n
DlgDocCharSetCR\t\t: "Cyrillic",\r\n
DlgDocCharSetGR\t\t: "Greek",\r\n
DlgDocCharSetJP\t\t: "Japanese",\r\n
DlgDocCharSetKR\t\t: "Korean",\r\n
DlgDocCharSetTR\t\t: "Turkish",\r\n
DlgDocCharSetUN\t\t: "Unicode (UTF-8)",\r\n
DlgDocCharSetWE\t\t: "Western European",\r\n
DlgDocCharSetOther\t: "他の文字セット符号化",\r\n
\r\n
DlgDocDocType\t\t: "文書タイプヘッダー",\r\n
DlgDocDocTypeOther\t: "その他文書タイプヘッダー",\r\n
DlgDocIncXHTML\t\t: "XHTML宣言をインクルード",\r\n
DlgDocBgColor\t\t: "背景色",\r\n
DlgDocBgImage\t\t: "背景画像 URL",\r\n
DlgDocBgNoScroll\t: "スクロールしない背景",\r\n
DlgDocCText\t\t\t: "テキスト",\r\n
DlgDocCLink\t\t\t: "リンク",\r\n
DlgDocCVisited\t\t: "アクセス済みリンク",\r\n
DlgDocCActive\t\t: "アクセス中リンク",\r\n
DlgDocMargins\t\t: "ページ・マージン",\r\n
DlgDocMaTop\t\t\t: "上部",\r\n
DlgDocMaLeft\t\t: "左",\r\n
DlgDocMaRight\t\t: "右",\r\n
DlgDocMaBottom\t\t: "下部",\r\n
DlgDocMeIndex\t\t: "文書のキーワード(カンマ区切り)",\r\n
DlgDocMeDescr\t\t: "文書の概要",\r\n
DlgDocMeAuthor\t\t: "文書の作者",\r\n
DlgDocMeCopy\t\t: "文書の著作権",\r\n
DlgDocPreview\t\t: "プレビュー",\r\n
\r\n
// Templates Dialog\r\n
Templates\t\t\t: "テンプレート(雛形)",\r\n
DlgTemplatesTitle\t: "テンプレート内容",\r\n
DlgTemplatesSelMsg\t: "エディターで使用するテンプレートを選択してください。<br>(現在のエディタの内容は失われます):",\r\n
DlgTemplatesLoading\t: "テンプレート一覧読み込み中. しばらくお待ちください...",\r\n
DlgTemplatesNoTpl\t: "(テンプレートが定義されていません)",\r\n
DlgTemplatesReplace\t: "現在のエディタの内容と置換えをします",\r\n
\r\n
// About Dialog\r\n
DlgAboutAboutTab\t: "バージョン情報",\r\n
DlgAboutBrowserInfoTab\t: "ブラウザ情報",\r\n
DlgAboutLicenseTab\t: "ライセンス",\r\n
DlgAboutVersion\t\t: "バージョン",\r\n
DlgAboutInfo\t\t: "より詳しい情報はこちらで",\r\n
\r\n
// Div Dialog\r\n
DlgDivGeneralTab\t: "全般",\r\n
DlgDivAdvancedTab\t: "高度な設定",\r\n
DlgDivStyle\t\t: "スタイル",\r\n
DlgDivInlineStyle\t: "インラインスタイル",\r\n
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
            <value> <int>21439</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
