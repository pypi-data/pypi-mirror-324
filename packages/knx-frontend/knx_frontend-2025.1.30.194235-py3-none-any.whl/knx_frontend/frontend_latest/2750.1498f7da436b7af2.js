export const ids=["2750"];export const modules={61239:function(e,t,r){r.d(t,{v:()=>i});var a=r(36719),n=r(79575);function i(e,t){const r=(0,n.M)(e.entity_id),i=void 0!==t?t:e?.state;if(["button","event","input_button","scene"].includes(r))return i!==a.nZ;if((0,a.rk)(i))return!1;if(i===a.PX&&"alert"!==r)return!1;switch(r){case"alarm_control_panel":return"disarmed"!==i;case"alert":return"idle"!==i;case"cover":case"valve":return"closed"!==i;case"device_tracker":case"person":return"not_home"!==i;case"lawn_mower":return["mowing","error"].includes(i);case"lock":return"locked"!==i;case"media_player":return"standby"!==i;case"vacuum":return!["idle","docked","paused"].includes(i);case"plant":return"problem"===i;case"group":return["on","home","open","locked","problem"].includes(i);case"timer":return"active"===i;case"camera":return"streaming"===i}return!0}},42877:function(e,t,r){var a=r(44249),n=r(72621),i=r(57243),o=r(50778),l=r(38653),s=r(11297);r(17949),r(59414);const d={boolean:()=>r.e("2154").then(r.bind(r,13755)),constant:()=>r.e("4418").then(r.bind(r,92152)),float:()=>r.e("4608").then(r.bind(r,68091)),grid:()=>r.e("4351").then(r.bind(r,39090)),expandable:()=>r.e("9823").then(r.bind(r,78446)),integer:()=>r.e("9456").then(r.bind(r,93285)),multi_select:()=>Promise.all([r.e("7493"),r.e("5079"),r.e("1808")]).then(r.bind(r,87092)),positive_time_period_dict:()=>r.e("5058").then(r.bind(r,96636)),select:()=>r.e("1083").then(r.bind(r,6102)),string:()=>r.e("9752").then(r.bind(r,58701))},u=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,a.Z)([(0,o.Mo)("ha-form")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof i.fl&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{"selector"in e||d[e.type]?.()}))}},{kind:"method",key:"render",value:function(){return i.dy`
      <div class="root" part="root">
        ${this.error&&this.error.base?i.dy`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{const t=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),r=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return i.dy`
            ${t?i.dy`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(t,e)}
                  </ha-alert>
                `:r?i.dy`
                    <ha-alert own-margin alert-type="warning">
                      ${this._computeWarning(r,e)}
                    </ha-alert>
                  `:""}
            ${"selector"in e?i.dy`<ha-selector
                  .schema=${e}
                  .hass=${this.hass}
                  .name=${e.name}
                  .selector=${e.selector}
                  .value=${u(this.data,e)}
                  .label=${this._computeLabel(e,this.data)}
                  .disabled=${e.disabled||this.disabled||!1}
                  .placeholder=${e.required?"":e.default}
                  .helper=${this._computeHelper(e)}
                  .localizeValue=${this.localizeValue}
                  .required=${e.required||!1}
                  .context=${this._generateContext(e)}
                ></ha-selector>`:(0,l.h)(this.fieldElementName(e.type),{schema:e,data:u(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})}
          `}))}
      </div>
    `}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[r,a]of Object.entries(e.context))t[r]=this.data[a];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,n.Z)(r,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const r=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...r},(0,s.B)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?i.dy`<ul>
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
  `}}]}}),i.oi)},36719:function(e,t,r){r.d(t,{ON:()=>o,PX:()=>l,V_:()=>s,lz:()=>i,nZ:()=>n,rk:()=>u});var a=r(95907);const n="unavailable",i="unknown",o="on",l="off",s=[n,i],d=[n,i,l],u=(0,a.z)(s);(0,a.z)(d)}};
//# sourceMappingURL=2750.1498f7da436b7af2.js.map