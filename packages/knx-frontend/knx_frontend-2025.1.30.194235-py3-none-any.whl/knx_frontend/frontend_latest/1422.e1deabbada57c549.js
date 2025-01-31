export const ids=["1422"];export const modules={38344:function(i,e,t){t.r(e);var o=t(44249),n=(t(2060),t(57243)),s=t(50778),a=t(91583),l=t(11297),d=(t(20095),t(59897),t(74064),t(14002),t(70596),t(4557)),r=t(66193);(0,o.Z)([(0,s.Mo)("ha-input_select-form")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_options",value(){return[]}},{kind:"field",decorators:[(0,s.IO)("#option_input",!0)],key:"_optionInput",value:void 0},{kind:"method",key:"_optionMoved",value:function(i){i.stopPropagation();const{oldIndex:e,newIndex:t}=i.detail,o=this._options.concat(),n=o.splice(e,1)[0];o.splice(t,0,n),(0,l.B)(this,"value-changed",{value:{...this._item,options:o}})}},{kind:"set",key:"item",value:function(i){this._item=i,i?(this._name=i.name||"",this._icon=i.icon||"",this._options=i.options||[]):(this._name="",this._icon="",this._options=[])}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus()))}},{kind:"method",key:"render",value:function(){return this.hass?n.dy`
      <div class="form">
        <ha-textfield
          dialogInitialFocus
          autoValidate
          required
          .validationMessage=${this.hass.localize("ui.dialogs.helper_settings.required_error_msg")}
          .value=${this._name}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.name")}
          .configValue=${"name"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-icon-picker
          .hass=${this.hass}
          .value=${this._icon}
          .configValue=${"icon"}
          @value-changed=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.icon")}
        ></ha-icon-picker>
        <div class="header">
          ${this.hass.localize("ui.dialogs.helper_settings.input_select.options")}:
        </div>
        <ha-sortable @item-moved=${this._optionMoved} handle-selector=".handle">
          <mwc-list class="options">
            ${this._options.length?(0,a.r)(this._options,(i=>i),((i,e)=>n.dy`
                    <ha-list-item class="option" hasMeta>
                      <div class="optioncontent">
                        <div class="handle">
                          <ha-svg-icon .path=${"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"}></ha-svg-icon>
                        </div>
                        ${i}
                      </div>
                      <ha-icon-button
                        slot="meta"
                        .index=${e}
                        .label=${this.hass.localize("ui.dialogs.helper_settings.input_select.remove_option")}
                        @click=${this._removeOption}
                        .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                      ></ha-icon-button>
                    </ha-list-item>
                  `)):n.dy`
                  <ha-list-item noninteractive>
                    ${this.hass.localize("ui.dialogs.helper_settings.input_select.no_options")}
                  </ha-list-item>
                `}
          </mwc-list>
        </ha-sortable>
        <div class="layout horizontal center">
          <ha-textfield
            class="flex-auto"
            id="option_input"
            .label=${this.hass.localize("ui.dialogs.helper_settings.input_select.add_option")}
            @keydown=${this._handleKeyAdd}
          ></ha-textfield>
          <ha-button @click=${this._addOption}
            >${this.hass.localize("ui.dialogs.helper_settings.input_select.add")}</ha-button
          >
        </div>
      </div>
    `:n.Ld}},{kind:"method",key:"_handleKeyAdd",value:function(i){i.stopPropagation(),"Enter"===i.key&&this._addOption()}},{kind:"method",key:"_addOption",value:function(){const i=this._optionInput;i?.value&&((0,l.B)(this,"value-changed",{value:{...this._item,options:[...this._options,i.value]}}),i.value="")}},{kind:"method",key:"_removeOption",value:async function(i){const e=i.target.index;if(!(await(0,d.g7)(this,{title:this.hass.localize("ui.dialogs.helper_settings.input_select.confirm_delete.delete"),text:this.hass.localize("ui.dialogs.helper_settings.input_select.confirm_delete.prompt"),destructive:!0})))return;const t=[...this._options];t.splice(e,1),(0,l.B)(this,"value-changed",{value:{...this._item,options:t}})}},{kind:"method",key:"_valueChanged",value:function(i){if(!this.new&&!this._item)return;i.stopPropagation();const e=i.target.configValue,t=i.detail?.value||i.target.value;if(this[`_${e}`]===t)return;const o={...this._item};t?o[e]=t:delete o[e],(0,l.B)(this,"value-changed",{value:o})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.Qx,n.iv`
        .form {
          color: var(--primary-text-color);
        }
        .option {
          border: 1px solid var(--divider-color);
          border-radius: 4px;
          margin-top: 4px;
          --mdc-icon-button-size: 24px;
          --mdc-ripple-color: transparent;
          --mdc-list-side-padding: 16px;
          cursor: default;
          background-color: var(--card-background-color);
        }
        mwc-button {
          margin-left: 8px;
          margin-inline-start: 8px;
          margin-inline-end: initial;
        }
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        #option_input {
          margin-top: 8px;
        }
        .header {
          margin-top: 8px;
          margin-bottom: 8px;
        }
        .handle {
          cursor: move; /* fallback if grab cursor is unsupported */
          cursor: grab;
          padding-right: 12px;
          padding-inline-end: 12px;
          padding-inline-start: initial;
        }
        .handle ha-svg-icon {
          pointer-events: none;
          height: 24px;
        }
        .optioncontent {
          display: flex;
          align-items: center;
        }
      `]}}]}}),n.oi)}};
//# sourceMappingURL=1422.e1deabbada57c549.js.map