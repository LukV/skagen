<template>
    <v-dialog v-model="visible" persistent max-width="400">
        <v-form v-model="isFormValid" @submit.prevent="handlePasswordReset">
            <v-card>
                <v-card-title>Forgot password?</v-card-title>
                <v-card-text>
                    <v-alert v-if="serverError" type="error" class="mb-4" dismissible @click:close="serverError = ''">
                        {{ serverError }}
                    </v-alert>
                    <v-alert v-if="infoMessage" type="info" class="mb-4" dismissible @click:close="infoMessage = ''">
                        {{ infoMessage }}
                    </v-alert>
                    <v-text-field label="Email" v-model="email" autocomplete="off" required
                        :rules="[rules.required, rules.email]"></v-text-field>
                </v-card-text>
                <v-card-actions>
                    <v-btn text @click="closeModal">Cancel</v-btn>
                    <v-btn :loading="isLoading" color="primary" type="submit">Send Reset Email</v-btn>
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
        serverError: '',
        infoMessage: '',
        rules: {
            required: v => !!v || 'Required.',
            email: (v) =>
                /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || "Invalid email.",
        },
    }),
    methods: {
        ...mapActions(['requestPasswordReset']),
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
                await this.requestPasswordReset({ email: this.email });
                this.infoMessage = 'Password reset email sent. Please check your inbox.';
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