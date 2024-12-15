
      

<template>
  <header :class="{'app-header': true, 'no-border': hideBorder}">
    <!-- Left Section -->
    <div class="header-left">
      <img src="@/assets/images/skagen-icon.png" alt="Skågen Icon" class="logo" />
      <div v-if="showSearch" class="search-container">
        <input type="text" placeholder="Search..." class="search-input" />
        <button class="search-button">
          <svg width="20" height="20" viewBox="0 0 24 24">
            <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
            <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="2" fill="none"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Right Section -->
    <div class="header-right">
      <BaseButton v-if="showShare" class="px-sm py-sm">
        <ShareIcon class="icon" /> Share
      </BaseButton>
      <button v-if="showMore" class="icon-button more-button">
        <svg width="24" height="24" viewBox="0 0 24 24">
          <circle cx="12" cy="5" r="1.5" fill="currentColor" />
          <circle cx="12" cy="12" r="1.5" fill="currentColor" />
          <circle cx="12" cy="19" r="1.5" fill="currentColor" />
        </svg>
      </button>
      <!-- Mobile Hamburger Menu -->
      <button class="hamburger" @click="$router.push('/menu')">
        <svg width="24" height="24" viewBox="0 0 24 24">
          <path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
  </header>
</template>

<script>
import { ShareIcon } from '@heroicons/vue/24/solid';
import BaseButton from '../base/BaseButton.vue';

export default {
  name: 'AppHeader',
  components: { BaseButton, ShareIcon },
  computed: {
    showSearch() {
      return this.$route.meta.showSearch;
    },
    showShare() {
      return this.$route.meta.showShare;
    },
    showMore() {
      return this.$route.meta.showMore;
    },
    hideBorder() {
      return !this.showSearch && !this.showShare && !this.showMore;
    },
  },
};
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-background, #fff);
  border-bottom: 1px solid #ddd; /* Default border */
  padding: var(--spacing-md);
  height: 8S0px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.no-border {
  border-bottom: none;
}

.header-left,
.header-right {
  display: flex;
  align-items: center;
}

/* Search Container */
.search-container {
  display: flex;
  align-items: center;
  background: #fafafa;
  border: 1px solid #ddd; /* Subtle border */
  border-radius: 8px;
  padding: 6px 12px; /* Added padding */
  margin-left: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.search-input {
  border: none;
  background: none;
  outline: none;
  padding: 4px;
  width: 200px;
}

.search-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #888;
  margin-left: 8px;
}

/* Icon Buttons */
.icon-button {
  background: none;
  border: none;
  margin-left: 10px;
  cursor: pointer;
}

.hamburger {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  margin-left: 10px;
}

.logo {
  height: 30px;
  width: 30px;
  margin-right: 10px;
  display: none;
}

.icon {
  width: 1em;
  height: 1em;
  vertical-align: middle;
}

@media (max-width: 600px) {
  .search-container,
  .share-button,
  .more-button {
    display: none;
  }
  .hamburger, .logo {
    display: inline-block;
  }
  .app-header {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 0;
  }
}
</style>