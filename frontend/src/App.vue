<template>
  <v-app>
    <router-view />
    <router-view name="modal" />
  </v-app>
</template>

<script>
export default {
  name: 'App',
};
</script>