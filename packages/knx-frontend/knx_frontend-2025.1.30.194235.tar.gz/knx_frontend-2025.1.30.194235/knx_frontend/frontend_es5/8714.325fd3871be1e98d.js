"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8714"],{46784:function(e,t,i){i.a(e,(async function(e,s){try{i.d(t,{u:()=>d});var a=i(69440),n=i(27486),l=e([a]);a=(l.then?(await l)():l)[0];const d=(e,t)=>{try{var i,s;return null!==(i=null===(s=r(t))||void 0===s?void 0:s.of(e))&&void 0!==i?i:e}catch(a){return e}},r=(0,n.Z)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})));s()}catch(d){s(d)}}))},24022:function(e,t,i){i.a(e,(async function(e,t){try{var s=i(73577),a=i(72621),n=(i(71695),i(39527),i(67670),i(13334),i(47021),i(57243)),l=i(50778),d=i(11297),r=i(81036),c=i(46784),o=i(4855),u=(i(74064),i(58130),e([c]));c=(u.then?(await u)():u)[0];let p,h,b,v,g=e=>e;const k="preferred",y="last_used";(0,s.Z)([(0,l.Mo)("ha-assist-pipeline-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"includeLastUsed",value(){return!1}},{kind:"field",decorators:[(0,l.SB)()],key:"_pipelines",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_preferredPipeline",value(){return null}},{kind:"get",key:"_default",value:function(){return this.includeLastUsed?y:k}},{kind:"method",key:"render",value:function(){var e,t;if(!this._pipelines)return n.Ld;const i=null!==(e=this.value)&&void 0!==e?e:this._default;return(0,n.dy)(p||(p=g`
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
        <ha-list-item .value=${0}>
          ${0}
        </ha-list-item>
        ${0}
      </ha-select>
    `),this.label||this.hass.localize("ui.components.pipeline-picker.pipeline"),i,this.required,this.disabled,this._changed,r.U,this.includeLastUsed?(0,n.dy)(h||(h=g`
              <ha-list-item .value=${0}>
                ${0}
              </ha-list-item>
            `),y,this.hass.localize("ui.components.pipeline-picker.last_used")):null,k,this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:null===(t=this._pipelines.find((e=>e.id===this._preferredPipeline)))||void 0===t?void 0:t.name}),this._pipelines.map((e=>(0,n.dy)(b||(b=g`<ha-list-item .value=${0}>
              ${0}
              (${0})
            </ha-list-item>`),e.id,e.name,(0,c.u)(e.language,this.hass.locale)))))}},{kind:"method",key:"firstUpdated",value:function(e){(0,a.Z)(i,"firstUpdated",this,3)([e]),(0,o.SC)(this.hass).then((e=>{this._pipelines=e.pipelines,this._preferredPipeline=e.preferred_pipeline}))}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(v||(v=g`
    ha-select {
      width: 100%;
    }
  `))}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===this._default||(this.value=t.value===this._default?void 0:t.value,(0,d.B)(this,"value-changed",{value:this.value}))}}]}}),n.oi);t()}catch(p){t(p)}}))},93697:function(e,t,i){i.a(e,(async function(e,s){try{i.r(t),i.d(t,{HaAssistPipelineSelector:()=>p});var a=i(73577),n=(i(71695),i(47021),i(57243)),l=i(50778),d=i(24022),r=e([d]);d=(r.then?(await r)():r)[0];let c,o,u=e=>e,p=(0,a.Z)([(0,l.Mo)("ha-selector-assist_pipeline")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){var e;return(0,n.dy)(c||(c=u`
      <ha-assist-pipeline-picker
        .hass=${0}
        .value=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        .includeLastUsed=${0}
      ></ha-assist-pipeline-picker>
    `),this.hass,this.value,this.label,this.helper,this.disabled,this.required,Boolean(null===(e=this.selector.assist_pipeline)||void 0===e?void 0:e.include_last_used))}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(o||(o=u`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `))}}]}}),n.oi);s()}catch(c){s(c)}}))},4855:function(e,t,i){i.d(t,{Dy:()=>c,PA:()=>l,SC:()=>n,Xp:()=>a,af:()=>r,eP:()=>s,jZ:()=>d});i(71695),i(19423),i(47021);const s=(e,t,i)=>"run-start"===t.type?e={init_options:i,stage:"ready",run:t.data,events:[t]}:e?((e="wake_word-start"===t.type?Object.assign(Object.assign({},e),{},{stage:"wake_word",wake_word:Object.assign(Object.assign({},t.data),{},{done:!1})}):"wake_word-end"===t.type?Object.assign(Object.assign({},e),{},{wake_word:Object.assign(Object.assign(Object.assign({},e.wake_word),t.data),{},{done:!0})}):"stt-start"===t.type?Object.assign(Object.assign({},e),{},{stage:"stt",stt:Object.assign(Object.assign({},t.data),{},{done:!1})}):"stt-end"===t.type?Object.assign(Object.assign({},e),{},{stt:Object.assign(Object.assign(Object.assign({},e.stt),t.data),{},{done:!0})}):"intent-start"===t.type?Object.assign(Object.assign({},e),{},{stage:"intent",intent:Object.assign(Object.assign({},t.data),{},{done:!1})}):"intent-end"===t.type?Object.assign(Object.assign({},e),{},{intent:Object.assign(Object.assign(Object.assign({},e.intent),t.data),{},{done:!0})}):"tts-start"===t.type?Object.assign(Object.assign({},e),{},{stage:"tts",tts:Object.assign(Object.assign({},t.data),{},{done:!1})}):"tts-end"===t.type?Object.assign(Object.assign({},e),{},{tts:Object.assign(Object.assign(Object.assign({},e.tts),t.data),{},{done:!0})}):"run-end"===t.type?Object.assign(Object.assign({},e),{},{stage:"done"}):"error"===t.type?Object.assign(Object.assign({},e),{},{stage:"error",error:t.data}):Object.assign({},e)).events=[...e.events,t],e):void console.warn("Received unexpected event before receiving session",t),a=(e,t,i)=>e.connection.subscribeMessage(t,Object.assign(Object.assign({},i),{},{type:"assist_pipeline/run"})),n=e=>e.callWS({type:"assist_pipeline/pipeline/list"}),l=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:t}),d=(e,t)=>e.callWS(Object.assign({type:"assist_pipeline/pipeline/create"},t)),r=(e,t,i)=>e.callWS(Object.assign({type:"assist_pipeline/pipeline/update",pipeline_id:t},i)),c=e=>e.callWS({type:"assist_pipeline/language/list"})}}]);
//# sourceMappingURL=8714.325fd3871be1e98d.js.map