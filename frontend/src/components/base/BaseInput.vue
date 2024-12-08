<template>
    <div class="input-field-container">
      <div
        :class="[
          'input-wrapper',
          { 'input-wrapper--error': hasError }
        ]"
      >
        <!-- Left Icon Slot -->
        <span v-if="$slots['icon-left']" class="input-icon input-icon--left">
          <slot name="icon-left" />
        </span>
  
        <input
          :id="inputId"
          class="base-input"
          :type="showPassword ? 'text' : type"
          :disabled="disabled"
          :value="modelValue"
          :placeholder="(!label || isFloating) ? placeholder : ''"
          @focus="onFocus"
          @blur="onBlur"
          @input="updateValue"
          :style="{ paddingLeft: iconPaddingLeft, paddingRight: iconPaddingRight }"
          :aria-invalid="hasError ? 'true' : 'false'"
          :aria-describedby="hasError ? errorId : null"
        />
  
        <!-- Label (only shown if label prop is provided) -->
        <label
          v-if="label"
          :for="inputId"
          :class="['input-label', { 'input-label--floating': isFloating }]"
        >
          {{ label }}
        </label>
  
        <!-- Right Icon Slot / Password Toggle -->
        <span
          v-if="$slots['icon-right'] || (type === 'password' && !disabled)"
          class="input-icon input-icon--right"
          @click="togglePassword"
        >
          <slot name="icon-right" />
          <template v-if="type === 'password'">
            <i :class="showPassword ? 'fa fa-eye-slash' : 'fa fa-eye'"></i>
          </template>
        </span>
      </div>
  
      <!-- Validation Error -->
      <p v-if="errorMessage" :id="errorId" class="input-error-message">
        {{ errorMessage }}
      </p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'BaseInput',
    props: {
      type: { type: String, default: 'text' },
      label: { type: String, default: '' },
      placeholder: { type: String, default: '' },
      disabled: { type: Boolean, default: false },
      modelValue: { type: String, default: '' },
      required: { type: Boolean, default: false }
    },
    data() {
      return {
        isFocused: false,
        showPassword: false,
        inputId: 'input-' + Math.random().toString(36).substring(2, 9),
        errorId: 'error-' + Math.random().toString(36).substring(2, 9),
        errorMessage: ''
      };
    },
    computed: {
      hasError() {
        return this.errorMessage !== '';
      },
      isFloating() {
        return this.isFocused || (this.modelValue && this.modelValue.trim() !== '');
      },
      iconPaddingLeft() {
        return this.$slots['icon-left'] ? '36px' : '12px';
      },
      iconPaddingRight() {
        return (this.$slots['icon-right'] || (this.type === 'password' && !this.disabled)) ? '36px' : '12px';
      }
    },
    methods: {
      onFocus() {
        this.isFocused = true;
      },
      onBlur() {
        this.isFocused = false;
        if (this.required && !this.modelValue) {
          this.errorMessage = 'This field is required.';
        } else {
          this.errorMessage = '';
        }
      },
      togglePassword() {
        if (this.type === 'password') {
          this.showPassword = !this.showPassword;
        }
      },
      updateValue(event) {
        this.$emit('update:modelValue', event.target.value);
      }
    }
  };
  </script>
  
  <style scoped>
  .input-field-container {
    position: relative;
    width: 100%;
    margin-bottom: 16px;
  }
  
  .input-wrapper {
    position: relative;
    width: 100%;
    border: 1px solid #ccc;
    transition: border-color 0.2s ease-in-out;
    border-radius: 0;
  }
  
  .input-wrapper:focus-within {
    border-color: #6200ee;
  }
  
  .input-wrapper--error {
    border-color: red;
  }
  
  /* Label */
  .input-label {
    position: absolute;
    top: 50%;
    left: 12px;
    transform: translateY(-50%);
    color: #888;
    font-size: 1rem;
    transition: all 0.2s ease-in-out;
    pointer-events: none;
  }
  
  .input-label--floating {
    top: 0;
    transform: translateY(-100%);
    font-size: 0.75rem;
    color: #6200ee;
  }
  
  /* Input */
  .base-input {
    width: 100%;
    padding: 12px;
    border: none;
    font-size: 1rem;
    background-color: transparent;
    transition: background-color 0.2s ease-in-out;
  }
  
  .base-input:focus {
    outline: none;
  }
  
  /* Icons */
  .input-icon {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1rem;
    color: #888;
    cursor: pointer;
  }
  
  .input-icon--left {
    left: 12px;
  }
  
  .input-icon--right {
    right: 12px;
  }
  
  .input-icon:hover {
    color: #444;
  }
  
  /* Validation Error Message */
  .input-error-message {
    position: absolute;
    left: 12px;
    color: red;
    font-size: 0.75rem;
    background: #fff; 
    padding: 1px 4px;
    z-index: 10; 
  }
  </style>
  