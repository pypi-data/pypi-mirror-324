"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6997"],{61239:function(e,t,a){a.d(t,{v:()=>i});a(19083);var r=a(36719),n=a(79575);function i(e,t){const a=(0,n.M)(e.entity_id),i=void 0!==t?t:null==e?void 0:e.state;if(["button","event","input_button","scene"].includes(a))return i!==r.nZ;if((0,r.rk)(i))return!1;if(i===r.PX&&"alert"!==a)return!1;switch(a){case"alarm_control_panel":return"disarmed"!==i;case"alert":return"idle"!==i;case"cover":case"valve":return"closed"!==i;case"device_tracker":case"person":return"not_home"!==i;case"lawn_mower":return["mowing","error"].includes(i);case"lock":return"locked"!==i;case"media_player":return"standby"!==i;case"vacuum":return!["idle","docked","paused"].includes(i);case"plant":return"problem"===i;case"group":return["on","home","open","locked","problem"].includes(i);case"timer":return"active"===i;case"camera":return"streaming"===i}return!0}},42877:function(e,t,a){var r=a(73577),n=a(72621),i=(a(71695),a(19423),a(40251),a(39527),a(41360),a(13334),a(47021),a(57243)),o=a(50778),s=a(38653),l=a(11297);a(17949),a(59414);let d,u,c,h,m,p,b,f,k,v=e=>e;const y={boolean:()=>a.e("2154").then(a.bind(a,13755)),constant:()=>a.e("4418").then(a.bind(a,92152)),float:()=>a.e("4608").then(a.bind(a,68091)),grid:()=>a.e("4351").then(a.bind(a,39090)),expandable:()=>a.e("9823").then(a.bind(a,78446)),integer:()=>a.e("9456").then(a.bind(a,93285)),multi_select:()=>Promise.all([a.e("7493"),a.e("5079"),a.e("1808")]).then(a.bind(a,87092)),positive_time_period_dict:()=>Promise.all([a.e("2047"),a.e("5235")]).then(a.bind(a,96636)),select:()=>a.e("1083").then(a.bind(a,6102)),string:()=>a.e("9752").then(a.bind(a,58701))},g=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,r.Z)([(0,o.Mo)("ha-form")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof i.fl&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{var t;"selector"in e||null===(t=y[e.type])||void 0===t||t.call(y)}))}},{kind:"method",key:"render",value:function(){return(0,i.dy)(d||(d=v`
      <div class="root" part="root">
        ${0}
        ${0}
      </div>
    `),this.error&&this.error.base?(0,i.dy)(u||(u=v`
              <ha-alert alert-type="error">
                ${0}
              </ha-alert>
            `),this._computeError(this.error.base,this.schema)):"",this.schema.map((e=>{var t;const a=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),r=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return(0,i.dy)(c||(c=v`
            ${0}
            ${0}
          `),a?(0,i.dy)(h||(h=v`
                  <ha-alert own-margin alert-type="error">
                    ${0}
                  </ha-alert>
                `),this._computeError(a,e)):r?(0,i.dy)(m||(m=v`
                    <ha-alert own-margin alert-type="warning">
                      ${0}
                    </ha-alert>
                  `),this._computeWarning(r,e)):"","selector"in e?(0,i.dy)(p||(p=v`<ha-selector
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
                ></ha-selector>`),e,this.hass,e.name,e.selector,g(this.data,e),this._computeLabel(e,this.data),e.disabled||this.disabled||!1,e.required?"":e.default,this._computeHelper(e),this.localizeValue,e.required||!1,this._generateContext(e)):(0,s.h)(this.fieldElementName(e.type),Object.assign({schema:e,data:g(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:null===(t=this.hass)||void 0===t?void 0:t.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e)},this.getFormProperties())))})))}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[a,r]of Object.entries(e.context))t[a]=this.data[r];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,n.Z)(a,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data=Object.assign(Object.assign({},this.data),a),(0,l.B)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?(0,i.dy)(b||(b=v`<ul>
        ${0}
      </ul>`),e.map((e=>(0,i.dy)(f||(f=v`<li>
              ${0}
            </li>`),this.computeError?this.computeError(e,t):e)))):this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"field",static:!0,key:"styles",value(){return(0,i.iv)(k||(k=v`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `))}}]}}),i.oi)},41946:function(e,t,a){a.d(t,{iI:()=>n,oT:()=>r});a(19083),a(77439),a(19423),a(40251),a(97499),a(61006),a(13334);const r=e=>e.map((e=>{if("string"!==e.type)return e;switch(e.name){case"username":return Object.assign(Object.assign({},e),{},{autocomplete:"username",autofocus:!0});case"password":return Object.assign(Object.assign({},e),{},{autocomplete:"current-password"});case"code":return Object.assign(Object.assign({},e),{},{autocomplete:"one-time-code",autofocus:!0});default:return e}})),n=(e,t)=>e.callWS({type:"auth/sign_path",path:t})},36719:function(e,t,a){a.d(t,{ON:()=>o,PX:()=>s,V_:()=>l,lz:()=>i,nZ:()=>n,rk:()=>u});var r=a(95907);const n="unavailable",i="unknown",o="on",s="off",l=[n,i],d=[n,i,s],u=(0,r.z)(l);(0,r.z)(d)}}]);
//# sourceMappingURL=6997.edadc93583106eca.js.map