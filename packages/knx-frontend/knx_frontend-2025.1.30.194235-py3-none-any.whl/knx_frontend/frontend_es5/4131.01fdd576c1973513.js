"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["4131"],{24785:function(t,e,o){function i(t){return null==t||Array.isArray(t)?t:[t]}o.d(e,{r:()=>i})},49672:function(t,e,o){o.d(e,{p:()=>i});o(19083),o(61006);const i=(t,e)=>t&&t.config.components.includes(e)},82283:function(t,e,o){o.d(e,{i:()=>a});const i=(0,o(92492).P)((t=>{history.replaceState({scrollPosition:t},"")}),300),a=t=>e=>({kind:"method",placement:"prototype",key:e.key,descriptor:{set(t){i(t),this[`__${String(e.key)}`]=t},get(){var t;return this[`__${String(e.key)}`]||(null===(t=history.state)||void 0===t?void 0:t.scrollPosition)},enumerable:!0,configurable:!0},finisher(o){const i=o.prototype.connectedCallback;o.prototype.connectedCallback=function(){i.call(this);const o=this[e.key];o&&this.updateComplete.then((()=>{const e=this.renderRoot.querySelector(t);e&&setTimeout((()=>{e.scrollTop=o}),0)}))}}})},92492:function(t,e,o){o.d(e,{P:()=>i});o(71695),o(47021);const i=(t,e,o=!0,i=!0)=>{let a,n=0;const r=(...r)=>{const s=()=>{n=!1===o?0:Date.now(),a=void 0,t(...r)},l=Date.now();n||!1!==o||(n=l);const d=e-(l-n);d<=0||d>e?(a&&(clearTimeout(a),a=void 0),n=l,t(...r)):a||!1===i||(a=window.setTimeout(s,d))};return r.cancel=()=>{clearTimeout(a),a=void 0,n=0},r}},92500:function(t,e,o){o.r(e),o.d(e,{HaIconButtonArrowPrev:()=>d});var i=o(73577),a=(o(71695),o(47021),o(57243)),n=o(50778),r=o(80155);o(59897);let s,l=t=>t;let d=(0,i.Z)([(0,n.Mo)("ha-icon-button-arrow-prev")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_icon",value(){return"rtl"===r.E.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}},{kind:"method",key:"render",value:function(){var t;return(0,a.dy)(s||(s=l`
      <ha-icon-button
        .disabled=${0}
        .label=${0}
        .path=${0}
      ></ha-icon-button>
    `),this.disabled,this.label||(null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.back"))||"Back",this._icon)}}]}}),a.oi)},59897:function(t,e,o){o.r(e),o.d(e,{HaIconButton:()=>u});var i=o(73577),a=(o(71695),o(47021),o(74269),o(57243)),n=o(50778),r=o(20552);o(10508);let s,l,d,c,h=t=>t,u=(0,i.Z)([(0,n.Mo)("ha-icon-button")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"path",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:String,attribute:"aria-haspopup"})],key:"ariaHasPopup",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"hide-title",type:Boolean})],key:"hideTitle",value(){return!1}},{kind:"field",decorators:[(0,n.IO)("mwc-icon-button",!0)],key:"_button",value:void 0},{kind:"method",key:"focus",value:function(){var t;null===(t=this._button)||void 0===t||t.focus()}},{kind:"field",static:!0,key:"shadowRootOptions",value(){return{mode:"open",delegatesFocus:!0}}},{kind:"method",key:"render",value:function(){return(0,a.dy)(s||(s=h`
      <mwc-icon-button
        aria-label=${0}
        title=${0}
        aria-haspopup=${0}
        .disabled=${0}
      >
        ${0}
      </mwc-icon-button>
    `),(0,r.o)(this.label),(0,r.o)(this.hideTitle?void 0:this.label),(0,r.o)(this.ariaHasPopup),this.disabled,this.path?(0,a.dy)(l||(l=h`<ha-svg-icon .path=${0}></ha-svg-icon>`),this.path):(0,a.dy)(d||(d=h`<slot></slot>`)))}},{kind:"field",static:!0,key:"styles",value(){return(0,a.iv)(c||(c=h`
    :host {
      display: inline-block;
      outline: none;
    }
    :host([disabled]) {
      pointer-events: none;
    }
    mwc-icon-button {
      --mdc-theme-on-primary: currentColor;
      --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
    }
  `))}}]}}),a.oi)},89654:function(t,e,o){var i=o(73577),a=o(72621),n=(o(52247),o(71695),o(47021),o(57243)),r=o(50778),s=o(11297);o(19423);class l{constructor(){this.notifications=void 0,this.notifications={}}processMessage(t){if("removed"===t.type)for(const e of Object.keys(t.notifications))delete this.notifications[e];else this.notifications=Object.assign(Object.assign({},this.notifications),t.notifications);return Object.values(this.notifications)}}o(59897);let d,c,h,u=t=>t;(0,i.Z)([(0,r.Mo)("ha-menu-button")],(function(t,e){class o extends e{constructor(...e){super(...e),t(this)}}return{F:o,d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"hassio",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_hasNotifications",value(){return!1}},{kind:"field",decorators:[(0,r.SB)()],key:"_show",value(){return!1}},{kind:"field",key:"_alwaysVisible",value(){return!1}},{kind:"field",key:"_attachNotifOnConnect",value(){return!1}},{kind:"field",key:"_unsubNotifications",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.Z)(o,"connectedCallback",this,3)([]),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.Z)(o,"disconnectedCallback",this,3)([]),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}},{kind:"method",key:"render",value:function(){if(!this._show)return n.Ld;const t=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return(0,n.dy)(d||(d=u`
      <ha-icon-button
        .label=${0}
        .path=${0}
        @click=${0}
      ></ha-icon-button>
      ${0}
    `),this.hass.localize("ui.sidebar.sidebar_toggle"),"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z",this._toggleMenu,t?(0,n.dy)(c||(c=u`<div class="dot"></div>`)):"")}},{kind:"method",key:"firstUpdated",value:function(t){(0,a.Z)(o,"firstUpdated",this,3)([t]),this.hassio&&(this._alwaysVisible=(Number(window.parent.frontendVersion)||0)<20190710)}},{kind:"method",key:"willUpdate",value:function(t){if((0,a.Z)(o,"willUpdate",this,3)([t]),!t.has("narrow")&&!t.has("hass"))return;const e=t.has("hass")?t.get("hass"):this.hass,i=(t.has("narrow")?t.get("narrow"):this.narrow)||"always_hidden"===(null==e?void 0:e.dockedSidebar),n=this.narrow||"always_hidden"===this.hass.dockedSidebar;this.hasUpdated&&i===n||(this._show=n||this._alwaysVisible,n?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}},{kind:"method",key:"_subscribeNotifications",value:function(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=((t,e)=>{const o=new l,i=t.subscribeMessage((t=>e(o.processMessage(t))),{type:"persistent_notification/subscribe"});return()=>{i.then((t=>null==t?void 0:t()))}})(this.hass.connection,(t=>{this._hasNotifications=t.length>0}))}},{kind:"method",key:"_toggleMenu",value:function(){(0,s.B)(this,"hass-toggle-menu")}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(h||(h=u`
    :host {
      position: relative;
    }
    .dot {
      pointer-events: none;
      position: absolute;
      background-color: var(--accent-color);
      width: 12px;
      height: 12px;
      top: 9px;
      right: 7px;
      inset-inline-end: 7px;
      inset-inline-start: initial;
      border-radius: 50%;
      border: 2px solid var(--app-header-background-color);
    }
  `))}}]}}),n.oi)},10508:function(t,e,o){o.r(e),o.d(e,{HaSvgIcon:()=>h});var i=o(73577),a=(o(71695),o(47021),o(57243)),n=o(50778);let r,s,l,d,c=t=>t,h=(0,i.Z)([(0,n.Mo)("ha-svg-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.Cb)()],key:"path",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"secondaryPath",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"viewBox",value:void 0},{kind:"method",key:"render",value:function(){return(0,a.YP)(r||(r=c`
    <svg
      viewBox=${0}
      preserveAspectRatio="xMidYMid meet"
      focusable="false"
      role="img"
      aria-hidden="true"
    >
      <g>
        ${0}
        ${0}
      </g>
    </svg>`),this.viewBox||"0 0 24 24",this.path?(0,a.YP)(s||(s=c`<path class="primary-path" d=${0}></path>`),this.path):a.Ld,this.secondaryPath?(0,a.YP)(l||(l=c`<path class="secondary-path" d=${0}></path>`),this.secondaryPath):a.Ld)}},{kind:"field",static:!0,key:"styles",value(){return(0,a.iv)(d||(d=c`
    :host {
      display: var(--ha-icon-display, inline-flex);
      align-items: center;
      justify-content: center;
      position: relative;
      vertical-align: middle;
      fill: var(--icon-primary-color, currentcolor);
      width: var(--mdc-icon-size, 24px);
      height: var(--mdc-icon-size, 24px);
    }
    svg {
      width: 100%;
      height: 100%;
      pointer-events: none;
      display: block;
    }
    path.primary-path {
      opacity: var(--icon-primary-opactity, 1);
    }
    path.secondary-path {
      fill: var(--icon-secondary-color, currentcolor);
      opacity: var(--icon-secondary-opactity, 0.5);
    }
  `))}}]}}),a.oi)},66193:function(t,e,o){o.d(e,{$c:()=>f,Qx:()=>h,k1:()=>c,yu:()=>u});var i=o(57243);let a,n,r,s,l,d=t=>t;const c=(0,i.iv)(a||(a=d`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
    outline: none;
  }
`)),h=(0,i.iv)(n||(n=d`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
    margin-inline-start: 20px;
    margin-inline-end: initial;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  ha-button.warning,
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  ${0}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`),c),u=(0,i.iv)(r||(r=d`
  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-max-width: min(600px, 95vw);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --vertical-align-dialog: flex-end;
      --ha-dialog-border-radius: 0;
    }
  }
  mwc-button.warning,
  ha-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`)),f=(0,i.iv)(s||(s=d`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`));(0,i.iv)(l||(l=d`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`))}}]);
//# sourceMappingURL=4131.01fdd576c1973513.js.map