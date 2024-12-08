<template>
  <div id="app">
    <img class="mt-lg" alt="Skågen logo" width="100" src="./assets/images/skagen-icon.png" />
    <h1 class="mt-lg">The Birth Of The Skågen!</h1>
    <div class="button-container">
      <!-- Primary Button -->
      <BaseButton variant="primary">Primary Button</BaseButton>

      <!-- Secondary Button -->
      <BaseButton variant="secondary">Secondary Button</BaseButton>

      <!-- Button with Icon -->
      <BaseButton variant="primary">
        <CheckIcon class="icon" /> With Icon
      </BaseButton>

      <!-- Icon-Only Button -->
      <BaseButton variant="primary" :isIconOnly="true">
        <CheckIcon class="icon-only" />
      </BaseButton>

      <!-- Icon-Only Button Without Border -->
      <BaseButton variant="secondary">
        <CheckIcon class="icon-only" />
      </BaseButton>

      <!-- Fully Rounded Button -->
      <BaseButton variant="secondary" :rounded="true">
        Rounded Button
      </BaseButton>

      <!-- Small Button -->
      <BaseButton size="sm">Small Button</BaseButton>

      <!-- Large Button -->
      <BaseButton size="lg">Large Button</BaseButton>
    </div>

    <div class="input-container">
      <h2>Input Fields</h2>

      <!-- Basic Input -->
      <BaseInput placeholder="Enter your name" label="Name" v-model="formData.name" :required="true" />

      <!-- Password Input -->
      <BaseInput type="password" placeholder="Enter your password" v-model="formData.password" />

      <!-- Disabled Input -->
      <BaseInput placeholder="Disabled input" disabled />

      <!-- Custom Input Example -->
      <BaseInput placeholder="Custom placeholder" v-model="formData.custom" :required="true" />
    </div>
  </div>
</template>

<script>
import { CheckIcon } from '@heroicons/vue/24/solid';
import BaseInput from './components/base/BaseInput.vue';
import BaseButton from './components/base/BaseButton.vue';

export default {
  name: 'App',
  components: {
    BaseButton,
    BaseInput,
    CheckIcon,
  },
  data() {
    return {
      formData: {
        name: '',
        password: '',
        custom: '',
      },
    };
  },
};
</script>

<style scoped>
#app {
  text-align: center;
}

.button-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  /* Space between buttons */
  justify-content: center;
  align-items: center;
  margin-top: 24px;
}

.input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
  width: 100%;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

/* TODO: Move to BaseButton.vue */

.icon {
  width: 1em;
  height: 1em;
  vertical-align: middle;
}

.icon-only {
  width: 1.5em;
  /* Slightly larger for standalone icon */
  height: 1.5em;
}
</style>
