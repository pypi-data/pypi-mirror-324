"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6718"],{43527:function(e,t,i){var o=i(73577),n=i(72621),r=(i(71695),i(39527),i(41360),i(47021),i(22997),i(57243)),l=i(50778),a=i(80155),d=i(24067);let s,u,c=e=>e;(0,o.Z)([(0,l.Mo)("ha-button-menu")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:d.gA,value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,l.Cb)({attribute:"menu-corner"})],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,l.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,t;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(t=this._triggerButton)||void 0===t||t.focus()}},{kind:"method",key:"render",value:function(){return(0,r.dy)(s||(s=c`
      <div @click=${0}>
        <slot name="trigger" @slotchange=${0}></slot>
      </div>
      <mwc-menu
        .corner=${0}
        .menuCorner=${0}
        .fixed=${0}
        .multi=${0}
        .activatable=${0}
        .y=${0}
        .x=${0}
      >
        <slot></slot>
      </mwc-menu>
    `),this._handleClick,this._setTriggerAria,this.corner,this.menuCorner,this.fixed,this.multi,this.activatable,this.y,this.x)}},{kind:"method",key:"firstUpdated",value:function(e){(0,n.Z)(i,"firstUpdated",this,3)([e]),"rtl"===a.E.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"field",static:!0,key:"styles",value(){return(0,r.iv)(u||(u=c`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `))}}]}}),r.oi)},65099:function(e,t,i){i.r(t),i.d(t,{HaIconOverflowMenu:()=>y});var o=i(73577),n=(i(71695),i(13334),i(47021),i(14394),i(57243)),r=i(50778),l=i(35359),a=i(66193);i(43527),i(59897),i(74064),i(10508);let d,s,u,c,h,v,m,k,f,p=e=>e;let y=(0,o.Z)([(0,r.Mo)("ha-icon-overflow-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array})],key:"items",value(){return[]}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"method",key:"render",value:function(){return(0,n.dy)(d||(d=p`
      ${0}
    `),this.narrow?(0,n.dy)(s||(s=p` <!-- Collapsed representation for small screens -->
            <ha-button-menu
              @click=${0}
              @closed=${0}
              class="ha-icon-overflow-menu-overflow"
              absolute
            >
              <ha-icon-button
                .label=${0}
                .path=${0}
                slot="trigger"
              ></ha-icon-button>

              ${0}
            </ha-button-menu>`),this._handleIconOverflowMenuOpened,this._handleIconOverflowMenuClosed,this.hass.localize("ui.common.overflow_menu"),"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z",this.items.map((e=>e.divider?(0,n.dy)(u||(u=p`<li divider role="separator"></li>`)):(0,n.dy)(c||(c=p`<ha-list-item
                      graphic="icon"
                      ?disabled=${0}
                      @click=${0}
                      class=${0}
                    >
                      <div slot="graphic">
                        <ha-svg-icon
                          class=${0}
                          .path=${0}
                        ></ha-svg-icon>
                      </div>
                      ${0}
                    </ha-list-item> `),e.disabled,e.action,(0,l.$)({warning:Boolean(e.warning)}),(0,l.$)({warning:Boolean(e.warning)}),e.path,e.label)))):(0,n.dy)(h||(h=p`
            <!-- Icon representation for big screens -->
            ${0}
          `),this.items.map((e=>e.narrowOnly?"":e.divider?(0,n.dy)(v||(v=p`<div role="separator"></div>`)):(0,n.dy)(m||(m=p`<div>
                      ${0}
                      <ha-icon-button
                        @click=${0}
                        .label=${0}
                        .path=${0}
                        ?disabled=${0}
                      ></ha-icon-button>
                    </div> `),e.tooltip?(0,n.dy)(k||(k=p`<simple-tooltip
                            animation-delay="0"
                            position="left"
                          >
                            ${0}
                          </simple-tooltip>`),e.tooltip):"",e.action,e.label,e.path,e.disabled)))))}},{kind:"method",key:"_handleIconOverflowMenuOpened",value:function(e){e.stopPropagation();const t=this.closest(".mdc-data-table__row");t&&(t.style.zIndex="1")}},{kind:"method",key:"_handleIconOverflowMenuClosed",value:function(){const e=this.closest(".mdc-data-table__row");e&&(e.style.zIndex="")}},{kind:"get",static:!0,key:"styles",value:function(){return[a.Qx,(0,n.iv)(f||(f=p`
        :host {
          display: flex;
          justify-content: flex-end;
        }
        li[role="separator"] {
          border-bottom-color: var(--divider-color);
        }
        div[role="separator"] {
          border-right: 1px solid var(--divider-color);
          width: 1px;
        }
        ha-list-item[disabled] ha-svg-icon {
          color: var(--disabled-text-color);
        }
      `))]}}]}}),n.oi)}}]);
//# sourceMappingURL=6718.770be8b224218794.js.map