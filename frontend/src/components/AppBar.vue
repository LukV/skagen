<template>
  <v-app-bar>
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')"></v-app-bar-nav-icon>
    <v-spacer></v-spacer>

    <template v-if="isAuthenticated">
      <v-menu offset-y>
        <template v-slot:activator="{ props }">
          <v-avatar
            v-bind="props"
            class="mr-4"
            color="tertiary"
            size="32"
            style="cursor: pointer;"
          >
            <template v-if="user?.icon">
              <img :src="userIcon" alt="User Icon" />
            </template>
            <template v-else>
              {{ userInitials }}
            </template>
          </v-avatar>
        </template>
        <v-list>
          <v-list-item @click="viewProfile">
            <v-list-item-title>View Profile</v-list-item-title>
          </v-list-item>
          <v-list-item @click="doLogout">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
    <template v-else>
      <v-btn color="secondary" variant="text" class="mr-2" @click="goToSignup">
        Sign Up
      </v-btn>
      <v-btn color="primary" variant="flat" class="mr-4" @click="goToLogin">
        Log In
      </v-btn>
    </template>
  </v-app-bar>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated']),

    // Compute the user initials dynamically
    userInitials() {
      if (this.user?.username) {
        const initials = this.user.username.match(/[A-Z]/g) || [];
        return initials.length >= 2 ? initials.slice(0, 2).join('') : initials[0] || this.user.username[0].toUpperCase();
      } else if (this.user?.email) {
        const [localPart] = this.user.email.split('@');
        const parts = localPart.split('.');
        if (parts.length > 1) {
          return parts[0][0].toUpperCase() + parts[1][0].toUpperCase();
        }
        return localPart[0].toUpperCase();
      }
      return '❤️'; // Default fallback
    },

    // Compute the user icon URL
    userIcon() {
      return this.user?.icon ? `http://localhost:8000/avatars/${this.user.icon}` : null;
    },
  },
  methods: {
    ...mapActions(['logout']),

    async doLogout() {
      await this.logout();
      this.$router.push('/home');
    },

    viewProfile() {
      console.log('View Profile clicked!');
    },

    goToSignup() {
      this.$router.push({ name: 'signup' });
    },

    goToLogin() {
      this.$router.push({ name: 'login' });
    },
  },
};
</script>