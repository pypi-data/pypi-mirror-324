export const ids=["2469"];export const modules={10376:function(e,i,t){t.r(i),t.d(i,{HaAreaSelector:()=>k});var s=t(44249),a=t(57243),r=t(50778),d=t(27486),n=t(24785),l=t(99523),o=t(11297),u=t(82659),c=t(87055),h=t(45634),v=(t(69181),t(44573));(0,s.Z)([(0,r.Mo)("ha-areas-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"no-add"})],key:"noAdd",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:"picked-area-label"})],key:"pickedAreaLabel",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:"pick-area-label"})],key:"pickAreaLabel",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"method",key:"render",value:function(){if(!this.hass)return a.Ld;const e=this._currentAreas;return a.dy`
      ${e.map((e=>a.dy`
          <div>
            <ha-area-picker
              .curValue=${e}
              .noAdd=${this.noAdd}
              .hass=${this.hass}
              .value=${e}
              .label=${this.pickedAreaLabel}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .deviceFilter=${this.deviceFilter}
              .entityFilter=${this.entityFilter}
              .disabled=${this.disabled}
              @value-changed=${this._areaChanged}
            ></ha-area-picker>
          </div>
        `))}
      <div>
        <ha-area-picker
          .noAdd=${this.noAdd}
          .hass=${this.hass}
          .label=${this.pickAreaLabel}
          .helper=${this.helper}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .deviceFilter=${this.deviceFilter}
          .entityFilter=${this.entityFilter}
          .disabled=${this.disabled}
          .placeholder=${this.placeholder}
          .required=${this.required&&!e.length}
          @value-changed=${this._addArea}
          .excludeAreas=${e}
        ></ha-area-picker>
      </div>
    `}},{kind:"get",key:"_currentAreas",value:function(){return this.value||[]}},{kind:"method",key:"_updateAreas",value:async function(e){this.value=e,(0,o.B)(this,"value-changed",{value:e})}},{kind:"method",key:"_areaChanged",value:function(e){e.stopPropagation();const i=e.currentTarget.curValue,t=e.detail.value;if(t===i)return;const s=this._currentAreas;t&&!s.includes(t)?this._updateAreas(s.map((e=>e===i?t:e))):this._updateAreas(s.filter((e=>e!==i)))}},{kind:"method",key:"_addArea",value:function(e){e.stopPropagation();const i=e.detail.value;if(!i)return;e.currentTarget.value="";const t=this._currentAreas;t.includes(i)||this._updateAreas([...t,i])}},{kind:"field",static:!0,key:"styles",value(){return a.iv`
    div {
      margin-top: 8px;
    }
  `}}]}}),(0,v.f)(a.oi));let k=(0,s.Z)([(0,r.Mo)("ha-selector-area")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,r.SB)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_configEntries",value:void 0},{kind:"field",key:"_deviceIntegrationLookup",value(){return(0,d.Z)(l.HP)}},{kind:"method",key:"_hasIntegration",value:function(e){return e.area?.entity&&(0,n.r)(e.area.entity).some((e=>e.integration))||e.area?.device&&(0,n.r)(e.area.device).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){e.has("selector")&&void 0!==this.value&&(this.selector.area?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,o.B)(this,"value-changed",{value:this.value})):!this.selector.area?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,o.B)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"updated",value:function(e){e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,u.m)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,c.pB)(this.hass).then((e=>{this._configEntries=e})))}},{kind:"method",key:"render",value:function(){return this._hasIntegration(this.selector)&&!this._entitySources?a.Ld:this.selector.area?.multiple?a.dy`
      <ha-areas-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .pickAreaLabel=${this.label}
        no-add
        .deviceFilter=${this.selector.area?.device?this._filterDevices:void 0}
        .entityFilter=${this.selector.area?.entity?this._filterEntities:void 0}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-areas-picker>
    `:a.dy`
        <ha-area-picker
          .hass=${this.hass}
          .value=${this.value}
          .label=${this.label}
          .helper=${this.helper}
          no-add
          .deviceFilter=${this.selector.area?.device?this._filterDevices:void 0}
          .entityFilter=${this.selector.area?.entity?this._filterEntities:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
        ></ha-area-picker>
      `}},{kind:"field",key:"_filterEntities",value(){return e=>!this.selector.area?.entity||(0,n.r)(this.selector.area.entity).some((i=>(0,h.lV)(i,e,this._entitySources)))}},{kind:"field",key:"_filterDevices",value(){return e=>{if(!this.selector.area?.device)return!0;const i=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,n.r)(this.selector.area.device).some((t=>(0,h.lE)(t,e,i)))}}}]}}),a.oi)},82659:function(e,i,t){t.d(i,{m:()=>r});const s=async(e,i,t,a,r,...d)=>{const n=r,l=n[e],o=l=>a&&a(r,l.result)!==l.cacheKey?(n[e]=void 0,s(e,i,t,a,r,...d)):l.result;if(l)return l instanceof Promise?l.then(o):o(l);const u=t(r,...d);return n[e]=u,u.then((t=>{n[e]={result:t,cacheKey:a?.(r,t)},setTimeout((()=>{n[e]=void 0}),i)}),(()=>{n[e]=void 0})),u},a=e=>e.callWS({type:"entity/source"}),r=e=>s("_entitySources",3e4,a,(e=>Object.keys(e.states).length),e)},44573:function(e,i,t){t.d(i,{f:()=>d});var s=t(44249),a=t(72621),r=t(50778);const d=e=>(0,s.Z)(null,(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.Z)(t,"connectedCallback",this,3)([]),this._checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,a.Z)(t,"disconnectedCallback",this,3)([]),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){if((0,a.Z)(t,"updated",this,3)([e]),e.has("hass"))this._checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const i of e.keys())if(this.hassSubscribeRequiredHostProps.includes(i))return void this._checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"_checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&!this.hassSubscribeRequiredHostProps?.some((e=>void 0===this[e]))&&(this.__unsubs=this.hassSubscribe())}}]}}),e)}};
//# sourceMappingURL=2469.12443dbad5915b44.js.map