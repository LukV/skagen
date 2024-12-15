<template>
  <div class="sign-up-view mx-xl my-md">
    <h2 style="margin-bottom: -10px; text-align: center;">Sign Up</h2>
    <form @submit.prevent="handleSignUp">
      <!-- Name -->
      <BaseInput label="Name" placeholder="Enter your name" v-model="name" :required="true" />

      <!-- E-mail -->
      <BaseInput label="E-mail" placeholder="Enter your e-mail address" v-model="email" :required="true" />

      <!-- Password -->
      <BaseInput label="Password" type="password" placeholder="Enter your password" v-model="password"
        :required="true" />

      <!-- Avatar Selection -->
      <div class="avatar-selection-container">
        <p>Select your avatar:</p>
        <div class="avatar-grid">
          <!-- Existing avatar loop -->
          <div v-for="avatarIndex in 10" :key="avatarIndex" class="avatar-item"
            :class="{ selected: selectedAvatar === avatarIndex }" @click="selectedAvatar = avatarIndex">
            <img :src="require(`@/assets/images/avatar-${avatarIndex}.png`)" :alt="'Avatar ' + avatarIndex" />
          </div>

          <!-- Plus icon item at the end -->
          <button
            class="avatar-item add-avatar mt-sm"
            @click="onPlusClick"
            aria-label="Add new avatar"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              width="24"
              height="24"
              fill="white"
            >
              <path
                fill-rule="evenodd"
                d="M12 4.75a.75.75 0 01.75.75v5h5a.75.75 0 110 1.5h-5v5a.75.75 0 01-1.5 0v-5h-5a.75.75 0 110-1.5h5v-5A.75.75 0 0112 4.75z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>

      <div class="button-container mt-sm">
        <BaseButton variant="primary" class="px-xl py-md mt-md" style="width:200px;">
          Sign Up
        </BaseButton>
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
            <path fill="currentColor"
              d="M19.85 8.27c0.86 4.88-1.99 9.65-6.69 11.22-4.7 1.57-9.84-0.54-12.08-4.96C-1.16 10.11 0.18 4.72 4.22 1.85 8.26-1 13.79-0.48 17.22 3.1l-2.81 2.7c-2.1-2.18-5.47-2.5-7.93-0.75-2.47 1.75-3.28 5.04-1.91 7.73 1.37 2.7 4.5 3.98 7.37 3.03 2.87-0.96 4.6-3.87 4.08-6.85z" />
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
  name: 'SignUpView',
  components: {
    BaseInput,
    BaseButton
  },
  setup() {
    const store = useStore();
    const name = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const selectedAvatar = ref(null);

    function handleSignUp() {
      // Simple validation
      if (password.value !== confirmPassword.value) {
        alert('Passwords do not match.');
        return;
      }

      // Dispatch signup with relevant data
      store.dispatch('signup', {
        name: name.value,
        email: email.value,
        password: password.value,
        avatar: selectedAvatar.value
      });
    }

    return {
      name,
      email,
      password,
      confirmPassword,
      selectedAvatar,
      handleSignUp
    };
  }
};
</script>

<style scoped>
.sign-up-view {
  /* Basic spacing similar to LoginView */
  margin-top: 2rem;
}

.avatar-selection-container {
  margin-top: 1rem;
}

.avatar-grid {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(60px, 1fr));
  justify-items: center;
  margin-top: 0.5rem;
}

.avatar-item {
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 50%;
  padding: 0.25rem;
  transition: border-color 0.2s;
}

.avatar-item.selected {
  border-color: #007bff;
}

.avatar-item img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

/* Style for the "+" button */
.add-avatar {
  background-color: var(--color-primary, #007bff); 
  border: 8px solid var(--color-primary-lighter, #007bff); 
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.add-avatar:hover {
  background-color: var(--primary-color-hover, #0056b3); /* Darker primary for hover */
}

.add-avatar:focus {
  outline: 2px solid var(--primary-color, #007bff); /* Accessible focus style */
  outline-offset: 2px;
}

.button-container {
  text-align: center;
  margin-top: 1rem;
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