export const ids=["538"];export const modules={42877:function(e,t,a){var o=a(44249),n=a(72621),i=a(57243),r=a(50778),l=a(38653),s=a(11297);a(17949),a(59414);const d={boolean:()=>a.e("2154").then(a.bind(a,13755)),constant:()=>a.e("4418").then(a.bind(a,92152)),float:()=>a.e("4608").then(a.bind(a,68091)),grid:()=>a.e("4351").then(a.bind(a,39090)),expandable:()=>a.e("9823").then(a.bind(a,78446)),integer:()=>a.e("9456").then(a.bind(a,93285)),multi_select:()=>Promise.all([a.e("7493"),a.e("5079"),a.e("1808")]).then(a.bind(a,87092)),positive_time_period_dict:()=>a.e("5058").then(a.bind(a,96636)),select:()=>a.e("1083").then(a.bind(a,6102)),string:()=>a.e("9752").then(a.bind(a,58701))},c=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,o.Z)([(0,r.Mo)("ha-form")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof i.fl&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{"selector"in e||d[e.type]?.()}))}},{kind:"method",key:"render",value:function(){return i.dy`
      <div class="root" part="root">
        ${this.error&&this.error.base?i.dy`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{const t=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),a=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return i.dy`
            ${t?i.dy`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(t,e)}
                  </ha-alert>
                `:a?i.dy`
                    <ha-alert own-margin alert-type="warning">
                      ${this._computeWarning(a,e)}
                    </ha-alert>
                  `:""}
            ${"selector"in e?i.dy`<ha-selector
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
                ></ha-selector>`:(0,l.h)(this.fieldElementName(e.type),{schema:e,data:c(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})}
          `}))}
      </div>
    `}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[a,o]of Object.entries(e.context))t[a]=this.data[o];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,n.Z)(a,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...a},(0,s.B)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?i.dy`<ul>
        ${e.map((e=>i.dy`<li>
              ${this.computeError?this.computeError(e,t):e}
            </li>`))}
      </ul>`:this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"field",static:!0,key:"styles",value(){return i.iv`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `}}]}}),i.oi)},41533:function(e,t,a){a.r(t),a.d(t,{HaSelectorSelector:()=>c});var o=a(44249),n=a(57243),i=a(50778),r=a(27486),l=a(11297);a(17949),a(42877);const s={number:{min:1,max:100}},d={action:[],area:[{name:"multiple",selector:{boolean:{}}}],attribute:[{name:"entity_id",selector:{entity:{}}}],boolean:[],color_temp:[{name:"unit",selector:{select:{options:["kelvin","mired"]}}},{name:"min",selector:{number:{mode:"box"}}},{name:"max",selector:{number:{mode:"box"}}}],condition:[],date:[],datetime:[],device:[{name:"multiple",selector:{boolean:{}}}],duration:[{name:"enable_day",selector:{boolean:{}}},{name:"enable_millisecond",selector:{boolean:{}}}],entity:[{name:"multiple",selector:{boolean:{}}}],floor:[{name:"multiple",selector:{boolean:{}}}],icon:[],location:[],media:[],number:[{name:"min",selector:{number:{mode:"box",step:"any"}}},{name:"max",selector:{number:{mode:"box",step:"any"}}},{name:"step",selector:{number:{mode:"box",step:"any"}}}],object:[],color_rgb:[],select:[{name:"options",selector:{object:{}}},{name:"multiple",selector:{boolean:{}}}],state:[{name:"entity_id",selector:{entity:{}}}],target:[],template:[],text:[{name:"multiple",selector:{boolean:{}}},{name:"multiline",selector:{boolean:{}}},{name:"prefix",selector:{text:{}}},{name:"suffix",selector:{text:{}}}],theme:[],time:[]};let c=(0,o.Z)([(0,i.Mo)("ha-selector-selector")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"required",value(){return!0}},{kind:"field",key:"_yamlMode",value(){return!1}},{kind:"method",key:"shouldUpdate",value:function(e){return 1!==e.size||!e.has("hass")}},{kind:"field",key:"_schema",value(){return(0,r.Z)(((e,t)=>[{name:"type",selector:{select:{mode:"dropdown",required:!0,options:Object.keys(d).concat("manual").map((e=>({label:t(`ui.components.selectors.selector.types.${e}`)||e,value:e})))}}},..."manual"===e?[{name:"manual",selector:{object:{}}}]:[],...d[e]?d[e].length>1?[{name:"",type:"expandable",title:t("ui.components.selectors.selector.options"),schema:d[e]}]:d[e]:[]]))}},{kind:"method",key:"render",value:function(){let e,t;if(this._yamlMode)t="manual",e={type:t,manual:this.value};else{t=Object.keys(this.value)[0];const a=Object.values(this.value)[0];e={type:t,..."object"==typeof a?a:[]}}const a=this._schema(t,this.hass.localize);return n.dy`<ha-card>
      <div class="card-content">
        <p>${this.label?this.label:""}</p>
        <ha-form
          .hass=${this.hass}
          .data=${e}
          .schema=${a}
          .computeLabel=${this._computeLabelCallback}
          @value-changed=${this._valueChanged}
        ></ha-form></div
    ></ha-card>`}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value,a=t.type;if(!a||"object"!=typeof t||0===Object.keys(t).length)return;const o=Object.keys(this.value)[0];if("manual"===a&&!this._yamlMode)return this._yamlMode=!0,void this.requestUpdate();if("manual"===a&&void 0===t.manual)return;let n;"manual"!==a&&(this._yamlMode=!1),delete t.type,n="manual"===a?t.manual:a===o?{[a]:{...t.manual?t.manual[o]:t}}:{[a]:{...s[a]}},(0,l.B)(this,"value-changed",{value:n})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.components.selectors.selector.${e.name}`)||e.name}},{kind:"field",static:!0,key:"styles",value(){return n.iv`
    :host {
      --expansion-panel-summary-padding: 0 16px;
    }
    ha-alert {
      display: block;
      margin-bottom: 16px;
    }
    ha-card {
      margin: 0 0 16px 0;
    }
    ha-card.disabled {
      pointer-events: none;
      color: var(--disabled-text-color);
    }
    .card-content {
      padding: 0px 16px 16px 16px;
    }
    .title {
      font-size: 16px;
      padding-top: 16px;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 16px;
      padding-left: 16px;
      padding-right: 4px;
      padding-inline-start: 16px;
      padding-inline-end: 4px;
      white-space: nowrap;
    }
  `}}]}}),n.oi)}};
//# sourceMappingURL=538.3389257a59949e75.js.map