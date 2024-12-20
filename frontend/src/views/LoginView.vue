<template>
    <div class="login-view mx-xl my-md">
        <h2 style="margin-bottom: -10px; text-align: center;">Login</h2>
        <form @submit.prevent="goLogin">
            <BaseInput 
                placeholder="Enter your e-mail address" 
                label="E-mail" 
                v-model="email" 
                :errorMessage="errors.email"
                @validate="validateFieldHandler('email')"
            />
            <BaseInput 
                type="password" 
                label="Password" 
                placeholder="Enter your password" 
                v-model="password" 
                :errorMessage="errors.password"
                @validate="validateFieldHandler('password')" />
            <div class="forgot-password-container">
                <a href="#" @click="goForgotPassword">Forgot Password?</a>
            </div>
            <div class="button-container mt-sm">
                <BaseButton 
                    variant="primary" 
                    class="px-xl py-md mt-md" 
                    style="width:200px;"
                    :disabled="!isFormValid">Log in</BaseButton>
            </div>
        </form>
        <p class="or-container">OR</p>
        <div class="button-container">
            <BaseButton variant="secondary" class="px-lg py-md mb-md">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" width="20" height="20">
                    <defs>
                        <clipPath id="clip">
                        <path d="M0 0h20v20H0z" />
                        </clipPath>
                    </defs>
                    <g clip-path="url(#clip)">
                        <!-- Outer Circle -->
                        <path
                        fill="currentColor"
                        d="M19.85 8.27c0.86 4.88-1.99 9.65-6.69 11.22-4.7 1.57-9.84-0.54-12.08-4.96C-1.16 10.11 0.18 4.72 4.22 1.85 8.26-1 13.79-0.48 17.22 3.1l-2.81 2.7c-2.1-2.18-5.47-2.5-7.93-0.75-2.47 1.75-3.28 5.04-1.91 7.73 1.37 2.7 4.5 3.98 7.37 3.03 2.87-0.96 4.6-3.87 4.08-6.85z"
                        />
                        <!-- Horizontal Line -->
                        <path fill="currentColor" d="M10 8.27h9.85v3.5H10z" />
                    </g>
                </svg>
                Log in with Google
            </BaseButton>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex';
import BaseInput from '@/components/base/BaseInput.vue';
import BaseButton from '@/components/base/BaseButton.vue';
import { validateEmail, validatePassword, validateRequired, validateField } from '@/utils/validators';


export default {
    name: 'LoginView',
    components: {
        BaseInput,
        BaseButton
    },
    data() {
        return {
        email: '',
        password: '',
        errors: {
            email: '',
            password: '',
        },
        };
    },
    computed: {
        isFormValid() {
            return (
                !this.errors.email &&
                !this.errors.password &&
                this.email &&
                this.password
            );
        },
    },
    methods: {
        ...mapActions(['login', 'addNotification']),
        validateFieldHandler(field) {
            if (field === 'email') {
                this.errors.email = validateField(this.email, [validateRequired, validateEmail]);
            }
            if (field === 'password') {
                this.errors.password = validateField(this.password, [validateRequired, validatePassword]);
            }
        },
        async goLogin() {
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
                this.addNotification({ message: error.response?.data?.detail[0]?.msg || 'Authentication failed. Please try again.', type: 'error' });
            }
        },
        loginWithGmail() {
            // Emulate OAuth success
            console.log('Logging in with Gmail...');
        },
        goForgotPassword() {
            console.log('Forgot password...');
        },
        goSignUp() {
            console.log('Sign up...');
        }
    },
};
</script>

<style scoped>
.forgot-password-container {
    margin-top: -35px;
    text-align: right;
    font-size: 0.75rem;
}

.button-container {
    text-align: center;
}

.or-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin: 1.5rem 0; 
    position: relative;
}

.or-container::before,
.or-container::after {
    content: '';
    flex: 1;
    height: 1px;
    background-color: #ccc; 
    margin: 0 0.5rem; 
}

.or-container span {
  font-size: 0.875rem; 
  color: #666; 
  background: white; 
  padding: 0 0.5rem;
}
</style>