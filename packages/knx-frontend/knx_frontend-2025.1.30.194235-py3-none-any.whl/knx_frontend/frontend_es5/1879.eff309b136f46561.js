/*! For license information please see 1879.eff309b136f46561.js.LICENSE.txt */
"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1879"],{13270:function(t,e,i){i.a(t,(async function(t,e){try{var n=i(73577),s=(i(71695),i(47021),i(57243)),a=i(50778),r=i(31050),o=i(43420),c=i(92014),l=(i(10508),t([c]));c=(l.then?(await l)():l)[0];let d,h,u,v,f=t=>t;(0,n.Z)([(0,a.Mo)("ha-state-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"stateValue",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"icon",value:void 0},{kind:"method",key:"render",value:function(){var t,e;const i=this.icon||this.stateObj&&(null===(t=this.hass)||void 0===t||null===(t=t.entities[this.stateObj.entity_id])||void 0===t?void 0:t.icon)||(null===(e=this.stateObj)||void 0===e?void 0:e.attributes.icon);if(i)return(0,s.dy)(d||(d=f`<ha-icon .icon=${0}></ha-icon>`),i);if(!this.stateObj)return s.Ld;if(!this.hass)return this._renderFallback();const n=(0,c.gD)(this.hass,this.stateObj,this.stateValue).then((t=>t?(0,s.dy)(h||(h=f`<ha-icon .icon=${0}></ha-icon>`),t):this._renderFallback()));return(0,s.dy)(u||(u=f`${0}`),(0,r.C)(n))}},{kind:"method",key:"_renderFallback",value:function(){const t=(0,o.N)(this.stateObj);return(0,s.dy)(v||(v=f`
      <ha-svg-icon
        .path=${0}
      ></ha-svg-icon>
    `),c.Ls[t]||c.Rb)}}]}}),s.oi);e()}catch(d){e(d)}}))},56516:function(t,e,i){i.a(t,(async function(t,n){try{i.r(e),i.d(e,{KNXEntitiesView:()=>M});var s=i(73577),a=(i(71695),i(19423),i(40251),i(19134),i(47706),i(13334),i(47021),i(71513),i(75656),i(50100),i(18084),i(57243)),r=i(50778),o=i(27486),c=(i(68455),i(78616)),l=(i(12974),i(59897),i(13270)),d=(i(10508),i(64364)),h=i(80155),u=i(11297),v=i(4557),f=i(57259),y=i(57586),b=t([c,l]);[c,l]=b.then?(await b)():b;let k,_,p,$,m,C=t=>t;const g="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",x="M11 7V9H13V7H11M14 17V15H13V11H10V13H11V15H10V17H14M22 12C22 17.5 17.5 22 12 22C6.5 22 2 17.5 2 12C2 6.5 6.5 2 12 2C17.5 2 22 6.5 22 12M20 12C20 7.58 16.42 4 12 4C7.58 4 4 7.58 4 12C4 16.42 7.58 20 12 20C16.42 20 20 16.42 20 12Z",w="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",V="M14.06,9L15,9.94L5.92,19H5V18.08L14.06,9M17.66,3C17.41,3 17.15,3.1 16.96,3.29L15.13,5.12L18.88,8.87L20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18.17,3.09 17.92,3 17.66,3M14.06,6.19L3,17.25V21H6.75L17.81,9.94L14.06,6.19Z",H=new y.r("knx-entities-view");let M=(0,s.Z)([(0,r.Mo)("knx-entities-view")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"knx_entities",value(){return[]}},{kind:"field",decorators:[(0,r.SB)()],key:"filterDevice",value(){return null}},{kind:"method",key:"firstUpdated",value:function(){this._fetchEntities()}},{kind:"method",key:"willUpdate",value:function(){const t=new URLSearchParams(h.E.location.search);this.filterDevice=t.get("device_id")}},{kind:"method",key:"_fetchEntities",value:async function(){(0,f.Bd)(this.hass).then((t=>{H.debug(`Fetched ${t.length} entity entries.`),this.knx_entities=t.map((t=>{var e;const i=this.hass.states[t.entity_id],n=t.device_id?this.hass.devices[t.device_id]:void 0,s=null!==(e=t.area_id)&&void 0!==e?e:null==n?void 0:n.area_id,a=s?this.hass.areas[s]:void 0;return Object.assign(Object.assign({},t),{},{entityState:i,area:a})}))})).catch((t=>{H.error("getEntityEntries",t),(0,d.c)("/knx/error",{replace:!0,data:t})}))}},{kind:"field",key:"_columns",value(){return(0,o.Z)((t=>{const e="56px",i="176px";return{icon:{title:"",minWidth:e,maxWidth:e,type:"icon",template:t=>(0,a.dy)(k||(k=C`
          <ha-state-icon
            slot="item-icon"
            .hass=${0}
            .stateObj=${0}
          ></ha-state-icon>
        `),this.hass,t.entityState)},friendly_name:{showNarrow:!0,filterable:!0,sortable:!0,title:"Friendly Name",flex:2,template:t=>{var e,i;return null!==(e=null===(i=t.entityState)||void 0===i?void 0:i.attributes.friendly_name)&&void 0!==e?e:""}},entity_id:{filterable:!0,sortable:!0,title:"Entity ID",flex:1},device:{filterable:!0,sortable:!0,title:"Device",flex:1,template:t=>{var e;return t.device_id&&null!==(e=this.hass.devices[t.device_id].name)&&void 0!==e?e:""}},device_id:{hidden:!0,title:"Device ID",filterable:!0,template:t=>{var e;return null!==(e=t.device_id)&&void 0!==e?e:""}},area:{title:"Area",sortable:!0,filterable:!0,flex:1,template:t=>{var e,i;return null!==(e=null===(i=t.area)||void 0===i?void 0:i.name)&&void 0!==e?e:""}},actions:{showNarrow:!0,title:"",minWidth:i,maxWidth:i,type:"icon-button",template:t=>(0,a.dy)(_||(_=C`
          <ha-icon-button
            .label=${0}
            .path=${0}
            .entityEntry=${0}
            @click=${0}
          ></ha-icon-button>
          <ha-icon-button
            .label=${0}
            .path=${0}
            .entityEntry=${0}
            @click=${0}
          ></ha-icon-button>
          <ha-icon-button
            .label=${0}
            .path=${0}
            .entityEntry=${0}
            @click=${0}
          ></ha-icon-button>
        `),"More info",x,t,this._entityMoreInfo,this.hass.localize("ui.common.edit"),V,t,this._entityEdit,this.hass.localize("ui.common.delete"),g,t,this._entityDelete)}}}))}},{kind:"field",key:"_entityEdit",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,d.c)("/knx/entities/edit/"+e.entity_id)}}},{kind:"field",key:"_entityMoreInfo",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,u.B)(h.E.document.querySelector("home-assistant"),"hass-more-info",{entityId:e.entity_id})}}},{kind:"field",key:"_entityDelete",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,v.g7)(this,{text:`${this.hass.localize("ui.common.delete")} ${e.entity_id}?`}).then((t=>{t&&(0,f.Ks)(this.hass,e.entity_id).then((()=>{H.debug("entity deleted",e.entity_id),this._fetchEntities()})).catch((t=>{(0,v.Ys)(this,{title:"Deletion failed",text:t})}))}))}}},{kind:"method",key:"render",value:function(){return this.hass&&this.knx_entities?(0,a.dy)($||($=C`
      <hass-tabs-subpage-data-table
        .hass=${0}
        .narrow=${0}
        .route=${0}
        .tabs=${0}
        .localizeFunc=${0}
        .columns=${0}
        .data=${0}
        .hasFab=${0}
        .searchLabel=${0}
        .clickable=${0}
        .filter=${0}
      >
        <ha-fab
          slot="fab"
          .label=${0}
          extended
          @click=${0}
        >
          <ha-svg-icon slot="icon" .path=${0}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage-data-table>
    `),this.hass,this.narrow,this.route,this.tabs,this.knx.localize,this._columns(this.hass.language),this.knx_entities,!0,this.hass.localize("ui.components.data-table.search"),!1,this.filterDevice,this.hass.localize("ui.common.add"),this._entityCreate,w):(0,a.dy)(p||(p=C` <hass-loading-screen></hass-loading-screen> `))}},{kind:"method",key:"_entityCreate",value:function(){(0,d.c)("/knx/entities/create")}},{kind:"field",static:!0,key:"styles",value(){return(0,a.iv)(m||(m=C`
    hass-loading-screen {
      --app-header-background-color: var(--sidebar-background-color);
      --app-header-text-color: var(--sidebar-text-color);
    }
  `))}}]}}),a.oi);n()}catch(k){n(k)}}))},17743:function(t,e,i){var n=i(13053);t.exports=function(t,e,i){for(var s=0,a=arguments.length>2?i:n(e),r=new t(a);a>s;)r[s]=e[s++];return r}},37595:function(t,e,i){var n=i(31269),s=i(72878),a=i(25091),r=i(12360),o=i(70273),c=i(13053),l=i(72309),d=i(17743),h=Array,u=s([].push);t.exports=function(t,e,i,s){for(var v,f,y,b=r(t),k=a(b),_=n(e,i),p=l(null),$=c(k),m=0;$>m;m++)y=k[m],(f=o(_(y,m,b)))in p?u(p[f],y):p[f]=[y];if(s&&(v=s(b))!==h)for(f in p)p[f]=d(v,p[f]);return p}},58208:function(t,e,i){var n=i(22707),s=Math.floor,a=function(t,e){var i=t.length;if(i<8)for(var r,o,c=1;c<i;){for(o=c,r=t[c];o&&e(t[o-1],r)>0;)t[o]=t[--o];o!==c++&&(t[o]=r)}else for(var l=s(i/2),d=a(n(t,0,l),e),h=a(n(t,l),e),u=d.length,v=h.length,f=0,y=0;f<u||y<v;)t[f+y]=f<u&&y<v?e(d[f],h[y])<=0?d[f++]:h[y++]:f<u?d[f++]:h[y++];return t};t.exports=a},4597:function(t,e,i){var n=i(63253).match(/firefox\/(\d+)/i);t.exports=!!n&&+n[1]},66869:function(t,e,i){var n=i(63253);t.exports=/MSIE|Trident/.test(n)},6548:function(t,e,i){var n=i(63253).match(/AppleWebKit\/(\d+)\./);t.exports=!!n&&+n[1]},19444:function(t,e,i){var n=i(1569),s=i(58108);t.exports=function(t){if(s){try{return n.process.getBuiltinModule(t)}catch(e){}try{return Function('return require("'+t+'")')()}catch(e){}}}},22139:function(t,e,i){var n=i(40810),s=i(37595),a=i(35709);n({target:"Array",proto:!0},{group:function(t){return s(this,t,arguments.length>1?arguments[1]:void 0)}}),a("group")},31050:function(t,e,i){i.d(e,{C:()=>u});i(71695),i(40251),i(39527),i(67670),i(47021);var n=i(57708),s=i(53232),a=i(1714);i(63721),i(88230),i(52247);class r{constructor(t){this.G=t}disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}}class o{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null===(t=this.Z)||void 0===t||t.call(this),this.Y=this.Z=void 0}}var c=i(45779);const l=t=>!(0,s.pt)(t)&&"function"==typeof t.then,d=1073741823;class h extends a.sR{constructor(){super(...arguments),this._$C_t=d,this._$Cwt=[],this._$Cq=new r(this),this._$CK=new o}render(...t){var e;return null!==(e=t.find((t=>!l(t))))&&void 0!==e?e:n.Jb}update(t,e){const i=this._$Cwt;let s=i.length;this._$Cwt=e;const a=this._$Cq,r=this._$CK;this.isConnected||this.disconnected();for(let n=0;n<e.length&&!(n>this._$C_t);n++){const t=e[n];if(!l(t))return this._$C_t=n,t;n<s&&t===i[n]||(this._$C_t=d,s=0,Promise.resolve(t).then((async e=>{for(;r.get();)await r.get();const i=a.deref();if(void 0!==i){const n=i._$Cwt.indexOf(t);n>-1&&n<i._$C_t&&(i._$C_t=n,i.setValue(e))}})))}return n.Jb}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const u=(0,c.XM)(h)}}]);
//# sourceMappingURL=1879.eff309b136f46561.js.map