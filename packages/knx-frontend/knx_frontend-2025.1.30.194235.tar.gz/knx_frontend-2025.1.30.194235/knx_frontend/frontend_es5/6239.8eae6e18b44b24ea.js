"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6239"],{29241:function(e,i,t){t.r(i);var a=t(73577),s=(t(71695),t(19423),t(47021),t(57243)),o=t(50778),n=t(11297),r=(t(76418),t(52158),t(70596),t(66193));let l,d,h=e=>e;(0,a.Z)([(0,o.Mo)("ha-timer-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_duration",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_restore",value:void 0},{kind:"set",key:"item",value:function(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._duration=e.duration||"00:00:00",this._restore=e.restore||!1):(this._name="",this._icon="",this._duration="00:00:00",this._restore=!1)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}},{kind:"method",key:"render",value:function(){return this.hass?(0,s.dy)(l||(l=h`
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
          .configValue=${0}
          .value=${0}
          @input=${0}
          .label=${0}
        ></ha-textfield>
        <ha-formfield
          .label=${0}
        >
          <ha-checkbox
            .configValue=${0}
            .checked=${0}
            @click=${0}
          >
          </ha-checkbox>
        </ha-formfield>
      </div>
    `),this._name,"name",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.name"),this.hass.localize("ui.dialogs.helper_settings.required_error_msg"),this.hass,this._icon,"icon",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.icon"),"duration",this._duration,this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.timer.duration"),this.hass.localize("ui.dialogs.helper_settings.timer.restore"),"restore",this._restore,this._toggleRestore):s.Ld}},{kind:"method",key:"_valueChanged",value:function(e){var i;if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target.configValue,a=(null===(i=e.detail)||void 0===i?void 0:i.value)||e.target.value;if(this[`_${t}`]===a)return;const s=Object.assign({},this._item);a?s[t]=a:delete s[t],(0,n.B)(this,"value-changed",{value:s})}},{kind:"method",key:"_toggleRestore",value:function(){this._restore=!this._restore,(0,n.B)(this,"value-changed",{value:Object.assign(Object.assign({},this._item),{},{restore:this._restore})})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.Qx,(0,s.iv)(d||(d=h`
        .form {
          color: var(--primary-text-color);
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `))]}}]}}),s.oi)}}]);
//# sourceMappingURL=6239.8eae6e18b44b24ea.js.map