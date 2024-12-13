<template>
    <div class="auth-status">
      <!-- Collapsed mode: Always show a user icon button -->
      <template v-if="collapsed">
        <BaseButton variant="text" class="icon-button" @click="handleCollapsedClick">
          <UserIcon class="icon icon-md" />
        </BaseButton>
      </template>
  
      <!-- Expanded mode -->
      <template v-else>
        <div v-if="!isLoggedIn" class="auth-actions">
          <BaseButton variant="secondary" class="full-width px-md py-sm mb-xs" :rounded="true" @click="$emit('sign-up')">Sign up</BaseButton>
          <BaseButton variant="primary" class="full-width px-md py-sm" :rounded="true" @click="$emit('login')">Login</BaseButton>
        </div>
        <div v-else class="auth-actions">
          <div class="user-info">
            <span class="user-name">{{ userName }}</span>
            <BaseButton variant="text" @click="$emit('toggle-user-overlay')">Menu</BaseButton>
          </div>
          <BaseButton variant="text" class="full-width" @click="$emit('logout')">Logout</BaseButton>
        </div>
      </template>
    </div>
  </template>
  
  <script>
  import BaseButton from '../base/BaseButton.vue';
  import { UserIcon } from '@heroicons/vue/24/solid';
  
  export default {
    name: 'AuthStatus',
    components: { BaseButton, UserIcon },
    props: {
      collapsed: {
        type: Boolean,
        default: false
      },
      isLoggedIn: {
        type: Boolean,
        default: false
      },
      userName: {
        type: String,
        default: null
      }
    },
    methods: {
      handleCollapsedClick() {
        // If collapsed:
        // - If logged in, show overlay or menu (toggle-user-overlay)
        // - If logged out, perhaps show login/sign-up overlay?
        if (this.isLoggedIn) {
          this.$emit('toggle-user-overlay');
        } else {
          // Not logged in: for now, let's just open the sign-up or login
          // You could decide to directly open a login modal or something else.
          this.$emit('login'); 
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .auth-status {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    width: 100%;
  }
  
  .full-width {
    width: 100%;
  }
  
  .auth-actions {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .user-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .user-name {
    font-weight: bold;
    margin-right: var(--spacing-sm);
  }
  
  .icon-button {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .icon {
    flex-shrink: 0;
    flex-grow: 0;
  }
  </style>