<template>
    <v-dialog v-model="visible" persistent max-width="400">
      <v-form v-model="isFormValid" @submit.prevent="handlePasswordReset">
        <v-card>
          <v-card-title>Set New Password</v-card-title>
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
                <v-alert
                  v-if="infoMessage"
                  type="info"
                  class="mb-4"
                  dismissible
                  @click:close="infoMessage = ''"
                >
                  {{ infoMessage }}
                </v-alert>
                <v-text-field 
                  label="Email" 
                  v-model="email" 
                  autocomplete="off"
                  required
                  :rules="[rules.required, rules.email]"
                ></v-text-field>
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
                type="submit">Reset Password</v-btn>
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
      serverError: '',
      infoMessage: '',
      show: false,
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
    computed: {
        token() {
        return this.$route.query.token || '';
        },
    },
    methods: {
      ...mapActions(['resetPassword']),
      closeModal() {
        this.$router.push({ name: 'home' });
      },
      async handlePasswordReset() {
        if (!this.isFormValid) {
          return; // Stop if the form is invalid
        }
  
        this.isLoading = true;
        this.serverError = '';

        try {
            await this.resetPassword({
                email: this.email,
                newPassword: this.password,
                token: this.token,
            });
            this.infoMessage = 'Password has been reset successfully.';
        } catch (error) {
            if (error.response && error.response.data && error.response.data.detail) {
            this.serverError = error.response.data.detail; // Display error from server
          } else {
            this.serverError = 'An unexpected error occurred. Please try again.';
          }
          console.log(error);
        } finally {
          this.isLoading = false;
        }
      },

      async doLogin() {
  
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
      }
    },
  };
  </script>