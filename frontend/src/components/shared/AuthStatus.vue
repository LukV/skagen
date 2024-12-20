<template>
  <div class="auth-status">
    <!-- Collapsed mode -->
    <template v-if="collapsed">
      <div v-if="!isAuthenticated" class="auth-actions">
        <BaseButton variant="text" class="icon-button" @click="$router.push('/auth/login')">
          <UserIcon class="icon icon-md" />
        </BaseButton>
      </div>
      <div v-else class="auth-actions">
        <div class="user-info">
          <div class="avatar-username">
            <div class="avatar" :style="avatarStyle">
              <img v-if="user.avatar" :src="user.avatar" alt="User Avatar" class="avatar-img" />
              <span v-else class="avatar-letter">{{ user.username.charAt(0).toUpperCase() }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Expanded mode -->
    <template v-else>
      <div v-if="!isAuthenticated" class="auth-actions">
        <BaseButton variant="secondary" class="py-sm mb-xs" :rounded="true" @click="$router.push('/auth/signup')">
          Sign up
        </BaseButton>
        <BaseButton variant="primary" class="py-sm" :rounded="true" @click="$router.push('/auth/login')">
          Login
        </BaseButton>
      </div>
      <div v-else class="auth-actions">
        <div class="user-info">
          <div class="avatar-username">
            <div class="avatar" :style="avatarStyle">
              <!-- Show user's avatar if available -->
              <img v-if="user.avatar" :src="user.avatar" alt="User Avatar" class="avatar-img" />
              <!-- Otherwise, show a letter -->
              <span v-else class="avatar-letter">{{ user.username.charAt(0).toUpperCase() }}</span>
            </div>
            <span class="user-name">{{ user.username }}</span>
          </div>
          <BaseButton variant="text" class="icon-button" @click="$router.push('/account')">
            <Cog6ToothIcon class="icon icon-md" />
          </BaseButton>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import BaseButton from '../base/BaseButton.vue';
import { UserIcon, Cog6ToothIcon } from '@heroicons/vue/24/solid';
import { mapState, mapGetters } from 'vuex';

export default {
  name: 'AuthStatus',
  components: { BaseButton, UserIcon, Cog6ToothIcon },
  props: {
    collapsed: { type: Boolean, default: false },
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated']),
    avatarStyle() {
      // If we have an avatar image, no need for colored background.
      if (this.user.avatar) return {};

      // Three possible background colors and their darker text colors.
      // These should be visually distinct and have a nice contrast.
      const backgrounds = [
        { bg: '#FF5722', text: '#FFFFFF' }, // Vibrant orange, white text
        { bg: '#4CAF50', text: '#FFFFFF' }, // Bright green, white text
        { bg: '#3F51B5', text: '#FFFFFF' }, // Strong blue, white text
        { bg: '#E91E63', text: '#FFFFFF' }, // Pink, white text
        { bg: '#FFC107', text: '#000000' }, // Yellow, black text
      ];

      // For a consistent pick, we can hash the username and pick a color
      // or simply pick based on the first letter. Here we’ll do something simple:
      const index = this.user.username.charCodeAt(0) % backgrounds.length;
      const chosen = backgrounds[index];

      return {
        backgroundColor: chosen.bg,
        color: chosen.text
      };
    }
  },
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
  justify-content: space-between; /* space user info and cog icon apart */
  align-items: center;
  gap: var(--spacing-sm);
}

.avatar-username {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
  color: var(--color-text-lighter, #333);
}

.avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  flex-shrink: 0;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-letter {
  font-weight: bold;
  font-size: 1rem;
}
</style>