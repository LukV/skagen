<template>
    <v-dialog v-model="visible" persistent max-width="400">
      <v-card>
        <v-card-title>Sign Up</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field label="Email" required></v-text-field>
            <v-text-field label="Password" type="password" required></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeModal">Cancel</v-btn>
          <v-btn color="primary">Sign Up</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  export default {
    data: () => ({
      visible: true,
    }),
    methods: {
      closeModal() {
        this.$router.push({ name: 'home' });
      },
    },
  };
  </script>