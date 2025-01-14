<template>
  <v-app-bar>
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')"></v-app-bar-nav-icon>
    <v-spacer></v-spacer>

    <template v-if="isAuthenticated">
      <v-menu offset-y>
        <template v-slot:activator="{ props }">
          <v-avatar v-bind="props" class="mr-4" color="tertiary" size="32">
            {{ userInitials}}
          </v-avatar>
        </template>
        <v-list>
          <v-list-item @click="viewProfile">
            <v-list-item-title>View Profile</v-list-item-title>
          </v-list-item>
          <v-list-item @click="logout">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
    <template v-else>
      <v-btn color="secondary" variant="text" class="mr-2" @click="goToSignup">Sign Up</v-btn>
      <v-btn color="primary" variant="flat" class="mr-4" @click="goToLogin">Log In</v-btn>
    </template>
  </v-app-bar>
</template>

<script>
import { mapState, mapGetters } from 'vuex';

export default {
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated']),

    // Compute the user initials dynamically
    userInitials() {
      console.log(this.user);
      if (this.user?.username) {
        // Use first two capital letters from username, or fallback to first letter
        const initials = this.user.username.match(/[A-Z]/g) || [];
        return initials.length >= 2 ? initials.slice(0, 2).join('') : initials[0] || this.user.username[0].toUpperCase();
      } else if (this.user?.email) {
        // Derive initials from email
        const [localPart] = this.user.email.split('@');
        const parts = localPart.split('.');
        if (parts.length > 1) {
          return parts[0][0].toUpperCase() + parts[1][0].toUpperCase();
        }
        return localPart[0].toUpperCase();
      }
      return '❤️'; // Default fallback
    },
  },
  methods: {
    viewProfile() {
      console.log("View Profile clicked!");
    },
    logout() {
      console.log("Logout clicked!");
      this.$emit("logout");
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