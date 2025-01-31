export const ids=["6062"];export const modules={45207:function(e,o,a){a.r(o),a.d(o,{HaAddonSelector:()=>h});var i=a(44249),s=a(57243),t=a(50778),d=a(49672),n=a(11297),r=a(32770),l=a(46999);a(17949),a(69484),a(74064);const u=e=>s.dy`<ha-list-item twoline graphic="icon">
    <span>${e.name}</span>
    <span slot="secondary">${e.slug}</span>
    ${e.icon?s.dy`<img
          alt=""
          slot="graphic"
          .src="/api/hassio/addons/${e.slug}/icon"
        />`:""}
  </ha-list-item>`;(0,i.Z)([(0,t.Mo)("ha-addon-picker")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"value",value(){return""}},{kind:"field",decorators:[(0,t.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.SB)()],key:"_addons",value:void 0},{kind:"field",decorators:[(0,t.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,t.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,t.IO)("ha-combo-box")],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,t.SB)()],key:"_error",value:void 0},{kind:"method",key:"open",value:function(){this._comboBox?.open()}},{kind:"method",key:"focus",value:function(){this._comboBox?.focus()}},{kind:"method",key:"firstUpdated",value:function(){this._getAddons()}},{kind:"method",key:"render",value:function(){return this._error?s.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:this._addons?s.dy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.addon-picker.addon"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${u}
        .items=${this._addons}
        item-value-path="slug"
        item-id-path="slug"
        item-label-path="name"
        @value-changed=${this._addonChanged}
      ></ha-combo-box>
    `:s.Ld}},{kind:"method",key:"_getAddons",value:async function(){try{if((0,d.p)(this.hass,"hassio")){const e=await(0,l.yt)(this.hass);this._addons=e.addons.filter((e=>e.version)).sort(((e,o)=>(0,r.$)(e.name,o.name,this.hass.locale.language)))}else this._error=this.hass.localize("ui.components.addon-picker.error.no_supervisor")}catch(e){this._error=this.hass.localize("ui.components.addon-picker.error.fetch_addons")}}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_addonChanged",value:function(e){e.stopPropagation();const o=e.detail.value;o!==this._value&&this._setValue(o)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,n.B)(this,"value-changed",{value:e}),(0,n.B)(this,"change")}),0)}}]}}),s.oi);let h=(0,i.Z)([(0,t.Mo)("ha-selector-addon")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[(0,t.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,t.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,t.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return s.dy`<ha-addon-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      allow-custom-entity
    ></ha-addon-picker>`}},{kind:"field",static:!0,key:"styles",value(){return s.iv`
    ha-addon-picker {
      width: 100%;
    }
  `}}]}}),s.oi)},46999:function(e,o,a){a.d(o,{yt:()=>t,fU:()=>n,kP:()=>d});var i=a(99642),s=a(81054);const t=async e=>(0,i.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):(0,s.rY)(await e.callApi("GET","hassio/addons")),d=async(e,o)=>(0,i.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:`/addons/${o}/start`,method:"post",timeout:null}):e.callApi("POST",`hassio/addons/${o}/start`),n=async(e,o)=>{(0,i.I)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:`/addons/${o}/install`,method:"post",timeout:null}):await e.callApi("POST",`hassio/addons/${o}/install`)}},81054:function(e,o,a){a.d(o,{js:()=>s,rY:()=>i});const i=e=>e.data,s=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])}};
//# sourceMappingURL=6062.d43122452f41ee42.js.map