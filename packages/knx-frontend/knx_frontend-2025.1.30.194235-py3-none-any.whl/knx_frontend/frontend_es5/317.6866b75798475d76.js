"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["317"],{42877:function(e,t,a){var i=a(73577),o=a(72621),r=(a(71695),a(19423),a(40251),a(39527),a(41360),a(13334),a(47021),a(57243)),n=a(50778),s=a(38653),l=a(11297);a(17949),a(59414);let d,c,h,u,m,k,p,v,b,f=e=>e;const y={boolean:()=>a.e("2154").then(a.bind(a,13755)),constant:()=>a.e("4418").then(a.bind(a,92152)),float:()=>a.e("4608").then(a.bind(a,68091)),grid:()=>a.e("4351").then(a.bind(a,39090)),expandable:()=>a.e("9823").then(a.bind(a,78446)),integer:()=>a.e("9456").then(a.bind(a,93285)),multi_select:()=>Promise.all([a.e("7493"),a.e("5079"),a.e("1808")]).then(a.bind(a,87092)),positive_time_period_dict:()=>Promise.all([a.e("2047"),a.e("5235")]).then(a.bind(a,96636)),select:()=>a.e("1083").then(a.bind(a,6102)),string:()=>a.e("9752").then(a.bind(a,58701))},g=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,i.Z)([(0,n.Mo)("ha-form")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof r.fl&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{var t;"selector"in e||null===(t=y[e.type])||void 0===t||t.call(y)}))}},{kind:"method",key:"render",value:function(){return(0,r.dy)(d||(d=f`
      <div class="root" part="root">
        ${0}
        ${0}
      </div>
    `),this.error&&this.error.base?(0,r.dy)(c||(c=f`
              <ha-alert alert-type="error">
                ${0}
              </ha-alert>
            `),this._computeError(this.error.base,this.schema)):"",this.schema.map((e=>{var t;const a=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),i=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return(0,r.dy)(h||(h=f`
            ${0}
            ${0}
          `),a?(0,r.dy)(u||(u=f`
                  <ha-alert own-margin alert-type="error">
                    ${0}
                  </ha-alert>
                `),this._computeError(a,e)):i?(0,r.dy)(m||(m=f`
                    <ha-alert own-margin alert-type="warning">
                      ${0}
                    </ha-alert>
                  `),this._computeWarning(i,e)):"","selector"in e?(0,r.dy)(k||(k=f`<ha-selector
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
                ></ha-selector>`),e,this.hass,e.name,e.selector,g(this.data,e),this._computeLabel(e,this.data),e.disabled||this.disabled||!1,e.required?"":e.default,this._computeHelper(e),this.localizeValue,e.required||!1,this._generateContext(e)):(0,s.h)(this.fieldElementName(e.type),Object.assign({schema:e,data:g(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:null===(t=this.hass)||void 0===t?void 0:t.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e)},this.getFormProperties())))})))}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[a,i]of Object.entries(e.context))t[a]=this.data[i];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,o.Z)(a,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data=Object.assign(Object.assign({},this.data),a),(0,l.B)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?(0,r.dy)(p||(p=f`<ul>
        ${0}
      </ul>`),e.map((e=>(0,r.dy)(v||(v=f`<li>
              ${0}
            </li>`),this.computeError?this.computeError(e,t):e)))):this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"field",static:!0,key:"styles",value(){return(0,r.iv)(b||(b=f`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `))}}]}}),r.oi)},58202:function(e,t,a){a.r(t);var i=a(73577),o=(a(71695),a(47021),a(57243)),r=a(27486),n=a(50778),s=a(11297),l=a(44118),d=(a(42877),a(20095),a(66193));let c,h=e=>e,u=(0,i.Z)(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_params",value:void 0},{kind:"field",key:"_expand",value(){return!1}},{kind:"field",key:"_schema",value(){return(0,r.Z)((e=>[{name:"from",required:!0,selector:{time:{no_second:!0}}},{name:"to",required:!0,selector:{time:{no_second:!0}}},{name:"advanced_settings",type:"expandable",flatten:!0,expanded:e,schema:[{name:"data",required:!1,selector:{object:{}}}]}]))}},{kind:"method",key:"showDialog",value:function(e){var t;this._params=e,this._error=void 0,this._data=e.block,this._expand=!(null===(t=e.block)||void 0===t||!t.data)}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._data=void 0,(0,s.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params&&this._data?(0,o.dy)(c||(c=h`
      <ha-dialog
        open
        @closed=${0}
        .heading=${0}
      >
        <div>
          <ha-form
            .hass=${0}
            .schema=${0}
            .data=${0}
            .error=${0}
            .computeLabel=${0}
            @value-changed=${0}
          ></ha-form>
        </div>
        <ha-button
          slot="secondaryAction"
          class="warning"
          @click=${0}
        >
          ${0}
        </ha-button>
        <ha-button slot="primaryAction" @click=${0}>
          ${0}
        </ha-button>
      </ha-dialog>
    `),this.closeDialog,(0,l.i)(this.hass,this.hass.localize("ui.dialogs.helper_settings.schedule.edit_schedule_block")),this.hass,this._schema(this._expand),this._data,this._error,this._computeLabelCallback,this._valueChanged,this._deleteBlock,this.hass.localize("ui.common.delete"),this._updateBlock,this.hass.localize("ui.common.save")):o.Ld}},{kind:"method",key:"_valueChanged",value:function(e){this._error=void 0,this._data=e.detail.value}},{kind:"method",key:"_updateBlock",value:function(){try{this._params.updateBlock(this._data),this.closeDialog()}catch(e){this._error={base:e?e.message:"Unknown error"}}}},{kind:"method",key:"_deleteBlock",value:function(){try{this._params.deleteBlock(),this.closeDialog()}catch(e){this._error={base:e?e.message:"Unknown error"}}}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"from":return this.hass.localize("ui.dialogs.helper_settings.schedule.start");case"to":return this.hass.localize("ui.dialogs.helper_settings.schedule.end");case"data":return this.hass.localize("ui.dialogs.helper_settings.schedule.data");case"advanced_settings":return this.hass.localize("ui.dialogs.helper_settings.schedule.advanced_settings")}return""}}},{kind:"get",static:!0,key:"styles",value:function(){return[d.yu]}}]}}),o.oi);customElements.define("dialog-schedule-block-info",u)}}]);
//# sourceMappingURL=317.6866b75798475d76.js.map