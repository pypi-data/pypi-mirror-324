export const ids=["3032"];export const modules={37629:function(e,a,o){o.r(a),o.d(a,{HaBooleanSelector:()=>r});var t=o(44249),d=o(57243),i=o(50778),l=o(11297);o(52158),o(29939),o(20663);let r=(0,t.Z)([(0,i.Mo)("ha-selector-boolean")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"value",value(){return!1}},{kind:"field",decorators:[(0,i.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){return d.dy`
      <ha-formfield alignEnd spaceBetween .label=${this.label}>
        <ha-switch
          .checked=${this.value??!0===this.placeholder}
          @change=${this._handleChange}
          .disabled=${this.disabled}
        ></ha-switch>
        <span slot="label">
          <p class="primary">${this.label}</p>
          ${this.helper?d.dy`<p class="secondary">${this.helper}</p>`:d.Ld}
        </span>
      </ha-formfield>
    `}},{kind:"method",key:"_handleChange",value:function(e){const a=e.target.checked;this.value!==a&&(0,l.B)(this,"value-changed",{value:a})}},{kind:"field",static:!0,key:"styles",value(){return d.iv`
    ha-formfield {
      display: flex;
      min-height: 56px;
      align-items: center;
      --mdc-typography-body2-font-size: 1em;
    }
    p {
      margin: 0;
    }
    .secondary {
      direction: var(--direction);
      padding-top: 4px;
      box-sizing: border-box;
      color: var(--secondary-text-color);
      font-size: 0.875rem;
      font-weight: var(--mdc-typography-body2-font-weight, 400);
    }
  `}}]}}),d.oi)}};
//# sourceMappingURL=3032.6b24422accb1e20f.js.map