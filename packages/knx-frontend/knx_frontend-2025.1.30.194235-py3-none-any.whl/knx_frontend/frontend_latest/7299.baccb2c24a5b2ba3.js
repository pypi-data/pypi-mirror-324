export const ids=["7299"];export const modules={61145:function(e,t,i){var n={"./ha-icon":["86267","3377"],"./ha-icon-button-toggle":["25152","5291"],"./ha-svg-icon":["10508"],"./ha-icon-button-group":["52100","1744"],"./ha-svg-icon.ts":["10508"],"./ha-icon.ts":["86267","3377"],"./ha-icon-overflow-menu":["65099","6718"],"./ha-icon-next":["54220"],"./ha-icon-picker":["73979","348"],"./ha-qr-code.ts":["9643","3750","1442"],"./ha-icon-button-arrow-prev.ts":["92500"],"./ha-icon-button-arrow-prev":["92500"],"./ha-icon-overflow-menu.ts":["65099","6718"],"./ha-alert":["17949"],"./ha-icon-button-next":["63448","3666"],"./ha-icon-button":["59897"],"./ha-icon-button-next.ts":["63448","3666"],"./ha-icon-picker.ts":["73979","348"],"./ha-icon-button-group.ts":["52100","1744"],"./ha-icon-button-toggle.ts":["25152","5291"],"./ha-icon-button-arrow-next.ts":["63922","852"],"./ha-icon-button-prev.ts":["3961","170"],"./ha-icon-prev":["78716","6470"],"./ha-icon-prev.ts":["78716","6470"],"./ha-icon-button.ts":["59897"],"./ha-alert.ts":["17949"],"./ha-icon-button-prev":["3961","170"],"./ha-qr-code":["9643","3750","1442"],"./ha-icon-next.ts":["54220"],"./ha-icon-button-arrow-next":["63922","852"]};function o(e){if(!i.o(n,e))return Promise.resolve().then((function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}));var t=n[e],o=t[0];return Promise.all(t.slice(1).map(i.e)).then((function(){return i(o)}))}o.keys=()=>Object.keys(n),o.id=61145,e.exports=o},2292:function(e,t,i){var n={"./flow-preview-generic.ts":["7433","4224","2973","6160","4284","9478","669"],"./flow-preview-generic_camera.ts":["96738","4224","2973","6160","4284","9478","9336"],"./flow-preview-generic":["7433","4224","2973","6160","4284","9478","669"],"./flow-preview-generic_camera":["96738","4224","2973","6160","4284","9478","9336"],"./flow-preview-template.ts":["76144","4224","2973","6160","4284","9478","8063"],"./flow-preview-template":["76144","4224","2973","6160","4284","9478","8063"]};function o(e){if(!i.o(n,e))return Promise.resolve().then((function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}));var t=n[e],o=t[0];return Promise.all(t.slice(1).map(i.e)).then((function(){return i(o)}))}o.keys=()=>Object.keys(n),o.id=2292,e.exports=o},12328:function(e,t,i){i.d(t,{x:()=>n});const n=e=>{const t={};return e.forEach((e=>{if(void 0!==e.description?.suggested_value&&null!==e.description?.suggested_value)t[e.name]=e.description.suggested_value;else if("default"in e)t[e.name]=e.default;else if(e.required){if("boolean"===e.type)t[e.name]=!1;else if("string"===e.type)t[e.name]="";else if("integer"===e.type)t[e.name]="valueMin"in e?e.valueMin:0;else if("constant"===e.type)t[e.name]=e.value;else if("float"===e.type)t[e.name]=0;else if("select"===e.type){if(e.options.length){const i=e.options[0];t[e.name]=Array.isArray(i)?i[0]:i}}else if("positive_time_period_dict"===e.type)t[e.name]={hours:0,minutes:0,seconds:0};else if("expandable"===e.type)t[e.name]=n(e.schema);else if("selector"in e){const i=e.selector;if("device"in i)t[e.name]=i.device?.multiple?[]:"";else if("entity"in i)t[e.name]=i.entity?.multiple?[]:"";else if("area"in i)t[e.name]=i.area?.multiple?[]:"";else if("label"in i)t[e.name]=i.label?.multiple?[]:"";else if("boolean"in i)t[e.name]=!1;else if("addon"in i||"attribute"in i||"file"in i||"icon"in i||"template"in i||"text"in i||"theme"in i||"object"in i)t[e.name]="";else if("number"in i)t[e.name]=i.number?.min??0;else if("select"in i){if(i.select?.options.length){const n=i.select.options[0],o="string"==typeof n?n:n.value;t[e.name]=i.select.multiple?[o]:o}}else if("country"in i)i.country?.countries?.length&&(t[e.name]=i.country.countries[0]);else if("language"in i)i.language?.languages?.length&&(t[e.name]=i.language.languages[0]);else if("duration"in i)t[e.name]={hours:0,minutes:0,seconds:0};else if("time"in i)t[e.name]="00:00:00";else if("date"in i||"datetime"in i){const i=(new Date).toISOString().slice(0,10);t[e.name]=`${i}T00:00:00`}else if("color_rgb"in i)t[e.name]=[0,0,0];else if("color_temp"in i)t[e.name]=i.color_temp?.min_mireds??153;else if("action"in i||"trigger"in i||"condition"in i)t[e.name]=[];else{if(!("media"in i)&&!("target"in i))throw new Error(`Selector ${Object.keys(i)[0]} not supported in initial form data`);t[e.name]={}}}}else;})),t}},42877:function(e,t,i){var n=i(44249),o=i(72621),a=i(57243),s=i(50778),r=i(38653),l=i(11297);i(17949),i(59414);const d={boolean:()=>i.e("2154").then(i.bind(i,13755)),constant:()=>i.e("4418").then(i.bind(i,92152)),float:()=>i.e("4608").then(i.bind(i,68091)),grid:()=>i.e("4351").then(i.bind(i,39090)),expandable:()=>i.e("9823").then(i.bind(i,78446)),integer:()=>i.e("9456").then(i.bind(i,93285)),multi_select:()=>Promise.all([i.e("7493"),i.e("5079"),i.e("1808")]).then(i.bind(i,87092)),positive_time_period_dict:()=>i.e("5058").then(i.bind(i,96636)),select:()=>i.e("1083").then(i.bind(i,6102)),string:()=>i.e("9752").then(i.bind(i,58701))},c=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,n.Z)([(0,s.Mo)("ha-form")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof a.fl&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{"selector"in e||d[e.type]?.()}))}},{kind:"method",key:"render",value:function(){return a.dy`
      <div class="root" part="root">
        ${this.error&&this.error.base?a.dy`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{const t=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),i=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return a.dy`
            ${t?a.dy`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(t,e)}
                  </ha-alert>
                `:i?a.dy`
                    <ha-alert own-margin alert-type="warning">
                      ${this._computeWarning(i,e)}
                    </ha-alert>
                  `:""}
            ${"selector"in e?a.dy`<ha-selector
                  .schema=${e}
                  .hass=${this.hass}
                  .name=${e.name}
                  .selector=${e.selector}
                  .value=${c(this.data,e)}
                  .label=${this._computeLabel(e,this.data)}
                  .disabled=${e.disabled||this.disabled||!1}
                  .placeholder=${e.required?"":e.default}
                  .helper=${this._computeHelper(e)}
                  .localizeValue=${this.localizeValue}
                  .required=${e.required||!1}
                  .context=${this._generateContext(e)}
                ></ha-selector>`:(0,r.h)(this.fieldElementName(e.type),{schema:e,data:c(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})}
          `}))}
      </div>
    `}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[i,n]of Object.entries(e.context))t[i]=this.data[n];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,o.Z)(i,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const i=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...i},(0,l.B)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?a.dy`<ul>
        ${e.map((e=>a.dy`<li>
              ${this.computeError?this.computeError(e,t):e}
            </li>`))}
      </ul>`:this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"field",static:!0,key:"styles",value(){return a.iv`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `}}]}}),a.oi)},61158:function(e,t,i){var n=i(44249),o=i(57243),a=i(50778),s=i(72621),r=i(11297),l=i(75351);let d;const c={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};(0,n.Z)([(0,a.Mo)("ha-markdown-element")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[(0,a.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"allow-svg",type:Boolean})],key:"allowSvg",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"breaks",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value(){return!1}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"update",value:function(e){(0,s.Z)(n,"update",this,3)([e]),void 0!==this.content&&this._render()}},{kind:"method",key:"_render",value:async function(){this.innerHTML=await(async(e,t,n)=>(d||(d=(0,l.Ud)(new Worker(new URL(i.p+i.u("5845"),i.b)))),d.renderMarkdown(e,t,n)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg}),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const t=e.currentNode;if(t instanceof HTMLAnchorElement&&t.host!==document.location.host)t.target="_blank",t.rel="noreferrer noopener";else if(t instanceof HTMLImageElement)this.lazyImages&&(t.loading="lazy"),t.addEventListener("load",this._resize);else if(t instanceof HTMLQuoteElement){const i=t.firstElementChild?.firstChild?.textContent&&c.reType.exec(t.firstElementChild.firstChild.textContent);if(i){const{type:n}=i.groups,o=document.createElement("ha-alert");o.alertType=c.typeToHaAlert[n.toLowerCase()],o.append(...Array.from(t.childNodes).map((e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===i.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t})).reduce(((e,t)=>e.concat(t)),[]).filter((e=>e.textContent&&e.textContent!==i.input))),e.parentNode().replaceChild(o,t)}}else t instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(t.localName)&&i(61145)(`./${t.localName}`)}}},{kind:"field",key:"_resize",value(){return()=>(0,r.B)(this,"content-resize")}}]}}),o.fl),(0,n.Z)([(0,a.Mo)("ha-markdown")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"allow-svg",type:Boolean})],key:"allowSvg",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"breaks",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value(){return!1}},{kind:"method",key:"render",value:function(){return this.content?o.dy`<ha-markdown-element
      .content=${this.content}
      .allowSvg=${this.allowSvg}
      .breaks=${this.breaks}
      .lazyImages=${this.lazyImages}
    ></ha-markdown-element>`:o.Ld}},{kind:"field",static:!0,key:"styles",value(){return o.iv`
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
  `}}]}}),o.oi)},80495:function(e,t,i){i.d(t,{Bg:()=>h,DT:()=>c,SY:()=>l,aJ:()=>s,cz:()=>r,ko:()=>d});var n=i(4468),o=i(36719);let a=function(e){return e[e.ANNOUNCE=1]="ANNOUNCE",e}({});const s=(e,t,i)=>e.connection.subscribeMessage(i,{type:"assist_satellite/intercept_wake_word",entity_id:t}),r=(e,t)=>e.callWS({type:"assist_satellite/test_connection",entity_id:t}),l=(e,t,i)=>e.callService("assist_satellite","announce",{message:i},{entity_id:t}),d=(e,t)=>e.callWS({type:"assist_satellite/get_configuration",entity_id:t}),c=(e,t,i)=>e.callWS({type:"assist_satellite/set_wake_words",entity_id:t,wake_word_ids:i}),h=e=>e&&e.state!==o.nZ&&(0,n.e)(e,a.ANNOUNCE)},41946:function(e,t,i){i.d(t,{iI:()=>o,oT:()=>n});const n=e=>e.map((e=>{if("string"!==e.type)return e;switch(e.name){case"username":return{...e,autocomplete:"username",autofocus:!0};case"password":return{...e,autocomplete:"current-password"};case"code":return{...e,autocomplete:"one-time-code",autofocus:!0};default:return e}})),o=(e,t)=>e.callWS({type:"auth/sign_path",path:t})},79983:function(e,t,i){i.d(t,{D4:()=>a,D7:()=>d,Ky:()=>o,XO:()=>s,d4:()=>l,oi:()=>r});const n={"HA-Frontend-Base":`${location.protocol}//${location.host}`},o=(e,t,i)=>e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(e.userData?.showAdvanced),entry_id:i},n),a=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,n),s=(e,t,i)=>e.callApi("POST",`config/config_entries/flow/${t}`,i,n),r=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),l=(e,t)=>e.callApi("GET","config/config_entries/flow_handlers"+(t?`?type=${t}`:"")),d=e=>e.sendMessagePromise({type:"config_entries/flow/progress"})},36719:function(e,t,i){i.d(t,{ON:()=>s,PX:()=>r,V_:()=>l,lz:()=>a,nZ:()=>o,rk:()=>c});var n=i(95907);const o="unavailable",a="unknown",s="on",r="off",l=[o,a],d=[o,a,r],c=(0,n.z)(l);(0,n.z)(d)},44699:function(e,t,i){i.d(t,{H:()=>o,O:()=>a});const n=["generic_camera","template"],o=(e,t,i,n,o,a)=>e.connection.subscribeMessage(a,{type:`${t}/start_preview`,flow_id:i,flow_type:n,user_input:o}),a=e=>n.includes(e)?e:"generic"},65440:function(e,t,i){var n=i(44249),o=i(72621),a=(i(31622),i(57243)),s=i(50778),r=i(11297);i(90977),i(44118),i(59897);var l=i(66193),d=i(26205),c=i(4557);const h=()=>i.e("3393").then(i.bind(i,27295));var p=i(18694);const u=a.iv`
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
`;(0,n.Z)([(0,s.Mo)("step-flow-abort")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"params",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"domain",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)(i,"firstUpdated",this,3)([e]),"missing_credentials"===this.step.reason&&this._handleMissingCreds()}},{kind:"method",key:"render",value:function(){return"missing_credentials"===this.step.reason?a.Ld:a.dy`
      <h2>
        ${this.params.flowConfig.renderAbortHeader?this.params.flowConfig.renderAbortHeader(this.hass,this.step):this.hass.localize(`component.${this.domain}.title`)}
      </h2>
      <div class="content">
        ${this.params.flowConfig.renderAbortDescription(this.hass,this.step)}
      </div>
      <div class="buttons">
        <mwc-button @click=${this._flowDone}
          >${this.hass.localize("ui.panel.config.integrations.config_flow.close")}</mwc-button
        >
      </div>
    `}},{kind:"method",key:"_handleMissingCreds",value:async function(){var e,t;e=this.params.dialogParentElement,t={selectedDomain:this.domain,manifest:this.params.manifest,applicationCredentialAddedCallback:()=>{(0,p.t)(this.params.dialogParentElement,{dialogClosedCallback:this.params.dialogClosedCallback,startFlowHandler:this.domain,showAdvanced:this.hass.userData?.showAdvanced})}},(0,r.B)(e,"show-dialog",{dialogTag:"dialog-add-application-credential",dialogImport:h,dialogParams:t}),this._flowDone()}},{kind:"method",key:"_flowDone",value:function(){(0,r.B)(this,"flow-update",{step:void 0})}},{kind:"get",static:!0,key:"styles",value:function(){return u}}]}}),a.oi);var f=i(27486),m=i(79575),g=(i(69181),i(80495)),v=i(99523);const y=()=>Promise.all([i.e("4224"),i.e("7493"),i.e("3213"),i.e("6160"),i.e("3732")]).then(i.bind(i,66738));(0,n.Z)([(0,s.Mo)("step-flow-create-entry")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"field",key:"_devices",value(){return(0,f.Z)(((e,t,i)=>e&&i?t.filter((e=>e.config_entries.includes(i))):[]))}},{kind:"field",key:"_deviceEntities",value(){return(0,f.Z)(((e,t,i)=>t.filter((t=>t.device_id===e&&(!i||(0,m.M)(t.entity_id)===i)))))}},{kind:"method",key:"willUpdate",value:function(e){if(!e.has("devices")&&!e.has("hass"))return;const t=this._devices(this.flowConfig.showDevices,Object.values(this.hass.devices),this.step.result?.entry_id);if(1!==t.length||t[0].primary_config_entry!==this.step.result?.entry_id)return;const i=this._deviceEntities(t[0].id,Object.values(this.hass.entities),"assist_satellite");var n,o;i.length&&i.some((e=>(0,g.Bg)(this.hass.states[e.entity_id])))&&(this._flowDone(),n=this,o={deviceId:t[0].id},(0,r.B)(n,"show-dialog",{dialogTag:"ha-voice-assistant-setup-dialog",dialogImport:y,dialogParams:o}))}},{kind:"method",key:"render",value:function(){const e=this.hass.localize,t=this._devices(this.flowConfig.showDevices,Object.values(this.hass.devices),this.step.result?.entry_id);return a.dy`
      <h2>${e("ui.panel.config.integrations.config_flow.success")}!</h2>
      <div class="content">
        ${this.flowConfig.renderCreateEntryDescription(this.hass,this.step)}
        ${"not_loaded"===this.step.result?.state?a.dy`<span class="error"
              >${e("ui.panel.config.integrations.config_flow.not_loaded")}</span
            >`:a.Ld}
        ${0===t.length?a.Ld:a.dy`
              <p>
                ${e("ui.panel.config.integrations.config_flow.found_following_devices")}:
              </p>
              <div class="devices">
                ${t.map((e=>a.dy`
                    <div class="device">
                      <div>
                        <b>${(0,v.jL)(e,this.hass)}</b><br />
                        ${e.model||e.manufacturer?a.dy`${e.model}
                            ${e.manufacturer?a.dy`(${e.manufacturer})`:""}`:a.dy`&nbsp;`}
                      </div>
                      <ha-area-picker
                        .hass=${this.hass}
                        .device=${e.id}
                        .value=${e.area_id??void 0}
                        @value-changed=${this._areaPicked}
                      ></ha-area-picker>
                    </div>
                  `))}
              </div>
            `}
      </div>
      <div class="buttons">
        <mwc-button @click=${this._flowDone}
          >${e("ui.panel.config.integrations.config_flow.finish")}</mwc-button
        >
      </div>
    `}},{kind:"method",key:"_flowDone",value:function(){(0,r.B)(this,"flow-update",{step:void 0})}},{kind:"method",key:"_areaPicked",value:async function(e){const t=e.currentTarget,i=t.device,n=e.detail.value;try{await(0,v.t1)(this.hass,i,{area_id:n})}catch(o){(0,c.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_flow.error_saving_area",{error:o.message})}),t.value=null}}},{kind:"get",static:!0,key:"styles",value:function(){return[u,a.iv`
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
      `]}}]}}),a.oi),(0,n.Z)([(0,s.Mo)("step-flow-external")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){const e=this.hass.localize;return a.dy`
      <h2>${this.flowConfig.renderExternalStepHeader(this.hass,this.step)}</h2>
      <div class="content">
        ${this.flowConfig.renderExternalStepDescription(this.hass,this.step)}
        <div class="open-button">
          <a href=${this.step.url} target="_blank" rel="noreferrer">
            <mwc-button raised>
              ${e("ui.panel.config.integrations.config_flow.external_step.open_site")}
            </mwc-button>
          </a>
        </div>
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)(i,"firstUpdated",this,3)([e]),window.open(this.step.url)}},{kind:"get",static:!0,key:"styles",value:function(){return[u,a.iv`
        .open-button {
          text-align: center;
          padding: 24px 0;
        }
        .open-button a {
          text-decoration: none;
        }
      `]}}]}}),a.oi);i(14394);var w=i(38653);i(17949);var _=i(12328),k=(i(42877),i(61158),i(41946)),b=i(44699);(0,n.Z)([(0,s.Mo)("step-flow-form")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_loading",value(){return!1}},{kind:"field",decorators:[(0,s.SB)()],key:"_stepData",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_errorMsg",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)(n,"disconnectedCallback",this,3)([]),this.removeEventListener("keydown",this._handleKeyDown)}},{kind:"method",key:"render",value:function(){const e=this.step,t=this._stepDataProcessed;return a.dy`
      <h2>${this.flowConfig.renderShowFormStepHeader(this.hass,this.step)}</h2>
      <div class="content" @click=${this._clickHandler}>
        ${this.flowConfig.renderShowFormStepDescription(this.hass,this.step)}
        ${this._errorMsg?a.dy`<ha-alert alert-type="error">${this._errorMsg}</ha-alert>`:""}
        <ha-form
          .hass=${this.hass}
          .data=${t}
          .disabled=${this._loading}
          @value-changed=${this._stepDataChanged}
          .schema=${(0,k.oT)(e.data_schema)}
          .error=${e.errors}
          .computeLabel=${this._labelCallback}
          .computeHelper=${this._helperCallback}
          .computeError=${this._errorCallback}
          .localizeValue=${this._localizeValueCallback}
        ></ha-form>
      </div>
      ${e.preview?a.dy`<div class="preview" @set-flow-errors=${this._setError}>
            <h3>
              ${this.hass.localize("ui.panel.config.integrations.config_flow.preview")}:
            </h3>
            ${(0,w.h)(`flow-preview-${(0,b.O)(e.preview)}`,{hass:this.hass,domain:e.preview,flowType:this.flowConfig.flowType,handler:e.handler,stepId:e.step_id,flowId:e.flow_id,stepData:t})}
          </div>`:a.Ld}
      <div class="buttons">
        ${this._loading?a.dy`
              <div class="submit-spinner">
                <ha-circular-progress indeterminate></ha-circular-progress>
              </div>
            `:a.dy`
              <div>
                <mwc-button @click=${this._submitStep}>
                  ${this.flowConfig.renderShowFormStepSubmitButton(this.hass,this.step)}
                </mwc-button>
              </div>
            `}
      </div>
    `}},{kind:"method",key:"_setError",value:function(e){this.step={...this.step,errors:e.detail}}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)(n,"firstUpdated",this,3)([e]),setTimeout((()=>this.shadowRoot.querySelector("ha-form").focus()),0),this.addEventListener("keydown",this._handleKeyDown)}},{kind:"method",key:"willUpdate",value:function(e){(0,o.Z)(n,"willUpdate",this,3)([e]),e.has("step")&&this.step?.preview&&i(2292)(`./flow-preview-${(0,b.O)(this.step.preview)}`)}},{kind:"method",key:"_clickHandler",value:function(e){((e,t=!0)=>{if(e.defaultPrevented||0!==e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;const i=e.composedPath().find((e=>"A"===e.tagName));if(!i||i.target||i.hasAttribute("download")||"external"===i.getAttribute("rel"))return;let n=i.href;if(!n||-1!==n.indexOf("mailto:"))return;const o=window.location,a=o.origin||o.protocol+"//"+o.host;return 0===n.indexOf(a)&&(n=n.substr(a.length),"#"!==n)?(t&&e.preventDefault(),n):void 0})(e,!1)&&(0,r.B)(this,"flow-update",{step:void 0})}},{kind:"field",key:"_handleKeyDown",value(){return e=>{"Enter"===e.key&&this._submitStep()}}},{kind:"get",key:"_stepDataProcessed",value:function(){return void 0!==this._stepData||(this._stepData=(0,_.x)(this.step.data_schema)),this._stepData}},{kind:"method",key:"_submitStep",value:async function(){const e=this._stepData||{};if(!(void 0===e?void 0===this.step.data_schema.find((e=>e.required)):e&&this.step.data_schema.every((t=>!t.required||!["",void 0].includes(e[t.name])))))return void(this._errorMsg=this.hass.localize("ui.panel.config.integrations.config_flow.not_all_required_fields"));this._loading=!0,this._errorMsg=void 0;const t=this.step.flow_id,i={};Object.keys(e).forEach((t=>{const n=e[t];[void 0,""].includes(n)||(i[t]=n)}));try{const e=await this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,i);if(!this.step||t!==this.step.flow_id)return;(0,r.B)(this,"flow-update",{step:e})}catch(n){n&&n.body?(n.body.message&&(this._errorMsg=n.body.message),n.body.errors&&(this.step={...this.step,errors:n.body.errors}),n.body.message||n.body.errors||(this._errorMsg="Unknown error occurred")):this._errorMsg="Unknown error occurred"}finally{this._loading=!1}}},{kind:"method",key:"_stepDataChanged",value:function(e){this._stepData=e.detail.value}},{kind:"field",key:"_labelCallback",value(){return(e,t,i)=>this.flowConfig.renderShowFormStepFieldLabel(this.hass,this.step,e,i)}},{kind:"field",key:"_helperCallback",value(){return(e,t)=>this.flowConfig.renderShowFormStepFieldHelper(this.hass,this.step,e,t)}},{kind:"field",key:"_errorCallback",value(){return e=>this.flowConfig.renderShowFormStepFieldError(this.hass,this.step,e)}},{kind:"field",key:"_localizeValueCallback",value(){return e=>this.flowConfig.renderShowFormStepFieldLocalizeValue(this.hass,this.step,e)}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,u,a.iv`
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
      `]}}]}}),a.oi),(0,n.Z)([(0,s.Mo)("step-flow-loading")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"loadingReason",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"handler",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){const e=this.flowConfig.renderLoadingDescription(this.hass,this.loadingReason,this.handler,this.step);return a.dy`
      <div class="init-spinner">
        ${e?a.dy`<div>${e}</div>`:""}
        <ha-circular-progress indeterminate></ha-circular-progress>
      </div>
    `}},{kind:"field",static:!0,key:"styles",value(){return a.iv`
    .init-spinner {
      padding: 50px 100px;
      text-align: center;
    }
    ha-circular-progress {
      margin-top: 16px;
    }
  `}}]}}),a.oi);i(87319),i(54220);(0,n.Z)([(0,s.Mo)("step-flow-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){let e,t;if(Array.isArray(this.step.menu_options)){e=this.step.menu_options,t={};for(const i of e)t[i]=this.flowConfig.renderMenuOption(this.hass,this.step,i)}else e=Object.keys(this.step.menu_options),t=this.step.menu_options;const i=this.flowConfig.renderMenuDescription(this.hass,this.step);return a.dy`
      <h2>${this.flowConfig.renderMenuHeader(this.hass,this.step)}</h2>
      ${i?a.dy`<div class="content">${i}</div>`:""}
      <div class="options">
        ${e.map((e=>a.dy`
            <mwc-list-item hasMeta .step=${e} @click=${this._handleStep}>
              <span>${t[e]}</span>
              <ha-icon-next slot="meta"></ha-icon-next>
            </mwc-list-item>
          `))}
      </div>
    `}},{kind:"method",key:"_handleStep",value:function(e){(0,r.B)(this,"flow-update",{stepPromise:this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,{next_step_id:e.currentTarget.step})})}},{kind:"field",static:!0,key:"styles",value(){return[u,a.iv`
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
    `]}}]}}),a.oi),(0,n.Z)([(0,s.Mo)("step-flow-progress")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){return a.dy`
      <h2>
        ${this.flowConfig.renderShowFormProgressHeader(this.hass,this.step)}
      </h2>
      <div class="content">
        <ha-circular-progress indeterminate></ha-circular-progress>
        ${this.flowConfig.renderShowFormProgressDescription(this.hass,this.step)}
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[u,a.iv`
        .content {
          padding: 50px 100px;
          text-align: center;
        }
        ha-circular-progress {
          margin-bottom: 16px;
        }
      `]}}]}}),a.oi);let $=0;(0,n.Z)([(0,s.Mo)("dialog-data-entry-flow")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_loading",value:void 0},{kind:"field",key:"_instance",value(){return $}},{kind:"field",decorators:[(0,s.SB)()],key:"_step",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_handler",value:void 0},{kind:"field",key:"_unsubDataEntryFlowProgressed",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._instance=$++;const t=this._instance;let i;if(e.startFlowHandler){this._loading="loading_flow",this._handler=e.startFlowHandler;try{i=await this._params.flowConfig.createFlow(this.hass,e.startFlowHandler)}catch(n){this.closeDialog();let e=n.message||n.body||"Unknown error";return"string"!=typeof e&&(e=JSON.stringify(e)),void(0,c.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${e}`})}if(t!==this._instance)return}else{if(!e.continueFlowId)return;this._loading="loading_flow";try{i=await e.flowConfig.fetchFlow(this.hass,e.continueFlowId)}catch(n){this.closeDialog();let e=n.message||n.body||"Unknown error";return"string"!=typeof e&&(e=JSON.stringify(e)),void(0,c.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${e}`})}}t===this._instance&&(this._processStep(i),this._loading=void 0)}},{kind:"method",key:"closeDialog",value:function(){if(!this._params)return;const e=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));!this._step||e||this._params.continueFlowId||this._params.flowConfig.deleteFlow(this.hass,this._step.flow_id),this._step&&this._params.dialogClosedCallback&&this._params.dialogClosedCallback({flowFinished:e,entryId:"result"in this._step?this._step.result?.entry_id:void 0}),this._loading=void 0,this._step=void 0,this._params=void 0,this._handler=void 0,this._unsubDataEntryFlowProgressed&&(this._unsubDataEntryFlowProgressed.then((e=>{e()})),this._unsubDataEntryFlowProgressed=void 0),(0,r.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?a.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        hideActions
      >
        <div>
          ${this._loading||null===this._step?a.dy`
                <step-flow-loading
                  .flowConfig=${this._params.flowConfig}
                  .hass=${this.hass}
                  .loadingReason=${this._loading}
                  .handler=${this._handler}
                  .step=${this._step}
                ></step-flow-loading>
              `:void 0===this._step?"":a.dy`
                  <div class="dialog-actions">
                    ${["form","menu","external","progress","data_entry_flow_progressed"].includes(this._step?.type)&&this._params.manifest?.is_built_in||this._params.manifest?.documentation?a.dy`
                          <a
                            href=${this._params.manifest.is_built_in?(0,d.R)(this.hass,`/integrations/${this._params.manifest.domain}`):this._params?.manifest?.documentation}
                            target="_blank"
                            rel="noreferrer noopener"
                          >
                            <ha-icon-button
                              .label=${this.hass.localize("ui.common.help")}
                              .path=${"M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z"}
                            >
                            </ha-icon-button
                          ></a>
                        `:""}
                    <ha-icon-button
                      .label=${this.hass.localize("ui.panel.config.integrations.config_flow.dismiss")}
                      .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                      dialogAction="close"
                    ></ha-icon-button>
                  </div>
                  ${"form"===this._step.type?a.dy`
                        <step-flow-form
                          .flowConfig=${this._params.flowConfig}
                          .step=${this._step}
                          .hass=${this.hass}
                        ></step-flow-form>
                      `:"external"===this._step.type?a.dy`
                          <step-flow-external
                            .flowConfig=${this._params.flowConfig}
                            .step=${this._step}
                            .hass=${this.hass}
                          ></step-flow-external>
                        `:"abort"===this._step.type?a.dy`
                            <step-flow-abort
                              .params=${this._params}
                              .step=${this._step}
                              .hass=${this.hass}
                              .domain=${this._step.handler}
                            ></step-flow-abort>
                          `:"progress"===this._step.type?a.dy`
                              <step-flow-progress
                                .flowConfig=${this._params.flowConfig}
                                .step=${this._step}
                                .hass=${this.hass}
                              ></step-flow-progress>
                            `:"menu"===this._step.type?a.dy`
                                <step-flow-menu
                                  .flowConfig=${this._params.flowConfig}
                                  .step=${this._step}
                                  .hass=${this.hass}
                                ></step-flow-menu>
                              `:a.dy`
                                <step-flow-create-entry
                                  .flowConfig=${this._params.flowConfig}
                                  .step=${this._step}
                                  .hass=${this.hass}
                                ></step-flow-create-entry>
                              `}
                `}
        </div>
      </ha-dialog>
    `:a.Ld}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)(i,"firstUpdated",this,3)([e]),this.addEventListener("flow-update",(e=>{const{step:t,stepPromise:i}=e.detail;this._processStep(t||i)}))}},{kind:"method",key:"willUpdate",value:function(e){(0,o.Z)(i,"willUpdate",this,3)([e]),e.has("_step")&&this._step&&["external","progress"].includes(this._step.type)&&this._subscribeDataEntryFlowProgressed()}},{kind:"method",key:"_processStep",value:async function(e){if(void 0===e)return void this.closeDialog();let t;this._loading="loading_step";try{t=await e}catch(i){return this.closeDialog(),void(0,c.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:i?.body?.message})}finally{this._loading=void 0}this._step=void 0,await this.updateComplete,this._step=t}},{kind:"method",key:"_subscribeDataEntryFlowProgressed",value:async function(){var e,t;this._unsubDataEntryFlowProgressed||(this._unsubDataEntryFlowProgressed=(e=this.hass.connection,t=async e=>{e.data.flow_id===this._step?.flow_id&&this._processStep(this._params.flowConfig.fetchFlow(this.hass,this._step.flow_id))},e.subscribeEvents(t,"data_entry_flow_progressed")))}},{kind:"get",static:!0,key:"styles",value:function(){return[l.yu,a.iv`
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
      `]}}]}}),a.oi)},18694:function(e,t,i){i.d(t,{t:()=>r});var n=i(57243),o=i(79983),a=i(1275),s=i(43373);const r=(e,t)=>(0,s.w)(e,t,{flowType:"config_flow",showDevices:!0,createFlow:async(e,i)=>{const[n]=await Promise.all([(0,o.Ky)(e,i,t.entryId),e.loadFragmentTranslation("config"),e.loadBackendTranslation("config",i),e.loadBackendTranslation("selector",i),e.loadBackendTranslation("title",i)]);return n},fetchFlow:async(e,t)=>{const i=await(0,o.D4)(e,t);return await e.loadFragmentTranslation("config"),await e.loadBackendTranslation("config",i.handler),await e.loadBackendTranslation("selector",i.handler),i},handleFlowStep:o.XO,deleteFlow:o.oi,renderAbortDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?n.dy`
            <ha-markdown allow-svg breaks .content=${i}></ha-markdown>
          `:t.reason},renderShowFormStepHeader(e,t){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.title`,t.description_placeholders)||e.localize(`component.${t.handler}.title`)},renderShowFormStepDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?n.dy`
            <ha-markdown allow-svg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepFieldLabel(e,t,i,n){if("expandable"===i.type)return e.localize(`component.${t.handler}.config.step.${t.step_id}.sections.${i.name}.name`);const o=n?.path?.[0]?`sections.${n.path[0]}.`:"";return e.localize(`component.${t.handler}.config.step.${t.step_id}.${o}data.${i.name}`)||i.name},renderShowFormStepFieldHelper(e,t,i,o){if("expandable"===i.type)return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.sections.${i.name}.description`);const a=o?.path?.[0]?`sections.${o.path[0]}.`:"",s=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.${a}data_description.${i.name}`,t.description_placeholders);return s?n.dy`<ha-markdown breaks .content=${s}></ha-markdown>`:""},renderShowFormStepFieldError(e,t,i){return e.localize(`component.${t.translation_domain||t.translation_domain||t.handler}.config.error.${i}`,t.description_placeholders)||i},renderShowFormStepFieldLocalizeValue(e,t,i){return e.localize(`component.${t.handler}.selector.${i}`)},renderShowFormStepSubmitButton(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===t.last_step?"next":"submit"))},renderExternalStepHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site")},renderExternalStepDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.${t.step_id}.description`,t.description_placeholders);return n.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?n.dy`
              <ha-markdown
                allow-svg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return n.dy`
        ${i?n.dy`
              <ha-markdown
                allow-svg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config",{name:t.title})}
        </p>
      `},renderShowFormProgressHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`)},renderShowFormProgressDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return i?n.dy`
            <ha-markdown allow-svg breaks .content=${i}></ha-markdown>
          `:""},renderMenuHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`)},renderMenuDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?n.dy`
            <ha-markdown allow-svg breaks .content=${i}></ha-markdown>
          `:""},renderMenuOption(e,t,i){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.menu_options.${i}`,t.description_placeholders)},renderLoadingDescription(e,t,i,n){if("loading_flow"!==t&&"loading_step"!==t)return"";const o=n?.handler||i;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:o?(0,a.Lh)(e.localize,o):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},26205:function(e,t,i){i.d(t,{R:()=>n});const n=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}};
//# sourceMappingURL=7299.baccb2c24a5b2ba3.js.map