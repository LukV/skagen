<template>
  <v-app-bar color="background" flat>
    <!-- Logo and Navigation Links -->
    <v-toolbar-title>
      <span class="logo">Skågen</span>
    </v-toolbar-title>

    <v-btn-group>
      <v-btn text class="nav-link">Home</v-btn>
      <v-btn text class="nav-link">About</v-btn>
    </v-btn-group>

    <v-spacer />

    <!-- Sign Up and Login -->
    <v-btn text class="signup-button">Sign Up</v-btn>
    <v-btn outlined color="primary" class="login-button">Login</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "AppHeader",
};
</script>

<style scoped>
/* Styling for the logo */
.logo {
  font-family: "Poppins", sans-serif;
  font-weight: 300;
  font-size: 24px;
  color: var(--clr-primary);
}

/* Styling for navigation links */
.nav-link {
  text-transform: none; /* Prevent uppercase */
  font-size: 1rem; /* Adjust for readability */
  margin-left: 1rem;
}

/* Styling for buttons */
.signup-button {
  text-transform: none;
  font-size: 1rem;
}

.login-button {
  text-transform: none;
  font-size: 1rem;
}
</style>
