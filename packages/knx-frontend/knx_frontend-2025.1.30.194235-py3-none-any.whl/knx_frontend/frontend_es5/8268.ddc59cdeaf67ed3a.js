"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8268"],{99642:function(e,t,i){i.d(t,{I:()=>o});i(19083),i(71695),i(61006),i(47021);const o=(e,t,i,o)=>{const[a,n,r]=e.split(".",3);return Number(a)>t||Number(a)===t&&(void 0===o?Number(n)>=i:Number(n)>i)||void 0!==o&&Number(a)===t&&Number(n)===i&&Number(r)>=o}},9115:function(e,t,i){i.d(t,{K:()=>o});const o=e=>{switch(e.language){case"cs":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},58303:function(e,t,i){i.a(e,(async function(e,t){try{var o=i(73577),a=i(72621),n=(i(71695),i(13334),i(47021),i(87515)),r=i(57243),s=i(50778),l=i(35359),d=i(11297),c=(i(20095),i(59897),i(9115)),h=i(24785),u=i(84120),v=e([n]);n=(v.then?(await v)():v)[0];let p,f,b,k,g,m,x,y,w=e=>e;const _="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",$="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z";(0,o.Z)([(0,s.Mo)("ha-file-upload")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"accept",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"icon",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"secondary",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"supports",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Object})],key:"value",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"multiple",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"uploading",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Number})],key:"progress",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,attribute:"auto-open-file-dialog"})],key:"autoOpenFileDialog",value(){return!1}},{kind:"field",decorators:[(0,s.SB)()],key:"_drag",value(){return!1}},{kind:"field",decorators:[(0,s.IO)("#input")],key:"_input",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,a.Z)(i,"firstUpdated",this,3)([e]),this.autoOpenFileDialog&&this._openFilePicker()}},{kind:"get",key:"_name",value:function(){if(void 0===this.value)return"";if("string"==typeof this.value)return this.value;return(this.value instanceof FileList?Array.from(this.value):(0,h.r)(this.value)).map((e=>e.name)).join(", ")}},{kind:"method",key:"render",value:function(){var e,t,i,o,a;return(0,r.dy)(p||(p=w`
      ${0}
    `),this.uploading?(0,r.dy)(f||(f=w`<div class="container">
            <div class="uploading">
              <span class="header"
                >${0}</span
              >
              ${0}
            </div>
            <mwc-linear-progress
              .indeterminate=${0}
              .progress=${0}
            ></mwc-linear-progress>
          </div>`),this.value?null===(e=this.hass)||void 0===e?void 0:e.localize("ui.components.file-upload.uploading_name",{name:this._name}):null===(t=this.hass)||void 0===t?void 0:t.localize("ui.components.file-upload.uploading"),this.progress?(0,r.dy)(b||(b=w`<div class="progress">
                    ${0}${0}%
                  </div>`),this.progress,(0,c.K)(this.hass.locale)):r.Ld,!this.progress,this.progress?this.progress/100:void 0):(0,r.dy)(k||(k=w`<label
            for=${0}
            class="container ${0}"
            @drop=${0}
            @dragenter=${0}
            @dragover=${0}
            @dragleave=${0}
            @dragend=${0}
            >${0}
            <input
              id="input"
              type="file"
              class="file"
              .accept=${0}
              .multiple=${0}
              @change=${0}
          /></label>`),this.value?"":"input",(0,l.$)({dragged:this._drag,multiple:this.multiple,value:Boolean(this.value)}),this._handleDrop,this._handleDragStart,this._handleDragStart,this._handleDragEnd,this._handleDragEnd,this.value?"string"==typeof this.value?(0,r.dy)(m||(m=w`<div class="row">
                    <div class="value" @click=${0}>
                      <ha-svg-icon
                        .path=${0}
                      ></ha-svg-icon>
                      ${0}
                    </div>
                    <ha-icon-button
                      @click=${0}
                      .label=${0}
                      .path=${0}
                    ></ha-icon-button>
                  </div>`),this._openFilePicker,this.icon||$,this.value,this._clearValue,(null===(a=this.hass)||void 0===a?void 0:a.localize("ui.common.delete"))||"Delete",_):(this.value instanceof FileList?Array.from(this.value):(0,h.r)(this.value)).map((e=>{var t;return(0,r.dy)(x||(x=w`<div class="row">
                        <div class="value" @click=${0}>
                          <ha-svg-icon
                            .path=${0}
                          ></ha-svg-icon>
                          ${0} - ${0}
                        </div>
                        <ha-icon-button
                          @click=${0}
                          .label=${0}
                          .path=${0}
                        ></ha-icon-button>
                      </div>`),this._openFilePicker,this.icon||$,e.name,(0,u.d)(e.size),this._clearValue,(null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.delete"))||"Delete",_)})):(0,r.dy)(g||(g=w`<ha-svg-icon
                    class="big-icon"
                    .path=${0}
                  ></ha-svg-icon>
                  <ha-button unelevated @click=${0}>
                    ${0}
                  </ha-button>
                  <span class="secondary"
                    >${0}</span
                  >
                  <span class="supports">${0}</span>`),this.icon||$,this._openFilePicker,this.label||(null===(i=this.hass)||void 0===i?void 0:i.localize("ui.components.file-upload.label")),this.secondary||(null===(o=this.hass)||void 0===o?void 0:o.localize("ui.components.file-upload.secondary")),this.supports),this.accept,this.multiple,this._handleFilePicked))}},{kind:"method",key:"_openFilePicker",value:function(){var e;null===(e=this._input)||void 0===e||e.click()}},{kind:"method",key:"_handleDrop",value:function(e){var t;e.preventDefault(),e.stopPropagation(),null!==(t=e.dataTransfer)&&void 0!==t&&t.files&&(0,d.B)(this,"file-picked",{files:this.multiple||1===e.dataTransfer.files.length?Array.from(e.dataTransfer.files):[e.dataTransfer.files[0]]}),this._drag=!1}},{kind:"method",key:"_handleDragStart",value:function(e){e.preventDefault(),e.stopPropagation(),this._drag=!0}},{kind:"method",key:"_handleDragEnd",value:function(e){e.preventDefault(),e.stopPropagation(),this._drag=!1}},{kind:"method",key:"_handleFilePicked",value:function(e){0!==e.target.files.length&&(this.value=e.target.files,(0,d.B)(this,"file-picked",{files:e.target.files}))}},{kind:"method",key:"_clearValue",value:function(e){e.preventDefault(),this._input.value="",this.value=void 0,(0,d.B)(this,"change"),(0,d.B)(this,"files-cleared")}},{kind:"field",static:!0,key:"styles",value(){return(0,r.iv)(y||(y=w`
    :host {
      display: block;
      height: 240px;
    }
    :host([disabled]) {
      pointer-events: none;
      color: var(--disabled-text-color);
    }
    .container {
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border: solid 1px
        var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
      border-radius: var(--mdc-shape-small, 4px);
      height: 100%;
    }
    label.container {
      border: dashed 1px
        var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
      cursor: pointer;
    }
    .container .uploading {
      display: flex;
      flex-direction: column;
      width: 100%;
      align-items: flex-start;
      padding: 0 32px;
      box-sizing: border-box;
    }
    :host([disabled]) .container {
      border-color: var(--disabled-color);
    }
    label:hover,
    label.dragged {
      border-style: solid;
    }
    label.dragged {
      border-color: var(--primary-color);
    }
    .dragged:before {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      background-color: var(--primary-color);
      content: "";
      opacity: var(--dark-divider-opacity);
      pointer-events: none;
      border-radius: var(--mdc-shape-small, 4px);
    }
    label.value {
      cursor: default;
    }
    label.value.multiple {
      justify-content: unset;
      overflow: auto;
    }
    .highlight {
      color: var(--primary-color);
    }
    ha-button {
      margin-bottom: 4px;
    }
    .supports {
      color: var(--secondary-text-color);
      font-size: 12px;
    }
    :host([disabled]) .secondary {
      color: var(--disabled-text-color);
    }
    input.file {
      display: none;
    }
    .value {
      cursor: pointer;
    }
    .value ha-svg-icon {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
    .big-icon {
      --mdc-icon-size: 48px;
      margin-bottom: 8px;
    }
    ha-button {
      --mdc-button-outline-color: var(--primary-color);
      --mdc-icon-button-size: 24px;
    }
    mwc-linear-progress {
      width: 100%;
      padding: 8px 32px;
      box-sizing: border-box;
    }
    .header {
      font-weight: 500;
    }
    .progress {
      color: var(--secondary-text-color);
    }
    button.link {
      background: none;
      border: none;
      padding: 0;
      font-size: 14px;
      color: var(--primary-color);
      text-decoration: underline;
      cursor: pointer;
    }
  `))}}]}}),r.oi);t()}catch(p){t(p)}}))},96123:function(e,t,i){i.d(t,{Y:()=>a,c:()=>o});i(52247),i(40251);const o=async(e,t)=>{const i=new FormData;i.append("file",t);const o=await e.fetchWithAuth("/api/file_upload",{method:"POST",body:i});if(413===o.status)throw new Error(`Uploaded file is too large (${t.name})`);if(200!==o.status)throw new Error("Unknown error");return(await o.json()).file_id},a=async(e,t)=>e.callApi("DELETE","file_upload",{file_id:t})},81054:function(e,t,i){i.d(t,{js:()=>a,rY:()=>o});i(19083),i(71695),i(40251),i(92519),i(42179),i(89256),i(24931),i(88463),i(57449),i(19814),i(61006),i(47021),i(99642);const o=e=>e.data,a=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])},4557:function(e,t,i){i.d(t,{D9:()=>l,Ys:()=>r,g7:()=>s});i(71695),i(19423),i(40251),i(47021);var o=i(11297);const a=()=>Promise.all([i.e("7442"),i.e("4913")]).then(i.bind(i,51046)),n=(e,t,i)=>new Promise((n=>{const r=t.cancel,s=t.confirm;(0,o.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:a,dialogParams:Object.assign(Object.assign(Object.assign({},t),i),{},{cancel:()=>{n(!(null==i||!i.prompt)&&null),r&&r()},confirm:e=>{n(null==i||!i.prompt||e),s&&s(e)}})})})),r=(e,t)=>n(e,t),s=(e,t)=>n(e,t,{confirmation:!0}),l=(e,t)=>n(e,t,{prompt:!0})},32422:function(e,t,i){var o=i(73577),a=i(72621),n=(i(19083),i(71695),i(61006),i(39527),i(99790),i(67670),i(13334),i(47021),i(57243)),r=i(50778),s=i(35359),l=i(27486),d=i(82283),c=(i(92500),i(89654),i(10508),i(20552)),h=i(19799),u=i(23111);let v,p,f,b,k=e=>e,g=((0,o.Z)([(0,r.Mo)("ha-ripple")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:"attachableTouchController",value(){return new h.J(this,this._onTouchControlChange.bind(this))}},{kind:"method",key:"attach",value:function(e){(0,a.Z)(i,"attach",this,3)([e]),this.attachableTouchController.attach(e)}},{kind:"method",key:"detach",value:function(){(0,a.Z)(i,"detach",this,3)([]),this.attachableTouchController.detach()}},{kind:"field",key:"_handleTouchEnd",value(){return()=>{this.disabled||(0,a.Z)(i,"endPressAnimation",this,3)([])}}},{kind:"method",key:"_onTouchControlChange",value:function(e,t){null==e||e.removeEventListener("touchend",this._handleTouchEnd),null==t||t.addEventListener("touchend",this._handleTouchEnd)}},{kind:"field",static:!0,key:"styles",value(){return[...(0,a.Z)(i,"styles",this),(0,n.iv)(v||(v=k`
      :host {
        --md-ripple-hover-opacity: var(--ha-ripple-hover-opacity, 0.08);
        --md-ripple-pressed-opacity: var(--ha-ripple-pressed-opacity, 0.12);
        --md-ripple-hover-color: var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );
        --md-ripple-pressed-color: var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );
      }
    `))]}}]}}),u.M),e=>e);(0,o.Z)([(0,r.Mo)("ha-tab")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"active",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)()],key:"name",value:void 0},{kind:"method",key:"render",value:function(){return(0,n.dy)(p||(p=g`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${0}
        aria-label=${0}
        @keydown=${0}
      >
        ${0}
        <span class="name">${0}</span>
        <ha-ripple></ha-ripple>
      </div>
    `),this.active,(0,c.o)(this.name),this._handleKeyDown,this.narrow?(0,n.dy)(f||(f=g`<slot name="icon"></slot>`)):"",this.name)}},{kind:"method",key:"_handleKeyDown",value:function(e){"Enter"===e.key&&e.target.click()}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(b||(b=g`
    div {
      padding: 0 32px;
      display: flex;
      flex-direction: column;
      text-align: center;
      box-sizing: border-box;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: var(--header-height);
      cursor: pointer;
      position: relative;
      outline: none;
    }

    .name {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
    }

    :host([active]) {
      color: var(--primary-color);
    }

    :host(:not([narrow])[active]) div {
      border-bottom: 2px solid var(--primary-color);
    }

    :host([narrow]) {
      min-width: 0;
      display: flex;
      justify-content: center;
      overflow: hidden;
    }

    :host([narrow]) div {
      padding: 0 4px;
    }

    div:focus-visible:before {
      position: absolute;
      display: block;
      content: "";
      inset: 0;
      background-color: var(--secondary-text-color);
      opacity: 0.08;
    }
  `))}}]}}),n.oi);var m=i(66193),x=(i(36993),i(24785)),y=i(49672);const w=(e,t)=>!t.component||(0,x.r)(t.component).some((t=>(0,y.p)(e,t))),_=(e,t)=>!t.not_component||!(0,x.r)(t.not_component).some((t=>(0,y.p)(e,t))),$=e=>e.core,j=(e,t)=>(e=>e.advancedOnly)(t)&&!(e=>{var t;return null===(t=e.userData)||void 0===t?void 0:t.showAdvanced})(e);let C,z,P,B,F,D,T,H,L,M,V,A=e=>e;(0,o.Z)([(0,r.Mo)("hass-tabs-subpage")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"pane",value(){return!1}},{kind:"field",decorators:[(0,r.SB)()],key:"_activeTab",value:void 0},{kind:"field",decorators:[(0,d.i)(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return(0,l.Z)(((e,t,i,o,a,r)=>{const s=e.filter((e=>((e,t)=>($(t)||w(e,t))&&!j(e,t)&&_(e,t))(this.hass,e)));if(s.length<2){if(1===s.length){const e=s[0];return[e.translationKey?r(e.translationKey):e.name]}return[""]}return s.map((e=>(0,n.dy)(C||(C=A`
          <a href=${0}>
            <ha-tab
              .hass=${0}
              .active=${0}
              .narrow=${0}
              .name=${0}
            >
              ${0}
            </ha-tab>
          </a>
        `),e.path,this.hass,e.path===(null==t?void 0:t.path),this.narrow,e.translationKey?r(e.translationKey):e.name,e.iconPath?(0,n.dy)(z||(z=A`<ha-svg-icon
                    slot="icon"
                    .path=${0}
                  ></ha-svg-icon>`),e.iconPath):"")))}))}},{kind:"method",key:"willUpdate",value:function(e){e.has("route")&&(this._activeTab=this.tabs.find((e=>`${this.route.prefix}${this.route.path}`.includes(e.path)))),(0,a.Z)(i,"willUpdate",this,3)([e])}},{kind:"method",key:"render",value:function(){var e;const t=this._getTabs(this.tabs,this._activeTab,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),i=t.length>1;return(0,n.dy)(P||(P=A`
      <div class="toolbar">
        <slot name="toolbar">
          <div class="toolbar-content">
            ${0}
            ${0}
            ${0}
            <div id="toolbar-icon">
              <slot name="toolbar-icon"></slot>
            </div>
          </div>
        </slot>
        ${0}
      </div>
      <div class="container">
        ${0}
        <div
          class="content ha-scrollbar ${0}"
          @scroll=${0}
        >
          <slot></slot>
        </div>
      </div>
      <div id="fab" class=${0}>
        <slot name="fab"></slot>
      </div>
    `),this.mainPage||!this.backPath&&null!==(e=history.state)&&void 0!==e&&e.root?(0,n.dy)(B||(B=A`
                  <ha-menu-button
                    .hassio=${0}
                    .hass=${0}
                    .narrow=${0}
                  ></ha-menu-button>
                `),this.supervisor,this.hass,this.narrow):this.backPath?(0,n.dy)(F||(F=A`
                    <a href=${0}>
                      <ha-icon-button-arrow-prev
                        .hass=${0}
                      ></ha-icon-button-arrow-prev>
                    </a>
                  `),this.backPath,this.hass):(0,n.dy)(D||(D=A`
                    <ha-icon-button-arrow-prev
                      .hass=${0}
                      @click=${0}
                    ></ha-icon-button-arrow-prev>
                  `),this.hass,this._backTapped),this.narrow||!i?(0,n.dy)(T||(T=A`<div class="main-title">
                  <slot name="header">${0}</slot>
                </div>`),i?"":t[0]):"",i&&!this.narrow?(0,n.dy)(H||(H=A`<div id="tabbar">${0}</div>`),t):"",i&&this.narrow?(0,n.dy)(L||(L=A`<div id="tabbar" class="bottom-bar">${0}</div>`),t):"",this.pane?(0,n.dy)(M||(M=A`<div class="pane">
              <div class="shadow-container"></div>
              <div class="ha-scrollbar">
                <slot name="pane"></slot>
              </div>
            </div>`)):n.Ld,(0,s.$)({tabs:i}),this._saveScrollPos,(0,s.$)({tabs:i}))}},{kind:"method",decorators:[(0,r.hO)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[m.$c,(0,n.iv)(V||(V=A`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }

        :host([narrow]) {
          width: 100%;
          position: fixed;
        }

        .container {
          display: flex;
          height: calc(100% - var(--header-height));
        }

        :host([narrow]) .container {
          height: 100%;
        }

        ha-menu-button {
          margin-right: 24px;
          margin-inline-end: 24px;
          margin-inline-start: initial;
        }

        .toolbar {
          font-size: 20px;
          height: var(--header-height);
          background-color: var(--sidebar-background-color);
          font-weight: 400;
          border-bottom: 1px solid var(--divider-color);
          box-sizing: border-box;
        }
        .toolbar-content {
          padding: 8px 12px;
          display: flex;
          align-items: center;
          height: 100%;
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar-content {
            padding: 4px;
          }
        }
        .toolbar a {
          color: var(--sidebar-text-color);
          text-decoration: none;
        }
        .bottom-bar a {
          width: 25%;
        }

        #tabbar {
          display: flex;
          font-size: 14px;
          overflow: hidden;
        }

        #tabbar > a {
          overflow: hidden;
          max-width: 45%;
        }

        #tabbar.bottom-bar {
          position: absolute;
          bottom: 0;
          left: 0;
          padding: 0 16px;
          box-sizing: border-box;
          background-color: var(--sidebar-background-color);
          border-top: 1px solid var(--divider-color);
          justify-content: space-around;
          z-index: 2;
          font-size: 12px;
          width: 100%;
          padding-bottom: env(safe-area-inset-bottom);
        }

        #tabbar:not(.bottom-bar) {
          flex: 1;
          justify-content: center;
        }

        :host(:not([narrow])) #toolbar-icon {
          min-width: 40px;
        }

        ha-menu-button,
        ha-icon-button-arrow-prev,
        ::slotted([slot="toolbar-icon"]) {
          display: flex;
          flex-shrink: 0;
          pointer-events: auto;
          color: var(--sidebar-icon-color);
        }

        .main-title {
          flex: 1;
          max-height: var(--header-height);
          line-height: 20px;
          color: var(--sidebar-text-color);
          margin: var(--main-title-margin, var(--margin-title));
        }

        .content {
          position: relative;
          width: calc(
            100% - env(safe-area-inset-left) - env(safe-area-inset-right)
          );
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
          margin-inline-start: env(safe-area-inset-left);
          margin-inline-end: env(safe-area-inset-right);
          overflow: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([narrow]) .content {
          height: calc(100% - var(--header-height));
          height: calc(
            100% - var(--header-height) - env(safe-area-inset-bottom)
          );
        }

        :host([narrow]) .content.tabs {
          height: calc(100% - 2 * var(--header-height));
          height: calc(
            100% - 2 * var(--header-height) - env(safe-area-inset-bottom)
          );
        }

        #fab {
          position: fixed;
          right: calc(16px + env(safe-area-inset-right));
          inset-inline-end: calc(16px + env(safe-area-inset-right));
          inset-inline-start: initial;
          bottom: calc(16px + env(safe-area-inset-bottom));
          z-index: 1;
          display: flex;
          flex-wrap: wrap;
          justify-content: flex-end;
          gap: 8px;
        }
        :host([narrow]) #fab.tabs {
          bottom: calc(84px + env(safe-area-inset-bottom));
        }
        #fab[is-wide] {
          bottom: 24px;
          right: 24px;
          inset-inline-end: 24px;
          inset-inline-start: initial;
        }

        .pane {
          border-right: 1px solid var(--divider-color);
          border-inline-end: 1px solid var(--divider-color);
          border-inline-start: initial;
          box-sizing: border-box;
          display: flex;
          flex: 0 0 var(--sidepane-width, 250px);
          width: var(--sidepane-width, 250px);
          flex-direction: column;
          position: relative;
        }
        .pane .ha-scrollbar {
          flex: 1;
        }
      `))]}}]}}),n.oi)},84120:function(e,t,i){i.d(t,{d:()=>o});i(49278),i(95078);const o=(e=0,t=2)=>{if(0===e)return"0 Bytes";t=t<0?0:t;const i=Math.floor(Math.log(e)/Math.log(1024));return`${parseFloat((e/1024**i).toFixed(t))} ${["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][i]}`}},71698:function(e,t,i){i.d(t,{q:()=>o});const o="2025.1.30.194235"},64111:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t),i.d(t,{KNXInfo:()=>$});var a=i(73577),n=(i(71695),i(40251),i(47021),i(57243)),r=i(50778),s=i(11297),l=(i(1192),i(32422),i(20095),i(58303)),d=(i(68565),i(96123)),c=i(81054),h=i(4557),u=i(57259),v=i(57586),p=i(71698),f=e([l]);l=(f.then?(await f)():f)[0];let b,k,g,m,x,y=e=>e;const w="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z",_=new v.r("info");let $=(0,a.Z)([(0,r.Mo)("knx-info")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_projectPassword",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_uploading",value(){return!1}},{kind:"field",decorators:[(0,r.SB)()],key:"_projectFile",value:void 0},{kind:"method",key:"render",value:function(){return(0,n.dy)(b||(b=y`
      <hass-tabs-subpage
        .hass=${0}
        .narrow=${0}
        .route=${0}
        .tabs=${0}
        .localizeFunc=${0}
      >
        <div class="columns">
          ${0}
          ${0}
          ${0}
        </div>
      </hass-tabs-subpage>
    `),this.hass,this.narrow,this.route,this.tabs,this.knx.localize,this._renderInfoCard(),this.knx.info.project?this._renderProjectDataCard(this.knx.info.project):n.Ld,this._renderProjectUploadCard())}},{kind:"method",key:"_renderInfoCard",value:function(){return(0,n.dy)(k||(k=y` <ha-card class="knx-info">
      <div class="card-content knx-info-section">
        <div class="knx-content-row header">${0}</div>

        <div class="knx-content-row">
          <div>XKNX Version</div>
          <div>${0}</div>
        </div>

        <div class="knx-content-row">
          <div>KNX-Frontend Version</div>
          <div>${0}</div>
        </div>

        <div class="knx-content-row">
          <div>${0}</div>
          <div>
            ${0}
          </div>
        </div>

        <div class="knx-content-row">
          <div>${0}</div>
          <div>${0}</div>
        </div>

        <div class="knx-bug-report">
          ${0}
          <a href="https://github.com/XKNX/knx-integration" target="_blank">xknx/knx-integration</a>
        </div>

        <div class="knx-bug-report">
          ${0}
          <a href="https://my.knx.org" target="_blank">my.knx.org</a>
        </div>
      </div>
    </ha-card>`),this.knx.localize("info_information_header"),this.knx.info.version,p.q,this.knx.localize("info_connected_to_bus"),this.hass.localize(this.knx.info.connected?"ui.common.yes":"ui.common.no"),this.knx.localize("info_individual_address"),this.knx.info.current_address,this.knx.localize("info_issue_tracker"),this.knx.localize("info_my_knx"))}},{kind:"method",key:"_renderProjectDataCard",value:function(e){return(0,n.dy)(g||(g=y`
      <ha-card class="knx-info">
          <div class="card-content knx-content">
            <div class="header knx-content-row">
              ${0}
            </div>
            <div class="knx-content-row">
              <div>${0}</div>
              <div>${0}</div>
            </div>
            <div class="knx-content-row">
              <div>${0}</div>
              <div>${0}</div>
            </div>
            <div class="knx-content-row">
              <div>${0}</div>
              <div>${0}</div>
            </div>
            <div class="knx-content-row">
              <div>${0}</div>
              <div>${0}</div>
            </div>
            <div class="knx-button-row">
              <ha-button
                class="knx-warning push-right"
                @click=${0}
                .disabled=${0}
                >
                ${0}
              </ha-button>
            </div>
          </div>
        </div>
      </ha-card>
    `),this.knx.localize("info_project_data_header"),this.knx.localize("info_project_data_name"),e.name,this.knx.localize("info_project_data_last_modified"),new Date(e.last_modified).toUTCString(),this.knx.localize("info_project_data_tool_version"),e.tool_version,this.knx.localize("info_project_data_xknxproject_version"),e.xknxproject_version,this._removeProject,this._uploading||!this.knx.info.project,this.knx.localize("info_project_delete"))}},{kind:"method",key:"_renderProjectUploadCard",value:function(){var e;return(0,n.dy)(m||(m=y` <ha-card class="knx-info">
      <div class="card-content knx-content">
        <div class="knx-content-row header">${0}</div>
        <div class="knx-content-row">${0}</div>
        <div class="knx-content-row">
          <ha-file-upload
            .hass=${0}
            accept=".knxproj, .knxprojarchive"
            .icon=${0}
            .label=${0}
            .value=${0}
            .uploading=${0}
            @file-picked=${0}
          ></ha-file-upload>
        </div>
        <div class="knx-content-row">
          <ha-selector-text
            .hass=${0}
            .value=${0}
            .label=${0}
            .selector=${0}
            .required=${0}
            @value-changed=${0}
          >
          </ha-selector-text>
        </div>
        <div class="knx-button-row">
          <ha-button
            class="push-right"
            @click=${0}
            .disabled=${0}
            >${0}</ha-button
          >
        </div>
      </div>
    </ha-card>`),this.knx.localize("info_project_file_header"),this.knx.localize("info_project_upload_description"),this.hass,w,this.knx.localize("info_project_file"),null===(e=this._projectFile)||void 0===e?void 0:e.name,this._uploading,this._filePicked,this.hass,this._projectPassword||"",this.hass.localize("ui.login-form.password"),{text:{multiline:!1,type:"password"}},!1,this._passwordChanged,this._uploadFile,this._uploading||!this._projectFile,this.hass.localize("ui.common.submit"))}},{kind:"method",key:"_filePicked",value:function(e){this._projectFile=e.detail.files[0]}},{kind:"method",key:"_passwordChanged",value:function(e){this._projectPassword=e.detail.value}},{kind:"method",key:"_uploadFile",value:async function(e){const t=this._projectFile;if(void 0===t)return;let i;this._uploading=!0;try{const e=await(0,d.c)(this.hass,t);await(0,u.cO)(this.hass,e,this._projectPassword||"")}catch(o){i=o,(0,h.Ys)(this,{title:"Upload failed",text:(0,c.js)(o)})}finally{i||(this._projectFile=void 0,this._projectPassword=void 0),this._uploading=!1,(0,s.B)(this,"knx-reload")}}},{kind:"method",key:"_removeProject",value:async function(e){if(await(0,h.g7)(this,{text:this.knx.localize("info_project_delete")}))try{await(0,u.Hk)(this.hass)}catch(t){(0,h.Ys)(this,{title:"Deletion failed",text:(0,c.js)(t)})}finally{(0,s.B)(this,"knx-reload")}else _.debug("User cancelled deletion")}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(x||(x=y`
    .columns {
      display: flex;
      justify-content: center;
    }

    @media screen and (max-width: 1232px) {
      .columns {
        flex-direction: column;
      }

      .knx-button-row {
        margin-top: 20px;
      }

      .knx-info {
        margin-right: 8px;
      }
    }

    @media screen and (min-width: 1233px) {
      .knx-button-row {
        margin-top: auto;
      }

      .knx-info {
        width: 400px;
      }
    }

    .knx-info {
      margin-left: 8px;
      margin-top: 8px;
    }

    .knx-content {
      display: flex;
      flex-direction: column;
      height: 100%;
      box-sizing: border-box;
    }

    .knx-content-row {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }

    .knx-content-row > div:nth-child(2) {
      margin-left: 1rem;
    }

    .knx-button-row {
      display: flex;
      flex-direction: row;
      vertical-align: bottom;
      padding-top: 16px;
    }

    .push-left {
      margin-right: auto;
    }

    .push-right {
      margin-left: auto;
    }

    .knx-warning {
      --mdc-theme-primary: var(--error-color);
    }

    .knx-project-description {
      margin-top: -8px;
      padding: 0px 16px 16px;
    }

    .knx-delete-project-button {
      position: absolute;
      bottom: 0;
      right: 0;
    }

    .knx-bug-report {
      margin-top: 20px;

      a {
        text-decoration: none;
      }
    }

    .header {
      color: var(--ha-card-header-color, --primary-text-color);
      font-family: var(--ha-card-header-font-family, inherit);
      font-size: var(--ha-card-header-font-size, 24px);
      letter-spacing: -0.012em;
      line-height: 48px;
      padding: -4px 16px 16px;
      display: inline-block;
      margin-block-start: 0px;
      margin-block-end: 4px;
      font-weight: normal;
    }

    ha-file-upload,
    ha-selector-text {
      width: 100%;
      margin-top: 8px;
    }
  `))}}]}}),n.oi);o()}catch(b){o(b)}}))}}]);
//# sourceMappingURL=8268.ddc59cdeaf67ed3a.js.map