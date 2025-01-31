"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8660"],{66912:function(e,i,t){t.a(e,(async function(e,i){try{var s=t(73577),a=(t(19083),t(71695),t(61893),t(40251),t(61006),t(39527),t(92181),t(99790),t(13334),t(36993),t(47021),t(57243)),d=t(50778),l=t(27486),n=t(11297),r=t(79575),o=t(32770),c=t(59848),u=t(92374),h=t(69484),v=(t(74064),e([h]));h=(v.then?(await v)():v)[0];let k,y,f=e=>e;const b=e=>(0,a.dy)(k||(k=f`<ha-list-item .twoline=${0}>
    <span>${0}</span>
    <span slot="secondary">${0}</span>
  </ha-list-item>`),!!e.area,e.name,e.area);(0,s.Z)([(0,d.Mo)("ha-device-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Array,attribute:"exclude-devices"})],key:"excludeDevices",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,d.SB)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,d.IO)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value(){return!1}},{kind:"field",key:"_getDevices",value(){return(0,l.Z)(((e,i,t,s,a,d,l,n,c)=>{if(!e.length)return[{id:"no_devices",area:"",name:this.hass.localize("ui.components.device-picker.no_devices"),strings:[]}];let h={};(s||a||d||n)&&(h=(0,u.R6)(t));let v=e.filter((e=>e.id===this.value||!e.disabled_by));s&&(v=v.filter((e=>{const i=h[e.id];return!(!i||!i.length)&&h[e.id].some((e=>s.includes((0,r.M)(e.entity_id))))}))),a&&(v=v.filter((e=>{const i=h[e.id];return!i||!i.length||t.every((e=>!a.includes((0,r.M)(e.entity_id))))}))),c&&(v=v.filter((e=>!c.includes(e.id)))),d&&(v=v.filter((e=>{const i=h[e.id];return!(!i||!i.length)&&h[e.id].some((e=>{const i=this.hass.states[e.entity_id];return!!i&&(i.attributes.device_class&&d.includes(i.attributes.device_class))}))}))),n&&(v=v.filter((e=>{const i=h[e.id];return!(!i||!i.length)&&i.some((e=>{const i=this.hass.states[e.entity_id];return!!i&&n(i)}))}))),l&&(v=v.filter((e=>e.id===this.value||l(e))));const k=v.map((e=>{const t=(0,u.jL)(e,this.hass,h[e.id]);return{id:e.id,name:t||this.hass.localize("ui.components.device-picker.unnamed_device"),area:e.area_id&&i[e.area_id]?i[e.area_id].name:this.hass.localize("ui.components.device-picker.no_area"),strings:[t||""]}}));return k.length?1===k.length?k:k.sort(((e,i)=>(0,o.$)(e.name||"",i.name||"",this.hass.locale.language))):[{id:"no_devices",area:"",name:this.hass.localize("ui.components.device-picker.no_match"),strings:[]}]}))}},{kind:"method",key:"open",value:async function(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.open())}},{kind:"method",key:"focus",value:async function(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.focus())}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){this._init=!0;const e=this._getDevices(Object.values(this.hass.devices),this.hass.areas,Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeDevices);this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){return(0,a.dy)(y||(y=f`
      <ha-combo-box
        .hass=${0}
        .label=${0}
        .value=${0}
        .helper=${0}
        .renderer=${0}
        .disabled=${0}
        .required=${0}
        item-id-path="id"
        item-value-path="id"
        item-label-path="name"
        @opened-changed=${0}
        @value-changed=${0}
        @filter-changed=${0}
      ></ha-combo-box>
    `),this.hass,void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):this.label,this._value,this.helper,b,this.disabled,this.required,this._openedChanged,this._deviceChanged,this._filterChanged)}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_filterChanged",value:function(e){const i=e.target,t=e.detail.value.toLowerCase();i.filteredItems=t.length?(0,c.q)(t,i.items||[]):i.items}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();let i=e.detail.value;"no_devices"===i&&(i=""),i!==this._value&&this._setValue(i)}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,n.B)(this,"value-changed",{value:e}),(0,n.B)(this,"change")}),0)}}]}}),a.oi);i()}catch(k){i(k)}}))},95152:function(e,i,t){t.a(e,(async function(e,i){try{var s=t(73577),a=(t(19083),t(71695),t(40251),t(61006),t(39527),t(99790),t(13334),t(47021),t(57243)),d=t(50778),l=t(11297),n=t(66912),r=e([n]);n=(r.then?(await r)():r)[0];let o,c,u,h=e=>e;(0,s.Z)([(0,d.Mo)("ha-devices-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:"picked-device-label"})],key:"pickedDeviceLabel",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:"pick-device-label"})],key:"pickDeviceLabel",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return a.Ld;const e=this._currentDevices;return(0,a.dy)(o||(o=h`
      ${0}
      <div>
        <ha-device-picker
          allow-custom-entity
          .hass=${0}
          .helper=${0}
          .deviceFilter=${0}
          .entityFilter=${0}
          .includeDomains=${0}
          .excludeDomains=${0}
          .excludeDevices=${0}
          .includeDeviceClasses=${0}
          .label=${0}
          .disabled=${0}
          .required=${0}
          @value-changed=${0}
        ></ha-device-picker>
      </div>
    `),e.map((e=>(0,a.dy)(c||(c=h`
          <div>
            <ha-device-picker
              allow-custom-entity
              .curValue=${0}
              .hass=${0}
              .deviceFilter=${0}
              .entityFilter=${0}
              .includeDomains=${0}
              .excludeDomains=${0}
              .includeDeviceClasses=${0}
              .value=${0}
              .label=${0}
              .disabled=${0}
              @value-changed=${0}
            ></ha-device-picker>
          </div>
        `),e,this.hass,this.deviceFilter,this.entityFilter,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,e,this.pickedDeviceLabel,this.disabled,this._deviceChanged))),this.hass,this.helper,this.deviceFilter,this.entityFilter,this.includeDomains,this.excludeDomains,e,this.includeDeviceClasses,this.pickDeviceLabel,this.disabled,this.required&&!e.length,this._addDevice)}},{kind:"get",key:"_currentDevices",value:function(){return this.value||[]}},{kind:"method",key:"_updateDevices",value:async function(e){(0,l.B)(this,"value-changed",{value:e}),this.value=e}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();const i=e.currentTarget.curValue,t=e.detail.value;t!==i&&(void 0===t?this._updateDevices(this._currentDevices.filter((e=>e!==i))):this._updateDevices(this._currentDevices.map((e=>e===i?t:e))))}},{kind:"method",key:"_addDevice",value:async function(e){e.stopPropagation();const i=e.detail.value;if(e.currentTarget.value="",!i)return;const t=this._currentDevices;t.includes(i)||this._updateDevices([...t,i])}},{kind:"field",static:!0,key:"styles",value(){return(0,a.iv)(u||(u=h`
    div {
      margin-top: 8px;
    }
  `))}}]}}),a.oi);i()}catch(o){i(o)}}))},26784:function(e,i,t){t.a(e,(async function(e,s){try{t.r(i),t.d(i,{HaDeviceSelector:()=>$});var a=t(73577),d=t(72621),l=(t(71695),t(39527),t(99790),t(36993),t(47021),t(57243)),n=t(50778),r=t(27486),o=t(24785),c=t(11297),u=t(92374),h=t(82659),v=t(87055),k=t(45634),y=t(66912),f=t(95152),b=e([y,f]);[y,f]=b.then?(await b)():b;let p,m,_,g=e=>e,$=(0,a.Z)([(0,n.Mo)("ha-selector-device")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",key:"_deviceIntegrationLookup",value(){return(0,r.Z)(u.HP)}},{kind:"method",key:"_hasIntegration",value:function(e){var i,t;return(null===(i=e.device)||void 0===i?void 0:i.filter)&&(0,o.r)(e.device.filter).some((e=>e.integration))||(null===(t=e.device)||void 0===t?void 0:t.entity)&&(0,o.r)(e.device.entity).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){var i,t;e.has("selector")&&void 0!==this.value&&(null!==(i=this.selector.device)&&void 0!==i&&i.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,c.B)(this,"value-changed",{value:this.value})):null!==(t=this.selector.device)&&void 0!==t&&t.multiple||!Array.isArray(this.value)||(this.value=this.value[0],(0,c.B)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"updated",value:function(e){(0,d.Z)(t,"updated",this,3)([e]),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,h.m)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,v.pB)(this.hass).then((e=>{this._configEntries=e})))}},{kind:"method",key:"render",value:function(){var e,i,t;return this._hasIntegration(this.selector)&&!this._entitySources?l.Ld:null!==(e=this.selector.device)&&void 0!==e&&e.multiple?(0,l.dy)(m||(m=g`
      ${0}
      <ha-devices-picker
        .hass=${0}
        .value=${0}
        .helper=${0}
        .deviceFilter=${0}
        .entityFilter=${0}
        .disabled=${0}
        .required=${0}
      ></ha-devices-picker>
    `),this.label?(0,l.dy)(_||(_=g`<label>${0}</label>`),this.label):"",this.hass,this.value,this.helper,this._filterDevices,null!==(i=this.selector.device)&&void 0!==i&&i.entity?this._filterEntities:void 0,this.disabled,this.required):(0,l.dy)(p||(p=g`
        <ha-device-picker
          .hass=${0}
          .value=${0}
          .label=${0}
          .helper=${0}
          .deviceFilter=${0}
          .entityFilter=${0}
          .disabled=${0}
          .required=${0}
          allow-custom-entity
        ></ha-device-picker>
      `),this.hass,this.value,this.label,this.helper,this._filterDevices,null!==(t=this.selector.device)&&void 0!==t&&t.entity?this._filterEntities:void 0,this.disabled,this.required)}},{kind:"field",key:"_filterDevices",value(){return e=>{var i;if(null===(i=this.selector.device)||void 0===i||!i.filter)return!0;const t=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,o.r)(this.selector.device.filter).some((i=>(0,k.lE)(i,e,t)))}}},{kind:"field",key:"_filterEntities",value(){return e=>(0,o.r)(this.selector.device.entity).some((i=>(0,k.lV)(i,e,this._entitySources)))}}]}}),l.oi);s()}catch(p){s(p)}}))},82659:function(e,i,t){t.d(i,{m:()=>d});t(71695),t(40251),t(47021);const s=async(e,i,t,a,d,...l)=>{const n=d,r=n[e],o=r=>a&&a(d,r.result)!==r.cacheKey?(n[e]=void 0,s(e,i,t,a,d,...l)):r.result;if(r)return r instanceof Promise?r.then(o):o(r);const c=t(d,...l);return n[e]=c,c.then((t=>{n[e]={result:t,cacheKey:null==a?void 0:a(d,t)},setTimeout((()=>{n[e]=void 0}),i)}),(()=>{n[e]=void 0})),c},a=e=>e.callWS({type:"entity/source"}),d=e=>s("_entitySources",3e4,a,(e=>Object.keys(e.states).length),e)}}]);
//# sourceMappingURL=8660.1227cc1544820d68.js.map