export const ids=["4082"];export const modules={65326:function(e,t,r){r.r(t),r.d(t,{HaLabelSelector:()=>d});var i=r(44249),a=r(57243),l=r(50778),s=r(24785),n=r(11297);r(92687);let d=(0,i.Z)([(0,l.Mo)("ha-selector-label")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"name",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return this.selector.label.multiple?a.dy`
        <ha-labels-picker
          no-add
          .hass=${this.hass}
          .value=${(0,s.r)(this.value??[])}
          .required=${this.required}
          .disabled=${this.disabled}
          .label=${this.label}
          @value-changed=${this._handleChange}
        >
        </ha-labels-picker>
      `:a.dy`
      <ha-label-picker
        no-add
        .hass=${this.hass}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        .label=${this.label}
        @value-changed=${this._handleChange}
      >
      </ha-label-picker>
    `}},{kind:"method",key:"_handleChange",value:function(e){let t=e.detail.value;this.value!==t&&((""===t||Array.isArray(t)&&0===t.length)&&!this.required&&(t=void 0),(0,n.B)(this,"value-changed",{value:t}))}},{kind:"field",static:!0,key:"styles",value(){return a.iv`
    ha-labels-picker {
      display: block;
      width: 100%;
    }
  `}}]}}),a.oi)},94787:function(e,t,r){r.d(t,{B:()=>l});const i=e=>{let t=[];function r(r,i){e=i?r:Object.assign(Object.assign({},e),r);let a=t;for(let t=0;t<a.length;t++)a[t](e)}return{get state(){return e},action(t){function i(e){r(e,!1)}return function(){let r=[e];for(let e=0;e<arguments.length;e++)r.push(arguments[e]);let a=t.apply(this,r);if(null!=a)return a instanceof Promise?a.then(i):i(a)}},setState:r,clearState(){e=void 0},subscribe(e){return t.push(e),()=>{!function(e){let r=[];for(let i=0;i<t.length;i++)t[i]===e?e=null:r.push(t[i]);t=r}(e)}}}},a=(e,t,r,a,l={unsubGrace:!0})=>{if(e[t])return e[t];let s,n,d=0,o=i();const u=()=>{if(!r)throw new Error("Collection does not support refresh");return r(e).then((e=>o.setState(e,!0)))},c=()=>u().catch((t=>{if(e.connected)throw t})),h=()=>{n=void 0,s&&s.then((e=>{e()})),o.clearState(),e.removeEventListener("ready",u),e.removeEventListener("disconnected",v)},v=()=>{n&&(clearTimeout(n),h())};return e[t]={get state(){return o.state},refresh:u,subscribe(t){d++,1===d&&(()=>{if(void 0!==n)return clearTimeout(n),void(n=void 0);a&&(s=a(e,o)),r&&(e.addEventListener("ready",c),c()),e.addEventListener("disconnected",v)})();const i=o.subscribe(t);return void 0!==o.state&&setTimeout((()=>t(o.state)),0),()=>{i(),d--,d||(l.unsubGrace?n=setTimeout(h,5e3):h())}}},e[t]},l=(e,t,r,i,l)=>a(i,e,t,r).subscribe(l)}};
//# sourceMappingURL=4082.b7b3eeea261dae2b.js.map