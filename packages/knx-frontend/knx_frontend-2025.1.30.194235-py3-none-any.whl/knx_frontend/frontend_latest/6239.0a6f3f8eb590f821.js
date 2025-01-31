export const ids=["6239"];export const modules={29241:function(e,i,t){t.r(i);var a=t(44249),o=t(57243),s=t(50778),r=t(11297),l=(t(76418),t(52158),t(70596),t(66193));(0,a.Z)([(0,s.Mo)("ha-timer-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_duration",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_restore",value:void 0},{kind:"set",key:"item",value:function(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._duration=e.duration||"00:00:00",this._restore=e.restore||!1):(this._name="",this._icon="",this._duration="00:00:00",this._restore=!1)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus()))}},{kind:"method",key:"render",value:function(){return this.hass?o.dy`
      <div class="form">
        <ha-textfield
          .value=${this._name}
          .configValue=${"name"}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.name")}
          autoValidate
          required
          .validationMessage=${this.hass.localize("ui.dialogs.helper_settings.required_error_msg")}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${this.hass}
          .value=${this._icon}
          .configValue=${"icon"}
          @value-changed=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.icon")}
        ></ha-icon-picker>
        <ha-textfield
          .configValue=${"duration"}
          .value=${this._duration}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.timer.duration")}
        ></ha-textfield>
        <ha-formfield
          .label=${this.hass.localize("ui.dialogs.helper_settings.timer.restore")}
        >
          <ha-checkbox
            .configValue=${"restore"}
            .checked=${this._restore}
            @click=${this._toggleRestore}
          >
          </ha-checkbox>
        </ha-formfield>
      </div>
    `:o.Ld}},{kind:"method",key:"_valueChanged",value:function(e){if(!this.new&&!this._item)return;e.stopPropagation();const i=e.target.configValue,t=e.detail?.value||e.target.value;if(this[`_${i}`]===t)return;const a={...this._item};t?a[i]=t:delete a[i],(0,r.B)(this,"value-changed",{value:a})}},{kind:"method",key:"_toggleRestore",value:function(){this._restore=!this._restore,(0,r.B)(this,"value-changed",{value:{...this._item,restore:this._restore}})}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,o.iv`
        .form {
          color: var(--primary-text-color);
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `]}}]}}),o.oi)}};
//# sourceMappingURL=6239.0a6f3f8eb590f821.js.map