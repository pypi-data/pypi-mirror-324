var e={d:(t,n)=>{for(var r in n)e.o(n,r)&&!e.o(t,r)&&Object.defineProperty(t,r,{enumerable:!0,get:n[r]})},o:(e,t)=>Object.prototype.hasOwnProperty.call(e,t)},t={};e.d(t,{A:()=>o});var n=function(e,t,n,r){return new(n||(n=Promise))((function(o,l){function i(e){try{u(r.next(e))}catch(e){l(e)}}function a(e){try{u(r.throw(e))}catch(e){l(e)}}function u(e){var t;e.done?o(e.value):(t=e.value,t instanceof n?t:new n((function(e){e(t)}))).then(i,a)}u((r=r.apply(e,t||[])).next())}))},r=function(e,t){var n,r,o,l={label:0,sent:function(){if(1&o[0])throw o[1];return o[1]},trys:[],ops:[]},i=Object.create(("function"==typeof Iterator?Iterator:Object).prototype);return i.next=a(0),i.throw=a(1),i.return=a(2),"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function a(a){return function(u){return function(a){if(n)throw new TypeError("Generator is already executing.");for(;i&&(i=0,a[0]&&(l=0)),l;)try{if(n=1,r&&(o=2&a[0]?r.return:a[0]?r.throw||((o=r.return)&&o.call(r),0):r.next)&&!(o=o.call(r,a[1])).done)return o;switch(r=0,o&&(a=[2&a[0],o.value]),a[0]){case 0:case 1:o=a;break;case 4:return l.label++,{value:a[1],done:!1};case 5:l.label++,r=a[1],a=[0];continue;case 7:a=l.ops.pop(),l.trys.pop();continue;default:if(!((o=(o=l.trys).length>0&&o[o.length-1])||6!==a[0]&&2!==a[0])){l=0;continue}if(3===a[0]&&(!o||a[1]>o[0]&&a[1]<o[3])){l.label=a[1];break}if(6===a[0]&&l.label<o[1]){l.label=o[1],o=a;break}if(o&&l.label<o[2]){l.label=o[2],l.ops.push(a);break}o[2]&&l.ops.pop(),l.trys.pop();continue}a=t.call(e,l)}catch(e){a=[6,e],r=0}finally{n=o=0}if(5&a[0])throw a[1];return{value:a[0]?a[1]:void 0,done:!0}}([a,u])}}};const o={renderpluginfactory:function(e){var t=e.React,o=e.fnrf_zst;return{input_renderers:{"funcnodes_files.FileUpload":function(e){var l=e.io,i=t.useRef(null);return t.createElement("div",null,t.createElement("input",{className:"nodedatainput styledinput",type:"file",onChange:function(e){return n(void 0,void 0,void 0,(function(){var t,n,i,a,u,c,d,s,f,p;return r(this,(function(r){switch(r.label){case 0:if(!(t=e.target.files)||0===t.length)return[2];if(!(n=o.nodespace.get_node(l.node)))return[2];if(i=n.getState(),!(a=i.io.parent))return[2];u=void 0,c=0,r.label=1;case 1:return c<10?a.fullvalue?(u=a.fullvalue.path,[3,4]):void 0===a.try_get_full_value?[3,4]:(a.try_get_full_value(),[4,new Promise((function(e){return setTimeout(e,500)}))]):[3,4];case 2:if(r.sent(),i=n.getState(),!(a=i.io.parent))return[3,4];r.label=3;case 3:return c++,[3,1];case 4:return d=(new Date).getTime(),[4,null===(f=o.worker)||void 0===f?void 0:f.upload_file({files:t,onProgressCallback:function(e,t){!function(e,t,n){o.on_node_action({type:"update",id:l.node,node:{progress:{prefix:"Uploading",n:e,total:t,elapsed:((new Date).getTime()-n)/1e3,unit_scale:!0,unit:"B",unit_divisor:1024}},from_remote:!0})}(e,t,d)},root:u})];case 5:return s=r.sent(),null===(p=o.worker)||void 0===p||p.set_io_value({nid:l.node,ioid:l.id,value:s,set_default:!0}),[2]}}))}))},disabled:l.connected,style:{display:"none"},ref:i}),t.createElement("button",{className:"nodedatainput styledinput",disabled:l.connected,onClick:function(){var e;null===(e=i.current)||void 0===e||e.click()}},"Upload File"))},"funcnodes_files.FolderUpload":function(e){var l=e.io,i=t.useRef(null);return t.createElement("div",null,t.createElement("input",{className:"nodedatainput styledinput",type:"file",onChange:function(e){return n(void 0,void 0,void 0,(function(){var t,n,i,a,u,c,d,s,f,p;return r(this,(function(r){switch(r.label){case 0:if(!(t=e.target.files)||0===t.length)return[2];if(!(n=o.nodespace.get_node(l.node)))return[2];if(i=n.getState(),!(a=i.io.parent))return[2];u=void 0,c=0,r.label=1;case 1:return c<10?a.fullvalue?(u=a.fullvalue.path,[3,4]):void 0===a.try_get_full_value?[3,4]:(a.try_get_full_value(),[4,new Promise((function(e){return setTimeout(e,500)}))]):[3,4];case 2:if(r.sent(),i=n.getState(),!(a=i.io.parent))return[3,4];r.label=3;case 3:return c++,[3,1];case 4:return d=(new Date).getTime(),[4,null===(f=o.worker)||void 0===f?void 0:f.upload_file({files:t,onProgressCallback:function(e,t){!function(e,t,n){o.on_node_action({type:"update",id:l.node,node:{progress:{prefix:"Uploading",n:e,total:t,elapsed:((new Date).getTime()-n)/1e3,unit_scale:!0,unit:"B",unit_divisor:1024}},from_remote:!0})}(e,t,d)},root:u})];case 5:return s=r.sent(),null===(p=o.worker)||void 0===p||p.set_io_value({nid:l.node,ioid:l.id,value:s,set_default:!0}),[2]}}))}))},disabled:l.connected,style:{display:"none"},ref:i,webkitdirectory:"true",directory:"true",multiple:!0}),t.createElement("button",{className:"nodedatainput styledinput",disabled:l.connected,onClick:function(){var e;null===(e=i.current)||void 0===e||e.click()}},"Upload Folder"))}},output_renderers:{"funcnodes_files.FileDownload":function(e){var l=e.io,i=t.useRef(null);return t.createElement("div",null,t.createElement("a",{ref:i,style:{display:"none"},href:"",download:""}),t.createElement("button",{className:"nodedatainput styledinput",onClick:function(){return n(void 0,void 0,void 0,(function(){var e,t,n,a,u,c,d,s,f,p,v;return r(this,(function(r){switch(r.label){case 0:return[4,null===(v=o.worker)||void 0===v?void 0:v.get_io_full_value({nid:l.node,ioid:l.id})];case 1:return e=r.sent(),n=(t=e).filename,a=t.content,u=atob(a),c=new Array(u.length).fill(null).map((function(e,t){return u.charCodeAt(t)})),d=new Uint8Array(c),s=new Blob([d]),f=URL.createObjectURL(s),null==(p=i.current)||p.setAttribute("href",f),null==p||p.setAttribute("download",n),null==p||p.click(),[2]}}))}))}},"Download File"))}}}}};var l=t.A;export{l as default};
