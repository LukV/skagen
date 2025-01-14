<template>
  <v-dialog v-model="visible" persistent max-width="400">
    <v-card>
      <v-card-title>Login</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field label="Email" v-model="email" required></v-text-field>
          <v-text-field label="Password" v-model="password" type="password" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeModal">Cancel</v-btn>
        <v-btn color="primary" @click="doLogin()">Login</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data: () => ({
    visible: true,
    email: '',
    password: '',
  }),
  methods: {
    ...mapActions(['login']),
    closeModal() {
      if (window.history.length > 1) {
        this.$router.back();
      } else {
        this.$router.push({ name: 'home' });
      }
    },
    async doLogin() {
      try {
        await this.login({
          username: this.email,
          password: this.password,
        });

        if (window.history.length > 1) {
          this.$router.back();
        } else {
          this.$router.push({ name: 'home' });
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>