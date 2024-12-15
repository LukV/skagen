<template>
  <div class="auth-status">
    <!-- Collapsed mode -->
    <template v-if="collapsed">
      <BaseButton variant="text" class="icon-button" @click="$router.push('/auth/login')">
        <UserIcon class="icon icon-md" />
      </BaseButton>
    </template>

    <!-- Expanded mode -->
    <template v-else>
      <div v-if="!isLoggedIn" class="auth-actions">
        <BaseButton variant="secondary" class="py-sm mb-xs" :rounded="true" @click="$router.push('/auth/signup')">
          Sign up
        </BaseButton>
        <BaseButton variant="primary" class="py-sm" :rounded="true" @click="$router.push('/auth/login')">
          Login
        </BaseButton>
      </div>
      <div v-else class="auth-actions">
        <div class="user-info">
          <span class="user-name">{{ userName }}</span>
          <BaseButton variant="text" @click="toggleMenu">Menu</BaseButton>
        </div>
        <BaseButton variant="text" @click="logout">
          Logout
        </BaseButton>
      </div>
    </template>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import BaseButton from '../base/BaseButton.vue';
import { UserIcon } from '@heroicons/vue/24/solid';

export default {
  name: 'AuthStatus',
  components: { BaseButton, UserIcon },
  props: {
    collapsed: { type: Boolean, default: false },
    isLoggedIn: { type: Boolean, default: false },
    userName: { type: String, default: null }
  },
  setup() {
    const router = useRouter();

    const goToLogin = () => router.push('/auth/login');
    const goToSignup = () => router.push('/auth/signup');
    const goToForgotPassword = () => router.push('/auth/forget-password');
    const logout = () => {
      alert('Logged out'); // Replace with actual logout logic
    };

    return {
      goToLogin,
      goToSignup,
      goToForgotPassword,
      logout
    };
  }
};
</script>

<style scoped>
.auth-status {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
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