"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8713"],{78393:function(e,i,t){t.r(i),t.d(i,{HaTTSVoiceSelector:()=>u});var a=t(73577),s=(t(71695),t(47021),t(57243)),d=t(50778);t(27556);let l,o,n=e=>e,u=(0,a.Z)([(0,d.Mo)("ha-selector-tts_voice")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,i,t,a;return(0,s.dy)(l||(l=n`<ha-tts-voice-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .language=${0}
      .engineId=${0}
      .disabled=${0}
      .required=${0}
    ></ha-tts-voice-picker>`),this.hass,this.value,this.label,this.helper,(null===(e=this.selector.tts_voice)||void 0===e?void 0:e.language)||(null===(i=this.context)||void 0===i?void 0:i.language),(null===(t=this.selector.tts_voice)||void 0===t?void 0:t.engineId)||(null===(a=this.context)||void 0===a?void 0:a.engineId),this.disabled,this.required)}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(o||(o=n`
    ha-tts-picker {
      width: 100%;
    }
  `))}}]}}),s.oi)},27556:function(e,i,t){var a=t(73577),s=t(72621),d=(t(71695),t(40251),t(39527),t(67670),t(13334),t(47021),t(57243)),l=t(50778),o=t(11297),n=t(81036),u=t(56587),r=t(421);t(74064),t(58130);let v,c,h,k,y=e=>e;const g="__NONE_OPTION__";(0,a.Z)([(0,l.Mo)("ha-tts-voice-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"engineId",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"language",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.SB)()],key:"_voices",value:void 0},{kind:"field",decorators:[(0,l.IO)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"render",value:function(){var e,i;if(!this._voices)return d.Ld;const t=null!==(e=this.value)&&void 0!==e?e:this.required?null===(i=this._voices[0])||void 0===i?void 0:i.voice_id:g;return(0,d.dy)(v||(v=y`
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
    `),this.label||this.hass.localize("ui.components.tts-voice-picker.voice"),t,this.required,this.disabled,this._changed,n.U,this.required?d.Ld:(0,d.dy)(c||(c=y`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),g,this.hass.localize("ui.components.tts-voice-picker.none")),this._voices.map((e=>(0,d.dy)(h||(h=y`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),e.voice_id,e.name))))}},{kind:"method",key:"willUpdate",value:function(e){(0,s.Z)(t,"willUpdate",this,3)([e]),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}},{kind:"field",key:"_debouncedUpdateVoices",value(){return(0,u.D)((()=>this._updateVoices()),500)}},{kind:"method",key:"_updateVoices",value:async function(){this.engineId&&this.language?(this._voices=(await(0,r.MV)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((e=>e.voice_id===this.value))||(this.value=void 0,(0,o.B)(this,"value-changed",{value:this.value})))):this._voices=void 0}},{kind:"method",key:"updated",value:function(e){var i,a,d;((0,s.Z)(t,"updated",this,3)([e]),e.has("_voices")&&(null===(i=this._select)||void 0===i?void 0:i.value)!==this.value)&&(null===(a=this._select)||void 0===a||a.layoutOptions(),(0,o.B)(this,"value-changed",{value:null===(d=this._select)||void 0===d?void 0:d.value}))}},{kind:"field",static:!0,key:"styles",value(){return(0,d.iv)(k||(k=y`
    ha-select {
      width: 100%;
    }
  `))}},{kind:"method",key:"_changed",value:function(e){const i=e.target;!this.hass||""===i.value||i.value===this.value||void 0===this.value&&i.value===g||(this.value=i.value===g?void 0:i.value,(0,o.B)(this,"value-changed",{value:this.value}))}}]}}),d.oi)},421:function(e,i,t){t.d(i,{MV:()=>u,Wg:()=>o,Xk:()=>l,aT:()=>a,b_:()=>d,yP:()=>n});t(88044);const a=(e,i)=>e.callApi("POST","tts_get_url",i),s="media-source://tts/",d=e=>e.startsWith(s),l=e=>e.substring(19),o=(e,i,t)=>e.callWS({type:"tts/engine/list",language:i,country:t}),n=(e,i)=>e.callWS({type:"tts/engine/get",engine_id:i}),u=(e,i,t)=>e.callWS({type:"tts/engine/voices",engine_id:i,language:t})}}]);
//# sourceMappingURL=8713.3b9e2f21cafbcd04.js.map