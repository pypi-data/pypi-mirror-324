/*! For license information please see 1748.bf0acdcd4f30b85b.js.LICENSE.txt */
export const ids=["1748"];export const modules={13766:function(t,i,e){e.a(t,(async function(t,i){try{var s=e(44249),a=(e(87319),e(57243)),n=e(50778),d=e(27486),c=e(24785),l=e(11297),r=e(32770),o=e(76500),u=e(26205),h=(e(69484),e(10508),e(21881)),v=e(59848),k=t([h]);h=(k.then?(await k)():k)[0];(0,s.Z)([(0,n.Mo)("ha-statistic-picker")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"statistic-types"})],key:"statisticTypes",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1,type:Array})],key:"statisticIds",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Array,attribute:"include-statistics-unit-of-measurement"})],key:"includeStatisticsUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"include-unit-class"})],key:"includeUnitClass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"include-device-class"})],key:"includeDeviceClass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"entities-only"})],key:"entitiesOnly",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Array,attribute:"exclude-statistics"})],key:"excludeStatistics",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"helpMissingEntityUrl",value(){return"/more-info/statistics/"}},{kind:"field",decorators:[(0,n.SB)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.IO)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value(){return!1}},{kind:"field",key:"_statistics",value(){return[]}},{kind:"field",decorators:[(0,n.SB)()],key:"_filteredItems",value(){}},{kind:"field",key:"_rowRenderer",value(){return t=>a.dy`<mwc-list-item graphic="avatar" twoline>
      ${t.state?a.dy`<state-badge
            slot="graphic"
            .stateObj=${t.state}
            .hass=${this.hass}
          ></state-badge>`:""}
      <span>${t.name}</span>
      <span slot="secondary"
        >${""===t.id||"__missing"===t.id?a.dy`<a
              target="_blank"
              rel="noopener noreferrer"
              href=${(0,u.R)(this.hass,this.helpMissingEntityUrl)}
              >${this.hass.localize("ui.components.statistic-picker.learn_more")}</a
            >`:t.id}</span
      >
    </mwc-list-item>`}},{kind:"field",key:"_getStatistics",value(){return(0,d.Z)(((t,i,e,s,a,n,d)=>{if(!t.length)return[{id:"",name:this.hass.localize("ui.components.statistic-picker.no_statistics"),strings:[]}];if(i){const e=(0,c.r)(i);t=t.filter((t=>e.includes(t.statistics_unit_of_measurement)))}if(e){const i=(0,c.r)(e);t=t.filter((t=>i.includes(t.unit_class)))}if(s){const i=(0,c.r)(s);t=t.filter((t=>{const e=this.hass.states[t.statistic_id];return!e||i.includes(e.attributes.device_class||"")}))}const l=[];return t.forEach((t=>{if(n&&t.statistic_id!==d&&n.includes(t.statistic_id))return;const i=this.hass.states[t.statistic_id];if(!i){if(!a){const i=t.statistic_id,e=(0,o.Kd)(this.hass,t.statistic_id,t);l.push({id:i,name:e,strings:[i,e]})}return}const e=t.statistic_id,s=(0,o.Kd)(this.hass,t.statistic_id,t);l.push({id:e,name:s,state:i,strings:[e,s]})})),l.length?(l.length>1&&l.sort(((t,i)=>(0,r.$)(t.name||"",i.name||"",this.hass.locale.language))),l.push({id:"__missing",name:this.hass.localize("ui.components.statistic-picker.missing_entity"),strings:[]}),l):[{id:"",name:this.hass.localize("ui.components.statistic-picker.no_match"),strings:[]}]}))}},{kind:"method",key:"open",value:function(){this.comboBox?.open()}},{kind:"method",key:"focus",value:function(){this.comboBox?.focus()}},{kind:"method",key:"willUpdate",value:function(t){(!this.hasUpdated&&!this.statisticIds||t.has("statisticTypes"))&&this._getStatisticIds(),(!this._init&&this.statisticIds||t.has("_opened")&&this._opened)&&(this._init=!0,this.hasUpdated?this._statistics=this._getStatistics(this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics,this.value):this.updateComplete.then((()=>{this._statistics=this._getStatistics(this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics,this.value)})))}},{kind:"method",key:"render",value:function(){return 0===this._statistics.length?a.Ld:a.dy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.statistic-picker.statistic"):this.label}
        .value=${this._value}
        .renderer=${this._rowRenderer}
        .disabled=${this.disabled}
        .allowCustomValue=${this.allowCustomEntity}
        .items=${this._statistics}
        .filteredItems=${this._filteredItems??this._statistics}
        item-value-path="id"
        item-id-path="id"
        item-label-path="name"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._statisticChanged}
        @filter-changed=${this._filterChanged}
      ></ha-combo-box>
    `}},{kind:"method",key:"_getStatisticIds",value:async function(){this.statisticIds=await(0,o.uR)(this.hass,this.statisticTypes)}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_statisticChanged",value:function(t){t.stopPropagation();let i=t.detail.value;"__missing"===i&&(i=""),i!==this._value&&this._setValue(i)}},{kind:"method",key:"_openedChanged",value:function(t){this._opened=t.detail.value}},{kind:"method",key:"_filterChanged",value:function(t){const i=t.detail.value.toLowerCase();this._filteredItems=i.length?(0,v.q)(i,this._statistics):void 0}},{kind:"method",key:"_setValue",value:function(t){this.value=t,setTimeout((()=>{(0,l.B)(this,"value-changed",{value:t}),(0,l.B)(this,"change")}),0)}}]}}),a.oi);i()}catch(y){i(y)}}))},58749:function(t,i,e){e.a(t,(async function(t,i){try{var s=e(44249),a=e(57243),n=e(50778),d=e(91583),c=e(11297),l=e(13766),r=t([l]);l=(r.then?(await r)():r)[0];(0,s.Z)([(0,n.Mo)("ha-statistics-picker")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1,type:Array})],key:"statisticIds",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"statistic-types"})],key:"statisticTypes",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"picked-statistic-label"})],key:"pickedStatisticLabel",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"pick-statistic-label"})],key:"pickStatisticLabel",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"include-statistics-unit-of-measurement"})],key:"includeStatisticsUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"include-unit-class"})],key:"includeUnitClass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"include-device-class"})],key:"includeDeviceClass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"ignore-restrictions-on-first-statistic"})],key:"ignoreRestrictionsOnFirstStatistic",value(){return!1}},{kind:"method",key:"render",value:function(){if(!this.hass)return a.Ld;const t=this.ignoreRestrictionsOnFirstStatistic&&this._currentStatistics.length<=1,i=t?void 0:this.includeStatisticsUnitOfMeasurement,e=t?void 0:this.includeUnitClass,s=t?void 0:this.includeDeviceClass,n=t?void 0:this.statisticTypes;return a.dy`
      ${(0,d.r)(this._currentStatistics,(t=>t),(t=>a.dy`
          <div>
            <ha-statistic-picker
              .curValue=${t}
              .hass=${this.hass}
              .includeStatisticsUnitOfMeasurement=${i}
              .includeUnitClass=${e}
              .includeDeviceClass=${s}
              .value=${t}
              .statisticTypes=${n}
              .statisticIds=${this.statisticIds}
              .label=${this.pickedStatisticLabel}
              .excludeStatistics=${this.value}
              .allowCustomEntity=${this.allowCustomEntity}
              @value-changed=${this._statisticChanged}
            ></ha-statistic-picker>
          </div>
        `))}
      <div>
        <ha-statistic-picker
          .hass=${this.hass}
          .includeStatisticsUnitOfMeasurement=${this.includeStatisticsUnitOfMeasurement}
          .includeUnitClass=${this.includeUnitClass}
          .includeDeviceClass=${this.includeDeviceClass}
          .statisticTypes=${this.statisticTypes}
          .statisticIds=${this.statisticIds}
          .label=${this.pickStatisticLabel}
          .excludeStatistics=${this.value}
          .allowCustomEntity=${this.allowCustomEntity}
          @value-changed=${this._addStatistic}
        ></ha-statistic-picker>
      </div>
    `}},{kind:"get",key:"_currentStatistics",value:function(){return this.value||[]}},{kind:"method",key:"_updateStatistics",value:async function(t){this.value=t,(0,c.B)(this,"value-changed",{value:t})}},{kind:"method",key:"_statisticChanged",value:function(t){t.stopPropagation();const i=t.currentTarget.curValue,e=t.detail.value;if(e===i)return;const s=this._currentStatistics;e&&!s.includes(e)?this._updateStatistics(s.map((t=>t===i?e:t))):this._updateStatistics(s.filter((t=>t!==i)))}},{kind:"method",key:"_addStatistic",value:async function(t){t.stopPropagation();const i=t.detail.value;if(!i)return;if(t.currentTarget.value="",!i)return;const e=this._currentStatistics;e.includes(i)||this._updateStatistics([...e,i])}},{kind:"field",static:!0,key:"styles",value(){return a.iv`
    :host {
      width: 200px;
      display: block;
    }
    ha-statistic-picker {
      display: block;
      width: 100%;
      margin-top: 8px;
    }
  `}}]}}),a.oi);i()}catch(o){i(o)}}))},76422:function(t,i,e){e.a(t,(async function(t,s){try{e.r(i),e.d(i,{HaStatisticSelector:()=>r});var a=e(44249),n=e(57243),d=e(50778),c=e(58749),l=t([c]);c=(l.then?(await l)():l)[0];let r=(0,a.Z)([(0,d.Mo)("ha-selector-statistic")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return this.selector.statistic.multiple?n.dy`
      ${this.label?n.dy`<label>${this.label}</label>`:""}
      <ha-statistics-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-statistics-picker>
    `:n.dy`<ha-statistic-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-entity
      ></ha-statistic-picker>`}}]}}),n.oi);s()}catch(r){s(r)}}))},36719:function(t,i,e){e.d(i,{ON:()=>d,PX:()=>c,V_:()=>l,lz:()=>n,nZ:()=>a,rk:()=>o});var s=e(95907);const a="unavailable",n="unknown",d="on",c="off",l=[a,n],r=[a,n,c],o=(0,s.z)(l);(0,s.z)(r)},76500:function(t,i,e){e.d(i,{Kd:()=>n,uR:()=>a});var s=e(73525);const a=(t,i)=>t.callWS({type:"recorder/list_statistic_ids",statistic_type:i}),n=(t,i,e)=>{const a=t.states[i];return a?(0,s.C)(a):e?.name||i}},26205:function(t,i,e){e.d(i,{R:()=>s});const s=(t,i)=>`https://${t.config.version.includes("b")?"rc":t.config.version.includes("dev")?"next":"www"}.home-assistant.io${i}`},94571:function(t,i,e){e.d(i,{C:()=>h});var s=e(2841),a=e(53232),n=e(1714);class d{constructor(t){this.G=t}disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}}class c{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null===(t=this.Z)||void 0===t||t.call(this),this.Y=this.Z=void 0}}var l=e(45779);const r=t=>!(0,a.pt)(t)&&"function"==typeof t.then,o=1073741823;class u extends n.sR{constructor(){super(...arguments),this._$C_t=o,this._$Cwt=[],this._$Cq=new d(this),this._$CK=new c}render(...t){var i;return null!==(i=t.find((t=>!r(t))))&&void 0!==i?i:s.Jb}update(t,i){const e=this._$Cwt;let a=e.length;this._$Cwt=i;const n=this._$Cq,d=this._$CK;this.isConnected||this.disconnected();for(let s=0;s<i.length&&!(s>this._$C_t);s++){const t=i[s];if(!r(t))return this._$C_t=s,t;s<a&&t===e[s]||(this._$C_t=o,a=0,Promise.resolve(t).then((async i=>{for(;d.get();)await d.get();const e=n.deref();if(void 0!==e){const s=e._$Cwt.indexOf(t);s>-1&&s<e._$C_t&&(e._$C_t=s,e.setValue(i))}})))}return s.Jb}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const h=(0,l.XM)(u)}};
//# sourceMappingURL=1748.bf0acdcd4f30b85b.js.map