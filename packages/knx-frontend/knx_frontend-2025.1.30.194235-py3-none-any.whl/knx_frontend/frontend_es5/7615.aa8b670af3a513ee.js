"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["7615"],{19778:function(e,n,t){t.r(n),t.d(n,{HaConversationAgentSelector:()=>D});var o=t(73577),i=(t(71695),t(47021),t(57243)),a=t(50778),s=t(72621),r=(t(19083),t(40251),t(61006),t(39527),t(67670),t(13334),t(11297)),l=t(81036),d=t(56587),c=t(87055),u=t(31762),p=t(1275);t(19423);const h=(e,n)=>{var t;return e.callApi("POST","config/config_entries/options/flow",{handler:n,show_advanced_options:Boolean(null===(t=e.userData)||void 0===t?void 0:t.showAdvanced)})},g=(e,n)=>e.callApi("GET",`config/config_entries/options/flow/${n}`),v=(e,n,t)=>e.callApi("POST",`config/config_entries/options/flow/${n}`,t),m=(e,n)=>e.callApi("DELETE",`config/config_entries/options/flow/${n}`);var f=t(43373);let _,k,y,$,w,b,C=e=>e;t(74064),t(58130);var S=t(60498);let L,z,F,E,A,B=e=>e;const O="__NONE_OPTION__";(0,o.Z)([(0,a.Mo)("ha-conversation-agent-picker")],(function(e,n){class t extends n{constructor(...n){super(...n),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,a.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"language",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,a.SB)()],key:"_agents",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_configEntry",value:void 0},{kind:"method",key:"render",value:function(){var e;if(!this._agents)return i.Ld;let n=this.value;if(!n&&this.required){for(const e of this._agents)if("conversation.home_assistant"===e.id&&e.supported_languages.includes(this.language)){n=e.id;break}if(!n)for(const e of this._agents)if("*"===e.supported_languages&&e.supported_languages.includes(this.language)){n=e.id;break}}return n||(n=O),(0,i.dy)(L||(L=B`
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
        ${0}</ha-select
      >${0}
    `),this.label||this.hass.localize("ui.components.coversation-agent-picker.conversation_agent"),n,this.required,this.disabled,this._changed,l.U,this.required?i.Ld:(0,i.dy)(z||(z=B`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),O,this.hass.localize("ui.components.coversation-agent-picker.none")),this._agents.map((e=>(0,i.dy)(F||(F=B`<ha-list-item
              .value=${0}
              .disabled=${0}
            >
              ${0}
            </ha-list-item>`),e.id,"*"!==e.supported_languages&&0===e.supported_languages.length,e.name))),null!==(e=this._configEntry)&&void 0!==e&&e.supports_options?(0,i.dy)(E||(E=B`<ha-icon-button
            .path=${0}
            @click=${0}
          ></ha-icon-button>`),"M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z",this._openOptionsFlow):"")}},{kind:"method",key:"willUpdate",value:function(e){(0,s.Z)(t,"willUpdate",this,3)([e]),this.hasUpdated?e.has("language")&&this._debouncedUpdateAgents():this._updateAgents(),e.has("value")&&this._maybeFetchConfigEntry()}},{kind:"method",key:"_maybeFetchConfigEntry",value:async function(){if(this.value&&this.value in this.hass.entities)try{const e=await(0,S.L3)(this.hass,this.value);if(!e.config_entry_id)return void(this._configEntry=void 0);this._configEntry=(await(0,c.RQ)(this.hass,e.config_entry_id)).config_entry}catch(e){this._configEntry=void 0}else this._configEntry=void 0}},{kind:"field",key:"_debouncedUpdateAgents",value(){return(0,d.D)((()=>this._updateAgents()),500)}},{kind:"method",key:"_updateAgents",value:async function(){const{agents:e}=await(0,u.rM)(this.hass,this.language,this.hass.config.country||void 0);if(this._agents=e,!this.value)return;const n=e.find((e=>e.id===this.value));(0,r.B)(this,"supported-languages-changed",{value:null==n?void 0:n.supported_languages}),(!n||"*"!==n.supported_languages&&0===n.supported_languages.length)&&(this.value=void 0,(0,r.B)(this,"value-changed",{value:this.value}))}},{kind:"method",key:"_openOptionsFlow",value:async function(){var e,n,t;this._configEntry&&(e=this,n=this._configEntry,t={manifest:await(0,p.t4)(this.hass,this._configEntry.domain)},(0,f.w)(e,Object.assign({startFlowHandler:n.entry_id,domain:n.domain},t),{flowType:"options_flow",showDevices:!1,createFlow:async(e,t)=>{const[o]=await Promise.all([h(e,t),e.loadFragmentTranslation("config"),e.loadBackendTranslation("options",n.domain),e.loadBackendTranslation("selector",n.domain)]);return o},fetchFlow:async(e,t)=>{const[o]=await Promise.all([g(e,t),e.loadFragmentTranslation("config"),e.loadBackendTranslation("options",n.domain),e.loadBackendTranslation("selector",n.domain)]);return o},handleFlowStep:v,deleteFlow:m,renderAbortDescription(e,t){const o=e.localize(`component.${t.translation_domain||n.domain}.options.abort.${t.reason}`,t.description_placeholders);return o?(0,i.dy)(_||(_=C`
              <ha-markdown
                breaks
                allow-svg
                .content=${0}
              ></ha-markdown>
            `),o):t.reason},renderShowFormStepHeader(e,t){return e.localize(`component.${t.translation_domain||n.domain}.options.step.${t.step_id}.title`,t.description_placeholders)||e.localize("ui.dialogs.options_flow.form.header")},renderShowFormStepDescription(e,t){const o=e.localize(`component.${t.translation_domain||n.domain}.options.step.${t.step_id}.description`,t.description_placeholders);return o?(0,i.dy)(k||(k=C`
              <ha-markdown
                allow-svg
                breaks
                .content=${0}
              ></ha-markdown>
            `),o):""},renderShowFormStepFieldLabel(e,t,o,i){var a;if("expandable"===o.type)return e.localize(`component.${n.domain}.options.step.${t.step_id}.sections.${o.name}.name`);const s=null!=i&&null!==(a=i.path)&&void 0!==a&&a[0]?`sections.${i.path[0]}.`:"";return e.localize(`component.${n.domain}.options.step.${t.step_id}.${s}data.${o.name}`)||o.name},renderShowFormStepFieldHelper(e,t,o,a){var s;if("expandable"===o.type)return e.localize(`component.${t.translation_domain||n.domain}.options.step.${t.step_id}.sections.${o.name}.description`);const r=null!=a&&null!==(s=a.path)&&void 0!==s&&s[0]?`sections.${a.path[0]}.`:"",l=e.localize(`component.${t.translation_domain||n.domain}.options.step.${t.step_id}.${r}data_description.${o.name}`,t.description_placeholders);return l?(0,i.dy)(y||(y=C`<ha-markdown breaks .content=${0}></ha-markdown>`),l):""},renderShowFormStepFieldError(e,t,o){return e.localize(`component.${t.translation_domain||n.domain}.options.error.${o}`,t.description_placeholders)||o},renderShowFormStepFieldLocalizeValue(e,t,o){return e.localize(`component.${n.domain}.selector.${o}`)},renderShowFormStepSubmitButton(e,t){return e.localize(`component.${n.domain}.options.step.${t.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===t.last_step?"next":"submit"))},renderExternalStepHeader(e,n){return""},renderExternalStepDescription(e,n){return""},renderCreateEntryDescription(e,n){return(0,i.dy)($||($=C`
          <p>${0}</p>
        `),e.localize("ui.dialogs.options_flow.success.description"))},renderShowFormProgressHeader(e,t){return e.localize(`component.${n.domain}.options.step.${t.step_id}.title`)||e.localize(`component.${n.domain}.title`)},renderShowFormProgressDescription(e,t){const o=e.localize(`component.${t.translation_domain||n.domain}.options.progress.${t.progress_action}`,t.description_placeholders);return o?(0,i.dy)(w||(w=C`
              <ha-markdown
                allow-svg
                breaks
                .content=${0}
              ></ha-markdown>
            `),o):""},renderMenuHeader(e,t){return e.localize(`component.${n.domain}.options.step.${t.step_id}.title`)||e.localize(`component.${n.domain}.title`)},renderMenuDescription(e,t){const o=e.localize(`component.${t.translation_domain||n.domain}.options.step.${t.step_id}.description`,t.description_placeholders);return o?(0,i.dy)(b||(b=C`
              <ha-markdown
                allow-svg
                breaks
                .content=${0}
              ></ha-markdown>
            `),o):""},renderMenuOption(e,t,o){return e.localize(`component.${t.translation_domain||n.domain}.options.step.${t.step_id}.menu_options.${o}`,t.description_placeholders)},renderLoadingDescription(e,t){return e.localize(`component.${n.domain}.options.loading`)||("loading_flow"===t||"loading_step"===t?e.localize(`ui.dialogs.options_flow.loading.${t}`,{integration:(0,p.Lh)(e.localize,n.domain)}):"")}}))}},{kind:"field",static:!0,key:"styles",value(){return(0,i.iv)(A||(A=B`
    :host {
      display: flex;
      align-items: center;
    }
    ha-select {
      width: 100%;
    }
    ha-icon-button {
      color: var(--secondary-text-color);
    }
  `))}},{kind:"method",key:"_changed",value:function(e){var n;const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===O||(this.value=t.value===O?void 0:t.value,(0,r.B)(this,"value-changed",{value:this.value}),(0,r.B)(this,"supported-languages-changed",{value:null===(n=this._agents.find((e=>e.id===this.value)))||void 0===n?void 0:n.supported_languages}))}}]}}),i.oi);let T,x,M=e=>e,D=(0,o.Z)([(0,a.Mo)("ha-selector-conversation_agent")],(function(e,n){return{F:class extends n{constructor(...n){super(...n),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,n;return(0,i.dy)(T||(T=M`<ha-conversation-agent-picker
      .hass=${0}
      .value=${0}
      .language=${0}
      .label=${0}
      .helper=${0}
      .disabled=${0}
      .required=${0}
    ></ha-conversation-agent-picker>`),this.hass,this.value,(null===(e=this.selector.conversation_agent)||void 0===e?void 0:e.language)||(null===(n=this.context)||void 0===n?void 0:n.language),this.label,this.helper,this.disabled,this.required)}},{kind:"field",static:!0,key:"styles",value(){return(0,i.iv)(x||(x=M`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `))}}]}}),i.oi)},31762:function(e,n,t){t.d(n,{rM:()=>i,zt:()=>o});let o=function(e){return e[e.CONTROL=1]="CONTROL",e}({});const i=(e,n,t)=>e.callWS({type:"conversation/agent/list",language:n,country:t})},60498:function(e,n,t){t.d(n,{L3:()=>s,Mw:()=>l,vA:()=>a,w1:()=>r});t(19083),t(71695),t(61893),t(19423),t(39527),t(99790),t(67670),t(47021);var o=t(27486),i=t(73525);t(32770),t(56587);const a=(e,n)=>{if(n.name)return n.name;const t=e.states[n.entity_id];return t?(0,i.C)(t):n.original_name?n.original_name:n.entity_id},s=(e,n)=>e.callWS({type:"config/entity_registry/get",entity_id:n}),r=(0,o.Z)((e=>{const n={};for(const t of e)n[t.entity_id]=t;return n})),l=(0,o.Z)((e=>{const n={};for(const t of e)n[t.id]=t;return n}))},1275:function(e,n,t){t.d(n,{F3:()=>i,Lh:()=>o,t4:()=>a});t(56587);const o=(e,n,t)=>e(`component.${n}.title`)||(null==t?void 0:t.name)||n,i=(e,n)=>{const t={type:"manifest/list"};return n&&(t.integrations=n),e.callWS(t)},a=(e,n)=>e.callWS({type:"manifest/get",integration:n})},43373:function(e,n,t){t.d(n,{w:()=>a});t(71695),t(19423),t(40251),t(47021);var o=t(11297);const i=()=>Promise.all([t.e("4823"),t.e("9045")]).then(t.bind(t,22975)),a=(e,n,t)=>{(0,o.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:i,dialogParams:Object.assign(Object.assign({},n),{},{flowConfig:t,dialogParentElement:e})})}}}]);
//# sourceMappingURL=7615.aa8b670af3a513ee.js.map