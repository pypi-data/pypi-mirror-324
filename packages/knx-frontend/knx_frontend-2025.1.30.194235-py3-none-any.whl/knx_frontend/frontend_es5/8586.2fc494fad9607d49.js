"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8586"],{52804:function(e,t,i){i.d(t,{Q:()=>a});i(19134),i(97003);const a=e=>e.replace(/^_*(.)|_+(.)/g,((e,t,i)=>t?t.toUpperCase():" "+i.toUpperCase()))},53486:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),n=(i(19083),i(71695),i(92745),i(19423),i(40251),i(61006),i(39527),i(99790),i(41360),i(13334),i(47021),i(87319),i(57243)),o=i(50778),l=i(11297),s=i(52804),d=i(27357),r=i(69484),h=e([r]);r=(h.then?(await h)():h)[0];let u,c,v,p=e=>e;const k=[],f=e=>(0,n.dy)(u||(u=p`
  <mwc-list-item graphic="icon" .twoline=${0}>
    <ha-icon .icon=${0} slot="graphic"></ha-icon>
    <span>${0}</span>
    <span slot="secondary">${0}</span>
  </mwc-list-item>
`),!!e.title,e.icon,e.title||e.path,e.path),m=(e,t,i)=>{var a,n,o;return{path:`/${e}/${null!==(a=t.path)&&void 0!==a?a:i}`,icon:null!==(n=t.icon)&&void 0!==n?n:"mdi:view-compact",title:null!==(o=t.title)&&void 0!==o?o:t.path?(0,s.Q)(t.path):`${i}`}},b=(e,t)=>{var i;return{path:`/${t.url_path}`,icon:null!==(i=t.icon)&&void 0!==i?i:"mdi:view-dashboard",title:t.url_path===e.defaultPanel?e.localize("panel.states"):e.localize(`panel.${t.title}`)||t.title||(t.url_path?(0,s.Q)(t.url_path):"")}};(0,a.Z)([(0,o.Mo)("ha-navigation-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,o.SB)()],key:"_opened",value(){return!1}},{kind:"field",key:"navigationItemsLoaded",value(){return!1}},{kind:"field",key:"navigationItems",value(){return k}},{kind:"field",decorators:[(0,o.IO)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"method",key:"render",value:function(){return(0,n.dy)(c||(c=p`
      <ha-combo-box
        .hass=${0}
        item-value-path="path"
        item-label-path="path"
        .value=${0}
        allow-custom-value
        .filteredItems=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        .renderer=${0}
        @opened-changed=${0}
        @value-changed=${0}
        @filter-changed=${0}
      >
      </ha-combo-box>
    `),this.hass,this._value,this.navigationItems,this.label,this.helper,this.disabled,this.required,f,this._openedChanged,this._valueChanged,this._filterChanged)}},{kind:"method",key:"_openedChanged",value:async function(e){this._opened=e.detail.value,this._opened&&!this.navigationItemsLoaded&&this._loadNavigationItems()}},{kind:"method",key:"_loadNavigationItems",value:async function(){this.navigationItemsLoaded=!0;const e=Object.entries(this.hass.panels).map((([e,t])=>Object.assign({id:e},t))),t=e.filter((e=>"lovelace"===e.component_name)),i=await Promise.all(t.map((e=>(0,d.Q2)(this.hass.connection,"lovelace"===e.url_path?null:e.url_path,!0).then((t=>[e.id,t])).catch((t=>[e.id,void 0]))))),a=new Map(i);this.navigationItems=[];for(const n of e){this.navigationItems.push(b(this.hass,n));const e=a.get(n.id);e&&"views"in e&&e.views.forEach(((e,t)=>this.navigationItems.push(m(n.url_path,e,t))))}this.comboBox.filteredItems=this.navigationItems}},{kind:"method",key:"shouldUpdate",value:function(e){return!this._opened||e.has("_opened")}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this._setValue(e.detail.value)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,(0,l.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.detail.value.toLowerCase();if(t.length>=2){const e=[];this.navigationItems.forEach((i=>{(i.path.toLowerCase().includes(t)||i.title.toLowerCase().includes(t))&&e.push(i)})),e.length>0?this.comboBox.filteredItems=e:this.comboBox.filteredItems=[]}else this.comboBox.filteredItems=this.navigationItems}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"field",static:!0,key:"styles",value(){return(0,n.iv)(v||(v=p`
    ha-icon,
    ha-svg-icon {
      color: var(--primary-text-color);
      position: relative;
      bottom: 0px;
    }
    *[slot="prefix"] {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
  `))}}]}}),n.oi);t()}catch(u){t(u)}}))},5808:function(e,t,i){i.a(e,(async function(e,a){try{i.r(t),i.d(t,{HaNavigationSelector:()=>c});var n=i(73577),o=(i(71695),i(47021),i(57243)),l=i(50778),s=i(11297),d=i(53486),r=e([d]);d=(r.then?(await r)():r)[0];let h,u=e=>e,c=(0,n.Z)([(0,l.Mo)("ha-selector-navigation")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return(0,o.dy)(h||(h=u`
      <ha-navigation-picker
        .hass=${0}
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .helper=${0}
        @value-changed=${0}
      ></ha-navigation-picker>
    `),this.hass,this.label,this.value,this.required,this.disabled,this.helper,this._valueChanged)}},{kind:"method",key:"_valueChanged",value:function(e){(0,s.B)(this,"value-changed",{value:e.detail.value})}}]}}),o.oi);a()}catch(h){a(h)}}))},27357:function(e,t,i){i.d(t,{Q2:()=>a});const a=(e,t,i)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:i})}}]);
//# sourceMappingURL=8586.2fc494fad9607d49.js.map