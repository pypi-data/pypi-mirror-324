"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5010"],{26674:function(e,i,t){t.r(i),t.d(i,{HaSTTSelector:()=>C});var a=t(73577),s=(t(71695),t(47021),t(57243)),n=t(50778),d=t(72621),l=(t(19083),t(40251),t(61006),t(39527),t(67670),t(13334),t(11297)),u=t(81036),r=t(73525),o=t(56587),h=t(52829),v=(t(74064),t(58130),t(79575));let c,g,k,f,p=e=>e;const y="__NONE_OPTION__";(0,a.Z)([(0,n.Mo)("ha-stt-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"language",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.SB)()],key:"_engines",value:void 0},{kind:"method",key:"render",value:function(){if(!this._engines)return s.Ld;let e=this.value;if(!e&&this.required){for(const i of Object.values(this.hass.entities))if("cloud"===i.platform&&"stt"===(0,v.M)(i.entity_id)){e=i.entity_id;break}if(!e)for(const t of this._engines){var i;if(0!==(null==t||null===(i=t.supported_languages)||void 0===i?void 0:i.length)){e=t.engine_id;break}}}return e||(e=y),(0,s.dy)(c||(c=p`
      <ha-select
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        @selected=${0}
        @closed=${0}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${0}
        ${0}
      </ha-select>
    `),this.label||this.hass.localize("ui.components.stt-picker.stt"),e,this.required,this.disabled,this._changed,u.U,this.required?s.Ld:(0,s.dy)(g||(g=p`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),y,this.hass.localize("ui.components.stt-picker.none")),this._engines.map((i=>{var t;if(i.deprecated&&i.engine_id!==e)return s.Ld;let a;if(i.engine_id.includes(".")){const e=this.hass.states[i.engine_id];a=e?(0,r.C)(e):i.engine_id}else a=i.name||i.engine_id;return(0,s.dy)(k||(k=p`<ha-list-item
            .value=${0}
            .disabled=${0}
          >
            ${0}
          </ha-list-item>`),i.engine_id,0===(null===(t=i.supported_languages)||void 0===t?void 0:t.length),a)})))}},{kind:"method",key:"willUpdate",value:function(e){(0,d.Z)(t,"willUpdate",this,3)([e]),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}},{kind:"field",key:"_debouncedUpdateEngines",value(){return(0,o.D)((()=>this._updateEngines()),500)}},{kind:"method",key:"_updateEngines",value:async function(){var e;if(this._engines=(await(0,h.m)(this.hass,this.language,this.hass.config.country||void 0)).providers,!this.value)return;const i=this._engines.find((e=>e.engine_id===this.value));(0,l.B)(this,"supported-languages-changed",{value:null==i?void 0:i.supported_languages}),i&&0!==(null===(e=i.supported_languages)||void 0===e?void 0:e.length)||(this.value=void 0,(0,l.B)(this,"value-changed",{value:this.value}))}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(f||(f=p`
    ha-select {
      width: 100%;
    }
  `))}},{kind:"method",key:"_changed",value:function(e){var i;const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===y||(this.value=t.value===y?void 0:t.value,(0,l.B)(this,"value-changed",{value:this.value}),(0,l.B)(this,"supported-languages-changed",{value:null===(i=this._engines.find((e=>e.engine_id===this.value)))||void 0===i?void 0:i.supported_languages}))}}]}}),s.oi);let b,_,$=e=>e,C=(0,a.Z)([(0,n.Mo)("ha-selector-stt")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,i;return(0,s.dy)(b||(b=$`<ha-stt-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .language=${0}
      .disabled=${0}
      .required=${0}
    ></ha-stt-picker>`),this.hass,this.value,this.label,this.helper,(null===(e=this.selector.stt)||void 0===e?void 0:e.language)||(null===(i=this.context)||void 0===i?void 0:i.language),this.disabled,this.required)}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(_||(_=$`
    ha-stt-picker {
      width: 100%;
    }
  `))}}]}}),s.oi)},52829:function(e,i,t){t.d(i,{m:()=>a});const a=(e,i,t)=>e.callWS({type:"stt/engine/list",language:i,country:t})}}]);
//# sourceMappingURL=5010.165c202e40c1268a.js.map