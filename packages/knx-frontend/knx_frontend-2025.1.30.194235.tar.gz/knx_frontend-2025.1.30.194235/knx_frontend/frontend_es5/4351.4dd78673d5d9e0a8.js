"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["4351"],{39090:function(e,t,i){i.r(t),i.d(t,{HaFormGrid:()=>c});var a=i(73577),d=i(72621),o=(i(71695),i(40251),i(13334),i(47021),i(42877),i(57243)),r=i(50778);let s,l,u,n=e=>e,c=(0,a.Z)([(0,r.Mo)("ha-form-grid")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"focus",value:async function(){var e;await this.updateComplete,null===(e=this.renderRoot.querySelector("ha-form"))||void 0===e||e.focus()}},{kind:"method",key:"updated",value:function(e){(0,d.Z)(i,"updated",this,3)([e]),e.has("schema")&&(this.schema.column_min_width?this.style.setProperty("--form-grid-min-width",this.schema.column_min_width):this.style.setProperty("--form-grid-min-width",""))}},{kind:"method",key:"render",value:function(){return(0,o.dy)(s||(s=n`
      ${0}
    `),this.schema.schema.map((e=>(0,o.dy)(l||(l=n`
          <ha-form
            .hass=${0}
            .data=${0}
            .schema=${0}
            .disabled=${0}
            .computeLabel=${0}
            .computeHelper=${0}
            .localizeValue=${0}
          ></ha-form>
        `),this.hass,this.data,[e],this.disabled,this.computeLabel,this.computeHelper,this.localizeValue))))}},{kind:"field",static:!0,key:"styles",value(){return(0,o.iv)(u||(u=n`
    :host {
      display: grid !important;
      grid-template-columns: repeat(
        var(--form-grid-column-count, auto-fit),
        minmax(var(--form-grid-min-width, 200px), 1fr)
      );
      grid-column-gap: 8px;
      grid-row-gap: 24px;
    }
    :host > ha-form {
      display: block;
    }
  `))}}]}}),o.oi)}}]);
//# sourceMappingURL=4351.4dd78673d5d9e0a8.js.map