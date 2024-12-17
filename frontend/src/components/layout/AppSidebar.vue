<template>
  <aside class="app-sidebar" :class="{ collapsed }">
    <div class="sidebar-top">
      <div class="sidebar-header">
        <div class="brand">
          <RouterLink to="/home">
            <img v-if="!collapsed" src="@/assets/images/skagen-icon.png" alt="Skågen Icon" class="brand-icon" />
            <span v-if="!collapsed" class="brand-text mt-xs">Skågen</span>
          </RouterLink>
        </div>
        <BaseButton v-if="!collapsed" variant="text" @click="$emit('toggle-collapse')" class="mt-sm">
          <ChevronDoubleLeftIcon class="chevron-icon icon-sm" />
        </BaseButton>
        <BaseButton v-if="collapsed" variant="text" @click="$emit('toggle-collapse')" class="mt-sm">
          <ChevronDoubleRightIcon class="icon-md" />
        </BaseButton>
      </div>
      <div class="brand-baseline" v-if="!collapsed">Thought Validation</div>
    </div>

    <div class="sidebar-content">
      <!-- Menu goes here -->
    </div>

    <div class="sidebar-bottom">
      <AuthStatus
        :collapsed="collapsed"
        :is-logged-in="isLoggedIn"
        :user-name="userName"
        @sign-up="$emit('sign-up')"
        @login="$emit('login')"
        @logout="$emit('logout')"
        @toggle-user-overlay="$emit('toggle-user-overlay')"
      />
    </div>
  </aside>
</template>

<script>
import BaseButton from '../base/BaseButton.vue';
import AuthStatus from '../shared/AuthStatus.vue';
import { ChevronDoubleLeftIcon, ChevronDoubleRightIcon } from '@heroicons/vue/24/solid';

export default {
  name: 'AppSidebar',
  components: { BaseButton, AuthStatus, ChevronDoubleLeftIcon, ChevronDoubleRightIcon },
  props: {
    collapsed: {
      type: Boolean,
      default: false,
    },
    isLoggedIn: {
      type: Boolean,
      default: false,
    },
    userName: {
      type: String,
      default: null,
    },
  },
};
</script>

<style scoped>
.app-sidebar {
  transition: width 0.3s ease;
  width: 200px;
  background: var(--color-background-darker, #fff);
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.app-sidebar.collapsed {
  width: 50px;
}

.brand-text,
.brand-baseline {
  transition: opacity 0.3s ease;
}

.app-sidebar.collapsed .brand-text,
.app-sidebar.collapsed .brand-baseline {
  opacity: 0;
}

.sidebar-top {
  padding: var(--spacing-sm);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand a {
  display: flex;
  align-items: center; /* Vertically center the content */
  text-decoration: none;
  color: inherit; /* Optional: inherit text color */
}

.brand-icon {
  width: 30px;
  height: 30px;
  margin-right: var(--spacing-sm);
}

.brand-text {
  font-family: var(--font-heading, sans-serif);
  font-weight: var(--font-weight-bold, 500);
  font-size: 1.4rem;
}

.chevron-icon {
  cursor: pointer;
  color: var(--color-text, #2c3e50);
}

.brand-baseline {
  font-family: var(--font-base, sans-serif);
  font-size: 0.75rem;
  margin-top: -3px;
  color: var(--color-text-lighter, #566575);
}

.sidebar-content {
  flex: 1;
  padding: var(--spacing-md);
  overflow-y: auto;
}

.sidebar-bottom {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: var(--spacing-md);
}
</style>