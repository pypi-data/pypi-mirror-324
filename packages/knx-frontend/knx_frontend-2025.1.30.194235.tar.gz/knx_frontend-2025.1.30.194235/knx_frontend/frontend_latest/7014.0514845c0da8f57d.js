export const ids=["7014"];export const modules={34026:function(e,i,t){t.r(i);var a=t(44249),s=t(57243),l=t(50778),n=t(11297),o=(t(29939),t(70596),t(66193));(0,a.Z)([(0,l.Mo)("ha-counter-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_maximum",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_minimum",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_restore",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_initial",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_step",value:void 0},{kind:"set",key:"item",value:function(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._maximum=e.maximum??void 0,this._minimum=e.minimum??void 0,this._restore=e.restore??!0,this._step=e.step??1,this._initial=e.initial??0):(this._name="",this._icon="",this._maximum=void 0,this._minimum=void 0,this._restore=!0,this._step=1,this._initial=0)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus()))}},{kind:"method",key:"render",value:function(){return this.hass?s.dy`
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
          .value=${this._minimum}
          .configValue=${"minimum"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.minimum")}
        ></ha-textfield>
        <ha-textfield
          .value=${this._maximum}
          .configValue=${"maximum"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.maximum")}
        ></ha-textfield>
        <ha-textfield
          .value=${this._initial}
          .configValue=${"initial"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.initial")}
        ></ha-textfield>
        ${this.hass.userData?.showAdvanced?s.dy`
              <ha-textfield
                .value=${this._step}
                .configValue=${"step"}
                type="number"
                @input=${this._valueChanged}
                .label=${this.hass.localize("ui.dialogs.helper_settings.counter.step")}
              ></ha-textfield>
              <div class="row">
                <ha-switch
                  .checked=${this._restore}
                  .configValue=${"restore"}
                  @change=${this._valueChanged}
                >
                </ha-switch>
                <div>
                  ${this.hass.localize("ui.dialogs.helper_settings.counter.restore")}
                </div>
              </div>
            `:""}
      </div>
    `:s.Ld}},{kind:"method",key:"_valueChanged",value:function(e){if(!this.new&&!this._item)return;e.stopPropagation();const i=e.target,t=i.configValue,a="number"===i.type?""!==i.value?Number(i.value):void 0:"ha-switch"===i.localName?e.target.checked:e.detail?.value||i.value;if(this[`_${t}`]===a)return;const s={...this._item};void 0===a||""===a?delete s[t]:s[t]=a,(0,n.B)(this,"value-changed",{value:s})}},{kind:"get",static:!0,key:"styles",value:function(){return[o.Qx,s.iv`
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
      `]}}]}}),s.oi)}};
//# sourceMappingURL=7014.0514845c0da8f57d.js.map