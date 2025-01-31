"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["7014"],{34026:function(e,i,t){t.r(i);var a=t(73577),l=(t(71695),t(19423),t(47021),t(57243)),s=t(50778),n=t(11297),o=(t(29939),t(70596),t(66193));let d,u,r,h=e=>e;(0,a.Z)([(0,s.Mo)("ha-counter-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_maximum",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_minimum",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_restore",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_initial",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_step",value:void 0},{kind:"set",key:"item",value:function(e){var i,t,a,l,s;(this._item=e,e)?(this._name=e.name||"",this._icon=e.icon||"",this._maximum=null!==(i=e.maximum)&&void 0!==i?i:void 0,this._minimum=null!==(t=e.minimum)&&void 0!==t?t:void 0,this._restore=null===(a=e.restore)||void 0===a||a,this._step=null!==(l=e.step)&&void 0!==l?l:1,this._initial=null!==(s=e.initial)&&void 0!==s?s:0):(this._name="",this._icon="",this._maximum=void 0,this._minimum=void 0,this._restore=!0,this._step=1,this._initial=0)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}},{kind:"method",key:"render",value:function(){var e;return this.hass?(0,l.dy)(d||(d=h`
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
          @input=${0}
          .label=${0}
        ></ha-textfield>
        <ha-textfield
          .value=${0}
          .configValue=${0}
          type="number"
          @input=${0}
          .label=${0}
        ></ha-textfield>
        <ha-textfield
          .value=${0}
          .configValue=${0}
          type="number"
          @input=${0}
          .label=${0}
        ></ha-textfield>
        ${0}
      </div>
    `),this._name,"name",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.name"),this.hass.localize("ui.dialogs.helper_settings.required_error_msg"),this.hass,this._icon,"icon",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.icon"),this._minimum,"minimum",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.minimum"),this._maximum,"maximum",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.maximum"),this._initial,"initial",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.initial"),null!==(e=this.hass.userData)&&void 0!==e&&e.showAdvanced?(0,l.dy)(u||(u=h`
              <ha-textfield
                .value=${0}
                .configValue=${0}
                type="number"
                @input=${0}
                .label=${0}
              ></ha-textfield>
              <div class="row">
                <ha-switch
                  .checked=${0}
                  .configValue=${0}
                  @change=${0}
                >
                </ha-switch>
                <div>
                  ${0}
                </div>
              </div>
            `),this._step,"step",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.step"),this._restore,"restore",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.restore")):""):l.Ld}},{kind:"method",key:"_valueChanged",value:function(e){var i;if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target,a=t.configValue,l="number"===t.type?""!==t.value?Number(t.value):void 0:"ha-switch"===t.localName?e.target.checked:(null===(i=e.detail)||void 0===i?void 0:i.value)||t.value;if(this[`_${a}`]===l)return;const s=Object.assign({},this._item);void 0===l||""===l?delete s[a]:s[a]=l,(0,n.B)(this,"value-changed",{value:s})}},{kind:"get",static:!0,key:"styles",value:function(){return[o.Qx,(0,l.iv)(r||(r=h`
        .form {
          color: var(--primary-text-color);
        }
        .row {
          margin-top: 12px;
          margin-bottom: 12px;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
        }
        .row div {
          margin-left: 16px;
          margin-inline-start: 16px;
          margin-inline-end: initial;
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `))]}}]}}),l.oi)}}]);
//# sourceMappingURL=7014.bb409b22576c4f4f.js.map