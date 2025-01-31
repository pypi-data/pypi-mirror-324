"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1704"],{71942:function(e,a,o){o.a(e,(async function(e,a){try{var t=o(73577),i=(o(71695),o(61893),o(40251),o(39527),o(99790),o(47021),o(57243)),s=o(50778),d=o(49672),n=o(11297),r=o(32770),l=o(46999),u=(o(17949),o(69484)),c=(o(74064),e([u]));u=(c.then?(await c)():c)[0];let h,v,k,p,y=e=>e;const f=e=>(0,i.dy)(h||(h=y`<ha-list-item twoline graphic="icon">
    <span>${0}</span>
    <span slot="secondary">${0}</span>
    ${0}
  </ha-list-item>`),e.name,e.slug,e.icon?(0,i.dy)(v||(v=y`<img
          alt=""
          slot="graphic"
          .src="/api/hassio/addons/${0}/icon"
        />`),e.slug):"");(0,t.Z)([(0,s.Mo)("ha-addon-picker")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"value",value(){return""}},{kind:"field",decorators:[(0,s.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_addons",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,s.IO)("ha-combo-box")],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_error",value:void 0},{kind:"method",key:"open",value:function(){var e;null===(e=this._comboBox)||void 0===e||e.open()}},{kind:"method",key:"focus",value:function(){var e;null===(e=this._comboBox)||void 0===e||e.focus()}},{kind:"method",key:"firstUpdated",value:function(){this._getAddons()}},{kind:"method",key:"render",value:function(){return this._error?(0,i.dy)(k||(k=y`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):this._addons?(0,i.dy)(p||(p=y`
      <ha-combo-box
        .hass=${0}
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .helper=${0}
        .renderer=${0}
        .items=${0}
        item-value-path="slug"
        item-id-path="slug"
        item-label-path="name"
        @value-changed=${0}
      ></ha-combo-box>
    `),this.hass,void 0===this.label&&this.hass?this.hass.localize("ui.components.addon-picker.addon"):this.label,this._value,this.required,this.disabled,this.helper,f,this._addons,this._addonChanged):i.Ld}},{kind:"method",key:"_getAddons",value:async function(){try{if((0,d.p)(this.hass,"hassio")){const e=await(0,l.yt)(this.hass);this._addons=e.addons.filter((e=>e.version)).sort(((e,a)=>(0,r.$)(e.name,a.name,this.hass.locale.language)))}else this._error=this.hass.localize("ui.components.addon-picker.error.no_supervisor")}catch(e){this._error=this.hass.localize("ui.components.addon-picker.error.fetch_addons")}}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_addonChanged",value:function(e){e.stopPropagation();const a=e.detail.value;a!==this._value&&this._setValue(a)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,n.B)(this,"value-changed",{value:e}),(0,n.B)(this,"change")}),0)}}]}}),i.oi);a()}catch(h){a(h)}}))},4608:function(e,a,o){o.a(e,(async function(e,t){try{o.r(a),o.d(a,{HaAddonSelector:()=>h});var i=o(73577),s=(o(71695),o(47021),o(57243)),d=o(50778),n=o(71942),r=e([n]);n=(r.then?(await r)():r)[0];let l,u,c=e=>e,h=(0,i.Z)([(0,d.Mo)("ha-selector-addon")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return(0,s.dy)(l||(l=c`<ha-addon-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .disabled=${0}
      .required=${0}
      allow-custom-entity
    ></ha-addon-picker>`),this.hass,this.value,this.label,this.helper,this.disabled,this.required)}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(u||(u=c`
    ha-addon-picker {
      width: 100%;
    }
  `))}}]}}),s.oi);t()}catch(l){t(l)}}))},46999:function(e,a,o){o.d(a,{yt:()=>s,fU:()=>n,kP:()=>d});o(52247),o(40251),o(39527),o(67670);var t=o(99642),i=o(81054);const s=async e=>(0,t.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):(0,i.rY)(await e.callApi("GET","hassio/addons")),d=async(e,a)=>(0,t.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:`/addons/${a}/start`,method:"post",timeout:null}):e.callApi("POST",`hassio/addons/${a}/start`),n=async(e,a)=>{(0,t.I)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:`/addons/${a}/install`,method:"post",timeout:null}):await e.callApi("POST",`hassio/addons/${a}/install`)}},81054:function(e,a,o){o.d(a,{js:()=>i,rY:()=>t});o(19083),o(71695),o(40251),o(92519),o(42179),o(89256),o(24931),o(88463),o(57449),o(19814),o(61006),o(47021),o(99642);const t=e=>e.data,i=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])}}]);
//# sourceMappingURL=1704.1f79aef9eb8355e6.js.map