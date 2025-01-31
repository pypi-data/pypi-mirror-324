export const ids=["8713"];export const modules={78393:function(e,i,t){t.r(i),t.d(i,{HaTTSVoiceSelector:()=>l});var s=t(44249),a=t(57243),d=t(50778);t(27556);let l=(0,s.Z)([(0,d.Mo)("ha-selector-tts_voice")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return a.dy`<ha-tts-voice-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${this.selector.tts_voice?.language||this.context?.language}
      .engineId=${this.selector.tts_voice?.engineId||this.context?.engineId}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-tts-voice-picker>`}},{kind:"field",static:!0,key:"styles",value(){return a.iv`
    ha-tts-picker {
      width: 100%;
    }
  `}}]}}),a.oi)},27556:function(e,i,t){var s=t(44249),a=t(72621),d=t(57243),l=t(50778),o=t(11297),n=t(81036),u=t(56587),r=t(421);t(74064),t(58130);const c="__NONE_OPTION__";(0,s.Z)([(0,l.Mo)("ha-tts-voice-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"engineId",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"language",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.SB)()],key:"_voices",value:void 0},{kind:"field",decorators:[(0,l.IO)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"render",value:function(){if(!this._voices)return d.Ld;const e=this.value??(this.required?this._voices[0]?.voice_id:c);return d.dy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-voice-picker.voice")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${n.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?d.Ld:d.dy`<ha-list-item .value=${c}>
              ${this.hass.localize("ui.components.tts-voice-picker.none")}
            </ha-list-item>`}
        ${this._voices.map((e=>d.dy`<ha-list-item .value=${e.voice_id}>
              ${e.name}
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,a.Z)(t,"willUpdate",this,3)([e]),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}},{kind:"field",key:"_debouncedUpdateVoices",value(){return(0,u.D)((()=>this._updateVoices()),500)}},{kind:"method",key:"_updateVoices",value:async function(){this.engineId&&this.language?(this._voices=(await(0,r.MV)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((e=>e.voice_id===this.value))||(this.value=void 0,(0,o.B)(this,"value-changed",{value:this.value})))):this._voices=void 0}},{kind:"method",key:"updated",value:function(e){(0,a.Z)(t,"updated",this,3)([e]),e.has("_voices")&&this._select?.value!==this.value&&(this._select?.layoutOptions(),(0,o.B)(this,"value-changed",{value:this._select?.value}))}},{kind:"field",static:!0,key:"styles",value(){return d.iv`
    ha-select {
      width: 100%;
    }
  `}},{kind:"method",key:"_changed",value:function(e){const i=e.target;!this.hass||""===i.value||i.value===this.value||void 0===this.value&&i.value===c||(this.value=i.value===c?void 0:i.value,(0,o.B)(this,"value-changed",{value:this.value}))}}]}}),d.oi)},421:function(e,i,t){t.d(i,{MV:()=>u,Wg:()=>o,Xk:()=>l,aT:()=>s,b_:()=>d,yP:()=>n});const s=(e,i)=>e.callApi("POST","tts_get_url",i),a="media-source://tts/",d=e=>e.startsWith(a),l=e=>e.substring(19),o=(e,i,t)=>e.callWS({type:"tts/engine/list",language:i,country:t}),n=(e,i)=>e.callWS({type:"tts/engine/get",engine_id:i}),u=(e,i,t)=>e.callWS({type:"tts/engine/voices",engine_id:i,language:t})}};
//# sourceMappingURL=8713.8445756e52563bb1.js.map