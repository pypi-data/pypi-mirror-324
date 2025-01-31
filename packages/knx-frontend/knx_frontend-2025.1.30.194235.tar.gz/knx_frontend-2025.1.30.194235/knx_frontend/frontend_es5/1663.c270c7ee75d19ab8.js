"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1663"],{2701:function(e,i,t){t.a(e,(async function(e,i){try{var s=t(73577),a=(t(19083),t(71695),t(40251),t(61006),t(39527),t(99790),t(13334),t(47021),t(57243)),r=t(50778),d=t(11297),n=t(44573),l=t(69181),o=e([l]);l=(o.then?(await o)():o)[0];let u,c,h,v=e=>e;(0,s.Z)([(0,r.Mo)("ha-areas-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"no-add"})],key:"noAdd",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:"picked-area-label"})],key:"pickedAreaLabel",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:"pick-area-label"})],key:"pickAreaLabel",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"method",key:"render",value:function(){if(!this.hass)return a.Ld;const e=this._currentAreas;return(0,a.dy)(u||(u=v`
      ${0}
      <div>
        <ha-area-picker
          .noAdd=${0}
          .hass=${0}
          .label=${0}
          .helper=${0}
          .includeDomains=${0}
          .excludeDomains=${0}
          .includeDeviceClasses=${0}
          .deviceFilter=${0}
          .entityFilter=${0}
          .disabled=${0}
          .placeholder=${0}
          .required=${0}
          @value-changed=${0}
          .excludeAreas=${0}
        ></ha-area-picker>
      </div>
    `),e.map((e=>(0,a.dy)(c||(c=v`
          <div>
            <ha-area-picker
              .curValue=${0}
              .noAdd=${0}
              .hass=${0}
              .value=${0}
              .label=${0}
              .includeDomains=${0}
              .excludeDomains=${0}
              .includeDeviceClasses=${0}
              .deviceFilter=${0}
              .entityFilter=${0}
              .disabled=${0}
              @value-changed=${0}
            ></ha-area-picker>
          </div>
        `),e,this.noAdd,this.hass,e,this.pickedAreaLabel,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.disabled,this._areaChanged))),this.noAdd,this.hass,this.pickAreaLabel,this.helper,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.disabled,this.placeholder,this.required&&!e.length,this._addArea,e)}},{kind:"get",key:"_currentAreas",value:function(){return this.value||[]}},{kind:"method",key:"_updateAreas",value:async function(e){this.value=e,(0,d.B)(this,"value-changed",{value:e})}},{kind:"method",key:"_areaChanged",value:function(e){e.stopPropagation();const i=e.currentTarget.curValue,t=e.detail.value;if(t===i)return;const s=this._currentAreas;t&&!s.includes(t)?this._updateAreas(s.map((e=>e===i?t:e))):this._updateAreas(s.filter((e=>e!==i)))}},{kind:"method",key:"_addArea",value:function(e){e.stopPropagation();const i=e.detail.value;if(!i)return;e.currentTarget.value="";const t=this._currentAreas;t.includes(i)||this._updateAreas([...t,i])}},{kind:"field",static:!0,key:"styles",value(){return(0,a.iv)(h||(h=v`
    div {
      margin-top: 8px;
    }
  `))}}]}}),(0,n.f)(a.oi));i()}catch(u){i(u)}}))},5491:function(e,i,t){t.a(e,(async function(e,s){try{t.r(i),t.d(i,{HaAreaSelector:()=>$});var a=t(73577),r=(t(71695),t(39527),t(36993),t(47021),t(57243)),d=t(50778),n=t(27486),l=t(24785),o=t(92374),u=t(11297),c=t(82659),h=t(87055),v=t(45634),k=t(69181),y=t(2701),b=e([k,y]);[k,y]=b.then?(await b)():b;let f,p,_=e=>e,$=(0,a.Z)([(0,d.Mo)("ha-selector-area")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,d.SB)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_configEntries",value:void 0},{kind:"field",key:"_deviceIntegrationLookup",value(){return(0,n.Z)(o.HP)}},{kind:"method",key:"_hasIntegration",value:function(e){var i,t;return(null===(i=e.area)||void 0===i?void 0:i.entity)&&(0,l.r)(e.area.entity).some((e=>e.integration))||(null===(t=e.area)||void 0===t?void 0:t.device)&&(0,l.r)(e.area.device).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){var i,t;e.has("selector")&&void 0!==this.value&&(null!==(i=this.selector.area)&&void 0!==i&&i.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,u.B)(this,"value-changed",{value:this.value})):null!==(t=this.selector.area)&&void 0!==t&&t.multiple||!Array.isArray(this.value)||(this.value=this.value[0],(0,u.B)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"updated",value:function(e){e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,c.m)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,h.pB)(this.hass).then((e=>{this._configEntries=e})))}},{kind:"method",key:"render",value:function(){var e,i,t,s,a;return this._hasIntegration(this.selector)&&!this._entitySources?r.Ld:null!==(e=this.selector.area)&&void 0!==e&&e.multiple?(0,r.dy)(p||(p=_`
      <ha-areas-picker
        .hass=${0}
        .value=${0}
        .helper=${0}
        .pickAreaLabel=${0}
        no-add
        .deviceFilter=${0}
        .entityFilter=${0}
        .disabled=${0}
        .required=${0}
      ></ha-areas-picker>
    `),this.hass,this.value,this.helper,this.label,null!==(i=this.selector.area)&&void 0!==i&&i.device?this._filterDevices:void 0,null!==(t=this.selector.area)&&void 0!==t&&t.entity?this._filterEntities:void 0,this.disabled,this.required):(0,r.dy)(f||(f=_`
        <ha-area-picker
          .hass=${0}
          .value=${0}
          .label=${0}
          .helper=${0}
          no-add
          .deviceFilter=${0}
          .entityFilter=${0}
          .disabled=${0}
          .required=${0}
        ></ha-area-picker>
      `),this.hass,this.value,this.label,this.helper,null!==(s=this.selector.area)&&void 0!==s&&s.device?this._filterDevices:void 0,null!==(a=this.selector.area)&&void 0!==a&&a.entity?this._filterEntities:void 0,this.disabled,this.required)}},{kind:"field",key:"_filterEntities",value(){return e=>{var i;return null===(i=this.selector.area)||void 0===i||!i.entity||(0,l.r)(this.selector.area.entity).some((i=>(0,v.lV)(i,e,this._entitySources)))}}},{kind:"field",key:"_filterDevices",value(){return e=>{var i;if(null===(i=this.selector.area)||void 0===i||!i.device)return!0;const t=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,l.r)(this.selector.area.device).some((i=>(0,v.lE)(i,e,t)))}}}]}}),r.oi);s()}catch(f){s(f)}}))},82659:function(e,i,t){t.d(i,{m:()=>r});t(71695),t(40251),t(47021);const s=async(e,i,t,a,r,...d)=>{const n=r,l=n[e],o=l=>a&&a(r,l.result)!==l.cacheKey?(n[e]=void 0,s(e,i,t,a,r,...d)):l.result;if(l)return l instanceof Promise?l.then(o):o(l);const u=t(r,...d);return n[e]=u,u.then((t=>{n[e]={result:t,cacheKey:null==a?void 0:a(r,t)},setTimeout((()=>{n[e]=void 0}),i)}),(()=>{n[e]=void 0})),u},a=e=>e.callWS({type:"entity/source"}),r=e=>s("_entitySources",3e4,a,(e=>Object.keys(e.states).length),e)},44573:function(e,i,t){t.d(i,{f:()=>d});var s=t(73577),a=t(72621),r=(t(19083),t(71695),t(40251),t(61006),t(39527),t(36993),t(47021),t(50778));const d=e=>(0,s.Z)(null,(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.Z)(t,"connectedCallback",this,3)([]),this._checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,a.Z)(t,"disconnectedCallback",this,3)([]),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){if((0,a.Z)(t,"updated",this,3)([e]),e.has("hass"))this._checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const i of e.keys())if(this.hassSubscribeRequiredHostProps.includes(i))return void this._checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"_checkSubscribed",value:function(){var e;void 0!==this.__unsubs||!this.isConnected||void 0===this.hass||null!==(e=this.hassSubscribeRequiredHostProps)&&void 0!==e&&e.some((e=>void 0===this[e]))||(this.__unsubs=this.hassSubscribe())}}]}}),e)}}]);
//# sourceMappingURL=1663.c270c7ee75d19ab8.js.map