export const ids=["2041"];export const modules={5924:function(e,i,t){t.r(i),t.d(i,{HaConfigEntrySelector:()=>u});var n=t(44249),o=t(57243),a=t(50778),r=(t(87319),t(11297)),s=t(32770),d=t(87055),l=t(1275),c=t(85019);t(69484);(0,n.Z)([(0,a.Mo)("ha-config-entry-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"integration",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"value",value(){return""}},{kind:"field",decorators:[(0,a.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,a.IO)("ha-combo-box")],key:"_comboBox",value:void 0},{kind:"method",key:"open",value:function(){this._comboBox?.open()}},{kind:"method",key:"focus",value:function(){this._comboBox?.focus()}},{kind:"method",key:"firstUpdated",value:function(){this._getConfigEntries()}},{kind:"field",key:"_rowRenderer",value(){return e=>o.dy`<mwc-list-item twoline graphic="icon">
      <span
        >${e.title||this.hass.localize("ui.panel.config.integrations.config_entry.unnamed_entry")}</span
      >
      <span slot="secondary">${e.localized_domain_name}</span>
      <img
        alt=""
        slot="graphic"
        src=${(0,c.X1)({domain:e.domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}
        crossorigin="anonymous"
        referrerpolicy="no-referrer"
        @error=${this._onImageError}
        @load=${this._onImageLoad}
      />
    </mwc-list-item>`}},{kind:"method",key:"render",value:function(){return this._configEntries?o.dy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.config-entry-picker.config_entry"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${this._rowRenderer}
        .items=${this._configEntries}
        item-value-path="entry_id"
        item-id-path="entry_id"
        item-label-path="title"
        @value-changed=${this._valueChanged}
      ></ha-combo-box>
    `:o.Ld}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.visibility="hidden"}},{kind:"method",key:"_getConfigEntries",value:async function(){(0,d.pB)(this.hass,{type:["device","hub","service"],domain:this.integration}).then((e=>{this._configEntries=e.map((e=>({...e,localized_domain_name:(0,l.Lh)(this.hass.localize,e.domain)}))).sort(((e,i)=>(0,s.f)(e.localized_domain_name+e.title,i.localized_domain_name+i.title,this.hass.locale.language)))}))}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const i=e.detail.value;i!==this._value&&this._setValue(i)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,r.B)(this,"value-changed",{value:e}),(0,r.B)(this,"change")}),0)}}]}}),o.oi);let u=(0,n.Z)([(0,a.Mo)("ha-selector-config_entry")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return o.dy`<ha-config-entry-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      .integration=${this.selector.config_entry?.integration}
      allow-custom-entity
    ></ha-config-entry-picker>`}},{kind:"field",static:!0,key:"styles",value(){return o.iv`
    ha-config-entry-picker {
      width: 100%;
    }
  `}}]}}),o.oi)},1275:function(e,i,t){t.d(i,{F3:()=>o,Lh:()=>n,t4:()=>a});const n=(e,i,t)=>e(`component.${i}.title`)||t?.name||i,o=(e,i)=>{const t={type:"manifest/list"};return i&&(t.integrations=i),e.callWS(t)},a=(e,i)=>e.callWS({type:"manifest/get",integration:i})},85019:function(e,i,t){t.d(i,{X1:()=>n,u4:()=>o,zC:()=>a});const n=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,o=e=>e.split("/")[4],a=e=>e.startsWith("https://brands.home-assistant.io/")}};
//# sourceMappingURL=2041.635866d5d72bbb6c.js.map