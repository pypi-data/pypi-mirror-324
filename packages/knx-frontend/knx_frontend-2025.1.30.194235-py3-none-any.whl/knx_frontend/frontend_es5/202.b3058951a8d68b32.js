"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["202"],{95907:function(e,t,i){i.d(t,{z:()=>a});i(19083),i(61006);const a=e=>(t,i)=>e.includes(t,i)},38653:function(e,t,i){i.d(t,{h:()=>n});i(52247),i(71695),i(39527),i(41360),i(47021);var a=i(57243),o=i(92903);const n=(0,o.XM)(class extends o.Xe{constructor(e){if(super(e),this._element=void 0,e.type!==o.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}update(e,[t,i]){return this._element&&this._element.localName===t?(i&&Object.entries(i).forEach((([e,t])=>{this._element[e]=t})),a.Jb):this.render(t,i)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach((([e,t])=>{this._element[e]=t})),this._element}})},81036:function(e,t,i){i.d(t,{U:()=>a});const a=e=>e.stopPropagation()},73525:function(e,t,i){i.d(t,{C:()=>o});i(19134),i(11740),i(97003);var a=i(87729);const o=e=>{return t=e.entity_id,void 0===(i=e.attributes).friendly_name?(0,a.p)(t).replace(/_/g," "):(null!==(o=i.friendly_name)&&void 0!==o?o:"").toString();var t,i,o}},32770:function(e,t,i){i.d(t,{$:()=>s,f:()=>d});var a=i(27486);const o=(0,a.Z)((e=>new Intl.Collator(e))),n=(0,a.Z)((e=>new Intl.Collator(e,{sensitivity:"accent"}))),r=(e,t)=>e<t?-1:e>t?1:0,s=(e,t,i=void 0)=>null!==Intl&&void 0!==Intl&&Intl.Collator?o(i).compare(e,t):r(e,t),d=(e,t,i=void 0)=>null!==Intl&&void 0!==Intl&&Intl.Collator?n(i).compare(e,t):r(e.toLowerCase(),t.toLowerCase())},59848:function(e,t,i){i.d(t,{q:()=>y});i(71695),i(61893),i(39527),i(99790),i(13334),i(47021);var a=i(98637);i(52247),i(92745),i(11740);let o=function(e){return e[e.Null=0]="Null",e[e.Backspace=8]="Backspace",e[e.Tab=9]="Tab",e[e.LineFeed=10]="LineFeed",e[e.CarriageReturn=13]="CarriageReturn",e[e.Space=32]="Space",e[e.ExclamationMark=33]="ExclamationMark",e[e.DoubleQuote=34]="DoubleQuote",e[e.Hash=35]="Hash",e[e.DollarSign=36]="DollarSign",e[e.PercentSign=37]="PercentSign",e[e.Ampersand=38]="Ampersand",e[e.SingleQuote=39]="SingleQuote",e[e.OpenParen=40]="OpenParen",e[e.CloseParen=41]="CloseParen",e[e.Asterisk=42]="Asterisk",e[e.Plus=43]="Plus",e[e.Comma=44]="Comma",e[e.Dash=45]="Dash",e[e.Period=46]="Period",e[e.Slash=47]="Slash",e[e.Digit0=48]="Digit0",e[e.Digit1=49]="Digit1",e[e.Digit2=50]="Digit2",e[e.Digit3=51]="Digit3",e[e.Digit4=52]="Digit4",e[e.Digit5=53]="Digit5",e[e.Digit6=54]="Digit6",e[e.Digit7=55]="Digit7",e[e.Digit8=56]="Digit8",e[e.Digit9=57]="Digit9",e[e.Colon=58]="Colon",e[e.Semicolon=59]="Semicolon",e[e.LessThan=60]="LessThan",e[e.Equals=61]="Equals",e[e.GreaterThan=62]="GreaterThan",e[e.QuestionMark=63]="QuestionMark",e[e.AtSign=64]="AtSign",e[e.A=65]="A",e[e.B=66]="B",e[e.C=67]="C",e[e.D=68]="D",e[e.E=69]="E",e[e.F=70]="F",e[e.G=71]="G",e[e.H=72]="H",e[e.I=73]="I",e[e.J=74]="J",e[e.K=75]="K",e[e.L=76]="L",e[e.M=77]="M",e[e.N=78]="N",e[e.O=79]="O",e[e.P=80]="P",e[e.Q=81]="Q",e[e.R=82]="R",e[e.S=83]="S",e[e.T=84]="T",e[e.U=85]="U",e[e.V=86]="V",e[e.W=87]="W",e[e.X=88]="X",e[e.Y=89]="Y",e[e.Z=90]="Z",e[e.OpenSquareBracket=91]="OpenSquareBracket",e[e.Backslash=92]="Backslash",e[e.CloseSquareBracket=93]="CloseSquareBracket",e[e.Caret=94]="Caret",e[e.Underline=95]="Underline",e[e.BackTick=96]="BackTick",e[e.a=97]="a",e[e.b=98]="b",e[e.c=99]="c",e[e.d=100]="d",e[e.e=101]="e",e[e.f=102]="f",e[e.g=103]="g",e[e.h=104]="h",e[e.i=105]="i",e[e.j=106]="j",e[e.k=107]="k",e[e.l=108]="l",e[e.m=109]="m",e[e.n=110]="n",e[e.o=111]="o",e[e.p=112]="p",e[e.q=113]="q",e[e.r=114]="r",e[e.s=115]="s",e[e.t=116]="t",e[e.u=117]="u",e[e.v=118]="v",e[e.w=119]="w",e[e.x=120]="x",e[e.y=121]="y",e[e.z=122]="z",e[e.OpenCurlyBrace=123]="OpenCurlyBrace",e[e.Pipe=124]="Pipe",e[e.CloseCurlyBrace=125]="CloseCurlyBrace",e[e.Tilde=126]="Tilde",e}({});const n=128;function r(){const e=[],t=[];for(let i=0;i<=n;i++)t[i]=0;for(let i=0;i<=n;i++)e.push(t.slice(0));return e}function s(e,t){if(t<0||t>=e.length)return!1;const i=e.codePointAt(t);switch(i){case o.Underline:case o.Dash:case o.Period:case o.Space:case o.Slash:case o.Backslash:case o.SingleQuote:case o.DoubleQuote:case o.Colon:case o.DollarSign:case o.LessThan:case o.OpenParen:case o.OpenSquareBracket:return!0;case void 0:return!1;default:return(a=i)>=127462&&a<=127487||8986===a||8987===a||9200===a||9203===a||a>=9728&&a<=10175||11088===a||11093===a||a>=127744&&a<=128591||a>=128640&&a<=128764||a>=128992&&a<=129003||a>=129280&&a<=129535||a>=129648&&a<=129750?!0:!1}var a}function d(e,t){if(t<0||t>=e.length)return!1;switch(e.charCodeAt(t)){case o.Space:case o.Tab:return!0;default:return!1}}function l(e,t,i){return t[e]!==i[e]}var c=function(e){return e[e.Diag=1]="Diag",e[e.Left=2]="Left",e[e.LeftLeft=3]="LeftLeft",e}(c||{});function u(e,t,i,a,o,r,s){const d=e.length>n?n:e.length,u=a.length>n?n:a.length;if(i>=d||r>=u||d-i>u-r)return;if(!function(e,t,i,a,o,n,r=!1){for(;t<i&&o<n;)e[t]===a[o]&&(r&&(v[t]=o),t+=1),o+=1;return t===i}(t,i,d,o,r,u,!0))return;let b;!function(e,t,i,a,o,n){let r=e-1,s=t-1;for(;r>=i&&s>=a;)o[r]===n[s]&&(p[r]=s,r--),s--}(d,u,i,r,t,o);let y,k,_=1;const x=[!1];for(b=1,y=i;y<d;b++,y++){const n=v[y],s=p[y],l=y+1<d?p[y+1]:u;for(_=n-r+1,k=n;k<l;_++,k++){let d=Number.MIN_SAFE_INTEGER,l=!1;k<=s&&(d=h(e,t,y,i,a,o,k,u,r,0===m[b-1][_-1],x));let v=0;d!==Number.MAX_SAFE_INTEGER&&(l=!0,v=d+g[b-1][_-1]);const p=k>n,$=p?g[b][_-1]+(m[b][_-1]>0?-5:0):0,w=k>n+1&&m[b][_-1]>0,C=w?g[b][_-2]+(m[b][_-2]>0?-5:0):0;if(w&&(!p||C>=$)&&(!l||C>=v))g[b][_]=C,f[b][_]=c.LeftLeft,m[b][_]=0;else if(p&&(!l||$>=v))g[b][_]=$,f[b][_]=c.Left,m[b][_]=0;else{if(!l)throw new Error("not possible");g[b][_]=v,f[b][_]=c.Diag,m[b][_]=m[b-1][_-1]+1}}}if(!x[0]&&!s)return;b--,_--;const $=[g[b][_],r];let w=0,C=0;for(;b>=1;){let e=_;do{const t=f[b][e];if(t===c.LeftLeft)e-=2;else{if(t!==c.Left)break;e-=1}}while(e>=1);w>1&&t[i+b-1]===o[r+_-1]&&!l(e+r-1,a,o)&&w+1>m[b][e]&&(e=_),e===_?w++:w=1,C||(C=e),b--,_=e-1,$.push(_)}u===d&&($[0]+=2);const L=C-d;return $[0]-=L,$}function h(e,t,i,a,o,n,r,c,u,h,v){if(t[i]!==n[r])return Number.MIN_SAFE_INTEGER;let p=1,m=!1;return r===i-a?p=e[i]===o[r]?7:5:!l(r,o,n)||0!==r&&l(r-1,o,n)?!s(n,r)||0!==r&&s(n,r-1)?(s(n,r-1)||d(n,r-1))&&(p=5,m=!0):p=5:(p=e[i]===o[r]?7:5,m=!0),p>1&&i===a&&(v[0]=!0),m||(m=l(r,o,n)||s(n,r-1)||d(n,r-1)),i===a?r>u&&(p-=m?3:5):p+=h?m?2:0:m?0:1,r+1===c&&(p-=m?3:5),p}const v=b(256),p=b(256),m=r(),g=r(),f=r();function b(e){const t=[];for(let i=0;i<=e;i++)t[i]=0;return t}const y=(e,t)=>t.map((t=>(t.score=((e,t)=>{let i=Number.NEGATIVE_INFINITY;for(const o of t.strings){const t=u(e,(0,a._)(e.toLowerCase()),0,o,(0,a._)(o.toLowerCase()),0,!0);if(!t)continue;const n=0===t[0]?1:t[0];n>i&&(i=n)}if(i!==Number.NEGATIVE_INFINITY)return i})(e,t),t))).filter((e=>void 0!==e.score)).sort((({score:e=0},{score:t=0})=>e>t?-1:e<t?1:0))},98637:function(e,t,i){i.d(t,{_:()=>a});i(19134),i(97003);const a=e=>e.normalize("NFD").replace(/[\u0300-\u036F]/g,"")},56587:function(e,t,i){i.d(t,{D:()=>a});i(71695),i(47021);const a=(e,t,i=!1)=>{let a;const o=(...o)=>{const n=i&&!a;clearTimeout(a),a=window.setTimeout((()=>{a=void 0,e(...o)}),t),n&&e(...o)};return o.cancel=()=>{clearTimeout(a)},o}},84573:function(e,t,i){var a=i(73577),o=(i(71695),i(47021),i(74763)),n=i(50778);(0,a.Z)([(0,n.Mo)("ha-chip-set")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[]}}),o.l)},13978:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(47021),i(74514)),r=i(57243),s=i(50778);let d,l=e=>e;(0,a.Z)([(0,s.Mo)("ha-input-chip")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",static:!0,key:"styles",value(){return[...(0,o.Z)(i,"styles",this),(0,r.iv)(d||(d=l`
      :host {
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--primary-text-color);
        --md-sys-color-on-secondary-container: var(--primary-text-color);
        --md-input-chip-container-shape: 16px;
        --md-input-chip-outline-color: var(--outline-color);
        --md-input-chip-selected-container-color: rgba(
          var(--rgb-primary-text-color),
          0.15
        );
        --ha-input-chip-selected-container-opacity: 1;
        --md-input-chip-label-text-font: Roboto, sans-serif;
      }
      /** Set the size of mdc icons **/
      ::slotted([slot="icon"]) {
        display: flex;
        --mdc-icon-size: var(--md-input-chip-icon-size, 18px);
      }
      .selected::before {
        opacity: var(--ha-input-chip-selected-container-opacity);
      }
    `))]}}]}}),n.W)},17949:function(e,t,i){i.r(t);var a=i(73577),o=(i(71695),i(47021),i(57243)),n=i(50778),r=i(35359),s=i(11297);i(59897),i(10508);let d,l,c,u,h=e=>e;const v={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};(0,a.Z)([(0,n.Mo)("ha-alert")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)()],key:"title",value(){return""}},{kind:"field",decorators:[(0,n.Cb)({attribute:"alert-type"})],key:"alertType",value(){return"info"}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"dismissable",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"method",key:"render",value:function(){return(0,o.dy)(d||(d=h`
      <div
        class="issue-type ${0}"
        role="alert"
      >
        <div class="icon ${0}">
          <slot name="icon">
            <ha-svg-icon .path=${0}></ha-svg-icon>
          </slot>
        </div>
        <div class=${0}>
          <div class="main-content">
            ${0}
            <slot></slot>
          </div>
          <div class="action">
            <slot name="action">
              ${0}
            </slot>
          </div>
        </div>
      </div>
    `),(0,r.$)({[this.alertType]:!0}),this.title?"":"no-title",v[this.alertType],(0,r.$)({content:!0,narrow:this.narrow}),this.title?(0,o.dy)(l||(l=h`<div class="title">${0}</div>`),this.title):o.Ld,this.dismissable?(0,o.dy)(c||(c=h`<ha-icon-button
                    @click=${0}
                    label="Dismiss alert"
                    .path=${0}
                  ></ha-icon-button>`),this._dismissClicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):o.Ld)}},{kind:"method",key:"_dismissClicked",value:function(){(0,s.B)(this,"alert-dismissed-clicked")}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(u||(u=h`
    .issue-type {
      position: relative;
      padding: 8px;
      display: flex;
    }
    .issue-type::after {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      opacity: 0.12;
      pointer-events: none;
      content: "";
      border-radius: 4px;
    }
    .icon {
      z-index: 1;
    }
    .icon.no-title {
      align-self: center;
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      text-align: var(--float-start);
    }
    .content.narrow {
      flex-direction: column;
      align-items: flex-end;
    }
    .action {
      z-index: 1;
      width: min-content;
      --mdc-theme-primary: var(--primary-text-color);
    }
    .main-content {
      overflow-wrap: anywhere;
      word-break: break-word;
      margin-left: 8px;
      margin-right: 0;
      margin-inline-start: 8px;
      margin-inline-end: 0;
    }
    .title {
      margin-top: 2px;
      font-weight: bold;
    }
    .action mwc-button,
    .action ha-icon-button {
      --mdc-theme-primary: var(--primary-text-color);
      --mdc-icon-button-size: 36px;
    }
    .issue-type.info > .icon {
      color: var(--info-color);
    }
    .issue-type.info::after {
      background-color: var(--info-color);
    }

    .issue-type.warning > .icon {
      color: var(--warning-color);
    }
    .issue-type.warning::after {
      background-color: var(--warning-color);
    }

    .issue-type.error > .icon {
      color: var(--error-color);
    }
    .issue-type.error::after {
      background-color: var(--error-color);
    }

    .issue-type.success > .icon {
      color: var(--success-color);
    }
    .issue-type.success::after {
      background-color: var(--success-color);
    }
    :host ::slotted(ul) {
      margin: 0;
      padding-inline-start: 20px;
    }
  `))}}]}}),o.oi)},69181:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),o=(i(19083),i(71695),i(19423),i(40251),i(61006),i(39527),i(92181),i(99790),i(13334),i(36993),i(47021),i(57243)),n=i(50778),r=i(35359),s=i(27486),d=i(11297),l=i(79575),c=i(59848),u=i(71656),h=i(92374),v=i(4557),p=i(88233),m=i(69484),g=(i(59897),i(74064),i(10508),e([m]));m=(g.then?(await g)():g)[0];let f,b,y,k,_=e=>e;const x="M20 2H4C2.9 2 2 2.9 2 4V20C2 21.11 2.9 22 4 22H20C21.11 22 22 21.11 22 20V4C22 2.9 21.11 2 20 2M4 6L6 4H10.9L4 10.9V6M4 13.7L13.7 4H18.6L4 18.6V13.7M20 18L18 20H13.1L20 13.1V18M20 10.3L10.3 20H5.4L20 5.4V10.3Z",$=e=>(0,o.dy)(f||(f=_`<ha-list-item
    graphic="icon"
    class=${0}
  >
    ${0}
    ${0}
  </ha-list-item>`),(0,r.$)({"add-new":e.area_id===w}),e.icon?(0,o.dy)(b||(b=_`<ha-icon slot="graphic" .icon=${0}></ha-icon>`),e.icon):(0,o.dy)(y||(y=_`<ha-svg-icon slot="graphic" .path=${0}></ha-svg-icon>`),x),e.name),w="___ADD_NEW___",C="___NO_ITEMS___",L="___ADD_NEW_SUGGESTION___";(0,a.Z)([(0,n.Mo)("ha-area-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"no-add"})],key:"noAdd",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array,attribute:"exclude-areas"})],key:"excludeAreas",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.SB)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.IO)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_suggestion",value:void 0},{kind:"field",key:"_init",value(){return!1}},{kind:"method",key:"open",value:async function(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.open())}},{kind:"method",key:"focus",value:async function(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.focus())}},{kind:"field",key:"_getAreas",value(){return(0,s.Z)(((e,t,i,a,o,n,r,s,d,c)=>{let u,v,p={};(a||o||n||r||s)&&(p=(0,h.R6)(i),u=t,v=i.filter((e=>e.area_id)),a&&(u=u.filter((e=>{const t=p[e.id];return!(!t||!t.length)&&p[e.id].some((e=>a.includes((0,l.M)(e.entity_id))))})),v=v.filter((e=>a.includes((0,l.M)(e.entity_id))))),o&&(u=u.filter((e=>{const t=p[e.id];return!t||!t.length||i.every((e=>!o.includes((0,l.M)(e.entity_id))))})),v=v.filter((e=>!o.includes((0,l.M)(e.entity_id))))),n&&(u=u.filter((e=>{const t=p[e.id];return!(!t||!t.length)&&p[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&n.includes(t.attributes.device_class))}))})),v=v.filter((e=>{const t=this.hass.states[e.entity_id];return t.attributes.device_class&&n.includes(t.attributes.device_class)}))),r&&(u=u.filter((e=>r(e)))),s&&(u=u.filter((e=>{const t=p[e.id];return!(!t||!t.length)&&p[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&s(t)}))})),v=v.filter((e=>{const t=this.hass.states[e.entity_id];return!!t&&s(t)}))));let m,g=e;return u&&(m=u.filter((e=>e.area_id)).map((e=>e.area_id))),v&&(m=(null!=m?m:[]).concat(v.filter((e=>e.area_id)).map((e=>e.area_id)))),m&&(g=g.filter((e=>m.includes(e.area_id)))),c&&(g=g.filter((e=>!c.includes(e.area_id)))),g.length||(g=[{area_id:C,floor_id:null,name:this.hass.localize("ui.components.area-picker.no_areas"),picture:null,icon:null,aliases:[],labels:[],temperature_entity_id:null,humidity_entity_id:null,created_at:0,modified_at:0}]),d?g:[...g,{area_id:w,floor_id:null,name:this.hass.localize("ui.components.area-picker.add_new"),picture:null,icon:"mdi:plus",aliases:[],labels:[],temperature_entity_id:null,humidity_entity_id:null,created_at:0,modified_at:0}]}))}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){this._init=!0;const e=this._getAreas(Object.values(this.hass.areas),Object.values(this.hass.devices),Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.noAdd,this.excludeAreas).map((e=>Object.assign(Object.assign({},e),{},{strings:[e.area_id,...e.aliases,e.name]})));this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){var e;return(0,o.dy)(k||(k=_`
      <ha-combo-box
        .hass=${0}
        .helper=${0}
        item-value-path="area_id"
        item-id-path="area_id"
        item-label-path="name"
        .value=${0}
        .disabled=${0}
        .required=${0}
        .label=${0}
        .placeholder=${0}
        .renderer=${0}
        @filter-changed=${0}
        @opened-changed=${0}
        @value-changed=${0}
      >
      </ha-combo-box>
    `),this.hass,this.helper,this._value,this.disabled,this.required,void 0===this.label&&this.hass?this.hass.localize("ui.components.area-picker.area"):this.label,this.placeholder?null===(e=this.hass.areas[this.placeholder])||void 0===e?void 0:e.name:void 0,$,this._filterChanged,this._openedChanged,this._areaChanged)}},{kind:"method",key:"_filterChanged",value:function(e){var t;const i=e.target,a=e.detail.value;if(!a)return void(this.comboBox.filteredItems=this.comboBox.items);const o=(0,c.q)(a,(null===(t=i.items)||void 0===t?void 0:t.filter((e=>![C,w].includes(e.label_id))))||[]);0===o.length?this.noAdd?(this._suggestion=a,this.comboBox.filteredItems=[{area_id:L,floor_id:null,name:this.hass.localize("ui.components.area-picker.add_new_sugestion",{name:this._suggestion}),icon:"mdi:plus",picture:null,labels:[],aliases:[],temperature_entity_id:null,humidity_entity_id:null,created_at:0,modified_at:0}]):this.comboBox.filteredItems=[{area_id:C,floor_id:null,name:this.hass.localize("ui.components.area-picker.no_match"),icon:null,picture:null,labels:[],aliases:[],temperature_entity_id:null,humidity_entity_id:null,created_at:0,modified_at:0}]:this.comboBox.filteredItems=o}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_areaChanged",value:function(e){e.stopPropagation();let t=e.detail.value;if(t===C)return t="",void this.comboBox.setInputValue("");[L,w].includes(t)?(e.target.value=this._value,this.hass.loadFragmentTranslation("config"),(0,p.E)(this,{suggestedName:t===L?this._suggestion:"",createEntry:async e=>{try{const t=await(0,u.Lo)(this.hass,e),i=[...Object.values(this.hass.areas),t];this.comboBox.filteredItems=this._getAreas(i,Object.values(this.hass.devices),Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.noAdd,this.excludeAreas),await this.updateComplete,await this.comboBox.updateComplete,this._setValue(t.area_id)}catch(t){(0,v.Ys)(this,{title:this.hass.localize("ui.components.area-picker.failed_create_area"),text:t.message})}}}),this._suggestion=void 0,this.comboBox.setInputValue("")):t!==this._value&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,d.B)(this,"value-changed",{value:e}),(0,d.B)(this,"change")}),0)}}]}}),o.oi);t()}catch(f){t(f)}}))},76418:function(e,t,i){var a=i(73577),o=(i(71695),i(47021),i(92444)),n=i(76688),r=i(57243),s=i(50778);let d,l=e=>e;(0,a.Z)([(0,s.Mo)("ha-checkbox")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[n.W,(0,r.iv)(d||(d=l`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `))]}}]}}),o.A)},90977:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(47021),i(58795)),r=i(57243),s=i(50778);let d,l=e=>e;(0,a.Z)([(0,s.Mo)("ha-circular-progress")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,s.Cb)()],key:"size",value:void 0},{kind:"method",key:"updated",value:function(e){if((0,o.Z)(i,"updated",this,3)([e]),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,o.Z)(i,"styles",this),(0,r.iv)(d||(d=l`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-circular-progress-size: 48px;
      }
    `))]}}]}}),n.B)},69484:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),o=i(72621),n=(i(71695),i(40251),i(39527),i(41360),i(47021),i(2394)),r=i(28737),s=i(75662),d=i(57243),l=i(50778),c=i(20552),u=i(11297),h=(i(59897),i(74064),i(70596),e([r]));r=(h.then?(await h)():h)[0];let v,p,m,g,f,b,y=e=>e;const k="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",_="M7,10L12,15L17,10H7Z",x="M7,15L12,10L17,15H7Z";(0,s.hC)("vaadin-combo-box-item",(0,d.iv)(v||(v=y`
    :host {
      padding: 0 !important;
    }
    :host([focused]:not([disabled])) {
      background-color: rgba(var(--rgb-primary-text-color, 0, 0, 0), 0.12);
    }
    :host([selected]:not([disabled])) {
      background-color: transparent;
      color: var(--mdc-theme-primary);
      --mdc-ripple-color: var(--mdc-theme-primary);
      --mdc-theme-text-primary-on-background: var(--mdc-theme-primary);
    }
    :host([selected]:not([disabled])):before {
      background-color: var(--mdc-theme-primary);
      opacity: 0.12;
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
    :host([selected][focused]:not([disabled])):before {
      opacity: 0.24;
    }
    :host(:hover:not([disabled])) {
      background-color: transparent;
    }
    [part="content"] {
      width: 100%;
    }
    [part="checkmark"] {
      display: none;
    }
  `)));(0,a.Z)([(0,l.Mo)("ha-combo-box")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"validationMessage",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"invalid",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"icon",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"items",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"filteredItems",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"dataProvider",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:"allow-custom-value",type:Boolean})],key:"allowCustomValue",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:"item-value-path"})],key:"itemValuePath",value(){return"value"}},{kind:"field",decorators:[(0,l.Cb)({attribute:"item-label-path"})],key:"itemLabelPath",value(){return"label"}},{kind:"field",decorators:[(0,l.Cb)({attribute:"item-id-path"})],key:"itemIdPath",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"renderer",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"opened",value(){return!1}},{kind:"field",decorators:[(0,l.IO)("vaadin-combo-box-light",!0)],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,l.IO)("ha-textfield",!0)],key:"_inputElement",value:void 0},{kind:"field",key:"_overlayMutationObserver",value:void 0},{kind:"field",key:"_bodyMutationObserver",value:void 0},{kind:"method",key:"open",value:async function(){var e;await this.updateComplete,null===(e=this._comboBox)||void 0===e||e.open()}},{kind:"method",key:"focus",value:async function(){var e,t;await this.updateComplete,await(null===(e=this._inputElement)||void 0===e?void 0:e.updateComplete),null===(t=this._inputElement)||void 0===t||t.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)(i,"disconnectedCallback",this,3)([]),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}},{kind:"get",key:"selectedItem",value:function(){return this._comboBox.selectedItem}},{kind:"method",key:"setInputValue",value:function(e){this._comboBox.value=e}},{kind:"method",key:"render",value:function(){var e;return(0,d.dy)(p||(p=y`
      <!-- @ts-ignore Tag definition is not included in theme folder -->
      <vaadin-combo-box-light
        .itemValuePath=${0}
        .itemIdPath=${0}
        .itemLabelPath=${0}
        .items=${0}
        .value=${0}
        .filteredItems=${0}
        .dataProvider=${0}
        .allowCustomValue=${0}
        .disabled=${0}
        .required=${0}
        ${0}
        @opened-changed=${0}
        @filter-changed=${0}
        @value-changed=${0}
        attr-for-value="value"
      >
        <ha-textfield
          label=${0}
          placeholder=${0}
          ?disabled=${0}
          ?required=${0}
          validationMessage=${0}
          .errorMessage=${0}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          input-spellcheck="false"
          .suffix=${0}
          .icon=${0}
          .invalid=${0}
          .helper=${0}
          helperPersistent
        >
          <slot name="icon" slot="leadingIcon"></slot>
        </ha-textfield>
        ${0}
        <ha-svg-icon
          role="button"
          tabindex="-1"
          aria-label=${0}
          aria-expanded=${0}
          class="toggle-button"
          .path=${0}
          @click=${0}
        ></ha-svg-icon>
      </vaadin-combo-box-light>
    `),this.itemValuePath,this.itemIdPath,this.itemLabelPath,this.items,this.value||"",this.filteredItems,this.dataProvider,this.allowCustomValue,this.disabled,this.required,(0,n.t)(this.renderer||this._defaultRowRenderer),this._openedChanged,this._filterChanged,this._valueChanged,(0,c.o)(this.label),(0,c.o)(this.placeholder),this.disabled,this.required,(0,c.o)(this.validationMessage),this.errorMessage,(0,d.dy)(m||(m=y`<div
            style="width: 28px;"
            role="none presentation"
          ></div>`)),this.icon,this.invalid,this.helper,this.value?(0,d.dy)(g||(g=y`<ha-svg-icon
              role="button"
              tabindex="-1"
              aria-label=${0}
              class="clear-button"
              .path=${0}
              @click=${0}
            ></ha-svg-icon>`),(0,c.o)(null===(e=this.hass)||void 0===e?void 0:e.localize("ui.common.clear")),k,this._clearValue):"",(0,c.o)(this.label),this.opened?"true":"false",this.opened?x:_,this._toggleOpen)}},{kind:"field",key:"_defaultRowRenderer",value(){return e=>(0,d.dy)(f||(f=y`<ha-list-item>
      ${0}
    </ha-list-item>`),this.itemLabelPath?e[this.itemLabelPath]:e)}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),(0,u.B)(this,"value-changed",{value:void 0})}},{kind:"method",key:"_toggleOpen",value:function(e){var t,i;this.opened?(null===(t=this._comboBox)||void 0===t||t.close(),e.stopPropagation()):null===(i=this._comboBox)||void 0===i||i.inputElement.focus()}},{kind:"method",key:"_openedChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(setTimeout((()=>{this.opened=t}),0),(0,u.B)(this,"opened-changed",{value:e.detail.value}),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else{var i;null===(i=this._bodyMutationObserver)||void 0===i||i.disconnect(),this._bodyMutationObserver=void 0}}},{kind:"method",key:"_observeBody",value:function(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver((e=>{e.forEach((e=>{e.addedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)})),e.removedNodes.forEach((e=>{var t;"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),this._overlayMutationObserver=void 0)}))}))})),this._bodyMutationObserver.observe(document.body,{childList:!0}))}},{kind:"method",key:"_removeInert",value:function(e){var t;if(e.inert)return e.inert=!1,null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver((e=>{e.forEach((e=>{if("inert"===e.attributeName){const i=e.target;var t;if(i.inert)null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),this._overlayMutationObserver=void 0,i.inert=!1}}))})),this._overlayMutationObserver.observe(e,{attributes:!0}))}},{kind:"method",key:"_filterChanged",value:function(e){e.stopPropagation(),(0,u.B)(this,"filter-changed",{value:e.detail.value})}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0);const t=e.detail.value;t!==this.value&&(0,u.B)(this,"value-changed",{value:t||void 0})}},{kind:"field",static:!0,key:"styles",value(){return(0,d.iv)(b||(b=y`
    :host {
      display: block;
      width: 100%;
    }
    vaadin-combo-box-light {
      position: relative;
      --vaadin-combo-box-overlay-max-height: calc(45vh - 56px);
    }
    ha-textfield {
      width: 100%;
    }
    ha-textfield > ha-icon-button {
      --mdc-icon-button-size: 24px;
      padding: 2px;
      color: var(--secondary-text-color);
    }
    ha-svg-icon {
      color: var(--input-dropdown-icon-color);
      position: absolute;
      cursor: pointer;
    }
    .toggle-button {
      right: 12px;
      top: -10px;
      inset-inline-start: initial;
      inset-inline-end: 12px;
      direction: var(--direction);
    }
    :host([opened]) .toggle-button {
      color: var(--primary-color);
    }
    .clear-button {
      --mdc-icon-size: 20px;
      top: -7px;
      right: 36px;
      inset-inline-start: initial;
      inset-inline-end: 36px;
      direction: var(--direction);
    }
  `))}}]}}),d.oi);t()}catch(v){t(v)}}))},9388:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(47021),i(57243)),r=i(50778),s=i(35359),d=i(20552),l=i(91583),c=i(11297);i(10508);let u,h,v,p,m,g=e=>e;(0,a.Z)([(0,r.Mo)("ha-control-select")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"vertical",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"hide-label"})],key:"hideLabel",value(){return!1}},{kind:"field",decorators:[(0,r.SB)()],key:"_activeIndex",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)(i,"firstUpdated",this,3)([e]),this.setAttribute("role","listbox"),this.hasAttribute("tabindex")||this.setAttribute("tabindex","0")}},{kind:"method",key:"updated",value:function(e){if((0,o.Z)(i,"updated",this,3)([e]),e.has("_activeIndex")){var t;const e=null!=this._activeIndex?null===(t=this.options)||void 0===t||null===(t=t[this._activeIndex])||void 0===t?void 0:t.value:void 0,i=null!=e?`option-${e}`:void 0;this.setAttribute("aria-activedescendant",null!=i?i:"")}if(e.has("vertical")){const e=this.vertical?"vertical":"horizontal";this.setAttribute("aria-orientation",e)}}},{kind:"method",key:"connectedCallback",value:function(){(0,o.Z)(i,"connectedCallback",this,3)([]),this._setupListeners()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)(i,"disconnectedCallback",this,3)([]),this._destroyListeners()}},{kind:"method",key:"_setupListeners",value:function(){this.addEventListener("focus",this._handleFocus),this.addEventListener("blur",this._handleBlur),this.addEventListener("keydown",this._handleKeydown)}},{kind:"method",key:"_destroyListeners",value:function(){this.removeEventListener("focus",this._handleFocus),this.removeEventListener("blur",this._handleBlur),this.removeEventListener("keydown",this._handleKeydown)}},{kind:"method",key:"_handleFocus",value:function(){var e,t;this.disabled||(this._activeIndex=null!==(e=null!=this.value?null===(t=this.options)||void 0===t?void 0:t.findIndex((e=>e.value===this.value)):void 0)&&void 0!==e?e:0)}},{kind:"method",key:"_handleBlur",value:function(){this._activeIndex=void 0}},{kind:"method",key:"_handleKeydown",value:function(e){if(!this.options||null==this._activeIndex||this.disabled)return;const t=this.options[this._activeIndex].value;switch(e.key){case" ":this.value=t,(0,c.B)(this,"value-changed",{value:t});break;case"ArrowUp":case"ArrowLeft":this._activeIndex=this._activeIndex<=0?this.options.length-1:this._activeIndex-1;break;case"ArrowDown":case"ArrowRight":this._activeIndex=(this._activeIndex+1)%this.options.length;break;case"Home":this._activeIndex=0;break;case"End":this._activeIndex=this.options.length-1;break;default:return}e.preventDefault()}},{kind:"method",key:"_handleOptionClick",value:function(e){if(this.disabled)return;const t=e.target.value;this.value=t,(0,c.B)(this,"value-changed",{value:t})}},{kind:"method",key:"_handleOptionMouseDown",value:function(e){var t;if(this.disabled)return;e.preventDefault();const i=e.target.value;this._activeIndex=null===(t=this.options)||void 0===t?void 0:t.findIndex((e=>e.value===i))}},{kind:"method",key:"_handleOptionMouseUp",value:function(e){e.preventDefault(),this._activeIndex=void 0}},{kind:"method",key:"render",value:function(){return(0,n.dy)(u||(u=g`
      <div class="container">
        ${0}
      </div>
    `),this.options?(0,l.r)(this.options,(e=>e.value),((e,t)=>this._renderOption(e,t))):n.Ld)}},{kind:"method",key:"_renderOption",value:function(e,t){return(0,n.dy)(h||(h=g`
      <div
        id=${0}
        class=${0}
        role="option"
        .value=${0}
        aria-selected=${0}
        aria-label=${0}
        title=${0}
        @click=${0}
        @mousedown=${0}
        @mouseup=${0}
      >
        <div class="content">
          ${0}
          ${0}
        </div>
      </div>
    `),`option-${e.value}`,(0,s.$)({option:!0,selected:this.value===e.value,focused:this._activeIndex===t}),e.value,this.value===e.value,(0,d.o)(e.label),(0,d.o)(e.label),this._handleOptionClick,this._handleOptionMouseDown,this._handleOptionMouseUp,e.path?(0,n.dy)(v||(v=g`<ha-svg-icon .path=${0}></ha-svg-icon>`),e.path):e.icon||n.Ld,e.label&&!this.hideLabel?(0,n.dy)(p||(p=g`<span>${0}</span>`),e.label):n.Ld)}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(m||(m=g`
    :host {
      display: block;
      --control-select-color: var(--primary-color);
      --control-select-focused-opacity: 0.2;
      --control-select-selected-opacity: 1;
      --control-select-background: var(--disabled-color);
      --control-select-background-opacity: 0.2;
      --control-select-thickness: 40px;
      --control-select-border-radius: 10px;
      --control-select-padding: 4px;
      --control-select-button-border-radius: calc(
        var(--control-select-border-radius) - var(--control-select-padding)
      );
      --mdc-icon-size: 20px;
      height: var(--control-select-thickness);
      width: 100%;
      border-radius: var(--control-select-border-radius);
      outline: none;
      transition: box-shadow 180ms ease-in-out;
      font-style: normal;
      font-weight: 500;
      color: var(--primary-text-color);
      user-select: none;
      -webkit-tap-highlight-color: transparent;
    }
    :host(:focus-visible) {
      box-shadow: 0 0 0 2px var(--control-select-color);
    }
    :host([vertical]) {
      width: var(--control-select-thickness);
      height: 100%;
    }
    .container {
      position: relative;
      height: 100%;
      width: 100%;
      border-radius: var(--control-select-border-radius);
      transform: translateZ(0);
      overflow: hidden;
      display: flex;
      flex-direction: row;
      padding: var(--control-select-padding);
      box-sizing: border-box;
    }
    .container::before {
      position: absolute;
      content: "";
      top: 0;
      left: 0;
      height: 100%;
      width: 100%;
      background: var(--control-select-background);
      opacity: var(--control-select-background-opacity);
    }

    .container > *:not(:last-child) {
      margin-right: var(--control-select-padding);
      margin-inline-end: var(--control-select-padding);
      margin-inline-start: initial;
      direction: var(--direction);
    }
    .option {
      cursor: pointer;
      position: relative;
      flex: 1;
      height: 100%;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: var(--control-select-button-border-radius);
      overflow: hidden;
      /* For safari border-radius overflow */
      z-index: 0;
    }
    .content > *:not(:last-child) {
      margin-bottom: 4px;
    }
    .option::before {
      position: absolute;
      content: "";
      top: 0;
      left: 0;
      height: 100%;
      width: 100%;
      background-color: var(--control-select-color);
      opacity: 0;
      transition:
        background-color ease-in-out 180ms,
        opacity ease-in-out 80ms;
    }
    .option.focused::before,
    .option:hover::before {
      opacity: var(--control-select-focused-opacity);
    }
    .option.selected {
      color: white;
    }
    .option.selected::before {
      opacity: var(--control-select-selected-opacity);
    }
    .option .content {
      position: relative;
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      text-align: center;
      padding: 2px;
      width: 100%;
      box-sizing: border-box;
    }
    .option .content span {
      display: block;
      width: 100%;
      -webkit-hyphens: auto;
      -moz-hyphens: auto;
      hyphens: auto;
    }
    :host([vertical]) {
      width: var(--control-select-thickness);
      height: auto;
    }
    :host([vertical]) .container {
      flex-direction: column;
    }
    :host([vertical]) .container > *:not(:last-child) {
      margin-right: initial;
      margin-inline-end: initial;
      margin-bottom: var(--control-select-padding);
    }
    :host([disabled]) {
      --control-select-color: var(--disabled-color);
      --control-select-focused-opacity: 0;
      color: var(--disabled-color);
    }
    :host([disabled]) .option {
      cursor: not-allowed;
    }
  `))}}]}}),n.oi)},44118:function(e,t,i){i.d(t,{i:()=>m});var a=i(73577),o=i(72621),n=(i(68212),i(71695),i(47021),i(74966)),r=i(51408),s=i(57243),d=i(50778),l=i(24067);i(59897);let c,u,h,v=e=>e;const p=["button","ha-list-item"],m=(e,t)=>{var i;return(0,s.dy)(c||(c=v`
  <div class="header_title">
    <ha-icon-button
      .label=${0}
      .path=${0}
      dialogAction="close"
      class="header_button"
    ></ha-icon-button>
    <span>${0}</span>
  </div>
`),null!==(i=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close","M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",t)};(0,a.Z)([(0,d.Mo)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:l.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return(0,s.dy)(u||(u=v`<slot name="heading"> ${0} </slot>`),(0,o.Z)(i,"renderHeading",this,3)([]))}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,o.Z)(i,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,p].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)(i,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value(){return[r.W,(0,s.iv)(h||(h=v`
      :host([scrolled]) ::slotted(ha-dialog-header) {
        border-bottom: 1px solid
          var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
      }
      .mdc-dialog {
        --mdc-dialog-scroll-divider-color: var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );
        z-index: var(--dialog-z-index, 8);
        -webkit-backdrop-filter: var(
          --ha-dialog-scrim-backdrop-filter,
          var(--dialog-backdrop-filter, none)
        );
        backdrop-filter: var(
          --ha-dialog-scrim-backdrop-filter,
          var(--dialog-backdrop-filter, none)
        );
        --mdc-dialog-box-shadow: var(--dialog-box-shadow, none);
        --mdc-typography-headline6-font-weight: 400;
        --mdc-typography-headline6-font-size: 1.574rem;
      }
      .mdc-dialog__actions {
        justify-content: var(--justify-action-buttons, flex-end);
        padding-bottom: max(env(safe-area-inset-bottom), 24px);
      }
      .mdc-dialog__actions span:nth-child(1) {
        flex: var(--secondary-action-button-flex, unset);
      }
      .mdc-dialog__actions span:nth-child(2) {
        flex: var(--primary-action-button-flex, unset);
      }
      .mdc-dialog__container {
        align-items: var(--vertical-align-dialog, center);
      }
      .mdc-dialog__title {
        padding: 24px 24px 0 24px;
      }
      .mdc-dialog__title:has(span) {
        padding: 12px 12px 0;
      }
      .mdc-dialog__actions {
        padding: 12px 24px 12px 24px;
      }
      .mdc-dialog__title::before {
        content: unset;
      }
      .mdc-dialog .mdc-dialog__content {
        position: var(--dialog-content-position, relative);
        padding: var(--dialog-content-padding, 24px);
      }
      :host([hideactions]) .mdc-dialog .mdc-dialog__content {
        padding-bottom: max(
          var(--dialog-content-padding, 24px),
          env(safe-area-inset-bottom)
        );
      }
      .mdc-dialog .mdc-dialog__surface {
        position: var(--dialog-surface-position, relative);
        top: var(--dialog-surface-top);
        margin-top: var(--dialog-surface-margin-top);
        min-height: var(--mdc-dialog-min-height, auto);
        border-radius: var(--ha-dialog-border-radius, 28px);
        -webkit-backdrop-filter: var(--ha-dialog-surface-backdrop-filter, none);
        backdrop-filter: var(--ha-dialog-surface-backdrop-filter, none);
        background: var(
          --ha-dialog-surface-background,
          var(--mdc-theme-surface, #fff)
        );
      }
      :host([flexContent]) .mdc-dialog .mdc-dialog__content {
        display: flex;
        flex-direction: column;
      }
      .header_title {
        display: flex;
        align-items: center;
        direction: var(--direction);
      }
      .header_title span {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        display: block;
        padding-left: 4px;
      }
      .header_button {
        text-decoration: none;
        color: inherit;
        inset-inline-start: initial;
        inset-inline-end: -12px;
        direction: var(--direction);
      }
      .dialog-actions {
        inset-inline-start: initial !important;
        inset-inline-end: 0px !important;
        direction: var(--direction);
      }
    `))]}}]}}),n.M)},2383:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(40251),i(47021),i(57243)),r=i(50778),s=i(35359),d=i(11297),l=i(30137);i(10508);let c,u,h,v,p,m=e=>e;const g="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z";(0,a.Z)([(0,r.Mo)("ha-expansion-panel")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"expanded",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"outlined",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1,type:Boolean,reflect:!0})],key:"leftChevron",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1,type:Boolean,reflect:!0})],key:"noCollapse",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"secondary",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_showContent",value(){return this.expanded}},{kind:"field",decorators:[(0,r.IO)(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return(0,n.dy)(c||(c=m`
      <div class="top ${0}">
        <div
          id="summary"
          class=${0}
          @click=${0}
          @keydown=${0}
          @focus=${0}
          @blur=${0}
          role="button"
          tabindex=${0}
          aria-expanded=${0}
          aria-controls="sect1"
        >
          ${0}
          <slot name="header">
            <div class="header">
              ${0}
              <slot class="secondary" name="secondary">${0}</slot>
            </div>
          </slot>
          ${0}
          <slot name="icons"></slot>
        </div>
      </div>
      <div
        class="container ${0}"
        @transitionend=${0}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${0}
        tabindex="-1"
      >
        ${0}
      </div>
    `),(0,s.$)({expanded:this.expanded}),(0,s.$)({noCollapse:this.noCollapse}),this._toggleContainer,this._toggleContainer,this._focusChanged,this._focusChanged,this.noCollapse?-1:0,this.expanded,this.leftChevron&&!this.noCollapse?(0,n.dy)(u||(u=m`
                <ha-svg-icon
                  .path=${0}
                  class="summary-icon ${0}"
                ></ha-svg-icon>
              `),g,(0,s.$)({expanded:this.expanded})):"",this.header,this.secondary,this.leftChevron||this.noCollapse?"":(0,n.dy)(h||(h=m`
                <ha-svg-icon
                  .path=${0}
                  class="summary-icon ${0}"
                ></ha-svg-icon>
              `),g,(0,s.$)({expanded:this.expanded})),(0,s.$)({expanded:this.expanded}),this._handleTransitionEnd,!this.expanded,this._showContent?(0,n.dy)(v||(v=m`<slot></slot>`)):"")}},{kind:"method",key:"willUpdate",value:function(e){(0,o.Z)(i,"willUpdate",this,3)([e]),e.has("expanded")&&(this._showContent=this.expanded,setTimeout((()=>{this._container.style.overflow=this.expanded?"initial":"hidden"}),300))}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height"),this._container.style.overflow=this.expanded?"initial":"hidden",this._showContent=this.expanded}},{kind:"method",key:"_toggleContainer",value:async function(e){if(e.defaultPrevented)return;if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;if(e.preventDefault(),this.noCollapse)return;const t=!this.expanded;(0,d.B)(this,"expanded-will-change",{expanded:t}),this._container.style.overflow="hidden",t&&(this._showContent=!0,await(0,l.y)());const i=this._container.scrollHeight;this._container.style.height=`${i}px`,t||setTimeout((()=>{this._container.style.height="0px"}),0),this.expanded=t,(0,d.B)(this,"expanded-changed",{expanded:this.expanded})}},{kind:"method",key:"_focusChanged",value:function(e){this.noCollapse||this.shadowRoot.querySelector(".top").classList.toggle("focused","focus"===e.type)}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(p||(p=m`
    :host {
      display: block;
    }

    .top {
      display: flex;
      align-items: center;
      border-radius: var(--ha-card-border-radius, 12px);
    }

    .top.expanded {
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }

    .top.focused {
      background: var(--input-fill-color);
    }

    :host([outlined]) {
      box-shadow: none;
      border-width: 1px;
      border-style: solid;
      border-color: var(--outline-color);
      border-radius: var(--ha-card-border-radius, 12px);
    }

    .summary-icon {
      transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
      direction: var(--direction);
      margin-left: 8px;
      margin-inline-start: 8px;
      margin-inline-end: initial;
    }

    :host([leftchevron]) .summary-icon {
      margin-left: 0;
      margin-right: 8px;
      margin-inline-start: 0;
      margin-inline-end: 8px;
    }

    #summary {
      flex: 1;
      display: flex;
      padding: var(--expansion-panel-summary-padding, 0 8px);
      min-height: 48px;
      align-items: center;
      cursor: pointer;
      overflow: hidden;
      font-weight: 500;
      outline: none;
    }
    #summary.noCollapse {
      cursor: default;
    }

    .summary-icon.expanded {
      transform: rotate(180deg);
    }

    .header,
    ::slotted([slot="header"]) {
      flex: 1;
    }

    .container {
      padding: var(--expansion-panel-content-padding, 0 8px);
      overflow: hidden;
      transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
      height: 0px;
    }

    .container.expanded {
      height: auto;
    }

    .secondary {
      display: block;
      color: var(--secondary-text-color);
      font-size: 12px;
    }
  `))}}]}}),n.oi)},52158:function(e,t,i){var a=i(73577),o=(i(71695),i(47021),i(4918)),n=i(6394),r=i(57243),s=i(50778),d=i(35359),l=i(11297);let c,u,h=e=>e;(0,a.Z)([(0,s.Mo)("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return(0,r.dy)(c||(c=h` <div class="mdc-form-field ${0}">
      <slot></slot>
      <label class="mdc-label" @click=${0}>
        <slot name="label">${0}</slot>
      </label>
    </div>`),(0,d.$)(e),this._labelClick,this.label)}},{kind:"method",key:"_labelClick",value:function(){const e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,l.B)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,l.B)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value(){return[n.W,(0,r.iv)(u||(u=h`
      :host(:not([alignEnd])) ::slotted(ha-switch) {
        margin-right: 10px;
        margin-inline-end: 10px;
        margin-inline-start: inline;
      }
      .mdc-form-field {
        align-items: var(--ha-formfield-align-items, center);
        gap: 4px;
      }
      .mdc-form-field > label {
        direction: var(--direction);
        margin-inline-start: 0;
        margin-inline-end: auto;
        padding: 0;
      }
      :host([disabled]) label {
        color: var(--disabled-text-color);
      }
    `))]}}]}}),o.a)},54220:function(e,t,i){i.r(t),i.d(t,{HaIconNext:()=>s});var a=i(73577),o=(i(71695),i(47021),i(50778)),n=i(80155),r=i(10508);let s=(0,a.Z)([(0,o.Mo)("ha-icon-next")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)()],key:"path",value(){return"rtl"===n.E.document.dir?"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z":"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"}}]}}),r.HaSvgIcon)},74064:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(47021),i(65703)),r=i(46289),s=i(57243),d=i(50778);let l,c,u,h=e=>e;(0,a.Z)([(0,d.Mo)("ha-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,o.Z)(i,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[r.W,(0,s.iv)(l||(l=h`
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
          `)):(0,s.iv)(u||(u=h``))]}}]}}),n.K)},43972:function(e,t,i){var a=i(73577),o=(i(63721),i(71695),i(97499),i(13334),i(47021),i(2060),i(57243)),n=i(50778),r=i(20552),s=i(64364);i(54220),i(74064),i(10508);let d,l,c,u,h,v=e=>e;(0,a.Z)([(0,n.Mo)("ha-navigation-list")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"pages",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"has-secondary",type:Boolean})],key:"hasSecondary",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"method",key:"render",value:function(){return(0,o.dy)(d||(d=v`
      <mwc-list
        innerRole="menu"
        itemRoles="menuitem"
        innerAriaLabel=${0}
        @action=${0}
      >
        ${0}
      </mwc-list>
    `),(0,r.o)(this.label),this._handleListAction,this.pages.map((e=>(0,o.dy)(l||(l=v`
            <ha-list-item
              graphic="avatar"
              .twoline=${0}
              .hasMeta=${0}
            >
              <div
                slot="graphic"
                class=${0}
                .style="background-color: ${0}"
              >
                <ha-svg-icon .path=${0}></ha-svg-icon>
              </div>
              <span>${0}</span>
              ${0}
              ${0}
            </ha-list-item>
          `),this.hasSecondary,!this.narrow,e.iconColor?"icon-background":"",e.iconColor||"undefined",e.iconPath,e.name,this.hasSecondary?(0,o.dy)(c||(c=v`<span slot="secondary">${0}</span>`),e.description):"",this.narrow?"":(0,o.dy)(u||(u=v`<ha-icon-next slot="meta"></ha-icon-next>`))))))}},{kind:"method",key:"_handleListAction",value:function(e){const t=this.pages[e.detail.index].path;t.endsWith("#external-app-configuration")?this.hass.auth.external.fireMessage({type:"config_screen/show"}):(0,s.c)(t)}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(h||(h=v`
    :host {
      --mdc-list-vertical-padding: 0;
    }
    ha-svg-icon,
    ha-icon-next {
      color: var(--secondary-text-color);
      height: 24px;
      width: 24px;
      display: block;
    }
    ha-svg-icon {
      padding: 8px;
    }
    .icon-background {
      border-radius: 50%;
    }
    .icon-background ha-svg-icon {
      color: #fff;
    }
    ha-list-item {
      cursor: pointer;
      font-size: var(--navigation-list-item-title-font-size);
    }
  `))}}]}}),o.oi)},61631:function(e,t,i){var a=i(73577),o=(i(71695),i(47021),i(5601)),n=i(81577),r=i(57243),s=i(50778);let d,l=e=>e;(0,a.Z)([(0,s.Mo)("ha-radio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[n.W,(0,r.iv)(d||(d=l`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `))]}}]}}),o.J)},58130:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(40251),i(47021),i(60930)),r=i(9714),s=i(57243),d=i(50778),l=i(56587),c=i(30137);i(59897);let u,h,v,p,m=e=>e;(0,a.Z)([(0,d.Mo)("ha-select")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"icon",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean,reflect:!0})],key:"clearable",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({attribute:"inline-arrow",type:Boolean})],key:"inlineArrow",value(){return!1}},{kind:"method",key:"render",value:function(){return(0,s.dy)(u||(u=m`
      ${0}
      ${0}
    `),(0,o.Z)(i,"render",this,3)([]),this.clearable&&!this.required&&!this.disabled&&this.value?(0,s.dy)(h||(h=m`<ha-icon-button
            label="clear"
            @click=${0}
            .path=${0}
          ></ha-icon-button>`),this._clearValue,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):s.Ld)}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?(0,s.dy)(v||(v=m`<span class="mdc-select__icon"
      ><slot name="icon"></slot
    ></span>`)):s.Ld}},{kind:"method",key:"connectedCallback",value:function(){(0,o.Z)(i,"connectedCallback",this,3)([]),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"firstUpdated",value:async function(){var e;((0,o.Z)(i,"firstUpdated",this,3)([]),this.inlineArrow)&&(null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector(".mdc-select__selected-text-container"))||void 0===e||e.classList.add("inline-arrow"))}},{kind:"method",key:"updated",value:function(e){if((0,o.Z)(i,"updated",this,3)([e]),e.has("inlineArrow")){var t;const e=null===(t=this.shadowRoot)||void 0===t?void 0:t.querySelector(".mdc-select__selected-text-container");this.inlineArrow?null==e||e.classList.add("inline-arrow"):null==e||e.classList.remove("inline-arrow")}}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)(i,"disconnectedCallback",this,3)([]),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value(){return(0,l.D)((async()=>{await(0,c.y)(),this.layoutOptions()}),500)}},{kind:"field",static:!0,key:"styles",value(){return[r.W,(0,s.iv)(p||(p=m`
      :host([clearable]) {
        position: relative;
      }
      .mdc-select:not(.mdc-select--disabled) .mdc-select__icon {
        color: var(--secondary-text-color);
      }
      .mdc-select__anchor {
        width: var(--ha-select-min-width, 200px);
      }
      .mdc-select--filled .mdc-select__anchor {
        height: var(--ha-select-height, 56px);
      }
      .mdc-select--filled .mdc-floating-label {
        inset-inline-start: 12px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label {
        inset-inline-start: 48px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select .mdc-select__anchor {
        padding-inline-start: 12px;
        padding-inline-end: 0px;
        direction: var(--direction);
      }
      .mdc-select__anchor .mdc-floating-label--float-above {
        transform-origin: var(--float-start);
      }
      .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 0px);
      }
      :host([clearable]) .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 12px);
      }
      ha-icon-button {
        position: absolute;
        top: 10px;
        right: 28px;
        --mdc-icon-button-size: 36px;
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
        inset-inline-start: initial;
        inset-inline-end: 28px;
        direction: var(--direction);
      }
      .inline-arrow {
        flex-grow: 0;
      }
    `))]}}]}}),n.K)},35506:function(e,t,i){i.r(t),i.d(t,{HaNumberSelector:()=>p});var a=i(73577),o=(i(71695),i(11740),i(47021),i(57243)),n=i(50778),r=i(35359),s=i(11297);i(20663),i(97522),i(70596);let d,l,c,u,h,v=e=>e,p=(0,a.Z)([(0,n.Mo)("ha-selector-number")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Number})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Number})],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",key:"_valueStr",value(){return""}},{kind:"method",key:"willUpdate",value:function(e){e.has("value")&&(""!==this._valueStr&&this.value===Number(this._valueStr)||(this._valueStr=null==this.value||isNaN(this.value)?"":this.value.toString()))}},{kind:"method",key:"render",value:function(){var e,t,i,a,n,s,h,p,m,g,f,b,y,k;const _="box"===(null===(e=this.selector.number)||void 0===e?void 0:e.mode)||void 0===(null===(t=this.selector.number)||void 0===t?void 0:t.min)||void 0===(null===(i=this.selector.number)||void 0===i?void 0:i.max);let x;var $;if(!_&&(x=null!==($=this.selector.number.step)&&void 0!==$?$:1,"any"===x)){x=1;const e=(this.selector.number.max-this.selector.number.min)/100;for(;x>e;)x/=10}return(0,o.dy)(d||(d=v`
      ${0}
      <div class="input">
        ${0}
        <ha-textfield
          .inputMode=${0}
          .label=${0}
          .placeholder=${0}
          class=${0}
          .min=${0}
          .max=${0}
          .value=${0}
          .step=${0}
          helperPersistent
          .helper=${0}
          .disabled=${0}
          .required=${0}
          .suffix=${0}
          type="number"
          autoValidate
          ?no-spinner=${0}
          @input=${0}
        >
        </ha-textfield>
      </div>
      ${0}
    `),this.label&&!_?(0,o.dy)(l||(l=v`${0}${0}`),this.label,this.required?"*":""):o.Ld,_?o.Ld:(0,o.dy)(c||(c=v`
              <ha-slider
                labeled
                .min=${0}
                .max=${0}
                .value=${0}
                .step=${0}
                .disabled=${0}
                .required=${0}
                @change=${0}
                .ticks=${0}
              >
              </ha-slider>
            `),this.selector.number.min,this.selector.number.max,null!==(a=this.value)&&void 0!==a?a:"",x,this.disabled,this.required,this._handleSliderChange,null===(n=this.selector.number)||void 0===n?void 0:n.slider_ticks),"any"===(null===(s=this.selector.number)||void 0===s?void 0:s.step)||(null!==(h=null===(p=this.selector.number)||void 0===p?void 0:p.step)&&void 0!==h?h:1)%1!=0?"decimal":"numeric",_?this.label:void 0,this.placeholder,(0,r.$)({single:_}),null===(m=this.selector.number)||void 0===m?void 0:m.min,null===(g=this.selector.number)||void 0===g?void 0:g.max,null!==(f=this._valueStr)&&void 0!==f?f:"",null!==(b=null===(y=this.selector.number)||void 0===y?void 0:y.step)&&void 0!==b?b:1,_?this.helper:void 0,this.disabled,this.required,null===(k=this.selector.number)||void 0===k?void 0:k.unit_of_measurement,!_,this._handleInputChange,!_&&this.helper?(0,o.dy)(u||(u=v`<ha-input-helper-text>${0}</ha-input-helper-text>`),this.helper):o.Ld)}},{kind:"method",key:"_handleInputChange",value:function(e){e.stopPropagation(),this._valueStr=e.target.value;const t=""===e.target.value||isNaN(e.target.value)?void 0:Number(e.target.value);this.value!==t&&(0,s.B)(this,"value-changed",{value:t})}},{kind:"method",key:"_handleSliderChange",value:function(e){e.stopPropagation();const t=Number(e.target.value);this.value!==t&&(0,s.B)(this,"value-changed",{value:t})}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(h||(h=v`
    .input {
      display: flex;
      justify-content: space-between;
      align-items: center;
      direction: ltr;
    }
    ha-slider {
      flex: 1;
      margin-right: 16px;
      margin-inline-end: 16px;
      margin-inline-start: 0;
    }
    ha-textfield {
      --ha-textfield-input-width: 40px;
    }
    .single {
      --ha-textfield-input-width: unset;
      flex: 1;
    }
  `))}}]}}),o.oi)},51065:function(e,t,i){i.a(e,(async function(e,a){try{i.r(t),i.d(t,{HaSelectSelector:()=>D});var o=i(73577),n=(i(19083),i(71695),i(61893),i(84283),i(40251),i(61006),i(39527),i(99790),i(67670),i(41360),i(13334),i(36993),i(47021),i(87319),i(57243)),r=i(50778),s=i(91583),d=i(24785),l=i(11297),c=i(81036),u=i(32770),h=(i(84573),i(13978),i(76418),i(69484)),v=(i(52158),i(20663),i(61631),i(58130),i(14002),e([h]));h=(v.then?(await v)():v)[0];let p,m,g,f,b,y,k,_,x,$,w,C,L,S=e=>e;const B="M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z";let D=(0,o.Z)([(0,r.Mo)("ha-selector-select")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,r.IO)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"method",key:"_itemMoved",value:function(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail;this._move(t,i)}},{kind:"method",key:"_move",value:function(e,t){const i=this.value.concat(),a=i.splice(e,1)[0];i.splice(t,0,a),this.value=i,(0,l.B)(this,"value-changed",{value:i})}},{kind:"field",key:"_filter",value(){return""}},{kind:"method",key:"render",value:function(){var e,t,i,a,o,r,l,h,v,C;const L=(null===(e=this.selector.select)||void 0===e||null===(e=e.options)||void 0===e?void 0:e.map((e=>"object"==typeof e?e:{value:e,label:e})))||[],D=null===(t=this.selector.select)||void 0===t?void 0:t.translation_key;if(this.localizeValue&&D&&L.forEach((e=>{const t=this.localizeValue(`${D}.options.${e.value}`);t&&(e.label=t)})),null!==(i=this.selector.select)&&void 0!==i&&i.sort&&L.sort(((e,t)=>(0,u.f)(e.label,t.label,this.hass.locale.language))),!(null!==(a=this.selector.select)&&void 0!==a&&a.custom_value||null!==(o=this.selector.select)&&void 0!==o&&o.reorder||"list"!==this._mode)){var P;if(null===(P=this.selector.select)||void 0===P||!P.multiple)return(0,n.dy)(p||(p=S`
          <div>
            ${0}
            ${0}
          </div>
          ${0}
        `),this.label,L.map((e=>(0,n.dy)(m||(m=S`
                <ha-formfield
                  .label=${0}
                  .disabled=${0}
                >
                  <ha-radio
                    .checked=${0}
                    .value=${0}
                    .disabled=${0}
                    @change=${0}
                  ></ha-radio>
                </ha-formfield>
              `),e.label,e.disabled||this.disabled,e.value===this.value,e.value,e.disabled||this.disabled,this._valueChanged))),this._renderHelper());const e=this.value&&""!==this.value?(0,d.r)(this.value):[];return(0,n.dy)(g||(g=S`
        <div>
          ${0}
          ${0}
        </div>
        ${0}
      `),this.label,L.map((t=>(0,n.dy)(f||(f=S`
              <ha-formfield .label=${0}>
                <ha-checkbox
                  .checked=${0}
                  .value=${0}
                  .disabled=${0}
                  @change=${0}
                ></ha-checkbox>
              </ha-formfield>
            `),t.label,e.includes(t.value),t.value,t.disabled||this.disabled,this._checkboxChanged))),this._renderHelper())}if(null!==(r=this.selector.select)&&void 0!==r&&r.multiple){var M;const e=this.value&&""!==this.value?(0,d.r)(this.value):[],t=L.filter((t=>!(t.disabled||null!=e&&e.includes(t.value))));return(0,n.dy)(b||(b=S`
        ${0}

        <ha-combo-box
          item-value-path="value"
          item-label-path="label"
          .hass=${0}
          .label=${0}
          .helper=${0}
          .disabled=${0}
          .required=${0}
          .value=${0}
          .items=${0}
          .allowCustomValue=${0}
          @filter-changed=${0}
          @value-changed=${0}
          @opened-changed=${0}
        ></ha-combo-box>
      `),null!=e&&e.length?(0,n.dy)(y||(y=S`
              <ha-sortable
                no-style
                .disabled=${0}
                @item-moved=${0}
                handle-selector="button.primary.action"
              >
                <ha-chip-set>
                  ${0}
                </ha-chip-set>
              </ha-sortable>
            `),!this.selector.select.reorder,this._itemMoved,(0,s.r)(e,(e=>e),((e,t)=>{var i,a,o;const r=(null===(i=L.find((t=>t.value===e)))||void 0===i?void 0:i.label)||e;return(0,n.dy)(k||(k=S`
                        <ha-input-chip
                          .idx=${0}
                          @remove=${0}
                          .label=${0}
                          selected
                        >
                          ${0}
                          ${0}
                        </ha-input-chip>
                      `),t,this._removeItem,r,null!==(a=this.selector.select)&&void 0!==a&&a.reorder?(0,n.dy)(_||(_=S`
                                <ha-svg-icon
                                  slot="icon"
                                  .path=${0}
                                ></ha-svg-icon>
                              `),B):n.Ld,(null===(o=L.find((t=>t.value===e)))||void 0===o?void 0:o.label)||e)}))):n.Ld,this.hass,this.label,this.helper,this.disabled,this.required&&!e.length,"",t,null!==(M=this.selector.select.custom_value)&&void 0!==M&&M,this._filterChanged,this._comboBoxValueChanged,this._openedChanged)}if(null!==(l=this.selector.select)&&void 0!==l&&l.custom_value){void 0===this.value||Array.isArray(this.value)||L.find((e=>e.value===this.value))||L.unshift({value:this.value,label:this.value});const e=L.filter((e=>!e.disabled));return(0,n.dy)(x||(x=S`
        <ha-combo-box
          item-value-path="value"
          item-label-path="label"
          .hass=${0}
          .label=${0}
          .helper=${0}
          .disabled=${0}
          .required=${0}
          .items=${0}
          .value=${0}
          @filter-changed=${0}
          @value-changed=${0}
          @opened-changed=${0}
        ></ha-combo-box>
      `),this.hass,this.label,this.helper,this.disabled,this.required,e,this.value,this._filterChanged,this._comboBoxValueChanged,this._openedChanged)}return(0,n.dy)($||($=S`
      <ha-select
        fixedMenuPosition
        naturalMenuWidth
        .label=${0}
        .value=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        clearable
        @closed=${0}
        @selected=${0}
      >
        ${0}
      </ha-select>
    `),null!==(h=this.label)&&void 0!==h?h:"",null!==(v=this.value)&&void 0!==v?v:"",null!==(C=this.helper)&&void 0!==C?C:"",this.disabled,this.required,c.U,this._valueChanged,L.map((e=>(0,n.dy)(w||(w=S`
            <mwc-list-item .value=${0} .disabled=${0}
              >${0}</mwc-list-item
            >
          `),e.value,e.disabled,e.label))))}},{kind:"method",key:"_renderHelper",value:function(){return this.helper?(0,n.dy)(C||(C=S`<ha-input-helper-text>${0}</ha-input-helper-text>`),this.helper):""}},{kind:"get",key:"_mode",value:function(){var e,t;return(null===(e=this.selector.select)||void 0===e?void 0:e.mode)||(((null===(t=this.selector.select)||void 0===t||null===(t=t.options)||void 0===t?void 0:t.length)||0)<6?"list":"dropdown")}},{kind:"method",key:"_valueChanged",value:function(e){var t,i,a;if(e.stopPropagation(),-1===(null===(t=e.detail)||void 0===t?void 0:t.index)&&void 0!==this.value)return void(0,l.B)(this,"value-changed",{value:void 0});const o=(null===(i=e.detail)||void 0===i?void 0:i.value)||e.target.value;this.disabled||void 0===o||o===(null!==(a=this.value)&&void 0!==a?a:"")||(0,l.B)(this,"value-changed",{value:o})}},{kind:"method",key:"_checkboxChanged",value:function(e){if(e.stopPropagation(),this.disabled)return;let t;const i=e.target.value,a=e.target.checked,o=this.value&&""!==this.value?(0,d.r)(this.value):[];if(a){if(o.includes(i))return;t=[...o,i]}else{if(null==o||!o.includes(i))return;t=o.filter((e=>e!==i))}(0,l.B)(this,"value-changed",{value:t})}},{kind:"method",key:"_removeItem",value:async function(e){e.stopPropagation();const t=[...(0,d.r)(this.value)];t.splice(e.target.idx,1),(0,l.B)(this,"value-changed",{value:t}),await this.updateComplete,this._filterChanged()}},{kind:"method",key:"_comboBoxValueChanged",value:function(e){var t;e.stopPropagation();const i=e.detail.value;if(this.disabled||""===i)return;if(null===(t=this.selector.select)||void 0===t||!t.multiple)return void(0,l.B)(this,"value-changed",{value:i});const a=this.value&&""!==this.value?(0,d.r)(this.value):[];void 0!==i&&a.includes(i)||(setTimeout((()=>{this._filterChanged(),this.comboBox.setInputValue("")}),0),(0,l.B)(this,"value-changed",{value:[...a,i]}))}},{kind:"method",key:"_openedChanged",value:function(e){null!=e&&e.detail.value&&this._filterChanged()}},{kind:"method",key:"_filterChanged",value:function(e){var t,i;this._filter=(null==e?void 0:e.detail.value)||"";const a=null===(t=this.comboBox.items)||void 0===t?void 0:t.filter((e=>{var t;return(e.label||e.value).toLowerCase().includes(null===(t=this._filter)||void 0===t?void 0:t.toLowerCase())}));this._filter&&null!==(i=this.selector.select)&&void 0!==i&&i.custom_value&&a&&!a.some((e=>(e.label||e.value)===this._filter))&&a.unshift({label:this._filter,value:this._filter}),this.comboBox.filteredItems=a}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(L||(L=S`
    :host {
      position: relative;
    }
    ha-select,
    mwc-formfield,
    ha-formfield {
      display: block;
    }
    mwc-list-item[disabled] {
      --mdc-theme-text-primary-on-background: var(--disabled-text-color);
    }
    ha-chip-set {
      padding: 8px 0;
    }

    .sortable-fallback {
      display: none;
      opacity: 0;
    }

    .sortable-ghost {
      opacity: 0.4;
    }

    .sortable-drag {
      cursor: grabbing;
    }
  `))}}]}}),n.oi);a()}catch(p){a(p)}}))},59414:function(e,t,i){var a=i(73577),o=(i(71695),i(40251),i(19134),i(92519),i(42179),i(89256),i(24931),i(88463),i(57449),i(19814),i(97003),i(47021),i(57243)),n=i(50778),r=i(27486),s=i(38653),d=i(45634);let l,c=e=>e;const u={action:()=>Promise.all([i.e("8975"),i.e("6160"),i.e("1722"),i.e("7232"),i.e("1285"),i.e("5929"),i.e("2047"),i.e("5456"),i.e("7087"),i.e("3086"),i.e("2142"),i.e("8770")]).then(i.bind(i,2984)),addon:()=>i.e("1704").then(i.bind(i,4608)),area:()=>i.e("1663").then(i.bind(i,5491)),area_filter:()=>i.e("1720").then(i.bind(i,95318)),attribute:()=>Promise.all([i.e("1285"),i.e("6942")]).then(i.bind(i,56089)),assist_pipeline:()=>i.e("8714").then(i.bind(i,93697)),boolean:()=>i.e("3032").then(i.bind(i,37629)),color_rgb:()=>i.e("2751").then(i.bind(i,25369)),condition:()=>Promise.all([i.e("8975"),i.e("6160"),i.e("1722"),i.e("7232"),i.e("1285"),i.e("5929"),i.e("7087"),i.e("2846")]).then(i.bind(i,63781)),config_entry:()=>i.e("8133").then(i.bind(i,84023)),conversation_agent:()=>i.e("7615").then(i.bind(i,19778)),constant:()=>i.e("5828").then(i.bind(i,16079)),country:()=>i.e("9699").then(i.bind(i,52598)),date:()=>i.e("5832").then(i.bind(i,53372)),datetime:()=>i.e("3760").then(i.bind(i,7861)),device:()=>i.e("8660").then(i.bind(i,26784)),duration:()=>Promise.all([i.e("2047"),i.e("3334")]).then(i.bind(i,120)),entity:()=>Promise.all([i.e("6160"),i.e("1722"),i.e("3979")]).then(i.bind(i,92697)),statistic:()=>Promise.all([i.e("6160"),i.e("664")]).then(i.bind(i,76422)),file:()=>Promise.all([i.e("2311"),i.e("7097")]).then(i.bind(i,11838)),floor:()=>Promise.all([i.e("680"),i.e("9028")]).then(i.bind(i,19626)),label:()=>Promise.all([i.e("9009"),i.e("7137")]).then(i.bind(i,65326)),image:()=>Promise.all([i.e("2311"),i.e("5220"),i.e("7457")]).then(i.bind(i,7826)),background:()=>Promise.all([i.e("2311"),i.e("5220"),i.e("7473")]).then(i.bind(i,65735)),language:()=>i.e("2999").then(i.bind(i,37270)),navigation:()=>i.e("8586").then(i.bind(i,5808)),number:()=>Promise.resolve().then(i.bind(i,35506)),object:()=>Promise.all([i.e("7232"),i.e("5633")]).then(i.bind(i,54600)),qr_code:()=>Promise.all([i.e("3750"),i.e("2685")]).then(i.bind(i,34043)),select:()=>Promise.resolve().then(i.bind(i,51065)),selector:()=>i.e("538").then(i.bind(i,41533)),state:()=>i.e("4693").then(i.bind(i,99664)),backup_location:()=>i.e("592").then(i.bind(i,28838)),stt:()=>i.e("5010").then(i.bind(i,26674)),target:()=>Promise.all([i.e("7581"),i.e("6160"),i.e("1722"),i.e("2052")]).then(i.bind(i,34791)),template:()=>i.e("5012").then(i.bind(i,41581)),text:()=>Promise.resolve().then(i.bind(i,68565)),time:()=>i.e("9031").then(i.bind(i,93721)),icon:()=>i.e("1860").then(i.bind(i,2322)),media:()=>Promise.all([i.e("2142"),i.e("6997")]).then(i.bind(i,61527)),theme:()=>i.e("811").then(i.bind(i,29141)),button_toggle:()=>i.e("3185").then(i.bind(i,40515)),trigger:()=>Promise.all([i.e("8975"),i.e("6160"),i.e("1722"),i.e("7232"),i.e("1285"),i.e("5929"),i.e("5456"),i.e("7803")]).then(i.bind(i,14852)),tts:()=>i.e("1728").then(i.bind(i,19082)),tts_voice:()=>i.e("8713").then(i.bind(i,78393)),location:()=>i.e("6752").then(i.bind(i,68313)),color_temp:()=>Promise.all([i.e("2146"),i.e("6335")]).then(i.bind(i,88159)),ui_action:()=>Promise.all([i.e("3881"),i.e("7232"),i.e("3086"),i.e("189")]).then(i.bind(i,63599)),ui_color:()=>i.e("522").then(i.bind(i,5404)),ui_state_content:()=>Promise.all([i.e("4224"),i.e("4284"),i.e("4893")]).then(i.bind(i,65862))},h=new Set(["ui-action","ui-color"]);(0,a.Z)([(0,n.Mo)("ha-selector")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"name",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"focus",value:async function(){var e;await this.updateComplete,null===(e=this.renderRoot.querySelector("#selector"))||void 0===e||e.focus()}},{kind:"get",key:"_type",value:function(){const e=Object.keys(this.selector)[0];return h.has(e)?e.replace("-","_"):e}},{kind:"method",key:"willUpdate",value:function(e){var t;e.has("selector")&&this.selector&&(null===(t=u[this._type])||void 0===t||t.call(u))}},{kind:"field",key:"_handleLegacySelector",value(){return(0,r.Z)((e=>{if("entity"in e)return(0,d.CM)(e);if("device"in e)return(0,d.c9)(e);const t=Object.keys(this.selector)[0];return h.has(t)?{[t.replace("-","_")]:e[t]}:e}))}},{kind:"method",key:"render",value:function(){return(0,o.dy)(l||(l=c`
      ${0}
    `),(0,s.h)(`ha-selector-${this._type}`,{hass:this.hass,name:this.name,selector:this._handleLegacySelector(this.selector),value:this.value,label:this.label,placeholder:this.placeholder,disabled:this.disabled,required:this.required,helper:this.helper,context:this.context,localizeValue:this.localizeValue,id:"selector"}))}}]}}),o.oi)},18805:function(e,t,i){var a=i(73577),o=(i(71695),i(47021),i(57243)),n=i(50778);let r,s,d=e=>e;(0,a.Z)([(0,n.Mo)("ha-settings-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"slim",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"three-line"})],key:"threeLine",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"wrap-heading",reflect:!0})],key:"wrapHeading",value(){return!1}},{kind:"method",key:"render",value:function(){return(0,o.dy)(r||(r=d`
      <div class="prefix-wrap">
        <slot name="prefix"></slot>
        <div
          class="body"
          ?two-line=${0}
          ?three-line=${0}
        >
          <slot name="heading"></slot>
          <div class="secondary"><slot name="description"></slot></div>
        </div>
      </div>
      <div class="content"><slot></slot></div>
    `),!this.threeLine,this.threeLine)}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(s||(s=d`
    :host {
      display: flex;
      padding: 0 16px;
      align-content: normal;
      align-self: auto;
      align-items: center;
    }
    .body {
      padding-top: 8px;
      padding-bottom: 8px;
      padding-left: 0;
      padding-inline-start: 0;
      padding-right: 16px;
      padding-inline-end: 16px;
      overflow: hidden;
      display: var(--layout-vertical_-_display, flex);
      flex-direction: var(--layout-vertical_-_flex-direction, column);
      justify-content: var(--layout-center-justified_-_justify-content, center);
      flex: var(--layout-flex_-_flex, 1);
      flex-basis: var(--layout-flex_-_flex-basis, 0.000000001px);
    }
    .body[three-line] {
      min-height: var(--paper-item-body-three-line-min-height, 88px);
    }
    :host(:not([wrap-heading])) body > * {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .body > .secondary {
      display: block;
      padding-top: 4px;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      -webkit-font-smoothing: antialiased;
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      line-height: normal;
      color: var(--secondary-text-color);
    }
    .body[two-line] {
      min-height: calc(var(--paper-item-body-two-line-min-height, 72px) - 16px);
      flex: 1;
    }
    .content {
      display: contents;
    }
    :host(:not([narrow])) .content {
      display: var(--settings-row-content-display, flex);
      justify-content: flex-end;
      flex: 1;
      padding: 16px 0;
    }
    .content ::slotted(*) {
      width: var(--settings-row-content-width);
    }
    :host([narrow]) {
      align-items: normal;
      flex-direction: column;
      border-top: 1px solid var(--divider-color);
      padding-bottom: 8px;
    }
    ::slotted(ha-switch) {
      padding: 16px 0;
    }
    .secondary {
      white-space: normal;
    }
    .prefix-wrap {
      display: var(--settings-row-prefix-display);
    }
    :host([narrow]) .prefix-wrap {
      display: flex;
      align-items: center;
    }
    :host([slim]),
    :host([slim]) .content,
    :host([slim]) ::slotted(ha-switch) {
      padding: 0;
    }
    :host([slim]) .body {
      min-height: 0;
    }
  `))}}]}}),o.oi)},97522:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(47021),i(31875)),r=i(57243),s=i(50778),d=i(80155);let l,c=e=>e;(0,a.Z)([(0,s.Mo)("ha-slider")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"connectedCallback",value:function(){(0,o.Z)(i,"connectedCallback",this,3)([]),this.dir=d.E.document.dir}},{kind:"field",static:!0,key:"styles",value(){return[...(0,o.Z)(i,"styles",this),(0,r.iv)(l||(l=c`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-sys-color-on-primary: var(--text-primary-color);
        --md-sys-color-outline: var(--outline-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-slider-handle-width: 14px;
        --md-slider-handle-height: 14px;
        --md-slider-state-layer-size: 24px;
        min-width: 100px;
        min-inline-size: 100px;
        width: 200px;
      }
    `))]}}]}}),n.$)},14002:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(19423),i(40251),i(22139),i(39527),i(99790),i(47021),i(57243)),r=i(50778),s=i(11297);let d,l=e=>e;(0,a.Z)([(0,r.Mo)("ha-sortable")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",key:"_sortable",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"no-style"})],key:"noStyle",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:String,attribute:"draggable-selector"})],key:"draggableSelector",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:String,attribute:"handle-selector"})],key:"handleSelector",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:String,attribute:"filter"})],key:"filter",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:String})],key:"group",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"invert-swap"})],key:"invertSwap",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"rollback",value(){return!0}},{kind:"method",key:"updated",value:function(e){e.has("disabled")&&(this.disabled?this._destroySortable():this._createSortable())}},{kind:"field",key:"_shouldBeDestroy",value(){return!1}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)(a,"disconnectedCallback",this,3)([]),this._shouldBeDestroy=!0,setTimeout((()=>{this._shouldBeDestroy&&(this._destroySortable(),this._shouldBeDestroy=!1)}),1)}},{kind:"method",key:"connectedCallback",value:function(){(0,o.Z)(a,"connectedCallback",this,3)([]),this._shouldBeDestroy=!1,this.hasUpdated&&!this.disabled&&this._createSortable()}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"render",value:function(){return this.noStyle?n.Ld:(0,n.dy)(d||(d=l`
      <style>
        .sortable-fallback {
          display: none !important;
        }

        .sortable-ghost {
          box-shadow: 0 0 0 2px var(--primary-color);
          background: rgba(var(--rgb-primary-color), 0.25);
          border-radius: 4px;
          opacity: 0.4;
        }

        .sortable-drag {
          border-radius: 4px;
          opacity: 1;
          background: var(--card-background-color);
          box-shadow: 0px 4px 8px 3px #00000026;
          cursor: grabbing;
        }
      </style>
    `))}},{kind:"method",key:"_createSortable",value:async function(){if(this._sortable)return;const e=this.children[0];if(!e)return;const t=(await Promise.all([i.e("4153"),i.e("9358")]).then(i.bind(i,97659))).default,a=Object.assign(Object.assign({scroll:!0,forceAutoScrollFallback:!0,scrollSpeed:20,animation:150},this.options),{},{onChoose:this._handleChoose,onStart:this._handleStart,onEnd:this._handleEnd,onUpdate:this._handleUpdate,onAdd:this._handleAdd,onRemove:this._handleRemove});this.draggableSelector&&(a.draggable=this.draggableSelector),this.handleSelector&&(a.handle=this.handleSelector),void 0!==this.invertSwap&&(a.invertSwap=this.invertSwap),this.group&&(a.group=this.group),this.filter&&(a.filter=this.filter),this._sortable=new t(e,a)}},{kind:"field",key:"_handleUpdate",value(){return e=>{(0,s.B)(this,"item-moved",{newIndex:e.newIndex,oldIndex:e.oldIndex})}}},{kind:"field",key:"_handleAdd",value(){return e=>{(0,s.B)(this,"item-added",{index:e.newIndex,data:e.item.sortableData})}}},{kind:"field",key:"_handleRemove",value(){return e=>{(0,s.B)(this,"item-removed",{index:e.oldIndex})}}},{kind:"field",key:"_handleEnd",value(){return async e=>{(0,s.B)(this,"drag-end"),this.rollback&&e.item.placeholder&&(e.item.placeholder.replaceWith(e.item),delete e.item.placeholder)}}},{kind:"field",key:"_handleStart",value(){return()=>{(0,s.B)(this,"drag-start")}}},{kind:"field",key:"_handleChoose",value(){return e=>{this.rollback&&(e.item.placeholder=document.createComment("sort-placeholder"),e.item.after(e.item.placeholder))}}},{kind:"method",key:"_destroySortable",value:function(){this._sortable&&(this._sortable.destroy(),this._sortable=void 0)}}]}}),n.oi)},29939:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(47021),i(62523)),r=i(83835),s=i(57243),d=i(50778),l=i(26610);let c,u=e=>e;(0,a.Z)([(0,d.Mo)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"haptic",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){(0,o.Z)(i,"firstUpdated",this,3)([]),this.addEventListener("change",(()=>{this.haptic&&(0,l.j)("light")}))}},{kind:"field",static:!0,key:"styles",value(){return[r.W,(0,s.iv)(c||(c=u`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `))]}}]}}),n.H)},71656:function(e,t,i){i.d(t,{IO:()=>n,Lo:()=>o,a:()=>r});i(71695),i(92745),i(19423),i(47021);var a=i(32770);i(86912);const o=(e,t)=>e.callWS(Object.assign({type:"config/area_registry/create"},t)),n=(e,t,i)=>e.callWS(Object.assign({type:"config/area_registry/update",area_id:t},i)),r=(e,t)=>(i,o)=>{const n=t?t.indexOf(i):-1,r=t?t.indexOf(o):-1;if(-1===n&&-1===r){var s,d,l,c;const t=null!==(s=null==e||null===(d=e[i])||void 0===d?void 0:d.name)&&void 0!==s?s:i,n=null!==(l=null==e||null===(c=e[o])||void 0===c?void 0:c.name)&&void 0!==l?l:o;return(0,a.$)(t,n)}return-1===n?1:-1===r?-1:n-r}},92374:function(e,t,i){i.d(t,{jL:()=>o,R6:()=>r,HP:()=>s,t1:()=>n});i(71695),i(92745),i(61893),i(19423),i(92519),i(42179),i(89256),i(24931),i(88463),i(57449),i(19814),i(39527),i(99790),i(67670),i(47021);var a=i(73525);i(32770),i(56587);const o=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,o=e.states[t];if(o)return(0,a.C)(o)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device",{type:t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)}),n=(e,t,i)=>e.callWS(Object.assign({type:"config/device_registry/update",device_id:t},i)),r=e=>{const t={};for(const i of e)i.device_id&&(i.device_id in t||(t[i.device_id]=[]),t[i.device_id].push(i));return t},s=(e,t,i,a)=>{const o={};for(const n of t){const t=e[n.entity_id];null!=t&&t.domain&&null!==n.device_id&&(o[n.device_id]=o[n.device_id]||new Set,o[n.device_id].add(t.domain))}if(i&&a)for(const n of i)for(const e of n.config_entries){const t=a.find((t=>t.entry_id===e));null!=t&&t.domain&&(o[n.id]=o[n.id]||new Set,o[n.id].add(t.domain))}return o}},26610:function(e,t,i){i.d(t,{j:()=>o});var a=i(11297);const o=e=>{(0,a.B)(window,"haptic",e)}},45634:function(e,t,i){i.d(t,{CM:()=>k,QQ:()=>f,aV:()=>p,bq:()=>x,c9:()=>_,lE:()=>b,lV:()=>y,o1:()=>u,qJ:()=>g,qR:()=>h,vI:()=>m,xO:()=>v});var a=i(66374),o=(i(21414),i(19083),i(71695),i(92745),i(32126),i(19423),i(92519),i(42179),i(89256),i(24931),i(88463),i(57449),i(19814),i(61006),i(39527),i(99790),i(34810),i(41360),i(36993),i(47021),i(24785)),n=i(43420),r=i(4468),s=i(56395),d=i(92374);const l=["domain","integration","device_class"],c=["integration","manufacturer","model"],u=(e,t,i,a,o,n,r)=>{const s=[],d=[],l=[];return Object.values(i).forEach((i=>{i.labels.includes(t)&&m(e,o,a,i.area_id,n,r)&&l.push(i.area_id)})),Object.values(a).forEach((i=>{i.labels.includes(t)&&g(e,Object.values(o),i,n,r)&&d.push(i.id)})),Object.values(o).forEach((i=>{i.labels.includes(t)&&f(e.states[i.entity_id],n,r)&&s.push(i.entity_id)})),{areas:l,devices:d,entities:s}},h=(e,t,i,a,o)=>{const n=[];return Object.values(i).forEach((i=>{i.floor_id===t&&m(e,e.entities,e.devices,i.area_id,a,o)&&n.push(i.area_id)})),{areas:n}},v=(e,t,i,a,o,n)=>{const r=[],s=[];return Object.values(i).forEach((i=>{i.area_id===t&&g(e,Object.values(a),i,o,n)&&s.push(i.id)})),Object.values(a).forEach((i=>{i.area_id===t&&f(e.states[i.entity_id],o,n)&&r.push(i.entity_id)})),{devices:s,entities:r}},p=(e,t,i,a,o)=>{const n=[];return Object.values(i).forEach((i=>{i.device_id===t&&f(e.states[i.entity_id],a,o)&&n.push(i.entity_id)})),{entities:n}},m=(e,t,i,a,o,n)=>!!Object.values(i).some((i=>!(i.area_id!==a||!g(e,Object.values(t),i,o,n))))||Object.values(t).some((t=>!(t.area_id!==a||!f(e.states[t.entity_id],o,n)))),g=(e,t,i,a,n)=>{var r,s;const l=n?(0,d.HP)(n,t):void 0;if(null!==(r=a.target)&&void 0!==r&&r.device&&!(0,o.r)(a.target.device).some((e=>b(e,i,l))))return!1;if(null!==(s=a.target)&&void 0!==s&&s.entity){return t.filter((e=>e.device_id===i.id)).some((t=>{const i=e.states[t.entity_id];return f(i,a,n)}))}return!0},f=(e,t,i)=>{var a;return null===(a=t.target)||void 0===a||!a.entity||(0,o.r)(t.target.entity).some((t=>y(t,e,i)))},b=(e,t,i)=>{const{manufacturer:a,model:o,integration:n}=e;if(a&&t.manufacturer!==a)return!1;if(o&&t.model!==o)return!1;var r;if(n&&i&&(null==i||null===(r=i[t.id])||void 0===r||!r.has(n)))return!1;return!0},y=(e,t,i)=>{var a;const{domain:s,device_class:d,supported_features:l,integration:c}=e;if(s){const e=(0,n.N)(t);if(Array.isArray(s)?!s.includes(e):e!==s)return!1}if(d){const e=t.attributes.device_class;if(e&&Array.isArray(d)?!d.includes(e):e!==d)return!1}return!(l&&!(0,o.r)(l).some((e=>(0,r.e)(t,e))))&&(!c||(null==i||null===(a=i[t.entity_id])||void 0===a?void 0:a.domain)===c)},k=e=>{if(!e.entity)return{entity:null};if("filter"in e.entity)return e;const t=e.entity,{domain:i,integration:o,device_class:n}=t,r=(0,a.Z)(t,l);return i||o||n?{entity:Object.assign(Object.assign({},r),{},{filter:{domain:i,integration:o,device_class:n}})}:{entity:r}},_=e=>{if(!e.device)return{device:null};if("filter"in e.device)return e;const t=e.device,{integration:i,manufacturer:o,model:n}=t,r=(0,a.Z)(t,c);return i||o||n?{device:Object.assign(Object.assign({},r),{},{filter:{integration:i,manufacturer:o,model:n}})}:{device:r}},x=e=>{let t;var i;if("target"in e)t=(0,o.r)(null===(i=e.target)||void 0===i?void 0:i.entity);else if("entity"in e){var a,n;if(null!==(a=e.entity)&&void 0!==a&&a.include_entities)return;t=(0,o.r)(null===(n=e.entity)||void 0===n?void 0:n.filter)}if(!t)return;const r=t.flatMap((e=>e.integration||e.device_class||e.supported_features||!e.domain?[]:(0,o.r)(e.domain).filter((e=>(0,s.X)(e)))));return[...new Set(r)]}},86912:function(e,t,i){i(61893),i(32770),i(56587)},68455:function(e,t,i){i.r(t);var a=i(73577),o=(i(71695),i(47021),i(57243)),n=i(50778),r=(i(90977),i(92500),i(89654),i(66193));let s,d,l,c,u,h,v=e=>e;(0,a.Z)([(0,n.Mo)("hass-loading-screen")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"no-toolbar"})],key:"noToolbar",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"rootnav",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)()],key:"message",value:void 0},{kind:"method",key:"render",value:function(){var e;return(0,o.dy)(s||(s=v`
      ${0}
      <div class="content">
        <ha-circular-progress indeterminate></ha-circular-progress>
        ${0}
      </div>
    `),this.noToolbar?"":(0,o.dy)(d||(d=v`<div class="toolbar">
            ${0}
          </div>`),this.rootnav||null!==(e=history.state)&&void 0!==e&&e.root?(0,o.dy)(l||(l=v`
                  <ha-menu-button
                    .hass=${0}
                    .narrow=${0}
                  ></ha-menu-button>
                `),this.hass,this.narrow):(0,o.dy)(c||(c=v`
                  <ha-icon-button-arrow-prev
                    .hass=${0}
                    @click=${0}
                  ></ha-icon-button-arrow-prev>
                `),this.hass,this._handleBack)),this.message?(0,o.dy)(u||(u=v`<div id="loading-text">${0}</div>`),this.message):o.Ld)}},{kind:"method",key:"_handleBack",value:function(){history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[r.Qx,(0,o.iv)(h||(h=v`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }
        .toolbar {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: var(--header-height);
          padding: 8px 12px;
          pointer-events: none;
          background-color: var(--app-header-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar {
            padding: 4px;
          }
        }
        ha-menu-button,
        ha-icon-button-arrow-prev {
          pointer-events: auto;
        }
        .content {
          height: calc(100% - var(--header-height));
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        #loading-text {
          max-width: 350px;
          margin-top: 16px;
        }
      `))]}}]}}),o.oi)},51728:function(e,t,i){var a=i(73577),o=(i(71695),i(47021),i(57243)),n=i(50778),r=i(82283),s=(i(92500),i(89654),i(66193));let d,l,c,u,h,v=e=>e;(0,a.Z)([(0,n.Mo)("hass-subpage")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,r.i)(".content")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"render",value:function(){var e;return(0,o.dy)(d||(d=v`
      <div class="toolbar">
        ${0}

        <div class="main-title"><slot name="header">${0}</slot></div>
        <slot name="toolbar-icon"></slot>
      </div>
      <div class="content ha-scrollbar" @scroll=${0}>
        <slot></slot>
      </div>
      <div id="fab">
        <slot name="fab"></slot>
      </div>
    `),this.mainPage||null!==(e=history.state)&&void 0!==e&&e.root?(0,o.dy)(l||(l=v`
              <ha-menu-button
                .hassio=${0}
                .hass=${0}
                .narrow=${0}
              ></ha-menu-button>
            `),this.supervisor,this.hass,this.narrow):this.backPath?(0,o.dy)(c||(c=v`
                <a href=${0}>
                  <ha-icon-button-arrow-prev
                    .hass=${0}
                  ></ha-icon-button-arrow-prev>
                </a>
              `),this.backPath,this.hass):(0,o.dy)(u||(u=v`
                <ha-icon-button-arrow-prev
                  .hass=${0}
                  @click=${0}
                ></ha-icon-button-arrow-prev>
              `),this.hass,this._backTapped),this.header,this._saveScrollPos)}},{kind:"method",decorators:[(0,n.hO)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[s.$c,(0,o.iv)(h||(h=v`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
          overflow: hidden;
          position: relative;
        }

        :host([narrow]) {
          width: 100%;
          position: fixed;
        }

        .toolbar {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: var(--header-height);
          padding: 8px 12px;
          background-color: var(--app-header-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar {
            padding: 4px;
          }
        }
        .toolbar a {
          color: var(--sidebar-text-color);
          text-decoration: none;
        }

        ha-menu-button,
        ha-icon-button-arrow-prev,
        ::slotted([slot="toolbar-icon"]) {
          pointer-events: auto;
          color: var(--sidebar-icon-color);
        }

        .main-title {
          margin: var(--margin-title);
          line-height: 20px;
          min-width: 0;
          flex-grow: 1;
          overflow-wrap: break-word;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          text-overflow: ellipsis;
          padding-bottom: 1px;
        }

        .content {
          position: relative;
          width: 100%;
          height: calc(100% - 1px - var(--header-height));
          overflow-y: auto;
          overflow: auto;
          -webkit-overflow-scrolling: touch;
        }

        #fab {
          position: absolute;
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
      `))]}}]}}),o.oi)},88233:function(e,t,i){i.d(t,{E:()=>n});i(71695),i(40251),i(47021);var a=i(11297);const o=()=>Promise.all([i.e("2311"),i.e("6160"),i.e("1722"),i.e("5220"),i.e("9009"),i.e("680"),i.e("6835")]).then(i.bind(i,40600)),n=(e,t)=>{(0,a.B)(e,"show-dialog",{dialogTag:"dialog-area-registry-detail",dialogImport:o,dialogParams:t})}},56395:function(e,t,i){i.d(t,{X:()=>a});const a=(0,i(95907).z)(["input_boolean","input_button","input_text","input_number","input_datetime","input_select","counter","timer","schedule"])},68212:function(e,t,i){i(68212);Element.prototype.toggleAttribute||(Element.prototype.toggleAttribute=function(e,t){return void 0!==t&&(t=!!t),this.hasAttribute(e)?!!t||(this.removeAttribute(e),!1):!1!==t&&(this.setAttribute(e,""),!0)})},60085:function(e,t,i){i.a(e,(async function(e,a){try{i.d(t,{I:()=>v});i(39527),i(67670);var o=i(57243),n=(i(17949),i(1192),i(2383),i(51065)),r=(i(68565),i(18805),i(65414)),s=i(24394),d=i(6480),l=e([n,r,s]);[n,r,s]=l.then?(await l)():l;let c,u,h=e=>e;const v=(e,t,i,a)=>{var n,r;const s=t.device_info?(0,d.Q8)(e,t.device_info):void 0,l=s?null!==(n=s.name_by_user)&&void 0!==n?n:s.name:"",v=null==a?void 0:a.find((e=>!e.path||0===e.path.length));return(0,o.dy)(c||(c=h`
    <ha-card outlined>
      <h1 class="card-header">Entity configuration</h1>
      <p class="card-content">Home Assistant specific settings.</p>
      ${0}
      <ha-settings-row narrow>
        <div slot="heading">Device</div>
        <div slot="description">A device allows to group multiple entities.</div>
        <knx-device-picker
          .hass=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
        ></knx-device-picker>
      </ha-settings-row>
      <ha-settings-row narrow>
        <div slot="heading">Name</div>
        <div slot="description">Name of the entity.</div>
        <ha-selector-text
          .hass=${0}
          .label=${0}
          .required=${0}
          .selector=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
        ></ha-selector-text>
      </ha-settings-row>
      <ha-expansion-panel .header=${0} outlined>
        <ha-selector-select
          .hass=${0}
          .label=${0}
          .helper=${0}
          .required=${0}
          .selector=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
        ></ha-selector-select>
      </ha-expansion-panel>
    </ha-card>
  `),a&&v?(0,o.dy)(u||(u=h`<ha-alert
              .alertType=${0}
              .title=${0}
            ></ha-alert>`),"error",v.error_message):o.Ld,e,"device_info",null!==(r=t.device_info)&&void 0!==r?r:void 0,i,e,"Name",!s,{text:{type:"text",prefix:l}},"name",t.name,i,"Advanced",e,"Entity category","Leave empty for standard behaviour.",!1,{select:{multiple:!1,custom_value:!1,mode:"dropdown",options:[{value:"config",label:"Config"},{value:"diagnostic",label:"Diagnostic"}]}},"entity_category",t.entity_category,i)};a()}catch(c){a(c)}}))},15716:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),o=i(72621),n=(i(63721),i(71695),i(92551),i(19134),i(47706),i(39527),i(67670),i(13334),i(36993),i(47021),i(71513),i(75656),i(50100),i(18084),i(57243)),r=i(50778),s=i(46799),d=(i(1192),i(9388),i(10508),i(2383),i(59414),i(18805),i(80155)),l=i(11297),c=i(53926),u=(i(43522),i(65414)),h=i(60085),v=i(57586),p=i(2583),m=e([c,u,h]);[c,u,h]=m.then?(await m)():m;let g,f,b,y,k,_,x,$,w,C,L,S=e=>e;const B=new v.r("knx-configure-entity");(0,a.Z)([(0,r.Mo)("knx-configure-entity")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"platform",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"config",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array})],key:"schema",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"validationErrors",value:void 0},{kind:"method",key:"connectedCallback",value:function(){if((0,o.Z)(i,"connectedCallback",this,3)([]),!this.config){this.config={entity:{},knx:{}};const e=new URLSearchParams(d.E.location.search);this._url_suggestions=Object.fromEntries(e.entries());for(const[t,i]of Object.entries(this._url_suggestions))this._setNestedValue(t,i),(0,l.B)(this,"knx-entity-configuration-changed",this.config)}}},{kind:"method",key:"_setNestedValue",value:function(e,t){const i=e.split("."),a=i.pop();if(!a)return;let o=this.config;for(const n of i)n in o||(o[n]={}),o=o[n];o[a]=t}},{kind:"method",key:"render",value:function(){var e;const t=(0,p._)(this.validationErrors,"data");return(0,n.dy)(g||(g=S`
      <div class="header">
        <h1>
          <ha-svg-icon
            .path=${0}
            style=${0}
          ></ha-svg-icon>
          ${0}
        </h1>
        <p>${0}</p>
      </div>
      <slot name="knx-validation-error"></slot>
      <ha-card outlined>
        <h1 class="card-header">KNX configuration</h1>
        ${0}
      </ha-card>
      ${0}
    `),this.platform.iconPath,(0,s.V)({"background-color":this.platform.color}),this.platform.name,this.platform.description,this.generateRootGroups(this.platform.schema,(0,p._)(t,"knx")),(0,h.I)(this.hass,null!==(e=this.config.entity)&&void 0!==e?e:{},this._updateConfig("entity"),(0,p._)(t,"entity")))}},{kind:"method",key:"generateRootGroups",value:function(e,t){return(0,n.dy)(f||(f=S`
      ${0}
    `),e.map((e=>this._generateSettingsGroup(e,t))))}},{kind:"method",key:"_generateSettingsGroup",value:function(e,t){return!0===e.collapsible?(0,n.dy)(b||(b=S` <ha-expansion-panel
        outlined
        .header=${0}
        .secondary=${0}
        .expanded=${0}
        >${0}
      </ha-expansion-panel>`),e.heading,e.description,this._groupHasGroupAddressInConfig(e),this._generateItems(e.selectors,t)):(0,n.dy)(y||(y=S` <ha-settings-row narrow>
      <div slot="heading">${0}</div>
      <div slot="description">${0}</div>
      ${0}
    </ha-settings-row>`),e.heading,e.description,this._generateItems(e.selectors,t))}},{kind:"method",key:"_groupHasGroupAddressInConfig",value:function(e){return void 0!==this.config&&e.selectors.some((e=>"group_address"===e.type?this._hasGroupAddressInConfig(e,this.config.knx):"group_select"===e.type&&e.options.some((e=>e.schema.some((e=>"settings_group"===e.type?this._groupHasGroupAddressInConfig(e):"group_address"===e.type&&this._hasGroupAddressInConfig(e,this.config.knx)))))))}},{kind:"method",key:"_hasGroupAddressInConfig",value:function(e,t){var i;if(!(e.name in t))return!1;const a=t[e.name];return void 0!==a.write||(void 0!==a.state||!(null===(i=a.passive)||void 0===i||!i.length))}},{kind:"method",key:"_generateItems",value:function(e,t){return(0,n.dy)(k||(k=S`${0}`),e.map((e=>this._generateItem(e,t))))}},{kind:"method",key:"_generateItem",value:function(e,t){var i,a;switch(e.type){case"group_address":return(0,n.dy)(_||(_=S`
          <knx-group-address-selector
            .hass=${0}
            .knx=${0}
            .key=${0}
            .label=${0}
            .config=${0}
            .options=${0}
            .validationErrors=${0}
            @value-changed=${0}
          ></knx-group-address-selector>
        `),this.hass,this.knx,e.name,e.label,null!==(i=this.config.knx[e.name])&&void 0!==i?i:{},e.options,(0,p._)(t,e.name),this._updateConfig("knx"));case"selector":return(0,n.dy)(x||(x=S`
          <knx-selector-row
            .hass=${0}
            .key=${0}
            .selector=${0}
            .value=${0}
            @value-changed=${0}
          ></knx-selector-row>
        `),this.hass,e.name,e,this.config.knx[e.name],this._updateConfig("knx"));case"sync_state":return(0,n.dy)($||($=S`
          <knx-sync-state-selector-row
            .hass=${0}
            .key=${0}
            .value=${0}
            .noneValid=${0}
            @value-changed=${0}
          ></knx-sync-state-selector-row>
        `),this.hass,e.name,null===(a=this.config.knx[e.name])||void 0===a||a,!1,this._updateConfig("knx"));case"group_select":return this._generateGroupSelect(e,t);default:return B.error("Unknown selector type",e),n.Ld}}},{kind:"method",key:"_generateGroupSelect",value:function(e,t){var i;const a=null!==(i=this.config.knx[e.name])&&void 0!==i?i:this.config.knx[e.name]=e.options[0].value,o=e.options.find((e=>e.value===a));return void 0===o&&B.error("No option found for value",a),(0,n.dy)(w||(w=S` <ha-control-select
        .options=${0}
        .value=${0}
        .key=${0}
        @value-changed=${0}
      ></ha-control-select>
      ${0}`),e.options,a,e.name,this._updateConfig("knx"),o?(0,n.dy)(C||(C=S` <p class="group-description">${0}</p>
            <div class="group-selection">
              ${0}
            </div>`),o.description,o.schema.map((e=>"settings_group"===e.type?this._generateSettingsGroup(e,t):this._generateItem(e,t)))):n.Ld)}},{kind:"method",key:"_updateConfig",value:function(e){return t=>{t.stopPropagation(),this.config[e]||(this.config[e]={}),void 0===t.detail.value?(B.debug(`remove ${e} key "${t.target.key}"`),delete this.config[e][t.target.key]):(B.debug(`update ${e} key "${t.target.key}" with "${t.detail.value}"`),this.config[e][t.target.key]=t.detail.value),(0,l.B)(this,"knx-entity-configuration-changed",this.config),this.requestUpdate()}}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(L||(L=S`
    p {
      color: var(--secondary-text-color);
    }

    .header {
      color: var(--ha-card-header-color, --primary-text-color);
      font-family: var(--ha-card-header-font-family, inherit);
      padding: 0 16px 16px;

      & h1 {
        display: inline-flex;
        align-items: center;
        font-size: 26px;
        letter-spacing: -0.012em;
        line-height: 48px;
        font-weight: normal;
        margin-bottom: 14px;

        & ha-svg-icon {
          color: var(--text-primary-color);
          padding: 8px;
          background-color: var(--blue-color);
          border-radius: 50%;
          margin-right: 8px;
        }
      }

      & p {
        margin-top: -8px;
        line-height: 24px;
      }
    }

    ::slotted(ha-alert) {
      margin-top: 0 !important;
    }

    ha-card {
      margin-bottom: 24px;
      padding: 16px;

      & .card-header {
        display: inline-flex;
        align-items: center;
      }
    }

    ha-expansion-panel {
      margin-bottom: 16px;
    }
    ha-expansion-panel > :first-child:not(ha-settings-row) {
      margin-top: 16px; /* ha-settings-row has this margin internally */
    }
    ha-expansion-panel > ha-settings-row:first-child,
    ha-expansion-panel > knx-selector-row:first-child {
      border: 0;
    }

    ha-settings-row {
      margin-bottom: 8px;
      padding: 0;
    }
    ha-control-select {
      padding: 0;
      margin-bottom: 16px;
    }

    .group-description {
      align-items: center;
      margin-top: -8px;
      padding-left: 8px;
      padding-bottom: 8px;
    }

    .group-selection {
      padding-left: 16px;
      padding-right: 16px;
      & ha-settings-row:first-child {
        border-top: 0;
      }
    }

    knx-group-address-selector,
    ha-selector,
    ha-selector-text,
    ha-selector-select,
    knx-sync-state-selector-row,
    knx-device-picker {
      display: block;
      margin-bottom: 16px;
    }

    ha-alert {
      display: block;
      margin: 20px auto;
      max-width: 720px;

      & summary {
        padding: 10px;
      }
    }
  `))}}]}}),n.oi);t()}catch(g){t(g)}}))},24394:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),o=(i(19083),i(71695),i(61893),i(40251),i(39527),i(67670),i(13334),i(47021),i(57243)),n=i(50778),r=i(35359),s=i(27486),d=i(69484),l=(i(74064),i(46928)),c=i(11297),u=i(59848),h=i(32770),v=i(6480),p=e([d,l]);[d,l]=p.then?(await p)():p;let m,g,f,b=e=>e;const y=e=>(0,o.dy)(m||(m=b`<ha-list-item
    class=${0}
    .twoline=${0}
  >
    <span>${0}</span>
    <span slot="secondary">${0}</span>
  </ha-list-item>`),(0,r.$)({"add-new":"add_new"===e.id}),!!e.area,e.name,e.area);(0,a.Z)([(0,n.Mo)("knx-device-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.IO)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_showCreateDeviceDialog",value(){return!1}},{kind:"field",key:"_deviceId",value:void 0},{kind:"field",key:"_suggestion",value:void 0},{kind:"field",key:"_init",value(){return!1}},{kind:"field",key:"_getDevices",value(){return(0,s.Z)(((e,t)=>[{id:"add_new",name:"Add new device…",area:"",strings:[]},...e.map((e=>{var i,a;const o=null!==(i=null!==(a=e.name_by_user)&&void 0!==a?a:e.name)&&void 0!==i?i:"";return{id:e.id,identifier:(0,v.cG)(e),name:o,area:e.area_id&&t[e.area_id]?t[e.area_id].name:this.hass.localize("ui.components.device-picker.no_area"),strings:[o||""]}})).sort(((e,t)=>(0,h.$)(e.name||"",t.name||"",this.hass.locale.language)))]))}},{kind:"method",key:"_addDevice",value:async function(e){const t=[...(0,v.kc)(this.hass),e],i=this._getDevices(t,this.hass.areas);this.comboBox.items=i,this.comboBox.filteredItems=i,await this.updateComplete,await this.comboBox.updateComplete}},{kind:"method",key:"open",value:async function(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.open())}},{kind:"method",key:"focus",value:async function(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.focus())}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){var t;this._init=!0;const e=this._getDevices((0,v.kc)(this.hass),this.hass.areas),i=this.value?null===(t=e.find((e=>e.identifier===this.value)))||void 0===t?void 0:t.id:void 0;this.comboBox.value=i,this._deviceId=i,this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){return(0,o.dy)(g||(g=b`
      <ha-combo-box
        .hass=${0}
        .label=${0}
        .value=${0}
        .renderer=${0}
        item-id-path="id"
        item-value-path="id"
        item-label-path="name"
        @filter-changed=${0}
        @opened-changed=${0}
        @value-changed=${0}
      ></ha-combo-box>
      ${0}
    `),this.hass,void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):this.label,this._deviceId,y,this._filterChanged,this._openedChanged,this._deviceChanged,this._showCreateDeviceDialog?this._renderCreateDeviceDialog():o.Ld)}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.target,i=e.detail.value;if(!i)return void(this.comboBox.filteredItems=this.comboBox.items);const a=(0,u.q)(i,t.items||[]);this._suggestion=i,this.comboBox.filteredItems=[...a,{id:"add_new_suggestion",name:`Add new device '${this._suggestion}'`}]}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();let t=e.detail.value;"no_devices"===t&&(t=""),["add_new_suggestion","add_new"].includes(t)?(e.target.value=this._deviceId,this._openCreateDeviceDialog()):t!==this._deviceId&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){const t=this.comboBox.items.find((t=>t.id===e)),i=null==t?void 0:t.identifier;this.value=i,this._deviceId=null==t?void 0:t.id,setTimeout((()=>{(0,c.B)(this,"value-changed",{value:i}),(0,c.B)(this,"change")}),0)}},{kind:"method",key:"_renderCreateDeviceDialog",value:function(){return(0,o.dy)(f||(f=b`
      <knx-device-create-dialog
        .hass=${0}
        @create-device-dialog-closed=${0}
        .deviceName=${0}
      ></knx-device-create-dialog>
    `),this.hass,this._closeCreateDeviceDialog,this._suggestion)}},{kind:"method",key:"_openCreateDeviceDialog",value:function(){this._showCreateDeviceDialog=!0}},{kind:"method",key:"_closeCreateDeviceDialog",value:async function(e){const t=e.detail.newDevice;t?await this._addDevice(t):this.comboBox.setInputValue(""),this._setValue(null==t?void 0:t.id),this._suggestion=void 0,this._showCreateDeviceDialog=!1}}]}}),o.oi);t()}catch(m){t(m)}}))},13905:function(e,t,i){var a=i(73577),o=(i(63721),i(71695),i(13334),i(47021),i(57243)),n=i(50778),r=(i(52158),i(61631),i(11297));let s,d,l,c,u,h=e=>e;(0,a.Z)([(0,n.Mo)("knx-dpt-selector")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({type:Array})],key:"options",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"invalid",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"invalidMessage",value:void 0},{kind:"method",key:"render",value:function(){var e;return(0,o.dy)(s||(s=h`
      <div>
        ${0}
        ${0}
        ${0}
      </div>
    `),null!==(e=this.label)&&void 0!==e?e:o.Ld,this.options.map((e=>(0,o.dy)(d||(d=h`
            <div class="formfield">
              <ha-radio
                .checked=${0}
                .value=${0}
                .disabled=${0}
                @change=${0}
              ></ha-radio>
              <label .value=${0} @click=${0}>
                <p>${0}</p>
                ${0}
              </label>
            </div>
          `),e.value===this.value,e.value,this.disabled,this._valueChanged,e.value,this._valueChanged,e.label,e.description?(0,o.dy)(l||(l=h`<p class="secondary">${0}</p>`),e.description):o.Ld))),this.invalidMessage?(0,o.dy)(c||(c=h`<p class="invalid-message">${0}</p>`),this.invalidMessage):o.Ld)}},{kind:"method",key:"_valueChanged",value:function(e){var t;e.stopPropagation();const i=e.target.value;this.disabled||void 0===i||i===(null!==(t=this.value)&&void 0!==t?t:"")||(0,r.B)(this,"value-changed",{value:i})}},{kind:"field",static:!0,key:"styles",value(){return[(0,o.iv)(u||(u=h`
      :host([invalid]) div {
        color: var(--error-color);
      }

      .formfield {
        display: flex;
        align-items: center;
      }

      label {
        min-width: 200px; /* to make it easier to click */
      }

      p {
        pointer-events: none;
        color: var(--primary-text-color);
        margin: 0px;
      }

      .secondary {
        padding-top: 4px;
        font-family: var(
          --mdc-typography-body2-font-family,
          var(--mdc-typography-font-family, Roboto, sans-serif)
        );
        -webkit-font-smoothing: antialiased;
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        font-weight: var(--mdc-typography-body2-font-weight, 400);
        line-height: normal;
        color: var(--secondary-text-color);
      }

      .invalid-message {
        font-size: 0.75rem;
        color: var(--error-color);
        padding-left: 16px;
      }
    `))]}}]}}),o.oi)},53926:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),o=i(72621),n=(i(19083),i(71695),i(19423),i(40251),i(61006),i(39527),i(92181),i(99790),i(67670),i(41360),i(13334),i(47021),i(57243)),r=i(50778),s=i(35359),d=i(60738),l=(i(74064),i(51065)),c=(i(59897),i(11297)),u=(i(13905),i(10194)),h=i(97409),v=i(2583),p=e([l]);l=(p.then?(await p)():p)[0];let m,g,f,b,y,k=e=>e;const _="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z",x="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z",$=e=>e.map((e=>({value:e.address,label:`${e.address} - ${e.name}`})));(0,a.Z)([(0,r.Mo)("knx-group-address-selector")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.F_)({context:u.R,subscribe:!0})],key:"_dragDropContext",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"config",value(){return{}}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,r.Cb)({reflect:!0})],key:"key",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"validationErrors",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_showPassive",value(){return!1}},{kind:"field",key:"validGroupAddresses",value(){return[]}},{kind:"field",key:"filteredGroupAddresses",value(){return[]}},{kind:"field",key:"addressOptions",value(){return[]}},{kind:"field",key:"dptSelectorDisabled",value(){return!1}},{kind:"field",key:"_validGADropTarget",value:void 0},{kind:"field",key:"_dragOverTimeout",value(){return{}}},{kind:"field",decorators:[(0,r.IO)(".passive")],key:"_passiveContainer",value:void 0},{kind:"field",decorators:[(0,r.Kt)("ha-selector-select")],key:"_gaSelectors",value:void 0},{kind:"method",key:"getValidGroupAddresses",value:function(e){var t;return null!==(t=this.knx.project)&&void 0!==t&&t.project_loaded?Object.values(this.knx.project.knxproject.group_addresses).filter((t=>!!t.dpt&&(0,h.nK)(t.dpt,e))):[]}},{kind:"method",key:"getValidDptFromConfigValue",value:function(){var e;return this.config.dpt?null===(e=this.options.dptSelect)||void 0===e||null===(e=e.find((e=>e.value===this.config.dpt)))||void 0===e?void 0:e.dpt:void 0}},{kind:"method",key:"connectedCallback",value:function(){var e,t,a;(0,o.Z)(i,"connectedCallback",this,3)([]),this.validGroupAddresses=this.getValidGroupAddresses(null!==(e=null!==(t=this.options.validDPTs)&&void 0!==t?t:null===(a=this.options.dptSelect)||void 0===a?void 0:a.map((e=>e.dpt)))&&void 0!==e?e:[]),this.filteredGroupAddresses=this.validGroupAddresses,this.addressOptions=$(this.filteredGroupAddresses)}},{kind:"method",key:"shouldUpdate",value:function(e){return!(1===e.size&&e.has("hass"))}},{kind:"method",key:"willUpdate",value:function(e){var t;if(e.has("config")){var i,a;const t=this.getValidDptFromConfigValue();if((null===(i=e.get("config"))||void 0===i?void 0:i.dpt)!==this.config.dpt&&(this.filteredGroupAddresses=t?this.getValidGroupAddresses([t]):this.validGroupAddresses,this.addressOptions=$(this.filteredGroupAddresses)),t&&null!==(a=this.knx.project)&&void 0!==a&&a.project_loaded){var o;const e=[this.config.write,this.config.state,...null!==(o=this.config.passive)&&void 0!==o?o:[]].filter((e=>null!=e));this.dptSelectorDisabled=e.length>0&&e.every((e=>{var i;const a=null===(i=this.knx.project)||void 0===i||null===(i=i.knxproject.group_addresses[e])||void 0===i?void 0:i.dpt;return!!a&&(0,h.nK)(a,[t])}))}else this.dptSelectorDisabled=!1}this._validGADropTarget=null!==(t=this._dragDropContext)&&void 0!==t&&t.groupAddress?this.filteredGroupAddresses.includes(this._dragDropContext.groupAddress):void 0}},{kind:"method",key:"updated",value:function(e){e.has("validationErrors")&&this._gaSelectors.forEach((async e=>{var t;await e.updateComplete;const i=null===(t=(0,v._)(this.validationErrors,e.key))||void 0===t?void 0:t[0];e.comboBox.errorMessage=null==i?void 0:i.error_message,e.comboBox.invalid=!!i}))}},{kind:"method",key:"render",value:function(){const e=this.config.passive&&this.config.passive.length>0,t=!0===this._validGADropTarget,i=!1===this._validGADropTarget;return(0,n.dy)(m||(m=k`
      <div class="main">
        <div class="selectors">
          ${0}
          ${0}
        </div>
        <div class="options">
          <ha-icon-button
            .disabled=${0}
            .path=${0}
            .label=${0}
            @click=${0}
          ></ha-icon-button>
        </div>
      </div>
      <div
        class="passive ${0}"
        @transitionend=${0}
      >
        <ha-selector-select
          class=${0}
          .hass=${0}
          .label=${0}
          .required=${0}
          .selector=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
          @dragover=${0}
          @drop=${0}
        ></ha-selector-select>
      </div>
      ${0}
    `),this.options.write?(0,n.dy)(g||(g=k`<ha-selector-select
                class=${0}
                .hass=${0}
                .label=${0}
                .required=${0}
                .selector=${0}
                .key=${0}
                .value=${0}
                @value-changed=${0}
                @dragover=${0}
                @drop=${0}
              ></ha-selector-select>`),(0,s.$)({"valid-drop-zone":t,"invalid-drop-zone":i}),this.hass,"Send address"+(this.label?` - ${this.label}`:""),this.options.write.required,{select:{multiple:!1,custom_value:!0,options:this.addressOptions}},"write",this.config.write,this._updateConfig,this._dragOverHandler,this._dropHandler):n.Ld,this.options.state?(0,n.dy)(f||(f=k`<ha-selector-select
                class=${0}
                .hass=${0}
                .label=${0}
                .required=${0}
                .selector=${0}
                .key=${0}
                .value=${0}
                @value-changed=${0}
                @dragover=${0}
                @drop=${0}
              ></ha-selector-select>`),(0,s.$)({"valid-drop-zone":t,"invalid-drop-zone":i}),this.hass,"State address"+(this.label?` - ${this.label}`:""),this.options.state.required,{select:{multiple:!1,custom_value:!0,options:this.addressOptions}},"state",this.config.state,this._updateConfig,this._dragOverHandler,this._dropHandler):n.Ld,!!e,this._showPassive?x:_,"Toggle passive address visibility",this._togglePassiveVisibility,(0,s.$)({expanded:e||this._showPassive}),this._handleTransitionEnd,(0,s.$)({"valid-drop-zone":t,"invalid-drop-zone":i}),this.hass,"Passive addresses"+(this.label?` - ${this.label}`:""),!1,{select:{multiple:!0,custom_value:!0,options:this.addressOptions}},"passive",this.config.passive,this._updateConfig,this._dragOverHandler,this._dropHandler,this.options.dptSelect?this._renderDptSelector():n.Ld)}},{kind:"method",key:"_renderDptSelector",value:function(){var e;const t=null===(e=(0,v._)(this.validationErrors,"dpt"))||void 0===e?void 0:e[0];return(0,n.dy)(b||(b=k`<knx-dpt-selector
      .key=${0}
      .label=${0}
      .options=${0}
      .value=${0}
      .disabled=${0}
      .invalid=${0}
      .invalidMessage=${0}
      @value-changed=${0}
    >
    </knx-dpt-selector>`),"dpt","Datapoint type",this.options.dptSelect,this.config.dpt,this.dptSelectorDisabled,!!t,null==t?void 0:t.error_message,this._updateConfig)}},{kind:"method",key:"_updateConfig",value:function(e){e.stopPropagation();const t=e.target,i=e.detail.value,a=Object.assign(Object.assign({},this.config),{},{[t.key]:i});this._updateDptSelector(t.key,a),this.config=a,(0,c.B)(this,"value-changed",{value:this.config}),this.requestUpdate()}},{kind:"method",key:"_updateDptSelector",value:function(e,t){var i,a;if(!this.options.dptSelect||null===(i=this.knx.project)||void 0===i||!i.project_loaded)return;let o;if("write"===e||"state"===e)o=t[e];else{if("passive"!==e)return;{var n;const e=null===(n=t.passive)||void 0===n||null===(n=n.filter((e=>{var t;return!(null!==(t=this.config.passive)&&void 0!==t&&t.includes(e))})))||void 0===n?void 0:n[0];o=e}}if(t.write||t.state||null!==(a=t.passive)&&void 0!==a&&a.length||(t.dpt=void 0),void 0===this.config.dpt){var r,s;const e=null===(r=this.validGroupAddresses.find((e=>e.address===o)))||void 0===r?void 0:r.dpt;if(!e)return;const i=this.options.dptSelect.find((t=>t.dpt.main===e.main&&t.dpt.sub===e.sub)),a=i?i.value:null===(s=this.options.dptSelect.find((t=>(0,h.nK)(e,[t.dpt]))))||void 0===s?void 0:s.value;t.dpt=a}}},{kind:"method",key:"_togglePassiveVisibility",value:function(e){e.stopPropagation(),e.preventDefault();const t=!this._showPassive;this._passiveContainer.style.overflow="hidden";const i=this._passiveContainer.scrollHeight;this._passiveContainer.style.height=`${i}px`,t||setTimeout((()=>{this._passiveContainer.style.height="0px"}),0),this._showPassive=t}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._passiveContainer.style.removeProperty("height"),this._passiveContainer.style.overflow=this._showPassive?"initial":"hidden"}},{kind:"method",key:"_dragOverHandler",value:function(e){if(![...e.dataTransfer.types].includes("text/group-address"))return;e.preventDefault(),e.dataTransfer.dropEffect="move";const t=e.target;this._dragOverTimeout[t.key]?clearTimeout(this._dragOverTimeout[t.key]):t.classList.add("active-drop-zone"),this._dragOverTimeout[t.key]=setTimeout((()=>{delete this._dragOverTimeout[t.key],t.classList.remove("active-drop-zone")}),100)}},{kind:"method",key:"_dropHandler",value:function(e){const t=e.dataTransfer.getData("text/group-address");if(!t)return;e.stopPropagation(),e.preventDefault();const i=e.target,a=Object.assign({},this.config);if(i.selector.select.multiple){var o;const e=[...null!==(o=this.config[i.key])&&void 0!==o?o:[],t];a[i.key]=e}else a[i.key]=t;this._updateDptSelector(i.key,a),(0,c.B)(this,"value-changed",{value:a}),setTimeout((()=>i.comboBox._inputElement.blur()))}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(y||(y=k`
    .main {
      display: flex;
      flex-direction: row;
    }

    .selectors {
      flex: 1;
      padding-right: 16px;
    }

    .options {
      width: 48px;
      display: flex;
      flex-direction: column-reverse;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }

    .passive {
      overflow: hidden;
      transition: height 150ms cubic-bezier(0.4, 0, 0.2, 1);
      height: 0px;
      margin-right: 64px; /* compensate for .options */
    }

    .passive.expanded {
      height: auto;
    }

    ha-selector-select {
      display: block;
      margin-bottom: 16px;
      transition:
        box-shadow 250ms,
        opacity 250ms;
    }

    .valid-drop-zone {
      box-shadow: 0px 0px 5px 2px rgba(var(--rgb-primary-color), 0.5);
    }

    .valid-drop-zone.active-drop-zone {
      box-shadow: 0px 0px 5px 2px var(--primary-color);
    }

    .invalid-drop-zone {
      opacity: 0.5;
    }

    .invalid-drop-zone.active-drop-zone {
      box-shadow: 0px 0px 5px 2px var(--error-color);
    }
  `))}}]}}),n.oi);t()}catch(m){t(m)}}))},79764:function(e,t,i){var a=i(73577),o=i(72621),n=(i(63721),i(71695),i(92745),i(52805),i(92551),i(19134),i(32517),i(32114),i(39527),i(99790),i(13334),i(34595),i(47021),i(57243)),r=i(50778),s=i(91583),d=i(60738),l=(i(17949),i(10508),i(57586)),c=i(10194),u=i(97409),h=i(88769);let v,p,m,g,f,b,y,k,_,x,$,w,C,L,S=e=>e;const B=new l.r("knx-project-device-tree");(0,a.Z)([(0,r.Mo)("knx-project-device-tree")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.F_)({context:c.R})],key:"_dragDropContext",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"validDPTs",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_selectedDevice",value:void 0},{kind:"field",key:"deviceTree",value(){return[]}},{kind:"method",key:"connectedCallback",value:function(){var e;(0,o.Z)(i,"connectedCallback",this,3)([]);const t=null!==(e=this.validDPTs)&&void 0!==e&&e.length?(0,u.OJ)(this.data,this.validDPTs):this.data.communication_objects,a=Object.values(this.data.devices).map((e=>{const i=[],a=Object.fromEntries(Object.entries(e.channels).map((([e,t])=>[e,{name:t.name,comObjects:[]}])));for(const n of e.communication_object_ids){if(!(n in t))continue;const e=t[n];e.channel&&e.channel in a?a[e.channel].comObjects.push(e):i.push(e)}const o=Object.entries(a).reduce(((e,[t,i])=>(i.comObjects.length&&(e[t]=i),e)),{});return{ia:e.individual_address,name:e.name,manufacturer:e.manufacturer_name,description:e.description.split(/[\r\n]/,1)[0],noChannelComObjects:i,channels:o}}));this.deviceTree=a.filter((e=>!!e.noChannelComObjects.length||!!Object.keys(e.channels).length))}},{kind:"method",key:"render",value:function(){return(0,n.dy)(v||(v=S`<div class="device-tree-view">
      ${0}
    </div>`),this._selectedDevice?this._renderSelectedDevice(this._selectedDevice):this._renderDevices())}},{kind:"method",key:"_renderDevices",value:function(){return this.deviceTree.length?(0,n.dy)(m||(m=S`<ul class="devices">
      ${0}
    </ul>`),(0,s.r)(this.deviceTree,(e=>e.ia),(e=>(0,n.dy)(g||(g=S`<li class="clickable" @click=${0} .device=${0}>
            ${0}
          </li>`),this._selectDevice,e,this._renderDevice(e))))):(0,n.dy)(p||(p=S`<ha-alert alert-type="info">No suitable device found in project data.</ha-alert>`))}},{kind:"method",key:"_renderDevice",value:function(e){return(0,n.dy)(f||(f=S`<div class="item">
      <span class="icon ia">
        <ha-svg-icon .path=${0}></ha-svg-icon>
        <span>${0}</span>
      </span>
      <div class="description">
        <p>${0}</p>
        <p>${0}</p>
        ${0}
      </div>
    </div>`),"M15,20A1,1 0 0,0 14,19H13V17H17A2,2 0 0,0 19,15V5A2,2 0 0,0 17,3H7A2,2 0 0,0 5,5V15A2,2 0 0,0 7,17H11V19H10A1,1 0 0,0 9,20H2V22H9A1,1 0 0,0 10,23H14A1,1 0 0,0 15,22H22V20H15M7,15V5H17V15H7Z",e.ia,e.manufacturer,e.name,e.description?(0,n.dy)(b||(b=S`<p>${0}</p>`),e.description):n.Ld)}},{kind:"method",key:"_renderSelectedDevice",value:function(e){return(0,n.dy)(y||(y=S`<ul class="selected-device">
      <li class="back-item clickable" @click=${0}>
        <div class="item">
          <ha-svg-icon class="back-icon" .path=${0}></ha-svg-icon>
          ${0}
        </div>
      </li>
      ${0}
    </ul>`),this._selectDevice,"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",this._renderDevice(e),this._renderChannels(e))}},{kind:"method",key:"_renderChannels",value:function(e){return(0,n.dy)(k||(k=S`${0}
    ${0} `),this._renderComObjects(e.noChannelComObjects),(0,s.r)(Object.entries(e.channels),(([t,i])=>`${e.ia}_ch_${t}`),(([e,t])=>t.comObjects.length?(0,n.dy)(_||(_=S`<li class="channel">${0}</li>
              ${0}`),t.name,this._renderComObjects(t.comObjects)):n.Ld)))}},{kind:"method",key:"_renderComObjects",value:function(e){return(0,n.dy)(x||(x=S`${0} `),(0,s.r)(e,(e=>`${e.device_address}_co_${e.number}`),(e=>{return(0,n.dy)($||($=S`<li class="com-object">
          <div class="item">
            <span class="icon co"
              ><ha-svg-icon .path=${0}></ha-svg-icon
              ><span>${0}</span></span
            >
            <div class="description">
              <p>
                ${0}${0}
              </p>
              <p class="co-info">${0}</p>
            </div>
          </div>
          <ul class="group-addresses">
            ${0}
          </ul>
        </li>`),"M22 12C22 6.5 17.5 2 12 2S2 6.5 2 12 6.5 22 12 22 22 17.5 22 12M15 6.5L18.5 10L15 13.5V11H11V9H15V6.5M9 17.5L5.5 14L9 10.5V13H13V15H9V17.5Z",e.number,e.text,e.function_text?" - "+e.function_text:"",`${(t=e.flags).read?"R":"–"} ${t.write?"W":"–"} ${t.transmit?"T":"–"} ${t.update?"U":"–"}`,this._renderGroupAddresses(e.group_address_links));var t})))}},{kind:"method",key:"_renderGroupAddresses",value:function(e){const t=e.map((e=>this.data.group_addresses[e]));return(0,n.dy)(w||(w=S`${0} `),(0,s.r)(t,(e=>e.identifier),(e=>{var t,i,a,o,r,s;return(0,n.dy)(C||(C=S`<li
          draggable="true"
          @dragstart=${0}
          @dragend=${0}
          @mouseover=${0}
          @focus=${0}
          @mouseout=${0}
          @blur=${0}
          .ga=${0}
        >
          <div class="item">
            <ha-svg-icon
              class="drag-icon"
              .path=${0}
              .viewBox=${0}
            ></ha-svg-icon>
            <span class="icon ga">
              <span>${0}</span>
            </span>
            <div class="description">
              <p>${0}</p>
              <p class="ga-info">${0}</p>
            </div>
          </div>
        </li>`),null===(t=this._dragDropContext)||void 0===t?void 0:t.gaDragStartHandler,null===(i=this._dragDropContext)||void 0===i?void 0:i.gaDragEndHandler,null===(a=this._dragDropContext)||void 0===a?void 0:a.gaDragIndicatorStartHandler,null===(o=this._dragDropContext)||void 0===o?void 0:o.gaDragIndicatorStartHandler,null===(r=this._dragDropContext)||void 0===r?void 0:r.gaDragIndicatorEndHandler,null===(s=this._dragDropContext)||void 0===s?void 0:s.gaDragIndicatorEndHandler,e,"M9,3H11V5H9V3M13,3H15V5H13V3M9,7H11V9H9V7M13,7H15V9H13V7M9,11H11V13H9V11M13,11H15V13H13V11M9,15H11V17H9V15M13,15H15V17H13V15M9,19H11V21H9V19M13,19H15V21H13V19Z","4 0 16 24",e.address,e.name,(e=>{const t=(0,h.W)(e.dpt);return t?`DPT ${t}`:""})(e))})))}},{kind:"method",key:"_selectDevice",value:function(e){const t=e.target.device;B.debug("select device",t),this._selectedDevice=t,this.scrollTop=0}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(L||(L=S`
    :host {
      display: block;
      box-sizing: border-box;
      margin: 0;
      height: 100%;
      overflow-y: scroll;
      overflow-x: hidden;
      background-color: var(--sidebar-background-color);
      color: var(--sidebar-menu-button-text-color, --primary-text-color);
      margin-right: env(safe-area-inset-right);
      border-left: 1px solid var(--divider-color);
      padding-left: 8px;
    }

    ha-alert {
      display: block;
      margin-right: 8px;
      margin-top: 8px;
    }

    ul {
      list-style-type: none;
      padding: 0;
      margin-block-start: 8px;
    }

    li {
      display: block;
      margin-bottom: 4px;
      & div.item {
        /* icon and text */
        display: flex;
        align-items: center;
        pointer-events: none;
        & > div {
          /* optional container for multiple paragraphs */
          min-width: 0;
          width: 100%;
        }
      }
    }

    li p {
      margin: 0;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    span.icon {
      flex: 0 0 auto;
      display: inline-flex;
      /* align-self: stretch; */
      align-items: center;

      color: var(--text-primary-color);
      font-size: 1rem;
      font-weight: 700;
      border-radius: 12px;
      padding: 3px 6px;
      margin-right: 4px;

      & > ha-svg-icon {
        float: left;
        width: 16px;
        height: 16px;
        margin-right: 4px;
      }

      & > span {
        /* icon text */
        flex: 1;
        text-align: center;
      }
    }

    span.ia {
      flex-basis: 70px;
      background-color: var(--label-badge-grey);
      & > ha-svg-icon {
        transform: rotate(90deg);
      }
    }

    span.co {
      flex-basis: 44px;
      background-color: var(--amber-color);
    }

    span.ga {
      flex-basis: 54px;
      background-color: var(--knx-green);
    }

    .description {
      margin-top: 4px;
      margin-bottom: 4px;
    }

    p.co-info,
    p.ga-info {
      font-size: 0.85rem;
      font-weight: 300;
    }

    .back-item {
      margin-left: -8px; /* revert host padding to have gapless border */
      padding-left: 8px;
      margin-top: -8px; /* revert ul margin-block-start to have gapless hover effect */
      padding-top: 8px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--divider-color);
      margin-bottom: 8px;
    }

    .back-icon {
      margin-right: 8px;
      color: var(--label-badge-grey);
    }

    li.channel {
      border-top: 1px solid var(--divider-color);
      border-bottom: 1px solid var(--divider-color);
      padding: 4px 16px;
      font-weight: 500;
    }

    li.clickable {
      cursor: pointer;
    }
    li.clickable:hover {
      background-color: rgba(var(--rgb-primary-text-color), 0.04);
    }

    li[draggable="true"] {
      cursor: grab;
    }
    li[draggable="true"]:hover {
      border-radius: 12px;
      background-color: rgba(var(--rgb-primary-color), 0.2);
    }

    ul.group-addresses {
      margin-top: 0;
      margin-bottom: 8px;

      & > li:not(:first-child) {
        /* passive addresses for this com-object */
        opacity: 0.8;
      }
    }
  `))}}]}}),n.oi)},43522:function(e,t,i){var a=i(73577),o=i(72621),n=(i(71695),i(47021),i(57243)),r=i(50778),s=i(35359),d=i(11297);i(76418),i(59414),i(29939);let l,c,u,h,v=e=>e;(0,a.Z)([(0,r.Mo)("knx-selector-row")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"key",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_disabled",value(){return!1}},{kind:"field",key:"_haSelectorValue",value(){return null}},{kind:"field",key:"_inlineSelector",value(){return!1}},{kind:"field",key:"_optionalBooleanSelector",value(){return!1}},{kind:"method",key:"connectedCallback",value:function(){var e,t;(0,o.Z)(i,"connectedCallback",this,3)([]),this._disabled=!!this.selector.optional&&void 0===this.value,this._haSelectorValue=null!==(e=null!==(t=this.value)&&void 0!==t?t:this.selector.default)&&void 0!==e?e:null;const a="boolean"in this.selector.selector,n=a||"number"in this.selector.selector;this._inlineSelector=!this.selector.optional&&n,this._optionalBooleanSelector=!!this.selector.optional&&a,this._optionalBooleanSelector&&(this._haSelectorValue=!0)}},{kind:"method",key:"render",value:function(){const e=this._optionalBooleanSelector?n.Ld:(0,n.dy)(l||(l=v`<ha-selector
          class=${0}
          .hass=${0}
          .selector=${0}
          .disabled=${0}
          .value=${0}
          @value-changed=${0}
        ></ha-selector>`),(0,s.$)({"newline-selector":!this._inlineSelector}),this.hass,this.selector.selector,this._disabled,this._haSelectorValue,this._valueChange);return(0,n.dy)(c||(c=v`
      <div class="body">
        <div class="text">
          <p class="heading">${0}</p>
          <p class="description">${0}</p>
        </div>
        ${0}
      </div>
      ${0}
    `),this.selector.label,this.selector.helper,this.selector.optional?(0,n.dy)(u||(u=v`<ha-selector
              class="optional-switch"
              .selector=${0}
              .value=${0}
              @value-changed=${0}
            ></ha-selector>`),{boolean:{}},!this._disabled,this._toggleDisabled):this._inlineSelector?e:n.Ld,this._inlineSelector?n.Ld:e)}},{kind:"method",key:"_toggleDisabled",value:function(e){e.stopPropagation(),this._disabled=!this._disabled,this._propagateValue()}},{kind:"method",key:"_valueChange",value:function(e){e.stopPropagation(),this._haSelectorValue=e.detail.value,this._propagateValue()}},{kind:"method",key:"_propagateValue",value:function(){(0,d.B)(this,"value-changed",{value:this._disabled?void 0:this._haSelectorValue})}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(h||(h=v`
    :host {
      display: block;
      padding: 8px 16px 8px 0;
      border-top: 1px solid var(--divider-color);
    }
    .newline-selector {
      display: block;
      padding-top: 8px;
    }
    .body {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      row-gap: 8px;
    }
    .body > * {
      flex-grow: 1;
    }
    .text {
      flex-basis: 260px; /* min size of text - if inline selector is too big it will be pushed to next row */
    }
    .heading {
      margin: 0;
    }
    .description {
      margin: 0;
      display: block;
      padding-top: 4px;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      -webkit-font-smoothing: antialiased;
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      line-height: normal;
      color: var(--secondary-text-color);
    }
  `))}}]}}),n.oi)},65414:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),o=(i(71695),i(47021),i(57243)),n=i(50778),r=i(11297),s=(i(35506),i(51065)),d=e([s]);s=(d.then?(await d)():d)[0];let l,c,u=e=>e;(0,a.Z)([(0,n.Mo)("knx-sync-state-selector-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value(){return!0}},{kind:"field",decorators:[(0,n.Cb)()],key:"key",value(){return"sync_state"}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"noneValid",value(){return!0}},{kind:"field",key:"_strategy",value(){return!0}},{kind:"field",key:"_minutes",value(){return 60}},{kind:"method",key:"_hasMinutes",value:function(e){return"expire"===e||"every"===e}},{kind:"method",key:"willUpdate",value:function(){if("boolean"==typeof this.value)return void(this._strategy=this.value);const[e,t]=this.value.split(" ");this._strategy=e,+t&&(this._minutes=+t)}},{kind:"method",key:"render",value:function(){return(0,o.dy)(l||(l=u` <p class="description">
        Actively request state updates from KNX bus for state addresses.
      </p>
      <div class="inline">
        <ha-selector-select
          .hass=${0}
          .label=${0}
          .selector=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
        >
        </ha-selector-select>
        <ha-selector-number
          .hass=${0}
          .disabled=${0}
          .selector=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
        >
        </ha-selector-number>
      </div>`),this.hass,"Strategy",{select:{multiple:!1,custom_value:!1,mode:"dropdown",options:[{value:!0,label:"Default"},...this.noneValid?[{value:!1,label:"Never"}]:[],{value:"init",label:"Once when connection established"},{value:"expire",label:"Expire after last value update"},{value:"every",label:"Scheduled every"}]}},"strategy",this._strategy,this._handleChange,this.hass,!this._hasMinutes(this._strategy),{number:{min:2,max:1440,step:1,unit_of_measurement:"minutes"}},"minutes",this._minutes,this._handleChange)}},{kind:"method",key:"_handleChange",value:function(e){let t,i;e.stopPropagation(),"strategy"===e.target.key?(t=e.detail.value,i=this._minutes):(t=this._strategy,i=e.detail.value);const a=this._hasMinutes(t)?`${t} ${i}`:t;(0,r.B)(this,"value-changed",{value:a})}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(c||(c=u`
    .description {
      margin: 0;
      display: block;
      padding-top: 4px;
      padding-bottom: 8px;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      -webkit-font-smoothing: antialiased;
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      line-height: normal;
      color: var(--secondary-text-color);
    }
    .inline {
      width: 100%;
      display: inline-flex;
      flex-flow: row wrap;
      gap: 16px;
      justify-content: space-between;
    }
    .inline > * {
      flex: 1;
      width: 100%; /* to not overflow when wrapped */
    }
  `))}}]}}),o.oi);t()}catch(l){t(l)}}))},46928:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),o=(i(71695),i(40251),i(91895),i(47021),i(31622),i(57243)),n=i(50778),r=i(64364),s=i(69181),d=(i(44118),i(68565),i(11297)),l=i(66193),c=i(57259),u=i(57586),h=e([s]);s=(h.then?(await h)():h)[0];let v,p,m=e=>e;const g=new u.r("create_device_dialog");(0,a.Z)([(0,n.Mo)("knx-device-create-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"deviceName",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"area",value:void 0},{kind:"field",key:"_deviceEntry",value:void 0},{kind:"method",key:"closeDialog",value:function(e){(0,d.B)(this,"create-device-dialog-closed",{newDevice:this._deviceEntry},{bubbles:!1})}},{kind:"method",key:"_createDevice",value:function(){(0,c.fM)(this.hass,{name:this.deviceName,area_id:this.area}).then((e=>{this._deviceEntry=e})).catch((e=>{g.error("getGroupMonitorInfo",e),(0,r.c)("/knx/error",{replace:!0,data:e})})).finally((()=>{this.closeDialog(void 0)}))}},{kind:"method",key:"render",value:function(){return(0,o.dy)(v||(v=m`<ha-dialog
      open
      .heading=${0}
      scrimClickAction
      escapeKeyAction
      defaultAction="ignore"
    >
      <ha-selector-text
        .hass=${0}
        .label=${0}
        .required=${0}
        .selector=${0}
        .key=${0}
        .value=${0}
        @value-changed=${0}
      ></ha-selector-text>
      <ha-area-picker
        .hass=${0}
        .label=${0}
        .key=${0}
        .value=${0}
        @value-changed=${0}
      >
      </ha-area-picker>
      <mwc-button slot="secondaryAction" @click=${0}>
        ${0}
      </mwc-button>
      <mwc-button slot="primaryAction" @click=${0}>
        ${0}
      </mwc-button>
    </ha-dialog>`),"Create new device",this.hass,"Name",!0,{text:{type:"text"}},"deviceName",this.deviceName,this._valueChanged,this.hass,"Area","area",this.area,this._valueChanged,this.closeDialog,this.hass.localize("ui.common.cancel"),this._createDevice,this.hass.localize("ui.common.add"))}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this[e.target.key]=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[l.yu,(0,o.iv)(p||(p=m`
        @media all and (min-width: 600px) {
          ha-dialog {
            --mdc-dialog-min-width: 480px;
          }
        }
      `))]}}]}}),o.oi);t()}catch(v){t(v)}}))},77191:function(e,t,i){i.a(e,(async function(e,a){try{i.d(t,{i:()=>d});var o=i(92014),n=i(20337),r=e([o]);o=(r.then?(await r)():r)[0];const s="M18.4 1.6C18 1.2 17.5 1 17 1H7C6.5 1 6 1.2 5.6 1.6C5.2 2 5 2.5 5 3V21C5 21.5 5.2 22 5.6 22.4C6 22.8 6.5 23 7 23H17C17.5 23 18 22.8 18.4 22.4C18.8 22 19 21.5 19 21V3C19 2.5 18.8 2 18.4 1.6M16 7C16 7.6 15.6 8 15 8H9C8.4 8 8 7.6 8 7V5C8 4.4 8.4 4 9 4H15C15.6 4 16 4.4 16 5V7Z",d={binary_sensor:{name:"Binary Sensor",iconPath:"M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z",color:"var(--green-color)",description:"Read-only entity for binary datapoints. Window or door states etc.",schema:n.qu},switch:{name:"Switch",iconPath:s,color:"var(--blue-color)",description:"The KNX switch platform is used as an interface to switching actuators.",schema:n.wn},light:{name:"Light",iconPath:o.Ls.light,color:"var(--amber-color)",description:"The KNX light platform is used as an interface to dimming actuators, LED controllers, DALI gateways and similar.",schema:n.xz}};a()}catch(s){a(s)}}))},6480:function(e,t,i){i.d(t,{Q8:()=>r,cG:()=>s,kc:()=>n});i(39527),i(99790),i(67670),i(36993);const a=e=>"knx"===e[0],o=e=>e.identifiers.some(a),n=e=>Object.values(e.devices).filter(o),r=(e,t)=>Object.values(e.devices).find((e=>e.identifiers.find((e=>a(e)&&e[1]===t)))),s=e=>{const t=e.identifiers.find(a);return t?t[1]:void 0}},97409:function(e,t,i){i.d(t,{OJ:()=>o,nK:()=>a,ts:()=>n});i(71695),i(92745),i(52805),i(39527),i(41360),i(13334),i(34595),i(36993),i(47021);const a=(e,t)=>t.some((t=>e.main===t.main&&(!t.sub||e.sub===t.sub))),o=(e,t)=>{const i=((e,t)=>Object.entries(e.group_addresses).reduce(((e,[i,o])=>(o.dpt&&a(o.dpt,t)&&(e[i]=o),e)),{}))(e,t);return Object.entries(e.communication_objects).reduce(((e,[t,a])=>(a.group_address_links.some((e=>e in i))&&(e[t]=a),e)),{})},n=e=>{const t=[];return e.forEach((e=>{e.selectors.forEach((e=>{"group_address"===e.type&&(e.options.validDPTs?t.push(...e.options.validDPTs):e.options.dptSelect&&t.push(...e.options.dptSelect.map((e=>e.dpt))))}))})),t.reduce(((e,t)=>e.some((e=>{return a=t,(i=e).main===a.main&&i.sub===a.sub;var i,a}))?e:e.concat([t])),[])}},10194:function(e,t,i){i.d(t,{R:()=>s,Z:()=>r});i(63721);var a=i(60738);const o=new(i(57586).r)("knx-drag-drop-context"),n=Symbol("drag-drop-context");class r{constructor(e){this._groupAddress=void 0,this._updateObservers=void 0,this.gaDragStartHandler=e=>{var t;const i=e.target,a=i.ga;a?(this._groupAddress=a,o.debug("dragstart",a.address,this),null===(t=e.dataTransfer)||void 0===t||t.setData("text/group-address",a.address),this._updateObservers()):o.warn("dragstart: no 'ga' property found",i)},this.gaDragEndHandler=e=>{o.debug("dragend",this),this._groupAddress=void 0,this._updateObservers()},this.gaDragIndicatorStartHandler=e=>{const t=e.target.ga;t&&(this._groupAddress=t,o.debug("drag indicator start",t.address,this),this._updateObservers())},this.gaDragIndicatorEndHandler=e=>{o.debug("drag indicator end",this),this._groupAddress=void 0,this._updateObservers()},this._updateObservers=e}get groupAddress(){return this._groupAddress}}const s=(0,a.kr)(n)},88769:function(e,t,i){i.d(t,{W:()=>n,f:()=>o});i(52805),i(11740),i(39527),i(34595);var a=i(76848);const o={payload:e=>null==e.payload?"":Array.isArray(e.payload)?e.payload.reduce(((e,t)=>e+t.toString(16).padStart(2,"0")),"0x"):e.payload.toString(),valueWithUnit:e=>null==e.value?"":"number"==typeof e.value||"boolean"==typeof e.value||"string"==typeof e.value?e.value.toString()+(e.unit?" "+e.unit:""):(0,a.$w)(e.value),timeWithMilliseconds:e=>new Date(e.timestamp).toLocaleTimeString(["en-US"],{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dateWithMilliseconds:e=>new Date(e.timestamp).toLocaleTimeString([],{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dptNumber:e=>null==e.dpt_main?"":null==e.dpt_sub?e.dpt_main.toString():e.dpt_main.toString()+"."+e.dpt_sub.toString().padStart(3,"0"),dptNameNumber:e=>{const t=o.dptNumber(e);return null==e.dpt_name?`DPT ${t}`:t?`DPT ${t} ${e.dpt_name}`:e.dpt_name}},n=e=>null==e?"":e.main+(e.sub?"."+e.sub.toString().padStart(3,"0"):"")},20337:function(e,t,i){i.d(t,{qu:()=>a,wn:()=>o,xz:()=>n});const a=[{type:"settings_group",heading:"Binary sensor",description:"DPT 1 group addresses representing binary states.",selectors:[{name:"ga_sensor",type:"group_address",options:{state:{required:!0},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"invert",type:"selector",selector:{boolean:null},label:"Invert",helper:"Invert payload before processing.",optional:!0}]},{type:"settings_group",collapsible:!0,heading:"State properties",description:"Properties of the binary sensor state.",selectors:[{name:"ignore_internal_state",type:"selector",selector:{boolean:null},label:"Force update",helper:"Write each update to the state machine, even if the data is the same.",optional:!0},{name:"context_timeout",type:"selector",selector:{number:{min:0,max:10,step:.05,unit_of_measurement:"s"}},label:"Context timeout",helper:"The time in seconds between multiple identical telegram payloads would count towards an internal counter. This can be used to automate on mulit-clicks of a button. `0` to disable this feature.",default:.8,optional:!0},{name:"reset_after",type:"selector",selector:{number:{min:0,max:10,step:.1,unit_of_measurement:"s"}},label:"Reset after",helper:"Reset back to “off” state after specified seconds.",default:.8,optional:!0}]},{type:"settings_group",collapsible:!0,heading:"State updater",selectors:[{name:"sync_state",type:"sync_state"}]}],o=[{type:"settings_group",heading:"Switching",description:"DPT 1 group addresses controlling the switch function.",selectors:[{name:"ga_switch",type:"group_address",options:{write:{required:!0},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"invert",type:"selector",selector:{boolean:null},label:"Invert",helper:"Invert payloads before processing or sending."},{name:"respond_to_read",type:"selector",selector:{boolean:null},label:"Respond to read",helper:"Respond to GroupValueRead telegrams received to the configured address."}]},{type:"settings_group",collapsible:!0,heading:"State updater",selectors:[{name:"sync_state",type:"sync_state"}]}],n=[{type:"settings_group",heading:"Switching",description:"DPT 1 group addresses turning the light on or off.",selectors:[{name:"ga_switch",type:"group_address",options:{write:{required:!0},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}}]},{type:"settings_group",heading:"Brightness",description:"DPT 5 group addresses controlling the brightness.",selectors:[{name:"ga_brightness",type:"group_address",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"Color temperature",description:"Control the lights color temperature.",collapsible:!0,selectors:[{name:"ga_color_temp",type:"group_address",options:{write:{required:!1},state:{required:!1},passive:!0,dptSelect:[{value:"5.001",label:"Percent",description:"DPT 5.001",dpt:{main:5,sub:1}},{value:"7.600",label:"Kelvin",description:"DPT 7.600",dpt:{main:7,sub:600}},{value:"9",label:"2-byte float",description:"DPT 9",dpt:{main:9,sub:null}}]}},{name:"color_temp_min",type:"selector",label:"Warmest possible color temperature",default:2700,selector:{number:{min:1e3,max:9e3,step:1,unit_of_measurement:"Kelvin"}}},{name:"color_temp_max",type:"selector",label:"Coldest possible color temperature",default:6e3,selector:{number:{min:1e3,max:9e3,step:1,unit_of_measurement:"Kelvin"}}}]},{type:"settings_group",heading:"Color",description:"Control the light color.",collapsible:!0,selectors:[{type:"group_select",name:"_light_color_mode_schema",options:[{label:"Single address",description:"RGB, RGBW or XYY color controlled by a single group address",value:"default",schema:[{name:"ga_color",type:"group_address",options:{write:{required:!1},state:{required:!1},passive:!0,dptSelect:[{value:"232.600",label:"RGB",description:"DPT 232.600",dpt:{main:232,sub:600}},{value:"251.600",label:"RGBW",description:"DPT 251.600",dpt:{main:251,sub:600}},{value:"242.600",label:"XYY",description:"DPT 242.600",dpt:{main:242,sub:600}}]}}]},{label:"Individual addresses",description:"RGB(W) using individual state and brightness group addresses",value:"individual",schema:[{type:"settings_group",heading:"Red",description:"Control the lights red color. Brightness group address is required.",selectors:[{name:"ga_red_switch",type:"group_address",label:"Switch",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"ga_red_brightness",type:"group_address",label:"Brightness",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"Green",description:"Control the lights green color. Brightness group address is required.",selectors:[{name:"ga_green_switch",type:"group_address",label:"Switch",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"ga_green_brightness",type:"group_address",label:"Brightness",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"Blue",description:"Control the lights blue color. Brightness group address is required.",selectors:[{name:"ga_blue_switch",type:"group_address",label:"Switch",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"ga_blue_brightness",type:"group_address",label:"Brightness",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"White",description:"Control the lights white color. Brightness group address is required.",selectors:[{name:"ga_white_switch",type:"group_address",label:"Switch",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"ga_white_brightness",type:"group_address",label:"Brightness",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]}]},{label:"HSV",description:"Hue, saturation and brightness using individual group addresses",value:"hsv",schema:[{type:"settings_group",heading:"Hue",description:"Control the lights hue.",selectors:[{name:"ga_hue",type:"group_address",options:{write:{required:!0},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"Saturation",description:"Control the lights saturation.",selectors:[{name:"ga_saturation",type:"group_address",options:{write:{required:!0},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]}]}]}]},{type:"settings_group",collapsible:!0,heading:"State updater",selectors:[{name:"sync_state",type:"sync_state"}]}]},2583:function(e,t,i){i.d(t,{_:()=>a});i(71695),i(92745),i(19423),i(47021);const a=(e,t)=>{if(!e)return;const i=[];for(const a of e)if(a.path){const[e,...o]=a.path;e===t&&i.push(Object.assign(Object.assign({},a),{},{path:o}))}return i.length?i:void 0}},99165:function(e,t,i){i.a(e,(async function(e,a){try{i.r(t),i.d(t,{KNXCreateEntity:()=>M});var o=i(73577),n=(i(63721),i(63434),i(71695),i(40251),i(91895),i(96829),i(13334),i(47021),i(57243)),r=i(50778),s=i(60738),d=(i(68455),i(51728),i(17949),i(1192),i(12974),i(10508),i(43972),i(64364)),l=i(80155),c=i(11297),u=i(92492),h=i(15716),v=(i(79764),i(57259)),p=i(77191),m=i(97409),g=i(10194),f=i(57586),b=e([h,p]);[h,p]=b.then?(await b)():b;let y,k,_,x,$,w,C,L,S=e=>e;const B="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",D="M5,3A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5.5L18.5,3H17V9A1,1 0 0,1 16,10H8A1,1 0 0,1 7,9V3H5M12,4V9H15V4H12M7,12H17A1,1 0 0,1 18,13V19H6V13A1,1 0 0,1 7,12Z",P=new f.r("knx-create-entity");let M=(0,o.Z)([(0,r.Mo)("knx-create-entity")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_loading",value(){return!1}},{kind:"field",decorators:[(0,r.SB)()],key:"_validationErrors",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_validationBaseError",value:void 0},{kind:"field",decorators:[(0,r.IO)("ha-alert")],key:"_alertElement",value:void 0},{kind:"field",key:"_intent",value:void 0},{kind:"field",key:"entityPlatform",value:void 0},{kind:"field",key:"entityId",value:void 0},{kind:"field",key:"_dragDropContextProvider",value(){return new s.HQ(this,{context:g.R,initialValue:new g.Z((()=>{this._dragDropContextProvider.updateObservers()}))})}},{kind:"method",key:"firstUpdated",value:function(){this.knx.project||this.knx.loadProject().then((()=>{this.requestUpdate()}))}},{kind:"method",key:"willUpdate",value:function(e){if(e.has("route")){const e=this.route.prefix.split("/").at(-1);if("create"!==e&&"edit"!==e)return P.error("Unknown intent",e),void(this._intent=void 0);if(this._intent=e,"create"===e){const e=this.route.path.split("/")[1];this.entityPlatform=e,this._config=void 0,this._loading=!1}else"edit"===e&&(this.entityId=this.route.path.split("/")[1],this._loading=!0,(0,v.IK)(this.hass,this.entityId).then((e=>{const{platform:t,data:i}=e;this.entityPlatform=t,this._config=i})).catch((e=>{P.warn("Fetching entity config failed.",e),this.entityPlatform=void 0})).finally((()=>{this._loading=!1})))}}},{kind:"method",key:"render",value:function(){return this.hass&&this.knx.project&&this._intent&&!this._loading?"edit"===this._intent?this._renderEdit():this._renderCreate():(0,n.dy)(y||(y=S` <hass-loading-screen></hass-loading-screen> `))}},{kind:"method",key:"_renderCreate",value:function(){if(!this.entityPlatform)return this._renderTypeSelection();const e=p.i[this.entityPlatform];return e?this._renderEntityConfig(e,!0):(P.error("Unknown platform",this.entityPlatform),this._renderTypeSelection())}},{kind:"method",key:"_renderEdit",value:function(){if(!this.entityPlatform)return this._renderNotFound();const e=p.i[this.entityPlatform];return e?this._renderEntityConfig(e,!1):(P.error("Unknown platform",this.entityPlatform),this._renderNotFound())}},{kind:"method",key:"_renderNotFound",value:function(){return(0,n.dy)(k||(k=S`
      <hass-subpage
        .hass=${0}
        .narrow=${0}
        .back-path=${0}
        .header=${0}
      >
        <div class="content">
          <ha-alert alert-type="error">Entity not found: <code>${0}</code></ha-alert>
        </div>
      </hass-subpage>
    `),this.hass,this.narrow,this.backPath,"Edit entity",this.entityId)}},{kind:"method",key:"_renderTypeSelection",value:function(){return(0,n.dy)(_||(_=S`
      <hass-subpage
        .hass=${0}
        .narrow=${0}
        .back-path=${0}
        .header=${0}
      >
        <div class="type-selection">
          <ha-card outlined .header=${0}>
            <!-- <p>Some help text</p> -->
            <ha-navigation-list
              .hass=${0}
              .narrow=${0}
              .pages=${0}
              has-secondary
              .label=${0}
            ></ha-navigation-list>
          </ha-card>
        </div>
      </hass-subpage>
    `),this.hass,this.narrow,this.backPath,"Select entity type","Create KNX entity",this.hass,this.narrow,Object.entries(p.i).map((([e,t])=>({name:t.name,description:t.description,iconPath:t.iconPath,iconColor:t.color,path:`/knx/entities/create/${e}`}))),"Select entity type")}},{kind:"method",key:"_renderEntityConfig",value:function(e,t){var i,a,o;return(0,n.dy)(x||(x=S`<hass-subpage
      .hass=${0}
      .narrow=${0}
      .back-path=${0}
      .header=${0}
    >
      <div class="content">
        <div class="entity-config">
          <knx-configure-entity
            .hass=${0}
            .knx=${0}
            .platform=${0}
            .config=${0}
            .validationErrors=${0}
            @knx-entity-configuration-changed=${0}
          >
            ${0}
          </knx-configure-entity>
          <ha-fab
            .label=${0}
            extended
            @click=${0}
            ?disabled=${0}
          >
            <ha-svg-icon slot="icon" .path=${0}></ha-svg-icon>
          </ha-fab>
        </div>
        ${0}
      </div>
    </hass-subpage>`),this.hass,this.narrow,this.backPath,t?"Create new entity":`Edit ${this.entityId}`,this.hass,this.knx,e,this._config,this._validationErrors,this._configChanged,this._validationBaseError?(0,n.dy)($||($=S`<ha-alert slot="knx-validation-error" alert-type="error">
                  <details>
                    <summary><b>Validation error</b></summary>
                    <p>Base error: ${0}</p>
                    ${0}
                  </details>
                </ha-alert>`),this._validationBaseError,null!==(i=null===(a=this._validationErrors)||void 0===a?void 0:a.map((e=>{var t;return(0,n.dy)(w||(w=S`<p>
                          ${0}: ${0} in ${0}
                        </p>`),e.error_class,e.error_message,null===(t=e.path)||void 0===t?void 0:t.join(" / "))})))&&void 0!==i?i:n.Ld):n.Ld,t?"Create":"Save",t?this._entityCreate:this._entityUpdate,void 0===this._config,t?B:D,null!==(o=this.knx.project)&&void 0!==o&&o.project_loaded?(0,n.dy)(C||(C=S` <div class="panel">
              <knx-project-device-tree
                .data=${0}
                .validDPTs=${0}
              ></knx-project-device-tree>
            </div>`),this.knx.project.knxproject,(0,m.ts)(e.schema)):n.Ld)}},{kind:"method",key:"_configChanged",value:function(e){e.stopPropagation(),P.warn("configChanged",e.detail),this._config=e.detail,this._validationErrors&&this._entityValidate()}},{kind:"field",key:"_entityValidate",value(){return(0,u.P)((()=>{P.debug("validate",this._config),void 0!==this._config&&void 0!==this.entityPlatform&&(0,v.W4)(this.hass,{platform:this.entityPlatform,data:this._config}).then((e=>{this._handleValidationError(e,!1)})).catch((e=>{P.error("validateEntity",e),(0,d.c)("/knx/error",{replace:!0,data:e})}))}),250)}},{kind:"method",key:"_entityCreate",value:function(e){e.stopPropagation(),void 0!==this._config&&void 0!==this.entityPlatform?(0,v.JP)(this.hass,{platform:this.entityPlatform,data:this._config}).then((e=>{this._handleValidationError(e,!0)||(P.debug("Successfully created entity",e.entity_id),(0,d.c)("/knx/entities",{replace:!0}),e.entity_id?this._entityMoreInfoSettings(e.entity_id):P.error("entity_id not found after creation."))})).catch((e=>{P.error("Error creating entity",e),(0,d.c)("/knx/error",{replace:!0,data:e})})):P.error("No config found.")}},{kind:"method",key:"_entityUpdate",value:function(e){e.stopPropagation(),void 0!==this._config&&void 0!==this.entityId&&void 0!==this.entityPlatform?(0,v.i8)(this.hass,{platform:this.entityPlatform,entity_id:this.entityId,data:this._config}).then((e=>{this._handleValidationError(e,!0)||(P.debug("Successfully updated entity",this.entityId),(0,d.c)("/knx/entities",{replace:!0}))})).catch((e=>{P.error("Error updating entity",e),(0,d.c)("/knx/error",{replace:!0,data:e})})):P.error("No config found.")}},{kind:"method",key:"_handleValidationError",value:function(e,t){return!1===e.success?(P.warn("Validation error",e),this._validationErrors=e.errors,this._validationBaseError=e.error_base,t&&setTimeout((()=>this._alertElement.scrollIntoView({behavior:"smooth"}))),!0):(this._validationErrors=void 0,this._validationBaseError=void 0,P.debug("Validation passed",e.entity_id),!1)}},{kind:"method",key:"_entityMoreInfoSettings",value:function(e){(0,c.B)(l.E.document.querySelector("home-assistant"),"hass-more-info",{entityId:e,view:"settings"})}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(L||(L=S`
    hass-loading-screen {
      --app-header-background-color: var(--sidebar-background-color);
      --app-header-text-color: var(--sidebar-text-color);
    }

    .type-selection {
      margin: 20px auto 80px;
      max-width: 720px;
    }

    @media screen and (max-width: 600px) {
      .panel {
        display: none;
      }
    }

    .content {
      display: flex;
      flex-direction: row;
      height: 100%;
      width: 100%;

      & > .entity-config {
        flex-grow: 1;
        flex-shrink: 1;
        height: 100%;
        overflow-y: scroll;
      }

      & > .panel {
        flex-grow: 0;
        flex-shrink: 3;
        width: 480px;
        min-width: 280px;
      }
    }

    knx-configure-entity {
      display: block;
      margin: 20px auto 40px; /* leave 80px space for fab */
      max-width: 720px;
    }

    ha-alert {
      display: block;
      margin: 20px auto;
      max-width: 720px;

      & summary {
        padding: 10px;
      }
    }

    ha-fab {
      /* not slot="fab" to move out of panel */
      float: right;
      margin-right: calc(16px + env(safe-area-inset-right));
      margin-bottom: 40px;
      z-index: 1;
    }
  `))}}]}}),n.oi);a()}catch(y){a(y)}}))}}]);
//# sourceMappingURL=202.b3058951a8d68b32.js.map