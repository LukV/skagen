<template>
  <v-app>
    <v-container>
      <NavigationDrawer v-model:drawer="drawer" />
      <AppBar @toggle-drawer="toggleDrawer" />
      <v-main>
        <router-view />
        <router-view name="modal" />
      </v-main>
    </v-container>
  </v-app>
</template>

<script>
import NavigationDrawer from "@/components/NavigationDrawer.vue";
import AppBar from "@/components/AppBar.vue";

export default {
  name: 'App',
  components: {
    NavigationDrawer,
    AppBar,
  },
  data: () => ({
    drawer: true,
  }),
  methods: {
    toggleDrawer() {
      this.drawer = !this.drawer;
    },
  },
};
</script>

<style>
.logo-container {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    background-color: white;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>