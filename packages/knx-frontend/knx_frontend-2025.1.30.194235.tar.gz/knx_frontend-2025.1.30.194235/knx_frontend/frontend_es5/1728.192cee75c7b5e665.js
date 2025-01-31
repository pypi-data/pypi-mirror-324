"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1728"],{19082:function(e,i,t){t.r(i),t.d(i,{HaTTSSelector:()=>C});var s=t(73577),a=(t(71695),t(47021),t(57243)),n=t(50778),d=t(72621),l=(t(19083),t(40251),t(61006),t(39527),t(67670),t(13334),t(11297)),u=t(81036),r=t(73525),o=t(56587),h=t(421),v=(t(74064),t(58130),t(79575));let c,g,k,p,f=e=>e;const y="__NONE_OPTION__";(0,s.Z)([(0,n.Mo)("ha-tts-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"language",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.SB)()],key:"_engines",value:void 0},{kind:"method",key:"render",value:function(){if(!this._engines)return a.Ld;let e=this.value;if(!e&&this.required){for(const i of Object.values(this.hass.entities))if("cloud"===i.platform&&"tts"===(0,v.M)(i.entity_id)){e=i.entity_id;break}if(!e)for(const t of this._engines){var i;if(0!==(null==t||null===(i=t.supported_languages)||void 0===i?void 0:i.length)){e=t.engine_id;break}}}return e||(e=y),(0,a.dy)(c||(c=f`
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
    `),this.label||this.hass.localize("ui.components.tts-picker.tts"),e,this.required,this.disabled,this._changed,u.U,this.required?a.Ld:(0,a.dy)(g||(g=f`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),y,this.hass.localize("ui.components.tts-picker.none")),this._engines.map((i=>{var t;if(i.deprecated&&i.engine_id!==e)return a.Ld;let s;if(i.engine_id.includes(".")){const e=this.hass.states[i.engine_id];s=e?(0,r.C)(e):i.engine_id}else s=i.name||i.engine_id;return(0,a.dy)(k||(k=f`<ha-list-item
            .value=${0}
            .disabled=${0}
          >
            ${0}
          </ha-list-item>`),i.engine_id,0===(null===(t=i.supported_languages)||void 0===t?void 0:t.length),s)})))}},{kind:"method",key:"willUpdate",value:function(e){(0,d.Z)(t,"willUpdate",this,3)([e]),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}},{kind:"field",key:"_debouncedUpdateEngines",value(){return(0,o.D)((()=>this._updateEngines()),500)}},{kind:"method",key:"_updateEngines",value:async function(){var e;if(this._engines=(await(0,h.Wg)(this.hass,this.language,this.hass.config.country||void 0)).providers,!this.value)return;const i=this._engines.find((e=>e.engine_id===this.value));(0,l.B)(this,"supported-languages-changed",{value:null==i?void 0:i.supported_languages}),i&&0!==(null===(e=i.supported_languages)||void 0===e?void 0:e.length)||(this.value=void 0,(0,l.B)(this,"value-changed",{value:this.value}))}},{kind:"field",static:!0,key:"styles",value(){return(0,a.iv)(p||(p=f`
    ha-select {
      width: 100%;
    }
  `))}},{kind:"method",key:"_changed",value:function(e){var i;const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===y||(this.value=t.value===y?void 0:t.value,(0,l.B)(this,"value-changed",{value:this.value}),(0,l.B)(this,"supported-languages-changed",{value:null===(i=this._engines.find((e=>e.engine_id===this.value)))||void 0===i?void 0:i.supported_languages}))}}]}}),a.oi);let _,b,$=e=>e,C=(0,s.Z)([(0,n.Mo)("ha-selector-tts")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,i;return(0,a.dy)(_||(_=$`<ha-tts-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .language=${0}
      .disabled=${0}
      .required=${0}
    ></ha-tts-picker>`),this.hass,this.value,this.label,this.helper,(null===(e=this.selector.tts)||void 0===e?void 0:e.language)||(null===(i=this.context)||void 0===i?void 0:i.language),this.disabled,this.required)}},{kind:"field",static:!0,key:"styles",value(){return(0,a.iv)(b||(b=$`
    ha-tts-picker {
      width: 100%;
    }
  `))}}]}}),a.oi)},421:function(e,i,t){t.d(i,{MV:()=>r,Wg:()=>l,Xk:()=>d,aT:()=>s,b_:()=>n,yP:()=>u});t(88044);const s=(e,i)=>e.callApi("POST","tts_get_url",i),a="media-source://tts/",n=e=>e.startsWith(a),d=e=>e.substring(19),l=(e,i,t)=>e.callWS({type:"tts/engine/list",language:i,country:t}),u=(e,i)=>e.callWS({type:"tts/engine/get",engine_id:i}),r=(e,i,t)=>e.callWS({type:"tts/engine/voices",engine_id:i,language:t})}}]);
//# sourceMappingURL=1728.192cee75c7b5e665.js.map