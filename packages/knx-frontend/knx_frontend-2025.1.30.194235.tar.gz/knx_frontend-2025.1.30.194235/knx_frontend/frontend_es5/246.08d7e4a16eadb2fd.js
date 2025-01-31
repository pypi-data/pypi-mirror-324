"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["246"],{32422:function(e,t,a){var o=a(73577),i=a(72621),r=(a(19083),a(71695),a(61006),a(39527),a(99790),a(67670),a(13334),a(47021),a(57243)),n=a(50778),s=a(35359),l=a(27486),d=a(82283),c=(a(92500),a(89654),a(10508),a(20552)),h=a(19799),v=a(23111);let b,u,p,f,k=e=>e,y=((0,o.Z)([(0,n.Mo)("ha-ripple")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",key:"attachableTouchController",value(){return new h.J(this,this._onTouchControlChange.bind(this))}},{kind:"method",key:"attach",value:function(e){(0,i.Z)(a,"attach",this,3)([e]),this.attachableTouchController.attach(e)}},{kind:"method",key:"detach",value:function(){(0,i.Z)(a,"detach",this,3)([]),this.attachableTouchController.detach()}},{kind:"field",key:"_handleTouchEnd",value(){return()=>{this.disabled||(0,i.Z)(a,"endPressAnimation",this,3)([])}}},{kind:"method",key:"_onTouchControlChange",value:function(e,t){null==e||e.removeEventListener("touchend",this._handleTouchEnd),null==t||t.addEventListener("touchend",this._handleTouchEnd)}},{kind:"field",static:!0,key:"styles",value(){return[...(0,i.Z)(a,"styles",this),(0,r.iv)(b||(b=k`
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
    `))]}}]}}),v.M),e=>e);(0,o.Z)([(0,n.Mo)("ha-tab")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"active",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)()],key:"name",value:void 0},{kind:"method",key:"render",value:function(){return(0,r.dy)(u||(u=y`
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
    `),this.active,(0,c.o)(this.name),this._handleKeyDown,this.narrow?(0,r.dy)(p||(p=y`<slot name="icon"></slot>`)):"",this.name)}},{kind:"method",key:"_handleKeyDown",value:function(e){"Enter"===e.key&&e.target.click()}},{kind:"field",static:!0,key:"styles",value(){return(0,r.iv)(f||(f=y`
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
  `))}}]}}),r.oi);var m=a(66193),g=(a(36993),a(24785)),x=a(49672);const w=(e,t)=>!t.component||(0,g.r)(t.component).some((t=>(0,x.p)(e,t))),$=(e,t)=>!t.not_component||!(0,g.r)(t.not_component).some((t=>(0,x.p)(e,t))),C=e=>e.core,_=(e,t)=>(e=>e.advancedOnly)(t)&&!(e=>{var t;return null===(t=e.userData)||void 0===t?void 0:t.showAdvanced})(e);let T,z,P,Z,B,E,j,K,F,S,M,O=e=>e;(0,o.Z)([(0,n.Mo)("hass-tabs-subpage")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"pane",value(){return!1}},{kind:"field",decorators:[(0,n.SB)()],key:"_activeTab",value:void 0},{kind:"field",decorators:[(0,d.i)(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return(0,l.Z)(((e,t,a,o,i,n)=>{const s=e.filter((e=>((e,t)=>(C(t)||w(e,t))&&!_(e,t)&&$(e,t))(this.hass,e)));if(s.length<2){if(1===s.length){const e=s[0];return[e.translationKey?n(e.translationKey):e.name]}return[""]}return s.map((e=>(0,r.dy)(T||(T=O`
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
        `),e.path,this.hass,e.path===(null==t?void 0:t.path),this.narrow,e.translationKey?n(e.translationKey):e.name,e.iconPath?(0,r.dy)(z||(z=O`<ha-svg-icon
                    slot="icon"
                    .path=${0}
                  ></ha-svg-icon>`),e.iconPath):"")))}))}},{kind:"method",key:"willUpdate",value:function(e){e.has("route")&&(this._activeTab=this.tabs.find((e=>`${this.route.prefix}${this.route.path}`.includes(e.path)))),(0,i.Z)(a,"willUpdate",this,3)([e])}},{kind:"method",key:"render",value:function(){var e;const t=this._getTabs(this.tabs,this._activeTab,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),a=t.length>1;return(0,r.dy)(P||(P=O`
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
    `),this.mainPage||!this.backPath&&null!==(e=history.state)&&void 0!==e&&e.root?(0,r.dy)(Z||(Z=O`
                  <ha-menu-button
                    .hassio=${0}
                    .hass=${0}
                    .narrow=${0}
                  ></ha-menu-button>
                `),this.supervisor,this.hass,this.narrow):this.backPath?(0,r.dy)(B||(B=O`
                    <a href=${0}>
                      <ha-icon-button-arrow-prev
                        .hass=${0}
                      ></ha-icon-button-arrow-prev>
                    </a>
                  `),this.backPath,this.hass):(0,r.dy)(E||(E=O`
                    <ha-icon-button-arrow-prev
                      .hass=${0}
                      @click=${0}
                    ></ha-icon-button-arrow-prev>
                  `),this.hass,this._backTapped),this.narrow||!a?(0,r.dy)(j||(j=O`<div class="main-title">
                  <slot name="header">${0}</slot>
                </div>`),a?"":t[0]):"",a&&!this.narrow?(0,r.dy)(K||(K=O`<div id="tabbar">${0}</div>`),t):"",a&&this.narrow?(0,r.dy)(F||(F=O`<div id="tabbar" class="bottom-bar">${0}</div>`),t):"",this.pane?(0,r.dy)(S||(S=O`<div class="pane">
              <div class="shadow-container"></div>
              <div class="ha-scrollbar">
                <slot name="pane"></slot>
              </div>
            </div>`)):r.Ld,(0,s.$)({tabs:a}),this._saveScrollPos,(0,s.$)({tabs:a}))}},{kind:"method",decorators:[(0,n.hO)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[m.$c,(0,r.iv)(M||(M=O`
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
      `))]}}]}}),r.oi)},99187:function(e,t,a){a.r(t),a.d(t,{KNXError:()=>d});var o=a(73577),i=(a(71695),a(47021),a(57243)),r=a(50778),n=a(80155);a(32422),a(3035);let s,l=e=>e,d=(0,o.Z)([(0,r.Mo)("knx-error")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"method",key:"render",value:function(){var e,t;const a=null!==(e=null===(t=n.E.history.state)||void 0===t?void 0:t.message)&&void 0!==e?e:"Unknown error";return(0,i.dy)(s||(s=l`
      <hass-error-screen
        .hass=${0}
        .error=${0}
        .toolbar=${0}
        .rootnav=${0}
        .narrow=${0}
      ></hass-error-screen>
    `),this.hass,a,!0,!1,this.narrow)}}]}}),i.oi)}}]);
//# sourceMappingURL=246.08d7e4a16eadb2fd.js.map