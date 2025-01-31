/*! For license information please see 6334.8bb99472a6573447.js.LICENSE.txt */
"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6334"],{90916:function(t,i,e){e.d(i,{Z:()=>o});const n=t=>t<10?`0${t}`:t;function o(t){const i=Math.floor(t/3600),e=Math.floor(t%3600/60),o=Math.floor(t%3600%60);return i>0?`${i}:${n(e)}:${n(o)}`:e>0?`${e}:${n(o)}`:o>0?""+o:null}},79983:function(t,i,e){e.d(i,{D4:()=>a,D7:()=>d,Ky:()=>o,XO:()=>s,d4:()=>l,oi:()=>r});e(56587),e(1275);const n={"HA-Frontend-Base":`${location.protocol}//${location.host}`},o=(t,i,e)=>{var o;return t.callApi("POST","config/config_entries/flow",{handler:i,show_advanced_options:Boolean(null===(o=t.userData)||void 0===o?void 0:o.showAdvanced),entry_id:e},n)},a=(t,i)=>t.callApi("GET",`config/config_entries/flow/${i}`,void 0,n),s=(t,i,e)=>t.callApi("POST",`config/config_entries/flow/${i}`,e,n),r=(t,i)=>t.callApi("DELETE",`config/config_entries/flow/${i}`),l=(t,i)=>t.callApi("GET","config/config_entries/flow_handlers"+(i?`?type=${i}`:"")),d=t=>t.sendMessagePromise({type:"config_entries/flow/progress"})},32851:function(t,i,e){e.d(i,{AS:()=>o,KY:()=>n});e(19423);const n=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],o=(t,i)=>t.callWS(Object.assign({type:"schedule/create"},i))},80124:function(t,i,e){e.d(i,{rv:()=>s,eF:()=>o,mK:()=>a});e(19423),e(13334);var n=e(90916);const o=(t,i)=>t.callWS(Object.assign({type:"timer/create"},i)),a=t=>{if(!t.attributes.remaining)return;let i=function(t){const i=t.split(":").map(Number);return 3600*i[0]+60*i[1]+i[2]}(t.attributes.remaining);if("active"===t.state){const e=(new Date).getTime(),n=new Date(t.attributes.finishes_at).getTime();i=Math.max((n-e)/1e3,0)}return i},s=(t,i,e)=>{if(!i)return null;if("idle"===i.state||0===e)return t.formatEntityState(i);let o=(0,n.Z)(e||0)||"0";return"paused"===i.state&&(o=`${o} (${t.formatEntityState(i)})`),o}},18694:function(t,i,e){e.d(i,{t:()=>y});e(63721),e(71695),e(40251),e(47021);var n=e(57243),o=e(79983),a=e(1275),s=e(43373);let r,l,d,c,h,m,p,u,g,f=t=>t;const y=(t,i)=>(0,s.w)(t,i,{flowType:"config_flow",showDevices:!0,createFlow:async(t,e)=>{const[n]=await Promise.all([(0,o.Ky)(t,e,i.entryId),t.loadFragmentTranslation("config"),t.loadBackendTranslation("config",e),t.loadBackendTranslation("selector",e),t.loadBackendTranslation("title",e)]);return n},fetchFlow:async(t,i)=>{const e=await(0,o.D4)(t,i);return await t.loadFragmentTranslation("config"),await t.loadBackendTranslation("config",e.handler),await t.loadBackendTranslation("selector",e.handler),e},handleFlowStep:o.XO,deleteFlow:o.oi,renderAbortDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.abort.${i.reason}`,i.description_placeholders);return e?(0,n.dy)(r||(r=f`
            <ha-markdown allow-svg breaks .content=${0}></ha-markdown>
          `),e):i.reason},renderShowFormStepHeader(t,i){return t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.title`,i.description_placeholders)||t.localize(`component.${i.handler}.title`)},renderShowFormStepDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.description`,i.description_placeholders);return e?(0,n.dy)(l||(l=f`
            <ha-markdown allow-svg breaks .content=${0}></ha-markdown>
          `),e):""},renderShowFormStepFieldLabel(t,i,e,n){var o;if("expandable"===e.type)return t.localize(`component.${i.handler}.config.step.${i.step_id}.sections.${e.name}.name`);const a=null!=n&&null!==(o=n.path)&&void 0!==o&&o[0]?`sections.${n.path[0]}.`:"";return t.localize(`component.${i.handler}.config.step.${i.step_id}.${a}data.${e.name}`)||e.name},renderShowFormStepFieldHelper(t,i,e,o){var a;if("expandable"===e.type)return t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.sections.${e.name}.description`);const s=null!=o&&null!==(a=o.path)&&void 0!==a&&a[0]?`sections.${o.path[0]}.`:"",r=t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.${s}data_description.${e.name}`,i.description_placeholders);return r?(0,n.dy)(d||(d=f`<ha-markdown breaks .content=${0}></ha-markdown>`),r):""},renderShowFormStepFieldError(t,i,e){return t.localize(`component.${i.translation_domain||i.translation_domain||i.handler}.config.error.${e}`,i.description_placeholders)||e},renderShowFormStepFieldLocalizeValue(t,i,e){return t.localize(`component.${i.handler}.selector.${e}`)},renderShowFormStepSubmitButton(t,i){return t.localize(`component.${i.handler}.config.step.${i.step_id}.submit`)||t.localize("ui.panel.config.integrations.config_flow."+(!1===i.last_step?"next":"submit"))},renderExternalStepHeader(t,i){return t.localize(`component.${i.handler}.config.step.${i.step_id}.title`)||t.localize("ui.panel.config.integrations.config_flow.external_step.open_site")},renderExternalStepDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.${i.step_id}.description`,i.description_placeholders);return(0,n.dy)(c||(c=f`
        <p>
          ${0}
        </p>
        ${0}
      `),t.localize("ui.panel.config.integrations.config_flow.external_step.description"),e?(0,n.dy)(h||(h=f`
              <ha-markdown
                allow-svg
                breaks
                .content=${0}
              ></ha-markdown>
            `),e):"")},renderCreateEntryDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.create_entry.${i.description||"default"}`,i.description_placeholders);return(0,n.dy)(m||(m=f`
        ${0}
        <p>
          ${0}
        </p>
      `),e?(0,n.dy)(p||(p=f`
              <ha-markdown
                allow-svg
                breaks
                .content=${0}
              ></ha-markdown>
            `),e):"",t.localize("ui.panel.config.integrations.config_flow.created_config",{name:i.title}))},renderShowFormProgressHeader(t,i){return t.localize(`component.${i.handler}.config.step.${i.step_id}.title`)||t.localize(`component.${i.handler}.title`)},renderShowFormProgressDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.progress.${i.progress_action}`,i.description_placeholders);return e?(0,n.dy)(u||(u=f`
            <ha-markdown allow-svg breaks .content=${0}></ha-markdown>
          `),e):""},renderMenuHeader(t,i){return t.localize(`component.${i.handler}.config.step.${i.step_id}.title`)||t.localize(`component.${i.handler}.title`)},renderMenuDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.description`,i.description_placeholders);return e?(0,n.dy)(g||(g=f`
            <ha-markdown allow-svg breaks .content=${0}></ha-markdown>
          `),e):""},renderMenuOption(t,i,e){return t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.menu_options.${e}`,i.description_placeholders)},renderLoadingDescription(t,i,e,n){if("loading_flow"!==i&&"loading_step"!==i)return"";const o=(null==n?void 0:n.handler)||e;return t.localize(`ui.panel.config.integrations.config_flow.loading.${i}`,{integration:o?(0,a.Lh)(t.localize,o):t.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},43373:function(t,i,e){e.d(i,{w:()=>a});e(71695),e(19423),e(40251),e(47021);var n=e(11297);const o=()=>Promise.all([e.e("4823"),e.e("9045")]).then(e.bind(e,22975)),a=(t,i,e)=>{(0,n.B)(t,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:o,dialogParams:Object.assign(Object.assign({},i),{},{flowConfig:e,dialogParentElement:t})})}},84997:function(t,i,e){e.r(i),e.d(i,{DialogHelperDetail:()=>A});var n=e(73577),o=(e(19083),e(71695),e(92745),e(61893),e(40251),e(61006),e(39527),e(13334),e(36993),e(47021),e(31622),e(14394),e(57243)),a=e(50778),s=e(35359),r=e(27486),l=e(49672),d=e(38653),c=(e(90977),e(44118)),h=(e(74064),e(79983));e(19423);var m=e(1275),p=e(32851),u=e(80124),g=e(18694),f=e(66193),y=e(85019),_=e(56395),v=e(11297),w=e(32770);let b,k,$,S,x,F,z,C,L,E=t=>t;const T={input_boolean:{create:(t,i)=>t.callWS(Object.assign({type:"input_boolean/create"},i)),import:()=>e.e("3037").then(e.bind(e,50987)),alias:["switch","toggle"]},input_button:{create:(t,i)=>t.callWS(Object.assign({type:"input_button/create"},i)),import:()=>e.e("3457").then(e.bind(e,41343))},input_text:{create:(t,i)=>t.callWS(Object.assign({type:"input_text/create"},i)),import:()=>e.e("8193").then(e.bind(e,15861))},input_number:{create:(t,i)=>t.callWS(Object.assign({type:"input_number/create"},i)),import:()=>e.e("8456").then(e.bind(e,59795))},input_datetime:{create:(t,i)=>t.callWS(Object.assign({type:"input_datetime/create"},i)),import:()=>e.e("9857").then(e.bind(e,71403))},input_select:{create:(t,i)=>t.callWS(Object.assign({type:"input_select/create"},i)),import:()=>e.e("1422").then(e.bind(e,38344)),alias:["select","dropdown"]},counter:{create:(t,i)=>t.callWS(Object.assign({type:"counter/create"},i)),import:()=>e.e("7014").then(e.bind(e,34026))},timer:{create:u.eF,import:()=>e.e("6239").then(e.bind(e,29241)),alias:["countdown"]},schedule:{create:p.AS,import:()=>Promise.all([e.e("5536"),e.e("5864")]).then(e.bind(e,77595))}};let A=(0,n.Z)([(0,a.Mo)("dialog-helper-detail")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_item",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,a.SB)()],key:"_domain",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_submitting",value(){return!1}},{kind:"field",decorators:[(0,a.IO)(".form")],key:"_form",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_helperFlows",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_loading",value(){return!1}},{kind:"field",decorators:[(0,a.SB)()],key:"_filter",value:void 0},{kind:"field",key:"_params",value:void 0},{kind:"method",key:"showDialog",value:async function(t){this._params=t,this._domain=t.domain,this._item=void 0,this._domain&&this._domain in T&&await T[this._domain].import(),this._opened=!0,await this.updateComplete,this.hass.loadFragmentTranslation("config");const i=await(0,h.d4)(this.hass,["helper"]);await this.hass.loadBackendTranslation("title",i,!0),this._helperFlows=i}},{kind:"method",key:"closeDialog",value:function(){this._opened=!1,this._error=void 0,this._domain=void 0,this._params=void 0,this._filter=void 0,(0,v.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._opened)return o.Ld;let t;var i;if(this._domain)t=(0,o.dy)(b||(b=E`
        <div class="form" @value-changed=${0}>
          ${0}
          ${0}
        </div>
        <mwc-button
          slot="primaryAction"
          @click=${0}
          .disabled=${0}
        >
          ${0}
        </mwc-button>
        ${0}
      `),this._valueChanged,this._error?(0,o.dy)(k||(k=E`<div class="error">${0}</div>`),this._error):"",(0,d.h)(`ha-${this._domain}-form`,{hass:this.hass,item:this._item,new:!0}),this._createItem,this._submitting,this.hass.localize("ui.panel.config.helpers.dialog.create"),null!==(i=this._params)&&void 0!==i&&i.domain?o.Ld:(0,o.dy)($||($=E`<mwc-button
              slot="secondaryAction"
              @click=${0}
              .disabled=${0}
            >
              ${0}
            </mwc-button>`),this._goBack,this._submitting,this.hass.localize("ui.common.back")));else if(this._loading||void 0===this._helperFlows)t=(0,o.dy)(S||(S=E`<ha-circular-progress
        indeterminate
      ></ha-circular-progress>`));else{const i=this._filterHelpers(T,this._helperFlows,this._filter);t=(0,o.dy)(x||(x=E`
        <search-input
          .hass=${0}
          dialogInitialFocus="true"
          .filter=${0}
          @value-changed=${0}
          .label=${0}
        ></search-input>
        <mwc-list
          class="ha-scrollbar"
          innerRole="listbox"
          itemRoles="option"
          innerAriaLabel=${0}
          rootTabbable
          dialogInitialFocus
        >
          ${0}
        </mwc-list>
      `),this.hass,this._filter,this._filterChanged,this.hass.localize("ui.panel.config.integrations.search_helper"),this.hass.localize("ui.panel.config.helpers.dialog.create_helper"),i.map((([t,i])=>{var e;const n=!(t in T)||(0,l.p)(this.hass,t);return(0,o.dy)(F||(F=E`
              <ha-list-item
                .disabled=${0}
                hasmeta
                .domain=${0}
                @request-selected=${0}
                graphic="icon"
              >
                <img
                  slot="graphic"
                  loading="lazy"
                  alt=""
                  src=${0}
                  crossorigin="anonymous"
                  referrerpolicy="no-referrer"
                />
                <span class="item-text"> ${0} </span>
                <ha-icon-next slot="meta"></ha-icon-next>
              </ha-list-item>
              ${0}
            `),!n,t,this._domainPicked,(0,y.X1)({domain:t,type:"icon",useFallback:!0,darkOptimized:null===(e=this.hass.themes)||void 0===e?void 0:e.darkMode}),i,n?"":(0,o.dy)(z||(z=E`
                    <simple-tooltip animation-delay="0"
                      >${0}</simple-tooltip
                    >
                  `),this.hass.localize("ui.dialogs.helper_settings.platform_not_loaded",{platform:t})))})))}return(0,o.dy)(C||(C=E`
      <ha-dialog
        open
        @closed=${0}
        class=${0}
        scrimClickAction
        escapeKeyAction
        .hideActions=${0}
        .heading=${0}
      >
        ${0}
      </ha-dialog>
    `),this.closeDialog,(0,s.$)({"button-left":!this._domain}),!this._domain,(0,c.i)(this.hass,this._domain?this.hass.localize("ui.panel.config.helpers.dialog.create_platform",{platform:(0,_.X)(this._domain)&&this.hass.localize(`ui.panel.config.helpers.types.${this._domain}`)||this._domain}):this.hass.localize("ui.panel.config.helpers.dialog.create_helper")),t)}},{kind:"field",key:"_filterHelpers",value(){return(0,r.Z)(((t,i,e)=>{const n=[];for(const o of Object.keys(t))n.push([o,this.hass.localize(`ui.panel.config.helpers.types.${o}`)||o]);if(i)for(const o of i)n.push([o,(0,m.Lh)(this.hass.localize,o)]);return n.filter((([i,n])=>{if(e){var o;const a=e.toLowerCase();return n.toLowerCase().includes(a)||i.toLowerCase().includes(a)||((null===(o=t[i])||void 0===o?void 0:o.alias)||[]).some((t=>t.toLowerCase().includes(a)))}return!0})).sort(((t,i)=>(0,w.$)(t[1],i[1],this.hass.locale.language)))}))}},{kind:"method",key:"_filterChanged",value:async function(t){this._filter=t.detail.value}},{kind:"method",key:"_valueChanged",value:function(t){this._item=t.detail.value}},{kind:"method",key:"_createItem",value:async function(){if(this._domain&&this._item){this._submitting=!0,this._error="";try{var t;const i=await T[this._domain].create(this.hass,this._item);null!==(t=this._params)&&void 0!==t&&t.dialogClosedCallback&&i.id&&this._params.dialogClosedCallback({flowFinished:!0,entityId:`${this._domain}.${i.id}`}),this.closeDialog()}catch(i){this._error=i.message||"Unknown error"}finally{this._submitting=!1}}}},{kind:"method",key:"_domainPicked",value:async function(t){const i=t.target.closest("ha-list-item").domain;if(i in T){this._loading=!0;try{await T[i].import(),this._domain=i}finally{this._loading=!1}this._focusForm()}else(0,g.t)(this,{startFlowHandler:i,manifest:await(0,m.t4)(this.hass,i),dialogClosedCallback:this._params.dialogClosedCallback}),this.closeDialog()}},{kind:"method",key:"_focusForm",value:async function(){var t;await this.updateComplete,(null===(t=this._form)||void 0===t?void 0:t.lastElementChild).focus()}},{kind:"method",key:"_goBack",value:function(){this._domain=void 0,this._item=void 0,this._error=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return[f.$c,f.yu,(0,o.iv)(L||(L=E`
        ha-dialog.button-left {
          --justify-action-buttons: flex-start;
        }
        ha-dialog {
          --dialog-content-padding: 0;
          --dialog-scroll-divider-color: transparent;
          --mdc-dialog-max-height: 60vh;
        }
        @media all and (min-width: 550px) {
          ha-dialog {
            --mdc-dialog-min-width: 500px;
          }
        }
        ha-icon-next {
          width: 24px;
        }
        .form {
          padding: 24px;
        }
        search-input {
          display: block;
          margin: 16px 16px 0;
        }
        mwc-list {
          height: calc(60vh - 184px);
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          mwc-list {
            height: calc(100vh - 184px);
          }
        }
      `))]}}]}}),o.oi)},85019:function(t,i,e){e.d(i,{X1:()=>n,u4:()=>o,zC:()=>a});e(88044);const n=t=>`https://brands.home-assistant.io/${t.brand?"brands/":""}${t.useFallback?"_/":""}${t.domain}/${t.darkOptimized?"dark_":""}${t.type}.png`,o=t=>t.split("/")[4],a=t=>t.startsWith("https://brands.home-assistant.io/")},14394:function(t,i,e){e(19423),e(81804),e(39527),e(41360);var n=e(57243);let o,a,s=t=>t;class r extends n.oi{static get styles(){return[(0,n.iv)(o||(o=s`
        :host {
          display: block;
          position: absolute;
          outline: none;
          z-index: 1002;
          -moz-user-select: none;
          -ms-user-select: none;
          -webkit-user-select: none;
          user-select: none;
          cursor: default;
          pointer-events: none;
        }

        #tooltip {
          display: block;
          outline: none;
          font-size: var(--simple-tooltip-font-size, 10px);
          line-height: 1;
          background-color: var(--simple-tooltip-background, #616161);
          color: var(--simple-tooltip-text-color, white);
          padding: 8px;
          border-radius: var(--simple-tooltip-border-radius, 2px);
          width: var(--simple-tooltip-width);
        }

        @keyframes keyFrameScaleUp {
          0% {
            transform: scale(0);
          }

          100% {
            transform: scale(1);
          }
        }

        @keyframes keyFrameScaleDown {
          0% {
            transform: scale(1);
          }

          100% {
            transform: scale(0);
          }
        }

        @keyframes keyFrameFadeInOpacity {
          0% {
            opacity: 0;
          }

          100% {
            opacity: var(--simple-tooltip-opacity, 0.9);
          }
        }

        @keyframes keyFrameFadeOutOpacity {
          0% {
            opacity: var(--simple-tooltip-opacity, 0.9);
          }

          100% {
            opacity: 0;
          }
        }

        @keyframes keyFrameSlideDownIn {
          0% {
            transform: translateY(-2000px);
            opacity: 0;
          }

          10% {
            opacity: 0.2;
          }

          100% {
            transform: translateY(0);
            opacity: var(--simple-tooltip-opacity, 0.9);
          }
        }

        @keyframes keyFrameSlideDownOut {
          0% {
            transform: translateY(0);
            opacity: var(--simple-tooltip-opacity, 0.9);
          }

          10% {
            opacity: 0.2;
          }

          100% {
            transform: translateY(-2000px);
            opacity: 0;
          }
        }

        .fade-in-animation {
          opacity: 0;
          animation-delay: var(--simple-tooltip-delay-in, 500ms);
          animation-name: keyFrameFadeInOpacity;
          animation-iteration-count: 1;
          animation-timing-function: ease-in;
          animation-duration: var(--simple-tooltip-duration-in, 500ms);
          animation-fill-mode: forwards;
        }

        .fade-out-animation {
          opacity: var(--simple-tooltip-opacity, 0.9);
          animation-delay: var(--simple-tooltip-delay-out, 0ms);
          animation-name: keyFrameFadeOutOpacity;
          animation-iteration-count: 1;
          animation-timing-function: ease-in;
          animation-duration: var(--simple-tooltip-duration-out, 500ms);
          animation-fill-mode: forwards;
        }

        .scale-up-animation {
          transform: scale(0);
          opacity: var(--simple-tooltip-opacity, 0.9);
          animation-delay: var(--simple-tooltip-delay-in, 500ms);
          animation-name: keyFrameScaleUp;
          animation-iteration-count: 1;
          animation-timing-function: ease-in;
          animation-duration: var(--simple-tooltip-duration-in, 500ms);
          animation-fill-mode: forwards;
        }

        .scale-down-animation {
          transform: scale(1);
          opacity: var(--simple-tooltip-opacity, 0.9);
          animation-delay: var(--simple-tooltip-delay-out, 500ms);
          animation-name: keyFrameScaleDown;
          animation-iteration-count: 1;
          animation-timing-function: ease-in;
          animation-duration: var(--simple-tooltip-duration-out, 500ms);
          animation-fill-mode: forwards;
        }

        .slide-down-animation {
          transform: translateY(-2000px);
          opacity: 0;
          animation-delay: var(--simple-tooltip-delay-out, 500ms);
          animation-name: keyFrameSlideDownIn;
          animation-iteration-count: 1;
          animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
          animation-duration: var(--simple-tooltip-duration-out, 500ms);
          animation-fill-mode: forwards;
        }

        .slide-down-animation-out {
          transform: translateY(0);
          opacity: var(--simple-tooltip-opacity, 0.9);
          animation-delay: var(--simple-tooltip-delay-out, 500ms);
          animation-name: keyFrameSlideDownOut;
          animation-iteration-count: 1;
          animation-timing-function: cubic-bezier(0.4, 0, 1, 1);
          animation-duration: var(--simple-tooltip-duration-out, 500ms);
          animation-fill-mode: forwards;
        }

        .cancel-animation {
          animation-delay: -30s !important;
        }

        .hidden {
          position: absolute;
          left: -10000px;
          inset-inline-start: -10000px;
          inset-inline-end: initial;
          top: auto;
          width: 1px;
          height: 1px;
          overflow: hidden;
        }
      `))]}render(){return(0,n.dy)(a||(a=s` <div
      id="tooltip"
      class="hidden"
      @animationend="${0}"
    >
      <slot></slot>
    </div>`),this._onAnimationEnd)}static get properties(){return Object.assign(Object.assign({},super.properties),{},{for:{type:String},manualMode:{type:Boolean,attribute:"manual-mode"},position:{type:String},fitToVisibleBounds:{type:Boolean,attribute:"fit-to-visible-bounds"},offset:{type:Number},marginTop:{type:Number,attribute:"margin-top"},animationDelay:{type:Number,attribute:"animation-delay"},animationEntry:{type:String,attribute:"animation-entry"},animationExit:{type:String,attribute:"animation-exit"},_showing:{type:Boolean}})}static get tag(){return"simple-tooltip"}constructor(){super(),this.manualMode=!1,this.position="bottom",this.fitToVisibleBounds=!1,this.offset=14,this.marginTop=14,this.animationEntry="",this.animationExit="",this.animationConfig={entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]},setTimeout((()=>{this.addEventListener("webkitAnimationEnd",this._onAnimationEnd.bind(this)),this.addEventListener("mouseenter",this.hide.bind(this))}),0)}get target(){var t=this.parentNode,i=this.getRootNode();return this.for?i.querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t}disconnectedCallback(){this.manualMode||this._removeListeners(),super.disconnectedCallback()}playAnimation(t){"entry"===t?this.show():"exit"===t&&this.hide()}cancelAnimation(){this.shadowRoot.querySelector("#tooltip").classList.add("cancel-animation")}show(){if(!this._showing){if(""===this.textContent.trim()){for(var t=!0,i=this.children,e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.shadowRoot.querySelector("#tooltip").classList.remove("hidden"),this.shadowRoot.querySelector("#tooltip").classList.remove("cancel-animation"),this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.shadowRoot.querySelector("#tooltip").classList.add(this._getAnimationType("entry"))}}hide(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0,clearTimeout(this.__debounceCancel),this.__debounceCancel=setTimeout((()=>{this._cancelAnimation()}),5e3)}}updatePosition(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,n=this.offsetParent.getBoundingClientRect(),o=this._target.getBoundingClientRect(),a=this.getBoundingClientRect(),s=(o.width-a.width)/2,r=(o.height-a.height)/2,l=o.left-n.left,d=o.top-n.top;switch(this.position){case"top":i=l+s,e=d-a.height-t;break;case"bottom":i=l+s,e=d+o.height+t;break;case"left":i=l-a.width-t,e=d+r;break;case"right":i=l+o.width+t,e=d+r}this.fitToVisibleBounds?(n.left+i+a.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),n.top+e+a.height>window.innerHeight?(this.style.bottom=n.height-d+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}}_addListeners(){this._target&&(this._target.addEventListener("mouseenter",this.show.bind(this)),this._target.addEventListener("focus",this.show.bind(this)),this._target.addEventListener("mouseleave",this.hide.bind(this)),this._target.addEventListener("blur",this.hide.bind(this)),this._target.addEventListener("tap",this.hide.bind(this)))}_findTarget(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()}_manualModeChanged(){this.manualMode?this._removeListeners():this._addListeners()}_cancelAnimation(){this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("entry")),this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("exit")),this.shadowRoot.querySelector("#tooltip").classList.remove("cancel-animation"),this.shadowRoot.querySelector("#tooltip").classList.add("hidden")}_onAnimationFinish(){this._showing&&(this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("entry")),this.shadowRoot.querySelector("#tooltip").classList.remove("cancel-animation"),this.shadowRoot.querySelector("#tooltip").classList.add(this._getAnimationType("exit")))}_onAnimationEnd(){this._animationPlaying=!1,this._showing||(this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("exit")),this.shadowRoot.querySelector("#tooltip").classList.add("hidden"))}_getAnimationType(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?document.documentElement.style.setProperty("--simple-tooltip-delay-in",i+"ms"):"exit"===t&&document.documentElement.style.setProperty("--simple-tooltip-delay-out",i+"ms")}return this.animationConfig[t][0].name}}_removeListeners(){this._target&&(this._target.removeEventListener("mouseover",this.show.bind(this)),this._target.removeEventListener("focusin",this.show.bind(this)),this._target.removeEventListener("mouseout",this.hide.bind(this)),this._target.removeEventListener("focusout",this.hide.bind(this)),this._target.removeEventListener("click",this.hide.bind(this)))}firstUpdated(t){this.setAttribute("role","tooltip"),this.setAttribute("tabindex",-1),this._findTarget()}updated(t){t.forEach(((t,i)=>{"for"==i&&this._findTarget(this[i],t),"manualMode"==i&&this._manualModeChanged(this[i],t),"animationDelay"==i&&this._delayChange(this[i],t)}))}_delayChange(t){500!==t&&document.documentElement.style.setProperty("--simple-tooltip-delay-in",t+"ms")}}customElements.define(r.tag,r)}}]);
//# sourceMappingURL=6334.8bb99472a6573447.js.map