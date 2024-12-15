<template>
  <div class="app-container">
    <transition name="slide-sidebar">
      <AppSidebar
        v-if="!isMobile || sidebarOpen"
        :collapsed="isCollapsed"
        class="app-sidebar"
        @toggle-collapse="toggleSidebar"
      />
    </transition>

    <div class="right-col">
      <AppHeader />
      <main class="main-content">
        <router-view name="main" />
      </main>
    </div>

    <!-- Universal hModal: conditionally shows login/signUp/forgotPassword -->
    <UniversalModal :isMobile="isMobile">
      <router-view name="modal" />
    </UniversalModal>
  </div>
</template>

<script>
import { ref, onBeforeUnmount } from 'vue';
import AppHeader from './components/layout/AppHeader.vue';
import AppSidebar from './components/layout/AppSidebar.vue';
import UniversalModal from './components/layout/UniversalModal.vue';

export default {
  name: 'App',
  components: { AppHeader, AppSidebar, UniversalModal },
  setup() {
    const sidebarOpen = ref(false);
    const isCollapsed = ref(false);

    // Detect mobile
    const isMobile = ref(window.innerWidth <= 600);
    function handleResize() {
      isMobile.value = window.innerWidth <= 600;
      if (!isMobile.value) {
        sidebarOpen.value = false;
      }
    }
    window.addEventListener('resize', handleResize);
    onBeforeUnmount(() => {
      window.removeEventListener('resize', handleResize);
    });

    function toggleSidebarOpen() {
      sidebarOpen.value = !sidebarOpen.value;
    }
    function toggleSidebar() {
      isCollapsed.value = !isCollapsed.value;
    }

    return {
      sidebarOpen,
      isCollapsed,
      isMobile,
      toggleSidebarOpen,
      toggleSidebar
    };
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

/* Mobile Overlay */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  background-color: var(--color-background-darker, #fff);
}

.mobile-overlay-header {
  display: flex;
  justify-content: right;
  padding: var(--spacing-md);
  position: relative;
  background-color: var(--color-background, #fff);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.mobile-overlay-close {
  position: absolute;
  right: var(--spacing-md);
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm);
}

.mobile-overlay-content {
  flex: 1;
  padding: var(--spacing-md);
}

/* Auth section in mobile overlay */
.mobile-auth {
  margin-top: auto; /* Push to the bottom */
  padding: var(--spacing-lg);
}

/* Example styling for user overlay */
.user-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.user-overlay-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.app-sidebar {
  flex: 0 0 auto;
  transition: width 0.3s ease;
  width: 200px;
}

.app-sidebar.collapsed {
  width: 50px;
}

.right-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
}

/* Overlay for mobile */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

/* On mobile hide sidebar by default */
@media (max-width: 600px) {
  .app-sidebar {
    display: none;
  }

  /* When sidebarOpen is true, slide it in */
  .app-sidebar.slide-sidebar-enter-from,
  .app-sidebar.slide-sidebar-leave-to {
    transform: translateX(-100%);
  }
  .app-sidebar.slide-sidebar-enter-to,
  .app-sidebar.slide-sidebar-leave-from {
    transform: translateX(0);
  }
}

/* On desktop, no transform needed. Just collapse/expand width. */
</style>