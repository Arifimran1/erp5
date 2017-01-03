/*!
 * TableExport.js v3.2.10 (https://www.travismclarke.com)
 * Copyright 2016 Travis Clarke
 * Licensed under the MIT license
 */
!function(t,e){"function"==typeof define&&define.amd?define(["exports","jquery","file-saver","xlsx"],e):"object"==typeof exports&&"string"!=typeof exports.nodeName?e(exports,require("jquery"),require("file-saver"),require("xlsx")):e(t,t.jQuery,t.saveAs,t.XLSX)}(this,function(t,e,n,o){"use strict";var i=function(t,n,r){var s=this;s.settings=r?n:e.extend({},i.prototype.defaults,n),s.selectors=t;var a,p,f,l=i.prototype.rowDel,u=s.settings.ignoreRows instanceof Array?s.settings.ignoreRows:[s.settings.ignoreRows],c=s.settings.ignoreCols instanceof Array?s.settings.ignoreCols:[s.settings.ignoreCols],x=s.settings.ignoreCSS instanceof Array?s.settings.ignoreCSS.join(", "):s.settings.ignoreCSS;return s.settings.bootstrap?(a=i.prototype.bootstrap[0]+" ",p=i.prototype.bootstrap[1]+" ",f=i.prototype.bootstrap[2]+" "):(a=i.prototype.defaultButton+" ",p=f=""),s.selectors.each(function(){function t(t){var e=d.find("caption:not(.head)");e.length?e.append(t):d.prepend('<caption class="'+f+s.settings.position+'">'+t+"</caption>")}function n(e,n,o){var i="<button data-fileblob='"+e+"' class='"+a+p+o+"'>"+n+"</button>";t(i)}var d=e(this);r&&d.find("caption:not(.head)").remove();var y=d.find("tbody").find("tr"),y=s.settings.headings?y.add(d.find("thead>tr")):y,y=s.settings.footers?y.add(d.find("tfoot>tr")):y,m=s.settings.headings?d.find("thead>tr").length:0,g="id"===s.settings.fileName?d.attr("id")?d.attr("id"):i.prototype.defaultFileName:s.settings.fileName,h={xlsx:function(t,o){var r={},s=y.map(function(t,n){if(!~u.indexOf(t-m)&&!e(n).is(x)){var o=e(n).find("th, td");return[o.map(function(n,o){if(!~c.indexOf(n)&&!e(o).is(x)){if(o.hasAttribute("colspan")&&(r[t]=r[t]||{},r[t][n+1]=o.getAttribute("colspan")-1),o.hasAttribute("rowspan"))for(var i=1;i<o.getAttribute("rowspan");i++)r[t+i]=r[t+i]||{},r[t+i][n]=1;return r[t]&&r[t][n]?new Array(r[t][n]).concat(e(o).text()):e(o).text()}}).get()]}}).get(),a=i.prototype.escapeHtml(JSON.stringify({data:s,fileName:o,mimeType:i.prototype.xlsx.mimeType,fileExtension:i.prototype.xlsx.fileExtension})),p=i.prototype.xlsx.buttonContent,f=i.prototype.xlsx.defaultClass;n(a,p,f)},xlsm:function(t,o){var r={},s=y.map(function(t,n){if(!~u.indexOf(t-m)&&!e(n).is(x)){var o=e(n).find("th, td");return[o.map(function(n,o){if(!~c.indexOf(n)&&!e(o).is(x)){if(o.hasAttribute("colspan")&&(r[t]=r[t]||{},r[t][n+1]=o.getAttribute("colspan")-1),o.hasAttribute("rowspan"))for(var i=1;i<o.getAttribute("rowspan");i++)r[t+i]=r[t+i]||{},r[t+i][n]=1;return r[t]&&r[t][n]?new Array(r[t][n]).concat(e(o).text()):e(o).text()}}).get()]}}).get(),a=i.prototype.escapeHtml(JSON.stringify({data:s,fileName:o,mimeType:i.prototype.xls.mimeType,fileExtension:i.prototype.xls.fileExtension})),p=i.prototype.xls.buttonContent,f=i.prototype.xls.defaultClass;n(a,p,f)},xls:function(t,o){var r=i.prototype.xls.separator,s=y.map(function(t,n){if(!~u.indexOf(t-m)&&!e(n).is(x)){var o=e(n).find("th, td");return o.map(function(t,n){if(!~c.indexOf(t)&&!e(n).is(x))return e(n).text()}).get().join(r)}}).get().join(t),a=i.prototype.escapeHtml(JSON.stringify({data:s,fileName:o,mimeType:i.prototype.xls.mimeType,fileExtension:i.prototype.xls.fileExtension})),p=i.prototype.xls.buttonContent,f=i.prototype.xls.defaultClass;n(a,p,f)},csv:function(t,o){var r=i.prototype.csv.separator,s=y.map(function(t,n){if(!~u.indexOf(t-m)&&!e(n).is(x)){var o=e(n).find("th, td");return o.map(function(t,n){if(!~c.indexOf(t)&&!e(n).is(x))return e(n).text()}).get().join(r)}}).get().join(t),a=i.prototype.escapeHtml(JSON.stringify({data:s,fileName:o,mimeType:i.prototype.csv.mimeType,fileExtension:i.prototype.csv.fileExtension})),p=i.prototype.csv.buttonContent,f=i.prototype.csv.defaultClass;n(a,p,f)},txt:function(t,o){var r=i.prototype.txt.separator,s=y.map(function(t,n){if(!~u.indexOf(t-m)&&!e(n).is(x)){var o=e(n).find("th, td");return o.map(function(t,n){if(!~c.indexOf(t)&&!e(n).is(x))return e(n).text()}).get().join(r)}}).get().join(t),a=i.prototype.escapeHtml(JSON.stringify({data:s,fileName:o,mimeType:i.prototype.txt.mimeType,fileExtension:i.prototype.txt.fileExtension})),p=i.prototype.txt.buttonContent,f=i.prototype.txt.defaultClass;n(a,p,f)}};s.settings.formats.forEach(function(t){!(!o||"xls"!==t)&&(t="xlsm"),!o&&"xlsx"===t&&(t=null),t&&h[t](l,g)})}),e("button[data-fileblob]").off("click").on("click",function(){var t=e(this).data("fileblob"),n=t.data,o=t.fileName,r=t.mimeType,s=t.fileExtension;i.prototype.export2file(n,r,o,s)}),s};i.prototype={defaults:{headings:!0,footers:!0,formats:["xls","csv","txt"],fileName:"id",bootstrap:!0,position:"bottom",ignoreRows:null,ignoreCols:null,ignoreCSS:".tableexport-ignore"},charset:"charset=utf-8",defaultFileName:"myDownload",defaultButton:"button-default",bootstrap:["btn","btn-default","btn-toolbar"],rowDel:"\r\n",entityMap:{"&":"&#38;","<":"&#60;",">":"&#62;","'":"&#39;","/":"&#47"},xlsx:{defaultClass:"xlsx",buttonContent:"Export to xlsx",mimeType:"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",fileExtension:".xlsx"},xls:{defaultClass:"xls",buttonContent:"Export to xls",separator:"\t",mimeType:"application/vnd.ms-excel",fileExtension:".xls"},csv:{defaultClass:"csv",buttonContent:"Export to csv",separator:",",mimeType:"application/csv",fileExtension:".csv"},txt:{defaultClass:"txt",buttonContent:"Export to txt",separator:"  ",mimeType:"text/plain",fileExtension:".txt"},escapeHtml:function(t){return String(t).replace(/[&<>'\/]/g,function(t){return i.prototype.entityMap[t]})},dateNum:function(t,e){e&&(t+=1462);var n=Date.parse(t);return(n-new Date(Date.UTC(1899,11,30)))/864e5},createSheet:function(t){for(var e={},n={s:{c:1e7,r:1e7},e:{c:0,r:0}},i=0;i!=t.length;++i)for(var r=0;r!=t[i].length;++r){n.s.r>i&&(n.s.r=i),n.s.c>r&&(n.s.c=r),n.e.r<i&&(n.e.r=i),n.e.c<r&&(n.e.c=r);var s={v:t[i][r]};if(null!=s.v){var a=o.utils.encode_cell({c:r,r:i});"number"==typeof s.v?s.t="n":"boolean"==typeof s.v?s.t="b":s.v instanceof Date?(s.t="n",s.z=o.SSF._table[14],s.v=this.dateNum(s.v)):s.t="s",e[a]=s}}return n.s.c<1e7&&(e["!ref"]=o.utils.encode_range(n)),e},Workbook:function(){this.SheetNames=[],this.Sheets={}},string2ArrayBuffer:function(t){for(var e=new ArrayBuffer(t.length),n=new Uint8Array(e),o=0;o!=t.length;++o)n[o]=255&t.charCodeAt(o);return e},export2file:function(t,e,i,r){if(o&&r.startsWith(".xls")){var s=new this.Workbook,a=this.createSheet(t);s.SheetNames.push(i),s.Sheets[i]=a;var p={bookType:r.substr(1,3)+(r.substr(4)||"m"),bookSST:!1,type:"binary"},f=o.write(s,p);t=this.string2ArrayBuffer(f)}n(new Blob([t],{type:e+";"+this.charset}),i+r)},update:function(t){return new i(this.selectors,e.extend({},this.settings,t),(!0))},reset:function(){return new i(this.selectors,settings,(!0))},remove:function(){this.selectors.each(function(){e(this).find("caption:not(.head)").remove()})}},e.fn.tableExport=function(t,e){return new i(this,t,e)};for(var r in i.prototype)e.fn.tableExport[r]=i.prototype[r];t["default"]=t.TableExport=i});