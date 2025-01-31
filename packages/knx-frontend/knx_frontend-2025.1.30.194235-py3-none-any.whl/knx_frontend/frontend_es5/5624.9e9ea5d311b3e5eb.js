"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5624"],{90842:function(e,s,t){t.d(s,{t:()=>l});t(92745),t(77439),t(19423),t(39527),t(41360),t(88972);class a{constructor(e=window.localStorage){this.storage=void 0,this._storage={},this._listeners={},this.storage=e,e===window.localStorage&&window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((s=>s(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const s=this.storage.getItem(e);s&&(this._storage[e]=JSON.parse(s))}}subscribeChanges(e,s){return this._listeners[e]?this._listeners[e].push(s):this._listeners[e]=[s],()=>{this.unsubscribeChanges(e,s)}}unsubscribeChanges(e,s){if(!(e in this._listeners))return;const t=this._listeners[e].indexOf(s);-1!==t&&this._listeners[e].splice(t,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,s){const t=this._storage[e];this._storage[e]=s;try{void 0===s?this.storage.removeItem(e):this.storage.setItem(e,JSON.stringify(s))}catch(a){}finally{this._listeners[e]&&this._listeners[e].forEach((e=>e(t,s)))}}}const i={},l=e=>s=>{const t=e.storage||"localStorage";let l;t&&t in i?l=i[t]:(l=new a(window[t]),i[t]=l);const o=String(s.key),n=e.key||String(s.key),r=s.initializer?s.initializer():void 0;l.addFromStorage(n);const d=!1!==e.subscribe?e=>l.subscribeChanges(n,((t,a)=>{e.requestUpdate(s.key,t)})):void 0,h=()=>l.hasKey(n)?e.deserializer?e.deserializer(l.getValue(n)):l.getValue(n):r;return{kind:"method",placement:"prototype",key:s.key,descriptor:{set(t){((t,a)=>{let i;e.state&&(i=h()),l.setValue(n,e.serializer?e.serializer(a):a),e.state&&t.requestUpdate(s.key,i)})(this,t)},get(){return h()},enumerable:!0,configurable:!0},finisher(t){if(e.state&&e.subscribe){const e=t.prototype.connectedCallback,s=t.prototype.disconnectedCallback;t.prototype.connectedCallback=function(){e.call(this),this[`__unbsubLocalStorage${o}`]=null==d?void 0:d(this)},t.prototype.disconnectedCallback=function(){var e;s.call(this),null===(e=this[`__unbsubLocalStorage${o}`])||void 0===e||e.call(this),this[`__unbsubLocalStorage${o}`]=void 0}}e.state&&t.createProperty(s.key,Object.assign({noAccessor:!0},e.stateOptions))}}}},40137:function(e,s,t){t.r(s),t.d(s,{TTSTryDialog:()=>_});var a=t(73577),i=(t(71695),t(19423),t(40251),t(47021),t(57243)),l=t(50778),o=t(90842),n=t(11297),r=(t(20095),t(44118)),d=(t(54993),t(421)),h=t(4557);t(90977);let c,u,g,p,y=e=>e;let _=(0,a.Z)([(0,l.Mo)("dialog-tts-try")],(function(e,s){return{F:class extends s{constructor(...s){super(...s),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_loadingExample",value(){return!1}},{kind:"field",decorators:[(0,l.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_valid",value(){return!1}},{kind:"field",decorators:[(0,l.IO)("#message")],key:"_messageInput",value:void 0},{kind:"field",decorators:[(0,o.t)({key:"ttsTryMessages",state:!1,subscribe:!1})],key:"_messages",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._valid=Boolean(this._defaultMessage)}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,n.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"get",key:"_defaultMessage",value:function(){var e,s;const t=null===(e=this._params.language)||void 0===e?void 0:e.substring(0,2),a=this.hass.locale.language.substring(0,2);return t&&null!==(s=this._messages)&&void 0!==s&&s[t]?this._messages[t]:t===a?this.hass.localize("ui.dialogs.tts-try.message_example"):""}},{kind:"method",key:"render",value:function(){return this._params?(0,i.dy)(c||(c=y`
      <ha-dialog
        open
        @closed=${0}
        .heading=${0}
      >
        <ha-textarea
          autogrow
          id="message"
          .label=${0}
          .placeholder=${0}
          .value=${0}
          @input=${0}
          ?dialogInitialFocus=${0}
        >
        </ha-textarea>
        ${0}
      </ha-dialog>
    `),this.closeDialog,(0,r.i)(this.hass,this.hass.localize("ui.dialogs.tts-try.header")),this.hass.localize("ui.dialogs.tts-try.message"),this.hass.localize("ui.dialogs.tts-try.message_placeholder"),this._defaultMessage,this._inputChanged,!this._defaultMessage,this._loadingExample?(0,i.dy)(u||(u=y`
              <ha-circular-progress
                size="small"
                indeterminate
                slot="primaryAction"
                class="loading"
              ></ha-circular-progress>
            `)):(0,i.dy)(g||(g=y`
              <ha-button
                ?dialogInitialFocus=${0}
                slot="primaryAction"
                .label=${0}
                @click=${0}
                .disabled=${0}
              >
                <ha-svg-icon
                  slot="icon"
                  .path=${0}
                ></ha-svg-icon>
              </ha-button>
            `),Boolean(this._defaultMessage),this.hass.localize("ui.dialogs.tts-try.play"),this._playExample,!this._valid,"M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M10,16.5L16,12L10,7.5V16.5Z")):i.Ld}},{kind:"method",key:"_inputChanged",value:async function(){var e;this._valid=Boolean(null===(e=this._messageInput)||void 0===e?void 0:e.value)}},{kind:"method",key:"_playExample",value:async function(){var e;const s=null===(e=this._messageInput)||void 0===e?void 0:e.value;if(!s)return;const t=this._params.engine,a=this._params.language,i=this._params.voice;a&&(this._messages=Object.assign(Object.assign({},this._messages),{},{[a.substring(0,2)]:s})),this._loadingExample=!0;const l=new Audio;let o;l.play();try{o=(await(0,d.aT)(this.hass,{platform:t,message:s,language:a,options:{voice:i}})).path}catch(n){return this._loadingExample=!1,void(0,h.Ys)(this,{text:`Unable to load example. ${n.error||n.body||n}`,warning:!0})}l.src=o,l.addEventListener("canplaythrough",(()=>l.play())),l.addEventListener("playing",(()=>{this._loadingExample=!1})),l.addEventListener("error",(()=>{(0,h.Ys)(this,{title:"Error playing audio."}),this._loadingExample=!1}))}},{kind:"field",static:!0,key:"styles",value(){return(0,i.iv)(p||(p=y`
    ha-dialog {
      --mdc-dialog-max-width: 500px;
    }
    ha-textarea,
    ha-select {
      width: 100%;
    }
    ha-select {
      margin-top: 8px;
    }
    .loading {
      height: 36px;
    }
  `))}}]}}),i.oi)}}]);
//# sourceMappingURL=5624.9e9ea5d311b3e5eb.js.map