<template>
    <div v-if="showModal" class="modal-backdrop">
      
      <!-- Sticky Header with Close Button -->
      <header class="modal-header">
        <BaseButton variant="text" @click="closeModal">
          <XMarkIcon class="chevron-icon icon-lg" />
        </BaseButton>
      </header>
  
      <!-- Scrollable Body -->
      <div class="modal-body">
        <!-- Centered container for desktop screens with max-width=600px -->
        <div class="modal-inner">
          <div class="logo mt-lg">
            <img v-if="!collapsed" src="@/assets/images/skagen-icon.png" alt="Skågen Icon" class="brand-icon" />
          </div>
  
          <!-- Actual auth content (SignUpView, LoginView, etc.) goes here -->
          <slot @close-modal="closeModal" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { computed, onMounted, onUnmounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { XMarkIcon } from '@heroicons/vue/24/solid';
  import BaseButton from '../base/BaseButton.vue';
  
  export default {
      name: 'UniversalModal',
      components: { 
          BaseButton,
          XMarkIcon
      },
      props: {
          isMobile: { type: Boolean, default: false },
          collapsed: { type: Boolean, default: false }
      },
      setup() {
          const route = useRoute();
          const router = useRouter();
  
          const showModal = computed(() => route.meta.universalModal);
  
          function closeModal() {
            if (window.history.length > 1) {
              router.back();
            } else {
              router.push({ name: 'home' });
            }
          }
  
          // Close modal on ESC keypress
          function handleKeydown(event) {
              if (event.key === 'Escape') {
                  closeModal();
              }
          }
  
          onMounted(() => {
              window.addEventListener('keydown', handleKeydown);
          });
  
          onUnmounted(() => {
              window.removeEventListener('keydown', handleKeydown);
          });
  
          return {
              showModal,
              closeModal
          };
      }
  };
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--color-background-darkest, #fafafa);
    z-index: 2000;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }
  
  .modal-header {
    position: sticky;
    top: 0;
    padding: 0.5rem 1rem;
    text-align: right;
    z-index: 10;
  }
  
  .modal-inner {
    width: 100%;
  }
  
  .logo {
    text-align: center;
  }
  
  .brand-icon {
    width: 40px;
    height: 40px;
  }
  
  @media (min-width: 600px) {
    .modal-inner {
      max-width: 600px;
      margin: 2rem auto;
      background: #fafafa;
      padding: 2rem;
      border-radius: 4px;
    }
  }
  </style>