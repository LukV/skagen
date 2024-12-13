<template>
    <header class="app-header">
      <div class="header-left">
        <img src="@/assets/images/skagen-icon.png" alt="Skågen Icon" class="logo" />
      </div>
      <div class="header-right">
        <button class="hamburger" @click="$emit('toggle-sidebar')">
          <svg width="24" height="24" viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
        </button>
      </div>
    </header>
  </template>
  
  <script>
  export default {
    name: 'AppHeader'
  }
  </script>
  
  <style scoped>
  .app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--color-background, #fff);
    padding: var(--spacing-md);
    position: relative;
    flex-shrink: 0; /* don’t shrink */
    height: 60px;
  }
  
  .header-left, .header-right {
    display: flex;
    align-items: center;
  }
  
  .logo {
    display: none;
    height: 30px;
    width: 30px;
  }
  
  .hamburger {
    background: none;
    border: none;
    padding: var(--spacing-sm);
    cursor: pointer;
    display: none; /* hidden by default on desktop */
  }
  
  /* On smaller screens show hamburger */
  @media (max-width: 600px) {
    .hamburger {
      display: inline-block;
    }
    .logo {
      display: block;
    }
    .app-header {
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  }
  </style>