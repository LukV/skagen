<template>
  <v-app-bar color="surface" :elevation="0">
    <div class="d-flex align-center">
      <v-app-bar-title>
        <span class="logo ml-4 mr-2">Skågen</span>
      </v-app-bar-title>
      <div class="d-flex align-center">
        <div class="hidden-sm-and-down mt-1 ml-4">
          <router-link to="/home" class="nav-link mr-4">Home</router-link>
          <router-link to="/about" class="nav-link mr-4">About</router-link>
        </div>
      </div>
    </div>
    <template v-slot:append>
      <div class="hidden-sm-and-down mt-1">
        <router-link to="/auth/signup" class="nav-link mr-4">Sign up</router-link>
      </div>
      <div class="hidden-sm-and-down">
        <v-btn class="login-button mr-4 mt-1" rounded="xl" elevation="0" color="primary" href="/auth/login">Login</v-btn>
      </div>
      <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer" class="hidden-md-and-up"></v-app-bar-nav-icon>
    </template>
  </v-app-bar>
  <v-navigation-drawer v-model="drawer" :width="120" app temporary>
    <v-list>
      <v-list-item>
        <router-link to="/home" class="drawer-link">Home</router-link>
      </v-list-item>
      <v-list-item>
        <router-link to="/about" class="drawer-link">About</router-link>
      </v-list-item>
      <v-list-item>
        <router-link to="/auth/signup" class="drawer-link">Sign up</router-link>
      </v-list-item>
      <v-list-item>
        <router-link to="/auth/login" class="drawer-link">Login</router-link>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "AppHeader",
  data: () => ({
    drawer: false,
  }),

  watch: {
    group() {
      this.drawer = false
    },
  },
};
</script>

<style scoped>
.v-btn {
  padding: 0 16px;
}

.logo {
  font-family: "Poppins", sans-serif;
  font-weight: 300;
  font-size: 24px;
}

.login-button {
  background-color: var(--clr-primary) !important;
  color: var(--clr-surface) !important;
  border-radius: 8px;
  text-transform: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s, box-shadow 0.2s;
  font-size: 14px;
}

.login-button:hover {
  background-color: darken(var(--clr-secondary), 10%);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

a {
  font-size: 14px;
  color: var(--clr-primary);
  text-decoration: none;
  transition: color 0.6s ease;
}

a:hover {
  color: darken(var(--clr-header-text), 35%);
  text-decoration: underline;
}

a:active {
  color: var(--clr-primary);
}
</style>