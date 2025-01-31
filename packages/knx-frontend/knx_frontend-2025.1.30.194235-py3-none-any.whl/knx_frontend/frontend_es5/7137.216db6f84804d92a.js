"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["7137"],{65326:function(e,a,l){l.a(e,(async function(e,i){try{l.r(a),l.d(a,{HaLabelSelector:()=>b});var d=l(73577),r=(l(71695),l(47021),l(57243)),t=l(50778),s=l(24785),n=l(11297),o=l(35760),u=e([o]);o=(u.then?(await u)():u)[0];let h,c,k,v=e=>e,b=(0,d.Z)([(0,t.Mo)("ha-selector-label")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,t.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"name",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,t.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,t.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,t.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){var e;return this.selector.label.multiple?(0,r.dy)(h||(h=v`
        <ha-labels-picker
          no-add
          .hass=${0}
          .value=${0}
          .required=${0}
          .disabled=${0}
          .label=${0}
          @value-changed=${0}
        >
        </ha-labels-picker>
      `),this.hass,(0,s.r)(null!==(e=this.value)&&void 0!==e?e:[]),this.required,this.disabled,this.label,this._handleChange):(0,r.dy)(c||(c=v`
      <ha-label-picker
        no-add
        .hass=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .label=${0}
        @value-changed=${0}
      >
      </ha-label-picker>
    `),this.hass,this.value,this.required,this.disabled,this.label,this._handleChange)}},{kind:"method",key:"_handleChange",value:function(e){let a=e.detail.value;this.value!==a&&((""===a||Array.isArray(a)&&0===a.length)&&!this.required&&(a=void 0),(0,n.B)(this,"value-changed",{value:a}))}},{kind:"field",static:!0,key:"styles",value(){return(0,r.iv)(k||(k=v`
    ha-labels-picker {
      display: block;
      width: 100%;
    }
  `))}}]}}),r.oi);i()}catch(h){i(h)}}))}}]);
//# sourceMappingURL=7137.216db6f84804d92a.js.map