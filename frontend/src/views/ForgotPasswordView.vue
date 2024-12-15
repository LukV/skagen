<template>
    <div class="forgot-password-view">
      <h2>Forgot Password</h2>
      <p>Please enter your email below</p>
      <input v-model="email" placeholder="Email" />
      <button @click="resetPassword">Reset Password</button>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useStore } from 'vuex';
  
  export default {
    name: 'ForgotPasswordView',
    setup() {
      const store = useStore();
      const email = ref('');
  
      function resetPassword() {
        // If calling an API, do so here
        alert(`Reset link sent to ${email.value}`);
        store.dispatch('closeModal');
      }
  
      return {
        email,
        resetPassword
      };
    }
  };
  </script>