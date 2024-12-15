<template>
    <div class="login-view mx-xl my-md">
        <h2 style="margin-bottom: -10px; text-align: center;">Login</h2>
        <form @submit.prevent="handleSubmit">
            <BaseInput placeholder="Enter your e-mail address" label="E-mail" v-model="email" :required="true" />
            <BaseInput type="password" label="Password" placeholder="Enter your password" v-model="password" :required="true" />
            <div class="forgot-password-container">
                <a href="#" @click="goForgotPassword">Forgot Password?</a>
            </div>
            <div class="button-container mt-sm">
                <BaseButton variant="primary" class="px-xl py-md mt-md" style="width:200px;">Log in</BaseButton>
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
import { ref } from 'vue';
import { useStore } from 'vuex';
import BaseInput from '@/components/base/BaseInput.vue';
import BaseButton from '@/components/base/BaseButton.vue';


export default {
    name: 'LoginView',
    components: {
        BaseInput,
        BaseButton
    },
    setup() {
        const store = useStore();
        const email = ref('');
        const password = ref('');

        function handleSubmit() {
            // Normally call an API, etc. 
            store.dispatch('login', email.value);  // pass email if desired
        }

        function loginWithGmail() {
            // Emulate OAuth success
            store.dispatch('login', 'Gmail User');
        }

        function goForgotPassword() {
            store.dispatch('openAuthModal', 'forgotPassword');
        }
        function goSignUp() {
            store.dispatch('openAuthModal', 'signUp');
        }

        return {
            email,
            password,
            handleSubmit,
            loginWithGmail,
            goForgotPassword,
            goSignUp
        };
    }
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
  margin: 1.5rem 0; /* Adjust spacing as needed */
  position: relative;
}

.or-container::before,
.or-container::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: #ccc; /* Adjust the line color */
  margin: 0 0.5rem; /* Spacing between the line and text */
}

.or-container span {
  font-size: 0.875rem; /* Adjust font size */
  color: #666; /* Adjust text color */
  background: white; /* Matches background color for the "cut-out" effect */
  padding: 0 0.5rem; /* Add spacing around the text */
}
</style>