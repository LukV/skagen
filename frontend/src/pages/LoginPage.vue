<template>
    <v-container fluid class="login-container">
        <v-row justify="center" align="start">
            <v-col cols="12" md="4" lg="3">
                <!-- Logo -->
                <v-row justify="center">
                    <v-img src="@/assets/images/skagen-icon.png" max-width="48" class="ma-12" alt="Skågen Logo"></v-img>
                </v-row>

                <!-- Login Form Card -->
                <v-card color="surface" outlined class="pa-6">
                    <!-- Header -->
                    <h1 class="form-header mb-6 text-center">Log In</h1>

                    <!-- Form -->
                    <v-form ref="loginForm" v-model="isFormValid">
                        <!-- Email Field -->
                        <v-text-field label="E-mail address" v-model="form.email" type="email"
                            placeholder="john.doe@mail.com" variant="outlined" dense required
                            :rules="[rules.required, rules.email]" persistent-hint class="mb-3"></v-text-field>

                        <!-- Password Field -->
                        <v-text-field label="Password" v-model="form.password"
                            :type="passwordVisible ? 'text' : 'password'" variant="outlined" dense required
                            :rules="[rules.required]" persistent-hint class="mb-3"
                            :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
                            @click:append-inner="togglePasswordVisibility"></v-text-field>

                        <!-- Forgot Password Link -->
                        <v-row justify="end" class="mb-4">
                            <router-link to="/auth/forgot-password" class="text-link">
                                Forgot Password?
                            </router-link>
                        </v-row>

                        <!-- Submit Button -->
                        <v-row justify="center" class="mb-3">
                            <v-btn color="primary" size="large" class="mb-4" :disabled="!isFormValid"
                                @click="submitForm">
                                Log In
                            </v-btn>
                        </v-row>

                        <!-- Divider with OR -->
                        <v-row align="center" justify="center" class="divider-or mb-4">
                            <v-divider></v-divider>
                            <span class="or-text">OR</span>
                            <v-divider></v-divider>
                        </v-row>

                        <!-- Google Login -->
                        <v-row justify="center" class="mb-3">
                            <v-btn outlined size="large" class="google-login ma-4" @click="loginWithGoogle">
                                <v-icon left>mdi-google</v-icon>
                                Log in with Google
                            </v-btn>
                        </v-row>

                        <!-- Sign Up Link -->
                        <v-row justify="center">
                            <p class="signup-text">
                                Don't have an account?
                                <router-link to="/auth/signup" class="text-link">
                                    Sign Up
                                </router-link>
                            </p>
                        </v-row>
                    </v-form>
                </v-card>

                <!-- Navigation -->
                <v-row justify="center" class="mt-4">
                    <router-link to="/" class="text-link">
                        <v-icon left class="mr-1">mdi-arrow-left</v-icon>
                        Back to Skågen Home
                    </router-link>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data() {
        return {
            form: {
                email: "",
                password: "",
            },
            isFormValid: false,
            passwordVisible: false,
            rules: {
                required: (value) => !!value || "Required.",
                email: (value) =>
                    /.+@.+\..+/.test(value) || "E-mail must be valid.",
            },
        };
    },
    methods: {
        togglePasswordVisibility() {
            this.passwordVisible = !this.passwordVisible;
        },
        loginWithGoogle() {
            // Logic for Google login
        },
        submitForm() {
            if (this.isFormValid) {
                // Form submission logic
            }
        },
    },
};
</script>

<style scoped>
.login-container {
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    background-color: #f9f9f9;
}

.v-card {
    border-radius: 12px;
}

.form-header {
    font-size: 24px;
    font-weight: bold;
    color: var(--v-primary-base);
}

.signup-text {
    font-size: 14px;
    color: var(--v-subtext-base);
}

.text-link {
    text-decoration: underline;
    color: var(--v-primary-base);
    cursor: pointer;
    font-size: 14px;
}

.google-login {
    text-transform: none;
    width: auto;
    padding: 10px 20px;
}

.divider-or {
    position: relative;
    width: 100%;
}

.divider-or .or-text {
    position: absolute;
    background-color: #fff;
    padding: 0 10px;
    top: -12px;
    color: #666;
    font-size: 14px;
}
</style>