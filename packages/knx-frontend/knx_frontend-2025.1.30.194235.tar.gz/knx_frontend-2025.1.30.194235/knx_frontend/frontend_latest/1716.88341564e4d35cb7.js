export const ids=["1716"];export const modules={92500:function(t,i,e){e.r(i),e.d(i,{HaIconButtonArrowPrev:()=>r});var o=e(44249),n=e(57243),s=e(50778),a=e(80155);e(59897);let r=(0,o.Z)([(0,s.Mo)("ha-icon-button-arrow-prev")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_icon",value(){return"rtl"===a.E.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}},{kind:"method",key:"render",value:function(){return n.dy`
      <ha-icon-button
        .disabled=${this.disabled}
        .label=${this.label||this.hass?.localize("ui.common.back")||"Back"}
        .path=${this._icon}
      ></ha-icon-button>
    `}}]}}),n.oi)},59897:function(t,i,e){e.r(i),e.d(i,{HaIconButton:()=>r});var o=e(44249),n=(e(74269),e(57243)),s=e(50778),a=e(20552);e(10508);let r=(0,o.Z)([(0,s.Mo)("ha-icon-button")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:String})],key:"path",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:String})],key:"label",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:String,attribute:"aria-haspopup"})],key:"ariaHasPopup",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:"hide-title",type:Boolean})],key:"hideTitle",value(){return!1}},{kind:"field",decorators:[(0,s.IO)("mwc-icon-button",!0)],key:"_button",value:void 0},{kind:"method",key:"focus",value:function(){this._button?.focus()}},{kind:"field",static:!0,key:"shadowRootOptions",value(){return{mode:"open",delegatesFocus:!0}}},{kind:"method",key:"render",value:function(){return n.dy`
      <mwc-icon-button
        aria-label=${(0,a.o)(this.label)}
        title=${(0,a.o)(this.hideTitle?void 0:this.label)}
        aria-haspopup=${(0,a.o)(this.ariaHasPopup)}
        .disabled=${this.disabled}
      >
        ${this.path?n.dy`<ha-svg-icon .path=${this.path}></ha-svg-icon>`:n.dy`<slot></slot>`}
      </mwc-icon-button>
    `}},{kind:"field",static:!0,key:"styles",value(){return n.iv`
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
  `}}]}}),n.oi)},89654:function(t,i,e){var o=e(44249),n=e(72621),s=e(57243),a=e(50778),r=e(11297);class d{constructor(){this.notifications=void 0,this.notifications={}}processMessage(t){if("removed"===t.type)for(const i of Object.keys(t.notifications))delete this.notifications[i];else this.notifications={...this.notifications,...t.notifications};return Object.values(this.notifications)}}e(59897);(0,o.Z)([(0,a.Mo)("ha-menu-button")],(function(t,i){class e extends i{constructor(...i){super(...i),t(this)}}return{F:e,d:[{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"hassio",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_hasNotifications",value(){return!1}},{kind:"field",decorators:[(0,a.SB)()],key:"_show",value(){return!1}},{kind:"field",key:"_alwaysVisible",value(){return!1}},{kind:"field",key:"_attachNotifOnConnect",value(){return!1}},{kind:"field",key:"_unsubNotifications",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,n.Z)(e,"connectedCallback",this,3)([]),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}},{kind:"method",key:"disconnectedCallback",value:function(){(0,n.Z)(e,"disconnectedCallback",this,3)([]),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}},{kind:"method",key:"render",value:function(){if(!this._show)return s.Ld;const t=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return s.dy`
      <ha-icon-button
        .label=${this.hass.localize("ui.sidebar.sidebar_toggle")}
        .path=${"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"}
        @click=${this._toggleMenu}
      ></ha-icon-button>
      ${t?s.dy`<div class="dot"></div>`:""}
    `}},{kind:"method",key:"firstUpdated",value:function(t){(0,n.Z)(e,"firstUpdated",this,3)([t]),this.hassio&&(this._alwaysVisible=(Number(window.parent.frontendVersion)||0)<20190710)}},{kind:"method",key:"willUpdate",value:function(t){if((0,n.Z)(e,"willUpdate",this,3)([t]),!t.has("narrow")&&!t.has("hass"))return;const i=t.has("hass")?t.get("hass"):this.hass,o=(t.has("narrow")?t.get("narrow"):this.narrow)||"always_hidden"===i?.dockedSidebar,s=this.narrow||"always_hidden"===this.hass.dockedSidebar;this.hasUpdated&&o===s||(this._show=s||this._alwaysVisible,s?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}},{kind:"method",key:"_subscribeNotifications",value:function(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=((t,i)=>{const e=new d,o=t.subscribeMessage((t=>i(e.processMessage(t))),{type:"persistent_notification/subscribe"});return()=>{o.then((t=>t?.()))}})(this.hass.connection,(t=>{this._hasNotifications=t.length>0}))}},{kind:"method",key:"_toggleMenu",value:function(){(0,r.B)(this,"hass-toggle-menu")}},{kind:"field",static:!0,key:"styles",value(){return s.iv`
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
  `}}]}}),s.oi)},10508:function(t,i,e){e.r(i),e.d(i,{HaSvgIcon:()=>a});var o=e(44249),n=e(57243),s=e(50778);let a=(0,o.Z)([(0,s.Mo)("ha-svg-icon")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[(0,s.Cb)()],key:"path",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"secondaryPath",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"viewBox",value:void 0},{kind:"method",key:"render",value:function(){return n.YP`
    <svg
      viewBox=${this.viewBox||"0 0 24 24"}
      preserveAspectRatio="xMidYMid meet"
      focusable="false"
      role="img"
      aria-hidden="true"
    >
      <g>
        ${this.path?n.YP`<path class="primary-path" d=${this.path}></path>`:n.Ld}
        ${this.secondaryPath?n.YP`<path class="secondary-path" d=${this.secondaryPath}></path>`:n.Ld}
      </g>
    </svg>`}},{kind:"field",static:!0,key:"styles",value(){return n.iv`
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
  `}}]}}),n.oi)}};
//# sourceMappingURL=1716.88341564e4d35cb7.js.map