"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["9329"],{68024:function(e,i,t){var a=t(73577),s=(t(71695),t(40251),t(47021),t(57243)),n=t(50778),o=t(27486);t(42877);let d,l,r=e=>e;(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-config")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1,type:Array})],key:"supportedLanguages",value:void 0},{kind:"method",key:"focus",value:async function(){var e;await this.updateComplete;const i=null===(e=this.renderRoot)||void 0===e?void 0:e.querySelector("ha-form");null==i||i.focus()}},{kind:"field",key:"_schema",value(){return(0,o.Z)((e=>[{name:"",type:"grid",schema:[{name:"name",required:!0,selector:{text:{}}},e?{name:"language",required:!0,selector:{language:{languages:e}}}:{name:"",type:"constant"}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){return(0,s.dy)(d||(d=r`
      <div class="section">
        <div class="intro">
          <h3>
            ${0}
          </h3>
          <p>
            ${0}
          </p>
        </div>
        <ha-form
          .schema=${0}
          .data=${0}
          .hass=${0}
          .computeLabel=${0}
        ></ha-form>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.description"),this._schema(this.supportedLanguages),this.data,this.hass,this._computeLabel)}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(l||(l=r`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      box-sizing: border-box;
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-weight: normal;
      font-size: 22px;
      line-height: 28px;
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      margin-top: 0;
      margin-bottom: 0;
    }
  `))}}]}}),s.oi)},54859:function(e,i,t){var a=t(73577),s=(t(71695),t(92745),t(19423),t(47021),t(57243)),n=t(50778),o=t(27486),d=(t(42877),t(11297));let l,r,p=e=>e;(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-conversation")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value(){return(0,o.Z)(((e,i,t)=>{const a=[{name:"",type:"grid",schema:[{name:"conversation_engine",required:!0,selector:{conversation_agent:{language:i}}}]}];return"*"!==t&&null!=t&&t.length&&a[0].schema.push({name:"conversation_language",required:!0,selector:{language:{languages:t,no_sort:!0}}}),"conversation.home_assistant"!==e&&a.push({name:"prefer_local_intents",default:!0,selector:{boolean:{}}}),a}))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"field",key:"_computeHelper",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}_description`):""}},{kind:"method",key:"render",value:function(){var e,i;return(0,s.dy)(l||(l=p`
      <div class="section">
        <div class="intro">
          <h3>
            ${0}
          </h3>
          <p>
            ${0}
          </p>
        </div>
        <ha-form
          .schema=${0}
          .data=${0}
          .hass=${0}
          .computeLabel=${0}
          .computeHelper=${0}
          @supported-languages-changed=${0}
        ></ha-form>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.description"),this._schema(null===(e=this.data)||void 0===e?void 0:e.conversation_engine,null===(i=this.data)||void 0===i?void 0:i.language,this._supportedLanguages),this.data,this.hass,this._computeLabel,this._computeHelper,this._supportedLanguagesChanged)}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){"*"===e.detail.value&&setTimeout((()=>{const e=Object.assign({},this.data);e.conversation_language="*",(0,d.B)(this,"value-changed",{value:e})}),0),this._supportedLanguages=e.detail.value}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(r||(r=p`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      box-sizing: border-box;
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-weight: normal;
      font-size: 22px;
      line-height: 28px;
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      margin-top: 0;
      margin-bottom: 0;
    }
  `))}}]}}),s.oi)},46343:function(e,i,t){var a=t(73577),s=(t(71695),t(47021),t(57243)),n=t(50778),o=t(27486);t(42877);let d,l,r=e=>e;(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-stt")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value(){return(0,o.Z)(((e,i)=>[{name:"",type:"grid",schema:[{name:"stt_engine",selector:{stt:{language:e}}},null!=i&&i.length?{name:"stt_language",required:!0,selector:{language:{languages:i,no_sort:!0}}}:{name:"",type:"constant"}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){var e;return(0,s.dy)(d||(d=r`
      <div class="section">
        <div class="intro">
          <h3>
            ${0}
          </h3>
          <p>
            ${0}
          </p>
        </div>
        <ha-form
          .schema=${0}
          .data=${0}
          .hass=${0}
          .computeLabel=${0}
          @supported-languages-changed=${0}
        ></ha-form>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.description"),this._schema(null===(e=this.data)||void 0===e?void 0:e.language,this._supportedLanguages),this.data,this.hass,this._computeLabel,this._supportedLanguagesChanged)}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){this._supportedLanguages=e.detail.value}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(l||(l=r`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      box-sizing: border-box;
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-weight: normal;
      font-size: 22px;
      line-height: 28px;
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      margin-top: 0;
      margin-bottom: 0;
    }
  `))}}]}}),s.oi)},52511:function(e,i,t){var a=t(73577),s=(t(71695),t(40251),t(47021),t(57243)),n=t(50778),o=t(27486),d=(t(20095),t(42877),t(11297));const l=()=>t.e("5624").then(t.bind(t,40137));let r,p,u,c=e=>e;(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-tts")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value(){return(0,o.Z)(((e,i)=>[{name:"",type:"grid",schema:[{name:"tts_engine",selector:{tts:{language:e}}},null!=i&&i.length?{name:"tts_language",required:!0,selector:{language:{languages:i,no_sort:!0}}}:{name:"",type:"constant"},{name:"tts_voice",selector:{tts_voice:{}},context:{language:"tts_language",engineId:"tts_engine"},required:!0}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){var e,i;return(0,s.dy)(r||(r=c`
      <div class="section">
        <div class="content">
          <div class="intro">
          <h3>
            ${0}
          </h3>
          <p>
            ${0}
          </p>
          </div>
          <ha-form
            .schema=${0}
            .data=${0}
            .hass=${0}
            .computeLabel=${0}
            @supported-languages-changed=${0}
          ></ha-form>
        </div>

       ${0}
        </div>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.description"),this._schema(null===(e=this.data)||void 0===e?void 0:e.language,this._supportedLanguages),this.data,this.hass,this._computeLabel,this._supportedLanguagesChanged,null!==(i=this.data)&&void 0!==i&&i.tts_engine?(0,s.dy)(p||(p=c`<div class="footer">
               <ha-button
                 .label=${0}
                 @click=${0}
               >
               </ha-button>
             </div>`),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.try_tts"),this._preview):s.Ld)}},{kind:"method",key:"_preview",value:async function(){if(!this.data)return;const e=this.data.tts_engine,i=this.data.tts_language||void 0,t=this.data.tts_voice||void 0;var a,s;e&&(a=this,s={engine:e,language:i,voice:t},(0,d.B)(a,"show-dialog",{addHistory:!1,dialogTag:"dialog-tts-try",dialogImport:l,dialogParams:s}))}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){this._supportedLanguages=e.detail.value}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(u||(u=c`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
    }
    .content {
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-weight: normal;
      font-size: 22px;
      line-height: 28px;
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      margin-top: 0;
      margin-bottom: 0;
    }
    .footer {
      border-top: 1px solid var(--divider-color);
      padding: 8px 16px;
    }
  `))}}]}}),s.oi)},37744:function(e,i,t){var a=t(73577),s=(t(71695),t(19423),t(40251),t(39527),t(13334),t(36993),t(47021),t(57243)),n=t(50778),o=t(27486);t(42877);var d=t(11297);let l,r,p=e=>e;(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-wakeword")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_wakeWords",value:void 0},{kind:"field",key:"_schema",value(){return(0,o.Z)((e=>[{name:"",type:"grid",schema:[{name:"wake_word_entity",selector:{entity:{domain:"wake_word"}}},null!=e&&e.length?{name:"wake_word_id",required:!0,selector:{select:{mode:"dropdown",sort:!0,options:e.map((e=>({value:e.id,label:e.name})))}}}:{name:"",type:"constant"}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"willUpdate",value:function(e){var i,t,a,s;e.has("data")&&(null===(i=e.get("data"))||void 0===i?void 0:i.wake_word_entity)!==(null===(t=this.data)||void 0===t?void 0:t.wake_word_entity)&&(null!==(a=e.get("data"))&&void 0!==a&&a.wake_word_entity&&null!==(s=this.data)&&void 0!==s&&s.wake_word_id&&(0,d.B)(this,"value-changed",{value:Object.assign(Object.assign({},this.data),{},{wake_word_id:void 0})}),this._fetchWakeWords())}},{kind:"method",key:"render",value:function(){return(0,s.dy)(l||(l=p`
      <div class="section">
        <div class="content">
          <div class="intro">
            <h3>
              ${0}
            </h3>
            <p>
              ${0}
            </p>
            <ha-alert alert-type="info">
              ${0}
            </ha-alert>
          </div>
          <ha-form
            .schema=${0}
            .data=${0}
            .hass=${0}
            .computeLabel=${0}
          ></ha-form>
        </div>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.description"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.note"),this._schema(this._wakeWords),this.data,this.hass,this._computeLabel)}},{kind:"method",key:"_fetchWakeWords",value:async function(){var e,i;if(this._wakeWords=void 0,null===(e=this.data)||void 0===e||!e.wake_word_entity)return;const t=this.data.wake_word_entity,a=await(s=this.hass,n=t,s.callWS({type:"wake_word/info",entity_id:n}));var s,n,o;this.data.wake_word_entity===t&&(this._wakeWords=a.wake_words,!this.data||null!==(i=this.data)&&void 0!==i&&i.wake_word_id&&this._wakeWords.some((e=>e.id===this.data.wake_word_id))||(0,d.B)(this,"value-changed",{value:Object.assign(Object.assign({},this.data),{},{wake_word_id:null===(o=this._wakeWords[0])||void 0===o?void 0:o.id})}))}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(r||(r=p`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
    }
    .content {
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-weight: normal;
      font-size: 22px;
      line-height: 28px;
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      margin-top: 0;
      margin-bottom: 0;
    }
    a {
      color: var(--primary-color);
    }
  `))}}]}}),s.oi)},22380:function(e,i,t){t.a(e,(async function(e,i){try{var a=t(73577),s=(t(71695),t(77439),t(39527),t(41360),t(47021),t(57243)),n=t(50778),o=t(27486),d=t(4855),l=t(35047),r=e([l]);l=(r.then?(await r)():r)[0];let p,u,c,h=e=>e;(0,a.Z)([(0,n.Mo)("assist-render-pipeline-events")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"events",value:void 0},{kind:"field",key:"_processEvents",value(){return(0,o.Z)((e=>{let i;return e.forEach((e=>{i=(0,d.eP)(i,e)})),i}))}},{kind:"method",key:"render",value:function(){const e=this._processEvents(this.events);return e?(0,s.dy)(c||(c=h`
      <assist-render-pipeline-run
        .hass=${0}
        .pipelineRun=${0}
      ></assist-render-pipeline-run>
    `),this.hass,e):this.events.length?(0,s.dy)(p||(p=h`<ha-alert alert-type="error">Error showing run</ha-alert>
          <ha-card>
            <ha-expansion-panel>
              <span slot="header">Raw</span>
              <pre>${0}</pre>
            </ha-expansion-panel>
          </ha-card>`),JSON.stringify(this.events,null,2)):(0,s.dy)(u||(u=h`<ha-alert alert-type="warning"
        >There were no events in this run.</ha-alert
      >`))}}]}}),s.oi);i()}catch(p){i(p)}}))},35047:function(e,i,t){t.a(e,(async function(e,i){try{var a=t(73577),s=(t(71695),t(92745),t(39527),t(67670),t(13334),t(47021),t(57243)),n=t(50778),o=(t(1192),t(17949),t(20095),t(90977),t(2383),t(52745)),d=(t(27196),t(4557)),l=e([o]);o=(l.then?(await l)():l)[0];let r,p,u,c,h,v,g,_,m,k,y,f,w,b,$,x,L,R,z,W,C,A,S,E=e=>e;const B={pipeline:"Pipeline",language:"Language"},Z={engine:"Engine"},M={engine:"Engine"},O={engine:"Engine",language:"Language",intent_input:"Input"},P={engine:"Engine",language:"Language",voice:"Voice",tts_input:"Input"},T={ready:0,wake_word:1,stt:2,intent:3,tts:4,done:5,error:6},j=(e,i)=>e.init_options?T[e.init_options.start_stage]<=T[i]&&T[i]<=T[e.init_options.end_stage]:i in e,D=(e,i,t)=>"error"in e&&t===i?(0,s.dy)(r||(r=E`
    <ha-alert alert-type="error">
      ${0} (${0})
    </ha-alert>
  `),e.error.message,e.error.code):"",F=(e,i,t,a="-start")=>{const n=i.events.find((e=>e.type===`${t}`+a)),d=i.events.find((e=>e.type===`${t}-end`));if(!n)return"";if(!d)return"error"in i?(0,s.dy)(p||(p=E`❌`)):(0,s.dy)(u||(u=E`
      <ha-circular-progress size="small" indeterminate></ha-circular-progress>
    `));const l=new Date(d.timestamp).getTime()-new Date(n.timestamp).getTime(),r=(0,o.uf)(l/1e3,e.locale,{maximumFractionDigits:2});return(0,s.dy)(c||(c=E`${0}s ✅`),r)},q=(e,i)=>Object.entries(i).map((([i,t])=>(0,s.dy)(h||(h=E`
      <div class="row">
        <div>${0}</div>
        <div>${0}</div>
      </div>
    `),t,e[i]))),I=(e,i)=>{const t={};let a=!1;for(const s in e)s in i||"done"===s||(a=!0,t[s]=e[s]);return a?(0,s.dy)(v||(v=E`<ha-expansion-panel>
        <span slot="header">Raw</span>
        <ha-yaml-editor readOnly autoUpdate .value=${0}></ha-yaml-editor>
      </ha-expansion-panel>`),t):""};(0,a.Z)([(0,n.Mo)("assist-render-pipeline-run")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"pipelineRun",value:void 0},{kind:"method",key:"render",value:function(){var e,i,t,a;const n=this.pipelineRun&&["tts","intent","stt","wake_word"].find((e=>e in this.pipelineRun))||"ready",o=[],d=(this.pipelineRun.init_options&&"text"in this.pipelineRun.init_options.input?this.pipelineRun.init_options.input.text:void 0)||(null===(e=this.pipelineRun)||void 0===e||null===(e=e.stt)||void 0===e||null===(e=e.stt_output)||void 0===e?void 0:e.text)||(null===(i=this.pipelineRun)||void 0===i||null===(i=i.intent)||void 0===i?void 0:i.intent_input);return d&&o.push({from:"user",text:d}),null!==(t=this.pipelineRun)&&void 0!==t&&null!==(t=t.intent)&&void 0!==t&&null!==(t=t.intent_output)&&void 0!==t&&null!==(t=t.response)&&void 0!==t&&null!==(t=t.speech)&&void 0!==t&&null!==(t=t.plain)&&void 0!==t&&t.speech&&o.push({from:"hass",text:this.pipelineRun.intent.intent_output.response.speech.plain.speech}),(0,s.dy)(g||(g=E`
      <ha-card>
        <div class="card-content">
          <div class="row heading">
            <div>Run</div>
            <div>${0}</div>
          </div>

          ${0}
          ${0}
        </div>
      </ha-card>

      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      <ha-card>
        <ha-expansion-panel>
          <span slot="header">Raw</span>
          <ha-yaml-editor
            read-only
            auto-update
            .value=${0}
          ></ha-yaml-editor>
        </ha-expansion-panel>
      </ha-card>
    `),this.pipelineRun.stage,q(this.pipelineRun.run,B),o.length>0?(0,s.dy)(_||(_=E`
                <div class="messages">
                  ${0}
                </div>
                <div style="clear:both"></div>
              `),o.map((({from:e,text:i})=>(0,s.dy)(m||(m=E`
                      <div class=${0}>${0}</div>
                    `),`message ${e}`,i)))):"",D(this.pipelineRun,"ready",n),j(this.pipelineRun,"wake_word")?(0,s.dy)(k||(k=E`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Wake word</span>
                  ${0}
                </div>
                ${0}
              </div>
            </ha-card>
          `),F(this.hass,this.pipelineRun,"wake_word"),this.pipelineRun.wake_word?(0,s.dy)(y||(y=E`
                      <div class="card-content">
                        ${0}
                        ${0}
                        ${0}
                      </div>
                    `),q(this.pipelineRun.wake_word,M),this.pipelineRun.wake_word.wake_word_output?(0,s.dy)(f||(f=E`<div class="row">
                                <div>Model</div>
                                <div>
                                  ${0}
                                </div>
                              </div>
                              <div class="row">
                                <div>Timestamp</div>
                                <div>
                                  ${0}
                                </div>
                              </div>`),this.pipelineRun.wake_word.wake_word_output.ww_id,this.pipelineRun.wake_word.wake_word_output.timestamp):"",I(this.pipelineRun.wake_word,Z)):""):"",D(this.pipelineRun,"wake_word",n),j(this.pipelineRun,"stt")?(0,s.dy)(w||(w=E`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Speech-to-text</span>
                  ${0}
                </div>
                ${0}
              </div>
            </ha-card>
          `),F(this.hass,this.pipelineRun,"stt","-vad-end"),this.pipelineRun.stt?(0,s.dy)(b||(b=E`
                      <div class="card-content">
                        ${0}
                        <div class="row">
                          <div>Language</div>
                          <div>${0}</div>
                        </div>
                        ${0}
                        ${0}
                      </div>
                    `),q(this.pipelineRun.stt,M),this.pipelineRun.stt.metadata.language,this.pipelineRun.stt.stt_output?(0,s.dy)($||($=E`<div class="row">
                              <div>Output</div>
                              <div>${0}</div>
                            </div>`),this.pipelineRun.stt.stt_output.text):"",I(this.pipelineRun.stt,M)):""):"",D(this.pipelineRun,"stt",n),j(this.pipelineRun,"intent")?(0,s.dy)(x||(x=E`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Natural Language Processing</span>
                  ${0}
                </div>
                ${0}
              </div>
            </ha-card>
          `),F(this.hass,this.pipelineRun,"intent"),this.pipelineRun.intent?(0,s.dy)(L||(L=E`
                      <div class="card-content">
                        ${0}
                        ${0}
                        <div class="row">
                          <div>Prefer handling locally</div>
                          <div>
                            ${0}
                          </div>
                        </div>
                        <div class="row">
                          <div>Processed locally</div>
                          <div>
                            ${0}
                          </div>
                        </div>
                        ${0}
                      </div>
                    `),q(this.pipelineRun.intent,O),this.pipelineRun.intent.intent_output?(0,s.dy)(R||(R=E`<div class="row">
                                <div>Response type</div>
                                <div>
                                  ${0}
                                </div>
                              </div>
                              ${0}`),this.pipelineRun.intent.intent_output.response.response_type,"error"===this.pipelineRun.intent.intent_output.response.response_type?(0,s.dy)(z||(z=E`<div class="row">
                                    <div>Error code</div>
                                    <div>
                                      ${0}
                                    </div>
                                  </div>`),this.pipelineRun.intent.intent_output.response.data.code):""):"",this.pipelineRun.intent.prefer_local_intents,this.pipelineRun.intent.processed_locally,I(this.pipelineRun.intent,O)):""):"",D(this.pipelineRun,"intent",n),j(this.pipelineRun,"tts")?(0,s.dy)(W||(W=E`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Text-to-speech</span>
                  ${0}
                </div>
                ${0}
              </div>
              ${0}
            </ha-card>
          `),F(this.hass,this.pipelineRun,"tts"),this.pipelineRun.tts?(0,s.dy)(C||(C=E`
                      <div class="card-content">
                        ${0}
                        ${0}
                      </div>
                    `),q(this.pipelineRun.tts,P),I(this.pipelineRun.tts,P)):"",null!==(a=this.pipelineRun)&&void 0!==a&&null!==(a=a.tts)&&void 0!==a&&a.tts_output?(0,s.dy)(A||(A=E`
                    <div class="card-actions">
                      <ha-button @click=${0}>
                        Play Audio
                      </ha-button>
                    </div>
                  `),this._playTTS):""):"",D(this.pipelineRun,"tts",n),this.pipelineRun)}},{kind:"method",key:"_playTTS",value:function(){const e=this.pipelineRun.tts.tts_output.url,i=new Audio(e);i.addEventListener("error",(()=>{(0,d.Ys)(this,{title:"Error",text:"Error playing audio"})})),i.addEventListener("canplaythrough",(()=>{i.play()}))}},{kind:"field",static:!0,key:"styles",value(){return(0,s.iv)(S||(S=E`
    :host {
      display: block;
    }
    ha-card,
    ha-alert {
      display: block;
      margin-bottom: 16px;
    }
    .row {
      display: flex;
      justify-content: space-between;
    }
    .row > div:last-child {
      text-align: right;
    }
    ha-expansion-panel {
      padding-left: 8px;
      padding-inline-start: 8px;
      padding-inline-end: initial;
    }
    .card-content ha-expansion-panel {
      padding-left: 0px;
      padding-inline-start: 0px;
      padding-inline-end: initial;
      --expansion-panel-summary-padding: 0px;
      --expansion-panel-content-padding: 0px;
    }
    .heading {
      font-weight: 500;
      margin-bottom: 16px;
    }

    .messages {
      margin-top: 8px;
    }

    .message {
      font-size: 18px;
      margin: 8px 0;
      padding: 8px;
      border-radius: 15px;
      clear: both;
    }

    .message.user {
      margin-left: 24px;
      margin-inline-start: 24px;
      margin-inline-end: initial;
      float: var(--float-end);
      text-align: right;
      border-bottom-right-radius: 0px;
      background-color: var(--light-primary-color);
      color: var(--text-light-primary-color, var(--primary-text-color));
      direction: var(--direction);
    }

    .message.hass {
      margin-right: 24px;
      margin-inline-end: 24px;
      margin-inline-start: initial;
      float: var(--float-start);
      border-bottom-left-radius: 0px;
      background-color: var(--primary-color);
      color: var(--text-primary-color);
      direction: var(--direction);
    }
  `))}}]}}),s.oi);i()}catch(r){i(r)}}))},26942:function(e,i,t){t.a(e,(async function(e,a){try{t.r(i),t.d(i,{DialogVoiceAssistantPipelineDetail:()=>x});var s=t(73577),n=(t(71695),t(19423),t(40251),t(88044),t(39527),t(41360),t(36993),t(47021),t(57243)),o=t(50778),d=t(27486),l=t(11297),r=(t(20095),t(28906),t(42877),t(4855)),p=t(66193),u=(t(68024),t(54859),t(46343),t(52511),t(37744),t(22380)),c=t(79575),h=t(81036),v=e([u]);u=(v.then?(await v)():v)[0];let g,_,m,k,y,f,w=e=>e;const b="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",$="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z";let x=(0,s.Z)([(0,o.Mo)("dialog-voice-assistant-pipeline-detail")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_data",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_hideWakeWord",value(){return!1}},{kind:"field",decorators:[(0,o.SB)()],key:"_cloudActive",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_submitting",value(){return!1}},{kind:"field",decorators:[(0,o.SB)()],key:"_supportedLanguages",value:void 0},{kind:"method",key:"showDialog",value:function(e){if(this._params=e,this._error=void 0,this._cloudActive=this._params.cloudActiveSubscription,this._params.pipeline)return this._data=Object.assign({prefer_local_intents:!1},this._params.pipeline),void(this._hideWakeWord=this._params.hideWakeWord||!this._data.wake_word_entity);let i,t;if(this._hideWakeWord=!0,this._cloudActive)for(const a of Object.values(this.hass.entities))if("cloud"===a.platform)if("stt"===(0,c.M)(a.entity_id)){if(i=a.entity_id,t)break}else if("tts"===(0,c.M)(a.entity_id)&&(t=a.entity_id,i))break;this._data={language:(this.hass.config.language||this.hass.locale.language).substring(0,2),stt_engine:i,tts_engine:t}}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._data=void 0,this._hideWakeWord=!1,(0,l.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"firstUpdated",value:function(){this._getSupportedLanguages()}},{kind:"method",key:"_getSupportedLanguages",value:async function(){const{languages:e}=await(0,r.Dy)(this.hass);this._supportedLanguages=e}},{kind:"field",key:"_hasWakeWorkEntities",value(){return(0,d.Z)((e=>Object.keys(e).some((e=>e.startsWith("wake_word.")))))}},{kind:"method",key:"render",value:function(){var e,i,t;if(!this._params||!this._data)return n.Ld;const a=null!==(e=this._params.pipeline)&&void 0!==e&&e.id?this._params.pipeline.name:this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_title");return(0,n.dy)(g||(g=w`
      <ha-dialog
        open
        @closed=${0}
        scrimClickAction
        escapeKeyAction
        .heading=${0}
      >
        <ha-dialog-header slot="heading">
          <ha-icon-button
            slot="navigationIcon"
            dialogAction="cancel"
            .label=${0}
            .path=${0}
          ></ha-icon-button>
          <span slot="title" .title=${0}>${0}</span>
          ${0}
        </ha-dialog-header>
        <div class="content">
          ${0}
          <assist-pipeline-detail-config
            .hass=${0}
            .data=${0}
            .supportedLanguages=${0}
            keys="name,language"
            @value-changed=${0}
            ?dialogInitialFocus=${0}
          ></assist-pipeline-detail-config>
          <assist-pipeline-detail-conversation
            .hass=${0}
            .data=${0}
            keys="conversation_engine,conversation_language,prefer_local_intents"
            @value-changed=${0}
          ></assist-pipeline-detail-conversation>
          ${0}
          <assist-pipeline-detail-stt
            .hass=${0}
            .data=${0}
            keys="stt_engine,stt_language"
            @value-changed=${0}
          ></assist-pipeline-detail-stt>
          <assist-pipeline-detail-tts
            .hass=${0}
            .data=${0}
            keys="tts_engine,tts_language,tts_voice"
            @value-changed=${0}
          ></assist-pipeline-detail-tts>
          ${0}
        </div>
        <ha-button
          slot="primaryAction"
          @click=${0}
          .disabled=${0}
          dialogInitialFocus
        >
          ${0}
        </ha-button>
      </ha-dialog>
    `),this.closeDialog,a,this.hass.localize("ui.common.close"),b,a,a,this._hideWakeWord&&!this._params.hideWakeWord&&this._hasWakeWorkEntities(this.hass.states)?(0,n.dy)(_||(_=w`<ha-button-menu
                slot="actionItems"
                @action=${0}
                @closed=${0}
                menu-corner="END"
                corner="BOTTOM_END"
              >
                <ha-icon-button
                  .path=${0}
                  slot="trigger"
                ></ha-icon-button>
                <mwc-list-item>
                  ${0}
                </mwc-list-item></ha-button-menu
              >`),this._handleShowWakeWord,h.U,$,this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_streaming_wake_word")):n.Ld,this._error?(0,n.dy)(m||(m=w`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):n.Ld,this.hass,this._data,this._supportedLanguages,this._valueChanged,!(null!==(i=this._params.pipeline)&&void 0!==i&&i.id),this.hass,this._data,this._valueChanged,this._cloudActive||"cloud"!==this._data.tts_engine&&"cloud"!==this._data.stt_engine?n.Ld:(0,n.dy)(k||(k=w`
                <ha-alert alert-type="warning">
                  ${0}
                  <a href="/config/cloud" slot="action">
                    <ha-button>
                      ${0}
                    </ha-button>
                  </a>
                </ha-alert>
              `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_message"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_action")),this.hass,this._data,this._valueChanged,this.hass,this._data,this._valueChanged,this._hideWakeWord?n.Ld:(0,n.dy)(y||(y=w`<assist-pipeline-detail-wakeword
                .hass=${0}
                .data=${0}
                keys="wake_word_entity,wake_word_id"
                @value-changed=${0}
              ></assist-pipeline-detail-wakeword>`),this.hass,this._data,this._valueChanged),this._updatePipeline,this._submitting,null!==(t=this._params.pipeline)&&void 0!==t&&t.id?this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.update_assistant_action"):this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_action"))}},{kind:"method",key:"_handleShowWakeWord",value:function(){this._hideWakeWord=!1}},{kind:"method",key:"_valueChanged",value:function(e){this._error=void 0;const i={};e.currentTarget.getAttribute("keys").split(",").forEach((t=>{i[t]=e.detail.value[t]})),this._data=Object.assign(Object.assign({},this._data),i)}},{kind:"method",key:"_updatePipeline",value:async function(){this._submitting=!0;try{var e,i,t,a,s,n,o,d,l,r;const p=this._data,u={name:p.name,language:p.language,conversation_engine:p.conversation_engine,conversation_language:null!==(e=p.conversation_language)&&void 0!==e?e:null,prefer_local_intents:null===(i=p.prefer_local_intents)||void 0===i||i,stt_engine:null!==(t=p.stt_engine)&&void 0!==t?t:null,stt_language:null!==(a=p.stt_language)&&void 0!==a?a:null,tts_engine:null!==(s=p.tts_engine)&&void 0!==s?s:null,tts_language:null!==(n=p.tts_language)&&void 0!==n?n:null,tts_voice:null!==(o=p.tts_voice)&&void 0!==o?o:null,wake_word_entity:null!==(d=p.wake_word_entity)&&void 0!==d?d:null,wake_word_id:null!==(l=p.wake_word_id)&&void 0!==l?l:null};null!==(r=this._params.pipeline)&&void 0!==r&&r.id?await this._params.updatePipeline(u):this._params.createPipeline?await this._params.createPipeline(u):console.error("No createPipeline function provided"),this.closeDialog()}catch(p){this._error=(null==p?void 0:p.message)||"Unknown error"}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[p.yu,(0,n.iv)(f||(f=w`
        .content > *:not(:last-child) {
          margin-bottom: 16px;
          display: block;
        }
        ha-alert {
          margin-bottom: 16px;
          display: block;
        }
        a {
          text-decoration: none;
        }
      `))]}}]}}),n.oi);a()}catch(g){a(g)}}))}}]);
//# sourceMappingURL=9329.6fbc03c489215ebd.js.map