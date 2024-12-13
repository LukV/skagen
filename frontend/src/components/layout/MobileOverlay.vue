<template>
    <div class="mobile-overlay" v-show="open">
      <div class="overlay-backdrop" @click="$emit('close')"></div>
      <div class="overlay-content">
        <slot></slot>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MobileOverlay',
    props: {
      open: { type: Boolean, default: false }
    }
  }
  </script>
  
  <style scoped>
  .mobile-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: none; /* hidden by default */
    z-index: 9999;
  }
  
  .mobile-overlay[style*="display: block"] {
    display: block;
  }
  
  .overlay-backdrop {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.5);
  }
  
  .overlay-content {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 200px;
    background: var(--color-secondary, #fff);
    box-shadow: 2px 0 5px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
  }
  </style>