export const ids=["2154"];export const modules={13755:function(e,o,a){a.r(o),a.d(o,{HaFormBoolean:()=>n});var i=a(44249),t=a(57243),d=a(50778),r=a(11297);a(76418),a(52158);let n=(0,i.Z)([(0,d.Mo)("ha-form-boolean")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.IO)("ha-checkbox",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return t.dy`
      <ha-formfield .label=${this.label}>
        <ha-checkbox
          .checked=${this.data}
          .disabled=${this.disabled}
          @change=${this._valueChanged}
        ></ha-checkbox>
        <span slot="label">
          <p class="primary">${this.label}</p>
          ${this.helper?t.dy`<p class="secondary">${this.helper}</p>`:t.Ld}
        </span>
      </ha-formfield>
    `}},{kind:"method",key:"_valueChanged",value:function(e){(0,r.B)(this,"value-changed",{value:e.target.checked})}},{kind:"field",static:!0,key:"styles",value(){return t.iv`
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
  `}}]}}),t.oi)}};
//# sourceMappingURL=2154.76fff78c6cff6a22.js.map