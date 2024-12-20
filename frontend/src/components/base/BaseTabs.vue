<template>
    <div class="base-tabs">
      <div class="tabs-nav">
        <div 
          v-for="(tab, index) in tabs" 
          :key="index"
          class="tab-item" 
          :class="{ active: activeTab === tab.value }"
          @click="selectTab(tab.value)">
          {{ tab.label }}
        </div>
      </div>
      <div class="tabs-content">
        <slot></slot>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'BaseTabs',
    props: {
      tabs: {
        type: Array,
        required: true
      },
      modelValue: {
        type: String,
        default: ''
      }
    },
    computed: {
      activeTab() {
        return this.modelValue || (this.tabs.length > 0 ? this.tabs[0].value : '');
      }
    },
    methods: {
      selectTab(tabValue) {
        this.$emit('update:modelValue', tabValue);
      }
    }
  };
  </script>
  
  <style scoped>
  .base-tabs {
    display: flex;
    flex-direction: column;
  }
  
  .tabs-nav {
    display: flex;
    border-bottom: 1px solid #ddd;
  }
  
  .tab-item {
    padding: 0.75rem 1rem;
    cursor: pointer;
    position: relative;
  }
  
  .tab-item.active {
    font-weight: bold;
  }
  
  .tab-item.active::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: #000; /* underline for the active tab */
  }
  
  .tabs-content {
    padding: 1rem 0;
  }
  </style>