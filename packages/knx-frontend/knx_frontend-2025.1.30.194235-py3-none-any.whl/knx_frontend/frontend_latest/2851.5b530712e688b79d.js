/*! For license information please see 2851.5b530712e688b79d.js.LICENSE.txt */
export const ids=["2851"];export const modules={34082:function(e,t,i){i.d(t,{T:()=>s});const n=/^(\w+)\.(\w+)$/,s=e=>n.test(e)},94999:function(e,t,i){i.a(e,(async function(e,t){try{var n=i(44249),s=i(57243),a=i(50778),l=i(27486),d=i(11297),r=i(34082),o=i(59498),u=e([o]);o=(u.then?(await u)():u)[0];(0,n.Z)([(0,a.Mo)("ha-entities-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-unit-of-measurement"})],key:"includeUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-entities"})],key:"includeEntities",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"exclude-entities"})],key:"excludeEntities",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"picked-entity-label"})],key:"pickedEntityLabel",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"pick-entity-label"})],key:"pickEntityLabel",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1,type:Array})],key:"createDomains",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return s.Ld;const e=this._currentEntities;return s.dy`
      ${e.map((e=>s.dy`
          <div>
            <ha-entity-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeEntities=${this.includeEntities}
              .excludeEntities=${this.excludeEntities}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
              .entityFilter=${this.entityFilter}
              .value=${e}
              .label=${this.pickedEntityLabel}
              .disabled=${this.disabled}
              .createDomains=${this.createDomains}
              @value-changed=${this._entityChanged}
            ></ha-entity-picker>
          </div>
        `))}
      <div>
        <ha-entity-picker
          allow-custom-entity
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeEntities=${this.includeEntities}
          .excludeEntities=${this._excludeEntities(this.value,this.excludeEntities)}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
          .entityFilter=${this.entityFilter}
          .label=${this.pickEntityLabel}
          .helper=${this.helper}
          .disabled=${this.disabled}
          .createDomains=${this.createDomains}
          .required=${this.required&&!e.length}
          @value-changed=${this._addEntity}
        ></ha-entity-picker>
      </div>
    `}},{kind:"field",key:"_excludeEntities",value(){return(0,l.Z)(((e,t)=>void 0===e?t:[...t||[],...e]))}},{kind:"get",key:"_currentEntities",value:function(){return this.value||[]}},{kind:"method",key:"_updateEntities",value:async function(e){this.value=e,(0,d.B)(this,"value-changed",{value:e})}},{kind:"method",key:"_entityChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t||void 0!==i&&!(0,r.T)(i))return;const n=this._currentEntities;i&&!n.includes(i)?this._updateEntities(n.map((e=>e===t?i:e))):this._updateEntities(n.filter((e=>e!==t)))}},{kind:"method",key:"_addEntity",value:async function(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if(e.currentTarget.value="",!t)return;const i=this._currentEntities;i.includes(t)||this._updateEntities([...i,t])}},{kind:"field",static:!0,key:"styles",value(){return s.iv`
    div {
      margin-top: 8px;
    }
  `}}]}}),s.oi);t()}catch(c){t(c)}}))},59498:function(e,t,i){i.a(e,(async function(e,t){try{var n=i(44249),s=(i(74064),i(57243)),a=i(50778),l=i(27486),d=i(11297),r=i(79575),o=i(73525),u=i(59848),c=(i(69484),i(59897),i(10508),i(21881)),h=i(32770),y=i(73976),v=i(1275),k=i(56395),f=e([c]);c=(f.then?(await f)():f)[0];const m="___create-new-entity___";(0,n.Z)([(0,a.Mo)("ha-entity-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1,type:Array})],key:"createDomains",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-unit-of-measurement"})],key:"includeUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-entities"})],key:"includeEntities",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"exclude-entities"})],key:"excludeEntities",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"hide-clear-icon",type:Boolean})],key:"hideClearIcon",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({attribute:"item-label-path"})],key:"itemLabelPath",value(){return"friendly_name"}},{kind:"field",decorators:[(0,a.SB)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,a.IO)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"method",key:"open",value:async function(){await this.updateComplete,await(this.comboBox?.open())}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this.comboBox?.focus())}},{kind:"field",key:"_initedStates",value(){return!1}},{kind:"field",key:"_states",value(){return[]}},{kind:"field",key:"_rowRenderer",value(){return e=>s.dy`<ha-list-item graphic="avatar" .twoline=${!!e.entity_id}>
      ${e.state?s.dy`<state-badge
            slot="graphic"
            .stateObj=${e}
            .hass=${this.hass}
          ></state-badge>`:""}
      <span>${e.friendly_name}</span>
      <span slot="secondary"
        >${e.entity_id.startsWith(m)?this.hass.localize("ui.components.entity.entity-picker.new_entity"):e.entity_id}</span
      >
    </ha-list-item>`}},{kind:"field",key:"_getStates",value(){return(0,l.Z)(((e,t,i,n,s,a,l,d,u,c)=>{let y=[];if(!t)return[];let f=Object.keys(t.states);const p=c?.length?c.map((e=>{const i=t.localize("ui.components.entity.entity-picker.create_helper",{domain:(0,k.X)(e)?t.localize(`ui.panel.config.helpers.types.${e}`):(0,v.Lh)(t.localize,e)});return{entity_id:m+e,state:"on",last_changed:"",last_updated:"",context:{id:"",user_id:null,parent_id:null},friendly_name:i,attributes:{icon:"mdi:plus"},strings:[e,i]}})):[];return f.length?(d&&(f=f.filter((e=>d.includes(e)))),u&&(f=f.filter((e=>!u.includes(e)))),i&&(f=f.filter((e=>i.includes((0,r.M)(e))))),n&&(f=f.filter((e=>!n.includes((0,r.M)(e))))),y=f.map((e=>{const i=(0,o.C)(t.states[e])||e;return{...t.states[e],friendly_name:i,strings:[e,i]}})).sort(((e,t)=>(0,h.f)(e.friendly_name,t.friendly_name,this.hass.locale.language))),a&&(y=y.filter((e=>e.entity_id===this.value||e.attributes.device_class&&a.includes(e.attributes.device_class)))),l&&(y=y.filter((e=>e.entity_id===this.value||e.attributes.unit_of_measurement&&l.includes(e.attributes.unit_of_measurement)))),s&&(y=y.filter((e=>e.entity_id===this.value||s(e)))),y.length?(p?.length&&y.push(...p),y):[{entity_id:"",state:"",last_changed:"",last_updated:"",context:{id:"",user_id:null,parent_id:null},friendly_name:this.hass.localize("ui.components.entity.entity-picker.no_match"),attributes:{friendly_name:this.hass.localize("ui.components.entity.entity-picker.no_match"),icon:"mdi:magnify"},strings:[]},...p]):[{entity_id:"",state:"",last_changed:"",last_updated:"",context:{id:"",user_id:null,parent_id:null},friendly_name:this.hass.localize("ui.components.entity.entity-picker.no_entities"),attributes:{friendly_name:this.hass.localize("ui.components.entity.entity-picker.no_entities"),icon:"mdi:magnify"},strings:[]},...p]}))}},{kind:"method",key:"shouldUpdate",value:function(e){return!!(e.has("value")||e.has("label")||e.has("disabled"))||!(!e.has("_opened")&&this._opened)}},{kind:"method",key:"willUpdate",value:function(e){(!this._initedStates||e.has("_opened")&&this._opened)&&(this._states=this._getStates(this._opened,this.hass,this.includeDomains,this.excludeDomains,this.entityFilter,this.includeDeviceClasses,this.includeUnitOfMeasurement,this.includeEntities,this.excludeEntities,this.createDomains),this._initedStates&&(this.comboBox.filteredItems=this._states),this._initedStates=!0),e.has("createDomains")&&this.createDomains?.length&&this.hass.loadFragmentTranslation("config")}},{kind:"method",key:"render",value:function(){return s.dy`
      <ha-combo-box
        item-value-path="entity_id"
        .itemLabelPath=${this.itemLabelPath}
        .hass=${this.hass}
        .value=${this._value}
        .label=${void 0===this.label?this.hass.localize("ui.components.entity.entity-picker.entity"):this.label}
        .helper=${this.helper}
        .allowCustomValue=${this.allowCustomEntity}
        .filteredItems=${this._states}
        .renderer=${this._rowRenderer}
        .required=${this.required}
        .disabled=${this.disabled}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
        @filter-changed=${this._filterChanged}
      >
      </ha-combo-box>
    `}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value?.trim();if(t&&t.startsWith(m)){const e=t.substring(m.length);(0,y.j)(this,{domain:e,dialogClosedCallback:e=>{e.entityId&&this._setValue(e.entityId)}})}else t!==this._value&&this._setValue(t)}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.target,i=e.detail.value.trim().toLowerCase();t.filteredItems=i.length?(0,u.q)(i,this._states):this._states}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,d.B)(this,"value-changed",{value:e}),(0,d.B)(this,"change")}),0)}}]}}),s.oi);t()}catch(m){t(m)}}))},92697:function(e,t,i){i.a(e,(async function(e,n){try{i.r(t),i.d(t,{HaEntitySelector:()=>k});var s=i(44249),a=i(72621),l=i(57243),d=i(50778),r=i(24785),o=i(11297),u=i(82659),c=i(45634),h=i(94999),y=i(59498),v=e([h,y]);[h,y]=v.then?(await v)():v;let k=(0,s.Z)([(0,d.Mo)("ha-selector-entity")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,d.SB)()],key:"_createDomains",value:void 0},{kind:"method",key:"_hasIntegration",value:function(e){return e.entity?.filter&&(0,r.r)(e.entity.filter).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){e.has("selector")&&void 0!==this.value&&(this.selector.entity?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,o.B)(this,"value-changed",{value:this.value})):!this.selector.entity?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,o.B)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"render",value:function(){return this._hasIntegration(this.selector)&&!this._entitySources?l.Ld:this.selector.entity?.multiple?l.dy`
      ${this.label?l.dy`<label>${this.label}</label>`:""}
      <ha-entities-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .includeEntities=${this.selector.entity.include_entities}
        .excludeEntities=${this.selector.entity.exclude_entities}
        .entityFilter=${this._filterEntities}
        .createDomains=${this._createDomains}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-entities-picker>
    `:l.dy`<ha-entity-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .includeEntities=${this.selector.entity?.include_entities}
        .excludeEntities=${this.selector.entity?.exclude_entities}
        .entityFilter=${this._filterEntities}
        .createDomains=${this._createDomains}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-entity
      ></ha-entity-picker>`}},{kind:"method",key:"updated",value:function(e){(0,a.Z)(i,"updated",this,3)([e]),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,u.m)(this.hass).then((e=>{this._entitySources=e})),e.has("selector")&&(this._createDomains=(0,c.bq)(this.selector))}},{kind:"field",key:"_filterEntities",value(){return e=>!this.selector?.entity?.filter||(0,r.r)(this.selector.entity.filter).some((t=>(0,c.lV)(t,e,this._entitySources)))}}]}}),l.oi);n()}catch(k){n(k)}}))},36719:function(e,t,i){i.d(t,{ON:()=>l,PX:()=>d,V_:()=>r,lz:()=>a,nZ:()=>s,rk:()=>u});var n=i(95907);const s="unavailable",a="unknown",l="on",d="off",r=[s,a],o=[s,a,d],u=(0,n.z)(r);(0,n.z)(o)},82659:function(e,t,i){i.d(t,{m:()=>a});const n=async(e,t,i,s,a,...l)=>{const d=a,r=d[e],o=r=>s&&s(a,r.result)!==r.cacheKey?(d[e]=void 0,n(e,t,i,s,a,...l)):r.result;if(r)return r instanceof Promise?r.then(o):o(r);const u=i(a,...l);return d[e]=u,u.then((i=>{d[e]={result:i,cacheKey:s?.(a,i)},setTimeout((()=>{d[e]=void 0}),t)}),(()=>{d[e]=void 0})),u},s=e=>e.callWS({type:"entity/source"}),a=e=>n("_entitySources",3e4,s,(e=>Object.keys(e.states).length),e)},1275:function(e,t,i){i.d(t,{F3:()=>s,Lh:()=>n,t4:()=>a});const n=(e,t,i)=>e(`component.${t}.title`)||i?.name||t,s=(e,t)=>{const i={type:"manifest/list"};return t&&(i.integrations=t),e.callWS(i)},a=(e,t)=>e.callWS({type:"manifest/get",integration:t})},73976:function(e,t,i){i.d(t,{j:()=>a});var n=i(11297);const s=()=>i.e("6334").then(i.bind(i,84997)),a=(e,t)=>{(0,n.B)(e,"show-dialog",{dialogTag:"dialog-helper-detail",dialogImport:s,dialogParams:t})}},94571:function(e,t,i){i.d(t,{C:()=>h});var n=i(2841),s=i(53232),a=i(1714);class l{constructor(e){this.G=e}disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}}class d{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var e;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((e=>this.Z=e)))}resume(){var e;null===(e=this.Z)||void 0===e||e.call(this),this.Y=this.Z=void 0}}var r=i(45779);const o=e=>!(0,s.pt)(e)&&"function"==typeof e.then,u=1073741823;class c extends a.sR{constructor(){super(...arguments),this._$C_t=u,this._$Cwt=[],this._$Cq=new l(this),this._$CK=new d}render(...e){var t;return null!==(t=e.find((e=>!o(e))))&&void 0!==t?t:n.Jb}update(e,t){const i=this._$Cwt;let s=i.length;this._$Cwt=t;const a=this._$Cq,l=this._$CK;this.isConnected||this.disconnected();for(let n=0;n<t.length&&!(n>this._$C_t);n++){const e=t[n];if(!o(e))return this._$C_t=n,e;n<s&&e===i[n]||(this._$C_t=u,s=0,Promise.resolve(e).then((async t=>{for(;l.get();)await l.get();const i=a.deref();if(void 0!==i){const n=i._$Cwt.indexOf(e);n>-1&&n<i._$C_t&&(i._$C_t=n,i.setValue(t))}})))}return n.Jb}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const h=(0,r.XM)(c)}};
//# sourceMappingURL=2851.5b530712e688b79d.js.map