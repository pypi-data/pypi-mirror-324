"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["9456"],{93285:function(e,i,a){a.r(i),a.d(i,{HaFormInteger:()=>c});var t=a(73577),d=(a(68212),a(63721),a(71695),a(23669),a(47021),a(57243)),s=a(50778),l=a(11297);a(97522),a(76418),a(20663),a(70596);let h,u,n,r,o,v=e=>e,c=(0,t.Z)([(0,s.Mo)("ha-form-integer")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"localize",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.IO)("ha-textfield ha-slider")],key:"_input",value:void 0},{kind:"field",key:"_lastValue",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){var e,i;return void 0!==this.schema.valueMin&&void 0!==this.schema.valueMax&&this.schema.valueMax-this.schema.valueMin<256?(0,d.dy)(h||(h=v`
        <div>
          ${0}
          <div class="flex">
            ${0}
            <ha-slider
              labeled
              .value=${0}
              .min=${0}
              .max=${0}
              .disabled=${0}
              @change=${0}
            ></ha-slider>
          </div>
          ${0}
        </div>
      `),this.label,this.schema.required?"":(0,d.dy)(u||(u=v`
                  <ha-checkbox
                    @change=${0}
                    .checked=${0}
                    .disabled=${0}
                  ></ha-checkbox>
                `),this._handleCheckboxChange,void 0!==this.data,this.disabled),this._value,this.schema.valueMin,this.schema.valueMax,this.disabled||void 0===this.data&&!this.schema.required,this._valueChanged,this.helper?(0,d.dy)(n||(n=v`<ha-input-helper-text>${0}</ha-input-helper-text>`),this.helper):""):(0,d.dy)(r||(r=v`
      <ha-textfield
        type="number"
        inputMode="numeric"
        .label=${0}
        .helper=${0}
        helperPersistent
        .value=${0}
        .disabled=${0}
        .required=${0}
        .autoValidate=${0}
        .suffix=${0}
        .validationMessage=${0}
        @input=${0}
      ></ha-textfield>
    `),this.label,this.helper,void 0!==this.data?this.data:"",this.disabled,this.schema.required,this.schema.required,null===(e=this.schema.description)||void 0===e?void 0:e.suffix,this.schema.required?null===(i=this.localize)||void 0===i?void 0:i.call(this,"ui.common.error_required"):void 0,this._valueChanged)}},{kind:"method",key:"updated",value:function(e){e.has("schema")&&this.toggleAttribute("own-margin",!("valueMin"in this.schema&&"valueMax"in this.schema||!this.schema.required))}},{kind:"get",key:"_value",value:function(){var e,i;return void 0!==this.data?this.data:this.schema.required?void 0!==(null===(e=this.schema.description)||void 0===e?void 0:e.suggested_value)&&null!==(null===(i=this.schema.description)||void 0===i?void 0:i.suggested_value)||this.schema.default||this.schema.valueMin||0:this.schema.valueMin||0}},{kind:"method",key:"_handleCheckboxChange",value:function(e){let i;if(e.target.checked)for(const t of[this._lastValue,null===(a=this.schema.description)||void 0===a?void 0:a.suggested_value,this.schema.default,0]){var a;if(void 0!==t){i=t;break}}else this._lastValue=this.data;(0,l.B)(this,"value-changed",{value:i})}},{kind:"method",key:"_valueChanged",value:function(e){const i=e.target,a=i.value;let t;if(""!==a&&(t=parseInt(String(a))),this.data!==t)(0,l.B)(this,"value-changed",{value:t});else{const e=void 0===t?"":String(t);i.value!==e&&(i.value=e)}}},{kind:"field",static:!0,key:"styles",value(){return(0,d.iv)(o||(o=v`
    :host([own-margin]) {
      margin-bottom: 5px;
    }
    .flex {
      display: flex;
    }
    ha-slider {
      flex: 1;
    }
    ha-textfield {
      display: block;
    }
  `))}}]}}),d.oi)}}]);
//# sourceMappingURL=9456.08762355901514fe.js.map