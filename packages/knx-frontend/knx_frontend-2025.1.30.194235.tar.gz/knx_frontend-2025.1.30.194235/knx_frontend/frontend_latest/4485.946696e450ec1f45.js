export const ids=["4485"];export const modules={45501:function(e,i,t){var a=t(44249),d=(t(87319),t(57243)),l=t(50778),s=t(20552),n=t(11297),r=t(81036);t(58130),t(59897),t(70596),t(20663);(0,a.Z)([(0,l.Mo)("ha-base-time-input")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:"auto-validate",type:Boolean})],key:"autoValidate",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"format",value(){return 12}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"days",value(){return 0}},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"hours",value(){return 0}},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"minutes",value(){return 0}},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"seconds",value(){return 0}},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"milliseconds",value(){return 0}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"dayLabel",value(){return""}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hourLabel",value(){return""}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"minLabel",value(){return""}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"secLabel",value(){return""}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"millisecLabel",value(){return""}},{kind:"field",decorators:[(0,l.Cb)({attribute:"enable-second",type:Boolean})],key:"enableSecond",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:"enable-millisecond",type:Boolean})],key:"enableMillisecond",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:"enable-day",type:Boolean})],key:"enableDay",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:"no-hours-limit",type:Boolean})],key:"noHoursLimit",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"amPm",value(){return"AM"}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"clearable",value:void 0},{kind:"method",key:"render",value:function(){return d.dy`
      ${this.label?d.dy`<label>${this.label}${this.required?" *":""}</label>`:d.Ld}
      <div class="time-input-wrap-wrap">
        <div class="time-input-wrap">
          ${this.enableDay?d.dy`
                <ha-textfield
                  id="day"
                  type="number"
                  inputmode="numeric"
                  .value=${this.days.toFixed()}
                  .label=${this.dayLabel}
                  name="days"
                  @change=${this._valueChanged}
                  @focusin=${this._onFocus}
                  no-spinner
                  .required=${this.required}
                  .autoValidate=${this.autoValidate}
                  min="0"
                  .disabled=${this.disabled}
                  suffix=":"
                  class="hasSuffix"
                >
                </ha-textfield>
              `:d.Ld}

          <ha-textfield
            id="hour"
            type="number"
            inputmode="numeric"
            .value=${this.hours.toFixed()}
            .label=${this.hourLabel}
            name="hours"
            @change=${this._valueChanged}
            @focusin=${this._onFocus}
            no-spinner
            .required=${this.required}
            .autoValidate=${this.autoValidate}
            maxlength="2"
            max=${(0,s.o)(this._hourMax)}
            min="0"
            .disabled=${this.disabled}
            suffix=":"
            class="hasSuffix"
          >
          </ha-textfield>
          <ha-textfield
            id="min"
            type="number"
            inputmode="numeric"
            .value=${this._formatValue(this.minutes)}
            .label=${this.minLabel}
            @change=${this._valueChanged}
            @focusin=${this._onFocus}
            name="minutes"
            no-spinner
            .required=${this.required}
            .autoValidate=${this.autoValidate}
            maxlength="2"
            max="59"
            min="0"
            .disabled=${this.disabled}
            .suffix=${this.enableSecond?":":""}
            class=${this.enableSecond?"has-suffix":""}
          >
          </ha-textfield>
          ${this.enableSecond?d.dy`<ha-textfield
                id="sec"
                type="number"
                inputmode="numeric"
                .value=${this._formatValue(this.seconds)}
                .label=${this.secLabel}
                @change=${this._valueChanged}
                @focusin=${this._onFocus}
                name="seconds"
                no-spinner
                .required=${this.required}
                .autoValidate=${this.autoValidate}
                maxlength="2"
                max="59"
                min="0"
                .disabled=${this.disabled}
                .suffix=${this.enableMillisecond?":":""}
                class=${this.enableMillisecond?"has-suffix":""}
              >
              </ha-textfield>`:d.Ld}
          ${this.enableMillisecond?d.dy`<ha-textfield
                id="millisec"
                type="number"
                .value=${this._formatValue(this.milliseconds,3)}
                .label=${this.millisecLabel}
                @change=${this._valueChanged}
                @focusin=${this._onFocus}
                name="milliseconds"
                no-spinner
                .required=${this.required}
                .autoValidate=${this.autoValidate}
                maxlength="3"
                max="999"
                min="0"
                .disabled=${this.disabled}
              >
              </ha-textfield>`:d.Ld}
          ${!this.clearable||this.required||this.disabled?d.Ld:d.dy`<ha-icon-button
                label="clear"
                @click=${this._clearValue}
                .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              ></ha-icon-button>`}
        </div>

        ${24===this.format?d.Ld:d.dy`<ha-select
              .required=${this.required}
              .value=${this.amPm}
              .disabled=${this.disabled}
              name="amPm"
              naturalMenuWidth
              fixedMenuPosition
              @selected=${this._valueChanged}
              @closed=${r.U}
            >
              <mwc-list-item value="AM">AM</mwc-list-item>
              <mwc-list-item value="PM">PM</mwc-list-item>
            </ha-select>`}
      </div>
      ${this.helper?d.dy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:d.Ld}
    `}},{kind:"method",key:"_clearValue",value:function(){(0,n.B)(this,"value-changed")}},{kind:"method",key:"_valueChanged",value:function(e){const i=e.currentTarget;this[i.name]="amPm"===i.name?i.value:Number(i.value);const t={hours:this.hours,minutes:this.minutes,seconds:this.seconds,milliseconds:this.milliseconds};this.enableDay&&(t.days=this.days),12===this.format&&(t.amPm=this.amPm),(0,n.B)(this,"value-changed",{value:t})}},{kind:"method",key:"_onFocus",value:function(e){e.currentTarget.select()}},{kind:"method",key:"_formatValue",value:function(e,i=2){return e.toString().padStart(i,"0")}},{kind:"get",key:"_hourMax",value:function(){if(!this.noHoursLimit)return 12===this.format?12:23}},{kind:"field",static:!0,key:"styles",value(){return d.iv`
    :host([clearable]) {
      position: relative;
    }
    :host {
      display: block;
    }
    .time-input-wrap-wrap {
      display: flex;
    }
    .time-input-wrap {
      display: flex;
      flex: 1;
      border-radius: var(--mdc-shape-small, 4px) var(--mdc-shape-small, 4px) 0 0;
      overflow: hidden;
      position: relative;
      direction: ltr;
      padding-right: 3px;
    }
    ha-textfield {
      width: 55px;
      flex-grow: 1;
      text-align: center;
      --mdc-shape-small: 0;
      --text-field-appearance: none;
      --text-field-padding: 0 4px;
      --text-field-suffix-padding-left: 2px;
      --text-field-suffix-padding-right: 0;
      --text-field-text-align: center;
    }
    ha-textfield.hasSuffix {
      --text-field-padding: 0 0 0 4px;
    }
    ha-textfield:first-child {
      --text-field-border-top-left-radius: var(--mdc-shape-medium);
    }
    ha-textfield:last-child {
      --text-field-border-top-right-radius: var(--mdc-shape-medium);
    }
    ha-select {
      --mdc-shape-small: 0;
      width: 85px;
    }
    :host([clearable]) .mdc-select__anchor {
      padding-inline-end: var(--select-selected-text-padding-end, 12px);
    }
    ha-icon-button {
      position: relative;
      --mdc-icon-button-size: 36px;
      --mdc-icon-size: 20px;
      color: var(--secondary-text-color);
      direction: var(--direction);
      display: flex;
      align-items: center;
      background-color: var(--mdc-text-field-fill-color, whitesmoke);
      border-bottom-style: solid;
      border-bottom-width: 1px;
    }
    label {
      -moz-osx-font-smoothing: grayscale;
      -webkit-font-smoothing: antialiased;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      line-height: var(--mdc-typography-body2-line-height, 1.25rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      letter-spacing: var(
        --mdc-typography-body2-letter-spacing,
        0.0178571429em
      );
      text-decoration: var(--mdc-typography-body2-text-decoration, inherit);
      text-transform: var(--mdc-typography-body2-text-transform, inherit);
      color: var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));
      padding-left: 4px;
      padding-inline-start: 4px;
      padding-inline-end: initial;
    }
    ha-input-helper-text {
      padding-top: 8px;
      line-height: normal;
    }
  `}}]}}),d.oi)},22371:function(e,i,t){var a=t(44249),d=t(57243),l=t(50778),s=t(11297);t(45501);(0,a.Z)([(0,l.Mo)("ha-duration-input")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:"enable-millisecond",type:Boolean})],key:"enableMillisecond",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:"enable-day",type:Boolean})],key:"enableDay",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.IO)("paper-time-input",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return d.dy`
      <ha-base-time-input
        .label=${this.label}
        .helper=${this.helper}
        .required=${this.required}
        .clearable=${!this.required&&void 0!==this.data}
        .autoValidate=${this.required}
        .disabled=${this.disabled}
        errorMessage="Required"
        enable-second
        .enableMillisecond=${this.enableMillisecond}
        .enableDay=${this.enableDay}
        format="24"
        .days=${this._days}
        .hours=${this._hours}
        .minutes=${this._minutes}
        .seconds=${this._seconds}
        .milliseconds=${this._milliseconds}
        @value-changed=${this._durationChanged}
        no-hours-limit
        dayLabel="dd"
        hourLabel="hh"
        minLabel="mm"
        secLabel="ss"
        millisecLabel="ms"
      ></ha-base-time-input>
    `}},{kind:"get",key:"_days",value:function(){return this.data?.days?Number(this.data.days):this.required||this.data?0:NaN}},{kind:"get",key:"_hours",value:function(){return this.data?.hours?Number(this.data.hours):this.required||this.data?0:NaN}},{kind:"get",key:"_minutes",value:function(){return this.data?.minutes?Number(this.data.minutes):this.required||this.data?0:NaN}},{kind:"get",key:"_seconds",value:function(){return this.data?.seconds?Number(this.data.seconds):this.required||this.data?0:NaN}},{kind:"get",key:"_milliseconds",value:function(){return this.data?.milliseconds?Number(this.data.milliseconds):this.required||this.data?0:NaN}},{kind:"method",key:"_durationChanged",value:function(e){e.stopPropagation();const i=e.detail.value?{...e.detail.value}:void 0;i&&(i.hours||=0,i.minutes||=0,i.seconds||=0,"days"in i&&(i.days||=0),"milliseconds"in i&&(i.milliseconds||=0),this.enableMillisecond||i.milliseconds?i.milliseconds>999&&(i.seconds+=Math.floor(i.milliseconds/1e3),i.milliseconds%=1e3):delete i.milliseconds,i.seconds>59&&(i.minutes+=Math.floor(i.seconds/60),i.seconds%=60),i.minutes>59&&(i.hours+=Math.floor(i.minutes/60),i.minutes%=60),this.enableDay&&i.hours>24&&(i.days=(i.days??0)+Math.floor(i.hours/24),i.hours%=24)),(0,s.B)(this,"value-changed",{value:i})}}]}}),d.oi)},120:function(e,i,t){t.r(i),t.d(i,{HaTimeDuration:()=>s});var a=t(44249),d=t(57243),l=t(50778);t(22371);let s=(0,a.Z)([(0,l.Mo)("ha-selector-duration")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return d.dy`
      <ha-duration-input
        .label=${this.label}
        .helper=${this.helper}
        .data=${this.value}
        .disabled=${this.disabled}
        .required=${this.required}
        .enableDay=${this.selector.duration?.enable_day}
        .enableMillisecond=${this.selector.duration?.enable_millisecond}
      ></ha-duration-input>
    `}}]}}),d.oi)}};
//# sourceMappingURL=4485.946696e450ec1f45.js.map