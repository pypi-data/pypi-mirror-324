"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5392"],{47899:function(e,t,r){r.a(e,(async function(e,a){try{r.d(t,{Bt:()=>l});r(19083);var i=r(69440),n=r(88977),o=r(50177),s=e([i]);i=(s.then?(await s)():s)[0];const d=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],l=e=>e.first_weekday===o.FS.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(e.language).weekInfo.firstDay%7:(0,n.L)(e.language)%7:d.includes(e.first_weekday)?d.indexOf(e.first_weekday):1;a()}catch(d){a(d)}}))},52258:function(e,t,r){r.a(e,(async function(e,a){try{r.d(t,{G:()=>l});var i=r(69440),n=r(27486),o=r(66045),s=e([i,o]);[i,o]=s.then?(await s)():s;const d=(0,n.Z)((e=>new Intl.RelativeTimeFormat(e.language,{numeric:"auto"}))),l=(e,t,r,a=!0)=>{const i=(0,o.W)(e,r,t);return a?d(t).format(i.value,i.unit):Intl.NumberFormat(t.language,{style:"unit",unit:i.unit,unitDisplay:"long"}).format(Math.abs(i.value))};a()}catch(d){a(d)}}))},66045:function(e,t,r){r.a(e,(async function(e,a){try{r.d(t,{W:()=>p});r(19423);var i=r(13809),n=r(29558),o=r(57829),s=r(47899),d=e([s]);s=(d.then?(await d)():d)[0];const c=1e3,u=60,h=60*u;function p(e,t=Date.now(),r,a={}){const d=Object.assign(Object.assign({},g),a||{}),l=(+e-+t)/c;if(Math.abs(l)<d.second)return{value:Math.round(l),unit:"second"};const p=l/u;if(Math.abs(p)<d.minute)return{value:Math.round(p),unit:"minute"};const v=l/h;if(Math.abs(v)<d.hour)return{value:Math.round(v),unit:"hour"};const m=new Date(e),b=new Date(t);m.setHours(0,0,0,0),b.setHours(0,0,0,0);const f=(0,i.j)(m,b);if(0===f)return{value:Math.round(v),unit:"hour"};if(Math.abs(f)<d.day)return{value:f,unit:"day"};const k=(0,s.Bt)(r),y=(0,n.z)(m,{weekStartsOn:k}),x=(0,n.z)(b,{weekStartsOn:k}),_=(0,o.p)(y,x);if(0===_)return{value:f,unit:"day"};if(Math.abs(_)<d.week)return{value:_,unit:"week"};const w=m.getFullYear()-b.getFullYear(),$=12*w+m.getMonth()-b.getMonth();return 0===$?{value:_,unit:"week"}:Math.abs($)<d.month||0===w?{value:$,unit:"month"}:{value:Math.round(w),unit:"year"}}const g={second:45,minute:45,hour:22,day:5,week:4,month:11};a()}catch(l){a(l)}}))},43527:function(e,t,r){var a=r(73577),i=r(72621),n=(r(71695),r(39527),r(41360),r(47021),r(22997),r(57243)),o=r(50778),s=r(80155),d=r(24067);let l,c,u=e=>e;(0,a.Z)([(0,o.Mo)("ha-button-menu")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",key:d.gA,value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,o.Cb)({attribute:"menu-corner"})],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,o.Cb)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,o.Cb)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,o.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,t;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(t=this._triggerButton)||void 0===t||t.focus()}},{kind:"method",key:"render",value:function(){return(0,n.dy)(l||(l=u`
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
    `),this._handleClick,this._setTriggerAria,this.corner,this.menuCorner,this.fixed,this.multi,this.activatable,this.y,this.x)}},{kind:"method",key:"firstUpdated",value:function(e){(0,i.Z)(r,"firstUpdated",this,3)([e]),"rtl"===s.E.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(c||(c=u`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `))}}]}}),n.oi)},1192:function(e,t,r){var a=r(73577),i=(r(71695),r(47021),r(57243)),n=r(50778);let o,s,d,l=e=>e;(0,a.Z)([(0,n.Mo)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"raised",value(){return!1}},{kind:"field",static:!0,key:"styles",value(){return(0,i.iv)(o||(o=l`
    :host {
      background: var(
        --ha-card-background,
        var(--card-background-color, white)
      );
      -webkit-backdrop-filter: var(--ha-card-backdrop-filter, none);
      backdrop-filter: var(--ha-card-backdrop-filter, none);
      box-shadow: var(--ha-card-box-shadow, none);
      box-sizing: border-box;
      border-radius: var(--ha-card-border-radius, 12px);
      border-width: var(--ha-card-border-width, 1px);
      border-style: solid;
      border-color: var(--ha-card-border-color, var(--divider-color, #e0e0e0));
      color: var(--primary-text-color);
      display: block;
      transition: all 0.3s ease-out;
      position: relative;
    }

    :host([raised]) {
      border: none;
      box-shadow: var(
        --ha-card-box-shadow,
        0px 2px 1px -1px rgba(0, 0, 0, 0.2),
        0px 1px 1px 0px rgba(0, 0, 0, 0.14),
        0px 1px 3px 0px rgba(0, 0, 0, 0.12)
      );
    }

    .card-header,
    :host ::slotted(.card-header) {
      color: var(--ha-card-header-color, var(--primary-text-color));
      font-family: var(--ha-card-header-font-family, inherit);
      font-size: var(--ha-card-header-font-size, 24px);
      letter-spacing: -0.012em;
      line-height: 48px;
      padding: 12px 16px 16px;
      display: block;
      margin-block-start: 0px;
      margin-block-end: 0px;
      font-weight: normal;
    }

    :host ::slotted(.card-content:not(:first-child)),
    slot:not(:first-child)::slotted(.card-content) {
      padding-top: 0px;
      margin-top: -8px;
    }

    :host ::slotted(.card-content) {
      padding: 16px;
    }

    :host ::slotted(.card-actions) {
      border-top: 1px solid var(--divider-color, #e8e8e8);
      padding: 5px 16px;
    }
  `))}},{kind:"method",key:"render",value:function(){return(0,i.dy)(s||(s=l`
      ${0}
      <slot></slot>
    `),this.header?(0,i.dy)(d||(d=l`<h1 class="card-header">${0}</h1>`),this.header):i.Ld)}}]}}),i.oi)},65099:function(e,t,r){r.r(t),r.d(t,{HaIconOverflowMenu:()=>f});var a=r(73577),i=(r(71695),r(13334),r(47021),r(14394),r(57243)),n=r(50778),o=r(35359),s=r(66193);r(43527),r(59897),r(74064),r(10508);let d,l,c,u,h,p,g,v,m,b=e=>e;let f=(0,a.Z)([(0,n.Mo)("ha-icon-overflow-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array})],key:"items",value(){return[]}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"method",key:"render",value:function(){return(0,i.dy)(d||(d=b`
      ${0}
    `),this.narrow?(0,i.dy)(l||(l=b` <!-- Collapsed representation for small screens -->
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
            </ha-button-menu>`),this._handleIconOverflowMenuOpened,this._handleIconOverflowMenuClosed,this.hass.localize("ui.common.overflow_menu"),"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z",this.items.map((e=>e.divider?(0,i.dy)(c||(c=b`<li divider role="separator"></li>`)):(0,i.dy)(u||(u=b`<ha-list-item
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
                    </ha-list-item> `),e.disabled,e.action,(0,o.$)({warning:Boolean(e.warning)}),(0,o.$)({warning:Boolean(e.warning)}),e.path,e.label)))):(0,i.dy)(h||(h=b`
            <!-- Icon representation for big screens -->
            ${0}
          `),this.items.map((e=>e.narrowOnly?"":e.divider?(0,i.dy)(p||(p=b`<div role="separator"></div>`)):(0,i.dy)(g||(g=b`<div>
                      ${0}
                      <ha-icon-button
                        @click=${0}
                        .label=${0}
                        .path=${0}
                        ?disabled=${0}
                      ></ha-icon-button>
                    </div> `),e.tooltip?(0,i.dy)(v||(v=b`<simple-tooltip
                            animation-delay="0"
                            position="left"
                          >
                            ${0}
                          </simple-tooltip>`),e.tooltip):"",e.action,e.label,e.path,e.disabled)))))}},{kind:"method",key:"_handleIconOverflowMenuOpened",value:function(e){e.stopPropagation();const t=this.closest(".mdc-data-table__row");t&&(t.style.zIndex="1")}},{kind:"method",key:"_handleIconOverflowMenuClosed",value:function(){const e=this.closest(".mdc-data-table__row");e&&(e.style.zIndex="")}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,(0,i.iv)(m||(m=b`
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
      `))]}}]}}),i.oi)},74064:function(e,t,r){var a=r(73577),i=r(72621),n=(r(71695),r(47021),r(65703)),o=r(46289),s=r(57243),d=r(50778);let l,c,u,h=e=>e;(0,a.Z)([(0,d.Mo)("ha-list-item")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,i.Z)(r,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[o.W,(0,s.iv)(l||(l=h`
        :host {
          padding-left: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-start: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-right: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-end: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
        }
        :host([graphic="avatar"]:not([twoLine])),
        :host([graphic="icon"]:not([twoLine])) {
          height: 48px;
        }
        span.material-icons:first-of-type {
          margin-inline-start: 0px !important;
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            16px
          ) !important;
          direction: var(--direction) !important;
        }
        span.material-icons:last-of-type {
          margin-inline-start: auto !important;
          margin-inline-end: 0px !important;
          direction: var(--direction) !important;
        }
        .mdc-deprecated-list-item__meta {
          display: var(--mdc-list-item-meta-display);
          align-items: center;
          flex-shrink: 0;
        }
        :host([graphic="icon"]:not([twoline]))
          .mdc-deprecated-list-item__graphic {
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            20px
          ) !important;
        }
        :host([multiline-secondary]) {
          height: auto;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__text {
          padding: 8px 0;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text {
          text-overflow: initial;
          white-space: normal;
          overflow: auto;
          display: inline-block;
          margin-top: 10px;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__primary-text {
          margin-top: 10px;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__secondary-text::before {
          display: none;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__primary-text::before {
          display: none;
        }
        :host([disabled]) {
          color: var(--disabled-text-color);
        }
        :host([noninteractive]) {
          pointer-events: unset;
        }
      `)),"rtl"===document.dir?(0,s.iv)(c||(c=h`
            span.material-icons:first-of-type,
            span.material-icons:last-of-type {
              direction: rtl !important;
              --direction: rtl;
            }
          `)):(0,s.iv)(u||(u=h``))]}}]}}),n.K)},89595:function(e,t,r){r.d(t,{q:()=>l});r(52247),r(19083),r(61006),r(71695),r(23669),r(19134),r(44495),r(47021);const a=/^[v^~<>=]*?(\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+))?(?:-([\da-z\-]+(?:\.[\da-z\-]+)*))?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?)?)?$/i,i=e=>{if("string"!=typeof e)throw new TypeError("Invalid argument expected string");const t=e.match(a);if(!t)throw new Error(`Invalid argument not valid semver ('${e}' received)`);return t.shift(),t},n=e=>"*"===e||"x"===e||"X"===e,o=e=>{const t=parseInt(e,10);return isNaN(t)?e:t},s=(e,t)=>{if(n(e)||n(t))return 0;const[r,a]=((e,t)=>typeof e!=typeof t?[String(e),String(t)]:[e,t])(o(e),o(t));return r>a?1:r<a?-1:0},d=(e,t)=>{for(let r=0;r<Math.max(e.length,t.length);r++){const a=s(e[r]||"0",t[r]||"0");if(0!==a)return a}return 0},l=(e,t,r)=>{h(r);const a=((e,t)=>{const r=i(e),a=i(t),n=r.pop(),o=a.pop(),s=d(r,a);return 0!==s?s:n&&o?d(n.split("."),o.split(".")):n||o?n?-1:1:0})(e,t);return c[r].includes(a)},c={">":[1],">=":[0,1],"=":[0],"<=":[-1,0],"<":[-1],"!=":[-1,1]},u=Object.keys(c),h=e=>{if("string"!=typeof e)throw new TypeError("Invalid operator type, expected string but got "+typeof e);if(-1===u.indexOf(e))throw new Error(`Invalid operator, expected one of ${u.join("|")}`)}},12582:function(e,t,r){r.d(t,{Z:()=>a});r(11740),r(39527),r(41360),r(13334);function a(e){if(!e||"object"!=typeof e)return e;if("[object Date]"==Object.prototype.toString.call(e))return new Date(e.getTime());if(Array.isArray(e))return e.map(a);var t={};return Object.keys(e).forEach((function(r){t[r]=a(e[r])})),t}},94964:function(e,t,r){var a=r(73577),i=r(72621),n=(r(71695),r(52805),r(39527),r(41360),r(13334),r(34595),r(47021),r(57243)),o=r(50778),s=r(35359),d=r(11297),l=r(57586);let c,u,h,p,g,v,m=e=>e;const b=new l.r("knx-project-tree-view");(0,a.Z)([(0,o.Mo)("knx-project-tree-view")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"multiselect",value(){return!1}},{kind:"field",decorators:[(0,o.SB)()],key:"_selectableRanges",value(){return{}}},{kind:"method",key:"connectedCallback",value:function(){(0,i.Z)(r,"connectedCallback",this,3)([]);const e=t=>{Object.entries(t).forEach((([t,r])=>{r.group_addresses.length>0&&(this._selectableRanges[t]={selected:!1,groupAddresses:r.group_addresses}),e(r.group_ranges)}))};e(this.data.group_ranges),b.debug("ranges",this._selectableRanges)}},{kind:"method",key:"render",value:function(){return(0,n.dy)(c||(c=m`<div class="ha-tree-view">${0}</div>`),this._recurseData(this.data.group_ranges))}},{kind:"method",key:"_recurseData",value:function(e,t=0){const r=Object.entries(e).map((([e,r])=>{const a=Object.keys(r.group_ranges).length>0;if(!(a||r.group_addresses.length>0))return n.Ld;const i=e in this._selectableRanges,o=!!i&&this._selectableRanges[e].selected,d={"range-item":!0,"root-range":0===t,"sub-range":t>0,selectable:i,"selected-range":o,"non-selected-range":i&&!o},l=(0,n.dy)(u||(u=m`<div
        class=${0}
        toggle-range=${0}
        @click=${0}
      >
        <span class="range-key">${0}</span>
        <span class="range-text">${0}</span>
      </div>`),(0,s.$)(d),i?e:n.Ld,i?this.multiselect?this._selectionChangedMulti:this._selectionChangedSingle:n.Ld,e,r.name);if(a){const e={"root-group":0===t,"sub-group":0!==t};return(0,n.dy)(h||(h=m`<div class=${0}>
          ${0} ${0}
        </div>`),(0,s.$)(e),l,this._recurseData(r.group_ranges,t+1))}return(0,n.dy)(p||(p=m`${0}`),l)}));return(0,n.dy)(g||(g=m`${0}`),r)}},{kind:"method",key:"_selectionChangedMulti",value:function(e){const t=e.target.getAttribute("toggle-range");this._selectableRanges[t].selected=!this._selectableRanges[t].selected,this._selectionUpdate(),this.requestUpdate()}},{kind:"method",key:"_selectionChangedSingle",value:function(e){const t=e.target.getAttribute("toggle-range"),r=this._selectableRanges[t].selected;Object.values(this._selectableRanges).forEach((e=>{e.selected=!1})),this._selectableRanges[t].selected=!r,this._selectionUpdate(),this.requestUpdate()}},{kind:"method",key:"_selectionUpdate",value:function(){const e=Object.values(this._selectableRanges).reduce(((e,t)=>t.selected?e.concat(t.groupAddresses):e),[]);b.debug("selection changed",e),(0,d.B)(this,"knx-group-range-selection-changed",{groupAddresses:e})}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(v||(v=m`
    :host {
      margin: 0;
      height: 100%;
      overflow-y: scroll;
      overflow-x: hidden;
      background-color: var(--card-background-color);
    }

    .ha-tree-view {
      cursor: default;
    }

    .root-group {
      margin-bottom: 8px;
    }

    .root-group > * {
      padding-top: 5px;
      padding-bottom: 5px;
    }

    .range-item {
      display: block;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      font-size: 0.875rem;
    }

    .range-item > * {
      vertical-align: middle;
      pointer-events: none;
    }

    .range-key {
      color: var(--text-primary-color);
      font-size: 0.75rem;
      font-weight: 700;
      background-color: var(--label-badge-grey);
      border-radius: 4px;
      padding: 1px 4px;
      margin-right: 2px;
    }

    .root-range {
      padding-left: 8px;
      font-weight: 500;
      background-color: var(--secondary-background-color);

      & .range-key {
        color: var(--primary-text-color);
        background-color: var(--card-background-color);
      }
    }

    .sub-range {
      padding-left: 13px;
    }

    .selectable {
      cursor: pointer;
    }

    .selectable:hover {
      background-color: rgba(var(--rgb-primary-text-color), 0.04);
    }

    .selected-range {
      background-color: rgba(var(--rgb-primary-color), 0.12);

      & .range-key {
        background-color: var(--primary-color);
      }
    }

    .selected-range:hover {
      background-color: rgba(var(--rgb-primary-color), 0.07);
    }

    .non-selected-range {
      background-color: var(--card-background-color);
    }
  `))}}]}}),n.oi)},88769:function(e,t,r){r.d(t,{W:()=>n,f:()=>i});r(52805),r(11740),r(39527),r(34595);var a=r(76848);const i={payload:e=>null==e.payload?"":Array.isArray(e.payload)?e.payload.reduce(((e,t)=>e+t.toString(16).padStart(2,"0")),"0x"):e.payload.toString(),valueWithUnit:e=>null==e.value?"":"number"==typeof e.value||"boolean"==typeof e.value||"string"==typeof e.value?e.value.toString()+(e.unit?" "+e.unit:""):(0,a.$w)(e.value),timeWithMilliseconds:e=>new Date(e.timestamp).toLocaleTimeString(["en-US"],{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dateWithMilliseconds:e=>new Date(e.timestamp).toLocaleTimeString([],{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dptNumber:e=>null==e.dpt_main?"":null==e.dpt_sub?e.dpt_main.toString():e.dpt_main.toString()+"."+e.dpt_sub.toString().padStart(3,"0"),dptNameNumber:e=>{const t=i.dptNumber(e);return null==e.dpt_name?`DPT ${t}`:t?`DPT ${t} ${e.dpt_name}`:e.dpt_name}},n=e=>null==e?"":e.main+(e.sub?"."+e.sub.toString().padStart(3,"0"):"")},53463:function(e,t,r){r.a(e,(async function(e,a){try{r.r(t),r.d(t,{KNXProjectView:()=>T});var i=r(73577),n=r(72621),o=(r(19083),r(71695),r(92745),r(52805),r(19423),r(40251),r(11740),r(61006),r(39527),r(34595),r(47021),r(57243)),s=r(50778),d=r(27486),l=r(64364),c=(r(68455),r(32422),r(1192),r(59897),r(65099),r(26299),r(52258)),u=(r(94964),r(89595)),h=r(57259),p=r(57586),g=r(88769),v=e([c]);c=(v.then?(await v)():v)[0];let m,b,f,k,y,x,_,w,$,j,A,C,M=e=>e;const S="M6,13H18V11H6M3,6V8H21V6M10,18H14V16H10V18Z",O="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",R=new p.r("knx-project-view"),z="3.3.0";let T=(0,i.Z)([(0,s.Mo)("knx-project-view")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,s.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,reflect:!0,attribute:"range-selector-hidden"})],key:"rangeSelectorHidden",value(){return!0}},{kind:"field",decorators:[(0,s.SB)()],key:"_visibleGroupAddresses",value(){return[]}},{kind:"field",decorators:[(0,s.SB)()],key:"_groupRangeAvailable",value(){return!1}},{kind:"field",decorators:[(0,s.SB)()],key:"_subscribed",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_lastTelegrams",value(){return{}}},{kind:"method",key:"disconnectedCallback",value:function(){(0,n.Z)(r,"disconnectedCallback",this,3)([]),this._subscribed&&(this._subscribed(),this._subscribed=void 0)}},{kind:"method",key:"firstUpdated",value:async function(){this.knx.project?this._isGroupRangeAvailable():this.knx.loadProject().then((()=>{this._isGroupRangeAvailable(),this.requestUpdate()})),(0,h.ze)(this.hass).then((e=>{this._lastTelegrams=e})).catch((e=>{R.error("getGroupTelegrams",e),(0,l.c)("/knx/error",{replace:!0,data:e})})),this._subscribed=await(0,h.IP)(this.hass,(e=>{this.telegram_callback(e)}))}},{kind:"method",key:"_isGroupRangeAvailable",value:function(){var e,t;const r=null!==(e=null===(t=this.knx.project)||void 0===t?void 0:t.knxproject.info.xknxproject_version)&&void 0!==e?e:"0.0.0";R.debug("project version: "+r),this._groupRangeAvailable=(0,u.q)(r,z,">=")}},{kind:"method",key:"telegram_callback",value:function(e){this._lastTelegrams=Object.assign(Object.assign({},this._lastTelegrams),{},{[e.destination]:e})}},{kind:"field",key:"_columns",value(){return(0,d.Z)(((e,t)=>({address:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_address"),flex:1,minWidth:"100px"},name:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_name"),flex:3},dpt:{sortable:!0,filterable:!0,title:this.knx.localize("project_view_table_dpt"),flex:1,minWidth:"82px",template:e=>e.dpt?(0,o.dy)(m||(m=M`<span style="display:inline-block;width:24px;text-align:right;"
                  >${0}</span
                >${0} `),e.dpt.main,e.dpt.sub?"."+e.dpt.sub.toString().padStart(3,"0"):""):""},lastValue:{filterable:!0,title:this.knx.localize("project_view_table_last_value"),flex:2,template:e=>{const t=this._lastTelegrams[e.address];if(!t)return"";const r=g.f.payload(t);return null==t.value?(0,o.dy)(b||(b=M`<code>${0}</code>`),r):(0,o.dy)(f||(f=M`<div title=${0}>
            ${0}
          </div>`),r,g.f.valueWithUnit(this._lastTelegrams[e.address]))}},updated:{title:this.knx.localize("project_view_table_updated"),flex:1,showNarrow:!1,template:e=>{const t=this._lastTelegrams[e.address];if(!t)return"";const r=`${g.f.dateWithMilliseconds(t)}\n\n${t.source} ${t.source_name}`;return(0,o.dy)(k||(k=M`<div title=${0}>
            ${0}
          </div>`),r,(0,c.G)(new Date(t.timestamp),this.hass.locale))}},actions:{title:"",minWidth:"72px",type:"overflow-menu",template:e=>this._groupAddressMenu(e)}})))}},{kind:"method",key:"_groupAddressMenu",value:function(e){var t;const r=[];return 1===(null===(t=e.dpt)||void 0===t?void 0:t.main)&&r.push({path:O,label:"Create binary sensor",action:()=>{(0,l.c)("/knx/entities/create/binary_sensor?knx.ga_sensor.state="+e.address)}}),r.length?(0,o.dy)(y||(y=M`
          <ha-icon-overflow-menu .hass=${0} narrow .items=${0}> </ha-icon-overflow-menu>
        `),this.hass,r):o.Ld}},{kind:"method",key:"_getRows",value:function(e){return e.length?Object.entries(this.knx.project.knxproject.group_addresses).reduce(((t,[r,a])=>(e.includes(r)&&t.push(a),t)),[]):Object.values(this.knx.project.knxproject.group_addresses)}},{kind:"method",key:"_visibleAddressesChanged",value:function(e){this._visibleGroupAddresses=e.detail.groupAddresses}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.knx.project)return(0,o.dy)(x||(x=M` <hass-loading-screen></hass-loading-screen> `));const e=this._getRows(this._visibleGroupAddresses);return(0,o.dy)(_||(_=M`
      <hass-tabs-subpage
        .hass=${0}
        .narrow=${0}
        .route=${0}
        .tabs=${0}
        .localizeFunc=${0}
      >
        ${0}
      </hass-tabs-subpage>
    `),this.hass,this.narrow,this.route,this.tabs,this.knx.localize,this.knx.project.project_loaded?(0,o.dy)(w||(w=M`${0}
              <div class="sections">
                ${0}
                <ha-data-table
                  class="ga-table"
                  .hass=${0}
                  .columns=${0}
                  .data=${0}
                  .hasFab=${0}
                  .searchLabel=${0}
                  .clickable=${0}
                ></ha-data-table>
              </div>`),this.narrow&&this._groupRangeAvailable?(0,o.dy)($||($=M`<ha-icon-button
                    slot="toolbar-icon"
                    .label=${0}
                    .path=${0}
                    @click=${0}
                  ></ha-icon-button>`),this.hass.localize("ui.components.related-filter-menu.filter"),S,this._toggleRangeSelector):o.Ld,this._groupRangeAvailable?(0,o.dy)(j||(j=M`
                      <knx-project-tree-view
                        .data=${0}
                        @knx-group-range-selection-changed=${0}
                      ></knx-project-tree-view>
                    `),this.knx.project.knxproject,this._visibleAddressesChanged):o.Ld,this.hass,this._columns(this.narrow,this.hass.language),e,!1,this.hass.localize("ui.components.data-table.search"),!1):(0,o.dy)(A||(A=M` <ha-card .header=${0}>
              <div class="card-content">
                <p>${0}</p>
              </div>
            </ha-card>`),this.knx.localize("attention"),this.knx.localize("project_view_upload")))}},{kind:"method",key:"_toggleRangeSelector",value:function(){this.rangeSelectorHidden=!this.rangeSelectorHidden}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(C||(C=M`
    hass-loading-screen {
      --app-header-background-color: var(--sidebar-background-color);
      --app-header-text-color: var(--sidebar-text-color);
    }
    .sections {
      display: flex;
      flex-direction: row;
      height: 100%;
    }

    :host([narrow]) knx-project-tree-view {
      position: absolute;
      max-width: calc(100% - 60px); /* 100% -> max 871px before not narrow */
      z-index: 1;
      right: 0;
      transition: 0.5s;
      border-left: 1px solid var(--divider-color);
    }

    :host([narrow][range-selector-hidden]) knx-project-tree-view {
      width: 0;
    }

    :host(:not([narrow])) knx-project-tree-view {
      max-width: 255px; /* min 616px - 816px for tree-view + ga-table (depending on side menu) */
    }

    .ga-table {
      flex: 1;
    }
  `))}}]}}),o.oi);a()}catch(m){a(m)}}))}}]);
//# sourceMappingURL=5392.17bc9f023b67ae5e.js.map