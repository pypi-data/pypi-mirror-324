export const ids=["6942"];export const modules={3795:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(44249),o=i(57243),s=i(50778),d=i(4133),l=(i(69484),e([d]));d=(l.then?(await l)():l)[0];(0,a.Z)([(0,s.Mo)("ha-entity-attribute-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"entityId",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Array,attribute:"hide-attributes"})],key:"hideAttributes",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,attribute:"allow-custom-value"})],key:"allowCustomValue",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,s.IO)("ha-combo-box",!0)],key:"_comboBox",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return!(!e.has("_opened")&&this._opened)}},{kind:"method",key:"updated",value:function(e){if(e.has("_opened")&&this._opened){const e=this.entityId?this.hass.states[this.entityId]:void 0;this._comboBox.items=e?Object.keys(e.attributes).filter((e=>!this.hideAttributes?.includes(e))).map((t=>({value:t,label:(0,d.S)(this.hass.localize,e,this.hass.entities,t)}))):[]}}},{kind:"method",key:"render",value:function(){return this.hass?o.dy`
      <ha-combo-box
        .hass=${this.hass}
        .value=${this.value?(0,d.S)(this.hass.localize,this.hass.states[this.entityId],this.hass.entities,this.value):""}
        .autofocus=${this.autofocus}
        .label=${this.label??this.hass.localize("ui.components.entity.entity-attribute-picker.attribute")}
        .disabled=${this.disabled||!this.entityId}
        .required=${this.required}
        .helper=${this.helper}
        .allowCustomValue=${this.allowCustomValue}
        item-value-path="value"
        item-label-path="label"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
      </ha-combo-box>
    `:o.Ld}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){this.value=e.detail.value}}]}}),o.oi);t()}catch(r){t(r)}}))},56089:function(e,t,i){i.a(e,(async function(e,a){try{i.r(t),i.d(t,{HaSelectorAttribute:()=>h});var o=i(44249),s=i(72621),d=i(57243),l=i(50778),r=i(11297),n=i(3795),u=e([n]);n=(u.then?(await u)():u)[0];let h=(0,o.Z)([(0,l.Mo)("ha-selector-attribute")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return d.dy`
      <ha-entity-attribute-picker
        .hass=${this.hass}
        .entityId=${this.selector.attribute?.entity_id||this.context?.filter_entity}
        .hideAttributes=${this.selector.attribute?.hide_attributes}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-value
      ></ha-entity-attribute-picker>
    `}},{kind:"method",key:"updated",value:function(e){if((0,s.Z)(i,"updated",this,3)([e]),!this.value||this.selector.attribute?.entity_id||!e.has("context"))return;const t=e.get("context");if(!this.context||!t||t.filter_entity===this.context.filter_entity)return;let a=!1;if(this.context.filter_entity){const e=this.hass.states[this.context.filter_entity];e&&this.value in e.attributes||(a=!0)}else a=void 0!==this.value;a&&(0,r.B)(this,"value-changed",{value:void 0})}}]}}),d.oi);a()}catch(h){a(h)}}))}};
//# sourceMappingURL=6942.844310da2bf62fcf.js.map