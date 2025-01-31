"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6942"],{3795:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73577),o=(i(19083),i(71695),i(61006),i(39527),i(99790),i(13334),i(47021),i(57243)),d=i(50778),s=i(4133),l=i(69484),r=e([l,s]);[l,s]=r.then?(await r)():r;let n,u=e=>e;(0,a.Z)([(0,d.Mo)("ha-entity-attribute-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"entityId",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Array,attribute:"hide-attributes"})],key:"hideAttributes",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean,attribute:"allow-custom-value"})],key:"allowCustomValue",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,d.IO)("ha-combo-box",!0)],key:"_comboBox",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return!(!e.has("_opened")&&this._opened)}},{kind:"method",key:"updated",value:function(e){if(e.has("_opened")&&this._opened){const e=this.entityId?this.hass.states[this.entityId]:void 0;this._comboBox.items=e?Object.keys(e.attributes).filter((e=>{var t;return!(null!==(t=this.hideAttributes)&&void 0!==t&&t.includes(e))})).map((t=>({value:t,label:(0,s.S)(this.hass.localize,e,this.hass.entities,t)}))):[]}}},{kind:"method",key:"render",value:function(){var e;return this.hass?(0,o.dy)(n||(n=u`
      <ha-combo-box
        .hass=${0}
        .value=${0}
        .autofocus=${0}
        .label=${0}
        .disabled=${0}
        .required=${0}
        .helper=${0}
        .allowCustomValue=${0}
        item-value-path="value"
        item-label-path="label"
        @opened-changed=${0}
        @value-changed=${0}
      >
      </ha-combo-box>
    `),this.hass,this.value?(0,s.S)(this.hass.localize,this.hass.states[this.entityId],this.hass.entities,this.value):"",this.autofocus,null!==(e=this.label)&&void 0!==e?e:this.hass.localize("ui.components.entity.entity-attribute-picker.attribute"),this.disabled||!this.entityId,this.required,this.helper,this.allowCustomValue,this._openedChanged,this._valueChanged):o.Ld}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){this.value=e.detail.value}}]}}),o.oi);t()}catch(n){t(n)}}))},56089:function(e,t,i){i.a(e,(async function(e,a){try{i.r(t),i.d(t,{HaSelectorAttribute:()=>v});var o=i(73577),d=i(72621),s=(i(71695),i(47021),i(57243)),l=i(50778),r=i(11297),n=i(3795),u=e([n]);n=(u.then?(await u)():u)[0];let h,c=e=>e,v=(0,o.Z)([(0,l.Mo)("ha-selector-attribute")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,t,i;return(0,s.dy)(h||(h=c`
      <ha-entity-attribute-picker
        .hass=${0}
        .entityId=${0}
        .hideAttributes=${0}
        .value=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        allow-custom-value
      ></ha-entity-attribute-picker>
    `),this.hass,(null===(e=this.selector.attribute)||void 0===e?void 0:e.entity_id)||(null===(t=this.context)||void 0===t?void 0:t.filter_entity),null===(i=this.selector.attribute)||void 0===i?void 0:i.hide_attributes,this.value,this.label,this.helper,this.disabled,this.required)}},{kind:"method",key:"updated",value:function(e){var t;if((0,d.Z)(i,"updated",this,3)([e]),!this.value||null!==(t=this.selector.attribute)&&void 0!==t&&t.entity_id||!e.has("context"))return;const a=e.get("context");if(!this.context||!a||a.filter_entity===this.context.filter_entity)return;let o=!1;if(this.context.filter_entity){const e=this.hass.states[this.context.filter_entity];e&&this.value in e.attributes||(o=!0)}else o=void 0!==this.value;o&&(0,r.B)(this,"value-changed",{value:void 0})}}]}}),s.oi);a()}catch(h){a(h)}}))}}]);
//# sourceMappingURL=6942.8839550e0b1a6f26.js.map