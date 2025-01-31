/*! For license information please see 4978.7172040af6e42711.js.LICENSE.txt */
export const ids=["4978"];export const modules={13270:function(t,e,i){i.a(t,(async function(t,e){try{var n=i(44249),s=i(57243),a=i(50778),o=i(94571),r=i(43420),c=i(92014),d=(i(10508),t([c]));c=(d.then?(await d)():d)[0];(0,n.Z)([(0,a.Mo)("ha-state-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"stateValue",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"icon",value:void 0},{kind:"method",key:"render",value:function(){const t=this.icon||this.stateObj&&this.hass?.entities[this.stateObj.entity_id]?.icon||this.stateObj?.attributes.icon;if(t)return s.dy`<ha-icon .icon=${t}></ha-icon>`;if(!this.stateObj)return s.Ld;if(!this.hass)return this._renderFallback();const e=(0,c.gD)(this.hass,this.stateObj,this.stateValue).then((t=>t?s.dy`<ha-icon .icon=${t}></ha-icon>`:this._renderFallback()));return s.dy`${(0,o.C)(e)}`}},{kind:"method",key:"_renderFallback",value:function(){const t=(0,r.N)(this.stateObj);return s.dy`
      <ha-svg-icon
        .path=${c.Ls[t]||c.Rb}
      ></ha-svg-icon>
    `}}]}}),s.oi);e()}catch(h){e(h)}}))},56516:function(t,e,i){i.a(t,(async function(t,n){try{i.r(e),i.d(e,{KNXEntitiesView:()=>m});var s=i(44249),a=i(57243),o=i(50778),r=i(27486),c=(i(68455),i(13519),i(12974),i(59897),i(13270)),d=(i(10508),i(64364)),h=i(80155),l=i(11297),u=i(4557),y=i(57259),v=i(57586),b=t([c]);c=(b.then?(await b)():b)[0];const f="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",k="M11 7V9H13V7H11M14 17V15H13V11H10V13H11V15H10V17H14M22 12C22 17.5 17.5 22 12 22C6.5 22 2 17.5 2 12C2 6.5 6.5 2 12 2C17.5 2 22 6.5 22 12M20 12C20 7.58 16.42 4 12 4C7.58 4 4 7.58 4 12C4 16.42 7.58 20 12 20C16.42 20 20 16.42 20 12Z",_="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",$="M14.06,9L15,9.94L5.92,19H5V18.08L14.06,9M17.66,3C17.41,3 17.15,3.1 16.96,3.29L15.13,5.12L18.88,8.87L20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18.17,3.09 17.92,3 17.66,3M14.06,6.19L3,17.25V21H6.75L17.81,9.94L14.06,6.19Z",p=new v.r("knx-entities-view");let m=(0,s.Z)([(0,o.Mo)("knx-entities-view")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"knx_entities",value(){return[]}},{kind:"field",decorators:[(0,o.SB)()],key:"filterDevice",value(){return null}},{kind:"method",key:"firstUpdated",value:function(){this._fetchEntities()}},{kind:"method",key:"willUpdate",value:function(){const t=new URLSearchParams(h.E.location.search);this.filterDevice=t.get("device_id")}},{kind:"method",key:"_fetchEntities",value:async function(){(0,y.Bd)(this.hass).then((t=>{p.debug(`Fetched ${t.length} entity entries.`),this.knx_entities=t.map((t=>{const e=this.hass.states[t.entity_id],i=t.device_id?this.hass.devices[t.device_id]:void 0,n=t.area_id??i?.area_id,s=n?this.hass.areas[n]:void 0;return{...t,entityState:e,area:s}}))})).catch((t=>{p.error("getEntityEntries",t),(0,d.c)("/knx/error",{replace:!0,data:t})}))}},{kind:"field",key:"_columns",value(){return(0,r.Z)((t=>{const e="56px",i="176px";return{icon:{title:"",minWidth:e,maxWidth:e,type:"icon",template:t=>a.dy`
          <ha-state-icon
            slot="item-icon"
            .hass=${this.hass}
            .stateObj=${t.entityState}
          ></ha-state-icon>
        `},friendly_name:{showNarrow:!0,filterable:!0,sortable:!0,title:"Friendly Name",flex:2,template:t=>t.entityState?.attributes.friendly_name??""},entity_id:{filterable:!0,sortable:!0,title:"Entity ID",flex:1},device:{filterable:!0,sortable:!0,title:"Device",flex:1,template:t=>t.device_id?this.hass.devices[t.device_id].name??"":""},device_id:{hidden:!0,title:"Device ID",filterable:!0,template:t=>t.device_id??""},area:{title:"Area",sortable:!0,filterable:!0,flex:1,template:t=>t.area?.name??""},actions:{showNarrow:!0,title:"",minWidth:i,maxWidth:i,type:"icon-button",template:t=>a.dy`
          <ha-icon-button
            .label=${"More info"}
            .path=${k}
            .entityEntry=${t}
            @click=${this._entityMoreInfo}
          ></ha-icon-button>
          <ha-icon-button
            .label=${this.hass.localize("ui.common.edit")}
            .path=${$}
            .entityEntry=${t}
            @click=${this._entityEdit}
          ></ha-icon-button>
          <ha-icon-button
            .label=${this.hass.localize("ui.common.delete")}
            .path=${f}
            .entityEntry=${t}
            @click=${this._entityDelete}
          ></ha-icon-button>
        `}}}))}},{kind:"field",key:"_entityEdit",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,d.c)("/knx/entities/edit/"+e.entity_id)}}},{kind:"field",key:"_entityMoreInfo",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,l.B)(h.E.document.querySelector("home-assistant"),"hass-more-info",{entityId:e.entity_id})}}},{kind:"field",key:"_entityDelete",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,u.g7)(this,{text:`${this.hass.localize("ui.common.delete")} ${e.entity_id}?`}).then((t=>{t&&(0,y.Ks)(this.hass,e.entity_id).then((()=>{p.debug("entity deleted",e.entity_id),this._fetchEntities()})).catch((t=>{(0,u.Ys)(this,{title:"Deletion failed",text:t})}))}))}}},{kind:"method",key:"render",value:function(){return this.hass&&this.knx_entities?a.dy`
      <hass-tabs-subpage-data-table
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${this.tabs}
        .localizeFunc=${this.knx.localize}
        .columns=${this._columns(this.hass.language)}
        .data=${this.knx_entities}
        .hasFab=${!0}
        .searchLabel=${this.hass.localize("ui.components.data-table.search")}
        .clickable=${!1}
        .filter=${this.filterDevice}
      >
        <ha-fab
          slot="fab"
          .label=${this.hass.localize("ui.common.add")}
          extended
          @click=${this._entityCreate}
        >
          <ha-svg-icon slot="icon" .path=${_}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage-data-table>
    `:a.dy` <hass-loading-screen></hass-loading-screen> `}},{kind:"method",key:"_entityCreate",value:function(){(0,d.c)("/knx/entities/create")}},{kind:"field",static:!0,key:"styles",value(){return a.iv`
    hass-loading-screen {
      --app-header-background-color: var(--sidebar-background-color);
      --app-header-text-color: var(--sidebar-text-color);
    }
  `}}]}}),a.oi);n()}catch(f){n(f)}}))},94571:function(t,e,i){i.d(e,{C:()=>u});var n=i(2841),s=i(53232),a=i(1714);class o{constructor(t){this.G=t}disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}}class r{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null===(t=this.Z)||void 0===t||t.call(this),this.Y=this.Z=void 0}}var c=i(45779);const d=t=>!(0,s.pt)(t)&&"function"==typeof t.then,h=1073741823;class l extends a.sR{constructor(){super(...arguments),this._$C_t=h,this._$Cwt=[],this._$Cq=new o(this),this._$CK=new r}render(...t){var e;return null!==(e=t.find((t=>!d(t))))&&void 0!==e?e:n.Jb}update(t,e){const i=this._$Cwt;let s=i.length;this._$Cwt=e;const a=this._$Cq,o=this._$CK;this.isConnected||this.disconnected();for(let n=0;n<e.length&&!(n>this._$C_t);n++){const t=e[n];if(!d(t))return this._$C_t=n,t;n<s&&t===i[n]||(this._$C_t=h,s=0,Promise.resolve(t).then((async e=>{for(;o.get();)await o.get();const i=a.deref();if(void 0!==i){const n=i._$Cwt.indexOf(t);n>-1&&n<i._$C_t&&(i._$C_t=n,i.setValue(e))}})))}return n.Jb}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const u=(0,c.XM)(l)}};
//# sourceMappingURL=4978.7172040af6e42711.js.map