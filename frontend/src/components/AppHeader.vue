<template>
  <v-app-bar color="background" flat>
    <v-toolbar-title class="text-primary">
      Skågen
    </v-toolbar-title>
    <v-spacer />
    <v-btn text color="textPrimary">Home</v-btn>
    <v-btn text color="textPrimary">About</v-btn>
    <v-btn color="primary" class="ml-4">Sign Up</v-btn>
    <v-btn outlined color="primary" class="ml-2">Login</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'AppHeader',
};
</script>

<style scoped>
.text-primary {
  color: var(--clr-primary);
}
</style>