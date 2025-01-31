/*! For license information please see 1860.72a41555735952e1.js.LICENSE.txt */
export const ids=["1860"];export const modules={2322:function(t,e,i){i.a(t,(async function(t,s){try{i.r(e),i.d(e,{HaIconSelector:()=>u});var n=i(44249),o=i(57243),a=i(50778),r=i(94571),c=i(11297),d=i(92014),h=i(13270),l=t([h,d]);[h,d]=l.then?(await l)():l;let u=(0,n.Z)([(0,a.Mo)("ha-selector-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){const t=this.context?.icon_entity,e=t?this.hass.states[t]:void 0,i=this.selector.icon?.placeholder||e?.attributes.icon||e&&(0,r.C)((0,d.gD)(this.hass,e));return o.dy`
      <ha-icon-picker
        .hass=${this.hass}
        .label=${this.label}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .placeholder=${this.selector.icon?.placeholder??i}
        @value-changed=${this._valueChanged}
      >
        ${!i&&e?o.dy`
              <ha-state-icon
                slot="fallback"
                .hass=${this.hass}
                .stateObj=${e}
              ></ha-state-icon>
            `:o.Ld}
      </ha-icon-picker>
    `}},{kind:"method",key:"_valueChanged",value:function(t){(0,c.B)(this,"value-changed",{value:t.detail.value})}}]}}),o.oi);s()}catch(u){s(u)}}))},13270:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(44249),n=i(57243),o=i(50778),a=i(94571),r=i(43420),c=i(92014),d=(i(10508),t([c]));c=(d.then?(await d)():d)[0];(0,s.Z)([(0,o.Mo)("ha-state-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"stateValue",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"icon",value:void 0},{kind:"method",key:"render",value:function(){const t=this.icon||this.stateObj&&this.hass?.entities[this.stateObj.entity_id]?.icon||this.stateObj?.attributes.icon;if(t)return n.dy`<ha-icon .icon=${t}></ha-icon>`;if(!this.stateObj)return n.Ld;if(!this.hass)return this._renderFallback();const e=(0,c.gD)(this.hass,this.stateObj,this.stateValue).then((t=>t?n.dy`<ha-icon .icon=${t}></ha-icon>`:this._renderFallback()));return n.dy`${(0,a.C)(e)}`}},{kind:"method",key:"_renderFallback",value:function(){const t=(0,r.N)(this.stateObj);return n.dy`
      <ha-svg-icon
        .path=${c.Ls[t]||c.Rb}
      ></ha-svg-icon>
    `}}]}}),n.oi);e()}catch(h){e(h)}}))},94571:function(t,e,i){i.d(e,{C:()=>u});var s=i(2841),n=i(53232),o=i(1714);class a{constructor(t){this.G=t}disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}}class r{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null===(t=this.Z)||void 0===t||t.call(this),this.Y=this.Z=void 0}}var c=i(45779);const d=t=>!(0,n.pt)(t)&&"function"==typeof t.then,h=1073741823;class l extends o.sR{constructor(){super(...arguments),this._$C_t=h,this._$Cwt=[],this._$Cq=new a(this),this._$CK=new r}render(...t){var e;return null!==(e=t.find((t=>!d(t))))&&void 0!==e?e:s.Jb}update(t,e){const i=this._$Cwt;let n=i.length;this._$Cwt=e;const o=this._$Cq,a=this._$CK;this.isConnected||this.disconnected();for(let s=0;s<e.length&&!(s>this._$C_t);s++){const t=e[s];if(!d(t))return this._$C_t=s,t;s<n&&t===i[s]||(this._$C_t=h,n=0,Promise.resolve(t).then((async e=>{for(;a.get();)await a.get();const i=o.deref();if(void 0!==i){const s=i._$Cwt.indexOf(t);s>-1&&s<i._$C_t&&(i._$C_t=s,i.setValue(e))}})))}return s.Jb}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const u=(0,c.XM)(l)}};
//# sourceMappingURL=1860.72a41555735952e1.js.map