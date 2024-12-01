<template>
    <v-container fluid class="signup-container">
        <v-row justify="center" align="start">
            <v-col cols="12" md="6" lg="4">
                <!-- Logo -->
                <v-row justify="center">
                    <v-img src="@/assets/images/skagen-icon.png" max-width="48" class="ma-12" alt="Skågen Logo"></v-img>
                </v-row>

                <!-- Signup Form Card -->
                <v-card color="surface" outlined class="pa-6">
                    <!-- Header -->
                    <h1 class="form-header mb-6 text-center">Sign up</h1>

                    <!-- Form -->
                    <v-form ref="signupForm" v-model="isFormValid">
                        <!-- Name Field -->
                        <v-text-field label="Full name or nickname" v-model="form.name" variant="outlined" dense
                            required :rules="[rules.required]" class="mb-3"></v-text-field>

                        <!-- Email Field -->
                        <v-text-field label="E-mail address" v-model="form.email" type="email"
                            placeholder="john.doe@mail.com" variant="outlined" dense required
                            :rules="[rules.required, rules.email]" persistent-hint class="mb-3"></v-text-field>

                        <!-- Password Field -->
                        <v-text-field label="Password" v-model="form.password"
                            :type="passwordVisible ? 'text' : 'password'" variant="outlined" dense required
                            :rules="[rules.required, rules.password]" persistent-hint class="mb-3"
                            :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
                            @click:append-inner="togglePasswordVisibility"></v-text-field>

                        <!-- Avatar Selection -->
                        <div class="mb-6">
                            <p class="mb-8 font-weight-bold">Choose or upload (+) an avatar</p>
                            <v-row justify="center" class="avatar-row">
                                <v-col v-for="(avatar, index) in avatars" :key="index" cols="2" class="text-center">
                                    <v-avatar size="48" class="avatar-option"
                                        :class="{ selected: form.avatar === avatar }" @click="form.avatar = avatar">
                                        <img :src="avatar" alt="Avatar" />
                                    </v-avatar>
                                </v-col>
                                <v-col cols="2" class="text-center">
                                    <v-btn icon @click="uploadAvatar">
                                        <v-icon>mdi-plus</v-icon>
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </div>

                        <!-- Submit Button -->
                        <v-row justify="center" class="mb-3">
                            <v-btn color="primary" size="large" class="mb-4" :disabled="!isFormValid"
                                @click="submitForm">
                                Sign up
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
                                Sign in with Google
                            </v-btn>
                        </v-row>

                        <!-- Terms & Privacy -->
                        <v-row justify="center">
                            <p class="terms-text">
                                By signing up, I accept the
                                <router-link to="/about" class="text-link">
                                    Terms & Privacy
                                </router-link>
                                policies.
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
                name: "",
                email: "",
                password: "",
                avatar: "",
            },
            isFormValid: false,
            passwordVisible: false,
            avatars: Array.from({ length: 10 }, (_, i) =>
                require(`@/assets/images/avatar-${i + 1}.png`)
            ),
            rules: {
                required: (value) => !!value || "Required.",
                email: (value) =>
                    /.+@.+\..+/.test(value) || "E-mail must be valid.",
                password: (value) =>
                    value && value.length >= 8 || "Password must be at least 8 characters.",
            },
        };
    },
    methods: {
        togglePasswordVisibility() {
            this.passwordVisible = !this.passwordVisible;
        },
        uploadAvatar() {
            // Logic to upload avatar
        },
        loginWithGoogle() {
            // Logic for Google login
        },
        async submitForm() {
            // Form submission logic
        },
    },
};
</script>

<style scoped>
.signup-container {
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    /* Align to the top on mobile */
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

.terms-text {
    font-size: 14px;
    color: var(--v-subtext-base);
    /* Adjust this for clr--subtext */
}

.avatar-option {
    cursor: pointer;
    border: 2px solid transparent;
    transition: border-color 0.2s ease-in-out;
}

.avatar-option.selected {
    border-color: var(--v-primary-base);
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
    /* White background for OR */
    padding: 0 10px;
    top: -12px;
    color: #666;
    font-size: 14px;
}
</style>