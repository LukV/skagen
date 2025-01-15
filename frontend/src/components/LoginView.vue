<template>
  <v-dialog v-model="visible" persistent max-width="400">
    <v-form v-model="isFormValid" @submit.prevent="doLogin">
      <v-card>
        <v-card-title class="text-center">Login</v-card-title>
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

          <!-- Email Input -->
          <v-text-field
            label="Email"
            v-model="email"
            autocomplete="off"
            required
            class="mt-4"
            :rules="[rules.required, rules.email]"
          ></v-text-field>

          <!-- Password Input -->
          <v-text-field
            label="Password"
            :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required]"
            v-model="password"
            :type="show ? 'text' : 'password'"
            required
            @click:append-inner="show = !show"
          ></v-text-field>

          <!-- Forgot Password Link -->
          <router-link
            to="/auth/forgot-password"
            class="text-body-2 forgot-password-link"
          >
            Forgot Password?
          </router-link>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeModal">Cancel</v-btn>
          <v-btn :loading="isLoading" color="primary" type="submit">
            Login
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data: () => ({
    isFormValid: false,
    isLoading: false,
    visible: true,
    email: '',
    password: '',
    show: false,
    serverError: '',
    rules: {
      required: v => !!v || 'Required.',
      email: (v) =>
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || "Invalid email.",
    },
  }),
  methods: {
    ...mapActions(['login', 'googleLogin']),
    closeModal() {
      this.$router.push({ name: 'home' });
    },
    async doLogin() {
      if (!this.isFormValid) {
        return; // Stop if the form is invalid
      }

      this.isLoading = true;
      this.serverError = '';

      try {
        await this.login({
          username: this.email,
          password: this.password,
        });

        // Primary fallback: Check for `redirect` query parameter
        const redirectPath = this.$route.query.redirect;
        if (redirectPath) {
          this.$router.push(redirectPath);
          return;
        }

        // Last fallback: Redirect to home
        this.$router.push({ name: 'home' });
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
        this.serverError = error.response?.data?.detail || 'Google login failed.';
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.links {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}
.forgot-password-link,
.sign-up-link {
  color: var(--v-theme-on-surface);
  text-decoration: none;
}
.forgot-password-link:hover,
.sign-up-link:hover {
  text-decoration: underline;
}
</style>