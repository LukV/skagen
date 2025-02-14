<template>
  <v-dialog v-model="visible" persistent max-width="400">
    <v-form v-model="isFormValid" @submit.prevent="signUp">
      <v-card>
        <v-card-title class="text-center">Sign Up</v-card-title>
        <v-card-text>
          <v-alert
              v-if="serverError"
              type="error"
              class="mb-4"
              dismissible
              @click:close="serverError = ''"
            >
              {{ serverError }}
          </v-alert>

          <v-btn
            class="mb-4"
            prepend-icon="mdi-google"
            rounded="xs"
            block
            @click="initializeGoogleLogin"
          >
            Continue with Google
          </v-btn>

          <v-divider> or </v-divider>

          <v-text-field 
              label="Email" 
              v-model="email" 
              autocomplete="off"
              :rules="[rules.required, rules.email]"
              required></v-text-field>

          <v-text-field 
            label="Username" 
            v-model="username" 
            required></v-text-field>

          <v-text-field 
            label="Password"
            :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'" 
            :rules="[rules.required, rules.min, rules.max, rules.letter, rules.nr]"
            v-model="password" 
            :type="show ? 'text' : 'password'"
            required
            @click:append-inner="show = !show"></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-btn text @click="closeModal">Cancel</v-btn>
          <v-btn 
              :loading="isLoading"
              color="primary" 
              type="submit">Sign Up</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';
import apiClient from "@/utils/apiClient";

export default {
  data: () => ({
    isFormValid: false,
    isLoading: false,
    visible: true,
    email: '',
    password: '',
    username: '',
    show: false,
    serverError: '',
    rules: {
      required: v => !!v || 'Required.',
      email: (v) =>
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || "Invalid email.",
      min: v => v.length >= 8 || 'Min 8 characters',
      max: v => v.length <= 128 || 'Max 128 characters',
      letter: v => /[a-zA-Z]/.test(v) || 'Password must include at least one letter.',
      nr: v => /\d/.test(v) || 'Password must include at least one number.',
    },
  }),
  methods: {
    ...mapActions(['login', 'googleLogin']),
    closeModal() {
      this.$router.push({ name: 'home' });
    },
    initializeGoogleLogin() {
      google.accounts.id.initialize({
        client_id: '283986039712-crlk7a09dvuurc8g5ogs0ihk9561kkbg.apps.googleusercontent.com',
        callback: this.handleGoogleCredentialResponse,
      });
      google.accounts.id.prompt(); // Display one-tap prompt
    },
    async handleGoogleCredentialResponse(response) {
      const token = response.credential;
      this.isLoading = true;

      try {
        await this.googleLogin({ token });

        const redirectPath = this.$route.query.redirect;
        if (redirectPath) {
          this.$router.push(redirectPath);
          return;
        }
        this.$router.push({ name: 'home' });
      } catch (error) {
        console.log(error)
        this.serverError = error.response?.data?.detail || 'Google login failed.';
      } finally {
        this.isLoading = false;
      }
    },
    async signUp() {
      if (!this.isFormValid) {
        return; // Stop if the form is invalid
      }
      this.isLoading = true;
      this.serverError = '';
      try {
        // Create a new user in the backend
        await apiClient.post('/users/', {
          email: this.email,
          username: this.username,
          password: this.password,
        });
        // Log the user in via Vuex action
        await this.login({
          username: this.username,
          password: this.password,
        });
        this.closeModal();
      } catch (error) {
        if (error.response && error.response.data && error.response.data.detail) {
          this.serverError = error.response.data.detail; // Display error from server
        } else {
          this.serverError = 'An unexpected error occurred. Please try again.';
        }
        console.log(error)
      } finally {
        this.isLoading = false;
      }
    }
  },
};
</script>