"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8456"],{59795:function(e,i,t){t.r(i);var a=t(73577),s=(t(71695),t(19423),t(47021),t(57243)),n=t(50778),l=t(11297),o=(t(52158),t(61631),t(70596),t(66193));let d,u,h,r=e=>e;(0,a.Z)([(0,n.Mo)("ha-input_number-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_max",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_min",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_mode",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_step",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_unit_of_measurement",value:void 0},{kind:"set",key:"item",value:function(e){var i,t,a;(this._item=e,e)?(this._name=e.name||"",this._icon=e.icon||"",this._max=null!==(i=e.max)&&void 0!==i?i:100,this._min=null!==(t=e.min)&&void 0!==t?t:0,this._mode=e.mode||"slider",this._step=null!==(a=e.step)&&void 0!==a?a:1,this._unit_of_measurement=e.unit_of_measurement):(this._item={min:0,max:100},this._name="",this._icon="",this._max=100,this._min=0,this._mode="slider",this._step=1)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}},{kind:"method",key:"render",value:function(){var e;return this.hass?(0,s.dy)(d||(d=r`
      <div class="form">
        <ha-textfield
          .value=${0}
          .configValue=${0}
          @input=${0}
          .label=${0}
          autoValidate
          required
          .validationMessage=${0}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${0}
          .value=${0}
          .configValue=${0}
          @value-changed=${0}
          .label=${0}
        ></ha-icon-picker>
        <ha-textfield
          .value=${0}
          .configValue=${0}
          type="number"
          step="any"
          @input=${0}
          .label=${0}
        ></ha-textfield>
        <ha-textfield
          .value=${0}
          .configValue=${0}
          type="number"
          step="any"
          @input=${0}
          .label=${0}
        ></ha-textfield>
        ${0}
      </div>
    `),this._name,"name",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.name"),this.hass.localize("ui.dialogs.helper_settings.required_error_msg"),this.hass,this._icon,"icon",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.icon"),this._min,"min",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.input_number.min"),this._max,"max",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.input_number.max"),null!==(e=this.hass.userData)&&void 0!==e&&e.showAdvanced?(0,s.dy)(u||(u=r`
              <div class="layout horizontal center justified">
                ${0}
                <ha-formfield
                  .label=${0}
                >
                  <ha-radio
                    name="mode"
                    value="slider"
                    .checked=${0}
                    @change=${0}
                  ></ha-radio>
                </ha-formfield>
                <ha-formfield
                  .label=${0}
                >
                  <ha-radio
                    name="mode"
                    value="box"
                    .checked=${0}
                    @change=${0}
                  ></ha-radio>
                </ha-formfield>
              </div>
              <ha-textfield
                .value=${0}
                .configValue=${0}
                type="number"
                step="any"
                @input=${0}
                .label=${0}
              ></ha-textfield>

              <ha-textfield
                .value=${0}
                .configValue=${0}
                @input=${0}
                .label=${0}
              ></ha-textfield>
            `),this.hass.localize("ui.dialogs.helper_settings.input_number.mode"),this.hass.localize("ui.dialogs.helper_settings.input_number.slider"),"slider"===this._mode,this._modeChanged,this.hass.localize("ui.dialogs.helper_settings.input_number.box"),"box"===this._mode,this._modeChanged,this._step,"step",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.input_number.step"),this._unit_of_measurement||"","unit_of_measurement",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.input_number.unit_of_measurement")):""):s.Ld}},{kind:"method",key:"_modeChanged",value:function(e){(0,l.B)(this,"value-changed",{value:Object.assign(Object.assign({},this._item),{},{mode:e.target.value})})}},{kind:"method",key:"_valueChanged",value:function(e){var i;if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target,a=t.configValue,s="number"===t.type?Number(t.value):(null===(i=e.detail)||void 0===i?void 0:i.value)||t.value;if(this[`_${a}`]===s)return;const n=Object.assign({},this._item);void 0===s||""===s?delete n[a]:n[a]=s,(0,l.B)(this,"value-changed",{value:n})}},{kind:"get",static:!0,key:"styles",value:function(){return[o.Qx,(0,s.iv)(h||(h=r`
        .form {
          color: var(--primary-text-color);
        }

        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
      `))]}}]}}),s.oi)}}]);
//# sourceMappingURL=8456.7e972b010dd30c5c.js.map