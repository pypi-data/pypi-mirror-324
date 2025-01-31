/*! For license information please see 6835.47e04e09e22793c4.js.LICENSE.txt */
"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6835"],{62304:function(e,i,t){var a=t(73577),s=(t(71695),t(47021),t(57243)),n=t(50778),r=t(11297);t(26375);let l,o=e=>e;(0,a.Z)([(0,n.Mo)("ha-aliases-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array})],key:"aliases",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){return this.aliases?(0,s.dy)(l||(l=o`
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
    `),this.hass,this.aliases,this.disabled,this.hass.localize("ui.dialogs.aliases.label"),this.hass.localize("ui.dialogs.aliases.remove"),this.hass.localize("ui.dialogs.aliases.add"),this._aliasesChanged):s.Ld}},{kind:"method",key:"_aliasesChanged",value:function(e){(0,r.B)(this,"value-changed",{value:e})}}]}}),s.oi)},86438:function(e,i,t){t.d(i,{Ft:()=>a,S$:()=>s,sy:()=>n});t(40251);const a="timestamp",s="temperature",n="humidity"},40600:function(e,i,t){t.a(e,(async function(e,a){try{t.r(i);var s=t(73577),n=(t(71695),t(40251),t(81804),t(47021),t(31622),t(2060),t(57243)),r=t(50778),l=t(11297),o=(t(17949),t(62304),t(44118)),h=t(10581),d=(t(18805),t(37643)),c=t(59498),u=(t(70596),t(35760)),_=t(66193),p=t(86438),y=e([h,d,c,u]);[h,d,c,u]=y.then?(await y)():y;let v,m,f,k,$,g=e=>e;const C={round:!1,type:"image/jpeg",quality:.75,aspectRatio:1.78},b=["sensor"],w=[p.S$],z=[p.sy];let E=(0,s.Z)(null,(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_aliases",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_labels",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_picture",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_floor",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_temperatureEntity",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_humidityEntity",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_submitting",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._error=void 0,this._params.entry?(this._name=this._params.entry.name,this._aliases=this._params.entry.aliases,this._labels=this._params.entry.labels,this._picture=this._params.entry.picture,this._icon=this._params.entry.icon,this._floor=this._params.entry.floor_id,this._temperatureEntity=this._params.entry.temperature_entity_id,this._humidityEntity=this._params.entry.humidity_entity_id):(this._name=this._params.suggestedName||"",this._aliases=[],this._labels=[],this._picture=null,this._icon=null,this._floor=null,this._temperatureEntity=null,this._humidityEntity=null),await this.updateComplete}},{kind:"method",key:"closeDialog",value:function(){this._error="",this._params=void 0,(0,l.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return n.Ld;const e=this._params.entry,i=!this._isNameValid(),t=!e;return(0,n.dy)(v||(v=g`
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

            <ha-icon-picker
              .hass=${0}
              .value=${0}
              @value-changed=${0}
              .label=${0}
            ></ha-icon-picker>

            <ha-floor-picker
              .hass=${0}
              .value=${0}
              @value-changed=${0}
              .label=${0}
            ></ha-floor-picker>

            <ha-labels-picker
              .hass=${0}
              .value=${0}
              @value-changed=${0}
            ></ha-labels-picker>

            <ha-picture-upload
              .hass=${0}
              .value=${0}
              crop
              select-media
              .cropOptions=${0}
              @change=${0}
            ></ha-picture-upload>

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

            ${0}
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
    `),this.closeDialog,(0,o.i)(this.hass,e?this.hass.localize("ui.panel.config.areas.editor.update_area"):this.hass.localize("ui.panel.config.areas.editor.create_area")),this._error?(0,n.dy)(m||(m=g`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):"",e?(0,n.dy)(f||(f=g`
                  <ha-settings-row>
                    <span slot="heading">
                      ${0}
                    </span>
                    <span slot="description"> ${0} </span>
                  </ha-settings-row>
                `),this.hass.localize("ui.panel.config.areas.editor.area_id"),e.area_id):n.Ld,this._name,this._nameChanged,this.hass.localize("ui.panel.config.areas.editor.name"),this.hass.localize("ui.panel.config.areas.editor.name_required"),this.hass,this._icon,this._iconChanged,this.hass.localize("ui.panel.config.areas.editor.icon"),this.hass,this._floor,this._floorChanged,this.hass.localize("ui.panel.config.areas.editor.floor"),this.hass,this._labels,this._labelsChanged,this.hass,this._picture,C,this._pictureChanged,this.hass.localize("ui.panel.config.areas.editor.aliases_section"),this.hass.localize("ui.panel.config.areas.editor.aliases_description"),this.hass,this._aliases,this._aliasesChanged,t?"":(0,n.dy)(k||(k=g`
                  <ha-entity-picker
                    .hass=${0}
                    .label=${0}
                    .helper=${0}
                    .value=${0}
                    .includeDomains=${0}
                    .includeDeviceClasses=${0}
                    .entityFilter=${0}
                    @value-changed=${0}
                  ></ha-entity-picker>

                  <ha-entity-picker
                    .hass=${0}
                    .label=${0}
                    .helper=${0}
                    .value=${0}
                    .includeDomains=${0}
                    .includeDeviceClasses=${0}
                    .entityFilter=${0}
                    @value-changed=${0}
                  ></ha-entity-picker>
                `),this.hass,this.hass.localize("ui.panel.config.areas.editor.temperature_entity"),this.hass.localize("ui.panel.config.areas.editor.temperature_entity_description"),this._temperatureEntity,b,w,this._areaEntityFilter,this._sensorChanged,this.hass,this.hass.localize("ui.panel.config.areas.editor.humidity_entity"),this.hass.localize("ui.panel.config.areas.editor.humidity_entity_description"),this._humidityEntity,b,z,this._areaEntityFilter,this._sensorChanged),this.closeDialog,this.hass.localize("ui.common.cancel"),this._updateEntry,i||this._submitting,e?this.hass.localize("ui.common.save"):this.hass.localize("ui.common.create"))}},{kind:"method",key:"_isNameValid",value:function(){return""!==this._name.trim()}},{kind:"field",key:"_areaEntityFilter",value(){return e=>{const i=this.hass.entities[e.entity_id];if(!i)return!1;const t=this._params.entry.area_id;if(i.area_id===t)return!0;if(!i.device_id)return!1;const a=this.hass.devices[i.device_id];return a&&a.area_id===t}}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._name=e.target.value}},{kind:"method",key:"_floorChanged",value:function(e){this._error=void 0,this._floor=e.detail.value}},{kind:"method",key:"_iconChanged",value:function(e){this._error=void 0,this._icon=e.detail.value}},{kind:"method",key:"_labelsChanged",value:function(e){this._error=void 0,this._labels=e.detail.value}},{kind:"method",key:"_pictureChanged",value:function(e){this._error=void 0,this._picture=e.target.value}},{kind:"method",key:"_aliasesChanged",value:function(e){this._aliases=e.detail.value}},{kind:"method",key:"_sensorChanged",value:function(e){this[`_${e.target.includeDeviceClasses[0]}Entity`]=e.detail.value||null}},{kind:"method",key:"_updateEntry",value:async function(){const e=!this._params.entry;this._submitting=!0;try{const i={name:this._name.trim(),picture:this._picture||(e?void 0:null),icon:this._icon||(e?void 0:null),floor_id:this._floor||(e?void 0:null),labels:this._labels||null,aliases:this._aliases,temperature_entity_id:this._temperatureEntity,humidity_entity_id:this._humidityEntity};e?await this._params.createEntry(i):await this._params.updateEntry(i),this.closeDialog()}catch(i){this._error=i.message||this.hass.localize("ui.panel.config.areas.editor.unknown_error")}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[_.yu,(0,n.iv)($||($=g`
        ha-aliases-editor,
        ha-entity-picker,
        ha-floor-picker,
        ha-icon-picker,
        ha-labels-picker,
        ha-picture-upload {
          display: block;
          margin-bottom: 16px;
        }
      `))]}}]}}),n.oi);customElements.define("dialog-area-registry-detail",E),a()}catch(v){a(v)}}))},31050:function(e,i,t){t.d(i,{C:()=>u});t(71695),t(40251),t(39527),t(67670),t(47021);var a=t(57708),s=t(53232),n=t(1714);t(63721),t(88230),t(52247);class r{constructor(e){this.G=e}disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}}class l{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var e;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((e=>this.Z=e)))}resume(){var e;null===(e=this.Z)||void 0===e||e.call(this),this.Y=this.Z=void 0}}var o=t(45779);const h=e=>!(0,s.pt)(e)&&"function"==typeof e.then,d=1073741823;class c extends n.sR{constructor(){super(...arguments),this._$C_t=d,this._$Cwt=[],this._$Cq=new r(this),this._$CK=new l}render(...e){var i;return null!==(i=e.find((e=>!h(e))))&&void 0!==i?i:a.Jb}update(e,i){const t=this._$Cwt;let s=t.length;this._$Cwt=i;const n=this._$Cq,r=this._$CK;this.isConnected||this.disconnected();for(let a=0;a<i.length&&!(a>this._$C_t);a++){const e=i[a];if(!h(e))return this._$C_t=a,e;a<s&&e===t[a]||(this._$C_t=d,s=0,Promise.resolve(e).then((async i=>{for(;r.get();)await r.get();const t=n.deref();if(void 0!==t){const a=t._$Cwt.indexOf(e);a>-1&&a<t._$C_t&&(t._$C_t=a,t.setValue(i))}})))}return a.Jb}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const u=(0,o.XM)(c)}}]);
//# sourceMappingURL=6835.47e04e09e22793c4.js.map