"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["2642"],{62304:function(e,a,i){var s=i(73577),t=(i(71695),i(47021),i(57243)),o=i(50778),l=i(11297);i(26375);let r,d=e=>e;(0,s.Z)([(0,o.Mo)("ha-aliases-editor")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Array})],key:"aliases",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){return this.aliases?(0,t.dy)(r||(r=d`
      <ha-multi-textfield
        .hass=${0}
        .value=${0}
        .disabled=${0}
        .label=${0}
        .removeLabel=${0}
        .addLabel=${0}
        item-index
        @value-changed=${0}
      >
      </ha-multi-textfield>
    `),this.hass,this.aliases,this.disabled,this.hass.localize("ui.dialogs.aliases.label"),this.hass.localize("ui.dialogs.aliases.remove"),this.hass.localize("ui.dialogs.aliases.add"),this._aliasesChanged):t.Ld}},{kind:"method",key:"_aliasesChanged",value:function(e){(0,l.B)(this,"value-changed",{value:e})}}]}}),t.oi)},89073:function(e,a,i){i.a(e,(async function(e,s){try{i.r(a);var t=i(73577),o=(i(71695),i(40251),i(92519),i(42179),i(89256),i(24931),i(88463),i(57449),i(19814),i(81804),i(39527),i(99790),i(13334),i(47021),i(31622),i(2060),i(57243)),l=i(50778),r=i(91583),d=i(27486),n=i(11297),h=(i(84573),i(13978),i(17949),i(62304),i(44118)),c=i(10581),u=(i(18805),i(10508),i(70596),i(69181)),v=i(66193),_=i(88233),m=i(71656),f=e([c,u]);[c,u]=f.then?(await f)():f;let p,k,y,g,$,A,b,C,w,z=e=>e;const x="M20 2H4C2.9 2 2 2.9 2 4V20C2 21.11 2.9 22 4 22H20C21.11 22 22 21.11 22 20V4C22 2.9 21.11 2 20 2M4 6L6 4H10.9L4 10.9V6M4 13.7L13.7 4H18.6L4 18.6V13.7M20 18L18 20H13.1L20 13.1V18M20 10.3L10.3 20H5.4L20 5.4V10.3Z";let L=(0,t.Z)(null,(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_aliases",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_level",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_submitting",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_addedAreas",value(){return new Set}},{kind:"field",decorators:[(0,l.SB)()],key:"_removedAreas",value(){return new Set}},{kind:"method",key:"showDialog",value:function(e){var a,i,s,t;this._params=e,this._error=void 0,this._name=this._params.entry?this._params.entry.name:this._params.suggestedName||"",this._aliases=(null===(a=this._params.entry)||void 0===a?void 0:a.aliases)||[],this._icon=(null===(i=this._params.entry)||void 0===i?void 0:i.icon)||null,this._level=null!==(s=null===(t=this._params.entry)||void 0===t?void 0:t.level)&&void 0!==s?s:null,this._addedAreas.clear(),this._removedAreas.clear()}},{kind:"method",key:"closeDialog",value:function(){this._error="",this._params=void 0,this._addedAreas.clear(),this._removedAreas.clear(),(0,n.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"field",key:"_floorAreas",value(){return(0,d.Z)(((e,a,i,s)=>Object.values(a).filter((a=>(a.floor_id===(null==e?void 0:e.floor_id)||i.has(a.area_id))&&!s.has(a.area_id)))))}},{kind:"method",key:"render",value:function(){var e;const a=this._floorAreas(null===(e=this._params)||void 0===e?void 0:e.entry,this.hass.areas,this._addedAreas,this._removedAreas);if(!this._params)return o.Ld;const i=this._params.entry,s=!this._isNameValid();return(0,o.dy)(p||(p=z`
      <ha-dialog
        open
        @closed=${0}
        .heading=${0}
      >
        <div>
          ${0}
          <div class="form">
            ${0}

            <ha-textfield
              .value=${0}
              @input=${0}
              .label=${0}
              .validationMessage=${0}
              required
              dialogInitialFocus
            ></ha-textfield>

            <ha-textfield
              .value=${0}
              @input=${0}
              .label=${0}
              type="number"
            ></ha-textfield>

            <ha-icon-picker
              .hass=${0}
              .value=${0}
              @value-changed=${0}
              .label=${0}
            >
              ${0}
            </ha-icon-picker>

            <h3 class="header">
              ${0}
            </h3>

            <p class="description">
              ${0}
            </p>
            ${0}
            <ha-area-picker
              no-add
              .hass=${0}
              @value-changed=${0}
              .excludeAreas=${0}
              .label=${0}
            ></ha-area-picker>

            <h3 class="header">
              ${0}
            </h3>

            <p class="description">
              ${0}
            </p>
            <ha-aliases-editor
              .hass=${0}
              .aliases=${0}
              @value-changed=${0}
            ></ha-aliases-editor>
          </div>
        </div>
        <mwc-button slot="secondaryAction" @click=${0}>
          ${0}
        </mwc-button>
        <mwc-button
          slot="primaryAction"
          @click=${0}
          .disabled=${0}
        >
          ${0}
        </mwc-button>
      </ha-dialog>
    `),this.closeDialog,(0,h.i)(this.hass,i?this.hass.localize("ui.panel.config.floors.editor.update_floor"):this.hass.localize("ui.panel.config.floors.editor.create_floor")),this._error?(0,o.dy)(k||(k=z`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):"",i?(0,o.dy)(y||(y=z`
                  <ha-settings-row>
                    <span slot="heading">
                      ${0}
                    </span>
                    <span slot="description">${0}</span>
                  </ha-settings-row>
                `),this.hass.localize("ui.panel.config.floors.editor.floor_id"),i.floor_id):o.Ld,this._name,this._nameChanged,this.hass.localize("ui.panel.config.floors.editor.name"),this.hass.localize("ui.panel.config.floors.editor.name_required"),this._level,this._levelChanged,this.hass.localize("ui.panel.config.floors.editor.level"),this.hass,this._icon,this._iconChanged,this.hass.localize("ui.panel.config.areas.editor.icon"),this._icon?o.Ld:(0,o.dy)(g||(g=z`
                    <ha-floor-icon
                      slot="fallback"
                      .floor=${0}
                    ></ha-floor-icon>
                  `),{level:this._level}),this.hass.localize("ui.panel.config.floors.editor.areas_section"),this.hass.localize("ui.panel.config.floors.editor.areas_description"),a.length?(0,o.dy)($||($=z`<ha-chip-set>
                  ${0}
                </ha-chip-set>`),(0,r.r)(a,(e=>e.area_id),(e=>(0,o.dy)(A||(A=z`<ha-input-chip
                        .area=${0}
                        @click=${0}
                        @remove=${0}
                        .label=${0}
                      >
                        ${0}
                      </ha-input-chip>`),e,this._openArea,this._removeArea,null==e?void 0:e.name,e.icon?(0,o.dy)(b||(b=z`<ha-icon
                              slot="icon"
                              .icon=${0}
                            ></ha-icon>`),e.icon):(0,o.dy)(C||(C=z`<ha-svg-icon
                              slot="icon"
                              .path=${0}
                            ></ha-svg-icon>`),x))))):o.Ld,this.hass,this._addArea,a.map((e=>e.area_id)),this.hass.localize("ui.panel.config.floors.editor.add_area"),this.hass.localize("ui.panel.config.floors.editor.aliases_section"),this.hass.localize("ui.panel.config.floors.editor.aliases_description"),this.hass,this._aliases,this._aliasesChanged,this.closeDialog,this.hass.localize("ui.common.cancel"),this._updateEntry,s||this._submitting,i?this.hass.localize("ui.common.save"):this.hass.localize("ui.common.create"))}},{kind:"method",key:"_openArea",value:function(e){const a=e.target.area;(0,_.E)(this,{entry:a,updateEntry:e=>(0,m.IO)(this.hass,a.area_id,e)})}},{kind:"method",key:"_removeArea",value:function(e){const a=e.target.area.area_id;if(this._addedAreas.has(a))return this._addedAreas.delete(a),void(this._addedAreas=new Set(this._addedAreas));this._removedAreas.add(a),this._removedAreas=new Set(this._removedAreas)}},{kind:"method",key:"_addArea",value:function(e){const a=e.detail.value;if(a){if(e.target.value="",this._removedAreas.has(a))return this._removedAreas.delete(a),void(this._removedAreas=new Set(this._removedAreas));this._addedAreas.add(a),this._addedAreas=new Set(this._addedAreas)}}},{kind:"method",key:"_isNameValid",value:function(){return""!==this._name.trim()}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._name=e.target.value}},{kind:"method",key:"_levelChanged",value:function(e){this._error=void 0,this._level=""===e.target.value?null:Number(e.target.value)}},{kind:"method",key:"_iconChanged",value:function(e){this._error=void 0,this._icon=e.detail.value}},{kind:"method",key:"_updateEntry",value:async function(){this._submitting=!0;const e=!this._params.entry;try{const a={name:this._name.trim(),icon:this._icon||(e?void 0:null),level:this._level,aliases:this._aliases};e?await this._params.createEntry(a,this._addedAreas):await this._params.updateEntry(a,this._addedAreas,this._removedAreas),this.closeDialog()}catch(a){this._error=a.message||this.hass.localize("ui.panel.config.floors.editor.unknown_error")}finally{this._submitting=!1}}},{kind:"method",key:"_aliasesChanged",value:function(e){this._aliases=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[v.Qx,v.yu,(0,o.iv)(w||(w=z`
        ha-textfield {
          display: block;
          margin-bottom: 16px;
        }
        ha-floor-icon {
          color: var(--secondary-text-color);
        }
        ha-chip-set {
          margin-bottom: 8px;
        }
      `))]}}]}}),o.oi);customElements.define("dialog-floor-registry-detail",L),s()}catch(p){s(p)}}))}}]);
//# sourceMappingURL=2642.8265aed02ffb2219.js.map