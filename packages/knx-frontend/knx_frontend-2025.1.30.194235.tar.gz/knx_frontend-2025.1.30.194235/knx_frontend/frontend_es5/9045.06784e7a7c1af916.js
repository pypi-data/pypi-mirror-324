(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["9045"],{61145:function(e,t,i){var n={"./ha-icon":["86267","3377"],"./ha-icon-button-toggle":["25152","5291"],"./ha-svg-icon":["10508"],"./ha-icon-button-group":["52100","1744"],"./ha-svg-icon.ts":["10508"],"./ha-icon.ts":["86267","3377"],"./ha-icon-overflow-menu":["65099","6718"],"./ha-icon-next":["54220"],"./ha-icon-picker":["73979","348"],"./ha-qr-code.ts":["9643","3750","1442"],"./ha-icon-button-arrow-prev.ts":["92500"],"./ha-icon-button-arrow-prev":["92500"],"./ha-icon-overflow-menu.ts":["65099","6718"],"./ha-alert":["17949"],"./ha-icon-button-next":["63448","3666"],"./ha-icon-button":["59897"],"./ha-icon-button-next.ts":["63448","3666"],"./ha-icon-picker.ts":["73979","348"],"./ha-icon-button-group.ts":["52100","1744"],"./ha-icon-button-toggle.ts":["25152","5291"],"./ha-icon-button-arrow-next.ts":["63922","852"],"./ha-icon-button-prev.ts":["3961","170"],"./ha-icon-prev":["78716","6470"],"./ha-icon-prev.ts":["78716","6470"],"./ha-icon-button.ts":["59897"],"./ha-alert.ts":["17949"],"./ha-icon-button-prev":["3961","170"],"./ha-qr-code":["9643","3750","1442"],"./ha-icon-next.ts":["54220"],"./ha-icon-button-arrow-next":["63922","852"]};function o(e){if(!i.o(n,e))return Promise.resolve().then((function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}));var t=n[e],o=t[0];return Promise.all(t.slice(1).map(i.e)).then((function(){return i(o)}))}o.keys=()=>Object.keys(n),o.id=61145,e.exports=o},2292:function(e,t,i){var n={"./flow-preview-generic.ts":["7433","4224","4645","6160","4284","2909","669"],"./flow-preview-generic_camera.ts":["96738","4224","4645","6160","4284","2909","9336"],"./flow-preview-generic":["7433","4224","4645","6160","4284","2909","669"],"./flow-preview-generic_camera":["96738","4224","4645","6160","4284","2909","9336"],"./flow-preview-template.ts":["76144","4224","4645","6160","4284","2909","8063"],"./flow-preview-template":["76144","4224","4645","6160","4284","2909","8063"]};function o(e){if(!i.o(n,e))return Promise.resolve().then((function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}));var t=n[e],o=t[0];return Promise.all(t.slice(1).map(i.e)).then((function(){return i(o)}))}o.keys=()=>Object.keys(n),o.id=2292,e.exports=o},12328:function(e,t,i){"use strict";i.d(t,{x:()=>n});i(63721),i(52247),i(39527),i(41360);const n=e=>{const t={};return e.forEach((e=>{var i,o;if(void 0!==(null===(i=e.description)||void 0===i?void 0:i.suggested_value)&&null!==(null===(o=e.description)||void 0===o?void 0:o.suggested_value))t[e.name]=e.description.suggested_value;else if("default"in e)t[e.name]=e.default;else if(e.required){if("boolean"===e.type)t[e.name]=!1;else if("string"===e.type)t[e.name]="";else if("integer"===e.type)t[e.name]="valueMin"in e?e.valueMin:0;else if("constant"===e.type)t[e.name]=e.value;else if("float"===e.type)t[e.name]=0;else if("select"===e.type){if(e.options.length){const i=e.options[0];t[e.name]=Array.isArray(i)?i[0]:i}}else if("positive_time_period_dict"===e.type)t[e.name]={hours:0,minutes:0,seconds:0};else if("expandable"===e.type)t[e.name]=n(e.schema);else if("selector"in e){const i=e.selector;var a;if("device"in i)t[e.name]=null!==(a=i.device)&&void 0!==a&&a.multiple?[]:"";else if("entity"in i){var s;t[e.name]=null!==(s=i.entity)&&void 0!==s&&s.multiple?[]:""}else if("area"in i){var r;t[e.name]=null!==(r=i.area)&&void 0!==r&&r.multiple?[]:""}else if("label"in i){var l;t[e.name]=null!==(l=i.label)&&void 0!==l&&l.multiple?[]:""}else if("boolean"in i)t[e.name]=!1;else if("addon"in i||"attribute"in i||"file"in i||"icon"in i||"template"in i||"text"in i||"theme"in i||"object"in i)t[e.name]="";else if("number"in i){var d,c;t[e.name]=null!==(d=null===(c=i.number)||void 0===c?void 0:c.min)&&void 0!==d?d:0}else if("select"in i){var h;if(null!==(h=i.select)&&void 0!==h&&h.options.length){const n=i.select.options[0],o="string"==typeof n?n:n.value;t[e.name]=i.select.multiple?[o]:o}}else if("country"in i){var u;null!==(u=i.country)&&void 0!==u&&null!==(u=u.countries)&&void 0!==u&&u.length&&(t[e.name]=i.country.countries[0])}else if("language"in i){var p;null!==(p=i.language)&&void 0!==p&&null!==(p=p.languages)&&void 0!==p&&p.length&&(t[e.name]=i.language.languages[0])}else if("duration"in i)t[e.name]={hours:0,minutes:0,seconds:0};else if("time"in i)t[e.name]="00:00:00";else if("date"in i||"datetime"in i){const i=(new Date).toISOString().slice(0,10);t[e.name]=`${i}T00:00:00`}else if("color_rgb"in i)t[e.name]=[0,0,0];else if("color_temp"in i){var f,m;t[e.name]=null!==(f=null===(m=i.color_temp)||void 0===m?void 0:m.min_mireds)&&void 0!==f?f:153}else if("action"in i||"trigger"in i||"condition"in i)t[e.name]=[];else{if(!("media"in i)&&!("target"in i))throw new Error(`Selector ${Object.keys(i)[0]} not supported in initial form data`);t[e.name]={}}}}else;})),t}},42877:function(e,t,i){"use strict";var n=i(73577),o=i(72621),a=(i(71695),i(19423),i(40251),i(39527),i(41360),i(13334),i(47021),i(57243)),s=i(50778),r=i(38653),l=i(11297);i(17949),i(59414);let d,c,h,u,p,f,m,g,v,y=e=>e;const w={boolean:()=>i.e("2154").then(i.bind(i,13755)),constant:()=>i.e("4418").then(i.bind(i,92152)),float:()=>i.e("4608").then(i.bind(i,68091)),grid:()=>i.e("4351").then(i.bind(i,39090)),expandable:()=>i.e("9823").then(i.bind(i,78446)),integer:()=>i.e("9456").then(i.bind(i,93285)),multi_select:()=>Promise.all([i.e("7493"),i.e("5079"),i.e("1808")]).then(i.bind(i,87092)),positive_time_period_dict:()=>Promise.all([i.e("2047"),i.e("5235")]).then(i.bind(i,96636)),select:()=>i.e("1083").then(i.bind(i,6102)),string:()=>i.e("9752").then(i.bind(i,58701))},k=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,n.Z)([(0,s.Mo)("ha-form")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof a.fl&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{var t;"selector"in e||null===(t=w[e.type])||void 0===t||t.call(w)}))}},{kind:"method",key:"render",value:function(){return(0,a.dy)(d||(d=y`
      <div class="root" part="root">
        ${0}
        ${0}
      </div>
    `),this.error&&this.error.base?(0,a.dy)(c||(c=y`
              <ha-alert alert-type="error">
                ${0}
              </ha-alert>
            `),this._computeError(this.error.base,this.schema)):"",this.schema.map((e=>{var t;const i=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),n=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return(0,a.dy)(h||(h=y`
            ${0}
            ${0}
          `),i?(0,a.dy)(u||(u=y`
                  <ha-alert own-margin alert-type="error">
                    ${0}
                  </ha-alert>
                `),this._computeError(i,e)):n?(0,a.dy)(p||(p=y`
                    <ha-alert own-margin alert-type="warning">
                      ${0}
                    </ha-alert>
                  `),this._computeWarning(n,e)):"","selector"in e?(0,a.dy)(f||(f=y`<ha-selector
                  .schema=${0}
                  .hass=${0}
                  .name=${0}
                  .selector=${0}
                  .value=${0}
                  .label=${0}
                  .disabled=${0}
                  .placeholder=${0}
                  .helper=${0}
                  .localizeValue=${0}
                  .required=${0}
                  .context=${0}
                ></ha-selector>`),e,this.hass,e.name,e.selector,k(this.data,e),this._computeLabel(e,this.data),e.disabled||this.disabled||!1,e.required?"":e.default,this._computeHelper(e),this.localizeValue,e.required||!1,this._generateContext(e)):(0,r.h)(this.fieldElementName(e.type),Object.assign({schema:e,data:k(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:null===(t=this.hass)||void 0===t?void 0:t.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e)},this.getFormProperties())))})))}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[i,n]of Object.entries(e.context))t[i]=this.data[n];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,o.Z)(i,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const i=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data=Object.assign(Object.assign({},this.data),i),(0,l.B)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?(0,a.dy)(m||(m=y`<ul>
        ${0}
      </ul>`),e.map((e=>(0,a.dy)(g||(g=y`<li>
              ${0}
            </li>`),this.computeError?this.computeError(e,t):e)))):this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"field",static:!0,key:"styles",value(){return(0,a.iv)(v||(v=y`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `))}}]}}),a.oi)},35189:function(e,t,i){"use strict";var n=i(73577),o=(i(71695),i(47021),i(57243)),a=i(50778),s=i(72621),r=(i(9656),i(92745),i(52805),i(69235),i(12385),i(19134),i(11740),i(97003),i(46692),i(39527),i(34595),i(86180));function l(e,t){return l=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},l(e,t)}i(52247);function d(){d=function(e,t){return new i(e,void 0,t)};var e=RegExp.prototype,t=new WeakMap;function i(e,n,o){var a=RegExp(e,n);return t.set(a,o||t.get(e)),l(a,i.prototype)}function n(e,i){var n=t.get(i);return Object.keys(n).reduce((function(t,i){var o=n[i];if("number"==typeof o)t[i]=e[o];else{for(var a=0;void 0===e[o[a]]&&a+1<o.length;)a++;t[i]=e[o[a]]}return t}),Object.create(null))}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&l(e,t)}(i,RegExp),i.prototype.exec=function(t){var i=e.exec.call(this,t);if(i){i.groups=n(i,this);var o=i.indices;o&&(o.groups=n(o,this))}return i},i.prototype[Symbol.replace]=function(i,o){if("string"==typeof o){var a=t.get(this);return e[Symbol.replace].call(this,i,o.replace(/\$<([^>]+)>/g,(function(e,t){var i=a[t];return"$"+(Array.isArray(i)?i.join("$"):i)})))}if("function"==typeof o){var s=this;return e[Symbol.replace].call(this,i,(function(){var e=arguments;return"object"!=(0,r.Z)(e[e.length-1])&&(e=[].slice.call(e)).push(n(e,s)),o.apply(this,e)}))}return e[Symbol.replace].call(this,i,o)},d.apply(this,arguments)}i(19083),i(40251),i(61006),i(99790),i(13334);var c=i(11297),h=(i(72700),i(8038),i(71513),i(75656),i(50100),i(18084),i(75351));let u;const p={reType:d(/((\[!(caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,{input:1,type:3}),typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};(0,n.Z)([(0,a.Mo)("ha-markdown-element")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[(0,a.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"allow-svg",type:Boolean})],key:"allowSvg",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"breaks",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value(){return!1}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"update",value:function(e){(0,s.Z)(n,"update",this,3)([e]),void 0!==this.content&&this._render()}},{kind:"method",key:"_render",value:async function(){this.innerHTML=await(async(e,t,n)=>(u||(u=(0,h.Ud)(new Worker(new URL(i.p+i.u("5845"),i.b)))),u.renderMarkdown(e,t,n)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg}),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const n=e.currentNode;if(n instanceof HTMLAnchorElement&&n.host!==document.location.host)n.target="_blank",n.rel="noreferrer noopener";else if(n instanceof HTMLImageElement)this.lazyImages&&(n.loading="lazy"),n.addEventListener("load",this._resize);else if(n instanceof HTMLQuoteElement){var t;const i=(null===(t=n.firstElementChild)||void 0===t||null===(t=t.firstChild)||void 0===t?void 0:t.textContent)&&p.reType.exec(n.firstElementChild.firstChild.textContent);if(i){const{type:t}=i.groups,o=document.createElement("ha-alert");o.alertType=p.typeToHaAlert[t.toLowerCase()],o.append(...Array.from(n.childNodes).map((e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){var n;const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===i.input&&null!==(n=e.textContent)&&void 0!==n&&n.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t})).reduce(((e,t)=>e.concat(t)),[]).filter((e=>e.textContent&&e.textContent!==i.input))),e.parentNode().replaceChild(o,n)}}else n instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(n.localName)&&i(61145)(`./${n.localName}`)}}},{kind:"field",key:"_resize",value(){return()=>(0,c.B)(this,"content-resize")}}]}}),o.fl);let f,m,g=e=>e;(0,n.Z)([(0,a.Mo)("ha-markdown")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"allow-svg",type:Boolean})],key:"allowSvg",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"breaks",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value(){return!1}},{kind:"method",key:"render",value:function(){return this.content?(0,o.dy)(f||(f=g`<ha-markdown-element
      .content=${0}
      .allowSvg=${0}
      .breaks=${0}
      .lazyImages=${0}
    ></ha-markdown-element>`),this.content,this.allowSvg,this.breaks,this.lazyImages):o.Ld}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(m||(m=g`
    :host {
      display: block;
    }
    ha-markdown-element {
      -ms-user-select: text;
      -webkit-user-select: text;
      -moz-user-select: text;
    }
    ha-markdown-element > *:first-child {
      margin-top: 0;
    }
    ha-markdown-element > *:last-child {
      margin-bottom: 0;
    }
    ha-alert {
      display: block;
      margin: 4px 0;
    }
    a {
      color: var(--primary-color);
    }
    img {
      max-width: 100%;
    }
    code,
    pre {
      background-color: var(--markdown-code-background-color, none);
      border-radius: 3px;
    }
    svg {
      background-color: var(--markdown-svg-background-color, none);
      color: var(--markdown-svg-color, none);
    }
    code {
      font-size: 85%;
      padding: 0.2em 0.4em;
    }
    pre code {
      padding: 0;
    }
    pre {
      padding: 16px;
      overflow: auto;
      line-height: 1.45;
      font-family: var(--code-font-family, monospace);
    }
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
      line-height: initial;
    }
    h2 {
      font-size: 1.5em;
      font-weight: bold;
    }
    hr {
      border-color: var(--divider-color);
      border-bottom: none;
      margin: 16px 0;
    }
  `))}}]}}),o.oi)},80495:function(e,t,i){"use strict";i.d(t,{Bg:()=>h,DT:()=>c,SY:()=>l,aJ:()=>s,cz:()=>r,ko:()=>d});var n=i(4468),o=i(36719);let a=function(e){return e[e.ANNOUNCE=1]="ANNOUNCE",e}({});const s=(e,t,i)=>e.connection.subscribeMessage(i,{type:"assist_satellite/intercept_wake_word",entity_id:t}),r=(e,t)=>e.callWS({type:"assist_satellite/test_connection",entity_id:t}),l=(e,t,i)=>e.callService("assist_satellite","announce",{message:i},{entity_id:t}),d=(e,t)=>e.callWS({type:"assist_satellite/get_configuration",entity_id:t}),c=(e,t,i)=>e.callWS({type:"assist_satellite/set_wake_words",entity_id:t,wake_word_ids:i}),h=e=>e&&e.state!==o.nZ&&(0,n.e)(e,a.ANNOUNCE)},41946:function(e,t,i){"use strict";i.d(t,{iI:()=>o,oT:()=>n});i(19083),i(77439),i(19423),i(40251),i(97499),i(61006),i(13334);const n=e=>e.map((e=>{if("string"!==e.type)return e;switch(e.name){case"username":return Object.assign(Object.assign({},e),{},{autocomplete:"username",autofocus:!0});case"password":return Object.assign(Object.assign({},e),{},{autocomplete:"current-password"});case"code":return Object.assign(Object.assign({},e),{},{autocomplete:"one-time-code",autofocus:!0});default:return e}})),o=(e,t)=>e.callWS({type:"auth/sign_path",path:t})},79983:function(e,t,i){"use strict";i.d(t,{D4:()=>a,D7:()=>d,Ky:()=>o,XO:()=>s,d4:()=>l,oi:()=>r});i(56587),i(1275);const n={"HA-Frontend-Base":`${location.protocol}//${location.host}`},o=(e,t,i)=>{var o;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(o=e.userData)||void 0===o?void 0:o.showAdvanced),entry_id:i},n)},a=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,n),s=(e,t,i)=>e.callApi("POST",`config/config_entries/flow/${t}`,i,n),r=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),l=(e,t)=>e.callApi("GET","config/config_entries/flow_handlers"+(t?`?type=${t}`:"")),d=e=>e.sendMessagePromise({type:"config_entries/flow/progress"})},83336:function(e,t,i){"use strict";i.d(t,{X:()=>n});const n=(e,t)=>e.subscribeEvents(t,"data_entry_flow_progressed")},36719:function(e,t,i){"use strict";i.d(t,{ON:()=>s,PX:()=>r,V_:()=>l,lz:()=>a,nZ:()=>o,rk:()=>c});var n=i(95907);const o="unavailable",a="unknown",s="on",r="off",l=[o,a],d=[o,a,r],c=(0,n.z)(l);(0,n.z)(d)},44699:function(e,t,i){"use strict";i.d(t,{H:()=>o,O:()=>a});i(19083);const n=["generic_camera","template"],o=(e,t,i,n,o,a)=>e.connection.subscribeMessage(a,{type:`${t}/start_preview`,flow_id:i,flow_type:n,user_input:o}),a=e=>n.includes(e)?e:"generic"},22975:function(e,t,i){"use strict";i.a(e,(async function(e,n){try{i.r(t);var o=i(73577),a=i(72621),s=(i(19083),i(71695),i(77439),i(40251),i(47021),i(31622),i(57243)),r=i(50778),l=i(11297),d=(i(90977),i(44118),i(59897),i(83336)),c=i(66193),h=i(26205),u=i(4557),p=(i(76085),i(27599)),f=(i(12924),i(41178),i(45385),i(29065),i(72959),e([p]));p=(f.then?(await f)():f)[0];let m,g,v,y,w,k,_,b,$,C,x,S=e=>e;const z="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",E="M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z";let F=0;(0,o.Z)([(0,r.Mo)("dialog-data-entry-flow")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_loading",value:void 0},{kind:"field",key:"_instance",value(){return F}},{kind:"field",decorators:[(0,r.SB)()],key:"_step",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_handler",value:void 0},{kind:"field",key:"_unsubDataEntryFlowProgressed",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._instance=F++;const t=this._instance;let i;if(e.startFlowHandler){this._loading="loading_flow",this._handler=e.startFlowHandler;try{i=await this._params.flowConfig.createFlow(this.hass,e.startFlowHandler)}catch(n){this.closeDialog();let e=n.message||n.body||"Unknown error";return"string"!=typeof e&&(e=JSON.stringify(e)),void(0,u.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${e}`})}if(t!==this._instance)return}else{if(!e.continueFlowId)return;this._loading="loading_flow";try{i=await e.flowConfig.fetchFlow(this.hass,e.continueFlowId)}catch(n){this.closeDialog();let e=n.message||n.body||"Unknown error";return"string"!=typeof e&&(e=JSON.stringify(e)),void(0,u.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${e}`})}}t===this._instance&&(this._processStep(i),this._loading=void 0)}},{kind:"method",key:"closeDialog",value:function(){if(!this._params)return;const e=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));var t;(!this._step||e||this._params.continueFlowId||this._params.flowConfig.deleteFlow(this.hass,this._step.flow_id),this._step&&this._params.dialogClosedCallback)&&this._params.dialogClosedCallback({flowFinished:e,entryId:"result"in this._step?null===(t=this._step.result)||void 0===t?void 0:t.entry_id:void 0});this._loading=void 0,this._step=void 0,this._params=void 0,this._handler=void 0,this._unsubDataEntryFlowProgressed&&(this._unsubDataEntryFlowProgressed.then((e=>{e()})),this._unsubDataEntryFlowProgressed=void 0),(0,l.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){var e,t,i,n;return this._params?(0,s.dy)(m||(m=S`
      <ha-dialog
        open
        @closed=${0}
        scrimClickAction
        escapeKeyAction
        hideActions
      >
        <div>
          ${0}
        </div>
      </ha-dialog>
    `),this.closeDialog,this._loading||null===this._step?(0,s.dy)(g||(g=S`
                <step-flow-loading
                  .flowConfig=${0}
                  .hass=${0}
                  .loadingReason=${0}
                  .handler=${0}
                  .step=${0}
                ></step-flow-loading>
              `),this._params.flowConfig,this.hass,this._loading,this._handler,this._step):void 0===this._step?"":(0,s.dy)(v||(v=S`
                  <div class="dialog-actions">
                    ${0}
                    <ha-icon-button
                      .label=${0}
                      .path=${0}
                      dialogAction="close"
                    ></ha-icon-button>
                  </div>
                  ${0}
                `),["form","menu","external","progress","data_entry_flow_progressed"].includes(null===(e=this._step)||void 0===e?void 0:e.type)&&null!==(t=this._params.manifest)&&void 0!==t&&t.is_built_in||null!==(i=this._params.manifest)&&void 0!==i&&i.documentation?(0,s.dy)(y||(y=S`
                          <a
                            href=${0}
                            target="_blank"
                            rel="noreferrer noopener"
                          >
                            <ha-icon-button
                              .label=${0}
                              .path=${0}
                            >
                            </ha-icon-button
                          ></a>
                        `),this._params.manifest.is_built_in?(0,h.R)(this.hass,`/integrations/${this._params.manifest.domain}`):null===(n=this._params)||void 0===n||null===(n=n.manifest)||void 0===n?void 0:n.documentation,this.hass.localize("ui.common.help"),E):"",this.hass.localize("ui.panel.config.integrations.config_flow.dismiss"),z,"form"===this._step.type?(0,s.dy)(w||(w=S`
                        <step-flow-form
                          .flowConfig=${0}
                          .step=${0}
                          .hass=${0}
                        ></step-flow-form>
                      `),this._params.flowConfig,this._step,this.hass):"external"===this._step.type?(0,s.dy)(k||(k=S`
                          <step-flow-external
                            .flowConfig=${0}
                            .step=${0}
                            .hass=${0}
                          ></step-flow-external>
                        `),this._params.flowConfig,this._step,this.hass):"abort"===this._step.type?(0,s.dy)(_||(_=S`
                            <step-flow-abort
                              .params=${0}
                              .step=${0}
                              .hass=${0}
                              .domain=${0}
                            ></step-flow-abort>
                          `),this._params,this._step,this.hass,this._step.handler):"progress"===this._step.type?(0,s.dy)(b||(b=S`
                              <step-flow-progress
                                .flowConfig=${0}
                                .step=${0}
                                .hass=${0}
                              ></step-flow-progress>
                            `),this._params.flowConfig,this._step,this.hass):"menu"===this._step.type?(0,s.dy)($||($=S`
                                <step-flow-menu
                                  .flowConfig=${0}
                                  .step=${0}
                                  .hass=${0}
                                ></step-flow-menu>
                              `),this._params.flowConfig,this._step,this.hass):(0,s.dy)(C||(C=S`
                                <step-flow-create-entry
                                  .flowConfig=${0}
                                  .step=${0}
                                  .hass=${0}
                                ></step-flow-create-entry>
                              `),this._params.flowConfig,this._step,this.hass))):s.Ld}},{kind:"method",key:"firstUpdated",value:function(e){(0,a.Z)(i,"firstUpdated",this,3)([e]),this.addEventListener("flow-update",(e=>{const{step:t,stepPromise:i}=e.detail;this._processStep(t||i)}))}},{kind:"method",key:"willUpdate",value:function(e){(0,a.Z)(i,"willUpdate",this,3)([e]),e.has("_step")&&this._step&&["external","progress"].includes(this._step.type)&&this._subscribeDataEntryFlowProgressed()}},{kind:"method",key:"_processStep",value:async function(e){if(void 0===e)return void this.closeDialog();let t;this._loading="loading_step";try{t=await e}catch(n){var i;return this.closeDialog(),void(0,u.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:null==n||null===(i=n.body)||void 0===i?void 0:i.message})}finally{this._loading=void 0}this._step=void 0,await this.updateComplete,this._step=t}},{kind:"method",key:"_subscribeDataEntryFlowProgressed",value:async function(){this._unsubDataEntryFlowProgressed||(this._unsubDataEntryFlowProgressed=(0,d.X)(this.hass.connection,(async e=>{var t;e.data.flow_id===(null===(t=this._step)||void 0===t?void 0:t.flow_id)&&this._processStep(this._params.flowConfig.fetchFlow(this.hass,this._step.flow_id))})))}},{kind:"get",static:!0,key:"styles",value:function(){return[c.yu,(0,s.iv)(x||(x=S`
        ha-dialog {
          --dialog-content-padding: 0;
        }
        .dialog-actions {
          padding: 16px;
          position: absolute;
          top: 0;
          right: 0;
          inset-inline-start: initial;
          inset-inline-end: 0px;
          direction: var(--direction);
        }
        .dialog-actions > * {
          color: var(--secondary-text-color);
        }
      `))]}}]}}),s.oi);n()}catch(m){n(m)}}))},18694:function(e,t,i){"use strict";i.d(t,{t:()=>v});i(63721),i(71695),i(40251),i(47021);var n=i(57243),o=i(79983),a=i(1275),s=i(43373);let r,l,d,c,h,u,p,f,m,g=e=>e;const v=(e,t)=>(0,s.w)(e,t,{flowType:"config_flow",showDevices:!0,createFlow:async(e,i)=>{const[n]=await Promise.all([(0,o.Ky)(e,i,t.entryId),e.loadFragmentTranslation("config"),e.loadBackendTranslation("config",i),e.loadBackendTranslation("selector",i),e.loadBackendTranslation("title",i)]);return n},fetchFlow:async(e,t)=>{const i=await(0,o.D4)(e,t);return await e.loadFragmentTranslation("config"),await e.loadBackendTranslation("config",i.handler),await e.loadBackendTranslation("selector",i.handler),i},handleFlowStep:o.XO,deleteFlow:o.oi,renderAbortDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?(0,n.dy)(r||(r=g`
            <ha-markdown allow-svg breaks .content=${0}></ha-markdown>
          `),i):t.reason},renderShowFormStepHeader(e,t){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.title`,t.description_placeholders)||e.localize(`component.${t.handler}.title`)},renderShowFormStepDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?(0,n.dy)(l||(l=g`
            <ha-markdown allow-svg breaks .content=${0}></ha-markdown>
          `),i):""},renderShowFormStepFieldLabel(e,t,i,n){var o;if("expandable"===i.type)return e.localize(`component.${t.handler}.config.step.${t.step_id}.sections.${i.name}.name`);const a=null!=n&&null!==(o=n.path)&&void 0!==o&&o[0]?`sections.${n.path[0]}.`:"";return e.localize(`component.${t.handler}.config.step.${t.step_id}.${a}data.${i.name}`)||i.name},renderShowFormStepFieldHelper(e,t,i,o){var a;if("expandable"===i.type)return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.sections.${i.name}.description`);const s=null!=o&&null!==(a=o.path)&&void 0!==a&&a[0]?`sections.${o.path[0]}.`:"",r=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.${s}data_description.${i.name}`,t.description_placeholders);return r?(0,n.dy)(d||(d=g`<ha-markdown breaks .content=${0}></ha-markdown>`),r):""},renderShowFormStepFieldError(e,t,i){return e.localize(`component.${t.translation_domain||t.translation_domain||t.handler}.config.error.${i}`,t.description_placeholders)||i},renderShowFormStepFieldLocalizeValue(e,t,i){return e.localize(`component.${t.handler}.selector.${i}`)},renderShowFormStepSubmitButton(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===t.last_step?"next":"submit"))},renderExternalStepHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site")},renderExternalStepDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.${t.step_id}.description`,t.description_placeholders);return(0,n.dy)(c||(c=g`
        <p>
          ${0}
        </p>
        ${0}
      `),e.localize("ui.panel.config.integrations.config_flow.external_step.description"),i?(0,n.dy)(h||(h=g`
              <ha-markdown
                allow-svg
                breaks
                .content=${0}
              ></ha-markdown>
            `),i):"")},renderCreateEntryDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return(0,n.dy)(u||(u=g`
        ${0}
        <p>
          ${0}
        </p>
      `),i?(0,n.dy)(p||(p=g`
              <ha-markdown
                allow-svg
                breaks
                .content=${0}
              ></ha-markdown>
            `),i):"",e.localize("ui.panel.config.integrations.config_flow.created_config",{name:t.title}))},renderShowFormProgressHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`)},renderShowFormProgressDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return i?(0,n.dy)(f||(f=g`
            <ha-markdown allow-svg breaks .content=${0}></ha-markdown>
          `),i):""},renderMenuHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`)},renderMenuDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?(0,n.dy)(m||(m=g`
            <ha-markdown allow-svg breaks .content=${0}></ha-markdown>
          `),i):""},renderMenuOption(e,t,i){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.menu_options.${i}`,t.description_placeholders)},renderLoadingDescription(e,t,i,n){if("loading_flow"!==t&&"loading_step"!==t)return"";const o=(null==n?void 0:n.handler)||i;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:o?(0,a.Lh)(e.localize,o):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},76085:function(e,t,i){"use strict";var n=i(73577),o=i(72621),a=(i(71695),i(40251),i(47021),i(31622),i(57243)),s=i(50778),r=i(11297);const l=()=>i.e("2138").then(i.bind(i,41088));var d=i(18694),c=i(95204);let h,u=e=>e;(0,n.Z)([(0,s.Mo)("step-flow-abort")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"params",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"domain",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)(i,"firstUpdated",this,3)([e]),"missing_credentials"===this.step.reason&&this._handleMissingCreds()}},{kind:"method",key:"render",value:function(){return"missing_credentials"===this.step.reason?a.Ld:(0,a.dy)(h||(h=u`
      <h2>
        ${0}
      </h2>
      <div class="content">
        ${0}
      </div>
      <div class="buttons">
        <mwc-button @click=${0}
          >${0}</mwc-button
        >
      </div>
    `),this.params.flowConfig.renderAbortHeader?this.params.flowConfig.renderAbortHeader(this.hass,this.step):this.hass.localize(`component.${this.domain}.title`),this.params.flowConfig.renderAbortDescription(this.hass,this.step),this._flowDone,this.hass.localize("ui.panel.config.integrations.config_flow.close"))}},{kind:"method",key:"_handleMissingCreds",value:async function(){var e,t;e=this.params.dialogParentElement,t={selectedDomain:this.domain,manifest:this.params.manifest,applicationCredentialAddedCallback:()=>{var e;(0,d.t)(this.params.dialogParentElement,{dialogClosedCallback:this.params.dialogClosedCallback,startFlowHandler:this.domain,showAdvanced:null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced})}},(0,r.B)(e,"show-dialog",{dialogTag:"dialog-add-application-credential",dialogImport:l,dialogParams:t}),this._flowDone()}},{kind:"method",key:"_flowDone",value:function(){(0,r.B)(this,"flow-update",{step:void 0})}},{kind:"get",static:!0,key:"styles",value:function(){return c.i}}]}}),a.oi)},27599:function(e,t,i){"use strict";i.a(e,(async function(e,t){try{var n=i(73577),o=(i(19083),i(71695),i(40251),i(61006),i(39527),i(99790),i(13334),i(36993),i(47021),i(31622),i(57243)),a=i(50778),s=i(27486),r=i(11297),l=i(79575),d=i(69181),c=i(80495),h=i(92374),u=i(4557),p=i(4383),f=i(95204),m=e([d]);d=(m.then?(await m)():m)[0];let g,v,y,w,k,_,b,$,C=e=>e;(0,n.Z)([(0,a.Mo)("step-flow-create-entry")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"field",key:"_devices",value(){return(0,s.Z)(((e,t,i)=>e&&i?t.filter((e=>e.config_entries.includes(i))):[]))}},{kind:"field",key:"_deviceEntities",value(){return(0,s.Z)(((e,t,i)=>t.filter((t=>t.device_id===e&&(!i||(0,l.M)(t.entity_id)===i)))))}},{kind:"method",key:"willUpdate",value:function(e){var t,i;if(!e.has("devices")&&!e.has("hass"))return;const n=this._devices(this.flowConfig.showDevices,Object.values(this.hass.devices),null===(t=this.step.result)||void 0===t?void 0:t.entry_id);if(1!==n.length||n[0].primary_config_entry!==(null===(i=this.step.result)||void 0===i?void 0:i.entry_id))return;const o=this._deviceEntities(n[0].id,Object.values(this.hass.entities),"assist_satellite");o.length&&o.some((e=>(0,c.Bg)(this.hass.states[e.entity_id])))&&(this._flowDone(),(0,p.k)(this,{deviceId:n[0].id}))}},{kind:"method",key:"render",value:function(){var e,t;const i=this.hass.localize,n=this._devices(this.flowConfig.showDevices,Object.values(this.hass.devices),null===(e=this.step.result)||void 0===e?void 0:e.entry_id);return(0,o.dy)(g||(g=C`
      <h2>${0}!</h2>
      <div class="content">
        ${0}
        ${0}
        ${0}
      </div>
      <div class="buttons">
        <mwc-button @click=${0}
          >${0}</mwc-button
        >
      </div>
    `),i("ui.panel.config.integrations.config_flow.success"),this.flowConfig.renderCreateEntryDescription(this.hass,this.step),"not_loaded"===(null===(t=this.step.result)||void 0===t?void 0:t.state)?(0,o.dy)(v||(v=C`<span class="error"
              >${0}</span
            >`),i("ui.panel.config.integrations.config_flow.not_loaded")):o.Ld,0===n.length?o.Ld:(0,o.dy)(y||(y=C`
              <p>
                ${0}:
              </p>
              <div class="devices">
                ${0}
              </div>
            `),i("ui.panel.config.integrations.config_flow.found_following_devices"),n.map((e=>{var t;return(0,o.dy)(w||(w=C`
                    <div class="device">
                      <div>
                        <b>${0}</b><br />
                        ${0}
                      </div>
                      <ha-area-picker
                        .hass=${0}
                        .device=${0}
                        .value=${0}
                        @value-changed=${0}
                      ></ha-area-picker>
                    </div>
                  `),(0,h.jL)(e,this.hass),e.model||e.manufacturer?(0,o.dy)(_||(_=C`${0}
                            ${0}`),e.model,e.manufacturer?(0,o.dy)(b||(b=C`(${0})`),e.manufacturer):""):(0,o.dy)(k||(k=C`&nbsp;`)),this.hass,e.id,null!==(t=e.area_id)&&void 0!==t?t:void 0,this._areaPicked)}))),this._flowDone,i("ui.panel.config.integrations.config_flow.finish"))}},{kind:"method",key:"_flowDone",value:function(){(0,r.B)(this,"flow-update",{step:void 0})}},{kind:"method",key:"_areaPicked",value:async function(e){const t=e.currentTarget,i=t.device,n=e.detail.value;try{await(0,h.t1)(this.hass,i,{area_id:n})}catch(o){(0,u.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_flow.error_saving_area",{error:o.message})}),t.value=null}}},{kind:"get",static:!0,key:"styles",value:function(){return[f.i,(0,o.iv)($||($=C`
        .devices {
          display: flex;
          flex-wrap: wrap;
          margin: -4px;
          max-height: 600px;
          overflow-y: auto;
        }
        .device {
          border: 1px solid var(--divider-color);
          padding: 5px;
          border-radius: 4px;
          margin: 4px;
          display: inline-block;
          width: 250px;
        }
        .buttons > *:last-child {
          margin-left: auto;
          margin-inline-start: auto;
          margin-inline-end: initial;
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          .device {
            width: 100%;
          }
        }
        .error {
          color: var(--error-color);
        }
      `))]}}]}}),o.oi);t()}catch(g){t(g)}}))},12924:function(e,t,i){"use strict";var n=i(73577),o=i(72621),a=(i(71695),i(47021),i(31622),i(57243)),s=i(50778),r=i(95204);let l,d,c=e=>e;(0,n.Z)([(0,s.Mo)("step-flow-external")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){const e=this.hass.localize;return(0,a.dy)(l||(l=c`
      <h2>${0}</h2>
      <div class="content">
        ${0}
        <div class="open-button">
          <a href=${0} target="_blank" rel="noreferrer">
            <mwc-button raised>
              ${0}
            </mwc-button>
          </a>
        </div>
      </div>
    `),this.flowConfig.renderExternalStepHeader(this.hass,this.step),this.flowConfig.renderExternalStepDescription(this.hass,this.step),this.step.url,e("ui.panel.config.integrations.config_flow.external_step.open_site"))}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)(i,"firstUpdated",this,3)([e]),window.open(this.step.url)}},{kind:"get",static:!0,key:"styles",value:function(){return[r.i,(0,a.iv)(d||(d=c`
        .open-button {
          text-align: center;
          padding: 24px 0;
        }
        .open-button a {
          text-decoration: none;
        }
      `))]}}]}}),a.oi)},41178:function(e,t,i){"use strict";var n=i(73577),o=i(72621),a=(i(19083),i(71695),i(19423),i(40251),i(61006),i(39527),i(92181),i(67670),i(41360),i(47021),i(14394),i(31622),i(57243)),s=i(50778),r=i(38653),l=i(11297);i(17949),i(90977);var d=i(12328),c=(i(42877),i(35189),i(41946)),h=i(95204),u=i(66193),p=i(44699);let f,m,g,v,y,w,k=e=>e;(0,n.Z)([(0,s.Mo)("step-flow-form")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_loading",value(){return!1}},{kind:"field",decorators:[(0,s.SB)()],key:"_stepData",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_errorMsg",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)(n,"disconnectedCallback",this,3)([]),this.removeEventListener("keydown",this._handleKeyDown)}},{kind:"method",key:"render",value:function(){const e=this.step,t=this._stepDataProcessed;return(0,a.dy)(f||(f=k`
      <h2>${0}</h2>
      <div class="content" @click=${0}>
        ${0}
        ${0}
        <ha-form
          .hass=${0}
          .data=${0}
          .disabled=${0}
          @value-changed=${0}
          .schema=${0}
          .error=${0}
          .computeLabel=${0}
          .computeHelper=${0}
          .computeError=${0}
          .localizeValue=${0}
        ></ha-form>
      </div>
      ${0}
      <div class="buttons">
        ${0}
      </div>
    `),this.flowConfig.renderShowFormStepHeader(this.hass,this.step),this._clickHandler,this.flowConfig.renderShowFormStepDescription(this.hass,this.step),this._errorMsg?(0,a.dy)(m||(m=k`<ha-alert alert-type="error">${0}</ha-alert>`),this._errorMsg):"",this.hass,t,this._loading,this._stepDataChanged,(0,c.oT)(e.data_schema),e.errors,this._labelCallback,this._helperCallback,this._errorCallback,this._localizeValueCallback,e.preview?(0,a.dy)(g||(g=k`<div class="preview" @set-flow-errors=${0}>
            <h3>
              ${0}:
            </h3>
            ${0}
          </div>`),this._setError,this.hass.localize("ui.panel.config.integrations.config_flow.preview"),(0,r.h)(`flow-preview-${(0,p.O)(e.preview)}`,{hass:this.hass,domain:e.preview,flowType:this.flowConfig.flowType,handler:e.handler,stepId:e.step_id,flowId:e.flow_id,stepData:t})):a.Ld,this._loading?(0,a.dy)(v||(v=k`
              <div class="submit-spinner">
                <ha-circular-progress indeterminate></ha-circular-progress>
              </div>
            `)):(0,a.dy)(y||(y=k`
              <div>
                <mwc-button @click=${0}>
                  ${0}
                </mwc-button>
              </div>
            `),this._submitStep,this.flowConfig.renderShowFormStepSubmitButton(this.hass,this.step)))}},{kind:"method",key:"_setError",value:function(e){this.step=Object.assign(Object.assign({},this.step),{},{errors:e.detail})}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)(n,"firstUpdated",this,3)([e]),setTimeout((()=>this.shadowRoot.querySelector("ha-form").focus()),0),this.addEventListener("keydown",this._handleKeyDown)}},{kind:"method",key:"willUpdate",value:function(e){var t;(0,o.Z)(n,"willUpdate",this,3)([e]),e.has("step")&&null!==(t=this.step)&&void 0!==t&&t.preview&&i(2292)(`./flow-preview-${(0,p.O)(this.step.preview)}`)}},{kind:"method",key:"_clickHandler",value:function(e){((e,t=!0)=>{if(e.defaultPrevented||0!==e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;const i=e.composedPath().find((e=>"A"===e.tagName));if(!i||i.target||i.hasAttribute("download")||"external"===i.getAttribute("rel"))return;let n=i.href;if(!n||-1!==n.indexOf("mailto:"))return;const o=window.location,a=o.origin||o.protocol+"//"+o.host;return 0===n.indexOf(a)&&(n=n.substr(a.length),"#"!==n)?(t&&e.preventDefault(),n):void 0})(e,!1)&&(0,l.B)(this,"flow-update",{step:void 0})}},{kind:"field",key:"_handleKeyDown",value(){return e=>{"Enter"===e.key&&this._submitStep()}}},{kind:"get",key:"_stepDataProcessed",value:function(){return void 0!==this._stepData||(this._stepData=(0,d.x)(this.step.data_schema)),this._stepData}},{kind:"method",key:"_submitStep",value:async function(){const e=this._stepData||{};if(!(void 0===e?void 0===this.step.data_schema.find((e=>e.required)):e&&this.step.data_schema.every((t=>!t.required||!["",void 0].includes(e[t.name])))))return void(this._errorMsg=this.hass.localize("ui.panel.config.integrations.config_flow.not_all_required_fields"));this._loading=!0,this._errorMsg=void 0;const t=this.step.flow_id,i={};Object.keys(e).forEach((t=>{const n=e[t];[void 0,""].includes(n)||(i[t]=n)}));try{const e=await this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,i);if(!this.step||t!==this.step.flow_id)return;(0,l.B)(this,"flow-update",{step:e})}catch(n){n&&n.body?(n.body.message&&(this._errorMsg=n.body.message),n.body.errors&&(this.step=Object.assign(Object.assign({},this.step),{},{errors:n.body.errors})),n.body.message||n.body.errors||(this._errorMsg="Unknown error occurred")):this._errorMsg="Unknown error occurred"}finally{this._loading=!1}}},{kind:"method",key:"_stepDataChanged",value:function(e){this._stepData=e.detail.value}},{kind:"field",key:"_labelCallback",value(){return(e,t,i)=>this.flowConfig.renderShowFormStepFieldLabel(this.hass,this.step,e,i)}},{kind:"field",key:"_helperCallback",value(){return(e,t)=>this.flowConfig.renderShowFormStepFieldHelper(this.hass,this.step,e,t)}},{kind:"field",key:"_errorCallback",value(){return e=>this.flowConfig.renderShowFormStepFieldError(this.hass,this.step,e)}},{kind:"field",key:"_localizeValueCallback",value(){return e=>this.flowConfig.renderShowFormStepFieldLocalizeValue(this.hass,this.step,e)}},{kind:"get",static:!0,key:"styles",value:function(){return[u.Qx,h.i,(0,a.iv)(w||(w=k`
        .error {
          color: red;
        }

        .submit-spinner {
          margin-right: 16px;
          margin-inline-end: 16px;
          margin-inline-start: initial;
        }

        ha-alert,
        ha-form {
          margin-top: 24px;
          display: block;
        }
        h2 {
          word-break: break-word;
          padding-inline-end: 72px;
          direction: var(--direction);
        }
      `))]}}]}}),a.oi)},45385:function(e,t,i){"use strict";var n=i(73577),o=(i(71695),i(47021),i(57243)),a=i(50778);i(90977);let s,r,l,d=e=>e;(0,n.Z)([(0,a.Mo)("step-flow-loading")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"loadingReason",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"handler",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){const e=this.flowConfig.renderLoadingDescription(this.hass,this.loadingReason,this.handler,this.step);return(0,o.dy)(s||(s=d`
      <div class="init-spinner">
        ${0}
        <ha-circular-progress indeterminate></ha-circular-progress>
      </div>
    `),e?(0,o.dy)(r||(r=d`<div>${0}</div>`),e):"")}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(l||(l=d`
    .init-spinner {
      padding: 50px 100px;
      text-align: center;
    }
    ha-circular-progress {
      margin-top: 16px;
    }
  `))}}]}}),o.oi)},29065:function(e,t,i){"use strict";var n=i(73577),o=(i(71695),i(13334),i(47021),i(87319),i(57243)),a=i(50778),s=(i(54220),i(95204)),r=i(11297);let l,d,c,h,u=e=>e;(0,n.Z)([(0,a.Mo)("step-flow-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){let e,t;if(Array.isArray(this.step.menu_options)){e=this.step.menu_options,t={};for(const i of e)t[i]=this.flowConfig.renderMenuOption(this.hass,this.step,i)}else e=Object.keys(this.step.menu_options),t=this.step.menu_options;const i=this.flowConfig.renderMenuDescription(this.hass,this.step);return(0,o.dy)(l||(l=u`
      <h2>${0}</h2>
      ${0}
      <div class="options">
        ${0}
      </div>
    `),this.flowConfig.renderMenuHeader(this.hass,this.step),i?(0,o.dy)(d||(d=u`<div class="content">${0}</div>`),i):"",e.map((e=>(0,o.dy)(c||(c=u`
            <mwc-list-item hasMeta .step=${0} @click=${0}>
              <span>${0}</span>
              <ha-icon-next slot="meta"></ha-icon-next>
            </mwc-list-item>
          `),e,this._handleStep,t[e]))))}},{kind:"method",key:"_handleStep",value:function(e){(0,r.B)(this,"flow-update",{stepPromise:this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,{next_step_id:e.currentTarget.step})})}},{kind:"field",static:!0,key:"styles",value(){return[s.i,(0,o.iv)(h||(h=u`
      .options {
        margin-top: 20px;
        margin-bottom: 8px;
      }
      .content {
        padding-bottom: 16px;
        border-bottom: 1px solid var(--divider-color);
      }
      .content + .options {
        margin-top: 8px;
      }
      mwc-list-item {
        --mdc-list-side-padding: 24px;
      }
    `))]}}]}}),o.oi)},72959:function(e,t,i){"use strict";var n=i(73577),o=(i(71695),i(47021),i(31622),i(57243)),a=i(50778),s=(i(90977),i(95204));let r,l,d=e=>e;(0,n.Z)([(0,a.Mo)("step-flow-progress")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){return(0,o.dy)(r||(r=d`
      <h2>
        ${0}
      </h2>
      <div class="content">
        <ha-circular-progress indeterminate></ha-circular-progress>
        ${0}
      </div>
    `),this.flowConfig.renderShowFormProgressHeader(this.hass,this.step),this.flowConfig.renderShowFormProgressDescription(this.hass,this.step))}},{kind:"get",static:!0,key:"styles",value:function(){return[s.i,(0,o.iv)(l||(l=d`
        .content {
          padding: 50px 100px;
          text-align: center;
        }
        ha-circular-progress {
          margin-bottom: 16px;
        }
      `))]}}]}}),o.oi)},95204:function(e,t,i){"use strict";i.d(t,{i:()=>o});let n;const o=(0,i(57243).iv)(n||(n=(e=>e)`
  h2 {
    margin: 24px 38px 0 0;
    margin-inline-start: 0px;
    margin-inline-end: 38px;
    padding: 0 24px;
    padding-inline-start: 24px;
    padding-inline-end: 24px;
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    font-family: var(
      --mdc-typography-headline6-font-family,
      var(--mdc-typography-font-family, Roboto, sans-serif)
    );
    font-size: var(--mdc-typography-headline6-font-size, 1.25rem);
    line-height: var(--mdc-typography-headline6-line-height, 2rem);
    font-weight: var(--mdc-typography-headline6-font-weight, 500);
    letter-spacing: var(--mdc-typography-headline6-letter-spacing, 0.0125em);
    text-decoration: var(--mdc-typography-headline6-text-decoration, inherit);
    text-transform: var(--mdc-typography-headline6-text-transform, inherit);
    box-sizing: border-box;
  }

  .content,
  .preview {
    margin-top: 20px;
    padding: 0 24px;
  }

  .buttons {
    position: relative;
    padding: 8px 16px 8px 24px;
    margin: 8px 0 0;
    color: var(--primary-color);
    display: flex;
    justify-content: flex-end;
  }

  ha-markdown {
    overflow-wrap: break-word;
  }
  ha-markdown a {
    color: var(--primary-color);
  }
  ha-markdown img:first-child:last-child {
    display: block;
    margin: 0 auto;
  }
`))},4383:function(e,t,i){"use strict";i.d(t,{k:()=>a});i(71695),i(40251),i(47021);var n=i(11297);const o=()=>Promise.all([i.e("4224"),i.e("7493"),i.e("676"),i.e("6160"),i.e("3732")]).then(i.bind(i,66738)),a=(e,t)=>{(0,n.B)(e,"show-dialog",{dialogTag:"ha-voice-assistant-setup-dialog",dialogImport:o,dialogParams:t})}},26205:function(e,t,i){"use strict";i.d(t,{R:()=>n});i(19083),i(61006);const n=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`},9656:function(e,t,i){"use strict";i(17954)("replace")}}]);
//# sourceMappingURL=9045.06784e7a7c1af916.js.map