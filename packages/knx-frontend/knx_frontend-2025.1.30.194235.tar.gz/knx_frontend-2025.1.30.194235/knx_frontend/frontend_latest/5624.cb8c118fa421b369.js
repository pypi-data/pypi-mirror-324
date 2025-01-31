export const ids=["5624"];export const modules={90842:function(e,s,t){t.d(s,{t:()=>o});class a{constructor(e=window.localStorage){this.storage=void 0,this._storage={},this._listeners={},this.storage=e,e===window.localStorage&&window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((s=>s(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const s=this.storage.getItem(e);s&&(this._storage[e]=JSON.parse(s))}}subscribeChanges(e,s){return this._listeners[e]?this._listeners[e].push(s):this._listeners[e]=[s],()=>{this.unsubscribeChanges(e,s)}}unsubscribeChanges(e,s){if(!(e in this._listeners))return;const t=this._listeners[e].indexOf(s);-1!==t&&this._listeners[e].splice(t,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,s){const t=this._storage[e];this._storage[e]=s;try{void 0===s?this.storage.removeItem(e):this.storage.setItem(e,JSON.stringify(s))}catch(a){}finally{this._listeners[e]&&this._listeners[e].forEach((e=>e(t,s)))}}}const i={},o=e=>s=>{const t=e.storage||"localStorage";let o;t&&t in i?o=i[t]:(o=new a(window[t]),i[t]=o);const l=String(s.key),r=e.key||String(s.key),n=s.initializer?s.initializer():void 0;o.addFromStorage(r);const d=!1!==e.subscribe?e=>o.subscribeChanges(r,((t,a)=>{e.requestUpdate(s.key,t)})):void 0,h=()=>o.hasKey(r)?e.deserializer?e.deserializer(o.getValue(r)):o.getValue(r):n;return{kind:"method",placement:"prototype",key:s.key,descriptor:{set(t){((t,a)=>{let i;e.state&&(i=h()),o.setValue(r,e.serializer?e.serializer(a):a),e.state&&t.requestUpdate(s.key,i)})(this,t)},get(){return h()},enumerable:!0,configurable:!0},finisher(t){if(e.state&&e.subscribe){const e=t.prototype.connectedCallback,s=t.prototype.disconnectedCallback;t.prototype.connectedCallback=function(){e.call(this),this[`__unbsubLocalStorage${l}`]=d?.(this)},t.prototype.disconnectedCallback=function(){s.call(this),this[`__unbsubLocalStorage${l}`]?.(),this[`__unbsubLocalStorage${l}`]=void 0}}e.state&&t.createProperty(s.key,{noAccessor:!0,...e.stateOptions})}}}},40137:function(e,s,t){t.r(s),t.d(s,{TTSTryDialog:()=>c});var a=t(44249),i=t(57243),o=t(50778),l=t(90842),r=t(11297),n=(t(20095),t(44118)),d=(t(54993),t(421)),h=t(4557);t(90977);let c=(0,a.Z)([(0,o.Mo)("dialog-tts-try")],(function(e,s){return{F:class extends s{constructor(...s){super(...s),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_loadingExample",value(){return!1}},{kind:"field",decorators:[(0,o.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_valid",value(){return!1}},{kind:"field",decorators:[(0,o.IO)("#message")],key:"_messageInput",value:void 0},{kind:"field",decorators:[(0,l.t)({key:"ttsTryMessages",state:!1,subscribe:!1})],key:"_messages",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._valid=Boolean(this._defaultMessage)}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,r.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"get",key:"_defaultMessage",value:function(){const e=this._params.language?.substring(0,2),s=this.hass.locale.language.substring(0,2);return e&&this._messages?.[e]?this._messages[e]:e===s?this.hass.localize("ui.dialogs.tts-try.message_example"):""}},{kind:"method",key:"render",value:function(){return this._params?i.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${(0,n.i)(this.hass,this.hass.localize("ui.dialogs.tts-try.header"))}
      >
        <ha-textarea
          autogrow
          id="message"
          .label=${this.hass.localize("ui.dialogs.tts-try.message")}
          .placeholder=${this.hass.localize("ui.dialogs.tts-try.message_placeholder")}
          .value=${this._defaultMessage}
          @input=${this._inputChanged}
          ?dialogInitialFocus=${!this._defaultMessage}
        >
        </ha-textarea>
        ${this._loadingExample?i.dy`
              <ha-circular-progress
                size="small"
                indeterminate
                slot="primaryAction"
                class="loading"
              ></ha-circular-progress>
            `:i.dy`
              <ha-button
                ?dialogInitialFocus=${Boolean(this._defaultMessage)}
                slot="primaryAction"
                .label=${this.hass.localize("ui.dialogs.tts-try.play")}
                @click=${this._playExample}
                .disabled=${!this._valid}
              >
                <ha-svg-icon
                  slot="icon"
                  .path=${"M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M10,16.5L16,12L10,7.5V16.5Z"}
                ></ha-svg-icon>
              </ha-button>
            `}
      </ha-dialog>
    `:i.Ld}},{kind:"method",key:"_inputChanged",value:async function(){this._valid=Boolean(this._messageInput?.value)}},{kind:"method",key:"_playExample",value:async function(){const e=this._messageInput?.value;if(!e)return;const s=this._params.engine,t=this._params.language,a=this._params.voice;t&&(this._messages={...this._messages,[t.substring(0,2)]:e}),this._loadingExample=!0;const i=new Audio;let o;i.play();try{o=(await(0,d.aT)(this.hass,{platform:s,message:e,language:t,options:{voice:a}})).path}catch(l){return this._loadingExample=!1,void(0,h.Ys)(this,{text:`Unable to load example. ${l.error||l.body||l}`,warning:!0})}i.src=o,i.addEventListener("canplaythrough",(()=>i.play())),i.addEventListener("playing",(()=>{this._loadingExample=!1})),i.addEventListener("error",(()=>{(0,h.Ys)(this,{title:"Error playing audio."}),this._loadingExample=!1}))}},{kind:"field",static:!0,key:"styles",value(){return i.iv`
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
  `}}]}}),i.oi)}};
//# sourceMappingURL=5624.cb8c118fa421b369.js.map