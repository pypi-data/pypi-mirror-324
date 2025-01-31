"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1422"],{38344:function(e,i,t){t.r(i);var n=t(73577),o=(t(71695),t(19423),t(40251),t(47021),t(2060),t(57243)),s=t(50778),a=t(91583),l=t(11297),d=(t(20095),t(59897),t(74064),t(14002),t(70596),t(4557)),r=t(66193);let c,h,u,p,v=e=>e;(0,n.Z)([(0,s.Mo)("ha-input_select-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_options",value(){return[]}},{kind:"field",decorators:[(0,s.IO)("#option_input",!0)],key:"_optionInput",value:void 0},{kind:"method",key:"_optionMoved",value:function(e){e.stopPropagation();const{oldIndex:i,newIndex:t}=e.detail,n=this._options.concat(),o=n.splice(i,1)[0];n.splice(t,0,o),(0,l.B)(this,"value-changed",{value:Object.assign(Object.assign({},this._item),{},{options:n})})}},{kind:"set",key:"item",value:function(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._options=e.options||[]):(this._name="",this._icon="",this._options=[])}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}},{kind:"method",key:"render",value:function(){return this.hass?(0,o.dy)(c||(c=v`
      <div class="form">
        <ha-textfield
          dialogInitialFocus
          autoValidate
          required
          .validationMessage=${0}
          .value=${0}
          .label=${0}
          .configValue=${0}
          @input=${0}
        ></ha-textfield>
        <ha-icon-picker
          .hass=${0}
          .value=${0}
          .configValue=${0}
          @value-changed=${0}
          .label=${0}
        ></ha-icon-picker>
        <div class="header">
          ${0}:
        </div>
        <ha-sortable @item-moved=${0} handle-selector=".handle">
          <mwc-list class="options">
            ${0}
          </mwc-list>
        </ha-sortable>
        <div class="layout horizontal center">
          <ha-textfield
            class="flex-auto"
            id="option_input"
            .label=${0}
            @keydown=${0}
          ></ha-textfield>
          <ha-button @click=${0}
            >${0}</ha-button
          >
        </div>
      </div>
    `),this.hass.localize("ui.dialogs.helper_settings.required_error_msg"),this._name,this.hass.localize("ui.dialogs.helper_settings.generic.name"),"name",this._valueChanged,this.hass,this._icon,"icon",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.icon"),this.hass.localize("ui.dialogs.helper_settings.input_select.options"),this._optionMoved,this._options.length?(0,a.r)(this._options,(e=>e),((e,i)=>(0,o.dy)(h||(h=v`
                    <ha-list-item class="option" hasMeta>
                      <div class="optioncontent">
                        <div class="handle">
                          <ha-svg-icon .path=${0}></ha-svg-icon>
                        </div>
                        ${0}
                      </div>
                      <ha-icon-button
                        slot="meta"
                        .index=${0}
                        .label=${0}
                        @click=${0}
                        .path=${0}
                      ></ha-icon-button>
                    </ha-list-item>
                  `),"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z",e,i,this.hass.localize("ui.dialogs.helper_settings.input_select.remove_option"),this._removeOption,"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"))):(0,o.dy)(u||(u=v`
                  <ha-list-item noninteractive>
                    ${0}
                  </ha-list-item>
                `),this.hass.localize("ui.dialogs.helper_settings.input_select.no_options")),this.hass.localize("ui.dialogs.helper_settings.input_select.add_option"),this._handleKeyAdd,this._addOption,this.hass.localize("ui.dialogs.helper_settings.input_select.add")):o.Ld}},{kind:"method",key:"_handleKeyAdd",value:function(e){e.stopPropagation(),"Enter"===e.key&&this._addOption()}},{kind:"method",key:"_addOption",value:function(){const e=this._optionInput;null!=e&&e.value&&((0,l.B)(this,"value-changed",{value:Object.assign(Object.assign({},this._item),{},{options:[...this._options,e.value]})}),e.value="")}},{kind:"method",key:"_removeOption",value:async function(e){const i=e.target.index;if(!(await(0,d.g7)(this,{title:this.hass.localize("ui.dialogs.helper_settings.input_select.confirm_delete.delete"),text:this.hass.localize("ui.dialogs.helper_settings.input_select.confirm_delete.prompt"),destructive:!0})))return;const t=[...this._options];t.splice(i,1),(0,l.B)(this,"value-changed",{value:Object.assign(Object.assign({},this._item),{},{options:t})})}},{kind:"method",key:"_valueChanged",value:function(e){var i;if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target.configValue,n=(null===(i=e.detail)||void 0===i?void 0:i.value)||e.target.value;if(this[`_${t}`]===n)return;const o=Object.assign({},this._item);n?o[t]=n:delete o[t],(0,l.B)(this,"value-changed",{value:o})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.Qx,(0,o.iv)(p||(p=v`
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
      `))]}}]}}),o.oi)}}]);
//# sourceMappingURL=1422.91a345f7e6c20c0a.js.map