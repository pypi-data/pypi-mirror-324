"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8133"],{33641:function(e,i,t){t.a(e,(async function(e,i){try{var n=t(73577),a=(t(71695),t(61893),t(19423),t(40251),t(13334),t(47021),t(87319),t(57243)),o=t(50778),r=t(11297),s=t(32770),d=t(87055),l=t(1275),c=t(85019),u=t(69484),h=e([u]);u=(h.then?(await h)():h)[0];let v,k,y=e=>e;(0,n.Z)([(0,o.Mo)("ha-config-entry-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"integration",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"value",value(){return""}},{kind:"field",decorators:[(0,o.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,o.IO)("ha-combo-box")],key:"_comboBox",value:void 0},{kind:"method",key:"open",value:function(){var e;null===(e=this._comboBox)||void 0===e||e.open()}},{kind:"method",key:"focus",value:function(){var e;null===(e=this._comboBox)||void 0===e||e.focus()}},{kind:"method",key:"firstUpdated",value:function(){this._getConfigEntries()}},{kind:"field",key:"_rowRenderer",value(){return e=>{var i;return(0,a.dy)(v||(v=y`<mwc-list-item twoline graphic="icon">
      <span
        >${0}</span
      >
      <span slot="secondary">${0}</span>
      <img
        alt=""
        slot="graphic"
        src=${0}
        crossorigin="anonymous"
        referrerpolicy="no-referrer"
        @error=${0}
        @load=${0}
      />
    </mwc-list-item>`),e.title||this.hass.localize("ui.panel.config.integrations.config_entry.unnamed_entry"),e.localized_domain_name,(0,c.X1)({domain:e.domain,type:"icon",darkOptimized:null===(i=this.hass.themes)||void 0===i?void 0:i.darkMode}),this._onImageError,this._onImageLoad)}}},{kind:"method",key:"render",value:function(){return this._configEntries?(0,a.dy)(k||(k=y`
      <ha-combo-box
        .hass=${0}
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .helper=${0}
        .renderer=${0}
        .items=${0}
        item-value-path="entry_id"
        item-id-path="entry_id"
        item-label-path="title"
        @value-changed=${0}
      ></ha-combo-box>
    `),this.hass,void 0===this.label&&this.hass?this.hass.localize("ui.components.config-entry-picker.config_entry"):this.label,this._value,this.required,this.disabled,this.helper,this._rowRenderer,this._configEntries,this._valueChanged):a.Ld}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.visibility="hidden"}},{kind:"method",key:"_getConfigEntries",value:async function(){(0,d.pB)(this.hass,{type:["device","hub","service"],domain:this.integration}).then((e=>{this._configEntries=e.map((e=>Object.assign(Object.assign({},e),{},{localized_domain_name:(0,l.Lh)(this.hass.localize,e.domain)}))).sort(((e,i)=>(0,s.f)(e.localized_domain_name+e.title,i.localized_domain_name+i.title,this.hass.locale.language)))}))}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const i=e.detail.value;i!==this._value&&this._setValue(i)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,r.B)(this,"value-changed",{value:e}),(0,r.B)(this,"change")}),0)}}]}}),a.oi);i()}catch(v){i(v)}}))},84023:function(e,i,t){t.a(e,(async function(e,n){try{t.r(i),t.d(i,{HaConfigEntrySelector:()=>h});var a=t(73577),o=(t(71695),t(47021),t(57243)),r=t(50778),s=t(33641),d=e([s]);s=(d.then?(await d)():d)[0];let l,c,u=e=>e,h=(0,a.Z)([(0,r.Mo)("ha-selector-config_entry")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){var e;return(0,o.dy)(l||(l=u`<ha-config-entry-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .disabled=${0}
      .required=${0}
      .integration=${0}
      allow-custom-entity
    ></ha-config-entry-picker>`),this.hass,this.value,this.label,this.helper,this.disabled,this.required,null===(e=this.selector.config_entry)||void 0===e?void 0:e.integration)}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(c||(c=u`
    ha-config-entry-picker {
      width: 100%;
    }
  `))}}]}}),o.oi);n()}catch(l){n(l)}}))},1275:function(e,i,t){t.d(i,{F3:()=>a,Lh:()=>n,t4:()=>o});t(56587);const n=(e,i,t)=>e(`component.${i}.title`)||(null==t?void 0:t.name)||i,a=(e,i)=>{const t={type:"manifest/list"};return i&&(t.integrations=i),e.callWS(t)},o=(e,i)=>e.callWS({type:"manifest/get",integration:i})},85019:function(e,i,t){t.d(i,{X1:()=>n,u4:()=>a,zC:()=>o});t(88044);const n=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,a=e=>e.split("/")[4],o=e=>e.startsWith("https://brands.home-assistant.io/")}}]);
//# sourceMappingURL=8133.75489e917b83e7d3.js.map